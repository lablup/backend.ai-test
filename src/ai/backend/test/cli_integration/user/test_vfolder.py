import json
from contextlib import closing

from ...utils.cli import EOF, ClientRunnerFunc


def test_create_vfolder(run: ClientRunnerFunc):
    # Create group first TODO: Unannotate the following code after group deletion issue is resolved.
    # with closing(run(['admin', 'group', 'add', 'default', 'testgroup'])) as p:
    #     p.expect(EOF)
    #     assert 'Group name testgroup is created in domain default' in p.before.decode(), \
    #         'Test group not created successfully.'

    # Create vfolder
    with closing(run(['vfolder', 'create',  '-p', 'rw', 'testfolder1', 'local:volume1'])) as p:
        p.expect(EOF)
        assert 'Virtual folder "testfolder1" is created' in p.before.decode(), 'Test folder1 not created successfully.'

    with closing(run(['vfolder', 'create', '-p', 'ro', 'testfolder2', 'local:volume1'])) as p:
        p.expect(EOF)
        assert 'Virtual folder "testfolder2" is created' in p.before.decode(), 'Test folder2 not created successfully.'

    # Check if vfolder is created
    with closing(run(['--output=json', 'vfolder', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        folder_list = loaded.get('items')
        assert isinstance(folder_list, list), 'Error in listing test folders!'

    testfolder1 = get_folder_from_list(folder_list, 'testfolder1')
    testfolder2 = get_folder_from_list(folder_list, 'testfolder2')

    assert bool(testfolder1), 'Test folder 1 doesn\'t exist!'
    assert testfolder1.get('permission') == 'rw', 'Test folder 1 permission mismatch.'

    assert bool(testfolder2), 'Test folder 2 doesn\'t exist!'
    assert testfolder2.get('permission') == 'ro', 'Test folder 2 permission mismatch.'


def test_rename_vfolder(run: ClientRunnerFunc):
    # Rename vfolder
    with closing(run(['vfolder', 'rename', 'testfolder1', 'testfolder3'])) as p:
        p.expect(EOF)
        assert 'Renamed' in p.before.decode(), 'Test folder1 not renamed successfully.'

    # Check if vfolder is updated
    with closing(run(['--output=json', 'vfolder', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        folder_list = loaded.get('items')
        assert isinstance(folder_list, list), 'Error in listing test folders!'

    testfolder3 = get_folder_from_list(folder_list, 'testfolder3')
    assert bool(testfolder3), 'Test folder 3 doesn\'t exist!'


def test_delete_vfolder(run: ClientRunnerFunc):
    with closing(run(['vfolder', 'delete', 'testfolder2'])) as p:
        p.expect(EOF)
        assert 'Deleted' in p.before.decode(), 'Test folder 2 not deleted successfully.'

    with closing(run(['vfolder', 'delete', 'testfolder3'])) as p:
        p.expect(EOF)
        assert 'Deleted' in p.before.decode(), 'Test folder 3 not deleted successfully.'


def test_list_vfolder(run: ClientRunnerFunc):
    with closing(run(['--output=json', 'vfolder', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        folder_list = loaded.get('items')
        assert isinstance(folder_list, list)


def get_folder_from_list(folders: list, foldername: str) -> dict:
    for folder in folders:
        if folder.get('name', '') == foldername:
            return folder

    return {}

