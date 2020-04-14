#!/bin/bash -e

pushd ../src

export CFLAGS="-Dcflags -O0 -ggdb3"
export CXXFLAGS="-Dcxxflags -O0 -ggdb3"
#export CPPFLAGS="-Dcppflags -I/usr/include/readline5 -O0 -ggdb3 -fsanitize=address -fPIE -fno-omit-frame-pointer"
export CPPFLAGS="-Dcppflags -I/usr/include/readline5 -O0 -ggdb3"
export LDFLAGS="-L%{_libdir}/readline5"

autoreconf -fi .

pv=${1-3}

./configure \
    --with-python=/usr/bin/python${pv} \
    --enable-non-distributable=no \
    --with-boost-python=boost_python${pv}7 \
    --with-realtime=uspace \
    --disable-check-runtime-deps \
    --disable-userspace-pci \

make -j$(getconf _NPROCESSORS_ONLN) -O V=1 2>&1 | tee ../fedora/build.log

echo "(cd ../src && sudo make setuid -n)"