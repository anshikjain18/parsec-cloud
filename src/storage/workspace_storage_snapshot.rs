// Parsec Cloud (https://parsec.cloud) Copyright (c) BUSL-1.1 (eventually AGPL-3.0) 2016-present Scille SAS

use libparsec::core_fs::{FSError, FSResult};
use pyo3::prelude::{pyclass, pymethods, IntoPy, PyObject, PyResult, Python};

use std::{
    collections::HashMap,
    sync::{
        atomic::{AtomicU32, Ordering},
        Arc, Mutex,
    },
};

use super::{
    file_or_folder_manifest_from_py_object, file_or_folder_manifest_into_py_object,
    fs_to_python_error, workspace_storage::WorkspaceStorage,
};
use crate::{
    data::LocalFileManifest,
    ids::{BlockID, ChunkID, EntryID},
    local_device::LocalDevice,
    regex::Regex,
    runtime::FutureIntoCoroutine,
    time::DateTime,
};

#[pyclass]
#[derive(Clone)]
pub(crate) struct WorkspaceStorageSnapshot {
    workspace_storage: WorkspaceStorage,
    cache: Arc<
        Mutex<HashMap<libparsec::types::EntryID, libparsec::core_fs::LocalFileOrFolderManifest>>,
    >,
    open_fds: Arc<Mutex<HashMap<u32, libparsec::types::EntryID>>>,
    fd_counter: Arc<AtomicU32>,
}

impl From<WorkspaceStorage> for WorkspaceStorageSnapshot {
    fn from(workspace_storage: WorkspaceStorage) -> Self {
        WorkspaceStorageSnapshot::new(workspace_storage)
    }
}

impl WorkspaceStorageSnapshot {
    fn new(workspace_storage: WorkspaceStorage) -> Self {
        Self {
            workspace_storage,
            cache: Arc::new(Mutex::new(HashMap::default())),
            fd_counter: Arc::new(AtomicU32::new(0)),
            open_fds: Arc::new(Mutex::new(HashMap::default())),
        }
    }
}

impl WorkspaceStorageSnapshot {
    fn get_next_fd(&self) -> u32 {
        self.fd_counter.fetch_add(1, Ordering::SeqCst)
    }

    fn get_manifest_internal(
        &self,
        entry_id: &libparsec::types::EntryID,
    ) -> FSResult<libparsec::core_fs::LocalFileOrFolderManifest> {
        self.cache
            .lock()
            .expect("Mutex is poisoned")
            .get(entry_id)
            .cloned()
            .ok_or(FSError::LocalMiss(**entry_id))
    }
}

#[pymethods]
impl WorkspaceStorageSnapshot {
    fn create_file_descriptor(&self, manifest: LocalFileManifest) -> u32 {
        let manifest = manifest.0;
        let manifest_id = manifest.base.id;
        let fd = self.get_next_fd();
        self.open_fds
            .lock()
            .expect("Mutex is poisoned")
            .insert(fd, manifest_id);
        fd
    }

    fn load_file_descriptor(&self, py: Python<'_>, fd: u32) -> FutureIntoCoroutine {
        let manifest = self
            .open_fds
            .lock()
            .expect("Mutex is poisoned")
            .get(&fd)
            .ok_or(FSError::InvalidFileDescriptor(
                libparsec::types::FileDescriptor(fd),
            ))
            .and_then(|entry_id| {
                self.get_manifest_internal(entry_id)
                    .map(|manifest| (entry_id, manifest))
            })
            .and_then(|(entry_id, manifest)| match manifest {
                libparsec::core_fs::LocalFileOrFolderManifest::File(manifest) => Ok(manifest),
                _ => Err(FSError::LocalMiss(**entry_id)),
            })
            .map(LocalFileManifest)
            .map(|manifest| manifest.into_py(py))
            .map_err(fs_to_python_error);

        FutureIntoCoroutine::ready(manifest)
    }

    fn remove_file_descriptor(&self, fd: u32) -> PyResult<()> {
        self.open_fds
            .lock()
            .expect("Mutex is poisoned")
            .remove(&fd)
            .ok_or(FSError::InvalidFileDescriptor(
                libparsec::types::FileDescriptor(fd),
            ))
            .map(|_| ())
            .map_err(fs_to_python_error)
    }

