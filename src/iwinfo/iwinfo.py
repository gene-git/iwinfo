#!/usr/bin/python
"""
Report wireless network info
"""
# pylint: disable=invalid-name
# import pdb
from lib import IwInfo

def main():
    """
    Invoked from /usr/bin/iwinfo
      - this has the right cap_net capabilities to permit network scans
    """
    #pdb.set_trace()

    iwinfo = IwInfo()
    iwinfo.get_network_info()
    iwinfo.report()

if __name__ == '__main__':
    main()
