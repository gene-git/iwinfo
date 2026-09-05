.. SPDX-License-Identifier: GPL-2.0-or-later

======
iwinfo
======

Overview
========

iwinfo : Provide useful information about wireless network(s)

This is a command line program which is run in any terminal.
It shows some information about existing wireless connections
along with the result of an optional scan for wireless devices.
Scan is turned on using *-s* option.

Scanning wireless networks requires elevated privileges, which means either by running as
root or by being provided with the required cap_net_xxx capablilities. 
Scanning is only permitted to users who are members of *wheel* group.

This package provides the application, written in python, along with a small
C-program which is installed with cap_net_raw and cap_net_admin [#]_ 
and it provides the capabilities for the program to be run non-root.

Since this does add some level of risk, scanning is limited to root and members
of the *wheel* group only. 

Some addititional information is gathered using *iwctl* when *iwd* is running. 
These are the *ip addres*, *security mode* (e.g. WPA2), and *transmission type* (e.g. 802.11ax).
These require either root or membership in *network* or *wheel* groups.

Others will still be able to get local wireless device and connection info, but will
not be able to scan the network(s).

Summary:

    =====  ====   =============== =====================
    Info   User   Group *network* Group *wheel* or root
    =====  ====   =============== =====================
    Basic   ✔          ✔               ✔ 
    Extra   ✕          ✔               ✔
    Scan    ✕          ✕               ✔
    =====  ====   =============== =====================

 * All git tags are signed with arch@sapience.com key which is available via WKD
   or download from https://www.sapience.com/tech. Add the key to your package builder gpg keyring.
   The key is included in the Arch package and the source= line with *?signed* at the end can be used
   to verify the git tag.  You can also manually verify the signature

.. [#] See man capabilities.

Key features
============

 * Shows local wireless device(s) and connection info.
 * Show summary of wireless hardware capabilities
 * Scans wireless network(s) and provides compact report

Recent Changes
==============

**5.1.0**

* Meson / meson-python for build and package management
* Simplify python code.
  New dependency:  pyconcurrent package
* Improve iwinfo.
  C-program which runs the application and if permitted (root or wheel)
  gives the application the approrpriate network capabilties to scan.
  The information other than scanning the network is available to
  unprivileged users. 

===============
Getting Started
===============

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


