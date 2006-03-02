%define tarname ruby-dbi
Summary:	Database Interface for Ruby
Summary(pl):	Interfejs do baz danych dla jêzyka Ruby
Name:		ruby-DBI
Version:	0.0.23
Release:	1
License:	GPL
Group:		Development/Languages
Source0:	http://rubyforge.org/frs/download.php/655/%{tarname}-all-%{version}.tar.gz
# Source0-md5:	7a713494d84bd4f5b877496970bcf13c
Patch0:		%{name}-prefix.patch
BuildRequires:	mysql-ruby
BuildRequires:	rpmbuild(macros) >= 1.277
BuildRequires:	ruby-devel >= 1:1.8.4-5
BuildRequires:	ruby-Postgres
BuildRequires:	ruby-odbc
BuildRequires:	sqlite-devel
Obsoletes:	ruby-dbi
%{?ruby_mod_ver_requires_eq}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DBI Module for Ruby.

%description -l pl
Modu³ DBI dla Ruby.

%package -n ruby-DBD-Mysql
Summary:	MySQL Database Driver for Ruby
Summary(pl):	Sterownik bazy danych MySQL dla jêzyka Ruby
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires:	ruby-mysql-library

%description -n ruby-DBD-Mysql
MySQL Database Driver for Ruby.

%description -n ruby-DBD-Mysql -l pl
Sterownik bazy danych MySQL dla jêzyka Ruby.

%package -n ruby-DBD-ODBC
Summary:	ODBC Database Driver for Ruby
Summary(pl):	Sterownik bazy danych ODBC dla jêzyka Ruby
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires:	ruby-odbc

%description -n ruby-DBD-ODBC
ODBC Database Driver for Ruby.

%description -n ruby-DBD-ODBC -l pl
Sterownik bazy danych ODBC dla jêzyka Ruby.

%package -n ruby-DBD-Pg
Summary:	PostgreSQL Database Driver for Ruby
Summary(pl):	Sterownik bazy danych PostgreSQL dla jêzyka Ruby
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires:	ruby-Postgres

%description -n ruby-DBD-Pg
PostgreSQL Database Driver for Ruby.

%description -n ruby-DBD-Pg -l pl
Sterownik bazy danych PostgreSQL dla jêzyka Ruby.

%package -n ruby-DBD-SQLite
Summary:	SQLite Database Driver for Ruby
Summary(pl):	Sterownik bazy danych SQLite dla jêzyka Ruby
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n ruby-DBD-SQLite
SQLite Database Driver for Ruby.

%description -n ruby-DBD-SQLite -l pl
Sterownik bazy danych SQLite dla jêzyka Ruby.

%prep
%setup -q -n %{tarname}-all
%patch0 -p1

find lib -type d -name 'test*' | xargs rm -r -v

%build
# dbd_sybase requires TDS API update
ruby setup.rb config \
	--with=dbi,dbd_mysql,dbd_proxy,dbd_pg,dbd_sqlite,dbd_sqlrelay,dbd_odbc \
	--prefix=$RPM_BUILD_ROOT \
	--rb-dir=%{ruby_rubylibdir} \
	--so-dir=%{ruby_archdir}

ruby setup.rb setup

rdoc -o rdoc lib ext
rdoc --ri --op ri lib lib/dbd_*/*

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_archdir},%{ruby_ridir}}
ruby setup.rb install

cp -a ri/ri/* $RPM_BUILD_ROOT%{ruby_ridir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README* rdoc
%attr(755,root,root) %{_bindir}/proxyserver.rb
%attr(755,root,root) %{_bindir}/sqlsh.rb
%dir %{ruby_rubylibdir}/DBD
%dir %{ruby_archdir}/DBD
%{ruby_rubylibdir}/DBD/Proxy
%{ruby_rubylibdir}/DBD/SQLRelay
%{ruby_rubylibdir}/dbi.rb
%{ruby_rubylibdir}/dbi
%{ruby_ridir}/DBI
%{ruby_ridir}/ColumnInfo
#%{ruby_ridir}/OCIError/cdesc-OCIError.yaml

%files -n ruby-DBD-Mysql
%defattr(644,root,root,755)
%{ruby_rubylibdir}/DBD/Mysql

%files -n ruby-DBD-ODBC
%defattr(644,root,root,755)
%{ruby_rubylibdir}/DBD/ODBC

%files -n ruby-DBD-Pg
%defattr(644,root,root,755)
%{ruby_rubylibdir}/DBD/Pg

%files -n ruby-DBD-SQLite
%defattr(644,root,root,755)
%dir %{ruby_archdir}/DBD/SQLite
%attr(755,root,root) %{ruby_archdir}/DBD/SQLite/SQLite.so
