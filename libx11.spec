%define	x11major	6
%define	xcbmajor	1

%define libx11 %mklibname x11_ %{x11major}
%define develname %mklibname x11 -d
%define libxorgoldname %mklibname xorg-x11

Name: libx11
Summary: X Library
Version: 1.5.0
Release: 2
Group: System/Libraries
License: MIT
URL: http://xorg.freedesktop.org
Source0: http://xorg.freedesktop.org/releases/individual/lib/libX11-%{version}.tar.bz2
Patch0: libX11-1.3.5-fix-null-pointer.patch
Patch1: libx11-fix-segfault.diff
BuildRequires: x11-util-macros		>= 1.1.5
BuildRequires: x11-xtrans-devel		>= 1.0.4
BuildRequires: libxdmcp-devel		>= 1.0.2
BuildRequires: libxau-devel		>= 1.0.3
BuildRequires: x11-proto-devel		>= 7.4
BuildRequires: groff			>= 1.20.1
BuildRequires: docbook-dtd43-xml
BuildRequires: xcb-devel
BuildRequires: xmlto
BuildRequires: x11-sgml-doctools

%rename libxorg-x11
# because of %{_datadir/X11} being owned by x11-server-common
Requires(pre): x11-server-common >= 1.4.0.90-13

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
Provides: %{name} = %{EVRD}
Requires(post): grep
Requires(postun): grep coreutils

%description -n %{libx11}
%{name} contains the shared libraries that most X programs
need to run properly. These shared libraries are in a separate package in
order to reduce the disk space needed to run X applications on a machine
without an X server (i.e, over a network).

#-----------------------------------------------------------

%package -n %{develname}
Summary: Development files for %{name}
Group: Development/X11
Requires: %{libx11} = %{EVRD}
Provides: libx11-devel = %{EVRD}
Conflicts: %{libxorgoldname}-devel < 7.0
Obsoletes: %{_lib}x11_6-devel
Obsoletes: %{_lib}x11-static-devel

%description -n %{develname}
%{name} includes the libraries, header files and documentation
you'll need to develop programs which run in X clients. X11 includes
the base Xlib library as well as the Xt and Xaw widget sets.

For guidance on programming with these libraries, O'Reilly & Associates
produces a series on X programming which you might find useful.

Install %{name} if you are going to develop programs which
will run as X clients.

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

#-----------------------------------------------------------

%package common
Summary: Common files used by the X.org
Group: System/X11

%description common
Common files used by the X.org

