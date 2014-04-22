%define         folly        d9c79af

Name:           hhvm
Version:        3.0.1
Release:        1%{?dist}
License:        PHP-3.01
Summary:        HHVM virtual machine, runtime, and JIT for the PHP language
Url:            http://hhvm.com
Group:          Development/Languages/Other
Source:         https://github.com/facebook/hhvm/archive/HHVM-%{version}.tar.gz
Source1:        https://github.com/facebook/folly/archive/%{folly}/folly-0.1-%{folly}.tar.gz
Source2:        hhvm.init
Source3:        hhvm.sysconfig
Source4:        server.ini
Source5:        php.ini

%if 0%{?rhel} == 6
%global         p_vendor     hhvm
%global         name_prefix  %{p_vendor}-
%endif

BuildRequires:  binutils-devel
BuildRequires:	bzip2-devel
BuildRequires:	%{?name_prefix}cmake >= 2.8.7
BuildRequires:	%{?name_prefix}boost-devel >= 1.50
BuildRequires:  elfutils-libelf-devel
BuildRequires:	expat-devel
BuildRequires:	freetype-devel
BuildRequires:	%{?name_prefix}glog-devel = 0.3.2
BuildRequires:	%{?name_prefix}ImageMagick-devel >= 6.8.0
BuildRequires:	inotify-tools-devel
BuildRequires:	jemalloc-devel >= 3.0.0
BuildRequires:	libc-client-devel
BuildRequires:	libcap-devel
BuildRequires:	libcurl-devel
BuildRequires:  libdwarf-devel
BuildRequires:	libedit-devel
BuildRequires:	libevent-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libicu-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmcrypt-devel
BuildRequires:	%{?name_prefix}libmemcached-devel >= 1.0.4
BuildRequires:	libpng-devel
BuildRequires:	libselinux-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	libzip-devel
BuildRequires:	mysql-devel
BuildRequires:	ncurses-devel
BuildRequires:	numactl-devel
BuildRequires:	oniguruma-devel
BuildRequires:	%{?name_prefix}ocaml
BuildRequires:	openssl-devel
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
BuildRequires:	pcre-devel
BuildRequires:	readline-devel
BuildRequires:	%{?name_prefix}tbb-devel >= 4.0
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
%if 0%{?rhel} == 6
BuildRequires:  devtoolset-2-binutils >= 2.23.52.0.1
BuildRequires:  devtoolset-2-gcc >= 4.7.0
BuildRequires:  devtoolset-2-gcc-c++ >= 4.7.0
%else
BuildRequires:  gcc >= 4.7.0
%endif
#BuildRequires:	imap-devel
#BuildRequires:	libbz2-devel
#BuildRequires:	libelf0-devel
#BuildRequires:	libexpat-devel
#BuildRequires:	libmysqlclient-devel
#BuildRequires:	libnuma-devel
#BuildRequires:	libopenssl-devel
#BuildRequires:	libpng12-devel
#BuildRequires:	openldap2-devel
BuildRequires:	pkgconfig(libpng)

%if 0%{?rhel} == 6
Requires: %{?name_prefix}boost-filesystem >= 1.50
Requires: %{?name_prefix}boost-program-options >= 1.50
Requires: %{?name_prefix}boost-regex >= 1.50
Requires: %{?name_prefix}boost-system >= 1.50
Requires: %{?name_prefix}boost-thread >= 1.50
Requires: %{?name_prefix}glog = 0.3.2
Requires: %{?name_prefix}ImageMagick-libs >= 6.8.0
Requires: %{?name_prefix}libmemcached-libs >= 1.0.4
Requires: %{?name_prefix}tbb >= 4.0
%{?filter_setup:
%filter_from_requires /libboost.*\.so.*/d; /libMagick.*\.so.*$/d; /libglog\.so.*$/d; /libmemcached\.so.*$/d; /libtbb\.so.*$/d
%filter_setup
}
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
HHVM is an open-source virtual machine designed for executing programs
written in Hack and PHP. HHVM uses a just-in-time (JIT) compilation
approach to achieve superior performance while maintaining the
development flexibility that PHP provides. HHVM can be used with a
FastCGI-based webserver.

%package server
Summary:          Init script to start HHVM as FastCGI daemon
Group:            Development/Languages/PHP
Requires:         %{name} = %{version}-%{release}
Requires(post):   chkconfig
Requires(preun):  chkconfig
Requires(preun):  initscripts

