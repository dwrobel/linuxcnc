# rpmbuild parameters:
# --without doc: Do not generate documentation (e.g. too speed up build).
# --nocheck: Do not run tests (e.g. too speed up build).
# --with asan

%{?python_enable_dependency_generator}

%global date 20200507
%global commit0 0a1635d818b0a200aa259392009f84b230153e17
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:          linuxcnc
Version:       2.9.0
Release:       0.17.%{date}git%{shortcommit0}%{?dist}
Summary:       Motion controller for CNC machines and robots
License:       GPLv2+
URL:           http://www.linuxcnc.io/
Source0:       https://github.com/linuxcnc/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{version}-%{date}git%{shortcommit0}.tar.gz
Source1:       %{name}-limits.conf
Patch1:   %{name}-0001-Disable-using-iptables.patch
Patch2:   %{name}-0002-Fix-honoring-C-CXX-CPP-LD-FLAGS-passed-to-the-config.patch
Patch3:   %{name}-0003-Make-sure-all-compilation-honors-CPPFLAGS.patch
Patch4:   %{name}-0004-Fix-linking-error-on-gcc10.patch
Patch5:   %{name}-0005-Remove-duplicate-checking-for-dblatex.patch
Patch6:   %{name}-0006-Fix-configure-integer-expression-expected-error.patch
Patch7:   %{name}-0007-Fix-python3-compatibility-for-persistence.py-popupke.patch

%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}

%global main_icon_file %{_datadir}/icons/hicolor/256x256/apps/%{name}icon.png
%global wizard_icon_file %{_datadir}/icons/hicolor/256x256/apps/%{name}-wizard.png
%global security_conf_file %{_sysconfdir}/security/limits.d/10-linuxcnc.conf

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: /usr/bin/git
BuildRequires: /usr/bin/which
BuildRequires: /usr/bin/intltool-extract
BuildRequires: autoconf
BuildRequires: autoconf-archive
BuildRequires: automake
BuildRequires: openssl-devel
BuildRequires: libusbx-devel
BuildRequires: gtk2-devel
BuildRequires: procps-ng
BuildRequires: psmisc
BuildRequires: compat-readline5-devel
BuildRequires: gettext-devel
# Just for checking sources compatibility with python2
BuildRequires: python2
BuildRequires: python3-devel
BuildRequires: libudev-devel
BuildRequires: avahi-devel
BuildRequires: boost-devel
%if 0%{?fedora} > 28
BuildRequires: boost-python3-devel
%endif
BuildRequires: python3-Yapps2
BuildRequires: kmod
BuildRequires: bwidget
BuildRequires: tkimg
BuildRequires: tclx
BuildRequires: boost-devel
BuildRequires: python3-Cython
BuildRequires: czmq-devel
BuildRequires: jansson-devel
BuildRequires: libmodbus-devel
BuildRequires: libuuid-devel
BuildRequires: libwebsockets-devel
BuildRequires: libtirpc-devel
BuildRequires: tcl-devel
BuildRequires: tk-devel
BuildRequires: python3-tkinter
BuildRequires: uriparser-devel
BuildRequires: mesa-libGLU-devel
BuildRequires: libXmu-devel
BuildRequires: libXaw-devel
BuildRequires: desktop-file-utils
BuildRequires: %{_bindir}/convert
#BuildRequires: libcgroup-devel
# for tests
BuildRequires: /usr/bin/dd
BuildRequires: /usr/bin/nc
%if 0%{!?_without_doc:1}
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

%description

%package uspace
Summary:       Motion controller for CNC machines and robots

Requires:      avahi
Requires:      blt
Requires:      bwidget
Requires:      hicolor-icon-theme
#Requires:      python2-mttkinter
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
Requires:      mesa-libGLU
# for /etc/security/limits.d
Requires:      pam
# for pncconf
Requires:      gnome-python2-gnome
# Disabled as we don't have python2-pyftpdlib on >=F30
## for mkwrapper GUI
#Requires:     python-avahi
#Requires:     pyftpdlib
# for latency-test
#Requires:     python2-tkinter
# for stepconf
Requires:      pygtk2-libglade
# for dir ownership of /etc/linuxcnc/rtapi.conf
Requires:      initscripts

# linuxcnc/axis
Requires:      pango
Requires:      python3-gobject
Requires:      python3-cairo

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


%if 0%{!?_without_doc:1}
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
export CPPFLAGS="-I%{_includedir}/readline5 $(pkg-config --cflags python3)"
export LDFLAGS="-L%{_libdir}/readline5 %{build_ldflags}"

%if 0%{?_with_asan:1}
    export CPPFLAGS="${CPPFLAGS} -fsanitize=undefined -fPIE -fno-omit-frame-pointer"
%endif

autoreconf -fi .
%configure \
    --with-python=/usr/bin/python3 \
    --enable-non-distributable=no \
    --with-boost-python=boost_python$(python3 -c 'import sys; print("{}{}".format(sys.version_info.major,sys.version_info.minor))') \
    --with-realtime=uspace \
    --disable-check-runtime-deps \
    --disable-userspace-pci \
