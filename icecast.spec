Name:		icecast
Version:	2.3.3
Release:	1
Summary:	Streaming Media Server
Epoch:		2
Group:		System/Servers
License:	GPL
URL:		http://www.icecast.org
Source0:	http://downloads.us.xiph.org/releases/icecast/%{name}-%{version}.tar.gz
Source1:	status3.xsl
Source2:	icecast.service
Source3:	icecast.logrotate
Source4:	icecast.xml
Patch0:		%{name}.conf.patch
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires(postun): rpm-helper
Requires(preun): rpm-helper
BuildRequires:	libxslt-devel
BuildRequires:	libcurl-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libogg-devel
BuildRequires:	libtheora-devel
BuildRequires:  speex-devel

%description
Icecast is an Internet based broadcasting system based on the Mpeg Layer III
streaming technology.  It was originally inspired by Nullsoft's Shoutcast
and also mp3serv by Scott Manley.  The icecast project was started for several
reasons: a) all broadcasting systems were pretty much closed source,
non-free software implementations, b) Shoutcast doesn't allow you to run your
own directory servers, or support them, and c) we thought it would be a
lot of fun.

%prep
%setup -q
%patch0 -p0 -b .orig
find -name "*.html" -or -name "*.jpg" -or -name "*.css" | xargs chmod 644
%{__sed} -i -e 's/icecast2/icecast/g' debian/icecast2.1


%build
%configure2_5x \
        --with-curl \
        --with-openssl \
        --with-ogg \
        --with-theora \
        --with-speex
%make

%install
%makeinstall_std
rm -rf %{buildroot}%{_datadir}/icecast/doc
rm -rf %{buildroot}%{_docdir}/icecast
install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/icecast/web/status3.xsl
install -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/icecast.service
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/icecast
install -D -m 640 %{SOURCE4} %{buildroot}%{_sysconfdir}/icecast.xml
install -D -m 644 debian/icecast2.1 %{buildroot}%{_mandir}/man1/icecast.1
mkdir -p %{buildroot}%{_localstatedir}/log/icecast
mkdir -p %{buildroot}%{_localstatedir}/run/icecast


%pre
%_pre_useradd %{name} %{_datadir}/%{name} /bin/false

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%files
%doc AUTHORS COPYING HACKING README TODO
%{_bindir}/%{name}
%{_datadir}/%{name}
%attr(-,icecast,icecast) %{_var}/log/%{name}
%attr(-,icecast,icecast) %dir %{_var}/run/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}.xml
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_mandir}/man1/icecast.1.*
%{_unitdir}/icecast.service


%changelog
* Wed Apr 27 2011 Jani Välimaa <wally@mandriva.org> 2:2.3.2-3mdv2011.0
+ Revision: 659756
- rebuild
  - rediff P0
  - drop buildroot definition
  - clean .spec a bit

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 2:2.3.2-2mdv2009.0
+ Revision: 267109
- rebuild early 2009.0 package (before pixel changes)

* Fri Jun 06 2008 Olivier Thauvin <nanardon@mandriva.org> 2:2.3.2-1mdv2009.0
+ Revision: 216555
- 2.3.2

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 David Walluck <walluck@mandriva.org> 2:2.3.1-5mdv2008.0
+ Revision: 82417
- don't mark initscript as %%config

* Sat Sep 08 2007 David Walluck <walluck@mandriva.org> 2:2.3.1-4mdv2008.0
+ Revision: 82287
- add LSB support to initscript
- added create line to logrotate
- check if PID exists in logrotate and silently handle errors
- uncompress initscript
- set the user to icecast in the initscript so that icecast will start


* Sat Feb 03 2007 Emmanuel Andry <eandry@mandriva.org> 2.3.1-3mdv2007.0
+ Revision: 116091
- bunzipped patch
- added patch from fedora to fix build against latest curl

* Tue Aug 08 2006 Olivier Thauvin <nanardon@mandriva.org> 2:2.3.1-2mdv2007.0
+ Revision: 53737
- fix prereq, rebuild
- Import icecast

* Tue Dec 20 2005 Olivier Thauvin <nanardon@mandriva.org> 2:2.3.1-1mdk
- 2.3.1

* Tue Oct 18 2005 Olivier Thauvin <nanardon@mandriva.org> 2:2.3.0-2mdk
- BuildRequires: speex-devel (misc)

* Mon Oct 17 2005 Olivier Thauvin <nanardon@mandriva.org> 2:2.3.0-1mdk
- 2.3.0

* Mon Aug 08 2005 Michael Scherer <misc@mandriva.org> 2:2.2.0-3mdk
- fix the default pid file ( not writable when run as non root )

* Mon Jul 04 2005 Michael Scherer <misc@mandriva.org> 2:2.2.0-2mdk
- proper logrotate support

* Sun May 22 2005 Michael Scherer <misc@mandriva.org> 2:2.2.0-1mdk
- new release
- rpmbuildupdate

* Wed Nov 24 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.1.0-2mdk
- From Cedric Devillers (brancaleone on #mandrakefr): 
    - Fix config patch
    - Fix logrotate config

* Sun Nov 21 2004 Olivier Thauvin <thauvin@aerov.jussieu.fr> 2.1.0-1mdk
- 2.1.0

* Sat Jul 03 2004 Rafael Garcia-Suarez <rgarciasuarez@mandrakesoft.com> 2.0.1-1mdk
- New version
- Rebuild for new curl

* Tue Mar 16 2004 Laurent Culioli <laurent@mandrakesoft.com> 2.0.0-2mdk
- fix initscript

