Name:           nodejs-tobi-cookie
Version:        0.3.2
Release:        2%{?dist}
Summary:        A cookie handling and cookie jar library for Node.js
BuildArch:      noarch

Group:          System Environment/Libraries
# a copy of the MIT license is included in Readme.md
License:        MIT
URL:            https://github.com/LearnBoost/tobi
Source0:        http://registry.npmjs.org/tobi/-/tobi-%{version}.tgz
Source1:        nodejs-tobi-cookie-package.json
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  nodejs-devel

%description
%summary.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %buildroot

mkdir -p %{buildroot}%{nodejs_sitelib}/tobi-cookie
cp -p lib/cookie/* %{buildroot}%{nodejs_sitelib}/tobi-cookie
install -pm0644 %{SOURCE1} %{buildroot}%{nodejs_sitelib}/tobi-cookie/package.json
sed -i 's/@VERSION@/%{version}/' \
    %{buildroot}%{nodejs_sitelib}/tobi-cookie/package.json

# This tries to work on the full tobi, because it checks the package.json in
# the current working directory.  I'm going to fix it to always use the one in
# the buildroot soon.  We can safely skip it since this package doesn't have
# any dependencies.
#%%nodejs_symlink_deps

%clean
rm -rf %buildroot

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/tobi-cookie
%doc Readme.md History.md

%changelog
* Sat Jan 26 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.2-2
- add missing build section

* Tue Jan 22 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.3.2-1
- initial package
