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

%define	rel	2
Summary:	Small, fast and secure FTP server
Summary(pl.UTF-8):	Mały, szybki i bezpieczny serwer FTP
Name:		pure-ftpd
Version:	1.0.52
Release:	%{rel}%{?with_extra:extra}
License:	BSD-like%{?with_extra:, GLPv2 for pure-config due to libcfg+ license}
Group:		Daemons
Source0:	https://download.pureftpd.org/pub/pure-ftpd/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	6fdd75053b7aaa0f45089a7bf7fcd0b4
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Source4:	ftpusers.tar.bz2
# Source4-md5:	76c80b6ec9f4d079a1e27316edddbe16
Source5:	http://twittner.host.sk/files/pure-config/pure-config-20041201.tar.gz
# Source5-md5:	3f2ff6b00b5c38ee11ce588ee5af6cf6
Patch0:		%{name}-config.patch

Patch2:		%{name}-pure-pw_passwd.patch
Patch3:		%{name}-mysql_config.patch
# from Fedora
Patch4:		0003-Allow-having-both-options-and-config-file-on-command.patch
Patch5:		paths.patch
Patch6:		%{name}-apparmor.patch
Patch7:		%{name}-mysql-utf8.patch
Patch8:		caps.patch
Patch9:		oob.patch

Patch11:        keep-spaces.patch
URL:		http://www.pureftpd.org/
%{?with_extra:BuildRequires:	autoconf >= 2.65}
%{?with_extra:BuildRequires:	automake >= 1:1.11.2}
BuildRequires:	libapparmor-devel
%{?with_cap:BuildRequires:	libcap-devel}
%{?with_extra:BuildRequires:	libcfg+-devel >= 0.6.2}
BuildRequires:	libsodium-devel
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_ldap:BuildRequires:	openldap-devel >= 2.3.0}
%{?with_tls:BuildRequires:	openssl-devel}
BuildRequires:	pam-devel
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	rpmbuild(macros) >= 1.304
Requires(post):		/usr/bin/openssl
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	pam >= 0.79.0
%{!?with_extra:Requires:	perl-base}
Requires:	rc-scripts
Provides:	ftpserver
Provides:	user(ftpauth)
Provides:	group(ftpauth)
Provides:	user(ftpcert)
Provides:	group(ftpcert)
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
Summary(pl.UTF-8):	Schemat LDAP dla Pure-FTPd
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers
Requires:	sed >= 4.0
BuildArch:	noarch

%description -n openldap-schema-pureftpd
This package contains an Pure-FTPd openldap schema.

%description -n openldap-schema-pureftpd -l pl.UTF-8
Ten pakiet zawiera schemat Pure-FTPd pureftpd.schema dla openldapa.

%prep
%setup -q -a 5
%patch -P0 -p0

%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1
%patch -P8 -p1
%patch -P9 -p1

%patch -P11 -p1

%{?with_extra:%patch -P2 -p1}

%build
%{__aclocal} -Im4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -DALLOW_DELETION_OF_TEMPORARY_FILES=1 -DALWAYS_SHOW_RESOLVED_SYMLINKS=1" \
	--disable-silent-rules \
	--with-boring \
	--with-altlog \
	--with-cookie \
	--with-diraliases \
	--with-extauth \
	--with-ftpwho \
	--with-language=english \
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
	%{?with_tls:--with-tls --with-certfile=/etc/pure-ftpd/ssl/pure-ftpd.pem} \
	--with-uploadscript \
	--with-virtualchroot \
	--with-virtualhosts \
	--with-apparmor

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
install -d $RPM_BUILD_ROOT/etc/{pam.d,sysconfig,security,rc.d/init.d,%{name}/{certd,authd,conf,ssl}} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/vhosts,%{_ftpdir},%{schemadir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/%{name}
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%{?with_ldap:install pureftpd-ldap.conf $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd-ldap.conf}
%{?with_mysql:install pureftpd-mysql.conf $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd-mysql.conf}
%{?with_pgsql:install pureftpd-pgsql.conf $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd-pgsql.conf}
cp -p pureftpd.schema $RPM_BUILD_ROOT%{schemadir}/pureftpd.schema

mv $RPM_BUILD_ROOT%{_sysconfdir}/{pure-ftpd,pureftpd}.conf

touch $RPM_BUILD_ROOT%{_sysconfdir}/{ftpusers,pureftpd-dir-aliases}
:> $RPM_BUILD_ROOT/etc/pure-ftpd/ssl/dhparams.pem

ln -s vhosts $RPM_BUILD_ROOT%{_sysconfdir}/pure-ftpd

bzip2 -dc %{SOURCE4} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
rm -f $RPM_BUILD_ROOT%{_mandir}/ftpusers-path.diff

%if %{with extra}
%{__make} -C pure-config install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -s /etc/pure-ftpd/ssl/dhparams.pem ]; then
	umask 027
	%{_bindir}/openssl dhparam -out /etc/pure-ftpd/ssl/dhparams.pem 2048 || :
