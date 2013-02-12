Name:       nodejs-chownr
Version:    0.0.1
Release:    6%{?dist}
Summary:    Changes file permissions recursively
License:    BSD
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/chownr
Source0:    http://registry.npmjs.org/chownr/-/chownr-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel

%description
Changes file permissions recursively, like `chown -R`.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/chownr
cp -p chownr.js package.json %{buildroot}%{nodejs_sitelib}/chownr

%nodejs_symlink_deps

#%%check
#%%tap test/*.js

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/chownr
%doc README.md LICENCE

%changelog
* Tue Jan 15 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.1-6
- rebuild with fresh tarball from upstream
- ship newly included LICENCE file

* Mon Jan 14 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.1-5
- correct license information

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.1-4
- add missing build section
- fix summary and description

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.1-3
- clean up for submission

* Fri Apr 27 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.1-2
- fix BuildRequires not present on <F17

* Thu Mar 29 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.1-1
- initial package
