#
# Conditional build:
%bcond_with	extra		# with additional, maybe useful, but unmaintained features
%bcond_without	ldap		# disable LDAP auth
%bcond_without	longusername	# with username length = 128 (default 32)
%bcond_without	mysql		# disable MySQL auth but disables PAM auth
%bcond_without	pgsql		# disable PostgreSQL support
%bcond_without	puredb		# disable pure-db support
%bcond_without	tls		# disable SSL/TLS support
%bcond_without	cap		# disable capabilities
#
Summary:	Small, fast and secure FTP server
Summary(pl.UTF-8):	Mały, szybki i bezpieczny serwer FTP
Name:		pure-ftpd
Version:	1.0.21
Release:	4%{?with_extra:extra}
Epoch:		0
License:	BSD-like%{?with_extra:, GLPv2 for pure-config due to libcfg+ license}
Group:		Daemons
Source0:	ftp://ftp.pureftpd.org/pub/pure-ftpd/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	ca8a8dbec0cd9c8ea92fc4c37ea9c410
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	ftpusers.tar.bz2
# Source3-md5:	76c80b6ec9f4d079a1e27316edddbe16
Source4:	http://twittner.host.sk/files/pure-config/pure-config-20041201.tar.gz
# Source4-md5:	3f2ff6b00b5c38ee11ce588ee5af6cf6
Patch0:		%{name}-config.patch
Patch1:		%{name}-path_to_ssl_cert_in_config.patch
Patch2:		%{name}-pure-pw_passwd.patch
Patch3:		%{name}-mysql_config.patch
Patch4:		%{name}-nosymlinks-hideuidmismatch.patch
Patch5:		%{name}-auth-can-delete-pure.patch
URL:		http://www.pureftpd.org/
%{?with_extra:BuildRequires:	autoconf}
%{?with_extra:BuildRequires:	automake}
%{?with_cap:BuildRequires:	libcap-devel}
%{?with_extra:BuildRequires:	libcfg+-devel >= 0.6.2}
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_ldap:BuildRequires:	openldap-devel >= 2.3.0}
%{?with_tls:BuildRequires:	openssl-devel}
BuildRequires:	pam-devel
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpmbuild(macros) >= 1.304
Requires(post,preun):	/sbin/chkconfig
Requires:	pam >= 0.79.0
%{!?with_extra:Requires:	perl-base}
Requires:	rc-scripts
Provides:	ftpserver
Obsoletes:	anonftp
Obsoletes:	bftpd
Obsoletes:	ftpd-BSD
Obsoletes:	ftpserver
Obsoletes:	glftpd
Obsoletes:	heimdal-ftpd
Obsoletes:	linux-ftpd
Obsoletes:	muddleftpd
Obsoletes:	proftpd
Obsoletes:	proftpd-common
Obsoletes:	proftpd-inetd
Obsoletes:	proftpd-standalone
Obsoletes:	troll-ftpd
Obsoletes:	vsftpd
Obsoletes:	wu-ftpd
Conflicts:	man-pages < 1.51
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ftpd
%define		_ftpdir		/home/services/ftp
%define		schemadir	/usr/share/openldap/schema

%description
Pure-FTPd is a fast, production-quality, standard-comformant FTP
server, based upon Troll-FTPd. Unlike other popular FTP servers, it
has no known security flaw, it is really trivial to set up and it is
especially designed for modern Linux kernels (setfsuid, sendfile,
capabilities) . Features include PAM support, IPv6, chroot()ed home
directories, virtual domains, built-in LS, anti-warez system, bounded
ports for passive downloads...

%description -l pl.UTF-8
Pure-FTPD to szybki, wysokiej jakości, odpowiadający standardom serwer
FTP bazujący na Troll-FTPd. W przeciwieństwie do innych serwerów FTP
nie ma znanych luk w bezpieczeństwie. Ponadto jest trywialny w
konfiguracji i specjalnie zaprojektowany dla nowych kerneli Linuksa
(setfsuid, sendfile, capabilibies). Możliwości to wsparcie dla PAM-a,
IPv6, chroot()owanych katalogów domowych, virtualne domeny, wbudowany
LS, system anty-warezowy, ograniczanie portów dla pasywnych
połączeń...

