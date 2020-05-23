# rpmbuild parameters:
# --without doc: Do not generate documentation (e.g. too speed up build).
# --nocheck: Do not run tests (e.g. too speed up build).
# --with asan

%if 0%{?rhel}
#TODO: temporarly disabled as it fails due to:
# - https://bugzilla.redhat.com/1833047
# - https://bugzilla.redhat.com/1833095
%bcond_with doc
%else
%bcond_without doc
%endif

%{?python_enable_dependency_generator}

%global date 20211119
%global commit0 a8ced9b0b120228875b5bb016db01ab228019351
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:          linuxcnc
Version:       2.9.0
Release:       0.56.%{date}git%{shortcommit0}%{?dist}
Summary:       Motion controller for CNC machines and robots
License:       GPLv2+
URL:           http://www.linuxcnc.io/
Source0:       https://github.com/linuxcnc/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{version}-%{date}git%{shortcommit0}.tar.gz
Source1:       %{name}-limits.conf
Patch1:   %{name}-0001-Fix-realtime-linuxcnc-script-installation.patch
Patch2:   %{name}-0002-Add-support-for-checking-text-x-script.python-in-pyc.patch
Patch3:   %{name}-0003-Disable-checking-version-for-python-development-pack.patch
Patch4:   %{name}-0004-Allow-to-overwrite-default-CXXFLAGS-no-psabi-std-gnu.patch
Patch5:   %{name}-0005-Make-sure-all-compilations-honors-CPPFLAGS.patch
Patch6:   %{name}-0006-Use-TEMP_FAILURE_RETRY-to-handle-EINTR-properly.patch
Patch7:   %{name}-0007-Remove-unused-thread_lock.patch
Patch8:   %{name}-0008-Unify-FIFO_SCHED-between-root-and-non-root-user.patch
Patch9:   %{name}-0009-Always-report-realtime-from-rtapi_is_realtime.patch
Patch10:   %{name}-0010-Disable-using-iptables-work-in-progress.patch
Patch11:   %{name}-0011-rootless-incr_io_usage.patch
Patch12:   %{name}-0012-rootless-incr_mem_usage.patch
Patch13:   %{name}-0013-Remove-direct-usage-of-inb-outb.patch
Patch14:   %{name}-0014-Add-halgraph.patch

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}

%global the_icon_file %{_datadir}/icons/hicolor/scalable/apps/linuxcncicon.svg
%global security_conf_file %{_sysconfdir}/security/limits.d/10-linuxcnc.conf

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: %{_bindir}/git
BuildRequires: %{_bindir}/which
BuildRequires: %{_bindir}/intltool-extract
BuildRequires: autoconf
##BuildRequires: autoconf-archive
BuildRequires: automake
BuildRequires: openssl-devel
BuildRequires: libusbx-devel
BuildRequires: gtk2-devel
BuildRequires: gtk3-devel
BuildRequires: procps-ng
BuildRequires: psmisc
BuildRequires: compat-readline5-devel
BuildRequires: gettext-devel
BuildRequires: python3-devel
BuildRequires: libudev-devel
##BuildRequires: avahi-devel
BuildRequires: boost-devel
BuildRequires: boost-python3-devel
BuildRequires: python3-Yapps2
BuildRequires: kmod
BuildRequires: bwidget
BuildRequires: tkimg
BuildRequires: tclx
BuildRequires: boost-devel
##BuildRequires: python3-Cython
##BuildRequires: czmq-devel
BuildRequires: libmodbus-devel
BuildRequires: libuuid-devel
BuildRequires: libtirpc-devel
BuildRequires: tcl-devel
BuildRequires: tk-devel
BuildRequires: python3-tkinter
BuildRequires: mesa-libGLU-devel
BuildRequires: libXmu-devel
BuildRequires: libXaw-devel
BuildRequires: desktop-file-utils
BuildRequires: python3-configobj
#BuildRequires: libcgroup-devel
# for tests
BuildRequires: %{_bindir}/dd
BuildRequires: %{_bindir}/nc
%if %{with doc}
# Documentation dependencies
# based on debian/configure DOC_DEPENDS=
BuildRequires: asciidoc
BuildRequires: dblatex >= 0.2.12
BuildRequires: texlive-latex-uni8
BuildRequires: texlive-fancybox
BuildRequires: asciidoc >= 8.5
BuildRequires: docbook-xsl
BuildRequires: dvipng
BuildRequires: ghostscript
BuildRequires: graphviz
BuildRequires: groff
BuildRequires: GraphicsMagick
BuildRequires: inkscape
BuildRequires: /usr/bin/rsvg-convert
BuildRequires: %{_bindir}/convert
# inkscape dependency
BuildRequires: libcanberra-gtk3
BuildRequires: PackageKit-gtk3-module
BuildRequires: python-lxml
BuildRequires: source-highlight
BuildRequires: texlive-collection-binextra
BuildRequires: texlive-collection-fontutils
BuildRequires: texlive-ifxetex
BuildRequires: texlive-collection-fontsrecommended
BuildRequires: texlive-cyrillic
BuildRequires: texlive-babel-french
BuildRequires: texlive-babel-german
BuildRequires: texlive-babel-polish
BuildRequires: texlive-german
BuildRequires: texlive-polski
BuildRequires: texlive-babel-spanish texlive-hyphen-spanish
BuildRequires: texlive-collection-latexrecommended
BuildRequires: libxslt
BuildRequires: asciidoc-latex
BuildRequires: texlive-multirow
# for html documentation
BuildRequires: linkchecker
%endif
%if 0%{?_with_asan:1}
BuildRequires: libasan
BuildRequires: libtsan
%endif


