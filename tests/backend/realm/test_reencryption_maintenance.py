# Parsec Cloud (https://parsec.cloud) Copyright (c) AGPLv3 2019 Scille SAS

import pytest

from parsec.api.protocole import RealmRole

from tests.backend.realm.conftest import (
    realm_start_reencryption_maintenance,
    realm_finish_reencryption_maintenance,
    vlob_read,
    vlob_maintenance_get_reencryption_batch,
    vlob_maintenance_save_reencryption_batch,
)


@pytest.mark.trio
async def test_start_bad_encryption_revision(backend, alice_backend_sock, realm):
    rep = await realm_start_reencryption_maintenance(
        alice_backend_sock, realm, 42, {"alice": b"wathever"}, check_rep=False
    )
    assert rep == {"status": "bad_encryption_revision"}


@pytest.mark.trio
async def test_start_bad_per_participant_message(backend, alice_backend_sock, alice, bob, realm):
    # Add bob for more fun !
    await backend.realm.update_roles(
        alice.organization_id, alice.device_id, realm, bob.user_id, RealmRole.READER
    )

    for msg in [
        {},
        {alice.user_id: b"ok"},
        {alice.user_id: b"ok", bob.user_id: b"ok", "zack": b"dunno this guy"},
    ]:
        rep = await realm_start_reencryption_maintenance(
            alice_backend_sock, realm, 2, {}, check_rep=False
        )
        assert rep == {
            "status": "maintenance_error",
            "reason": "Realm participants and message recipients mismatch",
        }


@pytest.mark.trio
async def test_start_already_in_maintenance(backend, alice_backend_sock, realm):
    await realm_start_reencryption_maintenance(alice_backend_sock, realm, 2, {"alice": b"wathever"})
    for encryption_revision in (2, 3):
        rep = await realm_start_reencryption_maintenance(
            alice_backend_sock, realm, encryption_revision, {"alice": b"wathever"}, check_rep=False
        )
        assert rep == {"status": "in_maintenance"}


@pytest.mark.trio
async def test_start_check_access_rights(backend, bob_backend_sock, alice, bob, realm):
    # User not part of the realm
    rep = await realm_start_reencryption_maintenance(
        bob_backend_sock, realm, 2, {"alice": b"wathever"}, check_rep=False
    )
    assert rep == {"status": "not_allowed"}

    # User part of the realm with various role
    for not_allowed_role in (RealmRole.READER, RealmRole.CONTRIBUTOR, RealmRole.MANAGER):
        await backend.realm.update_roles(
            alice.organization_id, alice.device_id, realm, bob.user_id, not_allowed_role
        )

        rep = await realm_start_reencryption_maintenance(
            bob_backend_sock, realm, 2, {"alice": b"foo", "bob": b"bar"}, check_rep=False
        )
        assert rep == {"status": "not_allowed"}

    # Finally, just make sure owner can do it
    await backend.realm.update_roles(
        alice.organization_id, alice.device_id, realm, bob.user_id, RealmRole.OWNER
    )

    rep = await realm_start_reencryption_maintenance(
        bob_backend_sock, realm, 2, {"alice": b"foo", "bob": b"bar"}, check_rep=False
    )
    assert rep == {"status": "ok"}


@pytest.mark.trio
async def test_start_other_organization(backend, sock_from_other_organization_factory, realm):
    async with sock_from_other_organization_factory(backend) as sock:
        rep = await realm_start_reencryption_maintenance(
            sock, realm, 2, {"alice": b"foo"}, check_rep=False
        )
    assert rep == {
        "status": "not_found",
        "reason": "Realm `a0000000-0000-0000-0000-000000000000` doesn't exist",
    }


@pytest.mark.trio
async def test_finish_not_in_maintenance(alice_backend_sock, realm):
    for encryption_revision in (2, 3):
        rep = await realm_finish_reencryption_maintenance(
            alice_backend_sock, realm, encryption_revision, check_rep=False
        )
        assert rep == {
            "status": "maintenance_error",
            "reason": "Realm `a0000000-0000-0000-0000-000000000000` not under maintenance",
        }


@pytest.mark.trio
async def test_reencryption_batch_not_during_maintenance(alice_backend_sock, realm):
    rep = await vlob_maintenance_get_reencryption_batch(alice_backend_sock, realm, 1)
    assert rep == {
        "status": "maintenance_error",
        "reason": "Realm `a0000000-0000-0000-0000-000000000000` not under maintenance",
    }

    rep = await vlob_maintenance_save_reencryption_batch(
        alice_backend_sock, realm, 1, [], check_rep=False
    )
    assert rep == {
        "status": "maintenance_error",
        "reason": "Realm `a0000000-0000-0000-0000-000000000000` not under maintenance",
    }

    rep = await realm_finish_reencryption_maintenance(alice_backend_sock, realm, 1, check_rep=False)
    assert rep == {
        "status": "maintenance_error",
        "reason": "Realm `a0000000-0000-0000-0000-000000000000` not under maintenance",
    }


