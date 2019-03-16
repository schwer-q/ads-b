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
