from uuid import UUID
from typing import List, Tuple
from collections import defaultdict

from parsec.types import DeviceID, OrganizationID
from parsec.event_bus import EventBus
from parsec.backend.beacon import BaseBeaconComponent
from parsec.backend.vlob import (
    BaseVlobComponent,
    VlobTrustSeedError,
    VlobVersionError,
    VlobNotFoundError,
    VlobAlreadyExistsError,
)


class MemoryVlob:
    def __init__(self, id, rts, wts):
        self.id = id
        self.rts = rts
        self.wts = wts
        self.blob_versions = []


class MemoryVlobComponent(BaseVlobComponent):
    def __init__(self, event_bus: EventBus, beacon_component: BaseBeaconComponent):
        self.event_bus = event_bus
        self.beacon_component = beacon_component
        self._organizations = defaultdict(dict)

    async def group_check(
        self, organization_id: OrganizationID, to_check: List[dict]
    ) -> List[dict]:
        changed = []
        for item in to_check:
            id = item["id"]
            rts = item["rts"]
            version = item["version"]
            if version == 0:
                changed.append({"id": id, "version": version})
            else:
                try:
                    current_version, _ = await self.read(organization_id, id, rts)
                except (VlobNotFoundError, VlobTrustSeedError):
                    continue
                if current_version != version:
                    changed.append({"id": id, "version": current_version})
        return changed

    async def create(
        self,
        organization_id: OrganizationID,
        id: UUID,
        rts: str,
        wts: str,
        blob: bytes,
        author: DeviceID,
        notify_beacon: UUID = None,
    ) -> None:
        vlobs = self._organizations[organization_id]

        vlob = MemoryVlob(id, rts, wts)
        vlob.blob_versions.append((blob, author))
        if vlob.id in vlobs:
            raise VlobAlreadyExistsError()
        vlobs[vlob.id] = vlob

        if notify_beacon:
            await self.beacon_component.update(organization_id, notify_beacon, id, 1, author)

    async def read(
        self, organization_id: OrganizationID, id: UUID, rts: str, version: int = None
    ) -> Tuple[int, bytes]:
        vlobs = self._organizations[organization_id]

        try:
            vlob = vlobs[id]
            if vlob.rts != rts:
                raise VlobTrustSeedError()

        except KeyError:
            raise VlobNotFoundError()

        if version is None:
            version = len(vlob.blob_versions)
        try:
            return (version, vlob.blob_versions[version - 1][0])

        except IndexError:
            raise VlobVersionError()

    async def update(
        self,
        organization_id: OrganizationID,
        id: UUID,
        wts: str,
        version: int,
        blob: bytes,
        author: DeviceID,
        notify_beacon: UUID = None,
    ) -> None:
        vlobs = self._organizations[organization_id]

        try:
            vlob = vlobs[id]
            if vlob.wts != wts:
                raise VlobTrustSeedError()

        except KeyError:
            raise VlobNotFoundError()

        if version - 1 == len(vlob.blob_versions):
            vlob.blob_versions.append((blob, author))
        else:
            raise VlobVersionError()

        if notify_beacon:
            await self.beacon_component.update(organization_id, notify_beacon, id, version, author)
