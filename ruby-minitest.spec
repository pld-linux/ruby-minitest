%define pkgname minitest
Summary:	Small and fast replacement for ruby's huge and slow test/unit.
Name:		ruby-%{pkgname}
Version:	1.5.0
Release:	0.1
License:	MIT/Ruby License
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	02a8c9d1afe9a4952e5b8d6f2fc202d7
Group:		Development/Languages
URL:		http://rubyforge.org/projects/bfts
BuildRequires:	rpmbuild(macros) >= 1.484
BuildRequires:	ruby >= 1:1.8.6
BuildRequires:	ruby-modules
%{?ruby_mod_ver_requires_eq}
#BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# nothing to be placed there. we're not noarch only because of ruby packaging
%define		_enable_debug_packages	0

%description
minitest/unit is a small and fast replacement for ruby's huge and slow
test/unit. This is meant to be clean and easy to use both as a regular test
writer and for language implementors that need a minimal set of methods to
bootstrap a working unit test suite. mini/spec is a functionally complete spec
engine. mini/mock, by Steven Baker, is a beautifully tiny mock object
framework. (This package was called miniunit once upon a time)

%package rdoc
Summary:	Documentation files for %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
Documentation files for %{pkgname}.

%prep
%setup -q -c
%{__tar} xf %{SOURCE0} -O data.tar.gz | %{__tar} xz
find -newer README.txt  -o -print | xargs touch --reference %{SOURCE0}

%build
rdoc --ri --op ri lib
rdoc --op rdoc lib
rm -rf ri/{Kernel,MockExpectationError,Module,Object,Test}
rm -f ri/created.rid

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_rubylibdir},%{ruby_ridir},%{ruby_rdocdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_rubylibdir}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc History.txt README.txt
%{ruby_rubylibdir}/%{pkgname}

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}
%{ruby_ridir}/MiniTest
