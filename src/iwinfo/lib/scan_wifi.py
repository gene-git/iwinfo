# SPDX-License-Identifier: MIT
# Copyright (c) 2023 Gene C
"""
Deals with scanning wifi
"""
from .run_prog import run_prog
from .parse_iw_scan import parse_iw_scan

def get_iw_scan(dev:str, iwscan:'IwScan'):
    """
    Use iw scan to get info from this device
    Requres priv capabilites - see class_iw for more info
    """
    # pylint: disable=duplicate-code
    pargs = ['/usr/bin/iw', 'dev', dev, 'scan']
    [ret, out, err] = run_prog(pargs)
    if ret != 0:
        if err:
            print(err)
        return
    result = out.splitlines()
    parse_iw_scan(result, iwscan)
