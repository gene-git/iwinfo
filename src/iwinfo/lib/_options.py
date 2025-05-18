# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
"""
Command line option handling
"""
# pylint: disable=too-few-public-methods
from typing import (Any, Dict, List, Tuple)
import argparse

type Opt = Tuple[str | Tuple[str, str], Dict[str, Any]]


class Options:
    """
    command line options

    Available options:
        Request wireless network scan (requires privs)
    """
    def __init__(self):
        desc: str = "iwinfo : provide information about wireless network(s)"
        self.okay: bool = True
        self.scan: bool = False

        opts: List[Opt] = []

        #
        # Establish the list of optiont
        #
        opt = (('-s', '--scan'),
               {'help': 'Scan wireless network(s)',
                'action': 'store_true',
                }
               )
        opts.append(opt)

        #
        # Parse them
        #
        par = argparse.ArgumentParser(description=desc)

        for (opt_list, kwargs) in opts:
            if isinstance(opt_list, str):
                par.add_argument(opt_list, **kwargs)
            else:
                par.add_argument(*opt_list, **kwargs)

        #
        # store result as attribute
        #
        parsed = par.parse_args()
        if parsed:
            for (key, val) in vars(parsed).items():
                setattr(self, key, val)
