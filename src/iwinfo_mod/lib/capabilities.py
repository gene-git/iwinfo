# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Check for cap_net_raw, cap_net_admin
"""
import os
import capng


def _check_have_net_caps() -> bool:
    """
    To scan capabilities requried:
        cap_net_raw, cap_net_admin
    libcap_ng version >= 0.6 provides python bindings to libcap_nd
    In addition, versions >= 0.8.3 provide drop ambient
    """
    #
    # Check have ambient caps
    #  - ambient is required to run programs for network scan (e.g. iw)
    #
    if not (capng.capng_have_capabilities(capng.CAPNG_SELECT_AMBIENT)
            > capng.CAPNG_NONE):
        return False

    #
    # Check have the network ones we need
    #
    need = [capng.CAP_NET_ADMIN, capng.CAP_NET_RAW]
    num_need = len(need)
    num_have = 0
    which = capng.CAPNG_AMBIENT
    for cap in need:
        if capng.capng_have_capability(which, cap):
            num_have += 1

    if num_have == num_need:
        return True
    return False


def have_net_caps() -> bool:
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
    # Capabilities needed
    #
    have_caps = _check_have_net_caps()

    return have_caps
