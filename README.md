specfiles
=========

[![Project Status: Active - The project has reached a stable, usable state and is being actively developed.](http://www.repostatus.org/badges/0.1.0/active.svg)](http://www.repostatus.org/#active)

A collection of my RPM spec files for RHEL/CentOS and Fedora. These are largely spec files from other repositories or upstream locations, modified to build on CentOS 5 and 6, or other distributions. Be aware that some of these are pulled in from my other repositories using git submodules.

* carbon.spec - [Graphite](http://graphite.wikidot.com/)'s carbon-cache daemon. (current version: 0.9.10; this is pulled in as an external)
* graphite-web.spec - [Graphite](http://graphite.wikidot.com/)'s graphite-web component. (current version: 0.9.10; this is pulled in as an external)
* nodejs/ - __NOTE__ - This is now included in EPEL, you should use the stuff there. nodejs, npm and all of their dependencies. This is a subdirectory because there are a LOT of them.
* nodejs-centos5.spec - (external) my fork of kazuhisya's 'nodejs-rpm' repo for CentOS 5.
* whisper.spec - [Graphite](http://graphite.wikidot.com/)'s whisper daemon. (current version: 0.9.10; this is pulled in as an external)



