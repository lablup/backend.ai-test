from __future__ import annotations

import os
from pathlib import Path
import re

import pytest

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