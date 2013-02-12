
%if 0%{?rhel}
# work around to allow us to find provides/requires with rpm < 4.9,
# which do not understand the magic in /usr/lib/rpm/nodejs.(req|prov)
%global __find_provides %{_rpmconfigdir}/nodejs.prov
%global __find_requires %{_rpmconfigdir}/nodejs.req
%global _use_internal_dependency_generator 0
%endif

Name:       nodejs-fstream
Version:    0.1.21
Release:    4%{?dist}
Summary:    Advanced file system stream objects for Node.js
License:    BSD
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/fstream
Source0:    http://registry.npmjs.org/fstream/-/fstream-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel

%if 0%{?rhel}
# this will ONLY build with the macros, scripts, etc. from redhat-rpm-config
BuildRequires: redhat-rpm-config
BuildRequires: /usr/bin/python

# CentOS 6.x and lower use rpm < 4.9, so they don't understand the fancy new automatic
# dependency generation for scripting languages
Requires: /bin/sh /bin/bash /usr/bin/env
%endif

%description
Provides advanced file system stream objects for Node.js.  These objects are
like FS streams, but with stat on them, and support directories and
symbolic links, as well as normal files.  Also, you can use them to set
the stats on a file, even if you don't change its contents, or to create
a symlink, etc.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/fstream
cp -pr lib fstream.js package.json %{buildroot}%{nodejs_sitelib}/fstream

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/fstream
%doc LICENSE README.md examples

%changelog
* Thu Feb 07 2013 Jason Antman <Jason.Antman@cmgdigital.com> - 0.1.21-4
- setup to build on CentOS 6 - force __find_provides and __find_requires to the scripts from nodejs/nodejs-devel
- force old external dependency generator, as the fancy logic triggered by /usr/lib/rpm/fileattrs/nodejs.attr isn't recognized by rpm < 4.9.0
- Also build requires nodejs, as the rpm macros and scripts are in that package instead of nodejs-devel.

* Sun Jan 13 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.1.21-3
- fix License tag

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.1.21-2
- add missing build section
- fix summary/description

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.1.21-1
- new upstream release 0.1.21
- clean up for submission

* Thu Mar 29 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.1.18-1
- New upstream release 0.1.18

* Wed Mar 28 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.1.17-1
- new upstream release 0.1.17

* Thu Mar 22 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.1.14-1
- new upstream release 0.1.14

* Sun Mar 04 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.1.13-1
- new upstream release 0.1.13

* Thu Feb 09 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.1.12-1
- new upstream release 0.1.12

* Sat Jan 21 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.1.11-1
- initial package
