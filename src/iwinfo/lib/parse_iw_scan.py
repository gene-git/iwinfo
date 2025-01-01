# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Parse output if 'iw scan'
"""
from .parse_tools import found_access_point

def parse_iw_scan(iw_output:[str], iwscan:'IwScanDevice') -> None:
    """
    Extract what we need from iw scan output from one iw device.
    Then Update the corresponding IwScanDevice with what was found
    Updates the list of IwScanItems
    """
    keys = ['SSID', 'freq', 'signal']

    scan_item = None
    for raw_row in iw_output:
        row = raw_row.strip()

        bssid = found_access_point(raw_row)
        if bssid:
            scan_item = iwscan.add_item(bssid)
            continue

        #row_split = row.split(':', 1)
        row_split = row.split(' ', 1)
        for key in keys:
            if row_split[0].startswith(key):
                if len(row_split) > 1:
                    value = row_split[1]
                    attrib =  key.lower().replace(' ', '_')
                    setattr(scan_item, attrib, value)
