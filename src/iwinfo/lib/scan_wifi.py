# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Deals with scanning wifi
"""
from typing import (List)
import time
from .run_prog import run_cmd
from .parse_iw_scan import parse_iw_scan
from ._iw_hosts import IwHosts


def get_iw_scan(device_name: str, iw_hosts: IwHosts):
    """
    Use iw scan to get info from this device
    Requres priv capabilites - see class_iw for more info
    NB this can occasionally get device busy - so try a couple times
    """
    max_tries = 3
    count = 0
    naptime = 0.2
    while count < max_tries:
        result = _iw_scan(device_name)
        if result:
            hosts = parse_iw_scan(result)
            iw_hosts.add_hosts(hosts)
            break
        time.sleep(naptime)


def _iw_scan(device_name: str) -> List[str]:
    """
    Use iw scan to get info from this device
    Requres priv capabilites - see class_iw for more info
    """
    result: List[str] = []
    pargs = ['/usr/bin/iw', 'dev', device_name, 'scan']
    result = run_cmd(pargs)
    return result
