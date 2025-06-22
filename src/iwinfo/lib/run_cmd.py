# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
External program execution
"""
from .run_prog import run_prog

def run_cmd(pargs: list[str]) -> list[str]:
    """
    Run cmd with provided arguments and return stdout.

    Variation of run_prog with simpler calling convention.
    Args:
        pargs (list[str]):
        Standard list of command and arguments.
    Returns:
        list[str]:
        list of lines of stdout from running program.
        May be empty list.

    """
    result: list[str] = []

    (ret, out, err) = run_prog(pargs)
    if ret != 0:
        if err:
            print(err)
        return result
    if out:
        result = out.splitlines()
    return result
