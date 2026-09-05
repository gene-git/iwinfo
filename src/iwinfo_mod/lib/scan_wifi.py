# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Deals with scanning wifi
"""
import time
from .parse_iw_scan import parse_iw_scan
from ._iw_hosts import IwHosts
from .run_cmd import Command


def get_iw_scan(device_name: str, iw_hosts: IwHosts):
    """
    Use iw scan to get info from this device
    Requres priv capabilites - see class_iw for more info
    NB this can occasionally get device busy - so try a couple times
    """
    max_tries = 3
    count = 0
    naptime = 0.2
    permitted: bool = True

    while permitted and count < max_tries:
        count += 1
        (permitted, result) = _iw_scan(device_name)
        if result:
            hosts = parse_iw_scan(result)
            iw_hosts.add_hosts(hosts)
            break
        time.sleep(naptime)


def _iw_scan(device_name: str) -> tuple[bool, list[str]]:
    """
    Use iw scan to get info from this device
    Requres priv capabilites - see class_iw for more info
    :returns: (permistted, result)
    """
    command = Command()

    result: list[str] = []
    pargs = ['/usr/bin/iw', 'dev', device_name, 'scan']
    result = command.run(pargs)

    permitted = True
    if command.ret != 0:
        if command.err and 'not permitted' in command.err:
            permitted = False
            print(f' Not permitted to scan : {device_name}')

    return (permitted, result)
