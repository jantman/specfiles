Name:       nodejs-graceful-fs
Version:    1.1.14
Release:    2%{?dist}
Summary:    'fs' module with incremental back-off on EMFILE
License:    MIT
Group:      Development/Libraries
URL:        https://github.com/isaacs/node-graceful-fs
Source0:    http://registry.npmjs.org/graceful-fs/-/graceful-fs-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel

%description
Just like node.js' fs module, but it does an incremental back-off when EMFILE is
encountered.  Useful in asynchronous situations where one needs to try to open
lots and lots of files.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/graceful-fs
cp -p graceful-fs.js package.json %{buildroot}%{nodejs_sitelib}/graceful-fs

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/graceful-fs
%doc README.md LICENSE

%changelog
* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.14-2
- add missing build section

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.14-1
- new upstream release 1.1.14
- clean up for submission

* Fri Apr 27 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.8-2
- guard Requires for F17 automatic depedency generation

* Thu Mar 22 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.8-1
- new upstream release 1.1.8

* Sun Jan 29 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.5-1
- new upstream release 1.1.5

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.4-2
- missing Group field for EL5

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.1.4-1
- new upstream release 1.1.4

* Thu Nov 10 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.2-0.1.20111109git33dee97
- new upstream release
- Node v0.6.0 compatibility fixes

* Tue Oct 25 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.1-1
- new upstream release

* Mon Aug 22 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.0.0-1
- initial package
