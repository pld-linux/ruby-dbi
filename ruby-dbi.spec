#
# Conditional build:
%bcond_without	rdoc		# build with rdoc
%bcond_with	ri		# build with ri
#
%define tarname dbi
Summary:	Database Interface for Ruby
Summary(pl.UTF-8):	Interfejs do baz danych dla języka Ruby
Name:		ruby-DBI
Version:	0.4.1
Release:	1
License:	GPL
Group:		Development/Languages
Source0:	http://rubyforge.org/frs/download.php/47537/dbi-%{version}.tar.gz
# Source0-md5:	71ffdfd63709f12635905616e39a203b
#Patch0:		%{name}-prefix.patch
#BuildRequires:	mysql-ruby
BuildRequires:	rpmbuild(macros) >= 1.277
#BuildRequires:	ruby-Postgres
BuildRequires:	ruby-devel >= 1:1.8.4-5
#BuildRequires:	ruby-odbc
#BuildRequires:	sqlite-devel
Suggests: ruby-dbd-mysql
Suggests: ruby-dbd-pg
Suggests: ruby-dbd-sqlite
Suggests: ruby-dbd-sqlite3
BuildRequires:	setup.rb >= 3.4.1
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
#%patch0 -p1

#find lib -type d -name 'test*' | xargs rm -r -v

%build
cp %{_datadir}/setup.rb .
ruby setup.rb config \
	--rbdir=%{ruby_rubylibdir} \
	--sodir=%{ruby_archdir}

ruby setup.rb setup

%if %{with rdoc}
rdoc -o rdoc lib
%endif
%if %{with ri}
rdoc --ri --op ri lib
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_archdir},%{ruby_ridir},%{_examplesdir}/%{name}-%{version}}
ruby setup.rb install \
	--prefix=$RPM_BUILD_ROOT

%if %{with ri}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
%endif
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/dbi
%doc README*
%if %{with rdoc}
%doc rdoc
%endif
%{ruby_rubylibdir}/dbi.rb
%{ruby_rubylibdir}/dbi
%if %{with ri}
%{ruby_ridir}/DBI
%{ruby_ridir}/ColumnInfo
#%{ruby_ridir}/OCIError/cdesc-OCIError.yaml
%endif
%{_examplesdir}/%{name}-%{version}
