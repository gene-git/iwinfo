.. SPDX-License-Identifier: MIT

######
iwinfo
######

Overview
========

iwinfo : Provide useful information about wireless network(s)

This is a command line program which is run in any terminal.
It shows some information about existing wireless connections
along with the result of an optional scan for wireless devices.
Scan is turned on using *-s* option.

Scanning wireless networks requires elevated privileges, which means either by running as
root or by being provided with the required cap_net_xxx capablilities. 

This package provides the application, written in python, along with a small
C-program which is installed with cap_net_raw and cap_net_admin [#]_ 
and it provides the capabilities for the program to be run non-root.
Since this does add some risk, scanning is limited to root and members
of the *wheel* group only.

Others will still be able to get local wireless device and connection info, but will
not be able to scan the network(s).

.. [#] See man capabilities.

Key features
============

 * Shows local wireless device(s) and connection info.
 * Show summary of wireless hardware capabilities
 * Scans wireless network(s) and provides compact report

New / Interesting
==================

 * First public release

###############
Getting Started
###############

Usage
=====

Run in a terminal :

 .. code-block:: bash

    iwinfo --help
    iwinfo
    iwinfo --scan

Configuration
=============

An optional configuration file for iwinfo goes in:

 .. code-block:: bash

   /etc/iwinfo/wifi.db

*wifi.db* allows you to provide additional information about known wireless devices on the netwwork.
File is in *toml* format and a sample is installed in */etc/iwinfo/wifi.db.sample*. If available, 
then this information is used in generating the reports.

Each device listed in the file should have an entry of the form::

    [ap0]
        ip = '10.0.0.10'
        mac_map = [['5GHz', 'x:x:x:x:x:x'],
               ['24Ghz', 'x:x:x:x:x:x'],
                ['lan', 'x:x:x:x:x:x'],
                ]
        model = 'Netgear R9000'
        info = 'Location Office 1'

The mac_map is a list of pairs of [key, mac-address]. The key can be any convenient string you choose.

.. iwinfo-opts:

Options
-------

By default no network scan is performed. To turn this on use:

 * (*-s, --scan*)


Sample Output
-------------

Sample output::

  Interfaces:
    wlan0:
        ap_bssid : xx:xx:xx:xx:xx:xx : Netgear xr500 Location Office 1
            ssid :  MagicalPlaces
            freq :  5745.0
        signal :  -53 dBm
    rx_bitrate :  866.7 MBit/s VHT-MCS 9 80MHz short GI VHT-NSS 2
    tx_bitrate :  866.7 MBit/s VHT-MCS 9 80MHz short GI VHT-NSS 2
    
    Devices:
        phy0:
                wifi-6E (802.11ax)   3-bands : 2.4-GHz 5-GHz 6-GHz

With --scan::

  Scan Results:
    wlan0:
    xx:xx:xx:xx:xx:xx:  MagicalPlaces-24     2432.0   -32.00 dBm : Netgear 9000  Office 1
  * xx:xx:xx:xx:xx:xx:  MagicalPlaces        5745.0   -49.00 dBm : Netgear 9000  Office 1
    yy:yy:yy:yy:yy:yy:  MyNeighbor-6G        5955.0   -55.00 dBm : Asus GT11000  Test Lab
    ...

The asterisk indicates machine is currently connected to that AP


########
Appendix
########

Note on CET Shadow Stack
========================

The code is compiled with this turned on. If for some reason you get an error compiling then
you may turn it off by changing the load flag to 'cet-report=warning' in *src/ambient/Makefile*.

This may happen if you have old glibc (pre 2.39).


Installation
============

Available on
 * `Github`_
 * `Archlinux AUR`_

On Arch you can build using the provided PKGBUILD in the packaging directory or from the AUR.
To build manually, clone the repo and :

 .. code-block:: bash

        rm -f dist/*
        /usr/bin/python -m build --wheel --no-isolation
        root_dest="/"
        ./scripts/do-install $root_dest

When running as non-root then set root_dest a user writable directory

Dependencies
============

* Run Time :

  * python          (>= 3.11)

* Building Package:

  * git
  * hatch
  * wheel
  * build
  * installer
  * rsync
  * gcc
  * make
  * libcap-ng

* Optional to buil docs:

  * sphinx
  * texlive-latexextra  (archlinux packaguing of texlive tools)

Philosophy
==========

We follow the *live at head commit* philosophy. This means we recommend using the
latest commit on git master branch. We also provide git tags. 

This approach is also taken by Google [1]_ [2]_.

License
=======

Created by Gene C. and licensed under the terms of the MIT license.

 * SPDX-License-Identifier: MIT
 * Copyright (c) 2023 Gene C


.. _Github: https://github.com/gene-git/iwinfo
.. _Archlinux AUR: https://aur.archlinux.org/packages/iwinfo

.. [1] https://github.com/google/googletest  
.. [2] https://abseil.io/about/philosophy#upgrade-support

