from __future__ import annotations

import click

from .context import CLIContext


@click.group(invoke_without_command=True, context_settings={'help_option_names': ['-h', '--help']})
@click.pass_context
def main(ctx: click.Context) -> None:
    """
    The testing toolkit for Backend.AI
    """
    ctx.obj = CLIContext()


if __name__ == '__main__':
    main()
