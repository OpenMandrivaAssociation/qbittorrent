%define prerel beta2

Name:		qbittorrent
Version:	2.2.0
Release:	%mkrel -c %prerel 1
Summary:	A lightweight but featureful BitTorrent client
Group:		Networking/File transfer
License:	GPLv2+
Url:		http://qbittorrent.sourceforge.net/
Source0:	%{name}-%{version}%{prerel}.tar.gz
# (fc) qbittorrent-2.2.0beta1 patch to disable extra debug
Patch0:		qbittorrent-2.2.0beta1-disable-extra-debug.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	qt4-devel >= 4.4
BuildRequires:	boost-devel
BuildRequires:	libtorrent-rasterbar-devel >= 0.14.4
BuildRequires:	libnotify-devel >= 0.4.2
Requires:	python
Requires:	geoip

%description
A lightweight but featureful BitTorrent client that aims to be very easy 
to use. It is multi-platform and provides a Qt4 graphical interface.

%package -n %{name}-nox
Summary:	A Headless Bittorrent Client
Group:		Networking/File transfer

%description -n %{name}-nox
A Headless Bittorrent Client with a feature rich Web UI allowing users to
control the clinet remotely.

%prep
%setup -q -n %{name}-%{version}%{prerel}
%patch0 -p1

%build
%setup_compile_flags
# headless aka nox
mkdir build-nox
cd build-nox
../configure	--prefix=%{_prefix} \
		--qtdir=%{qt4dir} \
		--disable-gui \
		--disable-libnotify \
		--disable-geoip-database
cp conf.pri ..
%make
mv -f ../conf.pri ../conf.pri.nox

# GUI
cd ..
mkdir build-gui
cd build-gui
../configure	--prefix=%{_prefix} \
		--qtdir=%{qt4dir}
cp conf.pri ..
%make
mv -f ../conf.pri ../conf.pri.gui


%install
rm -rf %{buildroot}
# install headless part
mv -f conf.pri.nox conf.pri
cd build-nox
make INSTALL_ROOT=%{buildroot} install

# install gui
cd ..
mv -f conf.pri.gui conf.pri
cd build-gui
make INSTALL_ROOT=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS Changelog COPYING NEWS README TODO
%{_bindir}/%{name}
%{_datadir}/applications/qBittorrent.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_mandir}/man1/%{name}.1*

%files -n  %{name}-nox
%defattr(-,root,root,-)
%{_bindir}/%{name}-nox
%{_mandir}/man1/%{name}-nox.1*
