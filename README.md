specfiles
=========

A collection of my RPM spec files for RHEL/CentOS and Fedora. These are largely spec files from other repositories or upstream locations, modified to build on CentOS 5 and 6, or other distributions. Be aware that some of these are pulled in from my other repositories using git submodules.

* carbon.spec - [Graphite](http://graphite.wikidot.com/)'s carbon-cache daemon. (current version: 0.9.10; this is pulled in as an external)
* graphite-web.spec - [Graphite](http://graphite.wikidot.com/)'s graphite-web component. (current version: 0.9.10; this is pulled in as an external)
* nodejs/ - nodejs, npm and all of their dependencies. This is a subdirectory because there are a LOT of them.
* whisper.spec - [Graphite](http://graphite.wikidot.com/)'s whisper daemon. (current version: 0.9.10; this is pulled in as an external)

To-Do:
------
* nodejs/gyp.spec: per tchollingsworth, fix to always use python26. http-parser build was failing on cent5 because gyp was using the system python 2.4, which it doesn't work with.
* nodejs/nodejs.spec: per tchollingsworth, the requirement of c-ares 1.9.0 would override c-ares 1.7.0 from RHEL Base, and EPEL must NOT override RHEL base. We need to know if 1.9.0 is *really* required, and if so, some up with a parallel-installable compatible package.
* nodejs/nodejs.spec: Need to figure out what's going on with packaging the LICENSE file, or need to make nodejs-docs depend on the nodejs package; we need to make sure the LICENSE file is *always* installed.

