Name:       upower

# >> macros
# << macros

Summary:    Power Management Service
Version:    0.9.21
Release:    1
Group:      System/Libraries
License:    GPLv2+
URL:        http://upower.freedesktop.org/
Source0:    http://upower.freedesktop.org/releases/upower-%{version}.tar.xz
Requires:   polkit >= 0.92
Requires:   udev
Requires:   pm-utils >= 1.2.2.1
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(gudev-1.0) >= 147
BuildRequires:  pkgconfig(libusb-1.0) >= 1.0.0
BuildRequires:  pkgconfig(dbus-1) >= 1.0
BuildRequires:  pkgconfig(dbus-glib-1) >= 0.76
BuildRequires:  pkgconfig(glib-2.0) >= 2.21.5
BuildRequires:  pkgconfig(gio-2.0) >= 2.16.1
BuildRequires:  pkgconfig(polkit-gobject-1) >= 0.97
BuildRequires:  pkgconfig(udev) >= 187
BuildRequires:  libtool
BuildRequires:  intltool
BuildRequires:  gettext
BuildRequires:  systemd-devel

%description
UPower (formerly DeviceKit-power) provides a daemon, API and command
line tools for managing power devices attached to the system.


%package devel
Summary:    Headers and libraries for UPower
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Headers and libraries for UPower.


%prep
%setup -q -n %{name}-%{version}/upower

%build
export PKG_CONFIG=pkg-config
./autogen.sh
%configure --disable-static \
    --disable-gtk-doc \
    --enable-systemd

make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}
%make_install

%find_lang upower

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f upower.lang
%defattr(-,root,root,-)
%doc NEWS COPYING AUTHORS HACKING README
%{_libdir}/libupower-glib.so.*
%config %{_sysconfdir}/dbus-1/system.d/*.conf
/lib/udev/rules.d/*.rules
%dir %{_localstatedir}/lib/upower
%dir %{_sysconfdir}/UPower
%config %{_sysconfdir}/UPower/UPower.conf
%{_bindir}/upower
%{_libexecdir}/upowerd
/lib/systemd/system-sleep/notify-upower.sh
%{_unitdir}/upower.service
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/dbus-1/system-services/*.service

%files devel
%defattr(-,root,root,-)
%{_datadir}/dbus-1/interfaces/*.xml
%{_libdir}/libupower-glib.so
%{_libdir}/pkgconfig/*.pc
%dir %{_includedir}/libupower-glib
%{_includedir}/libupower-glib/*.h
