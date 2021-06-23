%bcond_without nox
%define gitdate %{nil}

Name:		qbittorrent
Version:	4.3.5
Summary:	A lightweight but featureful BitTorrent client
Group:		Networking/File transfer
License:	GPLv2+
Url:		http://qbittorrent.sourceforge.net/
%if "%gitdate" != ""
Source0:	qBittorrent-master-%{gitdate}.zip
Release:	0.beta.1
%else
Source0:	http://downloads.sourceforge.net/project/qbittorrent/qbittorrent/qbittorrent-%{version}/qbittorrent-%{version}.tar.xz
Release:	2
%endif
# Patch for fix build issue introduced in qbittorrent 4.1.4 on non x64bit arch like armv7 or i686. (penguin)
# /src/base/utils/fs.cpp:346:10: error: case value evaluates to 4283649346, 
# which cannot be narrowed to type '__fsword_t' (aka 'int') [-Wc++11-narrowing]
#Patch0:		qbittorrent-x86-build-fix.patch
BuildRequires:	boost-devel
BuildRequires:	qmake5
BuildRequires:	qt5-linguist-tools
BuildRequires:	pkgconfig(libtorrent-rasterbar) >= 2.0.0
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
BuildRequires:	cmake
BuildRequires:	ninja
%if %{with nox}
BuildRequires:	systemd-rpm-macros
BuildRequires:	pkgconfig(libsystemd)
%endif
#BuildRequires:	qtchooser
Requires:	python
Requires:	geoip

%description
A lightweight but feature-full BitTorrent client that aims to be very easy 
to use. It is multi-platform and provides a Qt5 graphical interface.

%package -n %{name}-nox
Summary:	A Headless Bittorrent Client
Group:		Networking/File transfer

%description -n %{name}-nox
A Headless Bittorrent Client with a feature rich Web UI allowing users to
control the clinet remotely.

%prep
%if "%gitdate" != ""
%autosetup -p0 -n qBittorrent-master
%else
%autosetup -p0
%endif
%if %{with nox}
CMAKE_BUILD_DIR=build-nox %cmake -G Ninja -DGUI:BOOL=OFF -DDBUS:BOOL=ON -DSYSTEMD=ON
cd ..
%endif

CMAKE_BUILD_DIR=build-gui %cmake -G Ninja -DGUI:BOOL=ON -DDBUS:BOOL=ON

%build
# Headless, AKA nox (No X[11])
%if %{with nox}
%ninja_build -C build-nox
%endif

# GUI
%ninja_build -C build-gui

%install
# install headless part
%if %{with nox}
%ninja_install -C build-nox
%endif

# install gui
%ninja_install -C build-gui

%files
%doc AUTHORS Changelog COPYING NEWS TODO
%{_bindir}/%{name}
%{_datadir}/applications/org.%{name}.qBittorrent.desktop
%{_iconsdir}/hicolor/*/status/%{name}-tray.png
%{_iconsdir}/hicolor/*/status/%{name}-tray*.svg
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/metainfo/org.%{name}.qBittorrent.appdata.xml
%{_mandir}/man1/%{name}.1*

%if %{with nox}
%files -n  %{name}-nox
%{_bindir}/%{name}-nox
%{_unitdir}/*.service
%{_mandir}/man1/%{name}-nox.1*
%endif
