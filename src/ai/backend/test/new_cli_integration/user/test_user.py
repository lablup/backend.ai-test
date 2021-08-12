from contextlib import closing
import functools
import json
import re
import sys

import pytest

from ...utils.cli import EOF, ClientRunnerFunc

def test_add_user(run: ClientRunnerFunc):
    print("[ Add user ]")

    # Check if test account exists
    with closing(run(['--output=json', 'admin', 'user', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        user_list = loaded.get('items')

    test_user1 = get_user_from_json(user_list, 'testaccount1')
    test_user2 = get_user_from_json(user_list, 'testaccount2')
    test_user3 = get_user_from_json(user_list, 'testaccount3')

    if not bool(test_user1):
        # Add user
        add_arguments = ['--output=json', 'admin', 'user', 'add', '-u', 'testaccount1', '-n', 'John Doe',
                         '--need-password-change', 'default', 'testaccount1@lablup.com', '1q2w3e4r']
        with closing(run(add_arguments)) as p:
            p.expect(EOF)
            assert 'User testaccount1@lablup.com is created' in p.before.decode(), 'Account add error'

    if not bool(test_user2):
        # Add user
        add_arguments = ['--output=json', 'admin', 'user', 'add', '-u', 'testaccount2', '-n', 'John Roe', '-r', 'admin',
                         '-s', 'inactive', 'default', 'testaccount2@lablup.com', '1q2w3e4r']
        with closing(run(add_arguments)) as p:
            p.expect(EOF)
            assert 'User testaccount2@lablup.com is created' in p.before.decode(), 'Account add error'

    if not bool(test_user3):
        # Add user
        add_arguments = ['--output=json', 'admin', 'user', 'add', '-u', 'testaccount3', '-n', 'Richard Roe', '-r',
                         'monitor', '-s', 'before-verification', '--need-password-change', 'default',
                         'testaccount3@lablup.com', '1q2w3e4r']
        with closing(run(add_arguments)) as p:
            p.expect(EOF)
            assert 'User testaccount3@lablup.com is created' in p.before.decode(), 'Account add error'

    # Check if user is added
    with closing(run(['--output=json', 'admin', 'user', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        user_list = loaded.get('items')

    assert isinstance(user_list, list), 'Expected user list'
    added_user1 = get_user_from_json(user_list, 'testaccount1')
    added_user2 = get_user_from_json(user_list, 'testaccount2')
    added_user3 = get_user_from_json(user_list, 'testaccount3')

    assert bool(added_user1), 'Added account doesn\'t exist: Account#1'
    assert added_user1.get('email') == 'testaccount1@lablup.com', 'E-mail mismatch: Account#1'
    assert added_user1.get('full_name') == 'John Doe', 'Full name mismatch: Account#1'
    assert added_user1.get('status') == 'active', 'User status mismatch: Account#1'
    assert added_user1.get('role') == 'user', 'Role mismatch: Account#1'
    assert added_user1.get('need_password_change') == True, 'Password change status mismatch: Account#1'

    assert bool(added_user2), 'Added account doesn\'t exist: Account#2'
    assert added_user2.get('email') == 'testaccount2@lablup.com', 'E-mail mismatch: Account#2'
    assert added_user2.get('full_name') == 'John Roe', 'Full name mismatch: Account#2'
    assert added_user2.get('status') == 'inactive', 'User status mismatch: Account#2'
    assert added_user2.get('role') == 'admin', 'Role mismatch: Account#2'
    assert added_user2.get('need_password_change') == False, 'Password change status mismatch: Account#2'

    assert bool(added_user3), 'Added account doesn\'t exist: Account#3'
    assert added_user3.get('email') == 'testaccount3@lablup.com', 'E-mail mismatch: Account#3'
    assert added_user3.get('full_name') == 'Richard Roe', 'Full name mismatch: Account#3'
    assert added_user3.get('status') == 'before-verification', 'User status mismatch: Account#3'
    assert added_user3.get('role') == 'monitor', 'Role mismatch: Account#3'
    assert added_user3.get('need_password_change') == True, 'Password change status mismatch: Account#3'


def test_update_user(run: ClientRunnerFunc):
    print("[ Update user ]")

    # Check if user exists
    with closing(run(['--output=json', 'admin', 'user', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        user_list = loaded.get('items')
        assert isinstance(user_list, list), 'Expected user list'

    # Update user
    update_arguments = ['--output=json', 'admin', 'user', 'update', '-u', 'testaccount123', '-n', 'Foo Bar', '-s',
                        'inactive', 'testaccount1@lablup.com']
    with closing(run(update_arguments)) as p:
        p.expect(EOF)

    update_arguments = ['--output=json', 'admin', 'user', 'update', '-u', 'testaccount231', '-n', 'Baz Quz', '-s',
                        'active', '-r', 'admin', '--need-password-change', 'testaccount2@lablup.com']
    with closing(run(update_arguments)) as p:
        p.expect(EOF)

    update_arguments = ['--output=json', 'admin', 'user', 'update', '-u', 'testaccount312', '-n', 'Alice B.', '-s',
                        'active', '-r', 'monitor', 'testaccount3@lablup.com']
    with closing(run(update_arguments)) as p:
        p.expect(EOF)

    # Check if user is updated correctly
    with closing(run(['--output=json', 'admin', 'user', 'list'])) as p:
        p.expect(EOF)
        after_update_decoded = p.before.decode()
        after_update_loaded = json.loads(after_update_decoded)
        updated_user_list = after_update_loaded.get('items')
        assert isinstance(updated_user_list, list), 'Expected user list'

    test_user1 = get_user_from_json(updated_user_list, 'testaccount123')
    test_user2 = get_user_from_json(updated_user_list, 'testaccount231')
    test_user3 = get_user_from_json(updated_user_list, 'testaccount312')

    assert bool(test_user1), 'Account not found - Account#1'
    assert test_user1.get('full_name') == 'Foo Bar', 'Full name mismatch: Account#1'
    assert test_user1.get('status') == 'inactive', 'User status mismatch: Account#1'
    assert test_user1.get('role') == 'user', 'Role mismatch: Account#1'
    assert test_user1.get('need_password_change') == False, 'Password change status mismatch: Account#1'

    assert bool(test_user2), 'Account not found - Account#2'
    assert test_user2.get('full_name') == 'Baz Quz', 'Full name mismatch: Account#2'
    assert test_user2.get('status') == 'active', 'User status mismatch: Account#2'
    assert test_user2.get('role') == 'admin', 'Role mismatch: Account#2'
    assert test_user2.get('need_password_change') == True, 'Password change status mismatch: Account#2'

    assert bool(test_user3), 'Account not found - Account#3'
    assert test_user3.get('full_name') == 'Alice B.', 'Full name mismatch: Account#3'
    assert test_user3.get('status') == 'active', 'User status mismatch: Account#3'
    assert test_user3.get('role') == 'monitor', 'Role mismatch: Account#3'
    assert test_user3.get('need_password_change') == False, 'Password change status mismatch: Account#3'


def test_delete_user(run: ClientRunnerFunc):
    print("[ Delete user ]")
    pass


def get_user_from_json(users: list, username: str) -> dict:
    for user in users:
        if user.get('username') == username:
            return user

    return {}