%files common
%dir %{_datadir}/X11/locale
%{_datadir}/X11/locale/*
%{_libdir}/X11/Xcms.txt
%{_datadir}/X11/XErrorDB

#-----------------------------------------------------------

%package doc
Summary: Documentations used by the X.org
Group: System/X11
BuildArch: noarch
Conflicts: libx11-devel < 1.4.3-3

%description doc
Documentations used by the X.org

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
rm -rf %{buildroot}
%makeinstall_std

%files -n %{libx11}
%defattr(-,root,root)
%{_libdir}/libX11.so.%{x11major}*
%{_libdir}/libX11-xcb.so.%{xcbmajor}*


%changelog
* Wed Jun 20 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.5.0-1
+ Revision: 806529
- update to new version 1.5.0

* Fri Apr 13 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.99.901-3
+ Revision: 790497
- update patch 1 from mageia

* Wed Apr 11 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.99.901-2
+ Revision: 790330
- Patch1: workaround a crash in gnome-control-center (from mageia)

* Thu Mar 29 2012 Bernhard Rosenkraenzer <bero@bero.eu> 1.4.99.901-1
+ Revision: 788249
- Update to 1.4.99.901, needed for new libXi (and it works well)

* Fri Mar 09 2012 Paulo Andrade <pcpa@mandriva.com.br> 1.4.4-4
+ Revision: 783715
- Bump release for proper rebuild removing scriptlets.
- Remove scriptlets to help move from /usr/X11R6 to /usr.
- Revert to match packages in mirrors.
- Remove ancient scriptlet to switch from /usr/X11R6 to /usr.

* Thu Mar 08 2012 Paulo Andrade <pcpa@mandriva.com.br> 1.4.4-3
+ Revision: 783355
- Remove pre scriptlet to correct rpm upgrade moving from /usr/X11R6.

* Tue Dec 27 2011 Matthew Dawkins <mattydaw@mandriva.org> 1.4.4-2
+ Revision: 745514
- rebuild
- disabled static build
- removed .la files
- cleaned up spec

* Sat Aug 27 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.4.4-1
+ Revision: 697248
- update to new version 1.4.4

* Sun Jun 05 2011 Funda Wang <fwang@mandriva.org> 1.4.3-3
+ Revision: 682762
- split out doc files

* Sat Jun 04 2011 Funda Wang <fwang@mandriva.org> 1.4.3-2
+ Revision: 682737
- mark doc files

* Mon Apr 11 2011 Matthew Dawkins <mattydaw@mandriva.org> 1.4.3-1
+ Revision: 652660
- fixed major names
- new version 1.4.3
- defined x11-major and xcb-major for better major version tracking

* Sat Mar 12 2011 Funda Wang <fwang@mandriva.org> 1.4.1-4
+ Revision: 644020
- rebuild

* Sun Feb 27 2011 Funda Wang <fwang@mandriva.org> 1.4.1-3
+ Revision: 640203
- rebuild to obsolete old packages

* Thu Feb 17 2011 Matthew Dawkins <mattydaw@mandriva.org> 1.4.1-2
+ Revision: 638298
- added missing BR
- dropped major from devel and static pkgs
- added proper provides and obsoletes

* Wed Jan 12 2011 Thierry Vignaud <tv@mandriva.org> 1.4.1-1
+ Revision: 630956
- new release

* Wed Dec 01 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.4.0-2mdv2011.0
+ Revision: 604584
- Require xmlto and x11-sgml-doctools for full documentation

* Mon Nov 22 2010 Thierry Vignaud <tv@mandriva.org> 1.4.0-1mdv2011.0
+ Revision: 599629
- new release

* Sat Oct 30 2010 Thierry Vignaud <tv@mandriva.org> 1.3.99.903-1mdv2011.0
+ Revision: 590399
- new release

* Wed Sep 22 2010 Thierry Vignaud <tv@mandriva.org> 1.3.99.902-1mdv2011.0
+ Revision: 580459
- fix file list

* Mon Sep 20 2010 Thierry Vignaud <tv@mandriva.org> 1.3.6-1mdv2011.0
+ Revision: 580293
- fix file list
- new release

* Fri Sep 17 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.5-2mdv2011.0
+ Revision: 579264
- Patch0: fix segfault while passing null pointer (mdv #57779)

* Mon Aug 16 2010 Thierry Vignaud <tv@mandriva.org> 1.3.5-1mdv2011.0
+ Revision: 570273
- new release

* Wed Jul 21 2010 Thierry Vignaud <tv@mandriva.org> 1.3.4-1mdv2011.0
+ Revision: 556451
- new release

* Mon Jan 18 2010 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.3.3-1mdv2010.1
+ Revision: 493083
- New version: 1.3.3

* Tue Nov 24 2009 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.3.2-3mdv2010.1
+ Revision: 469771
- Re-enable docs now that we have a working groff

* Mon Nov 09 2009 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.3.2-2mdv2010.1
+ Revision: 463681
- New version: 1.3.2

* Tue Oct 27 2009 Paulo Ricardo Zanoni <pzanoni@mandriva.com> 1.2.2-2mdv2010.0
+ Revision: 459588
- Remove debug flags

* Fri Jul 10 2009 Colin Guthrie <cguthrie@mandriva.org> 1.2.2-1mdv2010.0
+ Revision: 394185
- New version: 1.2.2

* Wed May 20 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.2.1-2mdv2010.0
+ Revision: 378096
- use upstream compose and locale databases. The custom databases were
  supposed to ease the maintanence of these files, but they haven't been
  update in a long time.
- remove patch applied upstream

* Wed Apr 08 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.2.1-1mdv2009.1
+ Revision: 365222
- New version 1.2.1

* Tue Feb 17 2009 Colin Guthrie <cguthrie@mandriva.org> 1.2-1mdv2009.1
+ Revision: 342130
- New version: 1.2
- Try the upstream Compose.pre file (commit log says it's nicer now)

* Wed Feb 04 2009 Ander Conselvan de Oliveira <ander@mandriva.com> 1.1.99.2-4mdv2009.1
+ Revision: 337438
- Fix bug that caused hangs in applications such as Ekiga and OpenOffice(#45751)

* Thu Nov 06 2008 Colin Guthrie <cguthrie@mandriva.org> 1.1.99.2-3mdv2009.1
+ Revision: 300304
- Rebuild due to random failure on i586
- New version: 1.1.99.2 (rc)
- This uses the new libxcb socket handoff mechanism

  + Olivier Blin <blino@mandriva.org>
    - rebuild with xcb
    - build temporarily without xcb

* Fri Sep 05 2008 Thierry Vignaud <tv@mandriva.org> 1.1.5-1mdv2009.0
+ Revision: 281261
- fix xcb-devel BuildRequires
- new release
- remove merged patches
- fix group

* Thu Aug 07 2008 Ander Conselvan de Oliveira <ander@mandriva.com> 1.1.4-5mdv2009.0
+ Revision: 266990
- Fix quoting issue in postun scriptlet (bug #42569)

* Wed Aug 06 2008 Thierry Vignaud <tv@mandriva.org> 1.1.4-4mdv2009.0
+ Revision: 264937
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon May 26 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.1.4-3mdv2009.0
+ Revision: 211452
- o Cherry pick some commits added after libX11-1.1.4 tag
  o Don't add /usr/X11R6/lib to ld.so.conf in %%post, and now, also remove
  it in %%pre as it causes problems with recent changes to make /usr/X11R6
  a symlink to /usr.

* Mon May 05 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.1.4-2mdv2009.0
+ Revision: 201575
- Change ownership of %%{_datadir}/X11 to x11-server-common package.

* Mon Apr 14 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.1.4-1mdv2009.0
+ Revision: 192981
- Update to version 1.1.4.

* Mon Mar 31 2008 Anssi Hannula <anssi@mandriva.org> 1.1.3-6mdv2008.1
+ Revision: 191311
- move the script requires added in last release to binary package

* Sat Mar 01 2008 Olivier Blin <blino@mandriva.org> 1.1.3-5mdv2008.1
+ Revision: 176984
- require grep in post script (and coreutils in postun)

* Fri Feb 08 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.1.3-4mdv2008.1
+ Revision: 164304
- Enable xcb in libx11 build.
  Note that the real libX11.so changes are minimal, and to actually
  use xcb, it is required to explicitly link with libX11-xcb.so, and
  it should be better to also use xcb-devel headers (but there should
  not exist any binary incompatibility).
  One could also try the luck with a command like:
  LD_PRELOAD=/usr/lib/libX11-xcb.so run-some-program

* Mon Jan 14 2008 Paulo Andrade <pcpa@mandriva.com.br> 1.1.3-3mdv2008.1
+ Revision: 151524
- Update BuildRequires and rebuild.

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Colin Guthrie <cguthrie@mandriva.org>
    - Conditionally include files from XCB enable build.

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Fri Sep 28 2007 Frederic Crozat <fcrozat@mandriva.com> 1.1.3-2mdv2008.0
+ Revision: 93530
- Patch0 (GIT): add missing keys to XKeysymDB (Mdv bug #34247)

* Fri Aug 03 2007 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.3-1mdv2008.0
+ Revision: 58399
- drop patch 0 (merged upstream)
- new upstream version 1.1.3

  + Ademar de Souza Reis Jr <ademar@mandriva.com.br>
    - add missing libxcb build-requirement
    - build section cleanup

* Sun Jun 10 2007 Olivier Blin <blino@mandriva.org> 1.1.2-2mdv2008.0
+ Revision: 37943
- fix XGetMotionEvents prototype (should fix gimp paintbrush, submitted as upstream bug #11222)
- use -a option for automake and run autoheader (to ease building from git)

* Mon Jun 04 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.1.2-1mdv2008.0
+ Revision: 35178
- new upstream version: 1.1.2
- remove patch already applied (CVE-2007-1667)

* Thu May 03 2007 Ademar de Souza Reis Jr <ademar@mandriva.com.br> 1.1.1-3mdv2008.0
+ Revision: 22005
- add patch for CVE-2007-1667 (see #29818 comments)


* Sun Feb 18 2007 Götz Waschk <waschk@mandriva.org> 1.1.1-2mdv2007.0
+ Revision: 122277
- rebuild for pkgconfig deps

* Fri Feb 09 2007 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.1.1-1mdv2007.1
+ Revision: 118504
- new upstream release: 1.1.1

  + Pablo Saratxaga <pablo@mandriva.com>
    - merged {compose,locale}.dir with X11.org files
    - zh_HK.UTF-
    - added recognition of more locales (now in sync with DrakX)

* Thu Nov 16 2006 Pablo Saratxaga <pablo@mandriva.com> 1.0.3-3mdv2007.1
+ Revision: 84844
- improved default UTF-8 Compose file
- improved {locale,compose}.{dir,alias} with definitions for all our locales

* Fri Jul 07 2006 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.0.3-2mdv2007.0
+ Revision: 38413
- Removed wrong requires for mkcomposecache. Thanks for Stefan van der Eijk for pointing that.

  + Thierry Vignaud <tvignaud@mandriva.com>
    - fix group

* Tue Jul 04 2006 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.0.3-1mdv2007.0
+ Revision: 38293
- new upstream release (1.0.3):
  * Fix Compose Cache
  * One instance of checking the setuid() return value was missed

* Thu Jun 29 2006 Gustavo Pichorim Boiko <boiko@mandriva.com> 1.0.2-1mdv2007.0
+ Revision: 38132
- new upstream release (1.0.2). Highlights:
  * i18n: Separate data and lib directories
  * Break out locale data into separate data and library directories, under
  $(datadir) and $(libdir), respectively, by default.
  * im: add Braille input method (#6296)
  * fdo bug #3104: Compose table cache for faster X11 application starts.
  * Set XTHREADLIB correctly for dragonfly platforms.
  * Fix threading support on GNU/kFreeBSD systems.
  * Check setuid() return value
- removed patch for braille support (this release already has that)
- rebuild to fix cooker uploading
- renamed libx11_6-common to libx11-common
- increment release
- fixed more dependencies
- Adding X.org 7.0 to the repository

  + Frederic Crozat <fcrozat@mandriva.com>
    - Release 1.0.1
      Patch0 (GIT): add braille input method support

  + Andreas Hasenack <andreas@mandriva.com>
    - renamed mdv to packages because mdv is too generic and it's hosting only packages anyway

  + Laurent Montel <lmontel@mandriva.com>
    - Fix conflict on x86_64

  + Thierry Vignaud <tvignaud@mandriva.com>
    - provides/obsoletes libxorg-x11 (so that updates work smoothly)

