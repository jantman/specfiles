Name:       nodejs-abbrev
Version:    1.0.4
Release:    2%{?dist}
Group:      Development/Libraries
Summary:    Abbreviation calculator for Node.js
License:    MIT
URL:        https://github.com/isaacs/abbrev-js
Source0:    http://registry.npmjs.org/abbrev/-/abbrev-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel

%description
Calculate the set of unique abbreviations for a given set of strings.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/abbrev
cp -pr lib package.json %{buildroot}%{nodejs_sitelib}/abbrev

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/abbrev
%doc README.md LICENSE

%changelog
* Sun Jan 13 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.4-2
- fix missing dist macro in Release

* Thu Jan 10 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.4-1
- new upstream release 1.0.4
- include newly added LICENSE file

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.3-5
- add missing build section

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.3-4
- clean up for submission

* Fri Apr 27 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.3-3
- guard Requires for F17 automatic depedency generation

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.3-2
- missing Group field for EL5

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.3-1
- new upstream release 1.0.3

* Mon Aug 22 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.2-1
- initial package
