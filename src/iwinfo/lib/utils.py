# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Support tools
"""
import os
from typing import Iterable
import re

def dir_exists(indir):
    """
    Confirm indir exists and is a directory
    """
    return bool(os.path.exists(indir) and os.path.isdir(indir))

def filelist(indir, name_type='name'):
    """
    read directory and return list of files or links
    name_type : name or path
    """
    flist = []
    if dir_exists(indir):
        scan = os.scandir(indir)
        for item in scan:
            if item.is_file() or item.is_symlink():
                if name_type == 'path':
                    file = item.path
                else:
                    file = item.name
                flist.append(file)
        scan.close()
    return flist

def open_file(path, mode):
    """
    Open a file and return file object
    """
    # pylint: disable=W1514,R1732
    try:
        fobj = open(path, mode)
    except OSError as err:
        print(f'Error opening file {path} : {err}')
        fobj = None
    return fobj

def all_in(col1:Iterable, col2:Iterable):
    """ return true if every element of col1 is in col2 """
    s_col1 = set(col1)
    s_col2 = set(col2)
    return s_col1.intersection(s_col2) == s_col1

def any_in(col1:Iterable, col2:Iterable):
    """ return true if any element of col1 is in col2 """
    s_col1 = set(col1)
    s_col2 = set(col2)
    return s_col1.intersection(s_col2) != set()

def strip_ansi(txt:str) -> str:
    """
    Strip ansi escapes
    """
    ansi_escape = re.compile(
               br'(?:\x1B[@-Z\\-_]|[\x80-\x9A\x9C-\x9F]|(?:\x1B\[|\x9B)[0-?]*[ -/]*[@-~])'
            )
    clean = ansi_escape.sub(b'', txt.encode())
    clean = clean.decode().strip()
    return clean
