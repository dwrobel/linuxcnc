#!/bin/sh -ex
cd src
./autogen.sh
./configure --with-realtime=uspace --disable-check-runtime-deps --enable-build-documentation
make -O -j$(getconf _NPROCESSORS_ONLN) default pycheck V=1
timeout --signal=9 3600 ../scripts/rip-environment runtests -v
