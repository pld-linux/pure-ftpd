Summary:	Small, fast and secure FTP server
Summary(pl):	Mały, szybki i bezpieczny serwer FTP
Name:		pure-ftpd
Version:	0.99
Release:	1
License:	GPL
Group:		Daemons
Group(pl):	Serwery
Source0:	http://prdownloads.sourceforge.net/pureftpd/%{name}-%{version}.tar.gz
Source1:	pure-ftpd.pamd
Source2:	pure-ftpd.rc-inetd
URL:		http://www.pureftpd.org/
BuildRequires:	libcap-devel
BuildRequires:	pam-devel
BuildRequires:	automake
BuildRequires:	autoconf
Requires:	inetdaemon
Requires:	rc-inetd
Provides:	ftpserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	ftpserver
Obsoletes:	bftpd
Obsoletes:	anonftp
Obsoletes:	ftpd-BSD
Obsoletes:	heimdal-ftpd
Obsoletes:	linux-ftpd
Obsoletes:	proftpd
Obsoletes:	troll-ftpd
Obsoletes:	wu-ftpd

%description
Pure-FTPd is a fast, production-quality, standard-comformant FTP server,
based upon Troll-FTPd. Unlike other popular FTP servers, it has no known
security flaw, it is really trivial to set up and it is especially designed
for modern Linux kernels (setfsuid, sendfile, capabilities) . Features
include PAM support, IPv6, chroot()ed home directories, virtual domains,
built-in LS, anti-warez system, bounded ports for passive downloads...

%description -l pl
Pure-FTPD to szybki, wysokiej jakości, odpowiadający standardom serwer FTP
bazujący na Troll-FTPd. W przeciwieństwie do innych serwerów FTP nie
ma znanych luk w bezpieczeństwie. Ponadto jest trywialny w konfiguracji
i specjalnie zaprojektowany dla nowych kerneli Linuxa (setfsuid, sendfile,
capabilibies). Możliwości to wsparcie dla PAMa, IPv6, chroot()owanych
katalogów domowych, virtualne domeny, wbudowany LS, system anty-warezowy,
ograniczanie portów dla pasywnych połączeń...

%prep
%setup -q

%build
aclocal
autoconf
automake -a -c
%configure \
	--with-cookie \
	--with-pam \
	--with-throttling \
	--with-ratios \
	--with-ftpwho \
	--with-largefile \
	--with-uploadscript \
	--with-language=english

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{pam.d,sysconfig/rc-inetd,ftpd/vhosts,security}
install -d $RPM_BUILD_ROOT/home/ftp/Incoming

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/pure-ftpd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd/ftpd

touch $RPM_BUILD_ROOT%{_sysconfdir}/security/blacklist.ftp

gzip -9nf README

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	%{_sysconfdir}/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"%{_sysconfdir}/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

%postun
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	%{_sysconfdir}/rc.d/init.d/rc-inetd restart
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %dir %{_sysconfdir}/ftpd
%dir %{_sysconfdir}/ftpd/vhosts
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pam.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sysconfig/rc-inetd/ftpd
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/security/blacklist.ftp
%dir /home/ftp
%attr(755,ftp,ftp) %dir /home/ftp/Incoming

%{_mandir}/man?/*
