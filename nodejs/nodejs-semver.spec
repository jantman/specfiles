Name:       nodejs-semver
Version:    1.1.2
Release:    1%{?dist}
Summary:    Semantic versioner for npm
License:    MIT
Group:      Development/Libraries
URL:        https://github.com/isaacs/node-semver
Source0:    http://registry.npmjs.org/semver/-/semver-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel

%description
The semantic version comparison library for the Node.js package manager (npm).

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/semver
cp -pr bin package.json semver.js %{buildroot}%{nodejs_sitelib}/semver

mkdir -p %{buildroot}%{_bindir}
ln -sf ../lib/node_modules/semver/bin/semver %{buildroot}%{_bindir}

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/semver
%{_bindir}/semver
%doc README.md LICENSE

%changelog
* Thu Jan 10 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.2-1
- new upstream release 1.1.2

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.1-2
- add missing build section

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.1-1
- new upstream release 1.1.1
- clean up for submission

* Fri Apr 27 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.13-3
- guard Requires for F17 automatic depedency generation

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.13-2
- missing Group field for EL5

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.13-1
- new upstream release 1.0.13

* Thu Nov 17 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.11-1
- new upstream release 1.0.11

* Tue Oct 25 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.10-1
- new upstream release

* Mon Aug 22 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.9-1
- initial package
