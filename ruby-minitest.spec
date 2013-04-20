#
# Conditional build:
%bcond_without	tests		# build without tests

%define pkgname minitest
Summary:	Small and fast replacement for ruby's huge and slow test/unit
Name:		ruby-%{pkgname}
Version:	4.7.0
Release:	1
License:	MIT/Ruby License
Group:		Development/Languages
Source0:	http://gems.rubyforge.org/gems/%{pkgname}-%{version}.gem
# Source0-md5:	3f527181eb7a1e00c92d0088fff94525
URL:		http://rubyforge.org/projects/bfts
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
minitest/unit is a small and fast replacement for ruby's huge and slow
test/unit. This is meant to be clean and easy to use both as a regular
test writer and for language implementors that need a minimal set of
methods to bootstrap a working unit test suite. mini/spec is a
functionally complete spec engine. mini/mock, by Steven Baker, is a
beautifully tiny mock object framework. (This package was called
miniunit once upon a time)

%package rdoc
Summary:	Documentation files for %{pkgname}
Group:		Documentation
Requires:	ruby >= 1:1.8.7-4

%description rdoc
Documentation files for %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

find lib -type f | xargs sed -i -e '/^#!\/usr\/bin\/ruby.*/d'

%build
%if %{with tests}
# spec test suite is unstable.
# https://github.com/seattlerb/minitest/issues/257
mv test/minitest/test_minitest_spec.rb{,.ignore}

for f in test/minitest/test_*.rb; do
	ruby -Ilib:.:./test $f
done
%endif

rdoc --ri --op ri lib
rdoc --op rdoc lib
rm -rf ri/{PrideIO,ParallelEach,PrideLOL,Kernel,MockExpectationError,Module,Object,Test}
rm ri/created.rid
rm ri/cache.ri

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_ridir},%{ruby_rdocdir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a ri/* $RPM_BUILD_ROOT%{ruby_ridir}
cp -a rdoc $RPM_BUILD_ROOT%{ruby_rdocdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc History.txt README.txt
%dir %{ruby_vendorlibdir}/hoe
%{ruby_vendorlibdir}/hoe/minitest.rb
%{ruby_vendorlibdir}/minitest

%files rdoc
%defattr(644,root,root,755)
%{ruby_rdocdir}/%{name}-%{version}
%{ruby_ridir}/MiniTest
%{ruby_ridir}/Minitest
%{ruby_ridir}/Hoe
