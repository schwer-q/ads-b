#
# Copyright (c) 2017-2019, Quentin Schwerkolt
# All rights reserved.
#
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

Summary:	Decode ADS-B airplane beacon traffic with an RTL-SDR dongle
Name:		dump1090-fa
Version:	3.6.3
Release:	1%{?dist}
URL:		https://github.com/flightaware/dump1090
License:	GPLv2+
BuildRequires:	libbladeRF-devel
BuildRequires:	libusbx-devel
BuildRequires:	ncurses-devel
BuildRequires:	rtl-sdr-devel
BuildRequires:	systemd
Requires(pre):	shadow-utils
Requires:	lighttpd
Group:		Applications/Communications
Source0:	https://github.com/flightaware/dump1090/archive/v%{version}.tar.gz#/dump1090-fa-%{version}.tar.gz
Source1:	dump1090-fa.default
Source2:	dump1090-fa.service

%description
ADS-B Ground Station System for RTL-SDR
Networked Aviation Mode S / ADS-B decoder/translator with RTL-SDR software
defined radio USB device support.

This is FlightAware\'s packaging of dump1090-mutability, customized for use
in the PiAware sdcard images.

%prep
%setup -q -n dump1090-%{version}
# Prevent a build failure due to incompatible pointer type
sed -i 's/-Werror//' Makefile

%build
%make_build HTMLPATH=/usr/share/%{name}/html DUMP1090_VERSION=%{version} RTLSDR_PREFIX=/usr
#%make_build RTLSDR=no BLADERF=no DUMP1090_VERSION="piaware-%{version}" faup1090
%make_build DUMP1090_VERSION="piaware-%{version}" faup1090

%install
install -D -p -m 0755 dump1090 %{buildroot}/%{_bindir}/dump1090-fa
install -D -p -m 0755 view1090 %{buildroot}/%{_bindir}/view1090-fa
install -D -p -m 0755 faup1090 %{buildroot}/%{_libexecdir}/faup1090

install -D -p -m 0644 %{SOURCE1} %{buildroot}/%{_sysconfdir}/default/dump1090-fa

install -D -p -m 0644 %{SOURCE2} %{buildroot}/%{_unitdir}/dump1090-fa.service

