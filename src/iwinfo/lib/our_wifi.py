# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Deals with local wifi things
"""
from typing import (Dict, List)
from .run_prog import run_cmd
from .utils import filelist
from .parse_iw import (parse_iw, parse_iwctl_show)
from .phy_info import (IwPhyInfo, parse_iw_list)
from ._device_base import DeviceBase


def get_device_names() -> List[str]:
    """
    list of local wifi devices
    """
    netdir = '/sys/class/net'

    device_names: List[str] = []

    files = filelist(netdir)
    for file in files:
        if file.startswith('wl'):
            device_names.append(file)
    return device_names


def get_our_wifi_info(device: DeviceBase):
    """
    Use iw to get info about this device
    """
    # iw dev <dev> link
    _run_iw(device, 'link')

    # iw dev <dev> info
    _run_iw(device, 'info')

    # iw dev <dev> info
    _run_iw_dump(device)

    # if running iwd then can get
    _run_iwctl(device, 'show')


def _run_iw(device: DeviceBase, cmd: str):
    """
    Use iw dev <dev> <cmd>
    cmd is one of ('link', 'info')
    """
    pargs = ['/usr/bin/iw', 'dev', device.name, cmd]
    result = run_cmd(pargs)
    if result:
        parse_iw(result, cmd, device)


def _run_iw_dump(device: DeviceBase):
    """
    Use iw dev <dev> station dump
    cmd is one of ('link', 'info')
    """
    pargs = ['/usr/bin/iw', 'dev', device.name, 'station', 'dump']
    result = run_cmd(pargs)
    if result:
        parse_iw(result, 'dump', device)


def _run_iwctl(device: DeviceBase, cmd: str):
    """
    Use iwctl station <dev> <cmd>
    cmd is one of ('show')
    """
    if cmd != 'show':
        return

    pargs = ['/usr/bin/iwctl', 'station', device.name, cmd]
    result = run_cmd(pargs)
    if result:
        parse_iwctl_show(result, device)


def get_phy_list() -> Dict[str, IwPhyInfo]:
    """
    Try get all phy info

    Run "iw list".

    Returns:
        Dict[str, IwPhyInfo]:
        Dictionary phy info indexed by phy name.
    """
    pargs = ['/usr/bin/iw', 'list']
    result = run_cmd(pargs)
    phys = parse_iw_list(result)
    return phys
