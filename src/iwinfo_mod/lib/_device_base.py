# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Supoet class to get info from 'iw':
    Be much better if there was a library to call or if provided json output
    For now we will parse it's output

Runs iw dev <dev> 'command'
    command: station dump
                - the default
              scan - with -s or --scan.
                Needs: root or CAP_NET_RAW + CAP_NET_ADMIN
    Need
    sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/iwinfo
"""
# pylint: disable=too-many-instance-attributes,too-few-public-methods


class DeviceBase:
    """
    Info about 1 local device.

    Local means a device on the local machine.
    """
    def __init__(self, name: str):

        self.name: str = name
        self.ssid: str = ''
        self.freq: str = ''
        self.signal: str = ''
        self.rx_bitrate: str = ''
        self.tx_bitrate: str = ''
        self.ap_bssid: str = ''
        self.addr: str = ''       # device mac
        self.channel: str = ''

        self.authorized: bool = False
        self.authenticated: bool = False
        self.associated: bool = False

        # needs iwd running
        self.ipv4_address: str = ''
        self.ipv6_address: str = ''
        self.security: str = ''
        self.txmode: str = ''
        self.rxmode: str = ''
