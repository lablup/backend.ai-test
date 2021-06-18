"""
An integration test for the Backend.AI admin APIs.

It runs and checks the result of a series of CRUD commands for various entities including domain, group,
user, scaling group, resource policy, resource preset, etc.

As usual `backend.ai` commands, this script assumes that the environment variables are correctly
configured to access the manager API.
"""

import functools
from pathlib import Path
import re

from ...utils.cli import run as _run, EOF

_rs = functools.partial(re.search, flags=re.M)  # shortcut


def test_domain(client_bin: Path, client_environ: dict[str, str]) -> None:
    print("[ Domain ]")
    run = functools.partial(_run, env=client_environ)

    domain_name = 'testing'
    p = run([
        client_bin, 'admin', 'domains', 'add',
        '-i',
        '-d', 'test domain',
        domain_name,
    ])
    p.expect("is created")
    p.close()

    try:
        p = run([
            client_bin, 'admin', 'domain', '-n', domain_name,
        ])
        p.expect(EOF)
        assert _rs(f"^Name +{domain_name}".encode(), p.before)
        assert _rs(rb"^Description +test domain", p.before)
        assert _rs(rb"^Active\? +False", p.before)
        p.close()

        p = run([
            client_bin, 'admin', 'domains',
        ])
        p.expect(EOF)
        assert _rs(rb"^Name +Description +Active?", p.before)
        assert _rs(f"^{domain_name} +test domain +False".encode(), p.before)
        p.close()

        run([
            client_bin, 'admin', 'domains', 'update',
            '--is-active', 'true',
            '--total-resource-slots', '{"cpu":999,"mem":"999g"}',
            '--allowed-vfolder-hosts', 'local:volume1',
            '--allowed-vfolder-hosts', 'local:volume2',
            '--allowed-docker-registries', 'cr.backend.ai',
            domain_name,
        ])
        run([
            client_bin, 'admin', 'domains',
        ])
        run([
            client_bin, 'admin', 'domains', 'delete',
            domain_name,
        ])
        run([
            client_bin, 'admin', 'domains',
        ])
    finally:
        p = run([
            client_bin, 'admin', 'domains', 'purge',
            domain_name,
        ])
        p.expect_exact("Are you sure?")
        p.sendline("Y")
        run([
            client_bin, 'admin', 'domains',
        ])


def test_group():
    print("[ Group ]")
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
