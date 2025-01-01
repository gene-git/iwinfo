# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Parse output if 'iw list'
"""
# pylint: disable=too-many-branches,too-many-statements,too-few-public-methods
class IwPhyInfo:
    """ wifi capabilities by phy """
    def __init__(self, phy_name):
        self.phy = phy_name
        self.interface = None
        self.addr = None
        self.num_bands = 0
        self.freq: [str] = []
        self.wifi_type = None
        self.ieee_type = None

    def report(self):
        """ report what we found """
        wifi_type = self.wifi_type or 'wifi-?'
        ieee_type = self.ieee_type or '80211.?'
        ieee_type = f'({ieee_type})'
        freq = '-'
        if self.freq:
            freq = sorted(list(set(self.freq)))
            freq = ' '.join(freq)

        print(f'{"":6s} {wifi_type:>10s} {ieee_type:<10s} {self.num_bands:>3d}-bands : {freq}')

def parse_iw_list(iw_output:[str]) -> dict:
    """
    Extract what we need from iw output
    """
    phys = {}
    phy = None
    for row in iw_output:
        row = row.strip()
        srow = row.split()
        if row.startswith('Wiphy phy'):
            # new phy
            name = srow[1]
            phy = IwPhyInfo(name)
            phys[name] = phy
            continue

        if row.startswith('Band '):
            phy.num_bands += 1
            phy.wifi_type = 'wifi-1'

            phy.wifi_type = 'wifi-1'
            phy.ieee_type = '802.11b'
            if phy.num_bands >= 2:
                phy.wifi_type = 'wifi-3'
                phy.ieee_type = '802.11g'
            elif phy.num_bands >= 3:
                phy.wifi_type = 'wifi-6E'
                phy.ieee_type = '802.11ax'
            continue


        if '* 5180.0 MHz [36]' in row:
            phy.freq.append('5-GHz')
            if phy.num_bands == 1:
                phy.wifi_type = 'wifi-2'
                phy.ieee_type = '802.11a'
            else:
                phy.wifi_type = 'wifi-4'
                phy.ieee_type = '802.11n'
            continue

        if 'HT Max' in row:
            # has 2 bands - no need to check
            phy.wifi_type = 'wifi-4'
            phy.ieee_type = '802.11n'
            continue

        if 'VHT Capabilities' in row:
            phy.wifi_type = 'wifi-5'
            phy.ieee_type = '802.11ac'
            continue

        if 'HE RX MCS and NSS set <= 80 MHz' in row:
            phy.wifi_type = 'wifi-6'
            phy.ieee_type = '802.11ax'
            continue

        if '* 2412.0 MHz [1]' in row:
            phy.freq.append('2.4-GHz')
            continue

        if '* 5955.0 MHz [1]' in row:
            phy.wifi_type = 'wifi-6E'
            phy.ieee_type = '802.11ax'
            phy.freq.append('6-GHz')
            continue

        if 'EHT ' in row:
            phy.wifi_type = 'wifi-7'
            phy.ieee_type = '802.11be'
            continue
    return phys
