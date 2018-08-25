%define	major	6
%define	xcbmaj	1
%define libname	%mklibname x11_ %{major}
%define libxcb	%mklibname x11-xcb %{xcbmaj}
%define devname	%mklibname x11 -d

Summary:	X Library
Name:		libx11
Version:	1.6.6
Release:	1
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

%prep
%setup -qn libX11-%{version}
%apply_patches

%build
%configure \
    --disable-static \
    --enable-composecache

%make

%install
%makeinstall_std

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
%{_mandir}/man3/*.3.*
%{_mandir}/man5/*.5*
