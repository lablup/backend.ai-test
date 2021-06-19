import functools
import re

import pytest

from ...utils.cli import ClientRunnerFunc

_rs = functools.partial(re.search, flags=re.M)  # shortcut


@pytest.mark.dependency(
    depends=["domain_crud"],
    scope="package",
)
def test_group(temp_domain: str, run: ClientRunnerFunc) -> None:
    pass
