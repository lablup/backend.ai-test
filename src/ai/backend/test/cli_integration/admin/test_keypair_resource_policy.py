import json
from contextlib import closing

from ...utils.cli import EOF, ClientRunnerFunc


def test_add_keypair_resource_policy(run: ClientRunnerFunc):
    pass


def test_update_keypair_resource_policy(run: ClientRunnerFunc):
    pass


def test_delete_keypair_resource_policy(run: ClientRunnerFunc):
    pass


def test_list_keypair_resource_policy(run: ClientRunnerFunc):
    print("[ List keypair resource policy ]")
    with closing(run(['--output=json', 'admin', 'keypair-resource-policy', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        krp_list = loaded.get('items')
        assert isinstance(krp_list, list), 'Keypair resource policy list not printed properly'

