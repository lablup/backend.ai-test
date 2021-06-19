import functools
import re

import pytest

from ...utils.cli import ClientRunnerFunc

_rs = functools.partial(re.search, flags=re.M)  # shortcut
_dep_root = "src/ai/backend/test/cli_integration"


@pytest.mark.dependency(
    depends=[f"{_dep_root}/admin/test_domain.py::test_domain"],
    scope="package",
)
def test_group(temp_domain: str, run: ClientRunnerFunc) -> None:
    pass
