# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Local wifi informational database (optional)
"""
# pylint: disable=invalid-name,too-few-public-methods
import os
import tomllib as toml
from tomllib import TOMLDecodeError
from .utils import open_file


class KnownHost:
    """
    1 host from known_hosts file
    """
    def __init__(self, name):
        self.name: str = name
        self.ip: str = ''
        self.mac_map: dict[str, str] = {}
        self.make: str = ''
        self.model: str = ''
        self.info: str = ''


def _get_known_host_file() -> str:
    """
    Locate known hosts database file.

    Search order:
        Directories: ./etc/iwinfo, /etc/iwinfo
        Files: known-hosts.db, wifi.db, wifi.info
    """
    dirs = ['./etc/iwinfo', '/etc/iwinfo']
    files = ['known-hosts.toml', 'wifi.db', 'wifi.info']

    known_host_file = ''
    for tdir in dirs:
        for file in files:
            fpath = os.path.join(tdir, file)
            if os.path.exists(fpath):
                known_host_file = fpath
                break
        if known_host_file:
            break
    return known_host_file


def _read_known_hosts(known_hosts) -> dict[str, KnownHost]:
    """
    Read the known hosts file and map it into attributes
    """
    hosts: dict[str, KnownHost] = {}

    fob = open_file(known_hosts.dbfile, 'r')
    if not fob:
        return hosts

    #
    # db uses mac_map = [ [name1, mac], [name2, mac2], ...]
    # name can be '5 Ghz', or '2.4 Ghz' or 'lan' or anything else
    #
    data = fob.read()
    fob.close()
    try:
        tdata = toml.loads(data)
    except TOMLDecodeError as err:
        text = f'loading known hosts file {known_hosts.dbfile} '
        print(f'Error: {text}: {err}')
        return hosts

    device: KnownHost
    for (key, val) in tdata.items():
        if isinstance(val, dict):
            device = KnownHost(key)
            hosts[key] = device

            for (skey, sval) in val.items():

                if skey == 'mac_map':
                    for [name, mac] in sval:
                        device.mac_map[name] = mac
                else:
                    setattr(device, skey, sval)
        else:
            # Any top level global variables (not expected)
            setattr(known_hosts, key, val)

    return hosts


def _build_bssid_index(hosts: dict[str, KnownHost]) -> dict[str, KnownHost]:
    """
    build mac based index map
    """
    bssid_index: dict[str, KnownHost] = {}
    if not hosts:
        return bssid_index

    for (_name, host) in hosts.items():
        for (_mac_name, bssid) in host.mac_map.items():
            bssid = bssid.lower()
            bssid_index[bssid] = host

    return bssid_index


class KnownHosts:
    """
    Optional known wifi hosts database file.

    Allows additional Access Point info such as location
    IP address, make, model etc for each known host.
    """
    def __init__(self):
        self.dbfile: str = _get_known_host_file()
        self.hosts: dict[str, KnownHost] = {}
        self.hosts_by_bssid: dict[str, KnownHost] = {}

        if not self.dbfile:
            return

        self.hosts = _read_known_hosts(self)
        self.hosts_by_bssid = _build_bssid_index(self.hosts)

    def _get_host_info(self, bssid: str) -> tuple[str, str, str]:
        """
        Find device from mac
        """
        make = ''
        model = ''
        info = ''

        if not bssid or not self.hosts_by_bssid:
            return (make, model, info)

        bssid = bssid.lower()
        device = self.hosts_by_bssid.get(bssid)
        if device:
            make = device.make
            model = device.model
            info = device.info
        return (make, model, info)

    def host_info(self, bssid: str) -> str:
        """
        Return any known info about bssid.

        Args:
            bssid (str):
            bssid to lookup.

        Returns:
            str:
            Known info or empty string if nothing known.
        """
        info = ''
        (make, model, other_info) = self._get_host_info(bssid)
        if make:
            info += f'{make:>10s} '

        if model:
            info += f'{model:^10s} '

        if other_info:
            info += other_info

        return info
