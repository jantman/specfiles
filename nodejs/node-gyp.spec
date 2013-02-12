
%if 0%{?rhel}
# work around to allow us to find provides/requires with rpm < 4.9,
# which do not understand the magic in /usr/lib/rpm/nodejs.(req|prov)
%global __find_provides %{_rpmconfigdir}/nodejs.prov
%global __find_requires %{_rpmconfigdir}/nodejs.req
%global _use_internal_dependency_generator 0
%endif

Name:       node-gyp
Version:    0.8.2
Release:    4%{?dist}
Summary:    Node.js native addon build tool
License:    MIT
Group:      System Environment/Libraries
URL:        https://github.com/TooTallNate/node-gyp
Source0:    http://registry.npmjs.org/node-gyp/-/node-gyp-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

# These patches are Fedora-specific for the moment, although I'd like to find
# a way to support this kind of stuff upstream.

# use RPM installed headers by default instead of downloading a source tree
# for the currently running node version
Patch1:     node-gyp-addon-gypi.patch

# use the system gyp
Patch2:     node-gyp-system-gyp.patch

BuildRequires:  nodejs-devel

%if 0%{?rhel}
# this will ONLY build with the macros, scripts, etc. from redhat-rpm-config
BuildRequires: redhat-rpm-config
BuildRequires: /usr/bin/python

# CentOS 6.x and lower use rpm < 4.9, so they don't understand the fancy new automatic
# dependency generation for scripting languages
Requires: /bin/sh /bin/bash /usr/bin/env
%endif

Requires: gyp
Requires: nodejs-devel v8-devel libuv-devel
Requires: gcc-c++

%description
node-gyp is a cross-platform command-line tool written in Node.js for compiling
native addon modules for Node.js, which takes away the pain of dealing with the
various differences in build platforms. It is the replacement to the node-waf
program which is removed for node v0.8.

%prep
%setup -q -n package
%patch1 -p1
%patch2 -p1

%nodejs_fixdep request

#remove the bundled gyp
rm -rf gyp

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/node-gyp
cp -pr addon*.gypi bin lib legacy package.json %{buildroot}%{nodejs_sitelib}/node-gyp

mkdir -p %{buildroot}%{_bindir}
ln -sf ../lib/node_modules/node-gyp/bin/node-gyp.js %{buildroot}%{_bindir}/node-gyp

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/node-gyp
%{_bindir}/node-gyp
%doc README.md LICENSE

%changelog
* Thu Feb 07 2013 Jason Antman <Jason.Antman@cmgdigital.com> - 0.8.2-4
- setup to build on CentOS 6 - force __find_provides and __find_requires to the scripts from nodejs/nodejs-devel
- force old external dependency generator, as the fancy logic triggered by /usr/lib/rpm/fileattrs/nodejs.attr isn't recognized by rpm < 4.9.0
- Also build requires nodejs, as the rpm macros and scripts are in that package instead of nodejs-devel.

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.8.2-3
- add missing build section

* Sat Jan 05 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.8.2-2
- use RPM-installed headers by default
- now patched to use the system gyp instead of relying on a symlink

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.8.2-1
- new upstream release 0.8.2
- clean up for submission

* Thu Apr 26 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.4.1-2
- fix dependencies

* Wed Apr 18 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.4.1-1
- New upstream release 0.4.1

* Fri Apr 06 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.11-1
- New upstream release 0.3.11

* Mon Apr 02 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.10-1
- New upstream release 0.3.10

* Thu Mar 29 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.9-1
- New upstream release 0.3.9

* Wed Mar 28 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.8-1
- new upstream release 0.3.8

* Thu Mar 22 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.7-1
- new upstream release 0.3.7

* Thu Mar 15 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.5-1
- initial package
