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
