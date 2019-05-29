%global date 20190528
%global commit0 902117324cfba3bb4959401439d1e833d8b6e148
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:          machinekit
Version:       0.1
Release:       14.%{date}git%{shortcommit0}%{?dist}
Summary:       A platform for machine control applications
License:       GPLv2+
Group:         Applications/Engineering
URL:           http://www.machinekit.io/
Source0:       https://github.com/machinekit/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{version}-%{date}git%{shortcommit0}.tar.gz
Source1:       %{name}-limits.conf
# Reported upstream: https://github.com/machinekit/machinekit/pull/1102
Patch1:        %{name}-0001-Fixes-R_ARM_MOVW_ABS_NC-relocation-issue-on-armv7hl.patch
# Reported upstream: https://github.com/machinekit/machinekit/pull/1108
Patch2:        %{name}-0002-Remove-localization-file-for-non-existing-rs-country.patch
# Not sent upstream:
# we are not using setuid(2), but capabilities(7) instead
# see below capabilities for: {_libexecdir}/linuxcnc/rtapi_app_rt-preempt file
Patch3:        %{name}-0003-Remove-superfluous-checking-for-geteuid.patch
# we are building only for rt-preempt flavor so posix wouldn't work anyway
Patch4:        %{name}-0004-Remove-checking-for-RT-flavor-kernel.patch
Patch5:        %{name}-0005-Change-default-flavor-to-rt-preempt.patch
# remove platform specific compiler options
Patch6:        %{name}-0006-remove-platform-specific-compiler-options.patch
# Allow to use libtirpc as an <rpc/rpc.h> provider
Patch7:        %{name}-0007-Add-a-possibility-to-use-libtirpc-as-an-rpc-rpc.h-pr.patch
# Add missing <math.h> header file
Patch8:        %{name}-0008-Add-missing-math.h-header.patch
# Reported upstream: https://github.com/machinekit/machinekit-cnc/pull/58
Patch9:        %{name}-0009-Remove-ambiguous-python-shebang-use-python2-explicit.patch
# Reported upstream: https://github.com/machinekit/machinekit-cnc/pull/61
Patch10:       %{name}-0010-Fix-mangling-shebangs.patch
# Reported upstream: https://github.com/machinekit/machinekit-cnc/pull/59
Patch11:       %{name}-0011-Fix-configure-error-when-python-interpreter-is-avail.patch
# Reported upstream: https://github.com/machinekit/machinekit-cnc/pull/60
Patch12:       %{name}-0012-Remove-executable-bit-for-files-without-shebang.patch

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}

%global main_icon_file %{_datadir}/icons/hicolor/256x256/apps/%{name}icon.png
%global wizard_icon_file %{_datadir}/icons/hicolor/256x256/apps/%{name}-wizard.png
%global security_conf_file %{_sysconfdir}/security/limits.d/10-linuxcnc.conf

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: /usr/bin/git
BuildRequires: /usr/bin/which
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: openssl-devel
BuildRequires: libusbx-devel
BuildRequires: gtk2-devel
BuildRequires: procps-ng
BuildRequires: psmisc
BuildRequires: readline-devel
BuildRequires: gettext-devel
BuildRequires: python2-devel
BuildRequires: libudev-devel
BuildRequires: avahi-devel
BuildRequires: boost-devel
%if 0%{?fedora} > 28
BuildRequires: boost-python2-devel
%endif
BuildRequires: python2-Cython
BuildRequires: python3-Cython
BuildRequires: czmq-devel
BuildRequires: jansson-devel
BuildRequires: libmodbus-devel
BuildRequires: libuuid-devel
BuildRequires: libwebsockets-devel
BuildRequires: libtirpc-devel
BuildRequires: protobuf-devel
BuildRequires: protobuf-python
BuildRequires: pyftpdlib
BuildRequires: tcl-devel
BuildRequires: tk-devel
BuildRequires: tkinter
BuildRequires: uriparser-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: libXmu-devel
BuildRequires: libXaw-devel
BuildRequires: desktop-file-utils
BuildRequires: %{_bindir}/convert
BuildRequires: libcgroup-devel

Requires:      avahi
Requires:      blt
Requires:      bwidget
Requires:      hicolor-icon-theme
Requires:      python2-mttkinter
Requires:      tkimg
Requires:      pygtk2
# for ssh -X to work TODO: do we really need it?
Requires:      %{_bindir}/xauth
# for linuxcnc group creation
Requires:      %{_bindir}/getent
Requires:      %{_sbindir}/groupadd
# for /usr/share/X11/app-defaults
Requires:      libXt
# latency-test
Requires:      bc
# halmeter
Requires:      libcanberra-gtk2
Requires:      PackageKit-gtk3-module
# axis
Requires:      tcl-togl
# for /etc/security/limits.d
Requires:      pam
# for pncconf
Requires:      gnome-python2-gnome
# for mkwrapper GUI
Requires:      python-avahi
Requires:      pyftpdlib


