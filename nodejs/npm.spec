%if 0%{?rhel}
# work around to allow us to find provides/requires with rpm < 4.9,
# which do not understand the magic in /usr/lib/rpm/nodejs.(req|prov)
%global __find_provides %{_rpmconfigdir}/nodejs.prov
%global __find_requires %{_rpmconfigdir}/nodejs.req 
%global _use_internal_dependency_generator 0
%endif

Name:       npm
Version:    1.2.1
Release:    3%{?dist}
Summary:    Node.js Package Manager
License:    MITNFA
Group:      Development/Tools
URL:        http://npmjs.org/
Source0:    http://registry.npmjs.org/npm/-/npm-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires: nodejs-devel nodejs
%if 0%{?rhel}
# this will ONLY build with the macros, scripts, etc. from redhat-rpm-config
BuildRequires: redhat-rpm-config
BuildRequires: /usr/bin/python

# CentOS 6.x and lower use rpm < 4.9, so they don't understand the fancy new automatic
# dependency generation for scripting languages
Requires: /bin/sh /bin/bash /usr/bin/env /usr/bin/node
%endif

%description
npm is a package manager for node.js. You can use it to install and publish your
node programs. It manages dependencies and does other cool stuff.

%prep
%setup -q -n package

%nodejs_fixdep lru-cache 2.2.x
%nodejs_fixdep init-package-json 0.0.x

#remove bundled modules
rm -rf node_modules

#add a missing shebang
sed -i -e '1i#!/usr/bin/node' bin/read-package-json.js

# prefix all manpages with "npm-"
pushd man
for dir in *; do
    pushd $dir
    for page in *; do
        if [[ $page != npm* ]]; then
            mv $page npm-$page
        fi
    done
    popd
done
popd

# delete windows stuff
rm bin/npm.cmd bin/node-gyp-bin/node-gyp.cmd

# globals.1 and folders.1 are the same package and the former is outdated
# https://github.com/isaacs/npm/issues/3078
ln -sf npm-folders.1 man/man1/npm-global.1

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/npm
cp -pr bin lib cli.js package.json %{buildroot}%{nodejs_sitelib}/npm/

mkdir -p %{buildroot}%{_bindir}
ln -sf ../lib/node_modules/npm/bin/npm-cli.js %{buildroot}%{_bindir}/npm

# ghosted global config files
mkdir -p %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/npmrc
touch %{buildroot}%{_sysconfdir}/npmignore

# install to mandir
mkdir -p %{buildroot}%{_mandir}
cp -pr man/* %{buildroot}%{_mandir}/

# some symlinks to make `npm help` work
ln -sf %{_mandir} %{buildroot}%{nodejs_sitelib}/npm/man
ln -sf %{_defaultdocdir}/%{name}-%{version} %{buildroot}%{nodejs_sitelib}/npm/doc

%nodejs_symlink_deps

# probably needs network, need to investigate further
#%%check
#%%__nodejs test/run.js
#%%tap test/tap/*.js

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/npm
%ghost %{_sysconfdir}/npmrc
%ghost %{_sysconfdir}/npmignore
%{_bindir}/npm
%{_mandir}/man1/*
%{_mandir}/man3/*
%doc AUTHORS doc/* html README.md LICENSE

%changelog
* Wed Feb 06 2013 Jason Antman <Jason.Antman@cmgdigital.com> - 1.2.1-3
- add if block to set __find_provides and __find_requires on EL5/6, since
  rpm <= 4.9 doesn't know about the fancy logic triggered by
  /usr/lib/rpm/fileattrs/nodejs.attr from the nodejs/nodejs-devel package
- the required RPM macros and scripts are in nodejs not nodejs-devel,
  so install that too.

* Sat Jan 19 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.1-2
- fix rpmlint warnings

* Fri Jan 18 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.1-1
- new upstream release 1.2.1
- fix License tag

* Thu Jan 10 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.0-1
- new upstream release 1.2.0

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.70-2
- add missing build section

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.70-1
- new upstream release 1.1.70

* Wed May 02 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.19-1
- New upstream release 1.1.19

* Wed Apr 18 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.18-1
- New upstream release 1.1.18

* Fri Apr 06 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.16-1
- New upstream release 1.1.16

* Mon Apr 02 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.15-1
- New upstream release 1.1.15

* Thu Mar 29 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.14-1
- New upstream release 1.1.14

* Wed Mar 28 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.13-2
- new dependencies fstream-npm, uid-number, and fstream-ignore (indirectly)

* Wed Mar 28 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.13-1
- new upstream release 1.1.13

* Thu Mar 22 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.12-1
- new upstream release 1.1.12

* Thu Mar 15 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.9-1
- new upstream release 1.1.9

* Sun Mar 04 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.4-1
- new upstream release 1.1.4

* Sat Feb 25 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.2-1
- new upstream release 1.1.2

* Sat Feb 11 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.1-2
- fix node_modules symlink

* Thu Feb 09 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.1-1
- new upstream release 1.1.1

* Sun Jan 29 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.0-2.3
- new upstream release 1.1.0-3

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.0-2.2
- missing Group field for EL5

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.0-1.2
- new upstream release 1.1.0-2

* Tue Nov 17 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.106-1
- new upstream release 1.0.106
- ship manpages again

* Thu Nov 10 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.105-1
- new upstream release 1.0.105
- use relative symlinks instead of absolute
- fixes /usr/bin/npm symlink on i686

* Mon Nov 07 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.104-1
- new upstream release 1.0.104
- adds node 0.6 support

* Wed Oct 26 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.101-2
- missing Requires on nodejs-request
- Require compilers too so native modules build properly

* Tue Oct 25 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.101-1
- new upstream release
- use symlink /usr/lib/node_modules -> /usr/lib/nodejs instead of patching

* Thu Aug 25 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.26-2
- rebuilt with fixed nodejs_fixshebang macro from nodejs-devel-0.4.11-3

* Tue Aug 23 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.26-1
- initial package
