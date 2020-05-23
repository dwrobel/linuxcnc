#!/bin/bash -e

if ! dnf repolist | grep copr:copr.fedorainfracloud.org:dwrobel:python-Yapps2; then
    rpm -qv dnf-plugins-core 2>/dev/null || sudo dnf install dnf-plugins-core
    sudo dnf copr enable -y dwrobel/python-Yapps2
    sudo dnf builddep -y linuxcnc.spec
fi

pushd ../src

export CFLAGS="-Dcflags -O0 -ggdb3 -fno-gnu89-inline -std=gnu17"
export CXXFLAGS="-Dcxxflags -O0 -ggdb3 -std=c++17"
export CPPFLAGS="-Dcppflags -I/usr/include/readline5 $(pkg-config --cflags python${pv}) -O0 -ggdb3"
#export CPPFLAGS="-Dcppflags -I/usr/include/readline5 $(pkg-config --cflags python${pv}) -O0 -ggdb3 -fsanitize=address -fPIE -fno-omit-frame-pointer"
#ASAN_OPTIONS=halt_on_error=false LD_PRELOAD=/usr/lib64/libasan.so.5 linuxcnc
export LDFLAGS="-L/usr/lib64/readline5"

autoreconf -fi .

export ac_cv_path_CHECKLINK=/usr/bin/true

./configure \
    --enable-non-distributable=no \
    --with-realtime=uspace \

#    --enable-build-documentation=pdf
#    --enable-non-distributable=yes \

make -j$(getconf _NPROCESSORS_ONLN) -O V=1 2>&1 | tee ../fedora/build.log

#echo "(cd ../src && sudo make setuid -n)"
sudo setcap cap_ipc_lock,cap_net_admin,cap_sys_rawio,cap_sys_nice+ep  ../bin/rtapi_app
