
%if 0%{?rhel}
# work around to allow us to find provides/requires with rpm < 4.9,
# which do not understand the magic in /usr/lib/rpm/nodejs.(req|prov)
%global __find_provides %{_rpmconfigdir}/nodejs.prov
%global __find_requires %{_rpmconfigdir}/nodejs.req
%global _use_internal_dependency_generator 0
%endif

Name: nodejs
Version: 0.9.5
Release: 11%{?dist}
Summary: JavaScript runtime
License: MIT and ASL 2.0 and ISC and BSD
Group: Development/Languages
URL: http://nodejs.org/

# Exclusive archs must match v8
ExclusiveArch: %{ix86} x86_64 %{arm}

Source0: http://nodejs.org/dist/v%{version}/node-v%{version}.tar.gz
Source1: macros.nodejs
Source2: nodejs.attr
Source3: nodejs.prov
Source4: nodejs.req
Source5: nodejs-symlink-deps
Source6: nodejs-fixdep

# V8 presently breaks ABI at least every x.y release while never bumping SONAME,
# so we need to be more explicit until spot fixes that
%global v8_ge 1:3.13.7.5
%global v8_lt 1:3.14

BuildRequires: v8-devel >= %{v8_ge}
BuildRequires: http-parser-devel >= 2.0
BuildRequires: libuv-devel
BuildRequires: c-ares-devel >= 1.9.0
BuildRequires: zlib-devel
# Node.js requires some features from openssl 1.0.1 for SPDY support
BuildRequires: openssl-devel >= 1:1.0.1

%if 0%{?rhel}
# this will ONLY build with the macros, scripts, etc. from redhat-rpm-config
BuildRequires: redhat-rpm-config
BuildRequires: /usr/bin/python

# CentOS 6.x and lower use rpm < 4.9, so they don't understand the fancy new automatic
# dependency generation for scripting languages
Requires: /bin/sh /bin/bash /usr/bin/env
%endif

Requires: v8%{?isa} >= %{v8_ge}
Requires: v8%{?isa} < %{v8_lt}

#virtual provides for automatic depedency generation
Provides: nodejs(engine) = %{version}

# Node.js currently has a conflict with the 'node' package in Fedora
# The ham-radio group has agreed to rename their binary for us, but
# in the meantime, we're setting an explicit Conflicts: here
Conflicts: node <= 0.3.2-11

%description
Node.js is a platform built on Chrome's JavaScript runtime
for easily building fast, scalable network applications.
Node.js uses an event-driven, non-blocking I/O model that
makes it lightweight and efficient, perfect for data-intensive
real-time applications that run across distributed devices.

%package devel
Summary: JavaScript runtime - development headers
Group: Development/Languages
Requires: %{name} == %{version}-%{release}

%description devel
Development headers for the Node.js JavaScript runtime.

%package docs
Summary: Node.js API documentation
Group: Documentation

%description docs
The API documentation for the Node.js JavaScript runtime.

%prep
%setup -q -n node-v%{version}

# Make sure nothing gets included from bundled deps:
# We only delete the source and header files, because
# the remaining build scripts are still used.

find deps/cares -name "*.c" -exec rm -f {} \;
find deps/cares -name "*.h" -exec rm -f {} \;

find deps/npm -name "*.c" -exec rm -f {} \;
find deps/npm -name "*.h" -exec rm -f {} \;

find deps/zlib -name "*.c" -exec rm -f {} \;
find deps/zlib -name "*.h" -exec rm -f {} \;

find deps/v8 -name "*.c" -exec rm -f {} \;
find deps/v8 -name "*.h" -exec rm -f {} \;

find deps/http_parser -name "*.c" -exec rm -f {} \;
find deps/http_parser -name "*.h" -exec rm -f {} \;

find deps/openssl -name "*.c" -exec rm -f {} \;
find deps/openssl -name "*.h" -exec rm -f {} \;

find deps/uv -name "*.c" -exec rm -f {} \;
find deps/uv -name "*.h" -exec rm -f {} \;

%build
# build with debugging symbols and add defines from libuv (#892601)
export CFLAGS='%{optflags} -g -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64'
export CXXFLAGS='%{optflags} -g -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64'

./configure --prefix=%{_prefix} \
           --shared-v8 \
           --shared-openssl \
           --shared-zlib \
           --shared-cares \
           --shared-libuv \
           --shared-http-parser \
           --without-npm \
           --without-dtrace

# Setting BUILDTYPE=Debug builds both release and debug binaries
make BUILDTYPE=Debug %{?_smp_mflags}

%install
rm -rf %{buildroot}

./tools/install.py install %{buildroot}

# and remove dtrace file again
rm -rf %{buildroot}/%{_prefix}/lib/dtrace

# Set the binary permissions properly
chmod 0755 %{buildroot}/%{_bindir}/node

# Install the debug binary and set its permissions
install -Dpm0755 out/Debug/node %{buildroot}/%{_bindir}/node_g

# own the sitelib directory
mkdir -p %{buildroot}%{_prefix}/lib/node_modules