%description

%package uspace
Summary:       Motion controller for CNC machines and robots

Requires:      avahi
Requires:      blt
Requires:      bwidget
Requires:      hicolor-icon-theme
#Requires:      python2-mttkinter
Requires:      tkimg
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
Requires:      mesa-libGLU
Requires:      python3dist(pyopengl)
Requires:      python3dist(python-xlib)
# Requires:    pygtkglext
# Requires:    pygtksourceview
# Requires:    python2-xlib
# Editing GladeVCP .glade files
# Requires:    glade3
# plasmac
# Requires:    python2-configobj
# for /etc/security/limits.d
Requires:      pam
# for pncconf
#Requires:      gnome-python2-gnome
# Disabled as we don't have python2-pyftpdlib on >=F30
## for mkwrapper GUI
#Requires:     python-avahi
#Requires:     pyftpdlib
# for latency-test
#Requires:     python2-tkinter
# for stepconf
#Requires:      pygtk2-libglade
# for dir ownership of /etc/linuxcnc/rtapi.conf
Requires:      initscripts

# linuxcnc/axis
Requires:      pango
Requires:      python3-gobject
Requires:      python3-cairo
# halreport
Requires:      redhat-lsb-core

Recommends:    kernel-rt
Recommends:    tuned-profiles-realtime

Obsoletes:     machinekit <= 0.1


%description uspace
LinuxCNC is a motion controller for CNC machines and robots.
LinuxCNC is the next-generation Enhanced Machine Controller which
provides motion control for CNC machine tools and robotic
applications (milling, cutting, routing, etc.).


%package uspace-devel
Summary: Devel package for %{name}-uspace
Requires: %{name}-uspace = %{version}


%description uspace-devel
This package includes files needed to build new realtime components and
alternate front-ends for linuxcnc


%if %{with doc}
%package doc-en
BuildArch: noarch
Summary: English documentation for %{name}
Requires: %{name}-uspace = %{version}


%description doc-en
Description: Motion controller for CNC machines and robots (English documentation)
LinuxCNC is the next-generation Enhanced Machine Controller which
provides motion control for CNC machine tools and robotic
applications (milling, cutting, routing, etc.).
This package contains the documentation in Enghish.

%package doc-es
BuildArch: noarch
Summary: Spanish documentation for %{name}
Requires: %{name}-uspace = %{version}


%description doc-es
Description: Motion controller for CNC machines and robots (Spanish documentation)
LinuxCNC is the next-generation Enhanced Machine Controller which
provides motion control for CNC machine tools and robotic
applications (milling, cutting, routing, etc.).
This package contains the documentation in Spanish.

