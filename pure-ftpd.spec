Summary:	Small, fast and secure FTP server
Summary(pl):	Ma³y, szybki i bezpieczny serwer FTP
Name:		pure-ftpd
Version:	0.95 
Release:	1
License:	GPL
Group:		Daemons
Group(pl):	Serwery
Source0:	http://download.sourceforge.net/pureftpd/%{name}-%{version}.tar.gz
Source1:	pure-ftpd.pamd
Source2:	pure-ftpd.rc-inetd
Patch0:		pure-ftpd-macro.patch
URL:		http://pureftpd.sourceforge.net/
BuildRequires:	libcap-devel
BuildRequires:	pam-devel
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
Pure-FTPD to szybki, wysokiej jako¶ci, odpowiadaj±cy standardom serwer FTP
bazuj±cy na Troll-FTPd. W przeciwieñstwie do innych serwerów FTP nie
ma znanych luk w bezpieczeñstwie. Ponadto jest trywialny w konfiguracji
i specjalnie zaprojektowany dla nowych kerneli Linuxa (setfsuid, sendfile,
capabilibies). Mo¿liwo¶ci to wsparcie dla PAMa, IPv6, chroot()owanych
katalogów domowych, virtualne domeny, wbudowany LS, system anty-warezowy,
ograniczanie portów dla pasywnych po³±czeñ...

%prep
%setup -q
%patch -p1

%build
%configure \
	--with-cookie \
	--with-pam

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/{pam.d,sysconfig/rc-inetd,ftpd/vhosts,security} \
	$RPM_BUILD_ROOT/home/ftp/{upload,pub}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/pure-ftpd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/rc-inetd/ftpd

touch $RPM_BUILD_ROOT/etc/security/blacklist.ftp

gzip -9nf README

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

%postun
if [ "$1" = "0" -a -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart
fi

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,root) %config /etc/sysconfig/rc-inetd/ftpd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/*
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) /etc/security/blacklist.ftp
%attr(755,ftp,ftp) %dir /home/ftp/upload
%dir /home/ftp 
%dir /home/ftp/pub 
%dir %{_sysconfdir}/ftpd/vhosts

%{_mandir}/man*/*
