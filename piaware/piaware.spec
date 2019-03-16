#
# Copyright (c) 2018-2019, Quentin Schwerkolt
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define debug_package	%{nil}

Summary:	Decode ADS-B airplane beacon traffic with an RTL-SDR dongle
Name:		piaware
Version:	3.6.3
Release:	1%{?dist}
URL:		https://github.com/flightaware/piaware
License:	BSD
BuildRequires:	tcl-devel
BuildRequires:	openssl-perl
BuildRequires:	systemd
BuildRequires:	tcllauncher
Requires:	dump1090-fa
Requires:	itcl
Requires:	mlat-client
Requires:	netstat-monitor
Requires:	tcl
Requires:	tcllauncher
Requires:	tcllib
Requires:	tcltls
Group:		Applications/Communications
Source0:	https://github.com/flightaware/piaware/archive/v%{version}.tar.gz#/piaware-%{version}.tar.gz
Source1:	piaware.conf
Source2:	piaware.logrotate
Patch0:		piaware-faup1090.patch
Patch2:		piaware-mlat.patch

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitelib: %global tcl_sitelib %{_datadir}/tcl%{tcl_version}}

%description
%{Summary}

%prep
%setup -n %{name}-%{version}
sed -i -e 's/install -m 0755 $(TCLLAUNCHER)/ln -s tcllauncher/g' programs/*/Makefile
%patch0 -p1
%patch2 -p1

%build
exit 0

%install
%make_install

install -d %{buildroot}/%{tcl_sitelib}
mv %{buildroot}/%{_prefix}/lib/fa_adept_codec %{buildroot}/%{tcl_sitelib}
mv %{buildroot}/%{_prefix}/lib/piaware_packages %{buildroot}/%{tcl_sitelib}

install -D -p -m 0644 scripts/piaware.service %{buildroot}/%{_unitdir}/piaware.service
install -D -p -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/piaware.conf
install -D -p -m 0644 %{SOURCE2} %{buildroot}/%{_sysconfdir}/logrotate.d/piaware
touch %{buildroot}/%{_sysconfdir}/piaware.conf

%pre
/usr/sbin/useradd -s /sbin/nologin -M -r -d %{_datadir}/piaware \
		  -c 'piaware user' piaware &> /dev/null || :
exit 0

%post
%systemd_post piaware.service

%preun
%systemd_preun piaware.service

%postun
%systemd_postun_with_restart piaware.service

%files
%defattr(-,root,root,-)
%license LICENSE.txt
%doc README.md
%{_bindir}/piaware
%{_bindir}/piaware-config
%{_bindir}/piaware-status
%{_bindir}/pirehose
%{_prefix}/lib/piaware-config/*
%{_prefix}/lib/piaware-status/*
%{_prefix}/lib/piaware/*
%{_prefix}/lib/pirehose/*
%config(noreplace) %attr(0640,root,piaware) %{_sysconfdir}/piaware.conf
%{_sysconfdir}/logrotate.d/piaware
%{_unitdir}/piaware.service
%{tcl_sitelib}/fa_adept_codec/*
%{tcl_sitelib}/piaware_packages/*
%{_mandir}/man1/*

%changelog
* Wed Dec 26 2018 Quentin Schwerkolt
- Update to 3.6.3

* Fri Apr 7 2017 Quentin Schwerkolt
- Update to 3.5.0

* Sat Jan 21 2017 Quentin Schwerkolt
- Initial Version
