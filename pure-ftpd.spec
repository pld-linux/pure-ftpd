#
# Conditional build:
# _without_mysql - disable MySQL auth but disables PAM auth
# _without_ldap  - disable LDAP auth
# _without_pgsql - disable PostgreSQL support
# _without_tls   - support SSL/TLS
#
Summary:	Small, fast and secure FTP server
Summary(pl):	Ma³y, szybki i bezpieczny serwer FTP
Name:		pure-ftpd
Version:	1.0.16a
Release:	2
Epoch:		0
License:	BSD-like
Group:		Daemons
Source0:	ftp://ftp.pureftpd.org/pub/pure-ftpd/releases/%{name}-%{version}.tar.bz2
# Source0-md5:	9bb8e85367bda9a63afdcbe6e2d26c71
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	ftpusers.tar.bz2
# Source3-md5:	76c80b6ec9f4d079a1e27316edddbe16
URL:		http://www.pureftpd.org/
BuildRequires:	libcap-devel
%{!?_without_mysql:BuildRequires:	mysql-devel}
%{!?_without_ldap:BuildRequires:	openldap-devel}
%{!?_without_tls:BuildRequires:		openssl-devel}
%{!?_without_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	pam-devel
Prereq:		rc-scripts
Requires(post,preun):/sbin/chkconfig
Provides:	ftpserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	ftpserver
Obsoletes:	anonftp
Obsoletes:	bftpd
Obsoletes:	ftpd-BSD
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

%define		_sysconfdir	/etc/ftpd

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
(setfsuid, sendfile, capabilibies). Mo¿liwo¶ci to wsparcie dla PAMa,
IPv6, chroot()owanych katalogów domowych, virtualne domeny, wbudowany
LS, system anty-warezowy, ograniczanie portów dla pasywnych
po³±czeñ...

%prep
%setup -q

%build
%configure \
	--with-altlog \
	--with-puredb \
	--with-extauth \
	--with-pam \
	--with-cookie \
	--with-throttling \
	--with-ratios \
	--with-quotas \
	--with-ftpwho \
	--with-largefile \
	--with-uploadscript \
	--with-virtualhosts \
	--with-virtualchroot \
	--with-diraliases \
	--with-peruserlimits \
	%{!?_without_mysql:CPPFLAGS="-I%{_includedir}/mysql" --with-mysql} \
	%{!?_without_pgsql:--with-pgsql} \
	%{!?_without_ldap:--with-ldap} \
	%{!?_without_tls: --with-tls} \
	--with-language=english \
	--with-privsep

echo '#define	TLS_CERTIFICATE_PATH	"%{_sysconfdir}/ssl/pure-ftpd.pem"' >> config.h

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{pam.d,sysconfig,security,rc.d/init.d} \
	$RPM_BUILD_ROOT{%{_sysconfdir}/{vhosts,ssl},/home/services/ftp/Incoming}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%{!?_without_ldap:install pureftpd-ldap.conf $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd-ldap.conf}
%{!?_without_mysql:install pureftpd-mysql.conf $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd-mysql.conf}
%{!?_without_pgsql:install pureftpd-pgsql.conf $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd-pgsql.conf}
install configuration-file/pure-ftpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd.conf
install configuration-file/pure-config.pl $RPM_BUILD_ROOT%{_sbindir}
touch $RPM_BUILD_ROOT/etc/security/blacklist.ftp

ln -s vhosts $RPM_BUILD_ROOT%{_sysconfdir}/pure-ftpd

bzip2 -dc %{SOURCE3} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

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
%doc README* AUTHORS ChangeLog HISTORY NEWS THANKS pure*.conf
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/security/blacklist.ftp
%{!?_without_ldap:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pureftpd-ldap.conf}
%{!?_without_mysql:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pureftpd-mysql.conf}
%{!?_without_pgsql:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pureftpd-pgsql.conf}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pureftpd.conf
%attr(710,root,ftp) %dir %{_sysconfdir}
%dir %{_sysconfdir}/vhosts
%dir %{_sysconfdir}/pure-ftpd
%{!?_without_tls:%dir %{_sysconfdir}/ssl}
%dir /home/services/ftp
%attr(775,root,ftp) %dir /home/services/ftp/Incoming
%{_mandir}/man?/*
%lang(ja) %{_mandir}/ja/man5/ftpusers*
%lang(pl) %{_mandir}/pl/man5/ftpusers*
%lang(pt_BR) %{_mandir}/pt_BR/man5/ftpusers*
%lang(ru) %{_mandir}/ru/man5/ftpusers*
