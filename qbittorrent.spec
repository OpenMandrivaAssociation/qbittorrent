Name:		qbittorrent
Version:	2.1.1
Release:	%mkrel 1
Summary:	A lightweight but featureful BitTorrent client
Group:		Networking/File transfer
License:	GPLv2+
Url:		http://qbittorrent.sourceforge.net/
Source0:	%{name}-%{version}.tar.gz
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
#-------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}

%build
%setup_compile_flags
# configure and make the headless part first
./configure 	--disable-gui \
		--disable-libnotify \
		--disable-geoip-database \
		--prefix=%{_prefix}
%make
make clean

# now configure and make the gui part
./configure --prefix=%{_prefix}
%make


%install
rm -rf %{buildroot}
# install the gui files
make INSTALL_ROOT=%{buildroot} install
# install healdess files
install -m755 src/%{name}-nox %{buildroot}%{_bindir}
install -m644 doc/%{name}-nox.1 %{buildroot}%{_mandir}/man1

%clean
rm -rf %{buildroot}
