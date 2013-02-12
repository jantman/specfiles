
%if 0%{?rhel}
# work around to allow us to find provides/requires with rpm < 4.9,
# which do not understand the magic in /usr/lib/rpm/nodejs.(req|prov)
%global __find_provides %{_rpmconfigdir}/nodejs.prov
%global __find_requires %{_rpmconfigdir}/nodejs.req
%global _use_internal_dependency_generator 0
%endif

Name:           nodejs-osenv
Version:        0.0.3
Release:        3%{?dist}
Summary:        Look up environment settings specific to different operating systems
BuildArch:      noarch

Group:          System Environment/Libraries
License:        BSD
URL:            https://github.com/isaacs/osenv
Source0:        http://registry.npmjs.org/osenv/-/osenv-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

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
Look up environment settings specific to different operating systems.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %buildroot
mkdir -p %{buildroot}%{nodejs_sitelib}/osenv
cp -pr package.json osenv.js %{buildroot}%{nodejs_sitelib}/osenv

%nodejs_symlink_deps

%clean
rm -rf %buildroot

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/osenv
%doc LICENSE README.md

%changelog
* Thu Feb 07 2013 Jason Antman <Jason.Antman@cmgdigital.com> - 0.0.3-3
- setup to build on CentOS 6 - force __find_provides and __find_requires to the scripts from nodejs/nodejs-devel
- force old external dependency generator, as the fancy logic triggered by /usr/lib/rpm/fileattrs/nodejs.attr isn't recognized by rpm < 4.9.0
- Also build requires nodejs, as the rpm macros and scripts are in that package instead of nodejs-devel.

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.3-2
- add missing build section

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.3-1
- initial package generated by npm2rpm
