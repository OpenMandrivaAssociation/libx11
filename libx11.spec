%define major 6
%define xcbmaj 1
%define libname %mklibname x11_ %{major}
%define libxcb %mklibname x11-xcb %{xcbmaj}
%define devname %mklibname x11 -d

# Disabling LTO is a workaround for 32-bit gcc.
# No harm done because LTO is enabled manually for
# the 64-bit build.
%global _disable_lto 1
%global optflags %{optflags} -O3

# libx11 is used by wine and steam
%ifarch %{x86_64}
%bcond_without compat32
%else
%bcond_with compat32
%endif
%if %{with compat32}
%define lib32name libx11_%{major}
%define lib32xcb libx11-xcb%{xcbmaj}
%define dev32name libx11-devel
%endif

Summary:	X Library
Name:		libx11
Version:	1.6.9
Release:	3
Group:		System/Libraries
License:	MIT
Url:		http://xorg.freedesktop.org
Source0:	http://xorg.freedesktop.org/releases/individual/lib/libX11-%{version}.tar.bz2
Patch0:		libX11-1.3.5-fix-null-pointer.patch
Patch1:		libx11-fix-segfault.diff
BuildRequires:	docbook-dtd43-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	groff
BuildRequires:	x11-sgml-doctools
BuildRequires:	xmlto
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xdmcp)
BuildRequires:	pkgconfig(xorg-macros)
BuildRequires:	pkgconfig(xproto)
BuildRequires:	pkgconfig(xtrans)
%if %{with compat32}
BuildRequires:	devel(libXau)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libXdmcp)
%endif

%description
%{name} contains the shared libraries that most X programs
need to run properly. These shared libraries are in a separate package in
order to reduce the disk space needed to run X applications on a machine
without an X server (i.e, over a network).

%package common
Summary:	Common files used by the X.org
Group:		System/X11
BuildArch:	noarch
# because of _datadir/X11 being owned by x11-server-common
Requires(pre):	x11-server-common >= 1.4.0.90-13

%description common
Common files used by the X.org.

%package -n %{libname}
Summary:	X Library
Group:		Development/X11
Provides:	%{name} = %{EVRD}

%description -n %{libname}
This package contains a shared library for %{name}.

%package -n %{libxcb}
Summary:	X Library
Group:		Development/X11
Conflicts:	%{_lib}x11_6 < 1.6.0-2

%description -n %{libxcb}
This package contains a shared library for %{name}.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/X11
Requires:	%{libname} = %{EVRD}
Requires:	%{libxcb} = %{EVRD}

%description -n %{devname}
This package includes the development files for %{name}.

%if %{with compat32}
%package -n %{lib32name}
Summary:	X Library (32-bit)
Group:		Development/X11

%description -n %{lib32name}
This package contains a shared library for %{name}.

%package -n %{lib32xcb}
Summary:	X Library (32-bit)
Group:		Development/X11
Conflicts:	%{_lib}x11_6 < 1.6.0-2

%description -n %{lib32xcb}
This package contains a shared library for %{name}.

%package -n %{dev32name}
Summary:	Development files for %{name} (32-bit)
Group:		Development/X11
Requires:	%{devname} = %{EVRD}
Requires:	%{lib32name} = %{EVRD}
Requires:	%{lib32xcb} = %{EVRD}

%description -n %{dev32name}
This package includes the development files for %{name}.
%endif

%prep
%autosetup -n libX11-%{version} -p1
export CONFIGURE_TOP="`pwd`"

%if %{with compat32}
mkdir build32
cd build32
%configure32 --enable-composecache
cd ..
%endif

mkdir build
cd build
CFLAGS="%{optflags} -flto" LDFLAGS="%{ldflags} -flto" %configure --enable-composecache

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

%files common
%dir %{_datadir}/X11/locale
%{_datadir}/X11/locale/*
%{_datadir}/X11/Xcms.txt
%{_datadir}/X11/XErrorDB

%files -n %{libname}
%{_libdir}/libX11.so.%{major}*

%files -n %{libxcb}
%{_libdir}/libX11-xcb.so.%{xcbmaj}*

%files -n %{devname}
%doc %{_docdir}/libX11
%{_libdir}/libX11.so
%{_libdir}/libX11-xcb.so
%{_libdir}/pkgconfig/x11.pc
%{_libdir}/pkgconfig/x11-xcb.pc
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
%{_includedir}/X11/Xlib-xcb.h
%{_includedir}/X11/extensions/XKBgeom.h
%{_mandir}/man3/*.3.*
%{_mandir}/man5/*.5*

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libX11.so.%{major}*

%files -n %{lib32xcb}
%{_prefix}/lib/libX11-xcb.so.%{xcbmaj}*

%files -n %{dev32name}
%{_prefix}/lib/libX11.so
%{_prefix}/lib/libX11-xcb.so
%{_prefix}/lib/pkgconfig/x11.pc
%{_prefix}/lib/pkgconfig/x11-xcb.pc
%endif
