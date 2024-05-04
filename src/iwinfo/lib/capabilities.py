# SPDX-License-Identifier: MIT
# Copyright (c) 2023 Gene C
"""
Check for cap_net_raw, cap_net_admin
"""
import os
from ctypes import CDLL
from ctypes.util import find_library
#import prctl
from .utils import open_file

def _get_net_capabilities():
    """
    Gets the integer values of the capabilities we need
    from capabilities.h header file
    """
    need = ['CAP_NET_ADMIN', 'CAP_NET_RAW']
    num_caps = len(need)

    # in case we cannot find the defines
    def_caps = {'CAP_NET_ADMIN': 12, 'CAP_NET_RAW': 13}

    cap_file = '/usr/include/sys/capability.h'
    done = False
    caps = {}
    fob = open_file(cap_file, 'r')
    if fob:
        data = fob.read()
        fob.close()
        rows = data.splitlines()
        for row in rows:
            for cap in need:
                if cap in row:
                    caps[cap] = row.split(cap)[-1].strip()
                    if len(caps) == num_caps:
                        done = True
                        break
            if done:
                break
    if not done:
        caps = def_caps
    return caps

#def _have_net_caps_prctl():
#    """
#     - use python-prctl module.
#    """
#    # pylint: disable=no-member
#    has_caps = prctl.cap_inheritable.net_raw and prctl.cap_inheritable.net_admin
#    return has_caps

def _have_net_caps_libcap():
    """
     - use libcap shared library directly.
    """
    have_caps = False
    libcap = CDLL(find_library('cap'))

    # get the list of cap names and integer constants
    caps = _get_net_capabilities()

    # check we have them all
    num_caps = len(caps)
    num_have = 0
    for (_cap, cap_val) in caps.items():
        check = libcap.cap_get_ambient(cap_val)
        if check > 0:
            num_have += 1

    if num_have == num_caps:
        have_caps = True

    return have_caps


def have_net_caps():
    """
    check for net caps we need for iw
    Couple ways to do this.
     - use python-prctl module.
     - call libcap directly
       We call libcap to reduce reliance on python packages
    """
    # root ok
    is_root = bool(os.geteuid() == 0)
    if is_root:
        return is_root

    #
    # Pick one approach
    # have_caps = _have_net_caps_prctl()
    #
    have_caps = _have_net_caps_libcap()

    return have_caps
