# SPDX-License-Identifier: MIT
# Copyright (c) 2023 Gene C
"""
Local wifi informational database (optional)
"""
# pylint: disable=invalid-name,too-few-public-methods

import os
import tomllib as toml
from tomllib import TOMLDecodeError
from .utils import open_file


def _get_db_file():
    """ locate wifi info file """
    dirs = ['/etc/iwinfo', '/opt/adm-tools']
    files = ['wifi.db', 'wifi.info']

    dbfile = None
    for tdir in dirs:
        for file in files:
            fpath = os.path.join(tdir, file)
            if os.path.exists(fpath):
                dbfile = fpath
                break
        if dbfile:
            break
    return dbfile

def _read_wifi_db(wifi_db):
    """
    Read the config file and map it into attributes
    """
    devices = {}

    fob = open_file(wifi_db.dbfile, 'r')
    if not fob:
        return devices

    #
    # new db uses mac_map = [ [name1, mac], [name2, mac2], ...]
    # name can be '5 Ghz', or '2.4 Ghz' or 'lan' or ...
    # old uses i5GHz,i24Ghz, lan = mac
    #
    old_keys = ['i5GHz', 'i24Ghz', 'lan']

    data = fob.read()
    fob.close()
    try:
        tdata = toml.loads(data)
    except TOMLDecodeError as err:
        print(f'Error loading config {wifi_db.dbfile} : {err}')
        return devices

    device = None
    for (key, val) in tdata.items():
        if isinstance(val, dict):
            device = WifiDevice(key)
            devices[key] = device

            for (skey, sval) in val.items():

                if skey == 'mac_map':
                    for [name, mac] in sval:
                        device.mac_map[name] = mac

                elif skey in old_keys:
                    # old style - drop leading "i"
                    freq = skey.replace('i', '', 1)
                    device.mac_map[freq] = sval

                else:
                    setattr(device, skey, sval)
        else :
            # top level global variables (not expected)
            setattr(wifi_db, key, val)
    return devices

def _build_bssid_index(devices):
    """ build mac based index map """
    bssid_index = {}
    if not devices:
        return bssid_index

    for (_dev_name, device) in devices.items():
        for (_mac_name, bssid) in device.mac_map.items():
            bssid = bssid.lower()
            bssid_index[bssid] = device

    return bssid_index

class WifiDevice:
    """ 1 item from wifi_db file """
    def __init__(self, name):
        self.name = name
        self.ip = None
        self.mac_map = {}
        self.model = None
        self.info = None

class WifiDb:
    """ optional wifi info db """
    def __init__(self):
        self.dbfile = _get_db_file()
        self.devices = {}
        self.devices_by_bssid = {}

        if not self.dbfile:
            return

        self.devices = _read_wifi_db(self)
        self.devices_by_bssid = _build_bssid_index(self.devices)

    def get_dev_info(self, bssid):
        """
        Find device from mac
        """
        model = ''
        info = ''
        if not bssid or not self.devices_by_bssid:
            return (model, info)

        bssid = bssid.lower()
        device = self.devices_by_bssid.get(bssid)
        if device:
            model = device.model
            info = device.info
        return (model, info)
