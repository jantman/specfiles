Name:       nodejs-minimatch
Version:    0.2.9
Release:    2%{?dist}
Summary:    JavaScript glob matcher
License:    MIT
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/minimatch
Source0:    http://registry.npmjs.org/minimatch/-/minimatch-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel

%description
Converts glob expressions to JavaScript "RegExp" objects.

%prep
%setup -q -n package

%nodejs_fixdep lru-cache

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/minimatch
cp -p minimatch.js package.json %{buildroot}%{nodejs_sitelib}/minimatch

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/minimatch
%doc README.md LICENSE

%changelog
* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.2.9-2
- add missing build section

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.2.9-1
- new upstream release 0.2.9
- clean up for submission

* Fri Apr 27 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.2.4-2
- guard Requires for F17 automatic depedency generation

* Thu Mar 29 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.2.4-1
- New upstream release 0.2.4

* Thu Mar 29 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.2.2-2
- New upstream release 0.2.4

* Thu Mar 22 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.2.2-1
- new upstream release 0.2.2

* Sat Feb 25 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.2.0-1
- new upstream release 0.2.0

* Sun Dec 18 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.4-2
- add Group to make EL5 happy

* Mon Aug 22 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.4-1
- initial package
