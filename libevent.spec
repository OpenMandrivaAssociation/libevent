%define	major 5
%define libname	%mklibname event %{major}
%define develname %mklibname -d event

Summary:	Abstract asynchronous event notification library
Name:		libevent
Version:	2.0.10
Release:	%mkrel 2
Group:		System/Libraries
License:	BSD
URL:		http://www.monkey.org/~provos/libevent/
Source0:	http://www.monkey.org/~provos/%{name}-%{version}-stable.tar.gz
Source1:	http://www.monkey.org/~provos/%{name}-%{version}-stable.tar.gz.asc
Patch0:		libevent-version-info-only.diff
Patch1:		libevent-linkage_fix.diff
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRequires:	openssl-devel
BuildRequires:	doxygen
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The libevent API provides a mechanism to execute a callback function when a
specific event occurs on a file descriptor or after a timeout has been reached.
libevent is meant to replace the asynchronous event loop found in event driven
network servers. An application just needs to call event_dispatch() and can
then add or remove events dynamically without having to change the event loop.

%package -n	%{libname}
Summary:	Abstract asynchronous event notification library
Group:          System/Libraries

%description -n	%{libname}
The libevent API provides a mechanism to execute a callback function when a
specific event occurs on a file descriptor or after a timeout has been reached.
libevent is meant to replace the asynchronous event loop found in event driven
network servers. An application just needs to call event_dispatch() and can
then add or remove events dynamically without having to change the event loop.

%package -n	%{develname}
Summary:	Static library and header files for the libevent library
Group:		Development/C
Provides:	%{name}-devel = %{version}
Requires:	%{libname} = %{version}
Obsoletes:	%{mklibname -d event 2}

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

%build
autoreconf -fi

export CFLAGS="%{optflags} -fPIC"

%configure2_5x

make

# provide man pages
make doxygen
rm -f doxygen/man/man3/{major,minor,error,free}.3

#%%check
#pushd test
#    make verify
#popd

%install
rm -rf %{buildroot}

%makeinstall_std

# don't enforce python deps here
rm -f %{buildroot}%{_bindir}/event_rpcgen.py

# provide man pages
install -d %{buildroot}%{_mandir}/man3
install -m0644 doxygen/man/man3/*.3 %{buildroot}%{_mandir}/man3/

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files -n %{libname}
%defattr(-,root,root)
%doc README event_rpcgen.py
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*
