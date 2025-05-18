# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
run_prog.py
 Run program as a subprocess and return status, stdout and stderr
 gc 2022-04-17
"""
from typing import (List, Tuple)
import subprocess
from subprocess import SubprocessError


def run_prog(pargs,
             input_str: str = '',
             stdout: int = subprocess.PIPE,
             stderr: int = subprocess.PIPE
             ) -> Tuple[int, str, str]:
    """
    Run external program using subprocess
     pargs     - array of program + arguments ['prog', 'arg1', ...]
     input_str - if proviced will be sent to program's stdin
     stdout    - default is subprocess.PIPE and passed back as 'output'
     stderr    - default is subprocess.PIPE and passed back as 'errors'
    """
    bstring = None
    if input_str:
        bstring = bytearray(input_str, 'utf-8')

    try:
        ret = subprocess.run(pargs,
                             input=bstring,
                             stdout=stdout,
                             stderr=stderr,
                             check=False)

    except (FileNotFoundError, SubprocessError) as err:
        return (-1, '', str(err))

    retc = ret.returncode
    output: str = ''
    errors: str = ''

    if ret.stdout:
        output = str(ret.stdout, 'utf-8', errors='ignore')

    if ret.stderr:
        errors = str(ret.stderr, 'utf-8', errors='ignore')

    return (retc, output, errors)


def run_cmd(pargs: List[str]) -> List[str]:
    """
    Run cmd with provided arguments and return stdout.

    Variation of run_prog with simpler calling convention.
    Args:
        pargs (List[str]):
        Standard list of command and arguments.
    Returns:
        List[str]:
        List of lines of stdout from running program.
        May be empty list.

    """
    result: List[str] = []

    (ret, out, err) = run_prog(pargs)
    if ret != 0:
        if err:
            print(err)
        return result
    if out:
        result = out.splitlines()
    return result
