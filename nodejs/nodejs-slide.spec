
%if 0%{?rhel}
# work around to allow us to find provides/requires with rpm < 4.9,
# which do not understand the magic in /usr/lib/rpm/nodejs.(req|prov)
%global __find_provides %{_rpmconfigdir}/nodejs.prov
%global __find_requires %{_rpmconfigdir}/nodejs.req
%global _use_internal_dependency_generator 0
%endif

Name:       nodejs-slide
Version:    1.1.3
Release:    5%{?dist}
Summary:    A flow control library that fits in a slideshow
# license present in source control, will be added to future release
# https://raw.github.com/isaacs/slide-flow-control/master/LICENSE
License:    MIT
URL:        https://github.com/isaacs/slide-flow-control
Source0:    http://registry.npmjs.org/slide/-/slide-%{version}.tgz
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
Provides simple, easy callbacks for node.js.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/slide
cp -pr lib package.json %{buildroot}%{nodejs_sitelib}/slide

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/slide
%doc README.md nodejs-controlling-flow.pdf

%changelog
* Thu Feb 07 2013 Jason Antman <Jason.Antman@cmgdigital.com>
- setup to build on CentOS 6 - force __find_provides and __find_requires to the scripts from nodejs/nodejs-devel
- force old external dependency generator, as the fancy logic triggered by /usr/lib/rpm/fileattrs/nodejs.attr isn't recognized by rpm < 4.9.0
- Also build requires nodejs, as the rpm macros and scripts are in that package instead of nodejs-devel.

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.3-4
- add missing build section
- mention missing license

* Thu Apr 26 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.3-3
- missing package.json

* Thu Apr 26 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.3-2
- bring into conformance with newer library packaging standards
- guard Requires for F17 automatic dependency generation

* Mon Aug 22 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.3-1
- initial package
