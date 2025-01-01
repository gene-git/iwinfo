# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Command line options handling
"""
# pylint: disable=too-few-public-methods
import argparse

class IwOpts:
    """
    command line options
    """
    def __init__(self):
        desc = "iwinfo : provide information about wireless network(s)"
        self.okay = True
        self.scan = False
        opts = [
                [('-s', '--scan'),
                 {'help' : 'Scan wireless network(s)', 'action' : 'store_true'}],
               ]
        par = argparse.ArgumentParser(description=desc)
        for ((opt_s, opt_l), kwargs) in opts:
            par.add_argument(opt_s, opt_l, **kwargs)
        parsed = par.parse_args()
        if parsed:
            for (opt, val) in vars(parsed).items() :
                setattr(self, opt, val)

    def __getattr__(self, name):
        """ non-set items simply return None makes it easy to check existence"""
        return None
