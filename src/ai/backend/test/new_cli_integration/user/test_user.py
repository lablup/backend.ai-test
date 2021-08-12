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

    test_user = get_user_from_json(user_list, 'testaccount1')

    if not bool(test_user):
        # Add user
        add_arguments = ['--output=json', 'admin', 'user', 'add', '-u', 'testaccount1', '-n', 'John Doe',
                         '--need-password-change', 'default', 'testaccount1@lablup.com', '1q2w3e4r']
        with closing(run(add_arguments)) as p:
            p.expect(EOF)
            assert 'User testaccount1@lablup.com is created' in p.before.decode(), 'Account add error'

    # Check if user is added
    with closing(run(['--output=json', 'admin', 'user', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        user_list = loaded.get('items')

        assert isinstance(user_list, list), 'Expected user list'
        added_user = get_user_from_json(user_list, 'testaccount1')
        assert bool(added_user), 'Added account doesn\'t exist'
        assert added_user.get('email') == 'testaccount1@lablup.com', 'E-mail mismatch'
        assert added_user.get('full_name') == 'John Doe', 'Full name mismatch'
        assert added_user.get('status') == 'active', 'User status mismatch'
        assert added_user.get('need_password_change') == True, 'Password change status mismatch'


def test_update_user(run: ClientRunnerFunc):
    print("[ Update user ]")
    pass


def test_delete_user(run: ClientRunnerFunc):
    print("[ Delete user ]")
    pass


def get_user_from_json(users: list, username: str) -> dict:
    for user in users:
        if user.get('username') == username:
            return user

    return {}