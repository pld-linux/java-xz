#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		srcname		xz
%include	/usr/lib/rpm/macros.java
Summary:	Java implementation of XZ data compression
Name:		java-%{srcname}
Version:	1.5
Release:	1
License:	Public Domain
Group:		Libraries/Java
Source0:	http://tukaani.org/xz/xz-java-%{version}.zip
# Source0-md5:	9032553a25f41a277fa0bb56bcdb5f1e
URL:		http://tukaani.org/xz/java.html
BuildRequires:	ant
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	unzip
Requires:	jpackage-utils
Requires:	jre
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A complete implementation of XZ data compression in Java.

It features full support for the .xz file format specification version
1.0.4, single-threaded streamed compression and decompression,
single-threaded decompression with limited random access support, raw
streams (no .xz headers) for advanced users, including LZMA2 with
preset dictionary.

%package javadoc
Summary:	Javadocs for %{name}

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -c

# During documentation generation the upstream build.xml tries to download
# package-list from oracle.com. Create a dummy package-list to prevent that.
install -d extdoc && touch extdoc/package-list

%build
%ant maven

%install
rm -rf $RPM_BUILD_ROOT
# jar
install -d $RPM_BUILD_ROOT%{_javadir}
cp -p build/jar/%{srcname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a build/doc/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc COPYING README THANKS
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
