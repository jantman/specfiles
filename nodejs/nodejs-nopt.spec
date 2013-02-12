

%if 0%{?rhel}
# work around to allow us to find provides/requires with rpm < 4.9,
# which do not understand the magic in /usr/lib/rpm/nodejs.(req|prov)
%global __find_provides %{_rpmconfigdir}/nodejs.prov
%global __find_requires %{_rpmconfigdir}/nodejs.req
%global _use_internal_dependency_generator 0
%endif

Name:       nodejs-nopt
Version:    2.0.0
Release:    4%{?dist}
Summary:    Node.js option parsing
License:    MIT
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/nopt
Source0:    http://registry.npmjs.org/nopt/-/nopt-%{version}.tgz
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
An option parsing library for Node.js and its package manager (npm).

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/nopt
cp -pr bin lib package.json %{buildroot}%{nodejs_sitelib}/nopt

mkdir -p %{buildroot}%{_bindir}
ln -sf ../lib/node_modules/nopt/bin/nopt.js %{buildroot}%{_bindir}/nopt

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/nopt
%{_bindir}/nopt
%doc README.md LICENSE examples

%changelog
* Thu Feb 07 2013 Jason Antman <Jason.Antman@cmgdigital.com> - 2.0.0-4
- setup to build on CentOS 6 - force __find_provides and __find_requires to the scripts from nodejs/nodejs-devel
- force old external dependency generator, as the fancy logic triggered by /usr/lib/rpm/fileattrs/nodejs.attr isn't recognized by rpm < 4.9.0
- Also build requires nodejs, as the rpm macros and scripts are in that package instead of nodejs-devel.

* Sun Jan 13 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.0.0-3
- fix symlink to nopt script

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.0.0-2
- add missing build section

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.0.0-1
- new upstream release 2.0.0
- clean up for submission

* Fri Apr 27 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.10-4
- bring in line with newer module packaging standards

* Fri Apr 27 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.10-3
- guard Requires for F17 automatic depedency generation

* Sun Dec 18 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.10-2
- add Group to make EL5 happy

* Tue Oct 25 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> 1.0.10-1
- new upstream release

* Mon Aug 22 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.6-1
- initial package
