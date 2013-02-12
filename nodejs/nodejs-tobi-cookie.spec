
%if 0%{?rhel}
# work around to allow us to find provides/requires with rpm < 4.9,
# which do not understand the magic in /usr/lib/rpm/nodejs.(req|prov)
%global __find_provides %{_rpmconfigdir}/nodejs.prov
%global __find_requires %{_rpmconfigdir}/nodejs.req
%global _use_internal_dependency_generator 0
%endif

Name:           nodejs-tobi-cookie
Version:        0.3.2
Release:        3%{?dist}
Summary:        A cookie handling and cookie jar library for Node.js
BuildArch:      noarch

Group:          System Environment/Libraries
# a copy of the MIT license is included in Readme.md
License:        MIT
URL:            https://github.com/LearnBoost/tobi
Source0:        http://registry.npmjs.org/tobi/-/tobi-%{version}.tgz
Source1:        nodejs-tobi-cookie-package.json
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
%summary.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %buildroot

mkdir -p %{buildroot}%{nodejs_sitelib}/tobi-cookie
cp -p lib/cookie/* %{buildroot}%{nodejs_sitelib}/tobi-cookie
install -pm0644 %{SOURCE1} %{buildroot}%{nodejs_sitelib}/tobi-cookie/package.json
sed -i 's/@VERSION@/%{version}/' \
    %{buildroot}%{nodejs_sitelib}/tobi-cookie/package.json

# This tries to work on the full tobi, because it checks the package.json in
# the current working directory.  I'm going to fix it to always use the one in
# the buildroot soon.  We can safely skip it since this package doesn't have
# any dependencies.
#%%nodejs_symlink_deps

%clean
rm -rf %buildroot

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/tobi-cookie
%doc Readme.md History.md

%changelog
* Thu Feb 07 2013 Jason Antman <Jason.Antman@cmgdigital.com> - 0.3.2-3
- setup to build on CentOS 6 - force __find_provides and __find_requires to the scripts from nodejs/nodejs-devel
- force old external dependency generator, as the fancy logic triggered by /usr/lib/rpm/fileattrs/nodejs.attr isn't recognized by rpm < 4.9.0
- Also build requires nodejs, as the rpm macros and scripts are in that package instead of nodejs-devel.

* Sat Jan 26 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.2-2
- add missing build section

* Tue Jan 22 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.2-1
- initial package
