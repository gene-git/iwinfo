# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Parse output if 'iw scan'
"""
from .parse_tools import found_access_point
from ._iw_host import IwHost


def parse_iw_scan(iw_output: list[str]) -> list[IwHost]:
    """
    Extract what we need from iw scan output from one wireless device.

    Args:
        iw_output (list[str]):
        Output from running "iw scan"

    Returns:
        list[IwHost]:
        list of "IwHost".

    """
    keys = ['SSID', 'freq', 'signal']

    hosts: list[IwHost] = []
    if not iw_output:
        return hosts

    host: IwHost
    for raw_row in iw_output:
        row = raw_row.strip()

        bssid = found_access_point(raw_row)
        if bssid:
            host = IwHost(bssid)
            hosts.append(host)
            continue

        row_split = row.split(' ', 1)
        for key in keys:
            if row_split[0].startswith(key):
                if len(row_split) > 1:
                    value = row_split[1]
                    attrib = key.lower().replace(' ', '_')
                    setattr(host, attrib, value)
    return hosts
