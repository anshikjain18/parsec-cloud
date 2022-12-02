# Parsec Cloud (https://parsec.cloud) Copyright (c) BUSL-1.1 (eventually AGPL-3.0) 2016-present Scille SAS

# Message
from typing import Iterable

from parsec._parsec import DateTime, DeviceID

class MessageGetReq:
    def __init__(self, offset: int) -> None: ...
    def dump(self) -> bytes: ...
    @property
    def offset(self) -> int: ...

class MessageGetRep:
    def dump(self) -> bytes: ...
    @classmethod
    def load(cls, buf: bytes) -> "MessageGetRep": ...

class MessageGetRepOk(MessageGetRep):
    def __init__(self, messages: Iterable["Message"]) -> None: ...
    @property
    def messages(self) -> tuple["Message"]: ...

class MessageGetRepUnknownStatus(MessageGetRep):
    def __init__(self, status: str, reason: str | None) -> None: ...
    @property
    def status(self) -> str: ...
    @property
    def reason(self) -> str | None: ...

class Message:
    def __init__(self, count: int, sender: DeviceID, timestamp: DateTime, body: bytes) -> None: ...
    @property
    def count(self) -> int: ...
    @property
    def sender(self) -> DeviceID: ...
    @property
    def timestamp(self) -> DateTime: ...
    @property
    def body(self) -> bytes: ...
