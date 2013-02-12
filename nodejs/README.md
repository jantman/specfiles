nodejs specfiles
================

A collection of specfiles to build nodejs 0.9.5, npm and their dependencies on CentOS 6 (and maybe 5 if I ever get around to it). These are derived from the SRPMs currently in Fedora's Koji build system for fc19/Rawhide. For more information about these packages, see the following bugs in Fedora's Bugzilla: [908882](https://bugzilla.redhat.com/show_bug.cgi?id=908882).

Packages
--------
* gyp.spec
* http-parser.spec - [joyent/http-parser](http://github.com/joyent/http-parser), dependency of nodejs
* node-gyp.spec
* nodejs.spec - [nodejs](http://nodejs.org/)
* npm.spec - Node Package Manager
* v8.spec - [Google v8 Javascript Engine](http://code.google.com/p/v8/), modified from Fedora 19 Rawhide specfile, dependency of nodejs.

Utility Scripts
---------------
* centos_fix_nodejs_spec.py - script to "fix" the upstream specfiles for nodejs modules:
** add some missing things to buildrequires and requires
** override globals for __find_provides and __find_requires
** add changelog comment
** bump release number

nodejs/npm modules converted to RPM
------------------------------------
These are dependencies of npm:
* nodejs-abbrev.spec
* nodejs-ansi.spec
* nodejs-archy.spec
* nodejs-async.spec
* nodejs-block-stream.spec
* nodejs-charm.spec
* nodejs-chownr.spec
* nodejs-combined-stream.spec
* nodejs-config-chain.spec
* nodejs-couch-login.spec
* nodejs-delayed-stream.spec
* nodejs-form-data.spec
* nodejs-fstream-ignore.spec
* nodejs-fstream-npm.spec
* nodejs-fstream.spec
* nodejs-glob.spec
* nodejs-graceful-fs.spec
* nodejs-inherits.spec
* nodejs-ini.spec
* nodejs-init-package-json.spec
* nodejs-lockfile.spec
* nodejs-lru-cache.spec
* nodejs-mime.spec
* nodejs-minimatch.spec
* nodejs-mkdirp.spec
* nodejs-mute-stream.spec
* nodejs-nopt.spec
* nodejs-npmconf.spec
* nodejs-npmlog.spec
* nodejs-npm-registry-client.spec
* nodejs-once.spec
* nodejs-opener.spec
* nodejs-opts.spec
* nodejs-osenv.spec
* nodejs-promzard.spec
* nodejs-proto-list.spec
* nodejs-read-installed.spec
* nodejs-read-package-json.spec
* nodejs-read.spec
* nodejs-request.spec
* nodejs-retry.spec
* nodejs-rimraf.spec
* nodejs-semver.spec
* nodejs-sigmund.spec
* nodejs-slide.spec
* nodejs-tar.spec
* nodejs-tobi-cookie.spec
* nodejs-uid-number.spec
* nodejs-which.spec
* nodejs-yamlish.spec
