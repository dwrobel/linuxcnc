#!/bin/sh -ex
cd src
./autogen.sh
./configure --with-realtime=uspace --disable-check-runtime-deps --enable-build-documentation
make -O -j$(getconf _NPROCESSORS_ONLN) default pycheck V=1
sudo setcap cap_sys_rawio,cap_sys_nice+ep  ../bin/rtapi_app
timeout --signal=9 3600 ../scripts/rip-environment runtests $([ -z ${TRAVIS} ] && echo '-v') || \
    ([ -e ~/linuxcnc_debug.txt ] && cat ~/linuxcnc_debug.txt; \
     [ -e ~/linuxcnc_print.txt ] && cat ~/linuxcnc_print.txt ;false)
