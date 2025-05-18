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
        requires root or CAP_NET_RAW + CAP_NET_ADMIN
    Uses wifi.info file with local router info

    Need
    sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/iwinfo
"""
# pylint: disable=too-many-instance-attributes,too-few-public-methods
from typing import (Dict, List)
from .our_wifi import (get_phy_list, get_device_names)
from .phy_info import IwPhyInfo
from ._iw_hosts import IwHosts
from .scan_wifi import get_iw_scan
from .capabilities import have_net_caps
from ._known_hosts import KnownHosts
from ._options import Options
from ._device import Device


class IwInfo:
    """
    Gather wireless network info.

    Primarily we use 'iw' command and scrape the output.
    iw man page discourages this but until a better alternative
    is available we do use it that way.
    We also use iwctl when available for additional information.
    """
    def __init__(self):
        self.have_caps: bool = False
        self.do_scan: bool = False

        # local devices
        self.device_names: List[str] = []
        self.devices: Dict[str, Device] = {}
        self.ap_bssids: List[str] = []

        # phy info
        self.phys: Dict[str, IwPhyInfo]

        # scanned devices - do 1 scan per local device
        self.iw_hosts: Dict[str, IwHosts] = {}

        # Local wifi device info file (/etc/iwinfo/wifi.db)
        self.known_hosts = KnownHosts()

        # command line
        self.opts = Options()

        if self.opts.scan:
            self._scan_permissions_check()

    def _scan_permissions_check(self):
        """
        Scan wireless network(s)
           NB: Caps required
               Require: cap_net_raw, cap_net_admin
        """
        self.have_caps = have_net_caps()
        if self.have_caps:
            self.do_scan = True
        else:
            print('Skipping scan which requires elevated privileges')

    def get_our_wifi_info(self):
        """
        Get info about all local wifi devices
        """
        self.device_names = get_device_names()
        if self.device_names:

            for name in self.device_names:
                self.devices[name] = Device(name)
                self.devices[name].get_info()

                if self.do_scan:
                    self.iw_hosts[name] = IwHosts(name)

        # update ap bssid list
        self.get_ap_bssids()

        # update info for each phy
        self.phys = get_phy_list()

    def scan(self):
        """
        Scan network :
         - need privs to put devices into promiscuous mode
         - need cap_net_raw, cap_net_admin
        """
        if not self.have_caps:
            print('Scan requires elevated privileges')
            return
        for dev in self.device_names:
            get_iw_scan(dev, self.iw_hosts[dev])

    def get_ap_bssids(self):
        """ list of APs we are connected to """
        self.ap_bssids = []
        for (_dev, item) in self.devices.items():
            self.ap_bssids.append(item.ap_bssid)

    def get_network_info(self):
        """
        Do what has been requested
        """
        self.get_our_wifi_info()

    def report(self):
        """
        Print what we found
        """
        known_hosts = self.known_hosts
        print('\nInterfaces:')
        for (_dev, devices) in self.devices.items():
            devices.report(known_hosts)

        # phy report
        if self.phys:
            print('\nDevices:')
            for (name, phy_info) in self.phys.items():
                print(f'  {name}:')
                phy_info.report()

        if self.do_scan:
            print('\nScanning network ...')
            self.scan()
            for (dev, iw_hosts) in self.iw_hosts.items():
                print(f'  {dev}:')
                iw_hosts.report(self.ap_bssids, known_hosts)
