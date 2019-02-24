#
# Conditional build:
%bcond_without	cython	# Python extension based on Cython

Summary:	Query and change Linux monitor settings using DDC/CI and USB
Summary(pl.UTF-8):	Odczyt i zmiana ustawień monitora spod Linuksa przy użyciu DDC/CI i USB
Name:		ddcutil
Version:	0.9.5
Release:	1
License:	GPL v2+
Group:		X11/Applications
#Source0Download: https://github.com/rockowitz/ddcutil/releases
#TODO: use release tarballs: https://github.com/rockowitz/ddcutil/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source0:	https://github.com/rockowitz/ddcutil/archive/v%{version}.tar.gz
# Source0-md5:	de8d51d2101bb1cfb4d42f9a4373b6f4
Patch0:		%{name}-python.patch
URL:		http://www.ddcutil.com/
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.11
BuildRequires:	glib2-devel >= 1:2.32
BuildRequires:	libdrm-devel >= 2.4.67
BuildRequires:	libtool >= 2:2
BuildRequires:	libusb-devel >= 1.0.15
BuildRequires:	pkgconfig
%if %{with cython}
BuildRequires:	python-Cython
BuildRequires:	python-devel >= 1:2.6
BuildRequires:	python3-Cython
BuildRequires:	python3-devel >= 1:3.2
%endif
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	zlib-devel
Requires:	libdrm >= 2.4.67
Requires:	libusb >= 1.0.15
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ddcutil is a program for querying and changing monitor settings, such
as brightness and color levels.

ddcutil uses DDC/CI to communicate with monitors implementing MCCS
(Monitor Control Command Set) over I2C. Normally, the video driver for
the monitor exposes the I2C channel as devices named /dev/i2c-n. There
is also support for monitors (such as Apple Cinema and Eizo
ColorEdge) that implement MCCS using a USB connection.

A particular use case for ddcutil is as part of color profile
management. Monitor calibration is relative to the monitor color
settings currently in effect, e.g. red gain. ddcutil allows color
related settings to be saved at the time a monitor is calibrated, and
then restored when the calibration is applied.

%description -l pl.UTF-8
ddcutil to program do odczytu i zmiany ustawień monitora, takich jak
jasność i poziomy kolorów.

ddcutil wykorzystuje DDC/CI do komunikacji z monitorami obsługującymi
MCCS (Monitor Control Command Set) po I2C. Zwykle sterownik obrazu dla
monitora udostępnia kanał I2C jako urządzenia o nazwie /dev/i2c-n.
Jest także obsługa monitorów obsługujących MCCS po połączeniu USB (jak
Apple Cinema czy Eizo ColorEdge).

Szczególnym przypadkiem użycia ddcutil jest część zarządzania
profilami kolorów. Kalibracja monitora jest względem obecnych ustawień
kolorów monitora, np. współczynnika czerwieni. ddcutil pozwala na
zapisanie ustawień związanych z kolorami w czasie kalibracji monitora,
a następnie odtwarzanie ich przy aplikowaniu kalibracji.

%package devel
Summary:	ddcutil header files
Summary(pl.UTF-8):	Pliki nagłówkowe ddcutil
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.32
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXrandr-devel

%description devel
ddcutil header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe ddcutil.

%package -n python-cyddc
Summary:	Python 2 interface for ddcutil library
Summary(pl.UTF-8):	Interfejs Pythona 2 do biblioteki ddcutil
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-cyddc
Python 2 (Cython based) interface for ddcutil library.

%description -n python-cyddc -l pl.UTF-8
Interfejs Pythona 2 do biblioteki ddcutil, oparty na Cythonie.

%package -n python3-cyddc
Summary:	Python 3 interface for ddcutil library
Summary(pl.UTF-8):	Interfejs Pythona 3 do biblioteki ddcutil
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-cyddc
Python 3 (Cython based) interface for ddcutil library.

%description -n python3-cyddc -l pl.UTF-8
Interfejs Pythona 3 do biblioteki ddcutil, oparty na Cythonie.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
# no --enable-gobject-api: "GObject implementation has been mothballed. TODO: delete or comment out this section"
%configure \
	--disable-silent-rules \
	%{?with_cython:--enable-cython} \
	--enable-drm \
	--enable-lib \
	--enable-usb \
	--enable-x11
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	resfiles=

# distribute "resfiles" over destinations
install -d $RPM_BUILD_ROOT%{_datadir}/cmake/Modules \
	$RPM_BUILD_ROOT/etc/{X11/xorg.conf.d,udev/rules.d}
cp -p data/usr/share/cmake/Modules/FindDDCUtil.cmake $RPM_BUILD_ROOT%{_datadir}/cmake/Modules
# need customization if ever used
#cp -p data/etc/udev/rules.d/*.rules $RPM_BUILD_ROOT/etc/udev/rules.d
# xorg-driver-* package?
#cp -p data/etc/X11/xorg.conf.d/*.conf $RPM_BUILD_ROOT/etc/X11/xorg.conf.d

%if %{with cython}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/*.la
%{__rm} $RPM_BUILD_ROOT%{py3_sitedir}/*.la
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS.md README.md data/etc/udev/rules.d/*.rules data/etc/X11/xorg.conf.d/*.conf
%attr(755,root,root) %{_bindir}/ddcutil
%attr(755,root,root) %{_libdir}/libddcutil.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libddcutil.so.0
%{_mandir}/man1/ddcutil.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libddcutil.so
%{_includedir}/ddcutil*.h
%{_pkgconfigdir}/ddcutil.pc
%{_datadir}/cmake/Modules/FindDDCUtil.cmake

%if %{with cython}
%files -n python-cyddc
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/cyddc2.so

%files -n python3-cyddc
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/cyddc3.so
%endif
