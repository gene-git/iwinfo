# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
External program execution
"""
# pylint: disable=too-few-public-methods
from pyconcurrent import run_prog


class Command:
    """
    Run program and any track errors.
    """
    def __init__(self):
        self.ret: int = 0
        self.err: str = ''

    def run(self, pargs: list[str]) -> list[str]:
        """
        Run program and args in pargs.

        :paraam pargs: List of program and arguments.
        :returns: List of lines output by the program
                  self.ret is set to exit status
                  self.err holds the stderr from the program
        """
        result: list[str] = []
        (self.ret, out, self.err) = run_prog(pargs)
        if out:
            result = out.splitlines()
        return result


def run_cmd(pargs: list[str]) -> list[str]:
    """
    Run cmd with provided arguments and return stdout.

    Variation of run_prog with simpler calling convention.
    :param pargs: Standard list of command and arguments.
    :returns: list of lines of stdout from running program.
              May be empty list.
    """
    command = Command()
    result = command.run(pargs)
    if command.ret != 0:
        if command.err:
            print(command.err)
    return result
