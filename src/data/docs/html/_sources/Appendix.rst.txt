========
Appendix
========

Installation
============

On Arch you can build using the provided PKGBUILD in the packaging directory or from the AUR.
To build manually, clone the repo and ::

    ./scripts/do-build
    ./scripts/do-install <destination-dir>

Dependencies
============

* Run Time :

  * python          (>= 3.14)
  * libcap-ng
  * pycocurrent

* Building Package:

  * git
  * gcc
  * make
  * rsync


License
=======

Created by Gene C. and licensed under the terms of the GPL-2.0-or-later license.

 * SPDX-License-Identifier: GPL-2.0-or-later
 * SPDX-FileCopyrightText: © 2023-present  Gene C <arch@sapience.com>
