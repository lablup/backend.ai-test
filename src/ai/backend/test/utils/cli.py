from __future__ import annotations

from typing import (
    Sequence,
)

import pexpect


EOF = pexpect.EOF
TIMEOUT = pexpect.TIMEOUT


def run(
    args: Sequence[str],
    *,
    default_timeout: int = 5,
    **kwargs,
) -> pexpect.spawn:
    p = pexpect.spawn(
        str(args[0]),
        [str(arg) for arg in args[1:]],
        timeout=default_timeout,
        **kwargs,
    )
    return p