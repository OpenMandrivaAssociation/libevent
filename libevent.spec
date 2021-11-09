# libevent is used by avahi,
# avahi is used by pulseaudio,
# pulseaudio is used by wine
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define api 2.1
%define major 7
%define libname %mklibname event %{api} %{major}
%define libcore %mklibname event_core %{api} %{major}
%define libextra %mklibname event_extra %{api} %{major}
%define libopenssl %mklibname event_openssl %{api} %{major}
%define libpthreads %mklibname event_pthreads %{api} %{major}
%define devname %mklibname -d event
%define lib32name %mklib32name event %{api} %{major}
%define lib32core %mklib32name event_core %{api} %{major}
%define lib32extra %mklib32name event_extra %{api} %{major}
%define lib32openssl %mklib32name event_openssl %{api} %{major}
%define lib32pthreads %mklib32name event_pthreads %{api} %{major}
%define dev32name %mklib32name -d event

%global optflags %{optflags} -fPIC -O3 -lpthread

Summary:	Abstract asynchronous event notification library
Name:		libevent
Version:	2.1.12
Release:	2
Group:		System/Libraries
License:	BSD
Url:		http://www.monkey.org/~provos/libevent/
Source0:	http://github.com/libevent/libevent/releases/download/release-%{version}-stable/%{name}-%{version}-stable.tar.gz
Patch1:         libevent-linkage_fix.patch
BuildRequires:	pkgconfig(python)
BuildRequires:	doxygen
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)
%if %{with compat32}
BuildRequires:	devel(libssl)
BuildRequires:	devel(libz)
%endif

%description
The libevent API provides a mechanism to execute a callback function when a
specific event occurs on a file descriptor or after a timeout has been reached.
libevent is meant to replace the asynchronous event loop found in event driven
network servers. An application just needs to call event_dispatch() and can
then add or remove events dynamically without having to change the event loop.

%package -n %{libname}
Summary:	Abstract asynchronous event notification library
Group:		System/Libraries

%description -n %{libname}
The libevent API provides a mechanism to execute a callback function when a
specific event occurs on a file descriptor or after a timeout has been reached.
libevent is meant to replace the asynchronous event loop found in event driven
network servers. An application just needs to call event_dispatch() and can
then add or remove events dynamically without having to change the event loop.

%package -n %{libcore}
Summary:	Abstract asynchronous event notification library
Group:		System/Libraries

%description -n %{libcore}
This package contains a shared library for %{name}.

%package -n %{libextra}
Summary:	Abstract asynchronous event notification library
Group:		System/Libraries

%description -n %{libextra}
This package contains a shared library for %{name}.

%package -n %{libopenssl}
Summary:	Abstract asynchronous event notification library
Group:		System/Libraries

%description -n %{libopenssl}
This package contains a shared library for %{name}.

%package -n %{libpthreads}
Summary:	Abstract asynchronous event notification library
Group:		System/Libraries

%description -n %{libpthreads}
This package contains a shared library for %{name}.

%package -n %{devname}
Summary:	Development library and header files for the libevent library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libcore} = %{version}-%{release}
Requires:	%{libextra} = %{version}-%{release}
Requires:	%{libopenssl} = %{version}-%{release}
Requires:	%{libpthreads} = %{version}-%{release}

%description -n %{devname}
This package contains the development files for %{name}.

%if %{with compat32}
%package -n %{lib32name}
Summary:	Abstract asynchronous event notification library (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
The libevent API provides a mechanism to execute a callback function when a
specific event occurs on a file descriptor or after a timeout has been reached.
libevent is meant to replace the asynchronous event loop found in event driven
network servers. An application just needs to call event_dispatch() and can
then add or remove events dynamically without having to change the event loop.

%package -n %{lib32core}
Summary:	Abstract asynchronous event notification library (32-bit)
Group:		System/Libraries

%description -n %{lib32core}
This package contains a shared library for %{name}.

%package -n %{lib32extra}
Summary:	Abstract asynchronous event notification library (32-bit)
Group:		System/Libraries

%description -n %{lib32extra}
This package contains a shared library for %{name}.

%package -n %{lib32openssl}
Summary:	Abstract asynchronous event notification library (32-bit)
Group:		System/Libraries

%description -n %{lib32openssl}
This package contains a shared library for %{name}.

%package -n %{lib32pthreads}
Summary:	Abstract asynchronous event notification library (32-bit)
Group:		System/Libraries

%description -n %{lib32pthreads}
This package contains a shared library for %{name}.

%package -n %{dev32name}
Summary:	Development library and header files for the libevent library (32-bit)
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}
Requires:	%{lib32core} = %{version}-%{release}
Requires:	%{lib32extra} = %{version}-%{release}
Requires:	%{lib32openssl} = %{version}-%{release}
Requires:	%{lib32pthreads} = %{version}-%{release}

%description -n %{dev32name}
This package contains the development files for %{name}.
%endif

%prep
%autosetup -n %{name}-%{version}-stable -p1
./autogen.sh
# bork
sed -i -e "s|^GENERATE_MAN.*|GENERATE_MAN=YES|g" Doxyfile

export CONFIGURE_TOP="$(pwd)"
%if %{with compat32}
mkdir -p build32/test
cd build32
%configure32
cd ..
%endif

mkdir -p build/test
cd build
%configure

%build
%if %{with compat32}
%make_build -C build32
%endif
%make_build -C build

# provide man pages
doxygen Doxyfile

%install
%if %{with compat32}
%make_install -C build32
%endif
%make_install -C build

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
%{_bindir}/event_rpcgen.py
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libevent-%{api}.so.%{major}*

%files -n %{lib32core}
%{_prefix}/lib/libevent_core-%{api}.so.%{major}*

%files -n %{lib32extra}
%{_prefix}/lib/libevent_extra-%{api}.so.%{major}*

%files -n %{lib32openssl}
%{_prefix}/lib/libevent_openssl-%{api}.so.%{major}*

%files -n %{lib32pthreads}
%{_prefix}/lib/libevent_pthreads-%{api}.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/*.so
%{_prefix}/lib/pkgconfig/*.pc
%endif
