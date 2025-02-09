Summary:	Streaming Media Server
Name:		icecast
Version:	2.4.4
Release:	1
Epoch:		2
Group:		System/Servers
License:	GPLv2+
Url:		https://www.icecast.org
Source0:	http://downloads.us.xiph.org/releases/icecast/%{name}-%{version}.tar.gz
Source1:	status3.xsl
Source2:	icecast.service
Source3:	icecast.logrotate
Source4:	icecast.xml
Patch0:		%{name}.conf.patch
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(vorbis)
Requires(pre,postun):	rpm-helper
Requires(post,preun,postun):	systemd
Provides:	streaming-server

%description
Icecast is an Internet based broadcasting system based on the Mpeg Layer III
streaming technology.  It was originally inspired by Nullsoft's Shoutcast
and also mp3serv by Scott Manley.  The icecast project was started for several
reasons: a) all broadcasting systems were pretty much closed source,
non-free software implementations, b) Shoutcast doesn't allow you to run your
own directory servers, or support them, and c) we thought it would be a
lot of fun.

%files
%doc AUTHORS COPYING HACKING README TODO
%{_bindir}/%{name}
%{_datadir}/%{name}
%attr(-,icecast,icecast) %{_var}/log/%{name}
%attr(-,icecast,icecast) %dir %{_var}/run/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}.xml
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%{_unitdir}/icecast.service

%pre
%_pre_useradd %{name} %{_datadir}/%{name} /bin/false

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%_postun_userdel %{name}
%systemd_postun %{name}.service

#----------------------------------------------------------------------------

%prep
%autosetup -p1
find -name "*.html" -or -name "*.jpg" -or -name "*.css" | xargs chmod 644

%build
%configure \
	--with-curl \
	--with-openssl \
	--with-ogg \
	--with-theora \
	--with-speex
%make_build

%install
%make_install
rm -rf %{buildroot}%{_datadir}/icecast/doc
rm -rf %{buildroot}%{_docdir}/icecast
install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/icecast/web/status3.xsl
install -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/%{name}.service
install -D -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/icecast
install -D -m 640 %{SOURCE4} %{buildroot}%{_sysconfdir}/icecast.xml
mkdir -p %{buildroot}%{_localstatedir}/log/icecast
mkdir -p %{buildroot}%{_localstatedir}/run/icecast
