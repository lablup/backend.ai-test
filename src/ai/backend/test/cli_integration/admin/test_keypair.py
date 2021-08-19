import json
from contextlib import closing

from ...utils.cli import EOF, ClientRunnerFunc


def test_add_keypair(run: ClientRunnerFunc):
    pass


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