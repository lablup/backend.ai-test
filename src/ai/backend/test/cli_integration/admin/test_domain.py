"""
An integration test for the Backend.AI admin APIs.

It runs and checks the result of a series of CRUD commands for various entities including domain, group,
user, scaling group, resource policy, resource preset, etc.

As usual `backend.ai` commands, this script assumes that the environment variables are correctly
configured to access the manager API.
"""

from subprocess import run

import click


def test_domain():
    print("[ Domain ]")
    run([
        'backend.ai', 'admin', 'domains', 'add',
        '-i',
        '-d', 'test domain',
        'testing',
    ])
    run([
        'backend.ai', 'admin', 'domains',
    ])
    run([
        'backend.ai', 'admin', 'domains', 'update',
        '--is-active', 'true',
        '--total-resource-slots', '{"cpu":999,"mem":"999g"}',
        '--allowed-vfolder-hosts', 'local:volume1',
        '--allowed-vfolder-hosts', 'local:volume2',
        '--allowed-docker-registries', 'cr.backend.ai',
        'testing',
    ])
    run([
        'backend.ai', 'admin', 'domains',
    ])
    run([
        'backend.ai', 'admin', 'domains', 'delete',
        'testing',
    ])
    run([
        'backend.ai', 'admin', 'domains',
    ])
    run([
        'backend.ai', 'admin', 'domains', 'purge',
        'testing',
    ])
    run([
        'backend.ai', 'admin', 'domains',
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
