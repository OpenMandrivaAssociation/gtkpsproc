%define name	gtkpsproc
%define version	3.3b
%define release  %mkrel 1

Name: 	 	%{name}
Summary: 	Postscript printing interface
Version: 	%{version}
Release: 	%{release}

Source:		%{name}-%{version}.tar.bz2
URL:		http://www.rastersoft.com/gtkpsproc.html
License:	GPLv2+
Group:		System/Configuration/Printing
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	pkgconfig ImageMagick gtk2-devel
Requires:	gnome-python gnome-python-applet python-gobject
Requires:	python-gamin
Requires(post):	cups cups-common
Requires(postun): cups

%description
GtkPSproc provides an elegant graphical interface which shows up as a
virtual printer.  Printing to GtkPSproc allows for some advanced options
which your standard desktop interface may not provide, such as:
 * reverse order
 * multiple pages per sheet
 * booklet mode
 * double-side emulation
 * and more

You can run gtkpsproc from the command line.  To enable the cups backend,
you will have to configure your desktop to run the gtkpsproc-applet.

%prep
%setup -q

%build
make
										
%install
rm -rf $RPM_BUILD_ROOT
install -d %{buildroot}/%{_bindir}
install -m 755 gtkpsproc %{buildroot}/%{_bindir}/gtkpsproc
install -d %{buildroot}/%{_datadir}/gtkpsproc
install -d %{buildroot}/%{_datadir}/locale/es/LC_MESSAGES
install po/es.mo %{buildroot}/%{_datadir}/locale/es/LC_MESSAGES/gtkpsproc.mo
install gtkpsproc.glade %{buildroot}/%{_datadir}/gtkpsproc/
install pixmaps/* %{buildroot}/%{_datadir}/gtkpsproc/
install -d %{buildroot}/%{_datadir}/pixmaps
install gtkpsproc.svg %{buildroot}/%{_datadir}/pixmaps/
install -m 755 psproc_applet.py %{buildroot}/%{_bindir}/psproc_applet
install -d %{buildroot}/%{_prefix}/lib/cups/backend
install -m 755 psproc_backend.py %{buildroot}/%{_prefix}/lib/cups/backend/psproc_backend
#install -d %{buildroot}/%{_datadir}/cups/model
#install gtkpsprc.ppd %{buildroot}/%{_datadir}/cups/model/
install -d %{buildroot}/%{_libdir}/bonobo/servers
install gtkpsproc.server %{buildroot}/%{_libdir}/bonobo/servers/
install -d %{buildroot}/%{_datadir}/doc/gtkpsproc/html
install docs/* %{buildroot}/%{_datadir}/doc/gtkpsproc/html/

#menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{name}
Icon=%{name}
Name=GtkPSProc
Comment=Graphical printing interface
Categories=HardwareSettings;
EOF

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
convert -size 48x48 %name.svg $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
convert -size 32x32 %name.svg $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
convert -size 16x16 %name.svg $RPM_BUILD_ROOT/%_miconsdir/%name.png

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%post
lpadmin -p GtkPSproc -E -v psproc_backend:/
/etc/rc.d/init.d/cups restart
%if %mdkversion < 200900
%update_menus
%endif

%preun
killall gtkpsproc-applet
		
%postun
/etc/rc.d/init.d/cups restart
%if %mdkversion < 200900
%clean_menus
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc %{_datadir}/doc/%name
%{_bindir}/*
%{_libdir}/bonobo/servers/*
%{_prefix}/lib/cups/backend/*
%{_datadir}/%name
%{_datadir}/pixmaps/*
%{_datadir}/applications/mandriva-%name.desktop
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png

