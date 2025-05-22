# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Supoet class to get info from 'iw':
    Be much better if there was a library to call or if provided json output
    For now we will parse it's output

Runs iw dev <dev> 'command'
    commands:
      station dump
          - the default
      scan
          - with -s or --scan
            Needs root or CAP_NET_RAW + CAP_NET_ADMIN
    Uses wifi.info file with local router info

    Need
    sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/iwinfo
"""
# pylint: disable=too-many-instance-attributes,too-few-public-methods
from ._known_hosts import KnownHosts
from ._iw_host import IwHost


def _sort_key_freq(item: IwHost):
    """
    return freq attrib
    """
    band = item.freq
    if band:
        band = band.strip()[0]
    else:
        band = ''
    return band


def _sort_key_signal(item: IwHost):
    """ return freq attrib """
    return item.signal


class IwHosts:
    """
    All visible hosts identified on network associated with "device".

    e.g. Visible hosts on network /dev/wlan0.
    """
    def __init__(self, device: str):
        self.device: str = device

        # list of found IwHost
        # scan_items -> hosts
        self.scan_items: list[IwHost] = []

    def add_item(self, bssid: str) -> IwHost:
        """ Add new scan item """
        scan_item = IwHost(bssid)
        self.scan_items.append(scan_item)
        return scan_item

    def add_hosts(self, hosts: list[IwHost]):
        """
        Add list of hosts
        """
        if hosts:
            self.scan_items += hosts

    def sort_scan_items(self):
        """
        Sort scan items
          - freq band (i.e. digit) (high to low)
          - signal (low to high)
        Uses python 3 complex sorted. Sort on secondary column, then on primary
        """
        if not (self.scan_items and len(self.scan_items) > 1):
            return
        self.scan_items = sorted(self.scan_items, key=_sort_key_signal)
        self.scan_items.sort(key=_sort_key_freq, reverse=True)

    def report(self, ap_bssids: list[str], known_hosts: KnownHosts):
        """
        repore
        """
        self.sort_scan_items()
        hosts = self.scan_items

        for item in hosts:
            item.report(ap_bssids, known_hosts)
