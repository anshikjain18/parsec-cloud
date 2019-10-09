# Parsec Cloud (https://parsec.cloud) Copyright (c) AGPLv3 2019 Scille SAS

import trio

from structlog import get_logger

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from parsec.core import logged_core_factory
from parsec.core.local_device import (
    LocalDeviceError,
    load_device_with_password,
    load_device_with_pkcs11,
)
from parsec.core.mountpoint import MountpointConfigurationError, MountpointDriverCrash
from parsec.core.backend_connection import (
    BackendHandshakeError,
    BackendHandshakeAPIVersionError,
    BackendDeviceRevokedError,
)

from parsec.core.gui.trio_thread import QtToTrioJobScheduler, ThreadSafeQtSignal
from parsec.core.gui.custom_dialogs import show_error
from parsec.core.gui.lang import translate as _
from parsec.core.gui.login_widget import LoginWidget
from parsec.core.gui.central_widget import CentralWidget


logger = get_logger()


async def _do_run_core(config, device, event_bus, qt_on_ready):
    # Quick fix to avoid MultiError<Cancelled, ...> exception bubbling up
    # TODO: replace this by a proper generic MultiError handling
    with trio.MultiError.catch(lambda exc: None if isinstance(exc, trio.Cancelled) else exc):
        async with logged_core_factory(config=config, device=device, event_bus=None) as core:
            if config.mountpoint_enabled:
                await core.mountpoint_manager.mount_all()
            # Create our own job scheduler allows us to cancel all pending
            # jobs depending on us when we logout
            core_jobs_ctx = QtToTrioJobScheduler()
            async with trio.open_nursery() as nursery:
                await nursery.start(core_jobs_ctx._start)
                qt_on_ready.emit(core, core_jobs_ctx)


