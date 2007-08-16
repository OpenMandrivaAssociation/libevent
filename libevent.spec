%define	major 1
%define libname	%mklibname event %{major}
%define develname %mklibname -d event

Summary:	Abstract asynchronous event notification library
Name:		libevent
Version:	1.3d
Release:	%mkrel 1
Group:		System/Libraries
License:	BSD
URL:		http://www.monkey.org/~provos/libevent/
Source0:	http://www.monkey.org/~provos/%{name}-%{version}.tar.gz
Patch0:		libevent-version-info-only.diff
BuildRequires:	autoconf
BuildRequires:	libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

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
Obsoletes:	%{libname}-devel

%description -n	%{develname}
The libevent API provides a mechanism to execute a callback function when a
specific event occurs on a file descriptor or after a timeout has been reached.
libevent is meant to replace the asynchronous event loop found in event driven
network servers. An application just needs to call event_dispatch() and can
then add or remove events dynamically without having to change the event loop.

This package contains the static libevent library and its header files needed
to compile applications such as stegdetect, etc.

%prep

%setup -q
%patch0 -p0

%build
export WANT_AUTOCONF_2_5=1
rm -f configure
libtoolize --copy --force; aclocal; autoconf --force; autoheader; automake

export CFLAGS="%{optflags} -fPIC"

%configure2_5x

%make

%check
pushd test
    make verify
popd

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

# don't enforce python deps here
rm -f %{buildroot}%{_bindir}/event_rpcgen.py

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

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
%{_mandir}/man3/*
