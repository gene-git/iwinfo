# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Parse helpers
"""

def found_access_point(row:str) -> str:
    """
    check for new access point :
      - 'Connected to xx:xx:xx:xx:xx:xx (on wlan0)' (iw dev xxx link)
       'Station xx:xx:xx:xx:xx:xx (on wlan0)       (iw dev xxx station dump)
      - 'BSS xx:xx:xx:xx:xx:xx(on wlan0)'           (iw dev xxx scan)
    """
    bssid = None
    if not row:
        return bssid

    row_split = row.split()
    if row.startswith('Connected to'):
        bssid = row_split[2]
        #dev = row_split[4].split(')')[0]

    elif row.startswith('Station'):
        bssid = row_split[1]
        #dev = row_split[3].split(')')[0]

    elif row.startswith('BSS'):
        bssid = row_split[1].split('(')[0]
        #dev = row_split[2].split(')')[0]

    return bssid
