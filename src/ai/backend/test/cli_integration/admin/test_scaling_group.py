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
    # Update scaling group
    with closing(run(['admin', 'scaling-group', 'update', '-d', 'Test scaling group updated',
                      '--driver', 'non-static', '--scheduler', 'lifo', 'testgroup1'])) as p:
        p.expect(EOF)
        assert 'Scaling group testgroup1 is updated.' in p.before.decode(), \
            'Test scaling group not updated successfully'

    # Check if scaling group is updated
    with closing(run(['--output=json', 'admin', 'scaling-group', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        scaling_group_list = loaded.get('items')
        assert isinstance(scaling_group_list, list), 'Scaling group list not printed properly'

    testgroup = get_scaling_group_from_list(scaling_group_list, 'testgroup1')

    assert bool(testgroup), 'Test scaling group doesn\'t exist'
    assert testgroup.get('description') == 'Test scaling group updated', 'Scaling group description mismatch'
    assert testgroup.get('is_active') == True, 'Scaling group active status mismatch'
    assert testgroup.get('driver') == 'non-static', 'Scaling group driver mismatch'
    assert testgroup.get('scheduler') == 'lifo', 'Scaling group scheduler mismatch'



def test_delete_scaling_group(run: ClientRunnerFunc):
    with closing(run(['admin', 'scaling-group', 'delete', 'testgroup1'])) as p:
        p.expect(EOF)
        assert 'Scaling group is deleted: testgroup1.' in p.before.decode(), 'Test scaling group deletion unsuccessful'


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