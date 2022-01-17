import json
from contextlib import closing
from typing import Iterator

from ...utils.cli import EOF, ClientRunnerFunc


def test_add_group(run: ClientRunnerFunc, temp_domain: Iterator[str]):
    with closing(run([
        '--output=json',
        'admin', 'group', 'add',
        temp_domain,
        'test_user_group',
    ])) as p:
        p.expect(EOF)
        json_result = json.loads(p.before.decode())
        assert json_result.get('ok'), 'Group creation has failed'
        gid = json_result['group']['id']

    # Delete the created group
    with closing(run([
        'admin', 'group', 'purge', gid,
    ])) as p:
        p.expect_exact("Are you sure? [Y/n]")
        p.sendline('y')
        p.expect(EOF)


def test_add_users_to_group(run: ClientRunnerFunc, temp_domain: Iterator[str]):
    # Create a testing group
    with closing(run([
        '--output=json',
        'admin', 'group', 'add',
        temp_domain,
        'test_user_group',
    ])) as p:
        p.expect(EOF)
        json_result = json.loads(p.before.decode())
        gid = json_result['group']['id']

    # Create a testing user
    add_arguments = ['admin', 'user', 'add', 'default', 'test_user@lablup.com', '1q2w3e4r']
    with closing(run(add_arguments)) as p:
        p.expect(EOF)

    # Get user's UUID
    add_arguments = ['--output=json', 'admin', 'user', 'list']
    with closing(run(add_arguments)) as p:
        p.expect(EOF)
        json_result = json.loads(p.before.decode())
        user = [user if user['email'] == 'test_user@lablup.com' else None for user in json_result['items']][0]

    with closing(run([
        '--output=json',
        'admin', 'group', 'add-users',
        gid,
        user['uuid'],
    ])) as p:
        p.expect(EOF)
        json_result = json.loads(p.before.decode())
        assert json_result.get('ok'), 'Group update has failed'

    # Delete testing user
    add_arguments = ['admin', 'user', 'purge', user['email']]
    with closing(run(add_arguments)) as p:
        p.sendline('y')
        p.expect(EOF)

    # Delete the created group
    with closing(run([
        'admin', 'group', 'purge', gid,
    ])) as p:
        p.expect_exact("Are you sure? [Y/n]")
        p.sendline('y')
        p.expect(EOF)


def test_update_group(run: ClientRunnerFunc, temp_domain: Iterator[str]):
    # Create a testing group
    with closing(run([
        '--output=json',
        'admin', 'group', 'add',
        temp_domain,
        'test_user_group',
    ])) as p:
        p.expect(EOF)
        json_result = json.loads(p.before.decode())
        gid = json_result['group']['id']

    with closing(run([
        '--output=json',
        'admin', 'group', 'update',
        '-n', 'new_name',
        '-d', 'Description here',
        gid,
    ])) as p:
        p.expect(EOF)
        json_result = json.loads(p.before.decode())
        assert json_result.get('ok'), 'Group update has failed'

    # Delete the created group
    with closing(run([
        'admin', 'group', 'purge', gid,
    ])) as p:
        p.expect_exact("Are you sure? [Y/n]")
        p.sendline('y')
        p.expect(EOF)


def test_delete_group(run: ClientRunnerFunc, temp_domain: Iterator[str]):
    # Create a testing group
    with closing(run([
        '--output=json',
        'admin', 'group', 'add',
        temp_domain,
        'test_user_group',
    ])) as p:
        p.expect(EOF)
        json_result = json.loads(p.before.decode())
        gid = json_result['group']['id']

    # Delete a testing group
    with closing(run([
        '--output=json', 'admin', 'group', 'purge', gid,
    ])) as p:
        p.expect_exact("Are you sure? [Y/n]")
        p.sendline('y')
        p.expect(EOF)
        std_output = p.before.decode()
        json_output = std_output[std_output.index('{'):std_output.index('}') + 1]
        json_result = json.loads(json_output)
        assert json_result.get('ok'), 'Group deletion has failed'


def test_list_group(run: ClientRunnerFunc):
    with closing(run(['--output=json', 'admin', 'group', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        group_list = loaded.get('items')
        assert isinstance(group_list, list), 'Group list not printed properly'
