#
# Copyright (c) 2017-2018, Quentin Schwerkolt
# All rights reserved.
#

Summary:	This is tcllauncher, a launcher program for Tcl applications.
Name:		tcllauncher
Version:	1.8
Release:	1%{?dist}
URL:		https://github.com/flightaware/tcllauncher
License:	MIT
BuildRequires:	autoconf automake libtool
BuildRequires:	tcl-devel
Requires:	tclx
Source0:	https://github.com/flightaware/tcllauncher/archive/v%{version}.tar.gz#/tcllauncher-%{version}.tar.gz

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitelib: %global tcl_sitelib %{_datadir}/tcl%{tcl_version}}

%description
%{Summary}

%prep
%setup

%build
autoreconf -vif
%configure --libdir=%{tcl_sitelib}
%make_build

%install
%make_install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%license license.terms
%doc ChangeLog README.md
%{_bindir}/tcllauncher
%{tcl_sitelib}/Tcllauncher%{version}/*
%{_mandir}/mann/tcllauncher.n.gz

%changelog
* Wed Dec 26 2018 Quentin Schwerkolt
- Update to 1.8

* Fri Jan 27 2017 Quentin Schwerkolt
- Initial Version