# install rpm magic
install -Dpm0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.nodejs
install -Dpm0644 %{SOURCE2} %{buildroot}%{_rpmconfigdir}/fileattrs/nodejs.attr
install -pm0755 %{SOURCE3} %{buildroot}%{_rpmconfigdir}/nodejs.prov
install -pm0755 %{SOURCE4} %{buildroot}%{_rpmconfigdir}/nodejs.req
install -pm0755 %{SOURCE5} %{buildroot}%{_rpmconfigdir}/nodejs-symlink-deps
install -pm0755 %{SOURCE6} %{buildroot}%{_rpmconfigdir}/nodejs-fixdep

#install documentation
mkdir -p %{buildroot}%{_defaultdocdir}/%{name}-docs-%{version}/html
cp -pr doc/* %{buildroot}%{_defaultdocdir}/%{name}-docs-%{version}/html
rm -f %{_defaultdocdir}/%{name}-docs-%{version}/html/nodejs.1

#install development headers
#FIXME: we probably don't really need *.h but node-gyp downloads the whole
#freaking source tree so I can't be sure ATM
mkdir -p %{buildroot}%{_includedir}/node
cp -p src/*.h %{buildroot}%{_includedir}/node

#node-gyp needs common.gypi too
mkdir -p %{buildroot}%{_datadir}/node
cp -p common.gypi %{buildroot}%{_datadir}/node

%files
%doc ChangeLog LICENSE README.md AUTHORS
%{_bindir}/node
%{_mandir}/man1/node.*
%{_sysconfdir}/rpm/macros.nodejs
%{_rpmconfigdir}/fileattrs/nodejs.attr
%{_rpmconfigdir}/nodejs*
%dir %{_prefix}/lib/node_modules

%files devel
%{_bindir}/node_g
%{_includedir}/node
%{_datadir}/node

%files docs
%{_defaultdocdir}/%{name}-docs-%{version}

%changelog
* Thu Feb 07 2013 Jason Antman <Jason.Antman@cmgdigital.com> - 0.9.5-11
- setup to build on CentOS 6 - force __find_provides and __find_requires to the scripts from nodejs/nodejs-devel
- force old external dependency generator, as the fancy logic triggered by /usr/lib/rpm/fileattrs/nodejs.attr isn't recognized by rpm < 4.9.0
- Also build requires nodejs, as the rpm macros and scripts are in that package instead of nodejs-devel.

* Thu Jan 31 2013 Jason Antman <Jason.Antman@cmgdigital.com> - 0.9.5-10
- specify build requirement of c-ares-devel >= 1.9.0
- specify build requirement of libuv-devel 0.9.4
- remove duplicate %doc LICENSE that was causing cpio 'Bad magic' error on CentOS6

* Sat Jan 12 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-9
- fix brown paper bag bug in requires generation script

* Thu Jan 10 2013 Stephen Gallagher <sgallagh@redhat.com> - 0.9.5-8
- Build debug binary and install it in the nodejs-devel subpackage

* Thu Jan 10 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-7
- don't use make install since it rebuilds everything

* Thu Jan 10 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-6
- add %%{?isa}, epoch to v8 deps

* Wed Jan 09 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-5
- add defines to match libuv (#892601)
- make v8 dependency explicit (and thus more accurate)
- add -g to $C(XX)FLAGS instead of patching configure to add it
- don't write pointless 'npm(foo) > 0' deps

* Sat Jan 05 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-4
- install development headers
- add nodejs_sitearch macro

* Wed Jan 02 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-3
- make nodejs-symlink-deps actually work

* Tue Jan 01 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-2
- provide nodejs-devel so modules can BuildRequire it (and be consistent
  with other interpreted languages in the distro)

* Tue Jan 01 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.5-1
- new upstream release 0.9.5
- provide nodejs-devel for the moment
- fix minor bugs in RPM magic
- add nodejs_fixdep macro so packagers can easily adjust dependencies in
  package.json files

* Wed Dec 26 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.9.4-1
- new upstream release 0.9.4
- system library patches are now upstream
- respect optflags
- include documentation in subpackage
- add RPM dependency generation and related magic
- guard libuv depedency so it always gets bumped when nodejs does
- add -devel subpackage with enough to make node-gyp happy

* Wed Dec 19 2012 Dan Horák <dan[at]danny.cz> - 0.9.3-8
- set exclusive arch list to match v8

* Tue Dec 18 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-7
- Add remaining changes from code review
- Remove unnecessary BuildRequires on findutils
- Remove %%clean section

* Fri Dec 14 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-6
- Fixes from code review
- Fix executable permissions
- Correct the License field
- Build debuginfo properly

* Thu Dec 13 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-5
- Return back to using the standard binary name
- Temporarily adding a conflict against the ham radio node package until they
  complete an agreed rename of their binary.

* Wed Nov 28 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-4
- Rename binary and manpage to nodejs

* Mon Nov 19 2012 Stephen Gallagher <sgallagh@redhat.com> - 0.9.3-3
- Update to latest upstream development release 0.9.3
- Include upstreamed patches to unbundle dependent libraries

* Tue Oct 23 2012 Adrian Alves <alvesadrian@fedoraproject.org>  0.8.12-1
- Fixes and Patches suggested by Matthias Runge

* Mon Apr 09 2012 Adrian Alves <alvesadrian@fedoraproject.org> 0.6.5
- First build.

