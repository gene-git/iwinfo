# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Deals with local wifi things
"""
from .run_prog import run_prog
from .utils import filelist
from .parse_iw import (parse_iw, parse_iwctl_show)
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
    Use iw to get info about this device
    """
    # iw dev <dev> link
    _get_iw(dev, 'link', iwours)

    # iw dev <dev> info
    _get_iw(dev, 'info', iwours)

    # iw dev <dev> info
    _get_iw_dump(dev, iwours)

    # if running iwd then can get
    _get_iwctl(dev, 'show', iwours)

def _get_iw(dev:str, cmd:str, iwours:'IwOurs'):
    """
    Use iw dev <dev> <cmd>
    cmd is one of ('link', 'info')
    """
    pargs = ['/usr/bin/iw', 'dev', dev, cmd]
    result = _runit(pargs)
    if result:
        parse_iw(result, cmd, iwours)

def _get_iw_dump(dev:str, iwours:'IwOurs'):
    """
    Use iw dev <dev> station dump
    cmd is one of ('link', 'info')
    """
    pargs = ['/usr/bin/iw', 'dev', dev, 'station', 'dump']
    result = _runit(pargs)
    if result:
        parse_iw(result, 'dump', iwours)

def _get_iwctl(dev:str, cmd:str, iwours:'IwOurs'):
    """
    Use iwctl station <dev> <cmd>
    cmd is one of ('show')
    """
    if cmd != 'show':
        return

    pargs = ['/usr/bin/iwctl', 'station', dev, cmd]
    result = _runit(pargs)
    if result:
        parse_iwctl_show(result, iwours)

def get_phy_capabilities():
    """ try get all phy info """
    pargs = ['/usr/bin/iw', 'list']
    result = _runit(pargs)
    if result:
        phys = parse_iw_list(result)
        return phys
    return None

def _get_iw_dump(dev:str, iwours:'IwOurs'):
    """
    Use iw dev <dev> station dump
    cmd is one of ('link', 'info')
    """
    pargs = ['/usr/bin/iw', 'dev', dev, 'station', 'dump']
    result = _runit(pargs)
    if result:
        parse_iw(result, 'dump', iwours)

def _runit(pargs:[str]) -> [str]:
    """
    Runs pargs and returns output lines or None if failed
    """
    result = None
    [ret, out, err] = run_prog(pargs)
    if ret != 0:
        if err:
            print(err)
        return None
    if out:
        result = out.splitlines()
    return result
