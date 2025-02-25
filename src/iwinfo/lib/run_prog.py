# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
run_prog.py
 Run program as a subprocess and return status, stdout and stderr
 gc 2022-04-17
"""
import subprocess
from subprocess import SubprocessError

def run_prog(pargs, input_str=None,stdout=subprocess.PIPE,stderr=subprocess.PIPE):
    """
    Run external program using subprocess
        pargs       - array of program and any arguments ['prog', 'arg1', ...]
        input_str   - if proviced will be sent to program's stdin
        stdout      - if not provided uses subprocess.PIPE and passed back as 'output'
        stderr      - if not provided uses subprocess.PIPE and passed back as 'errors'
    """
    bstring = None
    if input_str:
        bstring = bytearray(input_str,'utf-8')

    try:
        ret = subprocess.run(pargs, input=bstring, stdout=stdout, stderr=stderr,check=False)
    except (FileNotFoundError, SubprocessError) as err:
        return [-1, None, err]

    retc = ret.returncode
    output = None
    errors = None
    if ret.stdout :
        output = str(ret.stdout, 'utf-8',errors='ignore')
    if ret.stderr :
        errors = str(ret.stderr, 'utf-8',errors='ignore')

    return [retc, output, errors]
