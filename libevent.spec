%define major 5
%define libname %mklibname event %{major}
%define develname %mklibname -d event

Summary:	Abstract asynchronous event notification library
Name:		libevent
Version:	2.0.21
Release:	1
Group:		System/Libraries
License:	BSD
URL:		http://www.monkey.org/~provos/libevent/
Source0:	https://github.com/downloads/libevent/libevent/%{name}-%{version}-stable.tar.gz
Source1:	https://github.com/downloads/libevent/libevent/%{name}-%{version}-stable.tar.gz.asc
Patch0:		libevent-version-info-only.diff
Patch1:		libevent-linkage_fix.diff
Patch2:		libevent-ldflags.diff
Patch3:		libevent-2.0.21-automake-1.13.patch
BuildRequires:	autoconf automake libtool
BuildRequires:	pkgconfig(openssl)
BuildRequires:	doxygen

%description
The libevent API provides a mechanism to execute a callback function when a
specific event occurs on a file descriptor or after a timeout has been reached.
libevent is meant to replace the asynchronous event loop found in event driven
network servers. An application just needs to call event_dispatch() and can
then add or remove events dynamically without having to change the event loop.

%package -n	%{libname}
Summary:	Abstract asynchronous event notification library
Group:		System/Libraries

%description -n	%{libname}
The libevent API provides a mechanism to execute a callback function when a
specific event occurs on a file descriptor or after a timeout has been reached.
libevent is meant to replace the asynchronous event loop found in event driven
network servers. An application just needs to call event_dispatch() and can
then add or remove events dynamically without having to change the event loop.

%package -n	%{develname}
Summary:	Static library and header files for the libevent library
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{develname}
The libevent API provides a mechanism to execute a callback function when a
specific event occurs on a file descriptor or after a timeout has been reached.
libevent is meant to replace the asynchronous event loop found in event driven
network servers. An application just needs to call event_dispatch() and can
then add or remove events dynamically without having to change the event loop.

This package contains the static libevent library and its header files needed
to compile applications such as stegdetect, etc.

%prep
%setup -q -n %{name}-%{version}-stable
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p1 -b .am13~

# bork
perl -pi -e "s|^GENERATE_MAN.*|GENERATE_MAN=YES|g" Doxyfile

mv -f configure.in configure.ac
autoreconf -fi

%build
export CFLAGS="%{optflags} -fPIC"

%configure2_5x --disable-static

make

# provide man pages
make doxygen
rm -f doxygen/man/man3/{major,minor,error,free}.3

%install
%makeinstall_std

# don't enforce python deps here
rm -f %{buildroot}%{_bindir}/event_rpcgen.py

# provide man pages
install -d %{buildroot}%{_mandir}/man3
install -m0644 doxygen/man/man3/*.3 %{buildroot}%{_mandir}/man3/

(cd %{buildroot}/%{_mandir}/man3/; F=`ls deprecated.3*`; mv $F libevent.$F)

%files -n %{libname}
%doc README event_rpcgen.py
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
