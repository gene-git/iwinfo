# SPDX-License-Identifier: MIT
# Copyright (c) 2023 Gene C
"""
Parse output if 'iw link'
"""
from .parse_tools import found_access_point

def parse_iw_link(iw_output:[str], iwours:'IwOurs') -> None:
    """
    Extract what we need from iw output
    Update the corresponding iwours attributes
    """
    keys = ['SSID', 'freq', 'signal', 'rx bitrate', 'tx bitrate']

    for row in iw_output:
        row = row.strip()

        bssid = found_access_point(row)
        if bssid:
            # AP line
            iwours.ap_bssid = bssid
            continue

        row_split = row.split(':', 1)
        for key in keys:
            if key in row_split[0]:
                if len(row_split) > 1:
                    value = row_split[1]
                    attrib =  key.lower().replace(' ', '_')
                    setattr(iwours, attrib, value)
