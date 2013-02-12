
%if 0%{?rhel}
# work around to allow us to find provides/requires with rpm < 4.9,
# which do not understand the magic in /usr/lib/rpm/nodejs.(req|prov)
%global __find_provides %{_rpmconfigdir}/nodejs.prov
%global __find_requires %{_rpmconfigdir}/nodejs.req
%global _use_internal_dependency_generator 0
%endif

Name:       nodejs-fstream-ignore
Version:    0.0.5
Release:    5%{?dist}
Summary:    A file stream object that can ignore files by globs
# a copy of the BSD license will be included in the next upstream release
# https://github.com/isaacs/fstream-ignore/commit/f5b9b1d981ff98ce1c92d4eac2b1aa91a142e421
License:    BSD
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/fstream-ignore
Source0:    http://registry.npmjs.org/fstream-ignore/-/fstream-ignore-%{version}.tgz
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
%{summary}.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/fstream-ignore
cp -pr ignore.js package.json %{buildroot}%{nodejs_sitelib}/fstream-ignore

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/fstream-ignore
%doc README.md example

%changelog
* Thu Feb 07 2013 Jason Antman <Jason.Antman@cmgdigital.com> - 0.0.5-5
- setup to build on CentOS 6 - force __find_provides and __find_requires to the scripts from nodejs/nodejs-devel
- force old external dependency generator, as the fancy logic triggered by /usr/lib/rpm/fileattrs/nodejs.attr isn't recognized by rpm < 4.9.0
- Also build requires nodejs, as the rpm macros and scripts are in that package instead of nodejs-devel.

* Tue Jan 22 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.5-4
- fix License tag

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.5-3
- add missing build section
- write better summary

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.5-2
- clean up for submission

* Wed Mar 28 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.5-1
- initial package
