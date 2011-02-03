%define version	2.6.5
%define prerel	0
%define rel	1

%if %prerel
%define srcname %{name}-%{version}%prerel
%define release %mkrel 0.%prerel.%rel
%else
%define srcname %{name}-%{version}
%define release %mkrel %rel
%endif

%define build_nox 1

Name:		qbittorrent
Version:	%{version}
Release:	%{release}
Summary:	A lightweight but featureful BitTorrent client
Group:		Networking/File transfer
License:	GPLv2+
Url:		http://qbittorrent.sourceforge.net/
%if %prerel
Source0:	http://downloads.sourceforge.net/project/qbittorrent/qbittorrent-unstable/%{name}-%{version}%{prerel}.tar.gz
%else
Source0:	http://downloads.sourceforge.net/project/qbittorrent/qbittorrent/qbittorrent-%{version}/qbittorrent-%{version}.tar.gz
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	qt4-devel >= 4:4.6
BuildRequires:	boost-devel
BuildRequires:	libtorrent-rasterbar-devel >= 0.14.4
BuildRequires:	libnotify-devel >= 0.4.2
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
%setup -q -n %{srcname}

%build
%setup_compile_flags
# headless aka nox
%if %build_nox
mkdir build-nox
pushd build-nox
  ../configure	--prefix=%{_prefix} \
		--qtdir=%{qt4dir} \
		--disable-gui \
		--disable-libnotify \
		--disable-geoip-database
  cp conf.pri ..
  %make
  mv -f ../conf.pri ../conf.pri.nox
popd
%endif

# GUI
mkdir build-gui
pushd build-gui
  ../configure	--prefix=%{_prefix} \
		--qtdir=%{qt4dir}
  cp conf.pri ..
  %make
  mv -f ../conf.pri ../conf.pri.gui
popd

%install
rm -rf %{buildroot}

# install headless part
%if %build_nox
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS Changelog COPYING NEWS README TODO
%{_bindir}/%{name}
%{_datadir}/applications/qBittorrent.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_mandir}/man1/%{name}.1*

%if %build_nox
%files -n  %{name}-nox
%defattr(-,root,root,-)
%{_bindir}/%{name}-nox
%{_mandir}/man1/%{name}-nox.1*
%endif
