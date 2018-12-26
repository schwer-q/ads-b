#
# Copyright (c) 2017-2018, Quentin Schwerkolt
# All rights reserved.
#

Summary:	Mode S multilateration client
Name:		mlat-client
Version:	0.2.10
Release:	1%{?dist}
URL:		https://github.com/mutability/mlat-client
License:	GPLv3+
BuildRequires:	python3-devel
Requires:	dump1090-fa
Requires:	python3
Group:		Application/Communications
Source0:	https://github.com/mutability/mlat-client/archive/v%{version}.tar.gz#/mlat-client-%{version}.tar.gz

%description
%{Summary}

%prep
%setup -n %{name}-%{version}

%build
%py3_build

%install
%py3_install

install -D -p -m 0755 %{buildroot}/%{_bindir}/fa-mlat-client %{buildroot}/%{_libexecdir}/fa-mlat-client
rm %{buildroot}/%{_bindir}/fa-mlat-client
install -D -p -m 0644 debian/mlat-client.logrotate %{buildroot}/%{_sysconfdir}/logrotate.d/mlat-client

%files
%defattr(-,root,root,-)
%{_bindir}/mlat-client
%{python3_sitearch}/*
%{_libexecdir}/fa-mlat-client
%{_sysconfdir}/logrotate.d/mlat-client

%changelog
* Wed Dec 26 2018 Quentin Schwerkolt
- update to 0.2.10
