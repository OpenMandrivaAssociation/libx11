%define	x11major	6
%define	xcbmajor	1

%define libx11 %mklibname x11_ %{x11major}
%define libx11xcb %mklibname x11-xcb %{xcbmajor}
%define devname %mklibname x11 -d

Summary:	X Library
Name:		libx11
Version:	1.6.0
Release:	2
Group:		System/Libraries
License:	MIT
Url:		http://xorg.freedesktop.org
Source0:	http://xorg.freedesktop.org/releases/individual/lib/libX11-%{version}.tar.bz2
Patch0:		libX11-1.3.5-fix-null-pointer.patch
Patch1:		libx11-fix-segfault.diff
BuildRequires:	docbook-dtd43-xml
BuildRequires:	groff
BuildRequires:	x11-sgml-doctools
BuildRequires:	x11-util-macros
BuildRequires:	xmlto
BuildRequires:	pkgconfig(xau)
BuildRequires:	pkgconfig(xcb)
BuildRequires:	pkgconfig(xdmcp)
BuildRequires:	pkgconfig(xproto)
BuildRequires:	pkgconfig(xtrans)

%rename libxorg-x11
# because of %{_datadir/X11} being owned by x11-server-common
Requires(pre):	x11-server-common >= 1.4.0.90-13

%description
%{name} contains the shared libraries that most X programs
need to run properly. These shared libraries are in a separate package in
order to reduce the disk space needed to run X applications on a machine
without an X server (i.e, over a network).

#-----------------------------------------------------------

%package -n %{libx11}
Summary:	X Library
Group:		Development/X11
Provides:	%{name} = %{EVRD}

%description -n %{libx11}
%{name} contains the shared libraries that most X programs
need to run properly. These shared libraries are in a separate package in
order to reduce the disk space needed to run X applications on a machine
without an X server (i.e, over a network).

%files -n %{libx11}
%{_libdir}/libX11.so.%{x11major}*

#-----------------------------------------------------------

%package -n %{libx11xcb}
Summary:	X Library
Group:		Development/X11
Conflicts:	%{_lib}x11_6 < 1.6.0-2

%description -n %{libx11xcb}
%{name} contains the shared libraries that most X programs
need to run properly. These shared libraries are in a separate package in
order to reduce the disk space needed to run X applications on a machine
without an X server (i.e, over a network).

%files -n %{libx11xcb}
%{_libdir}/libX11-xcb.so.%{xcbmajor}*

#-----------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/X11
# TODO: split into 2 devel packages
Requires:	%{libx11} = %{EVRD}
Requires:	%{libx11xcb} = %{EVRD}

%description -n %{devname}
%{name} includes the libraries, header files and documentation
you'll need to develop programs which run in X clients. X11 includes
the base Xlib library as well as the Xt and Xaw widget sets.

For guidance on programming with these libraries, O'Reilly & Associates
produces a series on X programming which you might find useful.

Install %{name} if you are going to develop programs which
will run as X clients.

%files -n %{devname}
%{_mandir}/man3/*.3.*
%{_libdir}/libX11.so
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
%{_libdir}/libX11-xcb.so
%{_libdir}/pkgconfig/x11-xcb.pc
%{_includedir}/X11/Xlib-xcb.h
%{_mandir}/man5/*.5*

#-----------------------------------------------------------

%package common
Summary:	Common files used by the X.org
Group:		System/X11

%description common
Common files used by the X.org.

%files common
%dir %{_datadir}/X11/locale
%{_datadir}/X11/locale/*
%{_datadir}/X11/Xcms.txt
%{_datadir}/X11/XErrorDB

#-----------------------------------------------------------

%package doc
Summary:	Documentations used by the X.org
Group:		System/X11
BuildArch:	noarch

%description doc
Documentations used by the X.org.

%files doc
%{_docdir}/libX11

#-----------------------------------------------------------

%prep
%setup -q -n libX11-%{version}
%patch0 -p1
%patch1 -p1

%build
%configure2_5x \
	--disable-static

%make

%install
%makeinstall_std

