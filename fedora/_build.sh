#!/bin/bash -e

pushd ../src

export CFLAGS="-Dcflags -O0 -ggdb3"
export CXXFLAGS="-Dcxxflags -O0 -ggdb3"
export CPPFLAGS="-Dcppflags -I/usr/include/readline5 -O0 -ggdb3"
export LDFLAGS="-L%{_libdir}/readline5"

autoreconf -fi .

./configure \
    --with-python=/usr/bin/python2 \
    --enable-non-distributable=no \
    --with-boost-python=boost_python27 \
    --with-realtime=uspace \
    --disable-check-runtime-deps \
    --disable-userspace-pci \

make -j$(getconf _NPROCESSORS_ONLN) V=1 2>&1 | tee build.log
