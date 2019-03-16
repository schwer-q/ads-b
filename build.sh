#!/bin/sh -
#
# Copyright (c) 2019, Quentin Schwerkolt
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

set -e
set -x

PACKAGES="libbladeRF dump1090-fa mlat-client tcllauncher piaware"
DIST='f29'
ARCH=`uname -m`
case "${ARCH}" in
    'armv7l')
	ARCH='armv7hl'
	;;
esac

for PKG in ${PACKAGES}; do
    if rpm -qa | grep -q ${PKG}; then
	sudo dnf remove ${PKG}
    fi
    cd ${PKG}
    DEPENDS=`grep '^BuildRequires:' *.spec | cut -f2 | cut -d' ' -f1`
    for DEP in ${DEPENDS}; do
	rpm -qa | grep -q ${DEP} || sudo dnf install ${DEP}
    done
    spectool -g *.spec
    fedpkg --release ${DIST} local
    sudo dnf install `ls -li ${ARCH}/*.rpm | tr -s ' ' | egrep -v 'debug|src' | sort -V | cut -d' ' -f10`
    cd ..
done
