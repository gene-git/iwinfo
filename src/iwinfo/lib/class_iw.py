# SPDX-License-Identifier: MIT
# Copyright (c) 2023 Gene C
"""
Supoet class to get info from 'iw':
    Be much better if there was a library to call or if provided json output
    For now we will parse it's output

Runs iw dev <dev> 'command'
    command : station dump - the default
              scan         - with -s or --scan (requires root or CAP_NET_RAW + CAP_NET_ADMIN)
    Uses wifi.info file with local router info

    Need
    sudo setcap cap_net_raw,cap_net_admin+eip /usr/bin/iwinfo
"""
# pylint: disable=too-many-instance-attributes,too-few-public-methods
from .our_wifi import get_wifi_devs
from .our_wifi import get_our_wifi_info
from .our_wifi import get_phy_capabilities
from .scan_wifi import get_iw_scan
from .capabilities import have_net_caps
from .class_db import WifiDb
from .class_opts import IwOpts

def _rpt_db_more_info(bssid, wifi_db):
    """
    Lookup any additional info on this bssid
    """
    more_info = ''
    if wifi_db:
        (model, info) = wifi_db.get_dev_info(bssid)
        if model:
            more_info = f'{model} '
        if info:
            more_info += info
    return more_info

class IwOurs:
    """ Info about 1 local device """
    def __init__(self, device):
        self.device = device
        #self.mac = None       # device mac
        self.ssid = None
        self.freq = None
        self.signal = None
        self.rx_bitrate= None
        self.tx_bitrate = None
        self.ap_bssid = None

    def get_info(self):
        """
        Find out what we can about this device
        """
        get_our_wifi_info(self.device, self)

    def report(self, wifi_db):
        """ print """
        more_info = _rpt_db_more_info(self.ap_bssid, wifi_db)
        print(f'  {self.device}:')
        print(f'    ap_bssid : {self.ap_bssid} : {more_info}')
        #print(f'         mac : {self.mac}')
        print(f'        ssid : {self.ssid}')
        print(f'        freq : {self.freq}')
        print(f'      signal : {self.signal}')
        print(f'  rx_bitrate : {self.rx_bitrate}')
        print(f'  tx_bitrate : {self.tx_bitrate}')

class IwScanItem:
    """ Info about 1 item from iw scan"""
    def __init__(self, bssid):
        self.bssid = bssid
        self.ssid = None
        self.freq = None
        self.signal = ''

    def report(self, ap_bssids, wifi_db):
        """ print """
        mark = ' '
        if self.bssid in ap_bssids:
            mark = '*'

        # any other info
        more_info = _rpt_db_more_info(self.bssid, wifi_db)

        bssid = self.bssid or '-'
        ssid = self.ssid or '-'
        freq = self.freq or '-'
        signal = self.signal or '-'

        print(f' {mark} {bssid}: {ssid:20s} {freq:8s} {signal} : {more_info}')

class IwScanDevice:
    """ Info about 1 item from iw scan"""
    def __init__(self, device):
        self.device = device

        # list of found IwScanItems
        self.scan_items = []

    def add_item(self, bssid:str) -> IwScanItem:
        """ Add new scan item """
        scan_item = IwScanItem(bssid)
        self.scan_items.append(scan_item)
        return scan_item

    def report(self, ap_bssids, wifi_db):
        """ report """
        # sort by signal

        #scan_items = sorted(self.scan_items, key=lambda x: (x.freq, x.signal))
        scan_items = self.scan_items
        if scan_items and len(scan_items) > 1:
            scan_items = sorted(self.scan_items, key=lambda x: (x.signal))
        if not scan_items:
            scan_items = []
        for item in scan_items:
            item.report(ap_bssids, wifi_db)

class IwInfo:
    """ my job is to get info from 'iw' """
    def __init__(self):
        self.have_caps = False
        self.do_scan = False
        # local devices
        self.devs = []
        self.ours = {}
        self.ap_bssids = []

        # phy info
        self.phys = None

        # scanned devices - do 1 scan per local device
        self.scan_device = {}

        # Local wifi device info file (/etc/iwinfo/wifi.db)
        self.wifi_db = WifiDb()

        # command line
        self.opts = IwOpts()

        if self.opts.scan:
            #
            # Scan wireless network(s)
            #    Caps required so we check for : cap_net_raw,cap_net_admin
            #
            self.have_caps = have_net_caps()
            if self.have_caps:
                self.do_scan = True
            else:
                print('Skipping scan which requires elevated privileges')

    def get_our_wifi_info(self):
        """
        Get info about all local wifi devices
        """
        devs = get_wifi_devs()
        if devs:
            self.devs = devs
            for dev in self.devs:
                self.ours[dev] = IwOurs(dev)
                self.ours[dev].get_info()
                if self.do_scan:
                    self.scan_device[dev] = IwScanDevice(dev)

        # update ap bssid list
        self.get_ap_bssids()

        # update info for each phy
        self.phys = get_phy_capabilities()

    def scan(self):
        """
        Scan network :
         - need privs to put devices into promiscuous mode
         - need cap_net_raw, cap_net_admin
        """
        if not self.have_caps:
            print('Scan requires elevated privileges')
            return
        for dev in self.devs:
            get_iw_scan(dev, self.scan_device[dev])

    def get_ap_bssids(self):
        """ list of APs we are connected to """
        self.ap_bssids = []
        for (_dev, item) in self.ours.items():
            self.ap_bssids.append(item.ap_bssid)

    def get_network_info(self):
        """
        Do what has been requested
        """
        self.get_our_wifi_info()
        if self.do_scan:
            self.scan()

    def report(self):
        """
        Print what we found
        """
        wifi_db = self.wifi_db
        print('\nInterfaces:')
        for (_dev, ours) in self.ours.items():
            ours.report(wifi_db)

        # phy report
        if self.phys:
            print('\nDevices:')
            for (name, phy_info) in self.phys.items():
                print(f'  {name}:')
                phy_info.report()

        if self.do_scan:
            print('\nScan Results:')
            for (dev, scan_device) in self.scan_device.items():
                print(f'  {dev}:')
                scan_device.report(self.ap_bssids, wifi_db)
