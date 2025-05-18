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
# pylint: disable=too-many-instance-attributes,too-few-public-methods
from .our_wifi import get_our_wifi_info
from ._device_base import DeviceBase
from ._known_hosts import KnownHosts


class Device(DeviceBase):
    """
    Info about 1 local device

    Actions/methods.
    """
    def get_info(self):
        """
        Find out what we can about this device
        """
        get_our_wifi_info(self)

    def report(self, known_hosts: KnownHosts):
        """
        print report
        """

        host_bssid = self.ap_bssid
        known_host_info = ''
        if known_hosts:
            known_host_info = known_hosts.host_info(host_bssid)

        print(f'  {self.name} :')
        print(f'{"ap_bssid":>15s} : {host_bssid} : {known_host_info}')
        print(f'{"ssid":>15s} : {self.ssid}')
        print(f'{"freq":>15s} : {self.freq}')

        if self.channel:
            print(f'{"channel":>15s} : {self.channel}')

        print(f'{"signal":>15s} : {self.signal}')
        print(f'{"rx_bitrate":>15s} : {self.rx_bitrate}')
        print(f'{"tx_bitrate":>15s} : {self.tx_bitrate}')

        if self.authorized:
            print(f'{"authorized":>15s} : {self.authorized}')

        if self.authenticated:
            print(f'{"authenticated":>15s} : {self.authenticated}')

        if self.associated:
            print(f'{"associated":>15s} : {self.associated}')

        if self.security:
            print(f'{"security":>15s} : {self.security}')

        if self.txmode:
            print(f'{"txmode":>15s} : {self.txmode}')

        if self.rxmode:
            print(f'{"rxmode":>15s} : {self.rxmode}')

        if self.addr:
            print(f'{"mac_addr":>15s} : {self.addr}')

        if self.ipv4_address:
            print(f'{"ipv4_address":>15s} : {self.ipv4_address}')

        if self.ipv6_address:
            print(f'{"ipv6_address":>15s} : {self.ipv6_address}')