@pytest.mark.trio
async def test_reencryption_batch_bad_revisison(alice_backend_sock, realm):
    await realm_start_reencryption_maintenance(alice_backend_sock, realm, 2, {"alice": b"foo"})

    rep = await vlob_maintenance_get_reencryption_batch(alice_backend_sock, realm, 1)
    assert rep == {"status": "bad_encryption_revision"}

    rep = await realm_finish_reencryption_maintenance(alice_backend_sock, realm, 1, check_rep=False)
    assert rep == {"status": "bad_encryption_revision"}


@pytest.mark.trio
async def test_reencryption(alice_backend_sock, realm, vlobs):
    await realm_start_reencryption_maintenance(alice_backend_sock, realm, 2, {"alice": b"foo"})
    # TODO: Test that Alice have received the message

    # Get the first (and only in our case) batch
    rep = await vlob_maintenance_get_reencryption_batch(alice_backend_sock, realm, 2)
    assert rep["status"] == "ok"
    assert len(rep["batch"]) == 3
    batch_entries = {(vlobs[0], 1), (vlobs[0], 2), (vlobs[1], 1)}
    assert {(x["vlob_id"], x["version"]) for x in rep["batch"]} == batch_entries

    # Save the modified batch
    updated_batch = [
        {
            "vlob_id": vlob_id,
            "version": version,
            "data": f"{vlob_id}::{version} reencrypted".encode(),
        }
        for vlob_id, version in batch_entries
    ]
    await vlob_maintenance_save_reencryption_batch(alice_backend_sock, realm, 2, updated_batch)

    # Finish the reencryption
    await realm_finish_reencryption_maintenance(alice_backend_sock, realm, 2)

    # Check the vlob have changed
    for vlob_id, version in batch_entries:
        rep = await vlob_read(alice_backend_sock, vlob_id, version, encryption_revision=2)
        assert rep["blob"] == f"{vlob_id}::{version} reencrypted".encode()


############ TODO  ####################
# TODO TODO TODO TODO

# @pytest.mark.trio
# @pytest.mark.parametrize('bob_role', [
#     None,
#     RealmRole.READER,
#     RealmRole.CONTRIBUTOR,
#     RealmRole.MANAGER,
# ])
# async def test_finish_check_access_rights(backend, bob_backend_sock, alice, bob, realm, bob_role):
#     await backend.realm.start_reencryption_maintenance(alice.organization_id, alice.device_id, realm, 2, )

#     # User not part of the realm
#     rep = await realm_finish_reencryption_maintenance(bob_backend_sock, realm, 2, {"alice": b"wathever"}, check_rep=False)
#     assert rep == {"status": "not_allowed"}

#     # User part of the realm with various role
#     for not_allowed_role in (
#         RealmRole.READER,
#         RealmRole.CONTRIBUTOR,
#         RealmRole.MANAGER,
#     ):
#         await backend.realm.update_roles(
#             alice.organization_id, alice.device_id, realm, bob.user_id, not_allowed_role
#         )

#         rep = await realm_finish_reencryption_maintenance(bob_backend_sock, realm, 2, {"alice": b"foo", "bob": b'bar'}, check_rep=False)
#         assert rep == {"status": "not_allowed"}

#     # Finally, just make sure owner can do it
#     await backend.realm.update_roles(
#         alice.organization_id, alice.device_id, realm, bob.user_id, RealmRole.OWNER
#     )

#     rep = await realm_finish_reencryption_maintenance(bob_backend_sock, realm, 2, {"alice": b"foo", "bob": b'bar'}, check_rep=False)
#     assert rep == {"status": "ok"}


# @pytest.mark.trio
# async def test_reencryption_maintenance(backend, alice_backend_sock, realm, vlobs):
#     rep = realm_start_reencryption_maintenance(realm, 2, {}, check_rep=False)
#     rep = await realm_status(alice_backend_sock, realm)
#     assert rep == {
#         "status": "ok",
#         "in_maintenance": False,
#         "maintenance_type": None,
#         "maintenance_started_by": None,
#         "maintenance_started_on": None,
#         "encryption_revision": 1,
#     }


# @pytest.mark.trio
# async def test_realm_lazy_created_by_new_vlob(backend, alice, alice_backend_sock):
#     NOW = Pendulum(2000, 1, 1)
#     VLOB_ID = UUID("00000000000000000000000000000001")
#     REALM_ID = UUID("0000000000000000000000000000000A")

#     await backend.vlob.create(alice.organization_id, alice.device_id, VLOB_ID, REALM_ID, NOW, b"v1")

#     rep = await vlob_poll_changes(alice_backend_sock, REALM_ID, 0)
#     assert rep == {"status": "ok", "current_checkpoint": 1, "changes": {VLOB_ID: 1}}

#     # Make sure author gets OWNER role

#     rep = await realm_get_roles(alice_backend_sock, REALM_ID)
#     assert rep == {"status": "ok", "users": {"alice": RealmRole.OWNER}}
