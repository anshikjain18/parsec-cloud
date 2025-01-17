# Parsec Cloud (https://parsec.cloud) Copyright (c) BUSL-1.1 2016-present Scille SAS

from __future__ import annotations

from parsec._parsec import EnrollmentID

class Req:
    def __init__(
        self,
        accept_payload: bytes,
        accept_payload_signature: bytes,
        accepter_der_x509_certificate: bytes,
        enrollment_id: EnrollmentID,
        device_certificate: bytes,
        user_certificate: bytes,
        redacted_device_certificate: bytes,
        redacted_user_certificate: bytes,
    ) -> None: ...
    def dump(self) -> bytes: ...
    @property
    def accept_payload(self) -> bytes: ...
    @property
    def accept_payload_signature(self) -> bytes: ...
    @property
    def accepter_der_x509_certificate(self) -> bytes: ...
    @property
    def enrollment_id(self) -> EnrollmentID: ...
    @property
    def device_certificate(self) -> bytes: ...
    @property
    def user_certificate(self) -> bytes: ...
    @property
    def redacted_device_certificate(self) -> bytes: ...
    @property
    def redacted_user_certificate(self) -> bytes: ...

class Rep:
    @staticmethod
    def load(raw: bytes) -> Rep: ...
    def dump(self) -> bytes: ...

class RepUnknownStatus(Rep):
    def __init__(self, status: str, reason: str | None) -> None: ...
    @property
    def status(self) -> str: ...
    @property
    def reason(self) -> str | None: ...

class RepOk(Rep):
    def __init__(
        self,
    ) -> None: ...

class RepNotAllowed(Rep):
    def __init__(self, reason: str | None) -> None: ...
    @property
    def reason(self) -> str | None: ...

class RepInvalidPayloadData(Rep):
    def __init__(self, reason: str | None) -> None: ...
    @property
    def reason(self) -> str | None: ...

class RepInvalidCertification(Rep):
    def __init__(self, reason: str | None) -> None: ...
    @property
    def reason(self) -> str | None: ...

class RepInvalidData(Rep):
    def __init__(self, reason: str | None) -> None: ...
    @property
    def reason(self) -> str | None: ...

class RepNotFound(Rep):
    def __init__(self, reason: str | None) -> None: ...
    @property
    def reason(self) -> str | None: ...

class RepNoLongerAvailable(Rep):
    def __init__(self, reason: str | None) -> None: ...
    @property
    def reason(self) -> str | None: ...

class RepAlreadyExists(Rep):
    def __init__(self, reason: str | None) -> None: ...
    @property
    def reason(self) -> str | None: ...

class RepActiveUsersLimitReached(Rep):
    def __init__(
        self,
    ) -> None: ...
