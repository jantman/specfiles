#!/usr/bin/python -t
# -*- mode: Python; indent-tabs-mode: nil; coding: utf-8 -*-
#
# Copyright (c) 2005-2009 Fedora Project
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#################################
# This script is based on version 1.0.6 of rpmdev-bumpspec from the rpmdev package.
# it is modified to also make the necessary changes for the package in question to
# build on CentOS 6 (and probably older as well).
#

import commands
import re
import subprocess
import sys
import textwrap
import time
from optparse import OptionParser

__version__ = "1.0.6"

NEW_BUILDREQUIRES = """%if 0%{?rhel}
# this will ONLY build with the macros, scripts, etc. from redhat-rpm-config
BuildRequires: redhat-rpm-config
BuildRequires: /usr/bin/python

# CentOS 6.x and lower use rpm < 4.9, so they don't understand the fancy new automatic
# dependency generation for scripting languages
Requires: /bin/sh /bin/bash /usr/bin/env
%endif
"""

CHANGELOG_COMMENT = """- setup to build on CentOS 6 - force __find_provides and __find_requires to the scripts from nodejs/nodejs-devel
- force old external dependency generator, as the fancy logic triggered by /usr/lib/rpm/fileattrs/nodejs.attr isn't recognized by rpm < 4.9.0
- Also build requires nodejs, as the rpm macros and scripts are in that package instead of nodejs-devel."""

NEW_MACROS = """
%if 0%{?rhel}
# work around to allow us to find provides/requires with rpm < 4.9,
# which do not understand the magic in /usr/lib/rpm/nodejs.(req|prov)
%global __find_provides %{_rpmconfigdir}/nodejs.prov
%global __find_requires %{_rpmconfigdir}/nodejs.req
%global _use_internal_dependency_generator 0
%endif
"""

class BumpSpecError(Exception):
    pass

class SpecFile:
    def __init__(self, filename, verbose=False, rightmost=False):
        self.verbose = verbose
        self.rightmost = rightmost

        self.filename = filename
        f = open(filename,"r")
        self.lines = f.readlines()
        f.close()
        
    def bumpRelease(self):
        bump_patterns = [(re.compile(r"^Release\s*:\s*(\d+.*)", re.I), self.increase), 
                       (re.compile(r"^%(?:define|global)\s+rel\s+(\d+.*)"), self.increase), 
                       (re.compile(r"^%(?:define|global)\s+release\s+(\d+.*)", re.I), self.increase), 
                       (re.compile(r"^Release\s*:\s+%release_func\s+(\d+.*)"), self.increase),
                       (re.compile(r"^%(?:define|global)\s+baserelease\s+(\d+.*)"), self.increase),
                       ]
        skip_pattern = re.compile(r"\$Revision:")
        for i in range(len(self.lines)):
            if skip_pattern.search(self.lines[i]):
                continue
            for bumpit, bumpit_func in bump_patterns:
                (self.lines[i], n) = bumpit.subn(bumpit_func, self.lines[i], 1)
                if n:  # bumped
                    return
        
        # Here, no line matched at all.
        # Happens with macro-overloaded spec files e.g.
        # Bump ^Release: ... line least-insignificant.
        for i in range(len(self.lines)):
            if self.lines[i].startswith('Release:'):
                old = self.lines[i][len('Release:'):].rstrip()
                new = self.increaseFallback(old)
                if self.verbose:
                    self.debugdiff(old, new)
                self.lines[i] = self.lines[i].replace(old, new)
                return

        if self.verbose:
            print >> sys.stderr, 'ERROR: No release value matched:', self.filename
            sys.exit(1)

    def addChangelogEntry(self, evr, entry, email):
        if len(evr):
            evrstring = ' - %s' % evr
        else:
            evrstring = ''
        changematch = re.compile(r"^%changelog")
        date = time.strftime("%a %b %d %Y", time.localtime(time.time()))
        newchangelogentry = "%%changelog\n* %s %s%s\n%s\n\n" % \
            (date, email, evrstring, entry)
        for i in range(len(self.lines)):
            if(changematch.match(self.lines[i])):
                self.lines[i] = newchangelogentry
                break

    def appendBuildRequires(self, addedString):
        buildmatch = re.compile(r"^BuildRequires:")
        buildline = 0
        for i in range(len(self.lines)):
            if(buildmatch.match(self.lines[i])):
                buildline = i
        if buildline is None:
            blankmatch = re.compile(r"^$")
            for i in range(len(self.lines)):
                if(blankmatch.match(self.lines[i])):
                    buildline = i-1
                    break
        self.lines[buildline] = "%s\n%s" % (self.lines[buildline], addedString)

    def prependMacros(self, addedString):
        namematch = re.compile(r"^Name:")
        nameline = 0
        for i in range(len(self.lines)):
            if(namematch.match(self.lines[i])):
                nameline = i
        self.lines[nameline] = "%s\n%s" % (addedString, self.lines[nameline])

    def increaseMain(self, release):
        if release.startswith('0.'):
            relre = re.compile(r'^0\.(?P<rel>\d+)(?P<post>.*)')
            pre = True
        else:
            relre = re.compile(r'^(?P<rel>\d+)(?P<post>.*)')
            pre = False
        relmatch = relre.search(release)
        if not relmatch:  # pattern match failed
            raise BumpSpecError
        value = int(relmatch.group('rel'))
        post = relmatch.group('post')

        if not pre:
            if post.find('rc')>=0:
                print 'WARNING: Bad pre-release versioning scheme:', self.filename
                raise BumpSpecError
            new = `value+1`+post
        else:
            new = '0.'+`value+1`+post
        return new

    def increaseJPP(self, release):
        """Fedora jpackage release versioning scheme"""

        relre = re.compile(r'(?P<prefix>.*)(?P<rel>\d+)(?P<jpp>jpp\.)(?P<post>.*)')
        relmatch = relre.search(release)
        if not relmatch:  # pattern match failed
            raise BumpSpecError
        
        prefix = relmatch.group('prefix')
        value = int(relmatch.group('rel'))
        jpp = relmatch.group('jpp')
        post = relmatch.group('post')

        newpost = self.increaseMain(post)
        new = prefix+str(value)+jpp+newpost
        return new

    def increaseFallback(self, release):
        """bump at the very-right or add .1 as a last resort"""
        relre = re.compile(r'(?P<prefix>.+\.)(?P<post>\d+$)')
        relmatch = relre.search(release)
        if relmatch:
            prefix = relmatch.group('prefix')
            post = relmatch.group('post')
            new = prefix+self.increaseMain(post)
        else:
            new = release.rstrip()+'.1'
        return new

    def increase(self, match):
        old = match.group(1)  # only the release value
        try:
            if self.rightmost:
                new = self.increaseFallback(old)
            elif old.find('jpp')>0:
                new = self.increaseJPP(old)
            else:
                new = self.increaseMain(old)
        except BumpSpecError:
            new = self.increaseFallback(old)
        if self.verbose:
            self.debugdiff(old, new)
        # group 0 is the full line that defines the release
        return match.group(0).replace(old, new)

    def writeFile(self, filename):
        f = open(filename, "w")
        f.writelines(self.lines)
        f.close()

    def debugdiff(self, old, new):
        print self.filename
        print '-%s' % old
        print '+%s\n' % new

