Name:		icecast
Version:	2.3.2
Release:	%mkrel 3
Summary:	Streaming Media Server
Epoch:		2
Group:		System/Servers
License:	GPL
URL:		http://www.icecast.org
Source0:	http://downloads.us.xiph.org/releases/icecast/%{name}-%{version}.tar.gz
Source1:	%{name}.init
Source2:	%{name}.logrotate
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

%build
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

install -d -m 755 %{buildroot}%{_var}/log/%{name}
install -d -m 755 %{buildroot}%{_datadir}/%{name}

# remove installed documentation
rm -rf %{buildroot}%{_datadir}/doc/%{name}

install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/%{name}

# logrotate
install -d %{buildroot}%{_sysconfdir}/logrotate.d/
install -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# to hold pid file ( need to be writable by icecast )
mkdir -p %{buildroot}/%{_var}/run/%{name}/

%clean 
rm -rf %{buildroot}

%pre
%_pre_useradd %{name} %{_datadir}/%{name} /bin/false

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING HACKING README TODO
%{_bindir}/%{name}
%{_datadir}/%{name}
%attr(-,icecast,icecast) %{_var}/log/%{name}
%attr(-,icecast,icecast) %dir %{_var}/run/%{name}/
%config(noreplace) %{_sysconfdir}/%{name}.xml
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
