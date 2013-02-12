
%if 0%{?rhel}
# work around to allow us to find provides/requires with rpm < 4.9,
# which do not understand the magic in /usr/lib/rpm/nodejs.(req|prov)
%global __find_provides %{_rpmconfigdir}/nodejs.prov
%global __find_requires %{_rpmconfigdir}/nodejs.req
%global _use_internal_dependency_generator 0
%endif

Name:       nodejs-glob
Version:    3.1.14
Release:    3%{?dist}
Summary:    A little globber for Node.js
License:    BSD
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/node-glob
Source0:    http://registry.npmjs.org/glob/-/glob-%{version}.tgz
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
This is a glob implementation in pure JavaScript. It uses the minimatch library
to do its matching.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/glob
cp -pr glob.js package.json %{buildroot}%{nodejs_sitelib}/glob

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/glob
%doc LICENSE README.md examples

%changelog
* Thu Feb 07 2013 Jason Antman <Jason.Antman@cmgdigital.com> - 3.1.14-3
- setup to build on CentOS 6 - force __find_provides and __find_requires to the scripts from nodejs/nodejs-devel
- force old external dependency generator, as the fancy logic triggered by /usr/lib/rpm/fileattrs/nodejs.attr isn't recognized by rpm < 4.9.0
- Also build requires nodejs, as the rpm macros and scripts are in that package instead of nodejs-devel.

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 3.1.14-2
- add missing build section
- adjust summary/description slightly

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 3.1.14-1
- new upstream release 3.1.14
- clean up for submission

* Thu Mar 22 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 3.1.9-1
- new upstream release 3.1.9

* Fri Mar 16 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 3.1.6-1
- initial package
