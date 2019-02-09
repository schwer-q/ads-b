#!/bin/sh -
#
# Copyright (c) 2019, Quentin Schwerkolt
# All rights reserved.
#

set -e
set -x

PACKAGES="libbladeRF dump1090-fa mlat-client tcllauncher piaware"
DIST='f29'
ARCH=`uname -m`

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