install -d %{buildroot}/%{_datadir}/%{name}/html
cp -a public_html/* %{buildroot}/%{_datadir}/%{name}/html

install -d %{buildroot}/%{_sysconfdir}/lighttpd/conf.d
cp -a debian/lighttpd/* %{buildroot}/%{_sysconfdir}/lighttpd/conf.d

%clean
rm -rf %{buildroot}

%pre
/usr/sbin/useradd -s /sbin/nologin -M -r -d %{_datarootdir}/%{name} \
                  -c 'flightaware dump1090 user' dump1090 &> /dev/null || :
exit 0

%post
%systemd_post dump1090-fa.service

%preun
%systemd_preun dump1090-fa.service

%postun
%systemd_postun_with_restart dump1090-fa.service

%files
%defattr(-,root,root,-)
%doc README.md README-json.md debian/changelog debian/README.librtlsdr
%license COPYING
%{_bindir}/dump1090-fa
%{_bindir}/view1090-fa
%{_libexecdir}/faup1090
%{_sysconfdir}/default/dump1090-fa
%{_sysconfdir}/lighttpd/conf.d/*
%{_unitdir}/dump1090-fa.service
%config(noreplace) %{_datarootdir}/%{name}/html/config.js
%{_datarootdir}/%{name}/html/db/0.json
%{_datarootdir}/%{name}/html/db/1.json
%{_datarootdir}/%{name}/html/db/2.json
%{_datarootdir}/%{name}/html/db/3.json
%{_datarootdir}/%{name}/html/db/39.json
%{_datarootdir}/%{name}/html/db/3C.json
%{_datarootdir}/%{name}/html/db/3C0.json
%{_datarootdir}/%{name}/html/db/3C01.json
%{_datarootdir}/%{name}/html/db/3C0A.json
%{_datarootdir}/%{name}/html/db/3C0B.json
%{_datarootdir}/%{name}/html/db/3C0C.json
%{_datarootdir}/%{name}/html/db/3C0D.json
%{_datarootdir}/%{name}/html/db/3C0E.json
%{_datarootdir}/%{name}/html/db/3C0F.json
%{_datarootdir}/%{name}/html/db/3C1.json
%{_datarootdir}/%{name}/html/db/3C16.json
%{_datarootdir}/%{name}/html/db/3C1A.json
%{_datarootdir}/%{name}/html/db/3C1B.json
%{_datarootdir}/%{name}/html/db/3C1C.json
%{_datarootdir}/%{name}/html/db/3C2.json
%{_datarootdir}/%{name}/html/db/3C29.json
%{_datarootdir}/%{name}/html/db/3C2A.json
%{_datarootdir}/%{name}/html/db/3C2B.json
%{_datarootdir}/%{name}/html/db/3C2C.json
%{_datarootdir}/%{name}/html/db/3C2D.json
%{_datarootdir}/%{name}/html/db/3C2E.json
%{_datarootdir}/%{name}/html/db/3C2F.json
%{_datarootdir}/%{name}/html/db/3C3.json
%{_datarootdir}/%{name}/html/db/3C38.json
%{_datarootdir}/%{name}/html/db/3C3A.json
%{_datarootdir}/%{name}/html/db/3C3B.json
%{_datarootdir}/%{name}/html/db/3C3C.json
%{_datarootdir}/%{name}/html/db/4.json
%{_datarootdir}/%{name}/html/db/40.json
%{_datarootdir}/%{name}/html/db/400.json
%{_datarootdir}/%{name}/html/db/406.json
%{_datarootdir}/%{name}/html/db/42.json
%{_datarootdir}/%{name}/html/db/43.json
%{_datarootdir}/%{name}/html/db/44.json
%{_datarootdir}/%{name}/html/db/48.json
%{_datarootdir}/%{name}/html/db/484.json
%{_datarootdir}/%{name}/html/db/4B.json
%{_datarootdir}/%{name}/html/db/4C.json
%{_datarootdir}/%{name}/html/db/5.json
%{_datarootdir}/%{name}/html/db/6.json
%{_datarootdir}/%{name}/html/db/7.json
%{_datarootdir}/%{name}/html/db/8.json
%{_datarootdir}/%{name}/html/db/9.json
%{_datarootdir}/%{name}/html/db/A.json
%{_datarootdir}/%{name}/html/db/A0.json
%{_datarootdir}/%{name}/html/db/A00.json
%{_datarootdir}/%{name}/html/db/A000.json
%{_datarootdir}/%{name}/html/db/A002.json
%{_datarootdir}/%{name}/html/db/A008.json
%{_datarootdir}/%{name}/html/db/A00B.json
%{_datarootdir}/%{name}/html/db/A01.json
%{_datarootdir}/%{name}/html/db/A016.json
%{_datarootdir}/%{name}/html/db/A01A.json
%{_datarootdir}/%{name}/html/db/A02.json
%{_datarootdir}/%{name}/html/db/A02A.json
%{_datarootdir}/%{name}/html/db/A02B.json
%{_datarootdir}/%{name}/html/db/A03.json
%{_datarootdir}/%{name}/html/db/A030.json
%{_datarootdir}/%{name}/html/db/A03E.json
%{_datarootdir}/%{name}/html/db/A04.json
%{_datarootdir}/%{name}/html/db/A049.json
%{_datarootdir}/%{name}/html/db/A05.json
%{_datarootdir}/%{name}/html/db/A050.json
%{_datarootdir}/%{name}/html/db/A052.json
%{_datarootdir}/%{name}/html/db/A06.json
%{_datarootdir}/%{name}/html/db/A07.json
%{_datarootdir}/%{name}/html/db/A08.json
%{_datarootdir}/%{name}/html/db/A09.json
%{_datarootdir}/%{name}/html/db/A0A.json
%{_datarootdir}/%{name}/html/db/A0B.json
%{_datarootdir}/%{name}/html/db/A0C.json
%{_datarootdir}/%{name}/html/db/A0D.json
%{_datarootdir}/%{name}/html/db/A0F.json
%{_datarootdir}/%{name}/html/db/A1.json
%{_datarootdir}/%{name}/html/db/A11.json
%{_datarootdir}/%{name}/html/db/A12.json
%{_datarootdir}/%{name}/html/db/A13.json
%{_datarootdir}/%{name}/html/db/A14.json
%{_datarootdir}/%{name}/html/db/A15.json
%{_datarootdir}/%{name}/html/db/A16.json
%{_datarootdir}/%{name}/html/db/A17.json
%{_datarootdir}/%{name}/html/db/A18.json
%{_datarootdir}/%{name}/html/db/A19.json
%{_datarootdir}/%{name}/html/db/A195.json
%{_datarootdir}/%{name}/html/db/A198.json
%{_datarootdir}/%{name}/html/db/A19C.json
%{_datarootdir}/%{name}/html/db/A1A.json
%{_datarootdir}/%{name}/html/db/A1A7.json
%{_datarootdir}/%{name}/html/db/A1AB.json
%{_datarootdir}/%{name}/html/db/A1B.json
%{_datarootdir}/%{name}/html/db/A1B6.json
%{_datarootdir}/%{name}/html/db/A1BC.json
%{_datarootdir}/%{name}/html/db/A1C.json
%{_datarootdir}/%{name}/html/db/A1CB.json
%{_datarootdir}/%{name}/html/db/A1D.json
%{_datarootdir}/%{name}/html/db/A1DE.json
%{_datarootdir}/%{name}/html/db/A1E.json
%{_datarootdir}/%{name}/html/db/A1EB.json
%{_datarootdir}/%{name}/html/db/A1EF.json
%{_datarootdir}/%{name}/html/db/A1F.json
%{_datarootdir}/%{name}/html/db/A2.json
%{_datarootdir}/%{name}/html/db/A20.json
%{_datarootdir}/%{name}/html/db/A21.json
%{_datarootdir}/%{name}/html/db/A22.json
%{_datarootdir}/%{name}/html/db/A23.json
%{_datarootdir}/%{name}/html/db/A24.json
%{_datarootdir}/%{name}/html/db/A25.json
%{_datarootdir}/%{name}/html/db/A26.json
%{_datarootdir}/%{name}/html/db/A27.json
%{_datarootdir}/%{name}/html/db/A28.json
%{_datarootdir}/%{name}/html/db/A29.json
%{_datarootdir}/%{name}/html/db/A2A.json
%{_datarootdir}/%{name}/html/db/A2C.json
%{_datarootdir}/%{name}/html/db/A2D.json
%{_datarootdir}/%{name}/html/db/A2E.json
%{_datarootdir}/%{name}/html/db/A2F.json
%{_datarootdir}/%{name}/html/db/A3.json
%{_datarootdir}/%{name}/html/db/A30.json
%{_datarootdir}/%{name}/html/db/A31.json
%{_datarootdir}/%{name}/html/db/A32.json
%{_datarootdir}/%{name}/html/db/A32D.json
%{_datarootdir}/%{name}/html/db/A33.json
%{_datarootdir}/%{name}/html/db/A34.json
%{_datarootdir}/%{name}/html/db/A34D.json
%{_datarootdir}/%{name}/html/db/A35.json
%{_datarootdir}/%{name}/html/db/A36.json
%{_datarootdir}/%{name}/html/db/A37.json
%{_datarootdir}/%{name}/html/db/A38.json
%{_datarootdir}/%{name}/html/db/A39.json
%{_datarootdir}/%{name}/html/db/A3A.json
%{_datarootdir}/%{name}/html/db/A3B.json
%{_datarootdir}/%{name}/html/db/A3C.json
%{_datarootdir}/%{name}/html/db/A3E.json
%{_datarootdir}/%{name}/html/db/A3F.json
%{_datarootdir}/%{name}/html/db/A4.json
%{_datarootdir}/%{name}/html/db/A40.json
%{_datarootdir}/%{name}/html/db/A41.json
%{_datarootdir}/%{name}/html/db/A42.json
%{_datarootdir}/%{name}/html/db/A43.json
%{_datarootdir}/%{name}/html/db/A44.json
%{_datarootdir}/%{name}/html/db/A45.json
%{_datarootdir}/%{name}/html/db/A47.json
%{_datarootdir}/%{name}/html/db/A48.json
%{_datarootdir}/%{name}/html/db/A49.json
%{_datarootdir}/%{name}/html/db/A4A.json
%{_datarootdir}/%{name}/html/db/A4A9.json
%{_datarootdir}/%{name}/html/db/A4B.json
%{_datarootdir}/%{name}/html/db/A4C.json
%{_datarootdir}/%{name}/html/db/A4D.json
%{_datarootdir}/%{name}/html/db/A4DE.json
%{_datarootdir}/%{name}/html/db/A4E.json
%{_datarootdir}/%{name}/html/db/A4F.json
%{_datarootdir}/%{name}/html/db/A5.json
%{_datarootdir}/%{name}/html/db/A50.json
%{_datarootdir}/%{name}/html/db/A51.json
%{_datarootdir}/%{name}/html/db/A52.json
%{_datarootdir}/%{name}/html/db/A53.json
%{_datarootdir}/%{name}/html/db/A54.json
%{_datarootdir}/%{name}/html/db/A55.json
%{_datarootdir}/%{name}/html/db/A56.json
%{_datarootdir}/%{name}/html/db/A57.json
%{_datarootdir}/%{name}/html/db/A58.json
%{_datarootdir}/%{name}/html/db/A59.json
%{_datarootdir}/%{name}/html/db/A5A.json
%{_datarootdir}/%{name}/html/db/A5B.json
%{_datarootdir}/%{name}/html/db/A5C.json
%{_datarootdir}/%{name}/html/db/A5E.json
%{_datarootdir}/%{name}/html/db/A5F.json
%{_datarootdir}/%{name}/html/db/A6.json
%{_datarootdir}/%{name}/html/db/A60.json
%{_datarootdir}/%{name}/html/db/A61.json
%{_datarootdir}/%{name}/html/db/A63.json
%{_datarootdir}/%{name}/html/db/A635.json
%{_datarootdir}/%{name}/html/db/A636.json
%{_datarootdir}/%{name}/html/db/A64.json
%{_datarootdir}/%{name}/html/db/A64F.json
%{_datarootdir}/%{name}/html/db/A65.json
%{_datarootdir}/%{name}/html/db/A66.json
%{_datarootdir}/%{name}/html/db/A67.json
%{_datarootdir}/%{name}/html/db/A68.json
%{_datarootdir}/%{name}/html/db/A69.json
%{_datarootdir}/%{name}/html/db/A6A.json
%{_datarootdir}/%{name}/html/db/A6B.json
%{_datarootdir}/%{name}/html/db/A6C.json
%{_datarootdir}/%{name}/html/db/A6D.json
%{_datarootdir}/%{name}/html/db/A6E.json
%{_datarootdir}/%{name}/html/db/A6F.json
%{_datarootdir}/%{name}/html/db/A7.json
%{_datarootdir}/%{name}/html/db/A70.json
%{_datarootdir}/%{name}/html/db/A71.json
%{_datarootdir}/%{name}/html/db/A72.json
%{_datarootdir}/%{name}/html/db/A73.json
%{_datarootdir}/%{name}/html/db/A74.json
%{_datarootdir}/%{name}/html/db/A75.json
%{_datarootdir}/%{name}/html/db/A76.json
%{_datarootdir}/%{name}/html/db/A77.json
%{_datarootdir}/%{name}/html/db/A78.json
%{_datarootdir}/%{name}/html/db/A79.json
%{_datarootdir}/%{name}/html/db/A7A.json
%{_datarootdir}/%{name}/html/db/A7C.json
%{_datarootdir}/%{name}/html/db/A7C4.json
%{_datarootdir}/%{name}/html/db/A7CA.json
%{_datarootdir}/%{name}/html/db/A7D.json
%{_datarootdir}/%{name}/html/db/A7E.json
%{_datarootdir}/%{name}/html/db/A7F.json
%{_datarootdir}/%{name}/html/db/A8.json
%{_datarootdir}/%{name}/html/db/A80.json
%{_datarootdir}/%{name}/html/db/A81.json
%{_datarootdir}/%{name}/html/db/A82.json
%{_datarootdir}/%{name}/html/db/A83.json
%{_datarootdir}/%{name}/html/db/A84.json
%{_datarootdir}/%{name}/html/db/A85.json
%{_datarootdir}/%{name}/html/db/A86.json
%{_datarootdir}/%{name}/html/db/A87.json
%{_datarootdir}/%{name}/html/db/A88.json
%{_datarootdir}/%{name}/html/db/A89.json
%{_datarootdir}/%{name}/html/db/A8A.json
%{_datarootdir}/%{name}/html/db/A8B.json
%{_datarootdir}/%{name}/html/db/A8C.json
%{_datarootdir}/%{name}/html/db/A8D.json
%{_datarootdir}/%{name}/html/db/A8F.json
%{_datarootdir}/%{name}/html/db/A9.json
%{_datarootdir}/%{name}/html/db/A90.json
%{_datarootdir}/%{name}/html/db/A92.json
%{_datarootdir}/%{name}/html/db/A93.json
%{_datarootdir}/%{name}/html/db/A94.json
%{_datarootdir}/%{name}/html/db/A95.json
%{_datarootdir}/%{name}/html/db/A957.json
%{_datarootdir}/%{name}/html/db/A95B.json
%{_datarootdir}/%{name}/html/db/A96.json
%{_datarootdir}/%{name}/html/db/A966.json
%{_datarootdir}/%{name}/html/db/A97.json
%{_datarootdir}/%{name}/html/db/A98.json
%{_datarootdir}/%{name}/html/db/A986.json
%{_datarootdir}/%{name}/html/db/A98A.json
%{_datarootdir}/%{name}/html/db/A99.json
%{_datarootdir}/%{name}/html/db/A9A.json
%{_datarootdir}/%{name}/html/db/A9B.json
%{_datarootdir}/%{name}/html/db/A9C.json
%{_datarootdir}/%{name}/html/db/A9D.json
%{_datarootdir}/%{name}/html/db/A9D6.json
%{_datarootdir}/%{name}/html/db/A9DD.json
%{_datarootdir}/%{name}/html/db/A9E.json
%{_datarootdir}/%{name}/html/db/A9E5.json
%{_datarootdir}/%{name}/html/db/A9E6.json
%{_datarootdir}/%{name}/html/db/A9F.json
%{_datarootdir}/%{name}/html/db/AA.json
%{_datarootdir}/%{name}/html/db/AA0.json
%{_datarootdir}/%{name}/html/db/AA1.json
%{_datarootdir}/%{name}/html/db/AA2.json
%{_datarootdir}/%{name}/html/db/AA3.json
%{_datarootdir}/%{name}/html/db/AA37.json
%{_datarootdir}/%{name}/html/db/AA4.json
%{_datarootdir}/%{name}/html/db/AA5.json
%{_datarootdir}/%{name}/html/db/AA6.json
%{_datarootdir}/%{name}/html/db/AA7.json
%{_datarootdir}/%{name}/html/db/AA8.json
%{_datarootdir}/%{name}/html/db/AA9.json
%{_datarootdir}/%{name}/html/db/AAA.json
%{_datarootdir}/%{name}/html/db/AAB.json
%{_datarootdir}/%{name}/html/db/AAD.json
%{_datarootdir}/%{name}/html/db/AAE.json
%{_datarootdir}/%{name}/html/db/AAEC.json
%{_datarootdir}/%{name}/html/db/AAF.json
%{_datarootdir}/%{name}/html/db/AB.json
%{_datarootdir}/%{name}/html/db/AB0.json
%{_datarootdir}/%{name}/html/db/AB1.json
%{_datarootdir}/%{name}/html/db/AB2.json
%{_datarootdir}/%{name}/html/db/AB3.json
%{_datarootdir}/%{name}/html/db/AB4.json
%{_datarootdir}/%{name}/html/db/AB5.json
%{_datarootdir}/%{name}/html/db/AB6.json
%{_datarootdir}/%{name}/html/db/AB7.json
%{_datarootdir}/%{name}/html/db/AB8.json
%{_datarootdir}/%{name}/html/db/AB9.json
%{_datarootdir}/%{name}/html/db/ABA.json
%{_datarootdir}/%{name}/html/db/ABB.json
%{_datarootdir}/%{name}/html/db/ABC.json
%{_datarootdir}/%{name}/html/db/ABE.json
%{_datarootdir}/%{name}/html/db/ABF.json
%{_datarootdir}/%{name}/html/db/AC.json
%{_datarootdir}/%{name}/html/db/AC0.json
%{_datarootdir}/%{name}/html/db/AC1.json
%{_datarootdir}/%{name}/html/db/AC2.json
%{_datarootdir}/%{name}/html/db/AC3.json
%{_datarootdir}/%{name}/html/db/AC4.json
%{_datarootdir}/%{name}/html/db/AC6.json
%{_datarootdir}/%{name}/html/db/AC7.json
%{_datarootdir}/%{name}/html/db/AC8.json
%{_datarootdir}/%{name}/html/db/AC9.json
%{_datarootdir}/%{name}/html/db/AC9D.json
%{_datarootdir}/%{name}/html/db/ACA.json
%{_datarootdir}/%{name}/html/db/ACB.json
%{_datarootdir}/%{name}/html/db/ACC.json
%{_datarootdir}/%{name}/html/db/ACD.json
%{_datarootdir}/%{name}/html/db/ACE.json
%{_datarootdir}/%{name}/html/db/ACF.json
%{_datarootdir}/%{name}/html/db/AD.json
%{_datarootdir}/%{name}/html/db/AD0.json
%{_datarootdir}/%{name}/html/db/AD1.json
%{_datarootdir}/%{name}/html/db/AD2.json
%{_datarootdir}/%{name}/html/db/AD3.json
%{_datarootdir}/%{name}/html/db/AD4.json
%{_datarootdir}/%{name}/html/db/AD5.json
%{_datarootdir}/%{name}/html/db/AD6.json
%{_datarootdir}/%{name}/html/db/AD7.json
%{_datarootdir}/%{name}/html/db/AD8.json
%{_datarootdir}/%{name}/html/db/AD9.json
%{_datarootdir}/%{name}/html/db/ADA.json
%{_datarootdir}/%{name}/html/db/ADB.json
%{_datarootdir}/%{name}/html/db/ADC.json
%{_datarootdir}/%{name}/html/db/ADD.json
%{_datarootdir}/%{name}/html/db/ADE.json
%{_datarootdir}/%{name}/html/db/B.json
%{_datarootdir}/%{name}/html/db/C.json
%{_datarootdir}/%{name}/html/db/D.json
%{_datarootdir}/%{name}/html/db/E.json
%{_datarootdir}/%{name}/html/db/F.json
%{_datarootdir}/%{name}/html/db/README
%{_datarootdir}/%{name}/html/db/aircraft_types/README
%{_datarootdir}/%{name}/html/db/aircraft_types/icao_aircraft_types.json
%{_datarootdir}/%{name}/html/dbloader.js
%{_datarootdir}/%{name}/html/flags-tiny/Afghanistan.png
%{_datarootdir}/%{name}/html/flags-tiny/Albania.png
%{_datarootdir}/%{name}/html/flags-tiny/Algeria.png
%{_datarootdir}/%{name}/html/flags-tiny/American_Samoa.png
%{_datarootdir}/%{name}/html/flags-tiny/Andorra.png
%{_datarootdir}/%{name}/html/flags-tiny/Angola.png
%{_datarootdir}/%{name}/html/flags-tiny/Anguilla.png
%{_datarootdir}/%{name}/html/flags-tiny/Antigua_and_Barbuda.png
%{_datarootdir}/%{name}/html/flags-tiny/Argentina.png
%{_datarootdir}/%{name}/html/flags-tiny/Armenia.png
%{_datarootdir}/%{name}/html/flags-tiny/Aruba.png
%{_datarootdir}/%{name}/html/flags-tiny/Australia.png
%{_datarootdir}/%{name}/html/flags-tiny/Austria.png
%{_datarootdir}/%{name}/html/flags-tiny/Azerbaijan.png
%{_datarootdir}/%{name}/html/flags-tiny/Bahamas.png
%{_datarootdir}/%{name}/html/flags-tiny/Bahrain.png
%{_datarootdir}/%{name}/html/flags-tiny/Bangladesh.png
%{_datarootdir}/%{name}/html/flags-tiny/Barbados.png
%{_datarootdir}/%{name}/html/flags-tiny/Belarus.png
%{_datarootdir}/%{name}/html/flags-tiny/Belgium.png
%{_datarootdir}/%{name}/html/flags-tiny/Belize.png
%{_datarootdir}/%{name}/html/flags-tiny/Benin.png
%{_datarootdir}/%{name}/html/flags-tiny/Bermuda.png
%{_datarootdir}/%{name}/html/flags-tiny/Bhutan.png
%{_datarootdir}/%{name}/html/flags-tiny/Bolivia.png
%{_datarootdir}/%{name}/html/flags-tiny/Bosnia.png
%{_datarootdir}/%{name}/html/flags-tiny/Botswana.png
%{_datarootdir}/%{name}/html/flags-tiny/Brazil.png
%{_datarootdir}/%{name}/html/flags-tiny/British_Virgin_Islands.png
%{_datarootdir}/%{name}/html/flags-tiny/Brunei.png
%{_datarootdir}/%{name}/html/flags-tiny/Bulgaria.png
%{_datarootdir}/%{name}/html/flags-tiny/Burkina_Faso.png
%{_datarootdir}/%{name}/html/flags-tiny/Burundi.png
%{_datarootdir}/%{name}/html/flags-tiny/Cambodia.png
%{_datarootdir}/%{name}/html/flags-tiny/Cameroon.png
%{_datarootdir}/%{name}/html/flags-tiny/Canada.png
%{_datarootdir}/%{name}/html/flags-tiny/Cape_Verde.png
%{_datarootdir}/%{name}/html/flags-tiny/Cayman_Islands.png
%{_datarootdir}/%{name}/html/flags-tiny/Central_African_Republic.png
%{_datarootdir}/%{name}/html/flags-tiny/Chad.png
%{_datarootdir}/%{name}/html/flags-tiny/Chile.png
%{_datarootdir}/%{name}/html/flags-tiny/China.png
%{_datarootdir}/%{name}/html/flags-tiny/Christmas_Island.png
%{_datarootdir}/%{name}/html/flags-tiny/Colombia.png
%{_datarootdir}/%{name}/html/flags-tiny/Comoros.png
%{_datarootdir}/%{name}/html/flags-tiny/Cook_Islands.png
%{_datarootdir}/%{name}/html/flags-tiny/Costa_Rica.png
%{_datarootdir}/%{name}/html/flags-tiny/Cote_d_Ivoire.png
%{_datarootdir}/%{name}/html/flags-tiny/Croatia.png
%{_datarootdir}/%{name}/html/flags-tiny/Cuba.png
%{_datarootdir}/%{name}/html/flags-tiny/Cyprus.png
%{_datarootdir}/%{name}/html/flags-tiny/Cyprus_Northern.png
%{_datarootdir}/%{name}/html/flags-tiny/Czech_Republic.png
%{_datarootdir}/%{name}/html/flags-tiny/Democratic_Republic_of_the_Congo.png
%{_datarootdir}/%{name}/html/flags-tiny/Denmark.png
%{_datarootdir}/%{name}/html/flags-tiny/Djibouti.png
%{_datarootdir}/%{name}/html/flags-tiny/Dominica.png
%{_datarootdir}/%{name}/html/flags-tiny/Dominican_Republic.png
%{_datarootdir}/%{name}/html/flags-tiny/Ecuador.png
%{_datarootdir}/%{name}/html/flags-tiny/Egypt.png
%{_datarootdir}/%{name}/html/flags-tiny/El_Salvador.png
%{_datarootdir}/%{name}/html/flags-tiny/Equatorial_Guinea.png
%{_datarootdir}/%{name}/html/flags-tiny/Eritrea.png
%{_datarootdir}/%{name}/html/flags-tiny/Estonia.png
%{_datarootdir}/%{name}/html/flags-tiny/Ethiopia.png
%{_datarootdir}/%{name}/html/flags-tiny/Falkland_Islands.png
%{_datarootdir}/%{name}/html/flags-tiny/Faroe_Islands.png
%{_datarootdir}/%{name}/html/flags-tiny/Fiji.png
%{_datarootdir}/%{name}/html/flags-tiny/Finland.png
%{_datarootdir}/%{name}/html/flags-tiny/France.png
%{_datarootdir}/%{name}/html/flags-tiny/French_Polynesia.png
%{_datarootdir}/%{name}/html/flags-tiny/Gabon.png
%{_datarootdir}/%{name}/html/flags-tiny/Gambia.png
%{_datarootdir}/%{name}/html/flags-tiny/Georgia.png
%{_datarootdir}/%{name}/html/flags-tiny/Germany.png
%{_datarootdir}/%{name}/html/flags-tiny/Ghana.png
%{_datarootdir}/%{name}/html/flags-tiny/Gibraltar.png
%{_datarootdir}/%{name}/html/flags-tiny/Greece.png
%{_datarootdir}/%{name}/html/flags-tiny/Greenland.png
%{_datarootdir}/%{name}/html/flags-tiny/Grenada.png
%{_datarootdir}/%{name}/html/flags-tiny/Guam.png
%{_datarootdir}/%{name}/html/flags-tiny/Guatemala.png
%{_datarootdir}/%{name}/html/flags-tiny/Guinea.png
%{_datarootdir}/%{name}/html/flags-tiny/Guinea_Bissau.png
%{_datarootdir}/%{name}/html/flags-tiny/Guyana.png
%{_datarootdir}/%{name}/html/flags-tiny/Haiti.png
%{_datarootdir}/%{name}/html/flags-tiny/Honduras.png
%{_datarootdir}/%{name}/html/flags-tiny/Hong_Kong.png
%{_datarootdir}/%{name}/html/flags-tiny/Hungary.png
%{_datarootdir}/%{name}/html/flags-tiny/Iceland.png
%{_datarootdir}/%{name}/html/flags-tiny/India.png
%{_datarootdir}/%{name}/html/flags-tiny/Indonesia.png
%{_datarootdir}/%{name}/html/flags-tiny/Iran.png
%{_datarootdir}/%{name}/html/flags-tiny/Iraq.png
%{_datarootdir}/%{name}/html/flags-tiny/Ireland.png
%{_datarootdir}/%{name}/html/flags-tiny/Israel.png
%{_datarootdir}/%{name}/html/flags-tiny/Italy.png
%{_datarootdir}/%{name}/html/flags-tiny/Jamaica.png
%{_datarootdir}/%{name}/html/flags-tiny/Japan.png
%{_datarootdir}/%{name}/html/flags-tiny/Jordan.png
%{_datarootdir}/%{name}/html/flags-tiny/Kazakhstan.png
%{_datarootdir}/%{name}/html/flags-tiny/Kenya.png
%{_datarootdir}/%{name}/html/flags-tiny/Kiribati.png
%{_datarootdir}/%{name}/html/flags-tiny/Kuwait.png
%{_datarootdir}/%{name}/html/flags-tiny/Kyrgyzstan.png
%{_datarootdir}/%{name}/html/flags-tiny/Laos.png
%{_datarootdir}/%{name}/html/flags-tiny/Latvia.png
%{_datarootdir}/%{name}/html/flags-tiny/Lebanon.png
%{_datarootdir}/%{name}/html/flags-tiny/Lesotho.png
%{_datarootdir}/%{name}/html/flags-tiny/Liberia.png
%{_datarootdir}/%{name}/html/flags-tiny/Libya.png
%{_datarootdir}/%{name}/html/flags-tiny/Liechtenstein.png
%{_datarootdir}/%{name}/html/flags-tiny/Lithuania.png
%{_datarootdir}/%{name}/html/flags-tiny/Luxembourg.png
%{_datarootdir}/%{name}/html/flags-tiny/Macao.png
%{_datarootdir}/%{name}/html/flags-tiny/Macedonia.png
%{_datarootdir}/%{name}/html/flags-tiny/Madagascar.png
%{_datarootdir}/%{name}/html/flags-tiny/Malawi.png
%{_datarootdir}/%{name}/html/flags-tiny/Malaysia.png
%{_datarootdir}/%{name}/html/flags-tiny/Maldives.png
%{_datarootdir}/%{name}/html/flags-tiny/Mali.png
%{_datarootdir}/%{name}/html/flags-tiny/Malta.png
%{_datarootdir}/%{name}/html/flags-tiny/Marshall_Islands.png
%{_datarootdir}/%{name}/html/flags-tiny/Martinique.png
%{_datarootdir}/%{name}/html/flags-tiny/Mauritania.png
%{_datarootdir}/%{name}/html/flags-tiny/Mauritius.png
%{_datarootdir}/%{name}/html/flags-tiny/Mexico.png
%{_datarootdir}/%{name}/html/flags-tiny/Micronesia.png
%{_datarootdir}/%{name}/html/flags-tiny/Moldova.png
%{_datarootdir}/%{name}/html/flags-tiny/Monaco.png
%{_datarootdir}/%{name}/html/flags-tiny/Mongolia.png
%{_datarootdir}/%{name}/html/flags-tiny/Montenegro.png
%{_datarootdir}/%{name}/html/flags-tiny/Montserrat.png
%{_datarootdir}/%{name}/html/flags-tiny/Morocco.png
%{_datarootdir}/%{name}/html/flags-tiny/Mozambique.png
%{_datarootdir}/%{name}/html/flags-tiny/Myanmar.png
%{_datarootdir}/%{name}/html/flags-tiny/Namibia.png
%{_datarootdir}/%{name}/html/flags-tiny/Nauru.png
%{_datarootdir}/%{name}/html/flags-tiny/Nepal.png
%{_datarootdir}/%{name}/html/flags-tiny/Netherlands.png
%{_datarootdir}/%{name}/html/flags-tiny/Netherlands_Antilles.png
%{_datarootdir}/%{name}/html/flags-tiny/New_Zealand.png
%{_datarootdir}/%{name}/html/flags-tiny/Nicaragua.png
%{_datarootdir}/%{name}/html/flags-tiny/Niger.png
%{_datarootdir}/%{name}/html/flags-tiny/Nigeria.png
%{_datarootdir}/%{name}/html/flags-tiny/Niue.png
%{_datarootdir}/%{name}/html/flags-tiny/Norfolk_Island.png
%{_datarootdir}/%{name}/html/flags-tiny/North_Korea.png
%{_datarootdir}/%{name}/html/flags-tiny/Norway.png
%{_datarootdir}/%{name}/html/flags-tiny/Oman.png
%{_datarootdir}/%{name}/html/flags-tiny/Pakistan.png
%{_datarootdir}/%{name}/html/flags-tiny/Palau.png
%{_datarootdir}/%{name}/html/flags-tiny/Panama.png
%{_datarootdir}/%{name}/html/flags-tiny/Papua_New_Guinea.png
%{_datarootdir}/%{name}/html/flags-tiny/Paraguay.png
%{_datarootdir}/%{name}/html/flags-tiny/Peru.png
%{_datarootdir}/%{name}/html/flags-tiny/Philippines.png
%{_datarootdir}/%{name}/html/flags-tiny/Pitcairn_Islands.png
%{_datarootdir}/%{name}/html/flags-tiny/Poland.png
%{_datarootdir}/%{name}/html/flags-tiny/Portugal.png
%{_datarootdir}/%{name}/html/flags-tiny/Puerto_Rico.png
%{_datarootdir}/%{name}/html/flags-tiny/Qatar.png
%{_datarootdir}/%{name}/html/flags-tiny/README.txt
%{_datarootdir}/%{name}/html/flags-tiny/Republic_of_the_Congo.png
%{_datarootdir}/%{name}/html/flags-tiny/Romania.png
%{_datarootdir}/%{name}/html/flags-tiny/Russian_Federation.png
%{_datarootdir}/%{name}/html/flags-tiny/Rwanda.png
%{_datarootdir}/%{name}/html/flags-tiny/Saint_Kitts_and_Nevis.png
%{_datarootdir}/%{name}/html/flags-tiny/Saint_Lucia.png
%{_datarootdir}/%{name}/html/flags-tiny/Saint_Pierre.png
%{_datarootdir}/%{name}/html/flags-tiny/Saint_Vicent_and_the_Grenadines.png
%{_datarootdir}/%{name}/html/flags-tiny/Samoa.png
%{_datarootdir}/%{name}/html/flags-tiny/San_Marino.png
%{_datarootdir}/%{name}/html/flags-tiny/Sao_Tome_and_Principe.png
%{_datarootdir}/%{name}/html/flags-tiny/Saudi_Arabia.png
%{_datarootdir}/%{name}/html/flags-tiny/Senegal.png
%{_datarootdir}/%{name}/html/flags-tiny/Serbia.png
%{_datarootdir}/%{name}/html/flags-tiny/Seychelles.png
%{_datarootdir}/%{name}/html/flags-tiny/Sierra_Leone.png
%{_datarootdir}/%{name}/html/flags-tiny/Singapore.png
%{_datarootdir}/%{name}/html/flags-tiny/Slovakia.png
%{_datarootdir}/%{name}/html/flags-tiny/Slovenia.png
%{_datarootdir}/%{name}/html/flags-tiny/Soloman_Islands.png
%{_datarootdir}/%{name}/html/flags-tiny/Somalia.png
%{_datarootdir}/%{name}/html/flags-tiny/South_Africa.png
%{_datarootdir}/%{name}/html/flags-tiny/South_Georgia.png
%{_datarootdir}/%{name}/html/flags-tiny/South_Korea.png
%{_datarootdir}/%{name}/html/flags-tiny/Soviet_Union.png
%{_datarootdir}/%{name}/html/flags-tiny/Spain.png
%{_datarootdir}/%{name}/html/flags-tiny/Sri_Lanka.png
%{_datarootdir}/%{name}/html/flags-tiny/Sudan.png
%{_datarootdir}/%{name}/html/flags-tiny/Suriname.png
%{_datarootdir}/%{name}/html/flags-tiny/Swaziland.png
%{_datarootdir}/%{name}/html/flags-tiny/Sweden.png
%{_datarootdir}/%{name}/html/flags-tiny/Switzerland.png
%{_datarootdir}/%{name}/html/flags-tiny/Syria.png
%{_datarootdir}/%{name}/html/flags-tiny/Taiwan.png
%{_datarootdir}/%{name}/html/flags-tiny/Tajikistan.png
%{_datarootdir}/%{name}/html/flags-tiny/Tanzania.png
%{_datarootdir}/%{name}/html/flags-tiny/Thailand.png
%{_datarootdir}/%{name}/html/flags-tiny/Tibet.png
%{_datarootdir}/%{name}/html/flags-tiny/Timor-Leste.png
%{_datarootdir}/%{name}/html/flags-tiny/Togo.png
%{_datarootdir}/%{name}/html/flags-tiny/Tonga.png
%{_datarootdir}/%{name}/html/flags-tiny/Trinidad_and_Tobago.png
%{_datarootdir}/%{name}/html/flags-tiny/Tunisia.png
%{_datarootdir}/%{name}/html/flags-tiny/Turkey.png
%{_datarootdir}/%{name}/html/flags-tiny/Turkmenistan.png
%{_datarootdir}/%{name}/html/flags-tiny/Turks_and_Caicos_Islands.png
%{_datarootdir}/%{name}/html/flags-tiny/Tuvalu.png
%{_datarootdir}/%{name}/html/flags-tiny/UAE.png
%{_datarootdir}/%{name}/html/flags-tiny/US_Virgin_Islands.png
%{_datarootdir}/%{name}/html/flags-tiny/Uganda.png
%{_datarootdir}/%{name}/html/flags-tiny/Ukraine.png
%{_datarootdir}/%{name}/html/flags-tiny/United_Kingdom.png
%{_datarootdir}/%{name}/html/flags-tiny/United_States_of_America.png
%{_datarootdir}/%{name}/html/flags-tiny/Uruguay.png
%{_datarootdir}/%{name}/html/flags-tiny/Uzbekistan.png
%{_datarootdir}/%{name}/html/flags-tiny/Vanuatu.png
%{_datarootdir}/%{name}/html/flags-tiny/Vatican_City.png
%{_datarootdir}/%{name}/html/flags-tiny/Venezuela.png
%{_datarootdir}/%{name}/html/flags-tiny/Vietnam.png
%{_datarootdir}/%{name}/html/flags-tiny/Wallis_and_Futuna.png
%{_datarootdir}/%{name}/html/flags-tiny/Yemen.png
%{_datarootdir}/%{name}/html/flags-tiny/Yugoslavia.png
%{_datarootdir}/%{name}/html/flags-tiny/Zambia.png
%{_datarootdir}/%{name}/html/flags-tiny/Zimbabwe.png
%{_datarootdir}/%{name}/html/flags-tiny/blank.png
%{_datarootdir}/%{name}/html/flags.js
%{_datarootdir}/%{name}/html/formatter.js
%{_datarootdir}/%{name}/html/images/alt_legend_feet.svg
%{_datarootdir}/%{name}/html/images/alt_legend_meters.svg
%{_datarootdir}/%{name}/html/images/box-checked.png
%{_datarootdir}/%{name}/html/images/box-checked@2x.png
%{_datarootdir}/%{name}/html/images/box-checked@3x.png
%{_datarootdir}/%{name}/html/images/box-empty.png
%{_datarootdir}/%{name}/html/images/box-empty@2x.png
%{_datarootdir}/%{name}/html/images/box-empty@3x.png
%{_datarootdir}/%{name}/html/images/close-settings.png
%{_datarootdir}/%{name}/html/images/close-settings@2x.png
%{_datarootdir}/%{name}/html/images/close-settings@3x.png
%{_datarootdir}/%{name}/html/images/column-adjust.png
%{_datarootdir}/%{name}/html/images/column-adjust@2x.png
%{_datarootdir}/%{name}/html/images/column-adjust@3x.png
%{_datarootdir}/%{name}/html/images/fa_logo_color.png
%{_datarootdir}/%{name}/html/images/fa_logo_color@2x.png
%{_datarootdir}/%{name}/html/images/fa_logo_color@3x.png
%{_datarootdir}/%{name}/html/images/ff-sv-logo.png
%{_datarootdir}/%{name}/html/images/ff-sv-logo@2x.png
%{_datarootdir}/%{name}/html/images/ff-sv-logo@3x.png
%{_datarootdir}/%{name}/html/images/hide_sidebar_active_48x40.png
%{_datarootdir}/%{name}/html/images/hide_sidebar_inactive_48x40.png
%{_datarootdir}/%{name}/html/images/icon-information@2x.png
%{_datarootdir}/%{name}/html/images/map-icon.png
%{_datarootdir}/%{name}/html/images/map-icon@2x.png
%{_datarootdir}/%{name}/html/images/map-icon@3x.png
%{_datarootdir}/%{name}/html/images/pa-sv-logo.png
%{_datarootdir}/%{name}/html/images/pa-sv-logo@2x.png
%{_datarootdir}/%{name}/html/images/pa-sv-logo@3x.png
%{_datarootdir}/%{name}/html/images/settings-icon.png
%{_datarootdir}/%{name}/html/images/settings-icon@2x.png
%{_datarootdir}/%{name}/html/images/settings-icon@3x.png
%{_datarootdir}/%{name}/html/images/show_sidebar_active_48x40.png
%{_datarootdir}/%{name}/html/images/show_sidebar_inactive_48x40.png
%{_datarootdir}/%{name}/html/images/table-icon.png
%{_datarootdir}/%{name}/html/images/table-icon@2x.png
%{_datarootdir}/%{name}/html/images/table-icon@3x.png
%{_datarootdir}/%{name}/html/images/toggle-height@2x.png
%{_datarootdir}/%{name}/html/images/toggle-width@2x.png
%{_datarootdir}/%{name}/html/images/zoom-in.png
%{_datarootdir}/%{name}/html/images/zoom-in@2x.png
%{_datarootdir}/%{name}/html/images/zoom-in@3x.png
%{_datarootdir}/%{name}/html/images/zoom-out.png
%{_datarootdir}/%{name}/html/images/zoom-out@2x.png
%{_datarootdir}/%{name}/html/images/zoom-out@3x.png
%{_datarootdir}/%{name}/html/index.html
%{_datarootdir}/%{name}/html/jquery/README
%{_datarootdir}/%{name}/html/jquery/jquery-3.0.0.min.js
%{_datarootdir}/%{name}/html/jquery/jquery-ui-1.11.4-smoothness.css
%{_datarootdir}/%{name}/html/jquery/jquery-ui-1.11.4.min.js
%{_datarootdir}/%{name}/html/jquery/plugins/jquery.validate.min.js
%{_datarootdir}/%{name}/html/layers.js
%{_datarootdir}/%{name}/html/markers.js
%{_datarootdir}/%{name}/html/ol/ol-4.4.2.css
%{_datarootdir}/%{name}/html/ol/ol-4.4.2.js
%{_datarootdir}/%{name}/html/ol/ol3-layerswitcher.css
%{_datarootdir}/%{name}/html/ol/ol3-layerswitcher.js
%{_datarootdir}/%{name}/html/planeObject.js
%{_datarootdir}/%{name}/html/registrations.js
%{_datarootdir}/%{name}/html/script.js
%{_datarootdir}/%{name}/html/spinny.gif
%{_datarootdir}/%{name}/html/style.css
%{_datarootdir}/%{name}/html/test/markers_test.html
%{_datarootdir}/%{name}/html/test/markers_test.js

%changelog
* Fri Nov 2 2018 Quentin Schwerkolt
- Update to 3.6.3

* Fri Apr 7 2017 Quentin Schwerkolt
- Update to 3.5.0

* Sat Jan 21 2017 Quentin Schwerkolt
- Initial Version
