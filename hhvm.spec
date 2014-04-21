#
# spec file for package 
#
# Copyright (c) 2014 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

Name:       hhvm
Version:	3.0.1
Release:	1.2
License:	PHP-3.01
Summary:	HHVM virtual machine, runtime, and JIT for the PHP language
Url:		http://hhvm.com
Group:		Development/Languages/Other
Source:		http://s3.amazonaws.com/cb-mirror/%{name}-%{version}.tar.gz
Source1:	http://s3.amazonaws.com/cb-mirror/folly.tar.gz
Source2:	hhvm.initscript
Source3:	hhvm.hdf
Source4:	hhvm.sysconfig

%if 0%{?rhel} == 6
BuildRequires:	hhvm-cmake
BuildRequires:	hhvm-boost-devel
BuildRequires:	freetype-devel
BuildRequires:	hhvm-glog-devel
BuildRequires:	hhvm-ImageMagick-devel
BuildRequires:	libc-client-devel
BuildRequires:	hhvm-inotify-tools-devel
BuildRequires:	bzip2-devel
BuildRequires:	hhvm-jemalloc-devel
BuildRequires:  hhvm-libdwarf-devel
BuildRequires:  elfutils-libelf-devel
BuildRequires:	expat-devel
BuildRequires:	hhvm-libmcrypt-devel
BuildRequires:	hhvm-libmemcached-devel
BuildRequires:	mysql-devel
BuildRequires:	numactl-devel
BuildRequires:	openssl-devel
BuildRequires:	libpng-devel
BuildRequires:	openldap-devel
BuildRequires:	hhvm-tbb-devel
BuildRequires:  devtoolset-2-binutils
BuildRequires:  devtoolset-2-gcc
BuildRequires:  devtoolset-2-gcc-c++
%else
BuildRequires:	cmake
BuildRequires:	binutils-devel
BuildRequires:	boost-devel
BuildRequires:	freetype2-devel
BuildRequires:	glog-devel
BuildRequires:	ImageMagick-devel
BuildRequires:	imap-devel
BuildRequires:	inotify-tools-devel
BuildRequires:	libbz2-devel
BuildRequires:	jemalloc-devel
BuildRequires:	libdwarf-devel
BuildRequires:	libelf0-devel
BuildRequires:	libexpat-devel
BuildRequires:	libmcrypt-devel
BuildRequires:	libmemcached-devel
BuildRequires:	libmysqlclient-devel
BuildRequires:	libnuma-devel
BuildRequires:	libopenssl-devel
BuildRequires:	libpng12-devel
BuildRequires:	openldap2-devel
BuildRequires:	tbb-devel
%endif

BuildRequires:	ocaml
BuildRequires:	binutils-devel
BuildRequires:	libcap-devel
BuildRequires:	libcurl-devel
BuildRequires:	libedit-devel
BuildRequires:	libevent-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libicu-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libselinux-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	libzip-devel
BuildRequires:	ncurses-devel
BuildRequires:	oniguruma-devel
BuildRequires:	pam-devel
BuildRequires:	pcre-devel
BuildRequires:	readline-devel
BuildRequires:	xz-devel
BuildRequires:	zlib-devel

BuildRequires:	pkgconfig(libpng)

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
HHVM is an open-source virtual machine designed for executing programs written in Hack and PHP. HHVM uses a just-in-time (JIT) compilation approach to achieve superior performance while maintaining the development flexibility that PHP provides.

%package devel
Summary:        HHVM virtual machine, runtime, and JIT for the PHP language
Group:          Development/Languages/Other

%description devel
HHVM is an open-source virtual machine designed for executing programs written in Hack and PHP. HHVM uses a just-in-time (JIT) compilation approach to achieve superior performance while maintaining the development flexibility that PHP provides.

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
export CMAKE_PREFIX_PATH=`pwd`
cmake -DCMAKE_INSTALL_PREFIX=/usr .
make %{?_smp_mflags}

%install
%make_install
%{__install} -p -D -m 0755 hphp/hhvm/hhvm %{buildroot}%{_bindir}/hhvm
%{__install} -p -D -m 0755 hphp/tools/hphpize/hphpize %{buildroot}%{_bindir}/hphpize

# Install initscript, sysconfig and hhvm configuration
%{__install} -p -D -m 0755 %{SOURCE2} %{buildroot}%{_initddir}/%{name}
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/hhvm/hhvm.hdf
%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/hhvm

# Create default directory
#%{__mkdir} -p %{buildroot}%{_var}/run/%{name}
#%{__mkdir} -p %{buildroot}%{_var}/log/%{name}
#%{__mkdir} -p %{buildroot}%{_var}/hhvm

%files
%defattr(-,root,root)
%doc README.md LICENSE.ZEND LICENSE.PHP
%{_bindir}/hhvm
%{_libdir}/libzip.so
%dir %{_sysconfdir}/hhvm
%config(noreplace) %{_sysconfdir}/hhvm/hhvm.hdf
%config(noreplace) %{_sysconfdir}/sysconfig/hhvm
%{_initddir}/hhvm

%files devel
%defattr(-,root,root)
%{_bindir}/hphpize
%{_includedir}/zip.h
%{_includedir}/zipconf.h
%{_libdir}/libzip.a

%changelog

