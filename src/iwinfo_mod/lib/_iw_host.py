# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Supoet class to get info from 'iw':
    Be much better if there was a library to call or if provided json output
    For now we will parse it's output

Runs iw dev <dev> 'command'
    command : station dump
                - the default
              scan - with -s or --scan
                Needs root or CAP_NET_RAW + CAP_NET_ADMIN

    Need
    sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/iwinfo
"""
# pylint: disable=too-few-public-methods
from ._known_hosts import KnownHosts


class IwHost:
    """
    One host seen on wireless network.

    Information discovered by iw scan.
    """
    def __init__(self, bssid):
        self.bssid: str = bssid
        self.ssid: str = ''
        self.freq: str = ''
        self.signal: str = ''

    def report(self, ap_bssids: list[str], known_hosts: KnownHosts):
        """
        Print one line report of this host.
        """
        mark = '*' if self.bssid in ap_bssids else ' '

        # any info known about this bssid
        known_host_info = known_hosts.host_info(self.bssid)

        bssid = self.bssid or '-'
        ssid = self.ssid or '-'
        freq = self.freq or '-'
        signal = self.signal or '-'

        base_info = f'{bssid}: {ssid:20s} {freq:8s} {signal}'
        print(f' {mark} {base_info} : {known_host_info}')
