#!/usr/bin/python
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Report wireless network info
"""
# pylint: disable=invalid-name
from lib import IwInfo


def main():
    """
    Invoked from /usr/bin/iwinfo
      - this has the right cap_net capabilities to permit network scans
    """
    iwinfo = IwInfo()
    iwinfo.get_network_info()
    iwinfo.report()


if __name__ == '__main__':
    main()
