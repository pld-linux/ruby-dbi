#
# Conditional build:
%bcond_without	rdoc		# build with rdoc
%bcond_with	ri		# build with ri
#
%define tarname dbi
Summary:	Database Interface for Ruby
Summary(pl.UTF-8):	Interfejs do baz danych dla języka Ruby
Name:		ruby-DBI
Version:	0.2.0
Release:	1
License:	GPL
Group:		Development/Languages
Source0:	http://rubyforge.org/frs/download.php/33959/dbi-%{version}.tar.gz
# Source0-md5:	b9836c3853a823432e45bccc4c29d333
Patch0:		%{name}-prefix.patch
BuildRequires:	mysql-ruby
BuildRequires:	rpmbuild(macros) >= 1.277
BuildRequires:	ruby-Postgres
BuildRequires:	ruby-devel >= 1:1.8.4-5
BuildRequires:	ruby-odbc
BuildRequires:	sqlite-devel
Obsoletes:	ruby-dbi
%{?ruby_mod_ver_requires_eq}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DBI Module for Ruby.

%description -l pl.UTF-8
Moduł DBI dla Ruby.

%package -n ruby-DBD-Mysql
Summary:	MySQL Database Driver for Ruby
Summary(pl.UTF-8):	Sterownik bazy danych MySQL dla języka Ruby
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires:	ruby-mysql-library

%description -n ruby-DBD-Mysql
MySQL Database Driver for Ruby.

%description -n ruby-DBD-Mysql -l pl.UTF-8
Sterownik bazy danych MySQL dla języka Ruby.

%package -n ruby-DBD-ODBC
Summary:	ODBC Database Driver for Ruby
Summary(pl.UTF-8):	Sterownik bazy danych ODBC dla języka Ruby
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires:	ruby-odbc

%description -n ruby-DBD-ODBC
ODBC Database Driver for Ruby.

%description -n ruby-DBD-ODBC -l pl.UTF-8
Sterownik bazy danych ODBC dla języka Ruby.

%package -n ruby-DBD-Pg
Summary:	PostgreSQL Database Driver for Ruby
Summary(pl.UTF-8):	Sterownik bazy danych PostgreSQL dla języka Ruby
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires:	ruby-Postgres

%description -n ruby-DBD-Pg
PostgreSQL Database Driver for Ruby.

%description -n ruby-DBD-Pg -l pl.UTF-8
Sterownik bazy danych PostgreSQL dla języka Ruby.

%package -n ruby-DBD-SQLite
Summary:	SQLite Database Driver for Ruby
Summary(pl.UTF-8):	Sterownik bazy danych SQLite dla języka Ruby
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description -n ruby-DBD-SQLite
SQLite Database Driver for Ruby.

%description -n ruby-DBD-SQLite -l pl.UTF-8
Sterownik bazy danych SQLite dla języka Ruby.

%prep
%setup -q -n dbi-%{version}
%patch0 -p1

#find lib -type d -name 'test*' | xargs rm -r -v

%build
# dbd_sybase requires TDS API update
ruby setup.rb config \
	--with=dbi,dbd_mysql,dbd_proxy,dbd_pg,dbd_sqlite,dbd_sqlrelay,dbd_odbc \
	--prefix=$RPM_BUILD_ROOT \
	--rb-dir=%{ruby_rubylibdir} \
	--so-dir=%{ruby_archdir}

ruby setup.rb setup

%if %{with rdoc}
rdoc -o rdoc lib ext
%endif
%if %{with ri}
rdoc --ri --op ri lib ext
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_archdir},%{ruby_ridir},%{_examplesdir}/%{name}-%{version}}
ruby setup.rb install

%if %{with ri}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
%endif
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README*
%if %{with rdoc}
%doc rdoc
%endif
%attr(755,root,root) %{_bindir}/proxyserver.rb
%attr(755,root,root) %{_bindir}/sqlsh.rb
%dir %{ruby_rubylibdir}/DBD
%{ruby_rubylibdir}/DBD/Proxy
%{ruby_rubylibdir}/DBD/SQLRelay
%{ruby_rubylibdir}/dbi.rb
%{ruby_rubylibdir}/dbi
%if %{with ri}
%{ruby_ridir}/DBI
%{ruby_ridir}/ColumnInfo
#%{ruby_ridir}/OCIError/cdesc-OCIError.yaml
%endif
%{_examplesdir}/%{name}-%{version}

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
%{ruby_rubylibdir}/DBD/SQLite
