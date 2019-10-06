%bcond_without nox
#debuginfo-without-sources
%define debug_package	%{nil}
%define gitdate 06.10.2019
Name:		qbittorrent
Version:	4.2.0
Summary:	A lightweight but featureful BitTorrent client
Group:		Networking/File transfer
License:	GPLv2+
Url:		http://qbittorrent.sourceforge.net/
%if "%gitdate" != ""
Source0:	qBittorrent-master-%{gitdate}.zip
Release:	0
%else
Source0:	http://downloads.sourceforge.net/project/qbittorrent/qbittorrent/qbittorrent-%{version}/qbittorrent-%{version}.tar.gz
# Patch for fix build issue introduced in qbittorrent 4.1.4 on non x64bit arch like armv7 or i686. (penguin)
# /src/base/utils/fs.cpp:346:10: error: case value evaluates to 4283649346, which cannot be narrowed to type '__fsword_t' (aka 'int') [-Wc++11-narrowing]
Patch0:		qbittorrent-x86-build-fix.patch
Release:	1
%endif
BuildRequires:	boost-devel
BuildRequires:	qmake5
BuildRequires:	qt5-linguist-tools
BuildRequires:	pkgconfig(libtorrent-rasterbar)
BuildRequires:	pkgconfig(Qt5Concurrent)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(openssl)
#BuildRequires:	qtchooser
Requires:	python
Requires:	geoip

%description
A lightweight but feature-full BitTorrent client that aims to be very easy 
to use. It is multi-platform and provides a Qt4 graphical interface.

%package -n %{name}-nox
Summary:	A Headless Bittorrent Client
Group:		Networking/File transfer

%description -n %{name}-nox
A Headless Bittorrent Client with a feature rich Web UI allowing users to
control the clinet remotely.

%prep
%if "%gitdate" != ""
%setup -q -n qBittorent-master-%{gitdate}
%else
%setup -q
%endif
%patch0 -p0

%build
%ifarch %{armx}
export CC=gcc
export CXX=g++
%endif
%setup_compile_flags

sed -i -e 's,@QBT_CONF_EXTRA_CFLAGS@,@QBT_CONF_EXTRA_CFLAGS@ -std=gnu++1y,' conf.pri.in

# headless aka nox
%if %{with nox}
%__mkdir build-nox
pushd build-nox
  ../configure	--prefix=%{_prefix} \
		--disable-gui \
		--with-qt5
  %__cp conf.pri ..
  sed -i -e 's/-fno-exceptions//' src/Makefile
  %make
  %__mv -f ../conf.pri ../conf.pri.nox
popd
%endif

# GUI
mkdir build-gui
pushd build-gui
  ../configure	--prefix=%{_prefix} --with-qt5
  cp conf.pri ..
  sed -i -e 's/-fno-exceptions//' src/Makefile
  %make 
  mv -f ../conf.pri ../conf.pri.gui
popd

%install
# install headless part
%if %{with nox}
cp -f conf.pri.nox conf.pri
pushd build-nox
  make INSTALL_ROOT=%{buildroot} install
popd
%endif

# install gui
cp -f conf.pri.gui conf.pri
pushd build-gui
  make INSTALL_ROOT=%{buildroot} install
popd

%files
%doc AUTHORS Changelog COPYING NEWS TODO
%{_bindir}/%{name}
%{_datadir}/applications/org.%{name}.qBittorrent.desktop
%{_iconsdir}/hicolor/*/status/%{name}-tray.png
%{_iconsdir}/hicolor/*/status/%{name}-tray*.svg
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/qbittorrent.png
%{_datadir}/metainfo/org.%{name}.qBittorrent.appdata.xml
%{_mandir}/man1/%{name}.1*

%if %{with nox}
%files -n  %{name}-nox
%{_bindir}/%{name}-nox
%{_mandir}/man1/%{name}-nox.1*
%endif
