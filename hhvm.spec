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

Name:           hhvm
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
BuildRequires:	ocaml
%if 0%{?rhel} == 6
BuildRequires:	cmake28
%else
BuildRequires:	cmake
%endif
BuildRequires:	binutils-devel
BuildRequires:	boost-devel
BuildRequires:	freetype2-devel
%if 0%{?rhel} == 6
BuildRequires:  gcc48
BuildRequires:  gcc48-c++
%endif
BuildRequires:	glog-devel
BuildRequires:	ImageMagick-devel
BuildRequires:	imap-devel
BuildRequires:	inotify-tools-devel
BuildRequires:	jemalloc-devel
BuildRequires:	libbz2-devel
BuildRequires:	libcap-devel
BuildRequires:	libcurl-devel
BuildRequires:	libdwarf-devel
BuildRequires:	libedit-devel
BuildRequires:	libelf0-devel
BuildRequires:	libevent-devel
BuildRequires:	libexpat-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libicu-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libmcrypt-devel
BuildRequires:	libmemcached-devel
BuildRequires:	libmysqlclient-devel
BuildRequires:	libnuma-devel
BuildRequires:	libopenssl-devel
BuildRequires:	libpng12-devel
BuildRequires:	libselinux-devel
BuildRequires:	libxml2-devel
BuildRequires:	libxslt-devel
BuildRequires:	libzip-devel
BuildRequires:	ncurses-devel
BuildRequires:	oniguruma-devel
BuildRequires:	openldap2-devel
BuildRequires:	pam-devel
BuildRequires:	pcre-devel
BuildRequires:	readline-devel
BuildRequires:	tbb-devel
BuildRequires:	xz-devel
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	fdupes
#Requires(post):	%insserv_prereq %fillup_prereq
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
# % configure
export CMAKE_PREFIX_PATH=`pwd`
%if 0%{?rhel} == 6
cmake28 \
%else
cmake \
%endif
  -DCMAKE_INSTALL_PREFIX=/usr -DLIBINOTIFY_LIBRARY=/usr/lib64/libinotifytools.so .
make %{?_smp_mflags}

%install
%make_install
export DONT_STRIP=1
rm -rf $RPM_BUILD_ROOT
%{__install} -p -D -m 0755 hphp/hhvm/hhvm %{buildroot}%{_bindir}/hhvm
%{__install} -p -D -m 0755 hphp/tools/hphpize/hphpize %{buildroot}%{_bindir}/hphpize

# Install initscript, sysconfig and hhvm configuration
%{__install} -p -D -m 0755 %{SOURCE2} %{buildroot}%{_initddir}/%{name}
%{__install} -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/hhvm/hhvm.hdf
%{__install} -p -D -m 0644 %{SOURCE4} %{buildroot}/var/adm/fillup-templates/sysconfig.%{name}

%{__mkdir} -p %{buildroot}/%{_sbindir}
ln -s %{_initddir}/%{name} %{buildroot}/%{_sbindir}/rc%{name}

# Create default directory
#%{__mkdir} -p %{buildroot}%{_var}/run/%{name}
#%{__mkdir} -p %{buildroot}%{_var}/log/%{name}
#%{__mkdir} -p %{buildroot}%{_var}/hhvm

%fdupes -s %{buildroot}/%{_sbindir}

%post
%fillup_and_insserv


%preun
%stop_on_removal

%postun
%restart_on_update
%insserv_cleanup

%files
%defattr(-,root,root)
%doc README.md LICENSE.ZEND LICENSE.PHP
%{_bindir}/hhvm
%{_sbindir}/rchhvm
%dir /etc/hhvm
/var/adm/fillup-templates/sysconfig.%{name}
%config(noreplace) /etc/hhvm/hhvm.hdf
%config(noreplace) /etc/init.d/hhvm

%files devel
%defattr(-,root,root)
%{_bindir}/hphpize

%changelog

