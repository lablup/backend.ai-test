import json
from contextlib import closing

from ...utils.cli import EOF, ClientRunnerFunc


def test_add_scaling_group(run: ClientRunnerFunc):
    pass


def test_update_scaling_group(run: ClientRunnerFunc):
    pass


def test_delete_scaling_group(run: ClientRunnerFunc):
    pass


def test_list_scaling_group(run: ClientRunnerFunc):
    with closing(run(['--output=json', 'admin', 'scaling-group', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        scaling_group_list = loaded.get('items')
        assert isinstance(scaling_group_list, list), 'Scaling group list not printed properly'