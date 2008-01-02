%define name	gtkpsproc
%define version	2.0
%define tarver	20
%define release  %mkrel 1

Name: 	 	%{name}
Summary: 	Postscript printing options GUI
Version: 	%{version}
Release: 	%{release}

Source:		%{name}%{tarver}.tar.bz2
URL:		http://www.rastersoft.com/gtkpsproc.html
License:	GPL
Group:		System/Configuration/Printing
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	pkgconfig ImageMagick gtk2-devel

%description
GtkPSproc is a front-end for the PSUTILS. PSUTILS is a set of little programs
that allows to manage in a lot of ways your PostScript files.
GtpPSproc is designed to work from nearly all programs that call LPR, acting
as an intermediary between the program and LPR program, but it can work alone
too.
GtkPSproc allows to adjust all the programs to your printer type (for example,
sending always the pages in reverse order), to group two or more pages in a
sigle sheet, to print booklets, and to easily print in double-side fashion. 

%prep
%setup -q -n %{name}%{tarver}

%build
cd devel
%configure2_5x
%make
										
%install
cd devel
rm -rf $RPM_BUILD_ROOT
%makeinstall
mkdir -p $RPM_BUILD_ROOT/%_datadir/pixmaps/%name
cp pixmaps/* $RPM_BUILD_ROOT/%_datadir/pixmaps/%name
cd ..

#menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications/
cat << EOF > %buildroot%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{name}
Icon=%{name}
Name=GtkPSProc
Comment=Postscript printing GUI
Categories=HardwareSettings;
EOF

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
convert -size 48x48 doc/canon.png $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
convert -size 32x32 doc/canon.png $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
convert -size 16x16 doc/canon.png $RPM_BUILD_ROOT/%_miconsdir/%name.png

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_menus
		
%postun
%clean_menus

%files -f %{name}.lang
%defattr(-,root,root)
%doc README doc/*
%{_bindir}/%name
%{_datadir}/pixmaps/%name
%{_datadir}/applications/mandriva-%name.desktop
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png

