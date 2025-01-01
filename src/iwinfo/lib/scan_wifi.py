# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Deals with scanning wifi
"""
import time
from .run_prog import run_prog
from .parse_iw_scan import parse_iw_scan

def get_iw_scan(dev:str, iwscan:'IwScanDevice'):
    """
    Use iw scan to get info from this device
    Requres priv capabilites - see class_iw for more info
    NB this can occasionally get device busy - so try a couple times
    """
    max_tries = 3
    count = 0
    naptime = 0.2
    while count < max_tries:
        result = _iw_scan(dev, quiet=True)
        if result:
            parse_iw_scan(result, iwscan)
            break
        time.sleep(naptime)

def _iw_scan(dev:str, quiet:bool=True):
    """
    Use iw scan to get info from this device
    Requres priv capabilites - see class_iw for more info
    """
    pargs = ['/usr/bin/iw', 'dev', dev, 'scan']
    [ret, out, err] = run_prog(pargs)
    if ret != 0:
        if err and not quiet:
            print(err)
        return None
    result = out.splitlines()
    return result
