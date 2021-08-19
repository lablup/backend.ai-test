import json
from contextlib import closing

from ...utils.cli import EOF, ClientRunnerFunc


def test_add_keypair(run: ClientRunnerFunc):
    """
    Test add keypair.
    This test should be execued first in test_keypair.py.
    """
    print("[ Add keypair ]")
    # Add test user
    add_arguments = ['--output=json', 'admin', 'user', 'add', '-u', 'adminkeypair', '-n', 'John Doe',
                     '-r', 'admin', 'default', 'adminkeypair@lablup.com', '1q2w3e4r']
    with closing(run(add_arguments)) as p:
        p.expect(EOF)
        assert 'User adminkeypair@lablup.com is created' in p.before.decode(), 'Account add error'

    add_arguments = ['--output=json', 'admin', 'user', 'add', '-u', 'userkeypair', '-n', 'Richard Doe',
                     'default', 'userkeypair@lablup.com', '1q2w3e4r']
    with closing(run(add_arguments)) as p:
        p.expect(EOF)
        assert 'User userkeypair@lablup.com is created' in p.before.decode(), 'Account add error'

    # Create keypair
    with closing(run(['admin', 'keypair', 'add', '-a', '-i', '-r', '25000', 'adminkeypair@lablup.com', 'default'])) as p:
        p.expect(EOF)
        assert 'Access Key:' in p.before.decode() and 'Secret Key:' in p.before.decode(), 'Keypair add error'

    with closing(run(['admin', 'keypair', 'add', 'userkeypair@lablup.com', 'default'])) as p:
        p.expect(EOF)
        assert 'Access Key:' in p.before.decode() and 'Secret Key:' in p.before.decode(), 'Keypair add error'

    # Check if keypair is added
    with closing(run(['--output=json', 'admin', 'keypair', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        keypair_list = loaded.get('items')
        assert isinstance(keypair_list, list), 'List not printed properly!'

    adminkeypair = get_keypair_from_list(keypair_list, 'adminkeypair@lablup.com')
    userkeypair = get_keypair_from_list(keypair_list, 'userkeypair@lablup.com')

    assert bool(adminkeypair), 'Admin keypair doesn\'t exist'
    assert adminkeypair.get('is_active') == False, 'Admin keypair is_active mismatch'
    assert adminkeypair.get('is_admin') == True, 'Admin keypair is_admin mismatch'
    assert adminkeypair.get('rate_limit') == 25000, 'Admin keypair rate_limit mismatch'
    assert adminkeypair.get('resource_policy') == 'default', 'Admin keypair resource_policy mismatch'

    assert bool(userkeypair), 'Admin keypair doesn\'t exist'
    assert userkeypair.get('is_active') == True, 'User keypair is_active mismatch'
    assert userkeypair.get('is_admin') == False, 'User keypair is_admin mismatch'
    assert userkeypair.get('rate_limit') == 5000, 'User keypair rate_limit mismatch'
    assert userkeypair.get('resource_policy') == 'default', 'User keypair resource_policy mismatch'


def test_update_keypair(run: ClientRunnerFunc):
    """
    Test update keypair.
    This test must be executed after test_add_keypair.
    """
    print("[ Update keypair ]")
    # Get access key
    with closing(run(['--output=json', 'admin', 'keypair', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        keypair_list = loaded.get('items')
        assert isinstance(keypair_list, list), 'List not printed properly!'

    adminkeypair = get_keypair_from_list(keypair_list, 'adminkeypair@lablup.com')
    userkeypair = get_keypair_from_list(keypair_list, 'userkeypair@lablup.com')

    assert bool(adminkeypair), 'Admin keypair info doesn\'t exist'
    assert bool(userkeypair), 'User keypair info doesn\'t exist'

    # Update keypair
    with closing(run(['admin', 'keypair', 'update', '--is-active', 'TRUE', '--is-admin', 'FALSE',
                      '-r', '15000', adminkeypair.get('access_key')])) as p:
        p.expect(EOF)
        assert 'Key pair is updated:' in p.before.decode(), 'Admin keypair update error'

    with closing(run(['admin', 'keypair', 'update', '--is-active', 'FALSE', '--is-admin', 'TRUE',
                      '-r', '15000', userkeypair.get('access_key')])) as p:
        p.expect(EOF)
        assert 'Key pair is updated:' in p.before.decode(), 'User keypair update error'

    # Check if keypair is updated
    with closing(run(['--output=json', 'admin', 'keypair', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        updated_keypair_list = loaded.get('items')
        assert isinstance(updated_keypair_list, list), 'List not printed properly!'

    updated_adminkeypair = get_keypair_from_list(updated_keypair_list, 'adminkeypair@lablup.com')
    updated_userkeypair = get_keypair_from_list(updated_keypair_list, 'userkeypair@lablup.com')

    assert bool(updated_adminkeypair), 'Admin keypair doesn\'t exist'
    assert updated_adminkeypair.get('is_active') == True, 'Admin keypair is_active mismatch'
    assert updated_adminkeypair.get('is_admin') == False, 'Admin keypair is_admin mismatch'
    assert updated_adminkeypair.get('rate_limit') == 15000, 'Admin keypair rate_limit mismatch'
    assert updated_adminkeypair.get('resource_policy') == 'default', 'Admin keypair resource_policy mismatch'

    assert bool(updated_userkeypair), 'Admin keypair doesn\'t exist'
    assert updated_userkeypair.get('is_active') == False, 'User keypair is_active mismatch'
    assert updated_userkeypair.get('is_admin') == True, 'User keypair is_admin mismatch'
    assert updated_userkeypair.get('rate_limit') == 15000, 'User keypair rate_limit mismatch'
    assert updated_userkeypair.get('resource_policy') == 'default', 'User keypair resource_policy mismatch'


def test_delete_keypair(run: ClientRunnerFunc):
    """
    Test delete keypair.
    This test must be executed after test_add_keypair.
    """
    print("[ Delete keypair ]")
    # Get access key
    with closing(run(['--output=json', 'admin', 'keypair', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        keypair_list = loaded.get('items')
        assert isinstance(keypair_list, list), 'List not printed properly!'

    adminkeypair = get_keypair_from_list(keypair_list, 'adminkeypair@lablup.com')
    userkeypair = get_keypair_from_list(keypair_list, 'userkeypair@lablup.com')

    assert bool(adminkeypair), 'Admin keypair info doesn\'t exist'
    assert bool(userkeypair), 'User keypair info doesn\'t exist'

    # Delete keypair
    with closing(run(['admin', 'keypair', 'delete', adminkeypair.get('access_key')])) as p:
        p.expect(EOF)
        print(p.before.decode())

    with closing(run(['admin', 'keypair', 'delete', userkeypair.get('access_key')])) as p:
        p.expect(EOF)
        print(p.before.decode())

    # Delete test user
    with closing(run(['admin', 'user', 'purge', 'adminkeypair@lablup.com'])) as p:
        p.sendline('y')
        p.expect(EOF)
        assert 'User is deleted:' in p.before.decode(), 'Account deletion failed: adminkeypair'

    with closing(run(['admin', 'user', 'purge', 'userkeypair@lablup.com'])) as p:
        p.sendline('y')
        p.expect(EOF)
        assert 'User is deleted:' in p.before.decode(), 'Account deletion failed: userkeypair'


def test_list_keypair(run: ClientRunnerFunc):
    """
    Test list keypair.
    """
    with closing(run(['--output=json', 'admin', 'keypair', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        keypair_list = loaded.get('items')
        assert isinstance(keypair_list, list), 'List not printed properly!'


def get_keypair_from_list(keypairs: list, userid: str) -> dict:
    for keypair in keypairs:
        if keypair.get('user_id', '') == userid:
            return keypair

    return {}