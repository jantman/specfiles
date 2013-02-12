Name:       nodejs-fstream-npm
Version:    0.1.3
Release:    2%{?dist}
Summary:    An fstream class for creating npm packages
License:    BSD
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/fstream-npm
Source0:    http://registry.npmjs.org/fstream-npm/-/fstream-npm-%{version}.tgz
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

mkdir -p %{buildroot}%{nodejs_sitelib}/fstream-npm
cp -pr fstream-npm.js package.json %{buildroot}%{nodejs_sitelib}/fstream-npm

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/fstream-npm
%doc README.md example LICENCE

%changelog
* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.1.3-2
- add missing build section

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.1.3-1
- new upstream release 0.1.3
- clean up for submission

* Wed Apr 18 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.6-1
- New upstream release 0.0.6

* Wed Mar 28 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.4-1
- initial package
