#
# Conditional build:
# _with_mysql - enables MySQL auth but disables PAM auth
# _with_ldap  - enabled LDAP auth
#
Summary:	Small, fast and secure FTP server
Summary(pl):	Ma�y, szybki i bezpieczny serwer FTP
Name:		pure-ftpd
Version:	1.0.12
Release:	2
Epoch:		0
License:	GPL
Group:		Daemons
Source0:	ftp://ftp.pureftpd.org/pub/pure-ftpd/releases/%{name}-%{version}.tar.bz2
Source1:	%{name}.pamd
Source2:	%{name}.init
Source3:	ftpusers.tar.bz2
Patch0:		%{name}-config.patch
URL:		http://www.pureftpd.org/
BuildRequires:	libcap-devel
%{?_with_mysql:BuildRequires:	mysql-devel}
%{?_with_ldap:BuildRequires:	openldap-devel}
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

%define		_	sysconfdir	/etc/ftpd

%description
Pure-FTPd is a fast, production-quality, standard-comformant FTP
server, based upon Troll-FTPd. Unlike other popular FTP servers, it
has no known security flaw, it is really trivial to set up and it is
especially designed for modern Linux kernels (setfsuid, sendfile,
capabilities) . Features include PAM support, IPv6, chroot()ed home
directories, virtual domains, built-in LS, anti-warez system, bounded
ports for passive downloads...

%description -l pl
Pure-FTPD to szybki, wysokiej jako�ci, odpowiadaj�cy standardom serwer
FTP bazuj�cy na Troll-FTPd. W przeciwie�stwie do innych serwer�w FTP
nie ma znanych luk w bezpiecze�stwie. Ponadto jest trywialny w
konfiguracji i specjalnie zaprojektowany dla nowych kerneli Linuksa
(setfsuid, sendfile, capabilibies). Mo�liwo�ci to wsparcie dla PAMa,
IPv6, chroot()owanych katalog�w domowych, virtualne domeny, wbudowany
LS, system anty-warezowy, ograniczanie port�w dla pasywnych
po��cze�...

%prep
%setup -q
%patch0 -p1

%build
%configure \
	%{?_with_mysql:CPPFLAGS="-I%{_includedir}/mysql" --with-mysql} \
	--with-altlog \
	--with-puredb \
	%{?!_with_mysql:--with-pam} \
	--with-cookie \
	--with-throttling \
	--with-ratios \
	--with-quotas \
	--with-ftpwho \
	--with-largefile \
	--with-uploadscript \
	--with-virtualhosts \
	--with-language=english \
	--with-virtualchroot \
	%{?_with_ldap:--with-ldap}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{pam.d,sysconfig,ftpd/vhosts,security,rc.d/init.d} \
	$RPM_BUILD_ROOT/home/ftp/Incoming

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install contrib/redhat.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd.conf
install pureftpd-mysql.conf	 $RPM_BUILD_ROOT%{_sysconfdir}/pureftpd-mysql.conf
touch $RPM_BUILD_ROOT/etc/security/blacklist.ftp

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
%dir %{_sysconfdir}/ftpd/vhosts
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{?!_with_mysql:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/*}
%{?!_with_mysql:%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/security/blacklist.ftp}
%attr(740,root,root) %dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pureftpd.conf
%{?_with_mysql:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pureftpd-mysql.conf}
%dir /home/ftp
%attr(775,root,ftp) %dir /home/ftp/Incoming
%{_mandir}/man?/*
%lang(ja) %{_mandir}/ja/man5/ftpusers*
%lang(pl) %{_mandir}/pl/man5/ftpusers*
%lang(pt_BR) %{_mandir}/pt_BR/man5/ftpusers*
%lang(ru) %{_mandir}/ru/man5/ftpusers*
