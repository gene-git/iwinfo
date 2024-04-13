# SPDX-License-Identifier: MIT
# Copyright (c) 2023 Gene C
"""
Deals with local wifi things
"""
from .run_prog import run_prog
from .utils import filelist
from .parse_iw_link import parse_iw_link
from .phy_info import parse_iw_list


def get_wifi_devs():
    """ list of local wifi devices """
    netdir = '/sys/class/net'
    files = filelist(netdir)
    devs = []
    for file in files:
        if file.startswith('wl'):
            devs.append(file)
    return devs

def get_our_wifi_info(dev, iwours):
    """
    Use iw station dump to get info about this device
    """
    # pylint: disable=duplicate-code
    pargs = ['/usr/bin/iw', 'dev', dev, 'link']
    [ret, out, err] = run_prog(pargs)
    if ret != 0:
        if err:
            print(err)
        return
    result = out.splitlines()
    parse_iw_link(result, iwours)

def get_phy_capabilities():
    """ try get all phy info """
    pargs = ['/usr/bin/iw', 'list']
    [ret, out, err] = run_prog(pargs)
    if ret != 0:
        if err:
            print(err)
        return None
    result = out.splitlines()
    phys = parse_iw_list(result)
    return phys
