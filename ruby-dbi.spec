%define	ruby_archdir	%(ruby -r rbconfig -e 'print Config::CONFIG["archdir"]')
%define ruby_rubylibdir %(ruby -r rbconfig -e 'print Config::CONFIG["rubylibdir"]')
%define	ruby_ridir	%(ruby -r rbconfig -e 'include Config; print File.join(CONFIG["datadir"], "ri", CONFIG["ruby_version"], "system")')
Summary:	DataBase Interface for Ruby
Summary(pl):	Interfejs do baz danych dla jêzyka Ruby
Name:		ruby-DBI
%define tarname ruby-dbi
Version:	0.0.21
Release:	2
License:	GPL
Group:		Development/Languages
Source0:	http://dl.sourceforge.net/%{tarname}/%{tarname}-all-%{version}.tar.gz
# Source0-md5:	e71784353b914ecdd02c9bdc5a21e65e
Patch0:		%{name}-prefix.patch
Patch1:		%{name}-timestamps.patch
URL:		http://www.tmtm.org/mysql/ruby/
BuildRequires:	ruby
BuildRequires:	ruby-devel
BuildRequires:	ruby-mysql
BuildRequires:	sqlite-devel
BuildRequires:	ruby-postgres
Obsoletes:	ruby-dbi
Requires:	ruby
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DBI Module for Ruby

%description -l pl
Modu³ DBI dla Ruby.

%package -n ruby-DBD-Mysql
Summary:	MySQL DataBase Driver for Ruby
Requires:	ruby-mysql
Group:	Development/Languages

%description -n ruby-DBD-Mysql
MySQL DataBase Driver for Ruby

%package -n ruby-DBD-SQLite
Summary:	SQLite DataBase Driver for Ruby
Group:	Development/Languages

%description -n ruby-DBD-SQLite
SQLite DataBase Driver for Ruby

%package -n ruby-DBD-Pg
Summary:	PostgreSQL DataBase Driver for Ruby
Group:	Development/Languages
Requires:	ruby-postgres

%description -n ruby-DBD-Pg
PostgreSQL DataBase Driver for Ruby

%prep
%setup -q -n %{tarname}-all
%patch0 -p1
%patch1 -p1

%build
find lib -type d -name 'test*' | xargs rm -r -v

ruby setup.rb config \
	--with=dbi,dbd_proxy,dbd_mysql,dbd_sqlite,dbd_sqlrelay,dbd_pg \
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
%{ruby_rubylibdir}/DBD/Mysql

%files -n ruby-DBD-SQLite
%{ruby_archdir}/DBD/SQLite

%files -n ruby-DBD-Pg
%{ruby_rubylibdir}/DBD/Pg/Pg.rb
