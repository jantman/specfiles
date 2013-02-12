
%if 0%{?rhel}
# work around to allow us to find provides/requires with rpm < 4.9,
# which do not understand the magic in /usr/lib/rpm/nodejs.(req|prov)
%global __find_provides %{_rpmconfigdir}/nodejs.prov
%global __find_requires %{_rpmconfigdir}/nodejs.req
%global _use_internal_dependency_generator 0
%endif

Name:       nodejs-request
Version:    2.12.0
Release:    6%{?dist}
Summary:    Simplified HTTP request client
License:    ASL 2.0
Group:      Development/Libraries
URL:        https://github.com/mikeal/request
Source0:    http://registry.npmjs.org/request/-/request-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

# use the seperate cookie module instead of the bundled version
Patch1: nodejs-request-unbundle-cookie.patch

BuildRequires:  nodejs-devel

%if 0%{?rhel}
# this will ONLY build with the macros, scripts, etc. from redhat-rpm-config
BuildRequires: redhat-rpm-config
BuildRequires: /usr/bin/python

# CentOS 6.x and lower use rpm < 4.9, so they don't understand the fancy new automatic
# dependency generation for scripting languages
Requires: /bin/sh /bin/bash /usr/bin/env
%endif

# explicit Requires are required because this package is not listed in the npm
# registry and thus not handled by the automatic dependency generator
Requires:   nodejs-tobi-cookie

%description
Request is designed to be the simplest way possible to make HTTP calls. It
supports HTTPS and follows redirects by default.

You can stream any response to a file stream. You can also stream a file to a
PUT or POST request.  It also supports a few simple server and proxy functions.

%prep
%setup -q -n package
%patch1

#remove bundled modules
rm -rf node_modules vendor

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/request
cp -pr *.js package.json %{buildroot}%{nodejs_sitelib}/request

%nodejs_symlink_deps
#we manually create this dependency link since tobi-cookie isn't in the npm registry
ln -sf %{nodejs_sitelib}/tobi-cookie \
    %{buildroot}%{nodejs_sitelib}/request/node_modules/tobi-cookie

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/request
%doc README.md LICENSE

%changelog
* Thu Feb 07 2013 Jason Antman <Jason.Antman@cmgdigital.com> - 2.12.0-6
- setup to build on CentOS 6 - force __find_provides and __find_requires to the scripts from nodejs/nodejs-devel
- force old external dependency generator, as the fancy logic triggered by /usr/lib/rpm/fileattrs/nodejs.attr isn't recognized by rpm < 4.9.0
- Also build requires nodejs, as the rpm macros and scripts are in that package instead of nodejs-devel.

* Tue Jan 29 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.12.0-5
- actually make patch work
- fix typo

* Mon Jan 28 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.12.0-4
- actually apply patch
- manually create dependency link to private module tobi-cookie

* Thu Jan 24 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.12.0-3
- unbundle cookie stuff

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.12.0-2
- add missing build section
- improve description

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.12.0-1
- new upstream release 2.12.0
- clean up for submission

* Wed Apr 18 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.9.202-1
- New upstream release 2.9.202

* Sun Mar 04 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.9.153-1
- new upstream release 2.9.153

* Sat Feb 25 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.9.151-1
- new upstream release 2.9.151

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.9.100-1
- new upstream release 2.9.100

* Thu Dec 22 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.9-1
- new upstream release 2.2.9

* Mon Nov 07 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.2.0-1
- new upstream release 2.2.0
- adds node v0.6 support

* Tue Oct 25 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.0-2.20110928.646c80dgit
- npm needs a newer git snapshot (apparently upstream moved to rolling release anyway)

* Tue Oct 25 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.0-1
- initial package