%package doc-fr
BuildArch: noarch
Summary: French documentation for %{name}
Requires: %{name}-uspace = %{version}


%description doc-fr
Description: Motion controller for CNC machines and robots (French documentation)
LinuxCNC is the next-generation Enhanced Machine Controller which
provides motion control for CNC machine tools and robotic
applications (milling, cutting, routing, etc.).
This package contains the documentation in French.
%endif


%prep
%autosetup -S git -n %{name}-%{commit0}
echo "%{version}-%{release}" >VERSION

pushd src
sed -i -e 's#\(EMC2_TCL_DIR=\)${prefix}/lib/tcltk/linuxcnc#\1%{tcl_sitearch}/linuxcnc%{version}#g' \
       -e 's#\(EMC2_TCL_LIB_DIR=\)${prefix}/lib/tcltk/linuxcnc#\1%{tcl_sitearch}/linuxcnc%{version}#g' \
       -e 's#\(EMC2_LANG_DIR=\)${prefix}/share/linuxcnc/tcl/msgs#\1%{tcl_sitearch}/linuxcnc/tcl/msgs#g' \
       -e 's#\(EMC2_RTLIB_DIR=\)${prefix}/lib/linuxcnc#\1%{_libdir}/linuxcnc#g' \
       configure.ac

# Allows to compile against compat-readline5
export CPPFLAGS="-I%{_includedir}/readline5"
export LDFLAGS="-L%{_libdir}/readline5 %{build_ldflags}"

%if 0%{?_with_asan:1}
    export CPPFLAGS="${CPPFLAGS} -fsanitize=undefined -fPIE -fno-omit-frame-pointer"
%endif

autoreconf -fi .
%configure \
    --with-python=%{__python3} \
    --enable-non-distributable=no \
    --with-boost-python=boost_python%{python3_version_nodots} \
    --with-realtime=uspace \
    --disable-check-runtime-deps \
    --disable-userspace-pci \
%if %{with doc}
    --enable-build-documentation=pdf \
%endif

popd

sed -i 's#lib/tcltk/linuxcnc#%{tcl_sitearch}/linuxcnc%{version}#g' \
    lib/python/rs274/options.py


%build
%{make_build} -C src V=1


%install
%{make_install} -C src V=1 \
    DESTDIR=%{buildroot} \
    DIR="install -d -m 0755" \
    EXE="install -m 0755" \
    FILE="install -m 0644" \
    SETUID="install -m 0755"

# remove static library
rm -f %{buildroot}%{_libdir}/liblinuxcnc.a

# install limits configuration
install -m 0644 -D %{SOURCE1} %{buildroot}%{security_conf_file}

# move X11 app-defaults to the correct location
mv %{buildroot}%{_sysconfdir}/X11 %{buildroot}%{_datadir}/

# remove duplicated .so files
rm -f %{buildroot}%{_libdir}/{compat.so,hal.so,rtapi.so,shmcommon.so}

# make .so files executable
find %{buildroot}%{_libdir} -type f -name '*.so*' -exec chmod 0755 {} \;

# install icon file
install -p -D -m 0644 \
    debian/extras/usr/share/icons/hicolor/scalable/apps/linuxcncicon.svg \
    %{buildroot}%{the_icon_file}

install -p -D -m 0644 docs/html/gcode.html \
    %{buildroot}%{_datadir}/doc/%{name}/gcode.html
install -p -D -m 0644 docs/html/gcode_fr.html \
    %{buildroot}%{_datadir}/doc/%{name}/gcode_fr.html

