specfiles
=========

A collection of my RPM spec files for RHEL/CentOS and Fedora. These are largely spec files from other repositories or upstream locations, modified to build on CentOS 5 and 6, or other distributions. Be aware that some of these are pulled in from my other repositories using git submodules.

* carbon.spec - [Graphite](http://graphite.wikidot.com/)'s carbon-cache daemon. (current version: 0.9.10)
* graphite-web.spec - [Graphite](http://graphite.wikidot.com/)'s graphite-web component. (current version: 0.9.10)
* http-parser.spec - [joyent/http-parser](http://github.com/joyent/http-parser), dependency of nodejs. (current version: 2.0)
* nodejs.spec - [nodejs](http://nodejs.org/). (current version: 0.9.5)
* v8.spec - [Google v8 Javascript Engine](http://code.google.com/p/v8/), modified from Fedora 19 Rawhide specfile, dependency of nodejs. This was done for my employer, [CMG Digital](http://www.cmgdigital.com/). (current version: 3.13.7.5)
* whisper.spec - [Graphite](http://graphite.wikidot.com/)'s whisper daemon. (current version: 0.9.10)
