
%if 0%{?rhel}
# work around to allow us to find provides/requires with rpm < 4.9,
# which do not understand the magic in /usr/lib/rpm/nodejs.(req|prov)
%global __find_provides %{_rpmconfigdir}/nodejs.prov
%global __find_requires %{_rpmconfigdir}/nodejs.req
%global _use_internal_dependency_generator 0
%endif

Name:       nodejs-read
Version:    1.0.4
Release:    5%{dist}
Summary:    An implementation of read(1) for node programs
License:    BSD
Group:      Development/Libraries
URL:        https://github.com/isaacs/read
Source0:    http://registry.npmjs.org/read/-/read-%{version}.tgz
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
A method for reading user input from stdin in node.js.  Similar to readline's
"question()" method, but with a few more features.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/read
cp -pr lib package.json %{buildroot}%{nodejs_sitelib}/read

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/read
%doc LICENCE README.md example

%changelog
* Thu Feb 07 2013 Jason Antman <Jason.Antman@cmgdigital.com> - 1.0.4-5
- setup to build on CentOS 6 - force __find_provides and __find_requires to the scripts from nodejs/nodejs-devel
- force old external dependency generator, as the fancy logic triggered by /usr/lib/rpm/fileattrs/nodejs.attr isn't recognized by rpm < 4.9.0
- Also build requires nodejs, as the rpm macros and scripts are in that package instead of nodejs-devel.

* Thu Jan 10 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.4-4
- add missing build section

* Mon Jan 07 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.4-2
- fix description
- add no-op build section

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.4-1
- new upstream release 1.0.4
- clean up for submission

* Fri Apr 27 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.2-2
- guard Requires for F17 automatic depedency generation

* Mon Apr 02 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.2-1
- New upstream release 0.0.2

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.1-1
- initial package