%package -n openldap-schema-pureftpd
Summary:	Pure-FTPd LDAP schema
Summary(pl.UTF-8):	Schemat LDAP Pure-FTPd'a
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers
Requires:	sed >= 4.0 

%description -n openldap-schema-pureftpd
This package contains an Pure-FTPd openldap schema.

%description -n openldap-schema-pureftpd -l pl.UTF-8
Ten pakiet zawiera schemat Pure-FTPd pureftpd.schema dla openldapa.

%prep
%setup -q -a 4
%patch0 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1
%{?with_extra:%patch1 -p1}
%{?with_extra:%patch2 -p1}

%build
# drop --without-cork for Th
%configure \
	--without-cork \
	--with-boring \
	--with-altlog \
	--with-cookie \
	--with-diraliases \
	--with-extauth \
	--with-ftpwho \
	--with-language=english \
	--with-largefile \
	%{!?with_cap:--without-capabilities} \
	%{?with_ldap:--with-ldap} \
	%{?with_mysql:CPPFLAGS="-I%{_includedir}/mysql" --with-mysql} \
	--with-pam \
	--with-peruserlimits \
	%{?with_pgsql:--with-pgsql} \
	--with-privsep \
	%{?with_puredb:--with-puredb} \
	--with-quotas \
	--with-ratios \
	--with-throttling \
	%{?with_tls:--with-tls --with-certfile=%{_sharedstatedir}/openssl/certs/ftpd.pem} \
	--with-uploadscript \
	--with-virtualchroot \
	--with-virtualhosts

%if %{with extra}
cd pure-config
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{pam.d,sysconfig,security,rc.d/init.d} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/vhosts,%{_ftpdir},%{schemadir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%{?with_ldap:install pureftpd-ldap.conf $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd-ldap.conf}
%{?with_mysql:install pureftpd-mysql.conf $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd-mysql.conf}
%{?with_pgsql:install pureftpd-pgsql.conf $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd-pgsql.conf}
install configuration-file/pure-ftpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd.conf
%{!?with_extra:install configuration-file/pure-config.pl $RPM_BUILD_ROOT%{_sbindir}}
install pureftpd.schema $RPM_BUILD_ROOT%{schemadir}/pureftpd.schema
touch $RPM_BUILD_ROOT/etc/security/blacklist.ftp

ln -s vhosts $RPM_BUILD_ROOT%{_sysconfdir}/pure-ftpd

bzip2 -dc %{SOURCE3} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
rm -f $RPM_BUILD_ROOT%{_mandir}/ftpusers-path.diff

%if %{with extra}
%{__make} -C pure-config install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart "PureFTPD daemon"

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%post -n openldap-schema-pureftpd
%openldap_schema_register %{schemadir}/pureftpd.schema -d core
%service -q ldap restart

%postun -n openldap-schema-pureftpd
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/pureftpd.schema
	%service -q ldap restart
fi


%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog CONTACT FAQ HISTORY NEWS README* THANKS pure*.conf pureftpd.schema
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.ftp
%{?with_ldap:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pureftpd-ldap.conf}
%{?with_mysql:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pureftpd-mysql.conf}
%{?with_pgsql:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pureftpd-pgsql.conf}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pureftpd.conf
%attr(710,root,ftp) %dir %{_sysconfdir}
%dir %{_sysconfdir}/vhosts
%dir %{_sysconfdir}/pure-ftpd
%dir %{_ftpdir}
%{_mandir}/man?/*
%lang(ja) %{_mandir}/ja/man5/ftpusers*
%lang(pl) %{_mandir}/pl/man5/ftpusers*
%lang(pt_BR) %{_mandir}/pt_BR/man5/ftpusers*
%lang(ru) %{_mandir}/ru/man5/ftpusers*

%files -n openldap-schema-pureftpd
%defattr(644,root,root,755) %{schemadir}/pureftpd.schema