%description
Machinekit is the next-generation Enhanced Machine Controller
which provides motion control for CNC machine tools and robotic
applications (milling, cutting, routing, etc.).


%package devel
Group: Development/Libraries
Summary: Devel package for %{name}
Requires: %{name} = %{version}


%description devel
Development headers and libraries for the %{name} package


%prep
%autosetup -S git -n %{name}-%{commit0}

# remove spurious executable permission
chmod a-x src/hal/user_comps/xhc-hb04.cc

cat <<EOF >scripts/get-git-sha
#!/bin/sh
# We don't have original .git directory
# So we intent to mimic the original behavior
echo %{shortcommit0}
EOF

cat <<EOF >scripts/get-version-from-git
#!/bin/sh
# We don't have original .git directory
# So we intent to mimic the original behavior
echo %{version}-%{shortcommit0}
EOF

pushd src
sed -i -e 's#\(EMC2_TCL_DIR=\)${prefix}/lib/tcltk/linuxcnc#\1%{tcl_sitearch}/linuxcnc%{version}#g' \
       -e 's#\(EMC2_TCL_LIB_DIR=\)${prefix}/lib/tcltk/linuxcnc#\1%{tcl_sitearch}/linuxcnc%{version}#g' \
       -e 's#\(EMC2_LANG_DIR=\)${prefix}/share/linuxcnc/tcl/msgs#\1%{tcl_sitearch}/linuxcnc/tcl/msgs#g' \
       -e 's#\(EMC2_RTLIB_DIR=\)${prefix}/lib/linuxcnc#\1%{_libdir}/linuxcnc#g' \
       configure.ac

./autogen.sh
export CFLAGS="%{optflags} -I/usr/include/tirpc"
%configure \
    --disable-shmdrv \
    --without-posix \
    --with-rt-preempt \
    --disable-emcweb \
    --enable-portable-parport \
    --disable-usermode-pci \
    --disable-webtalk \
    --with-tirpc \
    --with-platform-raspberry \
    --with-platform-socfpga \
    --with-platform-beaglebone \
    --with-platform-chip \
    --with-platform-zedboard \
    --with-tcl=%{_libdir} \
    --with-tk=%{_libdir} \
    EMC2_TCL_DIR=%{tcl_sitearch}/linuxcnc%{version} \
    EMC2_TCL_LIB_DIR=%{tcl_sitearch}/linuxcnc%{version} \

popd

sed -i 's#lib/tcltk/linuxcnc#%{tcl_sitearch}/linuxcnc%{version}#g' \
    lib/python/rs274/options.py


%build
make -C src %{?_smp_mflags} V=1


%install
make -C src install V=1 \
    DESTDIR=%{buildroot} \
    DIR="install -d -m 0755" \
    EXE="install -m 0755" \
    FILE="install -m 0644" \
    SETUID="install -m 0755"

# install limits configuration
install -m 0644 -D %{SOURCE1} %{buildroot}%{security_conf_file}

# align doc dir with package name
mv %{buildroot}%{_datadir}/doc/linuxcnc %{buildroot}%{_datadir}/doc/%{name}

# install man file
install -m 0644 man/man1/%{name}.1* %{buildroot}/%{_mandir}/man1/

# move X11 app-defaults to the correct location
mv %{buildroot}%{_sysconfdir}/X11 %{buildroot}%{_datadir}/

# remove duplicated .so files
rm -f %{buildroot}%{_libdir}/{compat.so,hal.so,rtapi.so,shmcommon.so}

# make .so files executable
find %{buildroot}%{_libdir} -type f -name '*.so*' -exec chmod 0755 {} \;

# install icon files
install -D -m 0644 %{name}icon.png %{buildroot}%{main_icon_file}
convert %{name}-wizard.gif %{buildroot}%{wizard_icon_file}

# install desktop files
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-key=Version \
  --set-key=Name --set-value="Machinekit" \
  --set-key=Icon --set-value=%{main_icon_file} \
  --set-key=Exec --set-value=%{_bindir}/%{name} \
  --set-key=Keywords --set-value="linuxcnc;cnc;emc" \
  share/applications/linuxcnc.desktop
mv %{buildroot}%{_datadir}/applications/linuxcnc.desktop \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-key=Version \
  --set-key=Icon --set-value=%{wizard_icon_file} \
  --set-key=Keywords --set-value="linuxcnc;cnc;config" \
  debian/extras/usr/share/applications/linuxcnc-pncconf.desktop
