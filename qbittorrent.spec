%bcond_without nox
%define gitdate %{nil}
#define beta rc2

Summary:		A lightweight but featureful BitTorrent client
Name:		qbittorrent
Version:		5.2.3
License:		GPLv2+
Group:	Networking/File transfer
Url:		https://qbittorrent.sourceforge.net
%if 0%{?beta:1}
Source0:	https://github.com/qbittorrent/qBittorrent/archive/refs/tags/release-%{version}%{?beta:%{beta}}.tar.gz
%else
Source0:	https://downloads.sourceforge.net/project/qbittorrent/qbittorrent/qbittorrent-%{version}/qbittorrent-%{version}.tar.xz
%endif
Release:	%{?beta:0.%{beta}.}2
# Patch for fix build issue introduced in qbittorrent 4.1.4 on non x64bit arch like armv7 or i686. (penguin)
# /src/base/utils/fs.cpp:346:10: error: case value evaluates to 4283649346, 
# which cannot be narrowed to type '__fsword_t' (aka 'int') [-Wc++11-narrowing]
#Patch0:		qbittorrent-x86-build-fix.patch
BuildRequires:		cmake
BuildRequires:		ninja
BuildRequires:		qmake-qt6
BuildRequires:		boost-devel >= 1.76
BuildRequires:		qt6-qtbase-sql-firebird
BuildRequires:		qt6-qtbase-sql-mariadb
BuildRequires:		qt6-qtbase-sql-odbc
BuildRequires:		qt6-qtbase-sql-postgresql
BuildRequires:		qt6-qtbase-theme-gtk3
BuildRequires:		qt6-qttools-linguist-tools
#BuildRequires:	qtchooser
BuildRequires:		cmake(Qt6)
BuildRequires:		pkgconfig(gl)
BuildRequires:		pkgconfig(libtorrent-rasterbar) >= 2.0.10
BuildRequires:		pkgconfig(libunwind-llvm)
BuildRequires:		pkgconfig(openssl) >= 3.0.2
BuildRequires:		pkgconfig(Qt6Concurrent)
BuildRequires:		pkgconfig(Qt6Core) >= 6.6.0
BuildRequires:		pkgconfig(Qt6DBus)
BuildRequires:		pkgconfig(Qt6Gui)
BuildRequires:		pkgconfig(Qt6Network)
BuildRequires:		pkgconfig(Qt6Sql)
BuildRequires:		pkgconfig(Qt6Svg)
BuildRequires:		pkgconfig(Qt6Widgets)
BuildRequires:		pkgconfig(Qt6Xml)
BuildRequires:		pkgconfig(vulkan)
BuildRequires:		pkgconfig(xkbcommon-x11)
BuildRequires:		pkgconfig(zlib) >= 1.2.11
%if %{with nox}
BuildRequires:		systemd-rpm-macros
BuildRequires:		pkgconfig(libsystemd)
%endif
Requires:	python
Requires:	geoip

%description
A lightweight but feature-full BitTorrent client that aims to be very easy
to use. It is multi-platform and provides a Qt6 graphical interface.

%files
%doc AUTHORS Changelog COPYING
%{_bindir}/%{name}
%{_datadir}/applications/org.%{name}.qBittorrent.desktop
%{_iconsdir}/hicolor/*/status/%{name}-tray.png
%{_iconsdir}/hicolor/*/status/%{name}-tray*.svg
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
%{_datadir}/metainfo/org.%{name}.qBittorrent.metainfo.xml
%{_mandir}/man1/%{name}.1*

#-----------------------------------------------------------------------------

%package -n %{name}-nox
Summary:	A Headless Bittorrent Client
Group:		Networking/File transfer

%description -n %{name}-nox
A Headless Bittorrent Client with a feature rich Web UI allowing users to
control the clinet remotely.

%if %{with nox}
%files -n  %{name}-nox
%{_bindir}/%{name}-nox
%{_unitdir}/*.service
%{_mandir}/man1/%{name}-nox.1*
%{_mandir}/ru/man1/%{name}-nox.1.*
%{_mandir}/ru/man1/%{name}.1.*
%{_datadir}/metainfo/org.%{name}.qBittorrent-nox.metainfo.xml
%endif

#-----------------------------------------------------------------------------

%prep
%if 0%{?beta:1}
%autosetup -p0 -n qBittorrent-release-%{version}%{?beta:%{beta}}
%else
%autosetup -p0
%endif

%if %{with nox}
CMAKE_BUILD_DIR=build-nox %cmake -G Ninja -DGUI:BOOL=OFF -DDBUS:BOOL=ON -DSYSTEMD:BOOL=ON -DQT6:BOOL=OFF
cd ..
%endif

CMAKE_BUILD_DIR=build-gui %cmake -G Ninja -DGUI:BOOL=ON -DDBUS:BOOL=ON -DQT6:BOOL=ON


%build
# Headless, AKA nox (No X[11])
%if %{with nox}
%ninja_build -C build-nox
%endif

# GUI
%ninja_build -C build-gui


%install
# Install headless part
%if %{with nox}
%ninja_install -C build-nox
%endif

# Install gui
%ninja_install -C build-gui
