Changelog
=========

Tags
====

.. code-block:: text

	2.0.1 (2024-04-13) -> 5.1.1 (2026-09-04)
	70 commits.

Commits
=======


* 2026-09-04  : **5.1.1**

.. code-block:: text

              - Add meson files to repo

* 2026-09-04  : **5.1.0, origin/master**

.. code-block:: text

              - **5.1.0**
            
                * Meson / meson-python for build and package management
                * Simplify python code.
                  New dependency:  pyconcurrent package
                * Improve iwinfo.
                  C-program which runs the application and if permitted (root or wheel)
                  gives the application the approrpriate network capabilties to scan.
                  The information other than scanning the network is available to
                  unprivileged users.
 2026-01-06   ⋯

.. code-block:: text

              - update Docs/Changelog

* 2026-01-06  : **5.0.1**

.. code-block:: text

              - PKGBUILD small change
 2026-01-04   ⋯

.. code-block:: text

              - update Docs/Changelog
              - **5.0.0**
            
                * Reorg source a little
                * Switch python packaging from hatch to uv
                * License GPL-2.0-or-later

* 2025-11-25  : **5.0.0**

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-11-25  : **4.8.0**

.. code-block:: text

              - New option "-v" prints all frequencies supported by each phy
                  mark any disabled channels, show if a channel is connect only using *no initiate radio*
                  DFS channels may display *radar detected*
              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-11-25  : **4.7.1**

.. code-block:: text

              - * Bug fix: Scan occasionally gets device busy which is handled by a couple of retries.
                  However, when device is not responding at all this kept trying repeatedly. Fixed
            
                * Bug fix: Misidentification of some phy(sical) (hardware) capabilities. Notably 802.11be (wifi-7)
 2025-06-26   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-06-26  : **4.5.0**

.. code-block:: text

              - Update local copy of latest run_prog() from pyconcurrent
 2025-06-22   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-06-22  : **4.4.0**

.. code-block:: text

              - Put run_cmd in its own file

* 2025-06-22  : **4.3.0**

.. code-block:: text

              - run_prog: sync our copy with latest from pyconcurrent
 2025-06-16   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-06-16  : **4.2.0**

.. code-block:: text

              - Improve way we run external programs - handle larger output, better exception managemen etc
 2025-05-21   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-05-21  : **4.1.0**

.. code-block:: text

              - Use builtin types where possible. e.g. typing.List -> list
 2025-05-18   ⋯

.. code-block:: text

              - update Docs/Changelog Docs/${my_name}.pdf

* 2025-05-18  : **4.0.0**

.. code-block:: text

              - Code now complies with: PEP-8, PEP-257, PEP-484 and PEP-561
                Code Refactor & clean ups.
                Wireless "host" database file name.
            
                  Preferred name is now known-hosts.toml, which aligns better with its purpose and format.
                  The previous names will continue to work just fine as well.
            
                  The known host file will first be looked for in the directory *./etc/iwinfo/* and then */etc/iwinfo/*.
 2025-02-25   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2025-02-25  : **3.5.1**

.. code-block:: text

              - Fix typo in PKGBUILD from 3.5.0
              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2025-02-25  : **3.5.0**

.. code-block:: text

              - More checking of missing programs. Found by aur report from @simona
                Add iwd as dependency to provide /usr/bin/iwctl
 2024-12-31   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/mkpkg.pdf for 3.4.2

* 2024-12-31  : **3.4.2**

.. code-block:: text

              - Git tags are now signed.
                Update SPDX tags
                Add git signing key to Arch Package
 2024-07-12   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-12  : **3.4.1**

.. code-block:: text

              - Update README
 2024-07-10   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-10  : **3.4.0**

.. code-block:: text

              - Bugfix when no user wifi.db returning incorrect number of parameters
              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-10  : **3.3.0**

.. code-block:: text

              - Report interface info before starting network scan
 2024-07-09   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-09  : **3.2.0**

.. code-block:: text

              - update Docs/Changelog.rst Docs/iwinfo.pdf
              - User wifi.db separate model into make, model
              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-09  : **3.0.0**

.. code-block:: text

              - Scan sort order now frequency band (high->low) then on signal (best->worst)
              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-09  : **2.10.0**

.. code-block:: text

              - Add channel and mac address to report
              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-09  : **2.9.0**

.. code-block:: text

              - Add channel and mac address to report
 2024-07-08   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-08  : **2.8.0**

.. code-block:: text

              - Add IP address to report
              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-08  : **2.7.0**

.. code-block:: text

              - Ensure works even if no active wifi settings
              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-08  : **2.6.1**

.. code-block:: text

              - bug in scanning report from too much tidying - dont always listen to pylint
              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-08  : **2.5.0**

.. code-block:: text

              - Additional fieleds in report:
                  connection status
                  security and wifi tx/rx mode if iwd is used
 2024-07-07   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-07-07  : **2.3.0**

.. code-block:: text

              - Scan report sort firt by band and then by signal instead of just signal
 2024-05-04   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-05-04  : **2.2.0**

.. code-block:: text

              - libcap-ng versions >= 0.6 provide python binding. We now use it instad of using our own calls to c-library libcap-ng.so
              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-05-04  : **2.1.0**

.. code-block:: text

              - We handle capabilities directly so drop all refs to prctl since its not used. Remove it from PKGBUILD as well
 2024-04-30   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-04-30  : **2.0.6**

.. code-block:: text

              - Take Changelog "hack" out of PKGBUILD ... was a bad idea
 2024-04-29   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-04-29  : **2.0.5**

.. code-block:: text

              - Improve pulling Changelog for pacman -Qc
 2024-04-13   ⋯

.. code-block:: text

              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-04-13  : **2.0.4**

.. code-block:: text

              - improve readme
              - tweak readme

* 2024-04-13  : **2.0.3**

.. code-block:: text

              - update Docs/Changelog.rst Docs/iwinfo.pdf
              - Add changelog to package so pacman -Qc shows it
              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-04-13  : **2.0.2**

.. code-block:: text

              - Change gitname in PKGBUILD
              - update Docs/Changelog.rst Docs/iwinfo.pdf

* 2024-04-13  : **2.0.1**

.. code-block:: text

              - Improve package description
              - Initial public release


