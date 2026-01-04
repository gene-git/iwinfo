#!/usr/bin/python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Parse output if 'iw list'
"""
# pylint: disable=too-many-branches,too-many-statements,too-few-public-methods
# pylint: disable=too-many-instance-attributes
import re


class IwFreq:
    """
    One Freq row
    """
    regex: re.Pattern
    inited: bool = False

    def __init__(self):
        self.freq: str = ''
        self.units: str = ''
        self.channel: str = ''
        self.power: str = ''
        self.comment: str = ''

        if not IwFreq.inited:
            self.regex_init()

    def regex_init(self):
        """
        How we parse frequency line
        """
        num = r'[\d]*'
        fnum = rf'{num}\.{num}'
        power = rf'{fnum} dBm|disabled'

        f1 = rf'^\* (?P<freq>{fnum}) (?P<units>[a-zA-Z]*)'
        f2 = r' \[(?P<channel>[\d]*)\]'
        f3 = rf' \((?P<power>{power})\)'
        f4 = r'(?P<comment>.*)'
        reg = f1 + f2 + f3 + f4

        IwFreq.regex = re.compile(reg)
        IwFreq.inited = True

    def parse(self, row: str) -> bool:
        """
        Parse:
            * 5700.0 MHz [140] (26.0 dBm) (radar detection)
            * 5845.0 MHz [169] (disabled)
        """
        if not row:
            return False

        scan = IwFreq.regex.search(row)
        if not scan:
            return False

        group = scan.groupdict()
        keys = ('freq', 'units', 'channel', 'power', 'comment')
        for key in keys:
            value = group.get(key)
            if value:
                setattr(self, key, value)

        return True


class IwFreqRange:
    """
    Frequency info for 1 band
    """
    def __init__(self, band: str):
        self.band: str = band
        self.iw_freq: list[IwFreq] = []

    def add(self, row: str):
        """
        Add items ~ from Frequency lines like:
            5300.0 MHz [60] (20.0 dBm) (radar detection)
            * 5885.0 MHz [177] (disabled)
        """
        if not row:
            return

        iw_freq = IwFreq()
        if iw_freq.parse(row):
            self.iw_freq.append(iw_freq)

    def print(self):
        """
        Report the range
        - show disabled frequencies
        """
        if not self.iw_freq:
            return

        print(f'{self.band:>12s}')

        for iwf in self.iw_freq:
            comment = ''
            if iwf.comment:
                comment = f'{iwf.comment}'
                if 'no IR' in comment:
                    comment = comment.replace('IR', 'initiate radio')
            channel = f'[{iwf.channel:>3s}]'
            info = f'{iwf.freq} {iwf.units} {channel} ({iwf.power}){comment}'
            print(f'{"":15s}{info}')
        print('')


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
        self.freq_range: list[IwFreqRange] = []
        self.wifi_type: str = ''
        self.ieee_type: str = ''

    def report(self, verb: bool = False):
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

        print(f'{"":3s} {wifi_type} {ieee_type} {num_bands} : {freq_str}')

        # show the frequency ranges.
        if verb:
            for freq_range in self.freq_range:
                freq_range.print()


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

    freq_start = False
    freq_range: IwFreqRange
    phy: IwPhyInfo
    for row in iw_output:
        row = row.strip()
        srow = row.split()

        #
        # New phy
        #
        if row.startswith('Wiphy phy'):
            # new phy
            name = srow[1]
            phy = IwPhyInfo(name)
            phys[name] = phy
            continue

        #
        # Parse freq range
        #  Band -> Frequencies -> (list of all freq)
        #
        if row.startswith('Band '):
            freq_start = False
            band = row.replace(':', '')
            freq_range = IwFreqRange(band)
            phy.freq_range.append(freq_range)

        if row.startswith('Frequencies:'):
            freq_start = True

        if freq_start and row.startswith('* ') and ' MHz [' in row and row.endswith(')'):
            freq_range.add(row)

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

            best_wifi = _wifi_best(phy.wifi_type, wifi_type)
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

            best_wifi = _wifi_best(phy.wifi_type, wifi_type)
            if best_wifi == wifi_type:
                phy.wifi_type = wifi_type
                phy.ieee_type = ieee_type
            continue

        if 'HT Max' in row:
            # has 2 bands - no need to check
            wifi_type = 'wifi-4'
            ieee_type = '802.11n'

            best_wifi = _wifi_best(phy.wifi_type, wifi_type)
            if best_wifi == wifi_type:
                phy.wifi_type = wifi_type
                phy.ieee_type = ieee_type
            continue

        if 'VHT Capabilities' in row:
            wifi_type = 'wifi-5'
            ieee_type = '802.11ac'

            best_wifi = _wifi_best(phy.wifi_type, wifi_type)
            if best_wifi == wifi_type:
                phy.wifi_type = wifi_type
                phy.ieee_type = ieee_type
            continue

        if 'HE RX MCS and NSS set <= 80 MHz' in row:
            wifi_type = 'wifi-6'
            ieee_type = '802.11ax'

            best_wifi = _wifi_best(phy.wifi_type, wifi_type)
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

            best_wifi = _wifi_best(phy.wifi_type, wifi_type)
            if best_wifi == wifi_type:
                phy.wifi_type = wifi_type
                phy.ieee_type = ieee_type
            continue

        if any(item in row for item in ('EHT MAC', 'EHT PHY')):
            wifi_type = 'wifi-7'
            ieee_type = '802.11be'
            best_wifi = _wifi_best(phy.wifi_type, wifi_type)
            if best_wifi == wifi_type:
                phy.wifi_type = wifi_type
                phy.ieee_type = ieee_type
            continue

    return phys


def _wifi_best(wifi_1: str, wifi_2: str):
    """
    Return best of wifi_1 or wifi_2
    e.g. wifi-6E > wifi-6
    """
    if wifi_1 > wifi_2:
        return wifi_1
    return wifi_2
