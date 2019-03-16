#
# Copyright (c) 2017-2019, Quentin Schwerkolt
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

Summary:	SDR radio receiver
Name:		libbladeRF
Version:	2.0.2
Release:	1%{?dist}
License:	GPLv2
Group:		System Enviroment/Libraries
URL:		https://nuand.com/bladeRF

Source0:	https://github.com/Nuand/bladeRF/archive/libbladeRF_v%{version}.tar.gz

BuildRequires:	cmake >= 2.8.5
BuildRequires:	gcc-c++
BuildRequires:	libusbx-devel
BuildRequires:	pkgconf

%description
Nuand bladeRF software-defined radio device
The Nuand bladeRF is an open-source software-defined radio (SDR) system,
comprised of an RF transceiver, a field-programmable gate array (FPGA),
a microcontroller driving a USB 3.0 interface, and a suite of host
libraries and drivers to facilitate interaction with the device.

%package	cli
Summary:	Command line utilities for %{name}
Group:		Applications/Engineering
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	cli
The %{name}-cli package contains command line utilities for use
with %{name}

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n bladeRF-libbladeRF_v%{version}

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%cmake ..
popd
%make_build -C %{_target_platform}

%install
# make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%make_install -C %{_target_platform}
find %{buildroot}

%ldconfig_scriptlets

%files
%license COPYING
%doc CHANGELOG README.md
%{_libdir}/libbladeRF.so.*
%{_sysconfdir}/udev/rules.d/88-nuand.rules

%files		cli
%{_bindir}/bladeRF-cli
%{_bindir}/bladeRF-fsk

%files		devel
%{_includedir}/bladeRF1.h
%{_includedir}/bladeRF2.h
%{_includedir}/libbladeRF.h
%{_libdir}/libbladeRF.so
%{_libdir}/pkgconfig/libbladeRF.pc

%changelog
* Mon Dec 24 2018 Quentin Schwerkolt
- Rewrite of libbladeRF package
- Update libbladeRF to 2.0.2
