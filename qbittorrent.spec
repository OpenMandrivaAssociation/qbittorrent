%define build_nox 1

Name:		qbittorrent
Version:	2.9.3
Release:	%mkrel 1
Summary:	A lightweight but featureful BitTorrent client
Group:		Networking/File transfer
License:	GPLv2+
Url:		http://qbittorrent.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/qbittorrent/qbittorrent/qbittorrent-%{version}/qbittorrent-%{version}.tar.gz
BuildRequires:	qt4-devel >= 4:4.6
BuildRequires:	boost-devel
BuildRequires:	libtorrent-rasterbar-devel >= 0.15.8
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
%setup -q -n %{name}-%{version}

%build
%setup_compile_flags
# headless aka nox
%if %{build_nox}
%__mkdir build-nox
pushd build-nox
  ../configure	--prefix=%{_prefix} \
		--qtdir=%{qt4dir} \
		--disable-gui \
		--disable-geoip-database
  %__cp conf.pri ..
  %make
  %__mv -f ../conf.pri ../conf.pri.nox
popd
%endif

# GUI
%__mkdir build-gui
pushd build-gui
  ../configure	--prefix=%{_prefix} \
		--qtdir=%{qt4dir}
  %__cp conf.pri ..
  %make
  %__mv -f ../conf.pri ../conf.pri.gui
popd

%install
%__rm -rf %{buildroot}

# install headless part
%if %build_nox
%__cp -f conf.pri.nox conf.pri
pushd build-nox
  make INSTALL_ROOT=%{buildroot} install
popd
%endif

# install gui
%__cp -f conf.pri.gui conf.pri
pushd build-gui
  make INSTALL_ROOT=%{buildroot} install
popd

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS Changelog COPYING NEWS README TODO
%{_bindir}/%{name}
%{_datadir}/applications/qBittorrent.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/qbittorrent.png
%{_mandir}/man1/%{name}.1*

%if %{build_nox}
%files -n  %{name}-nox
%defattr(-,root,root,-)
%{_bindir}/%{name}-nox
%{_mandir}/man1/%{name}-nox.1*
%endif
