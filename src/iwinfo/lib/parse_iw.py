# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Parse output if 'iw link' and 'iw info'
"""
from .parse_tools import found_access_point
from .utils import (any_in, strip_ansi)
from ._device_base import DeviceBase


def _parse_iw_row(keys: list[str], row_items: list[str], device: DeviceBase):
    """
    Extract what we need from iw output for each field in 'keys'
    Update the each device class attribute of same name (key)
    """
    for key in keys:
        if key in row_items[0]:
            if len(row_items) > 1:
                value = row_items[1]
                value = value.strip()
                attrib = key.lower().replace(' ', '_')
                setattr(device, attrib, value)


def _parse_iw_link(iw_output: list[str], device: DeviceBase):
    """
    Extract what we need from iw output
    Update the corresponding device class attributes
    """
    keys = ['SSID', 'freq', 'signal', 'rx bitrate', 'tx bitrate']

    for row in iw_output:
        row = row.strip()

        bssid = found_access_point(row)
        if bssid:
            # AP line
            device.ap_bssid = bssid
            continue

        row_items = row.split(':', 1)
        if any_in(keys, row_items):
            _parse_iw_row(keys, row_items, device)


def _parse_iw_info(iw_output: list[str], device: DeviceBase) -> None:
    """
    Extract what we need from iw output
    Update the corresponding device class attributes
    """
    keys = ['addr', 'channel']

    for row in iw_output:
        row = row.strip()

        row_items = row.split()
        if any_in(keys, row_items):
            _parse_iw_row(keys, row_items, device)


def _parse_iw_dump(iw_output: list[str], device: DeviceBase):
    """
    Extract what we need from iw station dump
    Update the corresponding device class attributes
    """
    keys = ['authorized', 'authenticated', 'associated']

    for row in iw_output:
        row = row.strip()

        row_items = row.split(':', 1)
        if any_in(keys, row_items):
            _parse_iw_row(keys, row_items, device)


def parse_iw(iw_output: list[str], cmd: str, device: DeviceBase):
    """
    Parse output of:
       iw dev <device> <cmd>
       cmd is one of ('link', 'info')
    """
    if cmd == 'link':
        _parse_iw_link(iw_output, device)

    elif cmd == 'info':
        _parse_iw_info(iw_output, device)

    elif cmd == 'dump':
        _parse_iw_dump(iw_output, device)


def parse_iwctl_show(iw_output: list[str], device: DeviceBase):
    """
    Extract what we need from 'iwctl station <dev> show' output
    Update the corresponding device class attributes
    """
    keys = ['IPv4_address', 'IPv6_address', 'Security', 'TxMode', 'RxMode']

    for row in iw_output:
        row = row.strip()
        row = strip_ansi(row)
        row = row.replace(' address', '_address')

        row_items = row.split()
        if 'Failed' in row_items or 'No matching' in row_items:
            continue

        if any_in(keys, row_items):
            _parse_iw_row(keys, row_items, device)
