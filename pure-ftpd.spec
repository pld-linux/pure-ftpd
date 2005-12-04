#
# Conditional build:
%bcond_with	extra		# with additional, maybe useful, but unmaintained features
%bcond_without	ldap		# disable LDAP auth
%bcond_without	longusername	# with username length = 128 (default 32)
%bcond_without	mysql		# disable MySQL auth but disables PAM auth
%bcond_without	pgsql		# disable PostgreSQL support
%bcond_without	puredb		# disable pure-db support
%bcond_without	tls		# disable SSL/TLS support
#
Summary:	Small, fast and secure FTP server
Summary(pl):	Ma³y, szybki i bezpieczny serwer FTP
Name:		pure-ftpd
Version:	1.0.20
Release:	10%{?with_extra:extra}
Epoch:		0
License:	BSD-like%{?with_extra:, GLPv2 for pure-config due to libcfg+ license}
Group:		Daemons
Source0:	ftp://ftp.pureftpd.org/pub/pure-ftpd/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	e928e9e15adf6b52bfe6183fdad20144
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	ftpusers.tar.bz2
# Source3-md5:	76c80b6ec9f4d079a1e27316edddbe16
Source4:	http://twittner.host.sk/files/pure-config/pure-config-20041201.tar.gz
# Source4-md5:	3f2ff6b00b5c38ee11ce588ee5af6cf6
Patch0:		%{name}-config.patch
Patch1:		%{name}-path_to_ssl_cert_in_config.patch
Patch2:		%{name}-pure-pw_passwd.patch
Patch3:		%{name}-userlength.patch
Patch4:		%{name}-mysql_config.patch
Patch5:		%{name}-nosymlinks-hideuidmismatch.patch
Patch6:		%{name}-auth-can-delete-pure.patch
URL:		http://www.pureftpd.org/
%{!?with_extra:Requires:	perl-base}
%{?with_extra:BuildRequires:	autoconf}
%{?with_extra:BuildRequires:	automake}
BuildRequires:	libcap-devel
%{?with_extra:BuildRequires:	libcfg+-devel >= 0.6.2}
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_ldap:BuildRequires:	openldap-devel}
%{?with_tls:BuildRequires:	openssl-devel}
BuildRequires:	pam-devel
%{?with_pgsql:BuildRequires:	postgresql-devel}
Requires(post,preun):	/sbin/chkconfig
Requires:	pam >= 0.79.0
Requires:	rc-scripts
Provides:	ftpserver
Obsoletes:	ftpserver
Obsoletes:	anonftp
Obsoletes:	bftpd
Obsoletes:	ftpd-BSD
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

%description
Pure-FTPd is a fast, production-quality, standard-comformant FTP
server, based upon Troll-FTPd. Unlike other popular FTP servers, it
has no known security flaw, it is really trivial to set up and it is
especially designed for modern Linux kernels (setfsuid, sendfile,
capabilities) . Features include PAM support, IPv6, chroot()ed home
directories, virtual domains, built-in LS, anti-warez system, bounded
ports for passive downloads...

%description -l pl
Pure-FTPD to szybki, wysokiej jako¶ci, odpowiadaj±cy standardom serwer
FTP bazuj±cy na Troll-FTPd. W przeciwieñstwie do innych serwerów FTP
nie ma znanych luk w bezpieczeñstwie. Ponadto jest trywialny w
konfiguracji i specjalnie zaprojektowany dla nowych kerneli Linuksa
(setfsuid, sendfile, capabilibies). Mo¿liwo¶ci to wsparcie dla PAM-a,
IPv6, chroot()owanych katalogów domowych, virtualne domeny, wbudowany
LS, system anty-warezowy, ograniczanie portów dla pasywnych
po³±czeñ...

%prep
%setup -q -a 4
%patch0 -p0
%patch4 -p1
%patch5 -p1
%patch6 -p1
%{?with_longusername:%patch3 -p1}
%{?with_extra:%patch1 -p1}
%{?with_extra:%patch2 -p1}

%build
%configure \
	--with-boring \
	--with-altlog \
	--with-cookie \
	--with-diraliases \
	--with-extauth \
	--with-ftpwho \
	--with-language=english \
	--with-largefile \
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
	$RPM_BUILD_ROOT{%{_sysconfdir}/vhosts,%{_ftpdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%{?with_ldap:install pureftpd-ldap.conf $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd-ldap.conf}
%{?with_mysql:install pureftpd-mysql.conf $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd-mysql.conf}
%{?with_pgsql:install pureftpd-pgsql.conf $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd-pgsql.conf}
install configuration-file/pure-ftpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd.conf
%{!?with_extra:install configuration-file/pure-config.pl $RPM_BUILD_ROOT%{_sbindir}}
touch $RPM_BUILD_ROOT/etc/security/blacklist.ftp

ln -s vhosts $RPM_BUILD_ROOT%{_sysconfdir}/pure-ftpd

bzip2 -dc %{SOURCE3} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

%if %{with extra}
cd pure-config
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f %{_var}/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start PureFTPD daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f %{_var}/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop 1>&2
	fi
	/sbin/chkconfig --del %{name}
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