# install desktop files
for app in debian/extras/usr/share/applications/*.desktop; do
    desktop-file-install \
      --dir %{buildroot}%{_datadir}/applications \
      ${app}
done

# It's just one file (alongside with gcoderef-fi.html) for which
# we do not provide sub-package
rm -f %{buildroot}%{_datadir}/applications/linuxcnc-gcoderef-vi.desktop


# collect locale files
%find_lang gmoccapy
%find_lang linuxcnc

# correct tcl/tk installation directory
install -d %{buildroot}%{tcl_sitearch}
mv %{buildroot}%{_prefix}/lib/tcltk/linuxcnc %{buildroot}%{tcl_sitearch}/linuxcnc%{version}
rm -rf %{buildroot}%{_prefix}/lib/tcltk

# TODO: qtpyvcp is not python3 compatible yet
# https://github.com/LinuxCNC/linuxcnc/issues/819
rm -rf %{buildroot}%{python3_sitelib}/qtvcp


%check
%{make_build} -C src pycheck V=1
#TODO run tests
#source ./scripts/rip-environment
#./scripts/runtests tests/


%pre
getent group linuxcnc > /dev/null || %{_sbindir}/groupadd -r linuxcnc
exit 0


%files uspace -f gmoccapy.lang -f linuxcnc.lang
%license COPYING COPYING.more
%{_sysconfdir}/linuxcnc/rtapi.conf
%config(noreplace) %{security_conf_file}
%{_bindir}/5axisgui
%{_bindir}/axis
%{_bindir}/axis-remote
%{_bindir}/classicladder
%{_bindir}/debuglevel
%{_bindir}/elbpcom
%{_bindir}/genserkins
%{_bindir}/gladevcp
%{_bindir}/gladevcp_demo
%{_bindir}/gmoccapy
%{_bindir}/gremlin_view
%{_bindir}/gs2_vfd
%{_bindir}/gscreen
%{_bindir}/halcmd
%{_bindir}/halcmd_twopass
%{_bindir}/halcompile
%{_bindir}/hal-histogram
%{_bindir}/hal_input
%{_bindir}/hal_manualtoolchange
%{_bindir}/halmeter
%{_bindir}/halreport
%{_bindir}/halrmt
%{_bindir}/halrun
%{_bindir}/halsampler
%{_bindir}/halscope
%{_bindir}/halshow
%{_bindir}/halstreamer
%{_bindir}/haltcl
%{_bindir}/halui
%{_bindir}/hbmgui
%{_bindir}/hexagui
%{_bindir}/hy_gt_vfd
%{_bindir}/hy_vfd
%{_bindir}/image-to-gcode
%{_bindir}/inivar
%{_bindir}/io
%{_bindir}/iov2
%{_bindir}/latency-histogram
%{_bindir}/latency-plot
%{_bindir}/latency-test
%{_bindir}/lineardelta
%{_bindir}/linuxcnc_info
%{_bindir}/linuxcnclcd
%{_bindir}/linuxcncmkdesktop
%{_bindir}/linuxcnc_module_helper
%{_bindir}/linuxcncrsh
%{_bindir}/linuxcncsvr
%{_bindir}/linuxcnctop
%{_bindir}/linuxcnc_var
%{_bindir}/maho600gui
%{_bindir}/max5gui
%{_bindir}/mb2hal
%{_bindir}/mdi
%{_bindir}/melfagui
%{_bindir}/milltask
%{_bindir}/millturngui
%{_bindir}/mitsub_vfd
%{_bindir}/monitor-xhc-hb04
%{_bindir}/motion-logger
%{_bindir}/moveoff_gui
%{_bindir}/%{name}
%{_bindir}/ngcgui
%{_bindir}/panelui
%{_bindir}/pi500_vfd
%{_bindir}/pmx485
%{_bindir}/pmx485-test
%{_bindir}/pncconf
%{_bindir}/puma560gui
%{_bindir}/pumagui
%{_bindir}/pyngcgui
%{_bindir}/pyui
%{_bindir}/pyvcp
%{_bindir}/pyvcp_demo
%{_bindir}/qtplasmac-cfg2prefs
%{_bindir}/qtplasmac-materials
%{_bindir}/qtplasmac-plasmac2qt
%{_bindir}/qtplasmac-setup
%{_bindir}/qtvcp
%{_bindir}/rotarydelta
%{_bindir}/rs274
%caps(cap_ipc_lock,cap_net_admin,cap_sys_rawio,cap_sys_nice+ep) %{_bindir}/rtapi_app
%{_bindir}/scaragui
%{_bindir}/schedrmt
%{_bindir}/scorbot-er-3
%{_bindir}/sendkeys
%{_bindir}/shuttle
%{_bindir}/sim_pin
%{_bindir}/simulate_probe
%{_bindir}/stepconf
%{_bindir}/svd-ps_vfd
%{_bindir}/teach-in
%{_bindir}/thermistor
%{_bindir}/tooledit
%{_bindir}/tool_mmap_read
%{_bindir}/tool_watch
%{_bindir}/touchy
%{_bindir}/update_ini
%{_bindir}/vfdb_vfd
%{_bindir}/vfs11_vfd
%{_bindir}/wj200_vfd
%{_bindir}/xhc-hb04
%{_bindir}/xhc-whb04b-6
%{_bindir}/xhc-hb04-accels
%{_bindir}/xyzac-trt-gui
%{_bindir}/xyzbc-trt-gui
%dir %{_prefix}/lib/%{name}
%dir %{_prefix}/lib/%{name}/modules
%{_prefix}/lib/%{name}/realtime
%{_prefix}/lib/%{name}/modules/*.so
%{_libdir}/*.so.*
%{_datadir}/axis
%{_datadir}/glade3
%{_datadir}/gmoccapy
%{_datadir}/gscreen
%{_datadir}/gtksourceview-2.0
%dir %{_datadir}/qtvcp
%{_datadir}/qtvcp/*
%{_datadir}/linuxcnc
%{_datadir}/X11/app-defaults/TkLinuxCNC
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-pncconf.desktop
%{_datadir}/applications/%{name}-stepconf.desktop
%{_datadir}/applications/%{name}-latency.desktop

%exclude %{_datadir}/doc/%{name}/axis_light_background

%if %{with doc}
%exclude %{_datadir}/doc/%{name}/*.pdf
%endif
%exclude %{_datadir}/doc/linuxcnc/gcode.html
%exclude %{_datadir}/doc/linuxcnc/gcode_fr.html
%exclude %{_datadir}/applications/linuxcnc-documentation.desktop
%exclude %{_datadir}/applications/linuxcnc-documentation_es.desktop
%exclude %{_datadir}/applications/linuxcnc-gcoderef.desktop
%exclude %{_datadir}/applications/linuxcnc-gcoderef_es.desktop
%exclude %{_datadir}/applications/linuxcnc-gcoderef_fr.desktop
%exclude %{_datadir}/applications/linuxcnc-gettingstarted_es.desktop
%exclude %{_datadir}/applications/linuxcnc-gettingstarted_fr.desktop
%exclude %{_datadir}/applications/linuxcnc-gettingstarted.desktop
%exclude %{_datadir}/applications/linuxcnc-halmanual_fr.desktop
%exclude %{_datadir}/applications/linuxcnc-integratorinfo.desktop
%exclude %{_datadir}/applications/linuxcnc-integratormanual_fr.desktop
%exclude %{_datadir}/applications/linuxcnc-manualpages.desktop
%exclude %{_datadir}/applications/linuxcnc-usermanual_fr.desktop
%exclude %{_datadir}/applications/linuxcnc-gettingstarted_cn.desktop
%exclude %{_datadir}/applications/linuxcnc-gcoderef_vi.desktop
%{_datadir}/doc/%{name}


%{the_icon_file}
%exclude %{_mandir}/man1/halcompile.1*
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_mandir}/man9/*.9*
%if %{with doc}
%exclude %{_datadir}/doc/linuxcnc/LinuxCNC_Developer_Manual.pdf
%endif
%{python3_sitelib}/*
%dir %{tcl_sitearch}/linuxcnc%{version}
%{tcl_sitearch}/linuxcnc%{version}/*


%files uspace-devel
%dir %{_includedir}/linuxcnc
%{_includedir}/linuxcnc/*.h
%{_includedir}/linuxcnc/*.hh
%{_libdir}/*.so
%{_mandir}/man1/halcompile.1*
%if %{with doc}
%{_datadir}/doc/linuxcnc/LinuxCNC_Developer_Manual.pdf
%endif
%{_bindir}/halcompile
%dir %{_datadir}/linuxcnc
%{_datadir}/linuxcnc/Makefile.modinc


%if %{with doc}
%files doc-en
%{_datadir}/doc/linuxcnc/gcode.html
%{_datadir}/applications/linuxcnc-gcoderef.desktop

%{_datadir}/doc/linuxcnc/LinuxCNC_Getting_Started.pdf
%{_datadir}/applications/linuxcnc-gettingstarted.desktop

%{_datadir}/doc/linuxcnc/LinuxCNC_Manual_Pages.pdf
%{_datadir}/applications/linuxcnc-manualpages.desktop

%{_datadir}/doc/linuxcnc/LinuxCNC_Documentation.pdf
%{_datadir}/applications/linuxcnc-documentation.desktop

%{_datadir}/doc/linuxcnc/LinuxCNC_Integrator.pdf
%{_datadir}/applications/linuxcnc-integratorinfo.desktop


%files doc-es
%{_datadir}/applications/linuxcnc-documentation_es.desktop
%{_datadir}/doc/linuxcnc/LinuxCNC_Getting_Started_es.pdf
%{_datadir}/applications/linuxcnc-gettingstarted_es.desktop
%{_datadir}/doc/linuxcnc/LinuxCNC_Documentation_es.pdf
%{_datadir}/applications/linuxcnc-gcoderef_es.desktop


%files doc-fr
%{_datadir}/doc/linuxcnc/gcode_fr.html
%{_datadir}/applications/linuxcnc-gcoderef_fr.desktop

%{_datadir}/doc/linuxcnc/LinuxCNC_Getting_Started_fr.pdf
%{_datadir}/applications/linuxcnc-gettingstarted_fr.desktop

%{_datadir}/doc/linuxcnc/LinuxCNC_User_Manual_fr.pdf
%{_datadir}/applications/linuxcnc-usermanual_fr.desktop

%{_datadir}/doc/linuxcnc/LinuxCNC_Integrator_Manual_fr.pdf
%{_datadir}/applications/linuxcnc-integratormanual_fr.desktop

%{_datadir}/doc/linuxcnc/LinuxCNC_HAL_Manual_fr.pdf
%{_datadir}/applications/linuxcnc-halmanual_fr.desktop
%endif


%changelog
* Fri Nov 19 2021 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.56.20211119gita8ced9b
- Update to the latest version
- Fix Require: python-xlib

* Fri Nov 19 2021 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.55.20211111git358a08f
- Recommends: kernel-rt, tuned-profiles-realtime
- Fix halgraph for python3
- Improve disabling iptables

* Fri Nov 19 2021 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.54.20211111git358a08f
- Add Requires for Xlib

* Thu Nov 18 2021 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.53.20211111git358a08f
- Add patch to fix lib/linuxcnc directory creation

* Thu Nov 18 2021 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.52.20211111git358a08f
- Add patch to fix location of realtime script

* Thu Nov 18 2021 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.51.20211111git358a08f
- Adjust Requires for centos-9-stream

* Thu Nov 18 2021 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.50.20211111git358a08f
- Adjust BR for centos-9-stream

* Thu Nov 11 2021 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.49.20211111git358a08f
- Update to the latest version
- Add patch to fix pycheck on Fedora >= 35
- Add patch to fix build error

* Wed Nov 10 2021 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.48.20211110git39d6366
- Update to the latest version
- Add patch to disable checking python devel package

* Tue Nov 09 2021 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.47.20211109git2c29020
- Update to the latest version

* Fri Oct 29 2021 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.46.20211029git05e7e47
- Update to the latest version
- Add patch to support python 3.10 in Fedora >=35

* Thu Oct 28 2021 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.45.20211027git1b9335f
- Fix BuildRequires

* Wed Oct 27 2021 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.44.20211027git1b9335f
- Update to the latest version

* Tue Aug 04 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.43.20200804git03ab5e6
- Update to the latest version

* Mon Jul 27 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.42.20200726git9b27ae3
- Update to the latest version

* Mon Jul 20 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.41.20200719git70c0db7
- Update to the latest version

* Wed Jul 15 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.40.20200715gita695f97
- Update to the latest version
- Drop patches upstream merged

* Mon Jul 13 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.39.20200713git613fc12
- Update to the latest version

* Thu Jul 09 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.38.20200709git774cc04
- Update to the latest version
- Drop patches upstream merged

* Mon Jul 06 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.37.20200705gitf423d30
- Update to the latest version

* Sun Jun 28 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.36.20200628gitf414ce9
- Update to the latest version
- Drop patches upstream merged

* Tue Jun 23 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.35.20200614gitcda96a4

* Mon Jun 15 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.34.20200614gitcda96a4
- Update to the latest version

* Mon Jun 08 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.33.20200608gitcc3a802
- Update to the latest version
- Drop patches upstream merged

* Fri Jun 05 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.32.20200530gitade0933
- Update to the latest version
- Drop patches upstream merged

* Sat May 30 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.31.20200530gitade0933

* Mon May 25 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.30.20200524gitdeddd4e
- Update to the latest version
- Switch to use capabilities

* Mon May 18 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.29.20200517git946aab6
- Update to the latest version
- Drop patches upstream merged

* Fri May 15 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.28.20200514git1d13406
- Add vectorized logo

* Thu May 14 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.27.20200514git1d13406
- Update to the latest version

* Thu May 14 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.26.20200513gitb5bdced
- Improve searching for LinuxCNC in GNOME

* Thu May 14 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.25.20200513gitb5bdced
- Improve searching for LinuxCNC in GNOME

* Wed May 13 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.24.20200512git7e15aa2
- Update to the latest version
- Drop patches upstream merged

* Tue May 12 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.23.20200512git402f37c
- Update to the latest version
- Drop patches upstream merged

* Mon May 11 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.22.20200511git21107ad
- Update to the latest version
- Drop patches upstream merged

* Mon May 11 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.21.20200511git21107ad

* Fri May 08 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.20.20200508gitf54b252
- Update to the latest version

* Fri May 08 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.19.20200508git1a8e686
- Update to the latest version
- Drop patches upstream merged

* Thu May 07 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.18.20200507git6dc7ceb
- Update to the latest version
- Drop patches upstream merged

* Wed May 06 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.17.20200507git0a1635d
- Update to the latest version
- Drop patches upstream merged

* Tue May 05 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.16.20200505gita28d412
- Enable building documentation
- Drop patches upstream merged

* Tue May 05 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.15.20200505gita28d412
- Update to the latest version

* Sun May 03 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.14.20200428git1ebe739
- Update to the latest version

* Tue Apr 28 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.12.20200428git1ebe739
- Update to the latest version

* Mon Apr 27 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.11.20200427git0c5769a
- Update to the latest version

* Sun Apr 26 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.8.20200425git1312cfa
- Update to the latest version

* Sat Apr 25 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.7.20200425git01d9048
- Update to the latest version

* Thu Apr 23 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.6.20200423git759ec2d
- Update to the latest version

* Tue Apr 21 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.5.20200421gitd4d1e02
- Update to the latest version
- Drop patches upstream merged

* Mon Apr 20 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.4.20200420git0558a25
- Update to the latest version
- Drop patches upstream merged

* Wed Apr 15 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.3.20200415git093b3b0
- Update to the latest version
- Create documentation sub-packages

* Tue Apr 14 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.2.20200414git21d7a94
- Update to the latest version
- Drop patches upstream merged

* Fri Apr 10 2020 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 2.9.0-0.1.20200412git5a8a9e2
- linuxcnc first version

* Sun Jun 02 2019 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-16.20190528git9021173
- Add patch to fix newthread cpu=
- Increase memlock to 256M

* Wed May 29 2019 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-15.20190528git9021173
- Update requires for latency-test

* Wed May 29 2019 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-14.20190528git9021173
- Rebase patches
- Disable mkwrapper due to lack of python2-pyftpdlib on >=f30
- Fix linking issues with tclstub
- Update to the lastest version

* Wed Feb 13 2019 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-13.20190123git1dfa004
- Fix Remove-executable-bit-for-files-without
- Mark patches reported upstream

* Wed Feb 13 2019 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-12.20190123git1dfa004
- Spec cleanup

* Wed Feb 13 2019 Damian Wrobel <dwrobel@ertelnet.rybnik.pl> - 0.1-11.20190123git1dfa004
- Remove ambiguous python shebang for >f30
- Fix mangling shebangs
- Fix configure error when %{_bindir}/python is not available

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
