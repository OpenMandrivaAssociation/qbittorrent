%define rel rc6

Name:		qbittorrent
Version:	2.1.0
Release:	%mkrel -c %{rel} 1
Summary:	A lightweight but featureful BitTorrent client
Group:		Networking/File transfer
License:	GPLv2+
Url:		http://qbittorrent.sourceforge.net/
Source0:	http://downloads.sourceforge.net/qbittorrent/%{name}-%{version}%{rel}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	qt4-devel >= 4.4
BuildRequires:	boost-devel
BuildRequires:	libtorrent-rasterbar-devel >= 0.14.7
BuildRequires:	libnotify-devel >= 0.4.2
Requires:	python
Requires:	geoip

%description
A lightweight but featureful BitTorrent client that aims to be very easy 
to use. It is multi-platform and provides a Qt4 graphical interface.

%files
%defattr(-,root,root,-)
%doc AUTHORS Changelog COPYING NEWS README TODO
%{_bindir}/%{name}
%{_datadir}/applications/qBittorrent.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_mandir}/man1/%{name}.1*

#-------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{version}%{rel}

%build
%setup_compile_flags
./configure --prefix=%{_prefix}
%make

%install
rm -rf %{buildroot}
make INSTALL_ROOT=%{buildroot} install

%clean
rm -rf %{buildroot}
