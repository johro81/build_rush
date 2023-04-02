%define _prefix /usr/local

Name:           rush
Version:        2.3
Release:        1%{?dist}
Summary:        GNU Restriced User Shell

License:        GPL-3.0-only
URL:            https://www.gnu.org.ua/software/rush/rush.html
Source0:        %{name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  make

%description
GNU Rush is a Restricted User Shell, designed for sites providing limited remote access to their resources, such as, for example, savannah.gnu.org. Its main program, rush, is configured as a user login shell for users that are allowed only remote access to the machine. Using a flexible configuration file, GNU Rush gives administrator complete control over the command lines that users execute, and allows to tune the usage of system resources, such as virtual memory, CPU time, etc. on a per-user basis.

In particular, GNU Rush allows to run remote programs in a chrooted environment, which helps tighten security when offering access over such programs as sftp-server or scp, that access the entire file system by default.

Another important feature of rush is notification. It allows to notify another processes via an INET or UNIX socket about termination of the user session.

All accesses via rush are monitored. GNU Rush includes two programs that help visualize the history of accesses: rushwho, which displays the list of currently logged in users, and rushlast, which shows the history of accesses. The output format of both utilities is configurable.

%prep
%setup -q

%build
./configure --prefix=/usr/local --sysconfdir=/etc
make

%install
rm -rf %{buildroot}
%make_install

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/rush-po
%attr(0755,root,root) %{_bindir}/rushlast
%attr(0755,root,root) %{_bindir}/rushwho
%attr(0755,root,root) %{_sbindir}/rush
%config /etc/rush.rc
%doc %{_infodir}/dir
%doc %{_infodir}/rush.info
%doc %{_mandir}/man1/rush-po.1
%doc %{_mandir}/man1/rushlast.1
%doc %{_mandir}/man1/rushwho.1
%doc %{_mandir}/man5/rush.rc.5
%doc %{_mandir}/man8/rush.8
%{_datadir}/locale/*
%license COPYING

%changelog
* Mon Apr 03 2023 Johan Rodin <johan.rodin@sigmatechnology.com> - 2.3-1
- First version being packaged
