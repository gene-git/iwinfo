=========
Changelog
=========

Tags
====

::

	2.0.1 (2024-04-13) -> 4.1.0 (2025-05-21)
	52 commits.

Commits
=======


* 2025-05-21  : **4.1.0**

::

                Use builtin types where possible. e.g. typing.List -> list
 2025-05-18     update Docs/Changelog Docs/${my_name}.pdf

* 2025-05-18  : **4.0.0**

::

                Code now complies with: PEP-8, PEP-257, PEP-484 and PEP-561
                Code Refactor & clean ups.
                Wireless "host" database file name.
                  Preferred name is now known-hosts.toml, which aligns better with its
                  purpose and format.
                  The previous names will continue to work just fine as well.
                  The known host file will first be looked for in the directory
                  *./etc/iwinfo/* and then */etc/iwinfo/*.
 2025-02-25     update Docs/Changelog.rst Docs/iwinfo.pdf

* 2025-02-25  : **3.5.1**

::

                Fix typo in PKGBUILD from 3.5.0
                update Docs/Changelog.rst Docs/iwinfo.pdf

* 2025-02-25  : **3.5.0**

::

                More checking of missing programs. Found by aur report from @simona
                Add iwd as dependency to provide /usr/bin/iwctl
 2024-12-31     update Docs/Changelog.rst Docs/mkpkg.pdf for 3.4.2

* 2024-12-31  : **3.4.2**

::

                Git tags are now signed.
                Update SPDX tags
                Add git signing key to Arch Package
 2024-07-12     update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-12  : **3.4.1**

::

                Update README
 2024-07-10     update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-10  : **3.4.0**

::

                Bugfix when no user wifi.db returning incorrect number of parameters
                update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-10  : **3.3.0**

::

                Report interface info before starting network scan
 2024-07-09     update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-09  : **3.2.0**

::

                update Docs/Changelog.rst Docs/iwinfo.pdf
                User wifi.db separate model into make, model
                update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-09  : **3.0.0**

::

                Scan sort order now frequency band (high->low) then on signal (best->worst)
                update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-09  : **2.10.0**

::

                Add channel and mac address to report
                update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-09  : **2.9.0**

::

                Add channel and mac address to report
 2024-07-08     update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-08  : **2.8.0**

::

                Add IP address to report
                update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-08  : **2.7.0**

::

                Ensure works even if no active wifi settings
                update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-08  : **2.6.1**

::

                bug in scanning report from too much tidying - dont always listen to pylint
                update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-08  : **2.5.0**

::

                Additional fieleds in report:
                  connection status
                  security and wifi tx/rx mode if iwd is used
 2024-07-07     update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-07  : **2.3.0**

::

                Scan report sort firt by band and then by signal instead of just signal
 2024-05-04     update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-05-04  : **2.2.0**

::

                libcap-ng versions >= 0.6 provide python binding. We now use it instad of
                using our own calls to c-library libcap-ng.so
                update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-05-04  : **2.1.0**

::

                We handle capabilities directly so drop all refs to prctl since its not
                used. Remove it from PKGBUILD as well
 2024-04-30     update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-04-30  : **2.0.6**

::

                Take Changelog "hack" out of PKGBUILD ... was a bad idea
 2024-04-29     update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-04-29  : **2.0.5**

::

                Improve pulling Changelog for pacman -Qc
 2024-04-13     update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-04-13  : **2.0.4**

::

                improve readme
                tweak readme

* 2024-04-13  : **2.0.3**

::

                update Docs/Changelog.rst Docs/iwinfo.pdf
                Add changelog to package so pacman -Qc shows it
                update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-04-13  : **2.0.2**

::

                Change gitname in PKGBUILD
                update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-04-13  : **2.0.1**

::

                Improve package description
                Initial public release