%if 0%{!?_without_doc:1}
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

# install icon files
install -D -m 0644 %{name}icon.png %{buildroot}%{main_icon_file}
convert %{name}-wizard.gif %{buildroot}%{wizard_icon_file}

# install desktop files
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-key=Version \
  --set-key=Name --set-value="LinuxCNC" \
  --set-key=Icon --set-value=%{main_icon_file} \
  --set-key=Exec --set-value=%{_bindir}/%{name} \
  --set-key=Keywords --set-value="linuxcnc;cnc;emc" \
  share/applications/linuxcnc.desktop

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-key=Version \
  --set-key=Icon --set-value=%{wizard_icon_file} \
  --set-key=Keywords --set-value="linuxcnc;cnc;config" \
  debian/extras/usr/share/applications/linuxcnc-pncconf.desktop

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --remove-key=Version \
  --set-key=Icon --set-value=%{wizard_icon_file} \
  --set-key=Keywords --set-value="linuxcnc;cnc;config" \
  debian/extras/usr/share/applications/linuxcnc-stepconf.desktop

# collect locale files
%find_lang gmoccapy
%find_lang linuxcnc

# correct tcl/tk installation directory
install -d %{buildroot}%{tcl_sitearch}
mv %{buildroot}%{_prefix}/lib/tcltk/linuxcnc %{buildroot}%{tcl_sitearch}/linuxcnc%{version}
rm -rf %{buildroot}%{_prefix}/lib/tcltk

# TODO: qtpyvcp is not python3 compatible
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
%{_sysconfdir}/init.d/realtime
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
%{_bindir}/milltask
%{_bindir}/mitsub_vfd
%{_bindir}/monitor-xhc-hb04
%{_bindir}/motion-logger
%{_bindir}/moveoff_gui
%{_bindir}/%{name}
%{_bindir}/ngcgui
%{_bindir}/panelui
%{_bindir}/pmx485
%{_bindir}/pncconf
%{_bindir}/puma560gui
%{_bindir}/pumagui
%{_bindir}/pyngcgui
%{_bindir}/pyui
%{_bindir}/pyvcp
%{_bindir}/pyvcp_demo
%{_bindir}/qtvcp
%{_bindir}/rotarydelta
%{_bindir}/rs274
# TODO % caps(cap_sys_rawio,cap_sys_nice=eip) % {_bindir}/rtapi_app
%attr(4755, root, root) %{_bindir}/rtapi_app
%{_bindir}/scaragui
%{_bindir}/schedrmt
%{_bindir}/scorbot-er-3
%{_bindir}/shuttle
%{_bindir}/sim_pin
%{_bindir}/simulate_probe
%{_bindir}/stepconf
%{_bindir}/svd-ps_vfd
%{_bindir}/teach-in
%{_bindir}/thermistor
%{_bindir}/tooledit
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
%{_prefix}/lib/%{name}/modules/*.so
%{_libdir}/*.so.*
%{_datadir}/axis
%exclude %{_datadir}/doc/%{name}/axis_light_background
%if 0%{!?_without_doc:1}
%exclude %{_datadir}/doc/%{name}/*.pdf
%endif
%exclude %{_datadir}/doc/%{name}/asciidoc-markup.txt
%exclude %{_datadir}/doc/%{name}/tklinuxcnc.txt
%{_datadir}/doc/%{name}
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
%{main_icon_file}
%{wizard_icon_file}
%exclude %{_mandir}/man1/halcompile.1*
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*
%{_mandir}/man9/*.9*
%if 0%{!?_without_doc:1}
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
%if 0%{!?_without_doc:1}
%{_datadir}/doc/linuxcnc/LinuxCNC_Developer_Manual.pdf
%endif
%{_bindir}/halcompile
%dir %{_datadir}/linuxcnc
%{_datadir}/linuxcnc/Makefile.modinc


%if 0%{!?_without_doc:1}
%files doc-en
%{_datadir}/doc/linuxcnc/LinuxCNC_Getting_Started.pdf
%{_datadir}/doc/linuxcnc/LinuxCNC_Manual_Pages.pdf
%{_datadir}/doc/linuxcnc/LinuxCNC_Documentation.pdf
%{_datadir}/doc/linuxcnc/LinuxCNC_Integrator.pdf


%files doc-es
%{_datadir}/doc/linuxcnc/LinuxCNC_Getting_Started_es.pdf
%{_datadir}/doc/linuxcnc/LinuxCNC_Documentation_es.pdf


%files doc-fr
%{_datadir}/doc/linuxcnc/LinuxCNC_Getting_Started_fr.pdf
%{_datadir}/doc/linuxcnc/LinuxCNC_User_Manual_fr.pdf
%{_datadir}/doc/linuxcnc/LinuxCNC_Integrator_Manual_fr.pdf
%{_datadir}/doc/linuxcnc/LinuxCNC_HAL_Manual_fr.pdf
%endif


%changelog
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
