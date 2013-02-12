Name:       nodejs-glob
Version:    3.1.14
Release:    2%{?dist}
Summary:    A little globber for Node.js
License:    BSD
Group:      System Environment/Libraries
URL:        https://github.com/isaacs/node-glob
Source0:    http://registry.npmjs.org/glob/-/glob-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel

%description
This is a glob implementation in pure JavaScript. It uses the minimatch library
to do its matching.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/glob
cp -pr glob.js package.json %{buildroot}%{nodejs_sitelib}/glob

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/glob
%doc LICENSE README.md examples

%changelog
* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 3.1.14-2
- add missing build section
- adjust summary/description slightly

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 3.1.14-1
- new upstream release 3.1.14
- clean up for submission

* Thu Mar 22 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 3.1.9-1
- new upstream release 3.1.9

* Fri Mar 16 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 3.1.6-1
- initial package