class InstanceWidget(QWidget):
    run_core_success = pyqtSignal()
    run_core_error = pyqtSignal()
    run_core_ready = pyqtSignal(object, object)
    logged_in = pyqtSignal()
    logged_out = pyqtSignal()
    state_changed = pyqtSignal(QWidget, str)

    def __init__(self, jobs_ctx, event_bus, config, **kwargs):
        super().__init__(**kwargs)
        self.jobs_ctx = jobs_ctx
        self.event_bus = event_bus
        self.config = config

        self.core = None
        self.core_jobs_ctx = None
        self.running_core_job = None

        self.run_core_success.connect(self.on_core_run_done)
        self.run_core_error.connect(self.on_core_run_error)
        self.run_core_ready.connect(self.on_run_core_ready)
        self.logged_in.connect(self.on_logged_in)
        self.logged_out.connect(self.on_logged_out)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.show_login_widget()

    @pyqtSlot(object, object)
    def _core_ready(self, core, core_jobs_ctx):
        self.run_core_ready.emit(core, core_jobs_ctx)

    @property
    def current_device(self):
        if self.core:
            return self.core.device
        return None

    @property
    def is_logged_in(self):
        return self.running_core_job is not None

    def start_core(self, device):
        assert not self.running_core_job
        assert not self.core
        assert not self.core_jobs_ctx

        self.running_core_job = self.jobs_ctx.submit_job(
            ThreadSafeQtSignal(self, "run_core_success"),
            ThreadSafeQtSignal(self, "run_core_error"),
            _do_run_core,
            self.config,
            device,
            self.event_bus,
            ThreadSafeQtSignal(self, "run_core_ready", object, object),
        )

    def on_run_core_ready(self, core, core_jobs_ctx):
        self.core = core
        self.core_jobs_ctx = core_jobs_ctx
        self.event_bus.send(
            "gui.config.changed",
            gui_last_device="{}:{}".format(
                self.core.device.organization_addr.organization_id, self.core.device.device_id
            ),
        )
        self.logged_in.emit()

    def on_core_run_error(self):
        assert self.running_core_job.is_finished()
        if self.running_core_job.status is not None:
            if "Device has been revoked" in str(self.running_core_job.exc):
                show_error(self, _("ERR_LOGIN_DEVICE_REVOKED"), exception=self.running_core_job.exc)
            else:
                logger.error("Unhandled error", exc_info=self.running_core_job.exc)
                show_error(self, _("ERR_LOGIN_UNKNOWN"), exception=self.running_core_job.exc)
        self.running_core_job = None
        self.core_jobs_ctx = None
        self.core = None
        self.logged_out.emit()

    def on_core_run_done(self):
        assert self.running_core_job.is_finished()
        self.running_core_job = None
        self.core_jobs_ctx = None
        self.core = None
        self.logged_out.emit()

    def stop_core(self):
        if self.running_core_job:
            self.running_core_job.cancel_and_join()

    def on_logged_out(self):
        self.state_changed.emit(self, "login")
        self.show_login_widget()

    def on_logged_in(self):
        self.state_changed.emit(self, "connected")
        self.show_central_widget()

    def logout(self):
        self.stop_core()

    def login_with_password(self, key_file, password):
        try:
            device = load_device_with_password(key_file, password)
            self.start_core(device)
        except LocalDeviceError as exc:
            show_error(self, _("ERR_LOGIN_AUTH_FAILED"), exception=exc)

        except BackendHandshakeAPIVersionError as exc:
            show_error(self, _("ERR_LOGIN_INCOMPATIBLE_VERSION"), exception=exc)

        except BackendDeviceRevokedError as exc:
            show_error(self, _("ERR_LOGIN_DEVICE_REVOKED"), exception=exc)

        except BackendHandshakeError as exc:
            show_error(self, _("ERR_LOGIN_UNKNOWN_USER"), exception=exc)

        except (RuntimeError, MountpointConfigurationError, MountpointDriverCrash) as exc:
            show_error(self, _("ERR_LOGIN_MOUNTPOINT"), exception=exc)

        except Exception as exc:
            logger.exception("Unhandled error during login")
            show_error(self, _("ERR_LOGIN_UNKNOWN"), exception=exc)

    def login_with_pkcs11(self, key_file, pkcs11_pin, pkcs11_key, pkcs11_token):
        try:
            device = load_device_with_pkcs11(
                key_file, token_id=pkcs11_token, key_id=pkcs11_key, pin=pkcs11_pin
            )
            self.start_core(device)
        except LocalDeviceError:
            show_error(self, _("ERR_LOGIN_AUTH_FAILED"))

        except BackendHandshakeAPIVersionError:
            show_error(self, _("ERR_LOGIN_INCOMPATIBLE_VERSION"))

        except BackendDeviceRevokedError:
            show_error(self, _("ERR_LOGIN_DEVICE_REVOKED"))

        except BackendHandshakeError:
            show_error(self, _("ERR_LOGIN_UNKNOWN_USER"))

        except (RuntimeError, MountpointConfigurationError, MountpointDriverCrash):
            show_error(self, _("ERR_LOGIN_MOUNTPOINT"))

        except Exception as exc:
            logger.exception("Unhandled error during login")
            show_error(self, _("ERR_LOGIN_UNKNOWN"), exception=exc)

    def show_central_widget(self):
        self.clear_widgets()
        central_widget = CentralWidget(
            self.core, self.core_jobs_ctx, self.core.event_bus, parent=self
        )
        self.layout().addWidget(central_widget)
        central_widget.logout_requested.connect(self.logout)
        central_widget.show()

    def show_login_widget(self, show_meth="show_login_widget", **kwargs):
        self.clear_widgets()
        login_widget = LoginWidget(self.jobs_ctx, self.event_bus, self.config, parent=self)
        self.layout().addWidget(login_widget)

        getattr(login_widget, show_meth)(**kwargs)

        login_widget.login_with_password_clicked.connect(self.login_with_password)
        login_widget.login_with_pkcs11_clicked.connect(self.login_with_pkcs11)
        login_widget.show()

    def clear_widgets(self):
        item = self.layout().takeAt(0)
        if item:
            item.widget().hide()
            item.widget().setParent(None)
