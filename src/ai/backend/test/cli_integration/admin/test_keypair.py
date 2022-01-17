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
        json_result = json.loads(p.before.decode())
        assert json_result.get('ok'), 'User creation has failed'

    add_arguments = ['--output=json', 'admin', 'user', 'add', '-u', 'userkeypair', '-n', 'Richard Doe',
                     'default', 'userkeypair@lablup.com', '1q2w3e4r']
    with closing(run(add_arguments)) as p:
        p.expect(EOF)
        json_result = json.loads(p.before.decode())
        assert json_result.get('ok'), 'User creation has failed'

    # Create keypair
    with closing(run(['admin', 'keypair', 'add', '-a', '-i', '-r', '25000', 'adminkeypair@lablup.com', 'default'])) as p:
        p.expect(EOF)
        listed_result = p.before.decode().split()
        assert 'access_key' in listed_result and 'secret_key' in listed_result, 'Admin-keypair creation has failed'

    with closing(run(['admin', 'keypair', 'add', 'userkeypair@lablup.com', 'default'])) as p:
        p.expect(EOF)
        listed_result = p.before.decode().split()
        assert 'access_key' in listed_result and 'secret_key' in listed_result, 'User-keypair creation has failed'

    # Check if keypair is added
    with closing(run(['--output=json', 'admin', 'keypair', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        keypair_list = loaded.get('items')
        assert isinstance(keypair_list, list), 'List not printed properly!'

    admin_keypair = get_keypair_from_list(keypair_list, 'adminkeypair@lablup.com')
    user_keypair = get_keypair_from_list(keypair_list, 'userkeypair@lablup.com')

    assert 'access_key' in admin_keypair, 'Admin keypair doesn\'t exist'
    assert admin_keypair.get('is_active') is False, 'Admin keypair is_active mismatch'
    assert admin_keypair.get('is_admin') is True, 'Admin keypair is_admin mismatch'
    assert admin_keypair.get('rate_limit') == 25000, 'Admin keypair rate_limit mismatch'
    assert admin_keypair.get('resource_policy') == 'default', 'Admin keypair resource_policy mismatch'

    assert 'access_key' in user_keypair, 'Admin keypair doesn\'t exist'
    assert user_keypair.get('is_active') is True, 'User keypair is_active mismatch'
    assert user_keypair.get('is_admin') is False, 'User keypair is_admin mismatch'
    assert user_keypair.get('rate_limit') == 5000, 'User keypair rate_limit mismatch'
    assert user_keypair.get('resource_policy') == 'default', 'User keypair resource_policy mismatch'


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

    admin_keypair = get_keypair_from_list(keypair_list, 'adminkeypair@lablup.com')
    user_keypair = get_keypair_from_list(keypair_list, 'userkeypair@lablup.com')
    assert 'access_key' in admin_keypair, 'Admin keypair info doesn\'t exist'
    assert 'access_key' in user_keypair, 'User keypair info doesn\'t exist'

    # Update keypair
    with closing(run([
        'admin', 'keypair', 'update',
        '--is-active', 'TRUE',
        '--is-admin', 'FALSE',
        '-r', '15000',
        admin_keypair['access_key'],
    ])) as p:
        p.expect(EOF)
        listed_result = p.before.decode().split()
        assert listed_result.index('ok') == listed_result.index('True') - 1, 'Admin keypair update has failed'

    with closing(run([
        'admin', 'keypair', 'update',
        '--is-active', 'FALSE',
        '--is-admin', 'TRUE',
        '-r', '15000',
        user_keypair['access_key'],
    ])) as p:
        p.expect(EOF)
        listed_result = p.before.decode().split()
        assert listed_result.index('ok') == listed_result.index('True') - 1, 'User keypair update has failed'

    # Check if keypair is updated
    with closing(run(['--output=json', 'admin', 'keypair', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        updated_keypair_list = loaded.get('items')
        assert isinstance(updated_keypair_list, list), 'List not printed properly!'

    updated_admin_keypair = get_keypair_from_list(updated_keypair_list, 'adminkeypair@lablup.com')
    updated_user_keypair = get_keypair_from_list(updated_keypair_list, 'userkeypair@lablup.com')

    assert 'access_key' in updated_admin_keypair, 'Admin keypair doesn\'t exist'
    assert updated_admin_keypair.get('is_active') is True, 'Admin keypair is_active mismatch'
    assert updated_admin_keypair.get('is_admin') is False, 'Admin keypair is_admin mismatch'
    assert updated_admin_keypair.get('rate_limit') == 15000, 'Admin keypair rate_limit mismatch'
    assert updated_admin_keypair.get('resource_policy') == 'default', 'Admin keypair resource_policy mismatch'

    assert 'access_key' in updated_user_keypair, 'Admin keypair doesn\'t exist'
    assert updated_user_keypair.get('is_active') is False, 'User keypair is_active mismatch'
    assert updated_user_keypair.get('is_admin') is True, 'User keypair is_admin mismatch'
    assert updated_user_keypair.get('rate_limit') == 15000, 'User keypair rate_limit mismatch'
    assert updated_user_keypair.get('resource_policy') == 'default', 'User keypair resource_policy mismatch'


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

    admin_keypair = get_keypair_from_list(keypair_list, 'adminkeypair@lablup.com')
    user_keypair = get_keypair_from_list(keypair_list, 'userkeypair@lablup.com')
    assert 'access_key' in admin_keypair, 'Admin keypair info doesn\'t exist'
    assert 'access_key' in user_keypair, 'User keypair info doesn\'t exist'

    # Delete keypair
    with closing(run(['admin', 'keypair', 'delete', admin_keypair['access_key']])) as p:
        p.expect(EOF)
        listed_result = p.before.decode().split()
        assert listed_result.index('ok') == listed_result.index('True') - 1, 'Admin-keypair deletion has failed'

    with closing(run(['admin', 'keypair', 'delete', user_keypair['access_key']])) as p:
        p.expect(EOF)
        listed_result = p.before.decode().split()
        assert listed_result.index('ok') == listed_result.index('True') - 1, 'User-keypair deletion has failed'

    # Delete test user
    with closing(run(['admin', 'user', 'purge', 'adminkeypair@lablup.com'])) as p:
        p.sendline('y')
        p.expect(EOF)
        listed_result = p.before.decode().split()
        assert listed_result.index('ok') == listed_result.index('True') - 1, 'Admin user deletion has failed'

    with closing(run(['admin', 'user', 'purge', 'userkeypair@lablup.com'])) as p:
        p.sendline('y')
        p.expect(EOF)
        listed_result = p.before.decode().split()
        assert listed_result.index('ok') == listed_result.index('True') - 1, 'User deletion has failed'


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
