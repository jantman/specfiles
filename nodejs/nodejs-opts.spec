Name:       nodejs-opts
Version:    1.2.2
Release:    2%{?dist}
Summary:    Javascript Command Line Options for Node.js
License:    BSD
Group:      System Environment/Libraries
URL:        http://joey.mazzarelli.com/2010/04/09/javascript-command-line-options-for-node-js/
Source0:    http://registry.npmjs.org/opts/-/opts-1.2.2.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel

%description
js-opts is a library for parsing command line options in javascript.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/opts
cp -pr js package.json %{buildroot}%{nodejs_sitelib}/opts

%nodejs_symlink_deps

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/opts
%doc LICENSE README examples

%changelog
* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.2-2
- add missing build section

* Sun Mar 04 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.2-1
- new upstream release 1.2.2
- clean up for submission

* Sun Dec 18 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.1-2
- add Group to make EL5 happy

* Thu Nov 17 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 1.2.1-1
- initial package
