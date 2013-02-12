
%if 0%{?rhel}
# work around to allow us to find provides/requires with rpm < 4.9,
# which do not understand the magic in /usr/lib/rpm/nodejs.(req|prov)
%global __find_provides %{_rpmconfigdir}/nodejs.prov
%global __find_requires %{_rpmconfigdir}/nodejs.req
%global _use_internal_dependency_generator 0
%endif

Name:       nodejs-lru-cache
Version:    2.2.1
Release:    3%{?dist}
Summary:    A least recently used cache object for Node.js
License:    MIT
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/node-lru-cache
Source0:    http://registry.npmjs.org/lru-cache/-/lru-cache-%{version}.tgz
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
A cache object that deletes the least recently used items.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/lru-cache
cp -pr lib package.json %{buildroot}%{nodejs_sitelib}/lru-cache

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/lru-cache
%doc AUTHORS README.md LICENSE

%changelog
* Thu Feb 07 2013 Jason Antman <Jason.Antman@cmgdigital.com> - 2.2.1-3
- setup to build on CentOS 6 - force __find_provides and __find_requires to the scripts from nodejs/nodejs-devel
- force old external dependency generator, as the fancy logic triggered by /usr/lib/rpm/fileattrs/nodejs.attr isn't recognized by rpm < 4.9.0
- Also build requires nodejs, as the rpm macros and scripts are in that package instead of nodejs-devel.

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.1-2
- add missing build section
- improve summary/description

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.1-1
- new upstream release 2.2.1
- clean up for submission

* Fri Apr 27 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.0-2
- fix BuildRequires not present on <F17

* Wed Apr 18 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.0-1
- New upstream release 1.1.0

* Wed Mar 28 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.6-1
- new upstream release 1.0.6

* Sat Feb 25 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.5-1
- new upstream release 1.0.5

* Sun Dec 18 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.4-2
- add Group to make EL5 happy

* Mon Aug 22 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.4-1
- initial package
