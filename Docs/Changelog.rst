Changelog
=========

**[3.3.0] ----- 2024-07-10** ::

	    Report interface info before starting network scan
	    update Docs/Changelog.rst Docs/iwinfo.pdf


**[3.2.0] ----- 2024-07-09** ::

	    update Docs/Changelog.rst Docs/iwinfo.pdf
	    User wifi.db separate model into make, model
	    update Docs/Changelog.rst Docs/iwinfo.pdf


**[3.0.0] ----- 2024-07-09** ::

	    Scan sort order now frequency band (high->low) then on signal (best->worst)
	    update Docs/Changelog.rst Docs/iwinfo.pdf


**[2.10.0] ----- 2024-07-09** ::

	    Add channel and mac address to report
	    update Docs/Changelog.rst Docs/iwinfo.pdf


**[2.9.0] ----- 2024-07-09** ::

	    Add channel and mac address to report
	    update Docs/Changelog.rst Docs/iwinfo.pdf


**[2.8.0] ----- 2024-07-08** ::

	    Add IP address to report
	    update Docs/Changelog.rst Docs/iwinfo.pdf


**[2.7.0] ----- 2024-07-08** ::

	    Ensure works even if no active wifi settings
	    update Docs/Changelog.rst Docs/iwinfo.pdf


**[2.6.1] ----- 2024-07-08** ::

	    bug in scanning report from too much tidying - dont always listen to pylint
	    update Docs/Changelog.rst Docs/iwinfo.pdf


**[2.5.0] ----- 2024-07-08** ::

	    Additional fieleds in report:
	      connection status
	      security and wifi tx/rx mode if iwd is used
	    update Docs/Changelog.rst Docs/iwinfo.pdf


**[2.3.0] ----- 2024-07-07** ::

	    Scan report sort firt by band and then by signal instead of just signal
	    update Docs/Changelog.rst Docs/iwinfo.pdf


**[2.2.0] ----- 2024-05-04** ::

	    libcap-ng versions >= 0.6 provide python binding. We now use it instad of using our own calls to c-library libcap-ng.so
	    update Docs/Changelog.rst Docs/iwinfo.pdf


**[2.1.0] ----- 2024-05-04** ::

	    We handle capabilities directly so drop all refs to prctl since its not used. Remove it from PKGBUILD as well
	    update Docs/Changelog.rst Docs/iwinfo.pdf


**[2.0.6] ----- 2024-04-30** ::

	    Take Changelog "hack" out of PKGBUILD ... was a bad idea
	    update Docs/Changelog.rst Docs/iwinfo.pdf


**[2.0.5] ----- 2024-04-29** ::

	    Improve pulling Changelog for pacman -Qc
	    update Docs/Changelog.rst Docs/iwinfo.pdf


**[2.0.4] ----- 2024-04-13** ::

	    improve readme
	    tweak readme


**[2.0.3] ----- 2024-04-13** ::

	    update Docs/Changelog.rst Docs/iwinfo.pdf
	    Add changelog to package so pacman -Qc shows it
	    update Docs/Changelog.rst Docs/iwinfo.pdf


**[2.0.2] ----- 2024-04-13** ::

	    Change gitname in PKGBUILD
	    update Docs/Changelog.rst Docs/iwinfo.pdf


**[2.0.1] ----- 2024-04-13** ::

	    Improve package description
	    Initial public release


