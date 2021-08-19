import json
from contextlib import closing

from ...utils.cli import EOF, ClientRunnerFunc


def test_add_scaling_group(run: ClientRunnerFunc):
    # Create scaling group
    with closing(run(['admin', 'scaling-group', 'add', '-d', 'Test scaling group', '-i', '--driver', 'static',
                      '--scheduler', 'fifo', 'testgroup1'])) as p:
        p.expect(EOF)
        assert 'Scaling group name testgroup1 is created.' in p.before.decode(), \
            'Test scaling group not created successfully'

    # Check if scaling group is created
    with closing(run(['--output=json', 'admin', 'scaling-group', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        scaling_group_list = loaded.get('items')
        assert isinstance(scaling_group_list, list), 'Scaling group list not printed properly'

    testgroup = get_scaling_group_from_list(scaling_group_list, 'testgroup1')

    assert bool(testgroup), 'Test scaling group doesn\'t exist'
    assert testgroup.get('description') == 'Test scaling group', 'Scaling group description mismatch'
    assert testgroup.get('is_active') == False, 'Scaling group active status mismatch'
    assert testgroup.get('driver') == 'static', 'Scaling group driver mismatch'
    assert testgroup.get('scheduler') == 'fifo', 'Scaling group scheduler mismatch'


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


def get_scaling_group_from_list(scaling_groups: list, groupname: str) -> dict:
    for sg in scaling_groups:
        if sg.get('name') == groupname:
            return sg

    return {}