    /// Return a chunk identified by `chunk_id`.
    /// Will look for the chunk in the [libparsec::core_fs::storage::ChunkStorage] & [libparsec::core_fs::storage::BlockStorage].
    fn get_chunk(&self, chunk_id: ChunkID) -> PyResult<FutureIntoCoroutine> {
        self.workspace_storage.get_chunk(chunk_id)
    }

    fn get_manifest(&self, entry_id: EntryID) -> FutureIntoCoroutine {
        let entry_id = entry_id.0;

        let res = self
            .get_manifest_internal(&entry_id)
            .map(file_or_folder_manifest_into_py_object)
            .map_err(fs_to_python_error);

        FutureIntoCoroutine::ready(res)
    }

    fn set_manifest(
        &self,
        py: Python,
        entry_id: EntryID,
        manifest: PyObject,
    ) -> PyResult<FutureIntoCoroutine> {
        let manifest = file_or_folder_manifest_from_py_object(py, &manifest)?;
        let entry_id = entry_id.0;

        let res = if manifest.need_sync() {
            Err(fs_to_python_error(FSError::WorkspaceStorageTimestamped))
        } else {
            // Currently we don't check if a manifest is locked.
            // Since we rely for the moment on the python locking system for the manifests.
            self.cache
                .lock()
                .expect("Mutex is poisoned")
                .insert(entry_id, manifest);
            Ok(py.None())
        };

        let fut = FutureIntoCoroutine::ready(res);

        Ok(fut)
    }

    fn get_prevent_sync_pattern(&self) -> PyResult<Regex> {
        self.workspace_storage.get_prevent_sync_pattern()
    }

    fn get_prevent_sync_pattern_fully_applied(&self) -> PyResult<bool> {
        self.workspace_storage
            .get_prevent_sync_pattern_fully_applied()
    }

    fn set_clean_block(&self, block_id: BlockID, block: &[u8]) -> PyResult<FutureIntoCoroutine> {
        self.workspace_storage.set_clean_block(block_id, block)
    }

    fn clear_clean_block(&self, block_id: BlockID) -> PyResult<FutureIntoCoroutine> {
        self.workspace_storage.clear_clean_block(block_id)
    }

    fn get_dirty_block(&self, block_id: BlockID) -> PyResult<FutureIntoCoroutine> {
        self.workspace_storage.get_dirty_block(block_id)
    }

    fn to_timestamp(&self) -> Self {
        Self::new(self.workspace_storage.clone())
    }

    /// Clear the local manifest cache
    fn clear_local_cache(&self, py: Python<'_>) -> FutureIntoCoroutine {
        self.cache.lock().expect("Mutex is poisoned").clear();

        FutureIntoCoroutine::ready(Ok(py.None()))
    }

    fn is_block_remanent(&self) -> PyResult<bool> {
        self.workspace_storage.is_block_remanent()
    }

    fn enable_block_remanence(&self) -> PyResult<FutureIntoCoroutine> {
        self.workspace_storage.enable_block_remanence()
    }

    fn disable_block_remanence(&self) -> PyResult<FutureIntoCoroutine> {
        self.workspace_storage.disable_block_remanence()
    }

    fn clear_unreferenced_blocks(
        &self,
        block_ids: Vec<BlockID>,
        not_accessed_after: DateTime,
    ) -> PyResult<FutureIntoCoroutine> {
        self.workspace_storage
            .clear_unreferenced_blocks(block_ids, not_accessed_after)
    }

    fn remove_clean_blocks(&self, block_ids: Vec<BlockID>) -> PyResult<FutureIntoCoroutine> {
        self.workspace_storage.remove_clean_blocks(block_ids)
    }

    #[getter]
    fn device(&self) -> PyResult<LocalDevice> {
        self.workspace_storage.device()
    }

    #[getter]
    fn workspace_id(&self) -> PyResult<EntryID> {
        self.workspace_storage.workspace_id()
    }

    fn is_clean_block(&self, block_id: BlockID) -> PyResult<FutureIntoCoroutine> {
        self.workspace_storage.is_clean_block(block_id)
    }
}