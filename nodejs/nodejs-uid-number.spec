Name:       nodejs-uid-number
Version:    0.0.3
Release:    4%{?dist}
Summary:    Convert a username/group name to a UID/GID number
License:    BSD
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/uid-number
Source0:    http://registry.npmjs.org/uid-number/-/uid-number-%{version}.tgz
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

mkdir -p %{buildroot}%{nodejs_sitelib}/uid-number
cp -pr *.js package.json %{buildroot}%{nodejs_sitelib}/uid-number

chmod 0644 %{buildroot}%{nodejs_sitelib}/uid-number/get-uid-gid.js

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/uid-number
%doc README.md LICENCE

%changelog
* Fri Jan 11 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.3-4
- really use a fresh tarball from upstream
- fix permissions
- include LICENCE file

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.3-3
- add missing build section
- rebuild with fresh tarball from upstream

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.3-2
- Clean up for submission

* Wed Mar 28 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.3-1
- initial package
