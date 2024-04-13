# SPDX-License-Identifier: MIT
# Copyright (c) 2023 Gene C
"""
Support tools
"""
import os

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