mv %{buildroot}%{_datadir}/applications/linuxcnc-pncconf.desktop \
    %{buildroot}%{_datadir}/applications/%{name}-pncconf.desktop

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-key=Version \
  --set-key=Icon --set-value=%{wizard_icon_file} \
  --set-key=Keywords --set-value="linuxcnc;cnc;config" \
  debian/extras/usr/share/applications/linuxcnc-stepconf.desktop
mv %{buildroot}%{_datadir}/applications/linuxcnc-stepconf.desktop \
    %{buildroot}%{_datadir}/applications/%{name}-stepconf.desktop

# collect locale files
%find_lang gmoccapy
%find_lang linuxcnc

# correct tcl/tk installation directory
install -d %{buildroot}%{tcl_sitearch}
mv %{buildroot}%{_prefix}/lib/tcltk/linuxcnc %{buildroot}%{tcl_sitearch}/linuxcnc%{version}
rm -rf %{buildroot}%{_prefix}/lib/tcltk

# install missing python package
install -d %{buildroot}%{python2_sitearch}/yapps
cp -a lib/python/yapps/*.py %{buildroot}%{python2_sitearch}/yapps/


%pre
getent group linuxcnc > /dev/null || %{_sbindir}/groupadd -r linuxcnc
exit 0


%files -f gmoccapy.lang -f linuxcnc.lang
%license COPYING
%dir %{_sysconfdir}/linuxcnc
%config(noreplace) %{_sysconfdir}/linuxcnc/machinekit.ini
%config(noreplace) %{_sysconfdir}/linuxcnc/rtapi.ini
%exclude %{_sysconfdir}/rsyslog.d
%exclude %{_sysconfdir}/security/limits.d/machinekit.conf
%config(noreplace) %{security_conf_file}
%exclude %{_sysconfdir}/udev/rules.d/50-shmdrv.rules
%{_bindir}/5axisgui
%{_bindir}/adxl345
%{_bindir}/axis
%{_bindir}/axis-remote
%{_bindir}/classicladder
%{_bindir}/configserver
%{_bindir}/debuglevel
%{_bindir}/drawbotkins
%exclude %{_bindir}/emcweb
%{_bindir}/encdec
%{_bindir}/g1-to-g23
%{_bindir}/gcode-to-ngc
%{_bindir}/genserkins
%{_bindir}/gladevcp
%{_bindir}/gladevcp_demo
%{_bindir}/gmoccapy
%{_bindir}/gremlin
%{_bindir}/gremlin_view
%{_bindir}/gs2_vfd
%{_bindir}/gscreen
%{_bindir}/halcmd
%{_bindir}/hal_gpio_mcp23017
%{_bindir}/hal-graph
%{_bindir}/hal_input
%{_bindir}/hal_manualtoolchange
%{_bindir}/halmeter
%{_bindir}/hal_pwm_pca9685
%{_bindir}/halrun
%{_bindir}/halsampler
%{_bindir}/halscope
%{_bindir}/halshow
%{_bindir}/hal_storage
%{_bindir}/halstreamer
%{_bindir}/haltalk
%{_bindir}/haltcl
%{_bindir}/hal_temp_ads7828
%{_bindir}/hal_temp_atlas
%{_bindir}/hal_temp_bbb
%{_bindir}/halui
%{_bindir}/hbmgui
%{_bindir}/hexagui
%{_bindir}/hy_vfd
%{_bindir}/image-to-gcode
%{_bindir}/io
%{_bindir}/iov2
%{_bindir}/keystick
%{_bindir}/latency-test
%{_bindir}/linmove
%{_bindir}/lintini
%{_bindir}/linuxcnc
%{_bindir}/linuxcnc_info
%{_bindir}/linuxcnclcd
%{_bindir}/linuxcncmkdesktop
%{_bindir}/linuxcncrsh
%{_bindir}/linuxcncsvr
%{_bindir}/linuxcnctop
%{_bindir}/linuxcnc_var
%{_bindir}/machinekit
%{_bindir}/maho600gui
%{_bindir}/mank
%{_bindir}/max5gui
%{_bindir}/mb2hal
%{_bindir}/mdi
%{_bindir}/milltask
%{_bindir}/mklauncher
%{_bindir}/mksocmemio
%{_bindir}/mkwrapper
%{_bindir}/ngcgui
%{_bindir}/npbdecode
%{_bindir}/pasm
%{_bindir}/pncconf
%{_bindir}/position
%{_bindir}/profile_axis
%{_bindir}/puma560gui
%{_bindir}/pumagui
%{_bindir}/pyngcgui
%{_bindir}/pyvcp
%{_bindir}/pyvcp_demo
%{_bindir}/realtime
%{_bindir}/rostock
%{_bindir}/rs274
%{_bindir}/rtprintf
%{_bindir}/scaragui
%{_bindir}/schedrmt
%{_bindir}/scounter
%{_bindir}/shuttlexpress
%{_bindir}/sim_pin
%{_bindir}/simulate_probe
%{_bindir}/sizes
%{_bindir}/stepconf
%{_bindir}/teach-in
%{_bindir}/tooledit
%{_bindir}/touchy
%{_bindir}/tracking-test
%{_bindir}/unionread
%{_bindir}/vfdb_vfd
%{_bindir}/vfs11_vfd
%{_bindir}/videoserver
%{_bindir}/xhc-hb04
%{_bindir}/xhc-whb04b-6
%{_bindir}/xlinuxcnc
%{python2_sitearch}/*.*
%{python2_sitearch}/drivers
%{python2_sitearch}/fdm
%{python2_sitearch}/gladevcp
%{python2_sitearch}/gmoccapy
%{python2_sitearch}/gscreen
%{python2_sitearch}/machinekit
%{python2_sitearch}/machinetalk
%{python2_sitearch}/rs274
%{python2_sitearch}/stepconf
%{python2_sitearch}/touchy
%{_libdir}/*.so.*
%exclude %{_libdir}/liblinuxcnc.a
%dir %{_libdir}/linuxcnc
%{_libdir}/linuxcnc/*.so
%dir %{_libdir}/linuxcnc/rt-preempt
%{_libdir}/linuxcnc/rt-preempt/*.so
%exclude %{_libexecdir}/linuxcnc/pci_read
%exclude %{_libexecdir}/linuxcnc/pci_write
%dir %{_libexecdir}/linuxcnc
%{_libexecdir}/linuxcnc/flavor
%{_libexecdir}/linuxcnc/inivar
%{_libexecdir}/linuxcnc/rtapi_msgd
%caps(cap_sys_rawio,cap_sys_nice=eip) %{_libexecdir}/linuxcnc/rtapi_app_rt-preempt
%{_datadir}/axis
%exclude %{_datadir}/doc/%{name}/axis_light_background
%{_datadir}/doc/%{name}
%{_datadir}/fdm
%{_datadir}/glade3
%{_datadir}/gmoccapy
%{_datadir}/gscreen
%{_datadir}/gtksourceview-2.0
# we're building without emcweb
%exclude %{_datadir}/linuxcnc/doc-root
%{_datadir}/linuxcnc
%{_datadir}/X11/app-defaults/TkLinuxCNC
%{_datadir}/X11/app-defaults/XEmc
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-pncconf.desktop
%{_datadir}/applications/%{name}-stepconf.desktop
%{main_icon_file}
%{wizard_icon_file}
%{_mandir}/man1/%{name}.1*
%dir %{tcl_sitearch}/linuxcnc%{version}
%{tcl_sitearch}/linuxcnc%{version}/*


%files devel
%{_bindir}/comp
%{_bindir}/instcomp
%{_bindir}/yapps
%{python2_sitearch}/yapps
%{_includedir}/linuxcnc
%{_libdir}/*.so


%changelog
* Wed May 29 2019 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-14.20190528git9021173
- Rebase patches
- Update to the lastest version

* Wed Feb 13 2019 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-13.20190123git1dfa004
- Fix Remove-executable-bit-for-files-without
- Mark patches reported upstream

* Wed Feb 13 2019 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-12.20190123git1dfa004
- Spec cleanup

* Wed Feb 13 2019 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-11.20190123git1dfa004
- Remove ambiguous python shebang for >f30
- Fix mangling shebangs
- Fix configure error when /usr/bin/python is not available

* Tue Feb 12 2019 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-10.20190123git1dfa004
- Fix compilation for f28

* Tue Feb 12 2019 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-9.20190123git1dfa004
- Update to the latest version

* Tue Aug 21 2018 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-8.20180801git308cb1f
- Add missing python3-Cython for >=f29

* Tue Aug 21 2018 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-7.20180801git308cb1f
- Update to the latest version
- Add patches to fix compilation issues

* Wed Oct 11 2017 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-6.20171013git15d5a3f
- Update to the latest version
- Add patch which removes compiler specific options from configure.ac

* Mon Jun 12 2017 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-5.git9c010da
- Update to the latest version

* Fri Feb 24 2017 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-4.git320e76d
- Update to the latest version

* Thu Feb 23 2017 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-3.git0459e8c
- Update to the latest version

* Thu Nov 24 2016 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-2.gitbcb7306
- Spec file cleanup

* Wed Nov 02 2016 Damian Wrobel <dwrobel@ertelnet.rybnik.pl>
- Initial RPM release
