# _with_mysql - enables MySQL auth but disables PAM auth
Summary:	Small, fast and secure FTP server
Summary(pl):	Mały, szybki i bezpieczny serwer FTP
Name:		pure-ftpd
Version:	1.0.3
Release:	1
License:	GPL
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
Source0:	http://pureftpd.sourceforge.net/files/%{name}-%{version}.tar.gz
Source1:	%{name}.pamd
Source2:	%{name}.init
Patch0:		%{name}-config.patch
URL:		http://www.pureftpd.org/
%{?_with_mysql:BuildRequires:	mysql-devel}
BuildRequires:	libcap-devel
BuildRequires:	pam-devel
BuildRequires:	automake
BuildRequires:	autoconf
Prereq:		rc-scripts
Prereq:		/sbin/chkconfig
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
Obsoletes:	troll-ftpd
Obsoletes:	wu-ftpd

%description
Pure-FTPd is a fast, production-quality, standard-comformant FTP
server, based upon Troll-FTPd. Unlike other popular FTP servers, it
has no known security flaw, it is really trivial to set up and it is
especially designed for modern Linux kernels (setfsuid, sendfile,
capabilities) . Features include PAM support, IPv6, chroot()ed home
directories, virtual domains, built-in LS, anti-warez system, bounded
ports for passive downloads...

%description -l pl
Pure-FTPD to szybki, wysokiej jakości, odpowiadający standardom serwer
FTP bazujący na Troll-FTPd. W przeciwieństwie do innych serwerów FTP
nie ma znanych luk w bezpieczeństwie. Ponadto jest trywialny w
konfiguracji i specjalnie zaprojektowany dla nowych kerneli Linuxa
(setfsuid, sendfile, capabilibies). Możliwości to wsparcie dla PAMa,
IPv6, chroot()owanych katalogów domowych, virtualne domeny, wbudowany
LS, system anty-warezowy, ograniczanie portów dla pasywnych
połączeń...

%prep
%setup -q
%patch0 -p1

%build
aclocal
autoconf
automake -a -c
%configure \
	--sysconfdir=/etc/ftpd \
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
	--with-language=english

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{pam.d,sysconfig,ftpd/vhosts,security,rc.d/init.d} \
	$RPM_BUILD_ROOT/home/ftp/Incoming

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/pam.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install contrib/redhat.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/ftpd/pureftpd.conf
install pureftpd-mysql.conf	 $RPM_BUILD_ROOT%{_sysconfdir}/ftpd/pureftpd-mysql.conf
touch $RPM_BUILD_ROOT/etc/security/blacklist.ftp

gzip -9nf README* AUTHORS ChangeLog HISTORY NEWS THANKS

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
%doc *.gz pure*.conf
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %dir /etc/ftpd
%dir %{_sysconfdir}/ftpd/vhosts
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftpd/pureftpd.conf
%{?_with_mysql:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftpd/pureftpd-mysql.conf}
%{?!_with_mysql:%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/*}
%{?!_with_mysql:%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/security/blacklist.ftp}
%dir /home/ftp
%attr(775,root,ftp) %dir /home/ftp/Incoming
%{_mandir}/man?/*
