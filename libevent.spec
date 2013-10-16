%define api	2.0
%define major	5
%define libname	%mklibname event %{api} %{major}
%define	libcore %mklibname event_core %{api} %{major}
%define	libextra %mklibname event_extra %{api} %{major}
%define	libopenssl %mklibname event_openssl %{api} %{major}
%define	libpthreads %mklibname event_pthreads %{api} %{major}
%define devname	%mklibname -d event

Summary:	Abstract asynchronous event notification library
Name:		libevent
Version:	2.0.21
Release:	6
Group:		System/Libraries
License:	BSD
Url:		http://www.monkey.org/~provos/libevent/
Source0:	http://cloud.github.com/downloads/libevent/libevent/%{name}-%{version}-stable.tar.gz
Source1:	http://cloud.github.com/downloads/libevent/libevent/%{name}-%{version}-stable.tar.gz.asc
#Patch0:		libevent-version-info-only.diff
Patch1:		libevent-linkage_fix.diff
#Patch2:		libevent-ldflags.diff
Patch3:		libevent-2.0.21-automake-1.13.patch
BuildRequires:	doxygen
BuildRequires:	libtool
BuildRequires:	pkgconfig(openssl)

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

%package -n	%{libcore}
Summary:	Abstract asynchronous event notification library
Group:		System/Libraries

%description -n	%{libcore}
This package contains a shared library for %{name}.

%package -n	%{libextra}
Summary:	Abstract asynchronous event notification library
Group:		System/Libraries

%description -n	%{libextra}
This package contains a shared library for %{name}.

%package -n	%{libopenssl}
Summary:	Abstract asynchronous event notification library
Group:		System/Libraries

%description -n	%{libopenssl}
This package contains a shared library for %{name}.

%package -n	%{libpthreads}
Summary:	Abstract asynchronous event notification library
Group:		System/Libraries

%description -n	%{libpthreads}
This package contains a shared library for %{name}.

%package -n	%{devname}
Summary:	Development library and header files for the libevent library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libcore} = %{version}-%{release}
Requires:	%{libextra} = %{version}-%{release}
Requires:	%{libopenssl} = %{version}-%{release}
Requires:	%{libpthreads} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the development files for %{name}.

%prep
%setup -qn %{name}-%{version}-stable
%apply_patches

# bork
sed -i -e "s|^GENERATE_MAN.*|GENERATE_MAN=YES|g" Doxyfile

mv -f configure.in configure.ac
autoreconf -fi

%build
export CFLAGS="%{optflags} -fPIC"
%configure2_5x --disable-static

%make

# provide man pages
make doxygen
rm -f doxygen/man/man3/{major,minor,error,free}.3

%install
%makeinstall_std

# provide man pages
install -d %{buildroot}%{_mandir}/man3
install -m0644 doxygen/man/man3/*.3 %{buildroot}%{_mandir}/man3/

(cd %{buildroot}/%{_mandir}/man3/; F=`ls deprecated.3*`; mv $F libevent.$F)

%files -n %{libname}
%{_libdir}/libevent-%{api}.so.%{major}*

%files -n %{libcore}
%{_libdir}/libevent_core-%{api}.so.%{major}*

%files -n %{libextra}
%{_libdir}/libevent_extra-%{api}.so.%{major}*

%files -n %{libopenssl}
%{_libdir}/libevent_openssl-%{api}.so.%{major}*

%files -n %{libpthreads}
%{_libdir}/libevent_pthreads-%{api}.so.%{major}*

%files -n %{devname}
%doc README
%{_bindir}/event_rpcgen.py
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

