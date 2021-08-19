import json
from contextlib import closing

from ...utils.cli import EOF, ClientRunnerFunc


def test_add_keypair(run: ClientRunnerFunc):
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
    pass


def test_delete_keypair(run: ClientRunnerFunc):
    pass


def test_list_keypair(run: ClientRunnerFunc):
    with closing(run(['--output=json', 'admin', 'keypair', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        keypair_list = loaded.get('items')
        assert isinstance(keypair_list, list)