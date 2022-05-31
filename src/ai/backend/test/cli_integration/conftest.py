from __future__ import annotations

import os
import re
import secrets
from collections import namedtuple
from contextlib import closing
from pathlib import Path
from typing import Callable, Iterator, Sequence, Tuple

import pexpect
import pytest
from faker import Faker

from ai.backend.test.utils.cli import ClientRunnerFunc, EOF, run as _run

_rx_env_export = re.compile(r"^(export )?(?P<key>\w+)=(?P<val>.*)$")


@pytest.fixture(scope="session")
def client_venv() -> Path:
    p = os.environ.get("BACKENDAI_TEST_CLIENT_VENV", None)
    if p is None:
        raise RuntimeError("Missing BACKENDAI_TEST_CLIENT_VENV env-var!")
    return Path(p)


@pytest.fixture(scope="session")
def client_bin(
    client_venv: Path,
) -> Path:
    return client_venv / 'bin' / 'backend.ai'


@pytest.fixture(scope="session")
def client_environ() -> dict[str, str]:
    p = os.environ.get("BACKENDAI_TEST_CLIENT_ENV", None)
    if p is None:
        raise RuntimeError("Missing BACKENDAI_TEST_CLIENT_ENV env-var!")
    envs = {}
    sample_admin_sh = Path(p)
    if sample_admin_sh.exists():
        lines = sample_admin_sh.read_text().splitlines()
        for line in lines:
            if m := _rx_env_export.search(line.strip()):
                envs[m.group('key')] = m.group('val')
    return envs


@pytest.fixture(scope="session")
def run(client_bin: Path, client_environ: dict[str, str]) -> Iterator[ClientRunnerFunc]:

    def run_impl(cmdargs: Sequence[str | Path], *args, **kwargs) -> pexpect.spawn:
        return _run([client_bin, *cmdargs], *args, **kwargs, env=client_environ)

    yield run_impl


@pytest.fixture
def domain_name() -> str:
    return f"testing-{secrets.token_hex(8)}"


@pytest.fixture
def temp_domain(domain_name: str, run: ClientRunnerFunc) -> Iterator[str]:
    run(['admin', 'domains', 'add', domain_name])
    print("==== temp_domain created ====")
    try:
        yield domain_name
    finally:
        with closing(run(['admin', 'domains', 'purge', domain_name])) as p:
            p.expect_exact("Are you sure?")
            p.sendline("Y")
            p.expect(EOF)


@pytest.fixture(scope="module")
def users(n: int = 3) -> Tuple[dict]:
    fake = Faker()
    return tuple(
        {
            'username': fake.user_name(),
            'full_name': fake.name(),
            'email': fake.email(),
            'password': fake.password(8),
            'role': ['user', 'admin', 'monitor'][i % 3],
            'status': ['active', 'inactive', 'before-verification', 'deleted'][i % 4],
            'need_password_change': [True, False, True][i % 3],
        }
        for i in range(n)
    )


KeypairOption = namedtuple('KeypairOption',
                           ('is_active', 'is_admin', 'rate_limit', 'resource_policy'))


@pytest.fixture(scope="module")
def keypair_options() -> Tuple[KeypairOption]:
    return tuple([
        KeypairOption(is_active=False, is_admin=True, rate_limit=25000, resource_policy='default'),
        KeypairOption(is_active=True, is_admin=False, rate_limit=None, resource_policy='default'),
        KeypairOption(is_active=True, is_admin=True, rate_limit=30000, resource_policy='default'),
    ])


@pytest.fixture(scope="module")
def new_keypair_options() -> Tuple[KeypairOption]:
    return tuple([
        KeypairOption(is_active=True, is_admin=False, rate_limit=15000, resource_policy='default'),
        KeypairOption(is_active=False, is_admin=True, rate_limit=15000, resource_policy='default'),
        KeypairOption(is_active=False, is_admin=False, rate_limit=10000, resource_policy='default'),
    ])


@pytest.fixture
def gen_username() -> Callable[None, str]:
    return lambda: Faker().user_name()


@pytest.fixture
def gen_fullname() -> Callable[None, str]:
    return lambda: Faker().name()
