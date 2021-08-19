import json
from contextlib import closing

from ...utils.cli import EOF, ClientRunnerFunc


def test_list_storage(run: ClientRunnerFunc):
    print("[ List storage ]")
    with closing(run(['--output=json', 'admin', 'storage', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        storage_list = loaded.get('items')
        assert isinstance(storage_list, list), 'Storage list not printed properly'


def test_info_storage(run: ClientRunnerFunc):
    pass