if __name__ == "__main__":
    usage = '''Usage: %prog [OPTION]... SPECFILE...

centos_fix_nodejs_spec.py bumps release tags in specfiles.'''

    version = '''centos_fix_nodejs_spec.py version %s

Copyright (c) 2005-2009 Fedora Project
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.''' % __version__

    userstring = subprocess.Popen("rpmdev-packager 2>/dev/null", shell = True,
                                  stdout = subprocess.PIPE).communicate()[0]
    userstring = userstring.strip() or None

    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--comment", default=CHANGELOG_COMMENT,
                      help="changelog comment (default: \"- rebuilt\")")
    parser.add_option("-u", "--userstring", default=userstring,
                      help="user name+email string (default: output from "+
                      "rpmdev-packager(1))")
    parser.add_option("-r", "--rightmost", default=False, action='store_true',
                      help="bump the rightmost integer or add a .1")
    parser.add_option("-V", "--verbose", default=False, action='store_true',
                      help="more output")
    parser.add_option("-v", "--version", default=False, action='store_true',
                      help="output version number and exit")
    (opts, args) = parser.parse_args()

    if opts.version:
        print version
        sys.exit(0)

    if not args:
        parser.error('No specfiles specified')

    if not opts.userstring:
        parser.error('Userstring required, see option -u')

    # Grab bullet, insert one if not found.
    bullet_re = re.compile(r'^([^\s\w])\s', re.UNICODE)
    bullet = "-"
    match = bullet_re.search(opts.comment)
    if match:
        bullet = match.group(1)
    else:
        opts.comment = bullet + " " + opts.comment

    # Format comment.
    if opts.comment.find("\n") == -1:
        wrapopts = { "subsequent_indent": (len(bullet)+1) * " ",
                     "break_long_words":  False }
        if sys.version_info[:2] > (2, 5):
            wrapopts["break_on_hyphens"] = False
        opts.comment = textwrap.fill(opts.comment, 80, **wrapopts)

    for aspec in args:
        s = SpecFile(aspec, opts.verbose, opts.rightmost)
        s.bumpRelease()
        s.appendBuildRequires(NEW_BUILDREQUIRES)
        s.prependMacros(NEW_MACROS)
        s.writeFile(aspec)

        # Get EVR for changelog entry.
        cmd = ("rpm", "-q", "--specfile", "--define", "dist %{nil}",
               "--qf=%|epoch?{%{epoch}:}:{}|%{version}-%{release}\n", aspec)
        popen = subprocess.Popen(cmd, stdout = subprocess.PIPE)
        evr = popen.communicate()[0].split("\n")[0]

        s.addChangelogEntry(evr, opts.comment, opts.userstring)
        s.writeFile(aspec)

sys.exit(0)
