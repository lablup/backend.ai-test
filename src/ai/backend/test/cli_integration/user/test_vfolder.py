import json
from contextlib import closing

from ...utils.cli import EOF, ClientRunnerFunc


def test_create_vfolder(run: ClientRunnerFunc):
    pass


def test_rename_vfolder(run: ClientRunnerFunc):
    pass


def test_delete_vfolder(run: ClientRunnerFunc):
    pass


def test_list_vfolder(run: ClientRunnerFunc):
    with closing(run(['--output=json', 'vfolder', 'list'])) as p:
        p.expect(EOF)
        decoded = p.before.decode()
        loaded = json.loads(decoded)
        folder_list = loaded.get('items')
        assert isinstance(folder_list, list)