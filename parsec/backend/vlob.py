# Parsec Cloud (https://parsec.cloud) Copyright (c) AGPLv3 2019 Scille SAS

from typing import List, Tuple, Dict, Optional
from uuid import UUID
import pendulum

from parsec.types import DeviceID, OrganizationID
from parsec.api.protocole import (
    vlob_create_serializer,
    vlob_read_serializer,
    vlob_update_serializer,
    vlob_group_check_serializer,
    vlob_poll_changes_serializer,
    vlob_maintenance_get_reencryption_batch_serializer,
    vlob_maintenance_save_reencryption_batch_serializer,
)
from parsec.backend.utils import catch_protocole_errors
from parsec.crypto import timestamps_in_the_ballpark


class VlobError(Exception):
    pass


class VlobAccessError(VlobError):
    pass


class VlobVersionError(VlobError):
    pass


class VlobNotFoundError(VlobError):
    pass


class VlobAlreadyExistsError(VlobError):
    pass


class VlobEncryptionRevisionError(VlobError):
    pass


class VlobInMaintenanceError(VlobError):
    pass


class VlobMaintenanceError(VlobError):
    pass


class BaseVlobComponent:
    @catch_protocole_errors
    async def api_vlob_create(self, client_ctx, msg):
        msg = vlob_create_serializer.req_load(msg)

        now = pendulum.now()
        if not timestamps_in_the_ballpark(msg["timestamp"], now):
            return {"status": "bad_timestamp", "reason": f"Timestamp is out of date."}

        try:
            await self.create(client_ctx.organization_id, client_ctx.device_id, **msg)

        except VlobAlreadyExistsError as exc:
            return vlob_create_serializer.rep_dump({"status": "already_exists", "reason": str(exc)})

        except VlobAccessError:
            return vlob_create_serializer.rep_dump({"status": "not_allowed"})

        except VlobEncryptionRevisionError:
            return vlob_create_serializer.rep_dump({"status": "bad_encryption_revision"})

        except VlobInMaintenanceError:
            return vlob_create_serializer.rep_dump({"status": "in_maintenance"})

        return vlob_create_serializer.rep_dump({"status": "ok"})

    @catch_protocole_errors
    async def api_vlob_read(self, client_ctx, msg):
        msg = vlob_read_serializer.req_load(msg)

        try:
            version, blob, author, created_on = await self.read(
                client_ctx.organization_id, client_ctx.device_id, **msg
            )

        except VlobNotFoundError as exc:
            return vlob_read_serializer.rep_dump({"status": "not_found", "reason": str(exc)})

        except VlobAccessError:
            return vlob_read_serializer.rep_dump({"status": "not_allowed"})

        except VlobVersionError:
            return vlob_read_serializer.rep_dump({"status": "bad_version"})

        except VlobEncryptionRevisionError:
            return vlob_create_serializer.rep_dump({"status": "bad_encryption_revision"})

        except VlobInMaintenanceError:
            return vlob_read_serializer.rep_dump({"status": "in_maintenance"})

        return vlob_read_serializer.rep_dump(
            {
                "status": "ok",
                "blob": blob,
                "version": version,
                "author": author,
                "timestamp": created_on,
            }
        )

    @catch_protocole_errors
    async def api_vlob_update(self, client_ctx, msg):
        msg = vlob_update_serializer.req_load(msg)

        now = pendulum.now()
        if not timestamps_in_the_ballpark(msg["timestamp"], now):
            return {"status": "bad_timestamp", "reason": f"Timestamp is out of date."}

        try:
            await self.update(client_ctx.organization_id, client_ctx.device_id, **msg)

        except VlobNotFoundError as exc:
            return vlob_update_serializer.rep_dump({"status": "not_found", "reason": str(exc)})

        except VlobAccessError:
            return vlob_update_serializer.rep_dump({"status": "not_allowed"})

        except VlobVersionError:
            return vlob_update_serializer.rep_dump({"status": "bad_version"})

        except VlobEncryptionRevisionError:
            return vlob_create_serializer.rep_dump({"status": "bad_encryption_revision"})

        except VlobInMaintenanceError:
            return vlob_update_serializer.rep_dump({"status": "in_maintenance"})

        return vlob_update_serializer.rep_dump({"status": "ok"})

    @catch_protocole_errors
    async def api_vlob_group_check(self, client_ctx, msg):
        msg = vlob_group_check_serializer.req_load(msg)
        try:
            changed = await self.group_check(
                client_ctx.organization_id, client_ctx.device_id, msg["to_check"]
            )

        except VlobInMaintenanceError:
            return vlob_group_check_serializer.rep_dump({"status": "in_maintenance"})

        return vlob_group_check_serializer.rep_dump({"status": "ok", "changed": changed})

    @catch_protocole_errors
    async def api_vlob_poll_changes(self, client_ctx, msg):
        msg = vlob_poll_changes_serializer.req_load(msg)

        # TODO: raise error if too many events since offset ?
        try:
            checkpoint, changes = await self.poll_changes(
                client_ctx.organization_id,
                client_ctx.device_id,
                msg["realm_id"],
                msg["last_checkpoint"],
            )

        except VlobAccessError:
            return vlob_poll_changes_serializer.rep_dump({"status": "not_allowed"})

        except VlobNotFoundError as exc:
            return vlob_poll_changes_serializer.rep_dump(
                {"status": "not_found", "reason": str(exc)}
            )

        except VlobInMaintenanceError:
            return vlob_poll_changes_serializer.rep_dump({"status": "in_maintenance"})

        return vlob_poll_changes_serializer.rep_dump(
            {"status": "ok", "current_checkpoint": checkpoint, "changes": changes}
        )

    @catch_protocole_errors
    async def api_vlob_maintenance_get_reencryption_batch(self, client_ctx, msg):
        msg = vlob_maintenance_get_reencryption_batch_serializer.req_load(msg)

        try:
            batch = await self.maintenance_get_reencryption_batch(
                client_ctx.organization_id, client_ctx.device_id, **msg
            )

        except VlobAccessError:
            return vlob_maintenance_get_reencryption_batch_serializer.rep_dump(
                {"status": "not_allowed"}
            )

        except VlobNotFoundError as exc:
            return vlob_maintenance_get_reencryption_batch_serializer.rep_dump(
                {"status": "not_found", "reason": str(exc)}
            )

        except VlobEncryptionRevisionError:
            return vlob_create_serializer.rep_dump({"status": "bad_encryption_revision"})

        except VlobMaintenanceError as exc:
            return vlob_maintenance_get_reencryption_batch_serializer.rep_dump(
                {"status": "maintenance_error", "reason": str(exc)}
            )

        return vlob_maintenance_get_reencryption_batch_serializer.rep_dump(
            {
                "status": "ok",
                "batch": [
                    {"vlob_id": vlob_id, "version": version, "data": data}
                    for vlob_id, version, data in batch
                ],
            }
        )

    @catch_protocole_errors
    async def api_vlob_maintenance_save_reencryption_batch(self, client_ctx, msg):
        msg = vlob_maintenance_save_reencryption_batch_serializer.req_load(msg)

        try:
            await self.maintenance_save_reencryption_batch(
                client_ctx.organization_id,
                client_ctx.device_id,
                realm_id=msg["realm_id"],
                encryption_revision=msg["encryption_revision"],
                batch=[(x["vlob_id"], x["version"], x["data"]) for x in msg["batch"]],
            )

        except VlobAccessError:
            return vlob_maintenance_save_reencryption_batch_serializer.rep_dump(
                {"status": "not_allowed"}
            )

        except VlobNotFoundError as exc:
            return vlob_maintenance_save_reencryption_batch_serializer.rep_dump(
                {"status": "not_found", "reason": str(exc)}
            )

        except VlobEncryptionRevisionError:
            return vlob_create_serializer.rep_dump({"status": "bad_encryption_revision"})

        except VlobMaintenanceError as exc:
            return vlob_maintenance_save_reencryption_batch_serializer.rep_dump(
                {"status": "maintenance_error", "reason": str(exc)}
            )

        return vlob_maintenance_save_reencryption_batch_serializer.rep_dump({"status": "ok"})

    async def create(
        self,
        organization_id: OrganizationID,
        author: DeviceID,
        vlob_id: UUID,
        realm_id: UUID,
        timestamp: pendulum.Pendulum,
        blob: bytes,
        encryption_revision: Optional[int] = None,
    ) -> None:
        """
        Raises:
            VlobAlreadyExistsError
            VlobEncryptionRevisionError: if encryption_revision mismatch
            VlobInMaintenanceError
        """
        raise NotImplementedError()

    async def read(
        self,
        organization_id: OrganizationID,
        author: DeviceID,
        vlob_id: UUID,
        version: Optional[int] = None,
        encryption_revision: Optional[int] = None,
    ) -> Tuple[int, bytes, DeviceID, pendulum.Pendulum]:
        """
        Raises:
            VlobAccessError
            VlobVersionError
            VlobNotFoundError
            VlobEncryptionRevisionError: if encryption_revision mismatch
            VlobInMaintenanceError
        """
        raise NotImplementedError()

    async def update(
        self,
        organization_id: OrganizationID,
        author: DeviceID,
        vlob_id: UUID,
        version: int,
        blob: bytes,
        encryption_revision: Optional[int] = None,
    ) -> None:
        """
        Raises:
            VlobAccessError
            VlobVersionError
            VlobNotFoundError
            VlobEncryptionRevisionError: if encryption_revision mismatch
            VlobInMaintenanceError
        """
        raise NotImplementedError()

    async def group_check(
        self, organization_id: OrganizationID, author: DeviceID, to_check: List[dict]
    ) -> List[dict]:
        """
        Raises: Nothing !
        """
        raise NotImplementedError()

    async def poll_changes(
        self, organization_id: OrganizationID, author: DeviceID, realm_id: UUID, checkpoint: int
    ) -> Tuple[int, Dict[UUID, int]]:
        """
        Raises:
            VlobInMaintenanceError
            VlobNotFoundError
            VlobAccessError
        """
        raise NotImplementedError()

    async def maintenance_get_reencryption_batch(
        self,
        organization_id: OrganizationID,
        author: DeviceID,
        realm_id: UUID,
        encryption_revision: int,
    ) -> List[Tuple[UUID, int, bytes]]:
        """
        Raises:
            VlobNotFoundError
            VlobAccessError
            VlobMaintenanceError: not in maintenance or bad encryption_revision
        """
        raise NotImplementedError()

    async def maintenance_save_reencryption_batch(
        self,
        organization_id: OrganizationID,
        author: DeviceID,
        realm_id: UUID,
        encryption_revision: int,
        batch: List[Tuple[UUID, int, bytes]],
    ) -> None:
        """
        Raises:
            VlobNotFoundError
            VlobAccessError
            VlobMaintenanceError: not in maintenance or bad encryption_revision
        """
        raise NotImplementedError()
