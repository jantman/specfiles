Name:       nodejs-block-stream
Version:    0.0.6
Release:    4%{?dist}
Summary:    A stream of blocks
License:    BSD
Group:      Development/Libraries
URL:        https://github.com/isaacs/block-stream
Source0:    http://registry.npmjs.org/block-stream/-/block-stream-%{version}.tgz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:  noarch

BuildRequires:  nodejs-devel

%description
Write data into it, and it'll output data in buffer blocks the size you
specify, padding with zeroes if necessary.

%prep
%setup -q -n package

%build
#nothing to do

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{nodejs_sitelib}/block-stream
cp -pr block-stream.js package.json %{buildroot}%{nodejs_sitelib}/block-stream

%nodejs_symlink_deps

# tests disabled until tap is packaged
#%%check
#%%tap test/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{nodejs_sitelib}/block-stream
%doc README.md LICENCE

%changelog
* Thu Jan 17 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.6-4
- correct Licensse tag
- include LICENCE file
- provide a better description

* Tue Jan 08 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.6-3
- add missing build section

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.6-2
- clean up for submission

* Mon Dec 31 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.6-1
- new upstream release 0.0.6

* Fri Apr 27 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.5-2
- guard Requires for F17 automatic depedency generation

* Sat Feb 25 2012 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.5-1
- new upstream release 0.0.5

* Sat Jan 21 2011 T.C. Hollingsworth <tchollingsworth@gmail.com> - 0.0.4-1
- initial package