fi

/sbin/chkconfig --add %{name}
%service %{name} restart "PureFTPD daemon"

%pre
%groupadd -g 326 ftpauth
%useradd -u 326 -d %{_ftpdir} -s /bin/false -c "FTP Auth daemon" -g ftpauth ftpauth
%groupadd -g 335 ftpcert
%useradd -u 335 -d %{_ftpdir} -s /bin/false -c "FTP Cert daemon" -g ftpcert ftpcert

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove ftpauth
	%groupremove ftpauth
	%userremove ftpcert
	%groupremove ftpcert
fi

%post -n openldap-schema-pureftpd
%openldap_schema_register %{schemadir}/pureftpd.schema -d core
%service -q ldap restart

%postun -n openldap-schema-pureftpd
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/pureftpd.schema
	%service -q ldap restart
fi

%triggerpostun -- %{name} < 1.0.41-2
%{?with_mysql:sed -i -e 's#MYSQLCrypt[\t ]\+all#MYSQLCrypt    any#gi' $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd-mysql.conf}
%{?with_pgsql:sed -i -e 's#PgSQLCrypt[\t ]\+all#PgSQLCrypt    any#gi' $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd-pgsql.conf}
sed -i -e 's#SSLCertFile#CertFile#gi' $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd.conf
exit 0

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING FAQ HISTORY NEWS README* THANKS pure*.conf pureftpd.schema
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%attr(751,root,root) %config(noreplace) %verify(not md5 mtime size) %dir /etc/%{name}
%attr(750,root,ftpauth) %config(noreplace) %verify(not md5 mtime size) %dir /etc/%{name}/authd
%attr(750,root,ftpcert) %config(noreplace) %verify(not md5 mtime size) %dir /etc/%{name}/certd
# for future /etc/ftpd -> /etc/pure-ftpd/conf migration
# %attr(750,root,root) %config(noreplace) %verify(not md5 mtime size) %dir /etc/%{name}/conf
%attr(750,root,root) %config(noreplace) %verify(not md5 mtime size) %dir /etc/%{name}/ssl
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %ghost /etc/%{name}/ssl/dhparams.pem
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftpusers
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pureftpd-dir-aliases
%{?with_ldap:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pureftpd-ldap.conf}
%{?with_mysql:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pureftpd-mysql.conf}
%{?with_pgsql:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pureftpd-pgsql.conf}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pureftpd.conf
%attr(710,root,ftp) %dir %{_sysconfdir}
%dir %{_sysconfdir}/vhosts
%{_sysconfdir}/pure-ftpd
%dir %{_ftpdir}
%{_mandir}/man?/*
%lang(ja) %{_mandir}/ja/man5/ftpusers*
%lang(pl) %{_mandir}/pl/man5/ftpusers*
%lang(pt_BR) %{_mandir}/pt_BR/man5/ftpusers*
%lang(ru) %{_mandir}/ru/man5/ftpusers*

%files -n openldap-schema-pureftpd
%defattr(644,root,root,755)
%{schemadir}/pureftpd.schema
