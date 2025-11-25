#!/usr/bin/python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Parse output if 'iw list'
"""
# pylint: disable=too-many-branches,too-many-statements,too-few-public-methods


class IwPhyInfo:
    """
    Info about one phy
    """
    def __init__(self, phy_name: str):
        self.phy: str = phy_name
        self.interface: str = ''
        self.addr: str = ''
        self.num_bands: int = 0
        self.freq: list[str] = []
        self.wifi_type: str = ''
        self.ieee_type: str = ''

    def report(self):
        """ report what we found """
        wifi_type = self.wifi_type or 'wifi-?'
        ieee_type = self.ieee_type or '80211.?'
        ieee_type = f'({ieee_type})'
        freq_str = '-'
        if self.freq:
            freq = sorted(list(set(self.freq)))
            freq_str = ' '.join(freq)

        wifi_type = f'{wifi_type:>10s}'
        ieee_type = f'{ieee_type:<10s}'
        num_bands = f'{self.num_bands:>3d}-bands'

        print(f'{"":6s} {wifi_type} {ieee_type} {num_bands} : {freq_str}')


def parse_iw_list(iw_output: list[str]) -> dict[str, IwPhyInfo]:
    """
    Extract data from 'iw list' output

    Args:
        iw_output (list[str]):
        Stdout from 'iw' command

    Returns:
        dict[name: str, phy: IwPhyInfo]
        dictionary of phy devices indexed by phy name.
    """
    phys: dict[str, IwPhyInfo] = {}

    if not iw_output:
        return phys

    # phy = None
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
            wifi_type = 'wifi-1'

            wifi_type = 'wifi-1'
            ieee_type = '802.11b'

            if phy.num_bands >= 2:
                wifi_type = 'wifi-3'
                ieee_type = '802.11g'
            elif phy.num_bands >= 3:
                wifi_type = 'wifi-6E'
                ieee_type = '802.11ax'

            best_wifi = _best_wifi(phy.wifi_type, wifi_type)
            if best_wifi == wifi_type:
                phy.wifi_type = wifi_type
                phy.ieee_type = ieee_type
            continue

        if '* 5180.0 MHz [36]' in row:
            phy.freq.append('5-GHz')

            if phy.num_bands == 1:
                wifi_type = 'wifi-2'
                ieee_type = '802.11a'
            else:
                wifi_type = 'wifi-4'
                ieee_type = '802.11n'

            best_wifi = _best_wifi(phy.wifi_type, wifi_type)
            if best_wifi == wifi_type:
                phy.wifi_type = wifi_type
                phy.ieee_type = ieee_type
            continue

        if 'HT Max' in row:
            # has 2 bands - no need to check
            wifi_type = 'wifi-4'
            ieee_type = '802.11n'

            best_wifi = _best_wifi(phy.wifi_type, wifi_type)
            if best_wifi == wifi_type:
                phy.wifi_type = wifi_type
                phy.ieee_type = ieee_type
            continue

        if 'VHT Capabilities' in row:
            wifi_type = 'wifi-5'
            ieee_type = '802.11ac'

            best_wifi = _best_wifi(phy.wifi_type, wifi_type)
            if best_wifi == wifi_type:
                phy.wifi_type = wifi_type
                phy.ieee_type = ieee_type
            continue

        if 'HE RX MCS and NSS set <= 80 MHz' in row:
            wifi_type = 'wifi-6'
            ieee_type = '802.11ax'

            best_wifi = _best_wifi(phy.wifi_type, wifi_type)
            if best_wifi == wifi_type:
                phy.wifi_type = wifi_type
                phy.ieee_type = ieee_type
            continue

        if '* 2412.0 MHz [1]' in row:
            phy.freq.append('2.4-GHz')
            continue

        if '* 5955.0 MHz [1]' in row:
            wifi_type = 'wifi-6E'
            ieee_type = '802.11ax'
            phy.freq.append('6-GHz')

            best_wifi = _best_wifi(phy.wifi_type, wifi_type)
            if best_wifi == wifi_type:
                phy.wifi_type = wifi_type
                phy.ieee_type = ieee_type
            continue

        if any(item in row for item in ('EHT MAC', 'EHT PHY')):
            wifi_type = 'wifi-7'
            ieee_type = '802.11be'
            best_wifi = _best_wifi(phy.wifi_type, wifi_type)
            if best_wifi == wifi_type:
                phy.wifi_type = wifi_type
                phy.ieee_type = ieee_type
            continue

    return phys


def _best_wifi(wifi_1: str, wifi_2: str):
    """
    Return best of wifi_1 or wifi_2
    e.g. wifi-6E > wifi-6
    """
    if wifi_1 > wifi_2:
        return wifi_1
    return wifi_2