%description server
Init script to start HHVM as FastCGI daemon

%package devel
Summary:          HHVM virtual machine, runtime, and JIT for the PHP language
Requires:         %{name} = %{version}-%{release}
Group:            Development/Languages/Other

%description devel
HHVM is an open-source virtual machine designed for executing programs
written in Hack and PHP. HHVM uses a just-in-time (JIT) compilation
approach to achieve superior performance while maintaining the
development flexibility that PHP provides.

This package contains the development files.

%prep

%setup -q -n %{name}-HHVM-%{version}
root=$(pwd)
cd hphp/submodules/folly
tar --strip-components=1 -xf %{SOURCE1}

%build
%if 0%{?rhel} == 6
. /opt/rh/devtoolset-2/enable
export PATH=/opt/hhvm/bin:$PATH
export CPATH="/opt/hhvm/include:/opt/hhvm/include/libdwarf:$CPATH"
export CPPFLAGS="-I/opt/hhvm/include -I/opt/hhvm/include/libdwarf $CPPFLAGS"
export LDFLAGS="-L/opt/hhvm/lib $LDFLAGS"
export LD_LIBRARY_PATH="/opt/hhvm/lib:$LD_LIBRARY_PATH"
%endif
export CMAKE_PREFIX_PATH=$(pwd)
cmake -DCMAKE_INSTALL_PREFIX=/usr .
make %{?_smp_mflags}

%install
%if 0%{?rhel} == 6
export PATH=/opt/hhvm/bin:$PATH
export LD_LIBRARY_PATH="/opt/hhvm/lib:$LD_LIBRARY_PATH"
%endif
%make_install
%{__install} -p -D -m 0755 hphp/hhvm/hhvm %{buildroot}%{_bindir}/hhvm
%{__install} -p -D -m 0755 hphp/tools/hphpize/hphpize %{buildroot}%{_bindir}/hphpize
%{__install} -p -D -m 0755 hphp/hack/bin/hh_client %{buildroot}%{_bindir}/hh_client
%{__install} -p -D -m 0755 hphp/hack/bin/hh_server %{buildroot}%{_bindir}/hh_server
# Remove superfluous stuff
%{__rm} %{buildroot}%{_includedir}/zip.h
%{__rm} %{buildroot}%{_includedir}/zipconf.h
%{__rm} %{buildroot}%{_prefix}/lib/libzip.a
%{__rm} %{buildroot}%{_prefix}/lib/libzip.so
# Install initscript, sysconfig and hhvm configuration
%{__install} -p -D -m 0755 %{SOURCE2} %{buildroot}%{_initddir}/hhvm
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/hhvm
%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/hhvm/server.ini
%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/hhvm/php.ini
# Create log files
%{__mkdir} -p %{buildroot}%{_localstatedir}/log/hhvm
touch %{buildroot}%{_localstatedir}/log/hhvm/access.log
touch %{buildroot}%{_localstatedir}/log/hhvm/error.log
%{__mkdir} -p %{buildroot}%{_localstatedir}/run/hhvm
touch %{buildroot}%{_localstatedir}/run/hhvm/hhvm.hhbc

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post server
/sbin/chkconfig --add hhvm

%preun server
if [ "$1" -eq 0 ]; then
    /sbin/service hhvm stop >/dev/null 2>&1
    /sbin/chkconfig --del hhvm
fi

%files
%defattr(-,root,root)
%doc README.md LICENSE.ZEND LICENSE.PHP
%{_bindir}/hhvm
%{_bindir}/hh_client
%{_bindir}/hh_server

%files server
%dir %{_sysconfdir}/hhvm
%config(noreplace) %{_sysconfdir}/hhvm/server.ini
%config(noreplace) %{_sysconfdir}/hhvm/php.ini
%config(noreplace) %{_sysconfdir}/sysconfig/hhvm
%{_initddir}/hhvm
%ghost %{_localstatedir}/log/hhvm/access.log
%ghost %{_localstatedir}/log/hhvm/error.log
%ghost %{_localstatedir}/run/hhvm/hhvm.hhbc

%files devel
%defattr(-,root,root)
%{_bindir}/hphpize

%changelog
* Tue Apr 22 2014 Alan Grosskurth <code@alan.grosskurth.ca> - 3.0.1-1
- Initial packaging
