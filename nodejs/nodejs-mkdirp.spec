Name:       nodejs-mkdirp
Version:    0.3.4
Release:    2%{?dist}
Summary:    Recursive directory creation module for Node.js
License:    MIT
Group:      Development/Libraries
URL:        https://github.com/substack/node-mkdirp
Source0:    http://registry.npmjs.org/mkdirp/-/mkdirp-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel

%description
Creates directories recursively, like `mkdir -p`.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/mkdirp
cp -pr index.js package.json %{buildroot}%{nodejs_sitelib}/mkdirp

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/mkdirp
%doc README.markdown examples LICENSE

%changelog
* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.4-2
- add missing build section
- improve summary/description

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.4-1
- new upstream release 0.3.4
- clean up for submission

* Wed May 02 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.2-1
- New upstream release 0.3.2

* Fri Apr 27 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.1-2
- guard Requires for F17 automatic depedency generation

* Mon Apr 02 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.1-1
- New upstream release 0.3.1

* Sat Jan 21 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.0-1
- new upstream release 0.3.0

* Thu Dec 22 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.2.1-1
- initial package
