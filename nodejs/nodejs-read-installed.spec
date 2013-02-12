Name:           nodejs-read-installed
Version:        0.0.4
Release:        2%{?dist}
Summary:        Returns a tree structure of all installed packages in a folder
BuildArch:      noarch

Group:          System Environment/Libraries
License:        BSD
URL:            https://github.com/isaacs/read-installed
Source0:        http://registry.npmjs.org/read-installed/-/read-installed-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  nodejs-devel

%description
Reads all the installed packages in a folder, and returns a tree structure with
all the data.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %buildroot
mkdir -p %{buildroot}%{nodejs_sitelib}/read-installed
cp -pr package.json read-installed.js %{buildroot}%{nodejs_sitelib}/read-installed

%nodejs_symlink_deps

%clean
rm -rf %buildroot

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/read-installed
%doc LICENSE README.md

%changelog
* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.4-2
- add missing build section
- fix URL

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.4-1
- initial package generated by npm2rpm
