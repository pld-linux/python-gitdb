#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (needs git checkout, not archive?)

%define		module	gitdb
Summary:	GitDB - pure-Python git object database
Summary(pl.UTF-8):	GitDB - czysto pythonowa baza danych obiektów gita
Name:		python-%{module}
# keep 2.x here for python2 support
Version:	2.0.6
Release:	1
Epoch:		1
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://github.com/gitpython-developers/gitdb/tags
Source0:	https://github.com/gitpython-developers/gitdb/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	b81077d817e8a03fe541ec76b456849d
URL:		https://github.com/gitpython-developers/gitdb
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
# or smmap2 >= 2.0.0
BuildRequires:	python-smmap >= 3.0.0
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%{?with_doc:BuildRequires:	sphinx-pdg-2}
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
GitDB allows you to access bare git repositories for reading and
writing. It aims at allowing full access to loose objects as well as
packs with performance and scalability in mind. It operates
exclusively on streams, allowing to handle large objects with a small
memory footprint.

%description -l pl.UTF-8
GitDB pozwala na dostęp do gołych repozytoriów gita do odczytu i
zapisu. Celem jest umożliwienie pełnego dostępu do luźnych obiektów,
jak i paczek z myślą o wydajności i skalowalności. Operuje wyłącznie
na strumieniach, pozwalając na obsługę dużych obiektów przy niewielkim
narzucie czasu.

%package apidocs
Summary:	API documentation for GitDB module
Summary(pl.UTF-8):	Dokumentacja API modułu GitDB
Group:		Documentation

%description apidocs
API documentation for GitDB module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu GitDB.

%prep
%setup -q -n %{module}-%{version}

# smmap 3.x uses smmap name
%{__sed} -i -e 's/smmap2 /smmap /' setup.py

%build
%py_build %{?with_tests:test}

%if %{with doc}
%{__make} -C doc html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/gitdb/test

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.rst
%dir %{py_sitescriptdir}/gitdb
%{py_sitescriptdir}/gitdb/*.py[co]
%{py_sitescriptdir}/gitdb/db
%{py_sitescriptdir}/gitdb/utils
%{py_sitescriptdir}/gitdb2-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/build/html/{_static,*.html,*.js}
%endif
