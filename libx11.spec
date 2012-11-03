%define x11major 6
%define xcbmajor 1

%define libx11 %mklibname x11_ %{x11major}
%define develname %mklibname x11 -d
%define libxorgoldname %mklibname xorg-x11

Name:		libx11
Summary:	X Library
Version:	1.5.0
Release:	2
Group:		System/Libraries
License:	MIT
URL:		http://xorg.freedesktop.org
Source0:	http://xorg.freedesktop.org/releases/individual/lib/libX11-%{version}.tar.bz2
Patch0:		libX11-1.3.5-fix-null-pointer.patch
Patch1:		libx11-fix-segfault.diff
BuildRequires:	x11-util-macros >= 1.1.5
BuildRequires:	x11-xtrans-devel >= 1.0.4
BuildRequires:	libxdmcp-devel >= 1.0.2
BuildRequires:	libxau-devel >= 1.0.3
BuildRequires:	x11-proto-devel >= 7.4
BuildRequires:	groff >= 1.20.1
BuildRequires:	docbook-dtd43-xml
BuildRequires:	xcb-devel
BuildRequires:	xmlto
BuildRequires:	x11-sgml-doctools

%rename		libxorg-x11
# because of %{_datadir/X11} being owned by x11-server-common
Requires(pre): x11-server-common >= 1.4.0.90-13

%description
%{name} contains the shared libraries that most X programs
need to run properly. These shared libraries are in a separate package in
order to reduce the disk space needed to run X applications on a machine
without an X server (i.e, over a network).

%package -n %{libx11}
Summary:	X Library
Group:		Development/X11
Conflicts:	%{libxorgoldname} < 7.0
Provides:	%{name} = %{version}
Requires(post):	grep
Requires(postun):	grep coreutils

%description -n %{libx11}
%{name} contains the shared libraries that most X programs
need to run properly. These shared libraries are in a separate package in
order to reduce the disk space needed to run X applications on a machine
without an X server (i.e, over a network).

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/X11
Requires:	%{libx11} = %{version}-%{release}
Provides:	libx11-devel = %{version}-%{release}
Conflicts:	%{libxorgoldname}-devel < 7.0
Obsoletes:	%{_lib}x11_6-devel
Obsoletes:	%{_lib}x11-static-devel

%description -n %{develname}
%{name} includes the libraries, header files and documentation
you'll need to develop programs which run in X clients. X11 includes
the base Xlib library as well as the Xt and Xaw widget sets.

For guidance on programming with these libraries, O'Reilly & Associates
produces a series on X programming which you might find useful.

Install %{name} if you are going to develop programs which
will run as X clients.

%package common
Summary:	Common files used by the X.org
Group:		System/X11

%description common
Common files used by the X.org.



#-----------------------------------------------------------

%package doc
Summary:	Documentations used by the X.org
Group:		System/X11
BuildArch:	noarch
Conflicts:	libx11-devel < 1.4.3-3

%description doc
Documentations used by the X.org.

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

%files -n %{libx11}
%{_libdir}/libX11.so.%{x11major}*
%{_libdir}/libX11-xcb.so.%{xcbmajor}*

%files -n %{develname}
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

%files common
%dir %{_datadir}/X11/locale
%{_datadir}/X11/locale/*
%{_libdir}/X11/Xcms.txt
%{_datadir}/X11/XErrorDB

%files doc
%{_docdir}/libX11
