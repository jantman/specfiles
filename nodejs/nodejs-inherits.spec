Name:       nodejs-inherits
Version:    1.0.0
Release:    6%{?dist}
Summary:    A tiny simple way to do classic inheritance in js
License:    WTFPL
Group:      Development/Libraries
URL:        https://github.com/isaacs/inherits
Source0:    http://registry.npmjs.org/inherits/-/inherits-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel

%description
%{summary}.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/inherits
cp -pr inherits.js package.json %{buildroot}%{nodejs_sitelib}/inherits

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/inherits
%doc README.md

%changelog
* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.0-6
- add missing build section

* Thu Jan 03 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.0-5
- correct license tag (thanks to Robin Lee)

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.0-4
- clean up for submission

* Fri Apr 27 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.0-3
- guard Requires for F17 automatic depedency generation

* Sat Feb 11 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.0-2
- switch to automatically generated provides/requires

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.0-1
- initial package
