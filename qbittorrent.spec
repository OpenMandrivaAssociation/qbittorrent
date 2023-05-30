%bcond_without nox
%bcond_without qt6

Name:		qbittorrent
Version:	4.5.3
Summary:	A lightweight but featureful BitTorrent client
Group:		Networking/File transfer
License:	GPLv2+
Url:		http://qbittorrent.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/qbittorrent/qbittorrent/qbittorrent-%{version}/qbittorrent-%{version}.tar.xz
Release:	1

BuildRequires:	boost-devel
BuildRequires:	qmake5
BuildRequires:	qt5-linguist-tools
BuildRequires:	pkgconfig(libtorrent-rasterbar) >= 2.0.0
BuildRequires:	pkgconfig(Qt5Concurrent)
BuildRequires:	pkgconfig(Qt5Core)
BuildRequires:	pkgconfig(Qt5DBus)
BuildRequires:	pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:	pkgconfig(Qt5Svg)
BuildRequires:	pkgconfig(Qt5Network)
BuildRequires:	pkgconfig(Qt5Widgets)
BuildRequires:	pkgconfig(Qt5Xml)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(libunwind-llvm)
BuildRequires:	cmake
BuildRequires:	ninja
%if %{with nox}
BuildRequires:	systemd-rpm-macros
BuildRequires:	pkgconfig(libsystemd)
%endif
#BuildRequires:	qtchooser
%if %{with qt6}
BuildRequires:  qt6-cmake
BuildRequires:  qmake-qt6
BuildRequires:	qt6-qttools
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:	cmake(Qt6Concurrent)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6DBus)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Sql)
BuildRequires:	cmake(Qt6Svg)
BuildRequires:	cmake(Qt6Network)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(Qt6Xml)
BuildRequires:  qt6-qtbase-sql-firebird
%endif
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
%autosetup -p1
%if %{with nox}
CMAKE_BUILD_DIR=build-nox %cmake -G Ninja -DGUI:BOOL=OFF -DDBUS:BOOL=ON -DSYSTEMD=ON
cd ..
%endif

CMAKE_BUILD_DIR=build-gui %cmake -G Ninja -DGUI:BOOL=ON -DDBUS:BOOL=ON
cd ..
%if %{with qt6}
CMAKE_BUILD_DIR=build-gui6 %cmake -G Ninja -DGUI:BOOL=ON -DDBUS:BOOL=ON -DQT6=ON
%endif

%build
# Headless, AKA nox (No X[11])
%if %{with nox}
%ninja_build -C build-nox
%endif

# GUI
%ninja_build -C build-gui

%if %{with qt6}
# GUI6
%ninja_build -C build-gui6
%endif

%install
# install headless part
%if %{with nox}
%ninja_install -C build-nox
%endif

# install gui
%ninja_install -C build-gui

%if %{with qt6}
#install gui6
%ninja_insrall -C build-gui6
%endif
%files
%doc AUTHORS Changelog COPYING
%{_bindir}/%{name}
%{_datadir}/applications/org.%{name}.qBittorrent.desktop
%{_iconsdir}/hicolor/*/status/%{name}-tray.png
%{_iconsdir}/hicolor/*/status/%{name}-tray*.svg
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_iconsdir}/hicolor/scalable/apps/qbittorrent.svg
%{_datadir}/metainfo/org.%{name}.qBittorrent.appdata.xml
%{_mandir}/man1/%{name}.1*

%if %{with nox}
%files -n  %{name}-nox
%{_bindir}/%{name}-nox
%{_unitdir}/*.service
%{_mandir}/man1/%{name}-nox.1*
%endif
