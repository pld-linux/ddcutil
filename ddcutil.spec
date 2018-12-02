Summary:	Query and change Linux monitor settings using DDC/CI and USB
Name:		ddcutil
Version:	0.9.3
Release:	2
License:	GPL v2+
Group:		X11/Applications
Source0:	https://github.com/rockowitz/ddcutil/archive/v%{version}.tar.gz
# Source0-md5:	d676ec9ca9f6488fa5888bb39175f2d5
Patch0:		%{name}-x32.patch
URL:		http://www.ddcutil.com/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.11
BuildRequires:	libdrm-devel >= 2.4.67
BuildRequires:	libtool
BuildRequires:	libusb-devel >= 1.0.15
BuildRequires:	pkgconfig
BuildRequires:	xorg-lib-libXrandr-devel
Requires:	libdrm >= 2.4.67
Requires:	libusb >= 1.0.15
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ddcutil is a program for querying and changing monitor settings, such
as brightness and color levels.

ddcutil uses DDC/CI to communicate with monitors implementing MCCS
(Monitor Control Command Set) over I2C. Normally, the video driver for
the monitor exposes the I2C channel as devices named /dev/i2c-n. There
is also psupport for monitors (such as Apple Cinema and Eizo
ColorEdge) that implement MCCS using a USB connection.

A particular use case for ddcutil is as part of color profile
management. Monitor calibration is relative to the monitor color
settings currently in effect, e.g. red gain. ddcutil allows color
related settings to be saved at the time a monitor is calibrated, and
then restored when the calibration is applied.

%package devel
Summary:	ddcutil header files
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
ddcutil header files.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-drm \
	--enable-lib \
	--enable-usb \
	--enable-x11
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS.md README.md
%attr(755,root,root) %{_bindir}/ddcutil
%attr(755,root,root) %{_libdir}/libddcutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libddcutil.so.0
%{_mandir}/man1/ddcutil.1*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/data

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libddcutil.so
%{_includedir}/ddcutil*.h
%{_pkgconfigdir}/ddcutil.pc
%{_datadir}/%{name}/data/FindDDCUtil.cmake
