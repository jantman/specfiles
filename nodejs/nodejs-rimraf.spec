Name:       nodejs-rimraf
Version:    2.1.1
Release:    2%{?dist}
Summary:    A deep deletion module for node.js
License:    MIT
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/rimraf
Source0:    http://registry.npmjs.org/rimraf/-/rimraf-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel

%description
%summary (like `rm -rf`).

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/rimraf
cp -pr rimraf.js package.json %{buildroot}%{nodejs_sitelib}/rimraf

%nodejs_symlink_deps

%check
cd test
bash run.sh

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/rimraf
%doc AUTHORS LICENSE README.md

%changelog
* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.1.1-2
- add missing build section

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.1.1-1
- new upstream release 2.1.1
- clean up for submission

* Fri Apr 27 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.0.1-2
- guard Requires for F17 automatic depedency generation

* Thu Feb 09 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 2.0.1-1
- new upstream release 2.0.1

* Tue Oct 25 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.9-1
- new upstream release

* Tue Aug 23 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.3-1
- initial package
