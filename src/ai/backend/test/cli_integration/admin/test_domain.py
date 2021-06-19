from contextlib import closing
import functools
import re

import pytest

from ...utils.cli import EOF, ClientRunnerFunc

_rs = functools.partial(re.search, flags=re.M)  # shortcut


@pytest.mark.dependency(name="domain_crud")
def test_domain(domain_name: str, run: ClientRunnerFunc) -> None:
    with closing(run([
        'admin', 'domains', 'add',
        '-i',
        '-d', 'test domain',
        domain_name,
    ])) as p:
        p.expect("is created")

    try:
        with closing(run([
            'admin', 'domain', '-n', domain_name,
        ])) as p:
            p.expect(EOF)
            assert _rs(f"^Name +{domain_name}".encode(), p.before)
            assert _rs(rb"^Description +test domain", p.before)
            assert _rs(rb"^Active\? +False", p.before)

        with closing(run([
            'admin', 'domains',
        ])) as p:
            p.expect(EOF)
            assert _rs(rb"^Name +Description +Active?", p.before)
            assert _rs(f"^{domain_name} +test domain +False".encode(), p.before)

        with closing(run([
            'admin', 'domains', 'update',
            '--is-active', 'true',
            '--total-resource-slots', '{"cpu":999,"mem":"999g"}',
            '--allowed-vfolder-hosts', 'local:volume1',
            '--allowed-vfolder-hosts', 'local:volume2',
            '--allowed-docker-registries', 'cr.backend.ai',
            domain_name,
        ])) as p:
            pass

        with closing(run([
            'admin', 'domains',
        ])) as p:
            pass

        with closing(run([
            'admin', 'domains', 'delete',
            domain_name,
        ])) as p:
            pass

        with closing(run([
            'admin', 'domains',
        ])) as p:
            pass
    finally:
        with closing(run([
            'admin', 'domains', 'purge',
            domain_name,
        ])) as p:
            p.expect_exact("Are you sure?")
            p.sendline("Y")

        with closing(run([
            'admin', 'domains',
        ])) as p:
            pass


def test_user():
    print("[ User ]")
    pass


def test_keypair():
    print("[ KeyPair ]")
    pass


def test_scaling_group():
    print("[ ScalingGroup ]")
    pass


def test_resource_policy():
    print("[ ResourcePolicy ]")
    pass


def test_resource_preset():
    print("[ ResourcePreset ]")
    pass
