%define enable_xcb 1
# mklibname should handle the special cases of library naming
%define libx11 %mklibname x11_ 6
%define libxorgoldname %mklibname xorg-x11
Name: libx11
Summary: X Library
Version: 1.1.4
Release: %mkrel 4
Group: Development/X11
License: MIT
URL: http://xorg.freedesktop.org
Source0: http://xorg.freedesktop.org/releases/individual/lib/libX11-%{version}.tar.bz2
# the new default unicode compose file is too human-unfriendly; keeping
# the old one...
Source10: X_Compose-en_US.UTF-8
# locale.dir, compose.dir, locale.alias files.
# maintaining them trough patches is a nightmare, as they change
# too much too often; it is easier to manage them separately -- pablo
Source11: X11-compose.dir
Source12: X11-locale.alias
Source13: X11-locale.dir
BuildRoot: %{_tmppath}/%{name}-root
Obsoletes: libxorg-x11
Provides: libxorg-x11

BuildRequires: x11-util-macros		>= 1.1.5
BuildRequires: x11-xtrans-devel		>= 1.0.4
BuildRequires: libxdmcp-devel		>= 1.0.2
BuildRequires: libxau-devel		>= 1.0.3
BuildRequires: x11-proto-devel		>= 7.3

# Some cherry picks of commits after libX11-1.1.4 tag
Patch1: 0001-Fix-fd.o-bug-15023-make-Xlib-sync-correctly-given-m.patch
Patch2: 0002-Bug-15884-Remove-useless-sleep-s-from-the-connec.patch
Patch3: 0003-Fix-missing-error-condition.patch
Patch4: 0004-added-error-check-in-Xcms-color-file-parser-closes.patch

# because of %{_datadir/X11} being owned by x11-server-common
Requires(pre): x11-server-common >= 1.4.0.90-13mdv

%if %{enable_xcb}
BuildRequires: libxcb-devel
%endif

%description
%{name} contains the shared libraries that most X programs
need to run properly. These shared libraries are in a separate package in
order to reduce the disk space needed to run X applications on a machine
without an X server (i.e, over a network).

#-----------------------------------------------------------

%package -n %{libx11}
Summary: X Library
Group: Development/X11
Conflicts: %{libxorgoldname} < 7.0
Provides: %{name} = %{version}
Requires(post): grep
Requires(postun): grep coreutils

%description -n %{libx11}
%{name} contains the shared libraries that most X programs
need to run properly. These shared libraries are in a separate package in
order to reduce the disk space needed to run X applications on a machine
without an X server (i.e, over a network).

%post -n %{libx11}
if  grep -q "^%{_prefix}/X11R6/lib$" /etc/ld.so.conf; then
    grep -v "^%{_prefix}/X11R6/lib$" /etc/ld.so.conf > /etc/ld.so.conf.new
    mv -f /etc/ld.so.conf.new /etc/ld.so.conf
    /sbin/ldconfig
fi

%postun -n %{libx11}
if [ "$1" = "0" -a `grep "^%{_prefix}/X11R6/lib$" /etc/ld.so.conf` != "" ]; then
    grep -v "^%{_prefix}/X11R6/lib$" /etc/ld.so.conf > /etc/ld.so.conf.new
    mv -f /etc/ld.so.conf.new /etc/ld.so.conf
    /sbin/ldconfig
fi

#-----------------------------------------------------------

%package -n %{libx11}-devel
Summary: Development files for %{name}
Group: Development/X11
Requires: %{libx11} = %{version}
Requires: x11-proto-devel >= 1.0.0
Provides: libx11-devel = %{version}-%{release}
Conflicts: %{libxorgoldname}-devel < 7.0

%description -n %{libx11}-devel
%{name} includes the libraries, header files and documentation
you'll need to develop programs which run in X clients. X11 includes
the base Xlib library as well as the Xt and Xaw widget sets.

For guidance on programming with these libraries, O'Reilly & Associates
produces a series on X programming which you might find useful.

Install %{name} if you are going to develop programs which
will run as X clients.

%pre -n %{libx11}-devel
if [ -h %{_includedir}/X11 ]; then
	rm -f %{_includedir}/X11
fi

%files -n %{libx11}-devel
%defattr(-,root,root)
%{_mandir}/man3/*.3.*
%{_libdir}/libX11.so
%{_libdir}/libX11.la
%{_libdir}/pkgconfig/x11.pc
%{_includedir}/X11/cursorfont.h
%{_includedir}/X11/ImUtil.h
%{_includedir}/X11/Xlocale.h
%{_includedir}/X11/Xcms.h
%{_includedir}/X11/Xlibint.h
%{_includedir}/X11/Xlib.h
%{_includedir}/X11/Xresource.h
%{_includedir}/X11/Xregion.h
%{_includedir}/X11/Xutil.h
%{_includedir}/X11/XlibConf.h
%{_includedir}/X11/XKBlib.h
%if %enable_xcb
%{_libdir}/libX11-xcb.so
%{_libdir}/libX11-xcb.la
%{_libdir}/pkgconfig/x11-xcb.pc
%{_includedir}/X11/Xlib-xcb.h
%endif

#-----------------------------------------------------------

%package -n %{libx11}-static-devel
Summary: Static development files for %{name}
Group: Development/X11
Requires: %{libx11}-devel = %{version}
Conflicts: %{libxorgoldname}-static-devel < 7.0
Provides: libx11-static-devel = %{version}-%{release}

%description -n %{libx11}-static-devel
Static development files for %{name}

%files -n %{libx11}-static-devel
%defattr(-,root,root)
%{_libdir}/libX11.a
%if %enable_xcb
%{_libdir}/libX11-xcb.a
%endif

#-----------------------------------------------------------

%package common
Summary: Common files used by the X.org
Group: System/X11

%description common
Common files used by the X.org

%files common
%defattr(-,root,root)
%dir %{_datadir}/X11/locale
%{_datadir}/X11/locale/*
%{_libdir}/X11/Xcms.txt
%{_datadir}/X11/XErrorDB
%{_datadir}/X11/XKeysymDB

#-----------------------------------------------------------

%prep
%setup -q -n libX11-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# backup the original files (so we can look at them later) and use our own
cp nls/compose.dir.pre nls/compose.dir.orig
cp nls/locale.alias.pre nls/locale.alias.orig
cp nls/locale.dir.pre nls/locale.dir.orig
cp nls/en_US.UTF-8/Compose.pre nls/en_US.UTF-8/Compose.orig
cat %{SOURCE10} | sed 's/#/XCOMM/' > nls/en_US.UTF-8/Compose.pre
cat %{SOURCE11} | sed 's/#/XCOMM/' > nls/compose.dir.pre
cat %{SOURCE12} | sed 's/#/XCOMM/' > nls/locale.alias.pre
cat %{SOURCE13} | sed 's/#/XCOMM/' > nls/locale.dir.pre

%build
CFLAGS="-O0 -g3" \
%configure2_5x \
		%if %enable_xcb
		--with-xcb
		%else
		--without-xcb
		%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%files -n %{libx11}
%defattr(-,root,root)
%{_libdir}/libX11.so.6
%{_libdir}/libX11.so.6.2.0
%if %enable_xcb
%{_libdir}/libX11-xcb.so.1
%{_libdir}/libX11-xcb.so.1.0.0
%endif
