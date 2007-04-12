%define name            wsdl4j
%define version         1.5.2
%define cvsver          1_5_2
%define release         %mkrel 3.2
%define section         free
%define gcj_support     1

# -----------------------------------------------------------------------------

Summary:        Web Services Description Language Toolkit for Java
Name:           %{name}
Version:        %{version}
Release:        %{release}
Epoch:		0
Group:          Development/Java
License:        CPL
URL:            http://sourceforge.net/projects/wsdl4j
# cvs -d:pserver:anonymous@wsdl4j.cvs.sourceforge.net:/cvsroot/wsdl4j login
# cvs -z3 -d:pserver:anonymous@wsdl4j.cvs.sourceforge.net:/cvsroot/wsdl4j co -P -r wsdl4j-1_5_2 wsdl4j
Source0:        http://download.sourceforge.net/wsdl4j/wsdl4j-src-%{version}.tar.bz2
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:       jaxp_parser_impl, java
BuildRequires:  ant, java-devel
BuildRequires:	jpackage-utils >= 0:1.5
BuildRequires:	junit
BuildRequires:	ant-junit

%description
The Web Services Description Language for Java Toolkit (WSDL4J) allows the
creation, representation, and manipulation of WSDL documents describing
services.  This codebase will eventually serve as a reference implementation
of the standard created by JSR110.

%package javadoc
Group:          Development/Java
Summary:        Javadoc for %{name}

%description javadoc
Javadoc for %{name}.

%prep
%setup -q -n %{name}

%build
export CLASSPATH=
export OPT_JAR_LIST="ant/ant-junit junit"
%ant -Dbuild.compiler=modern compile javadocs

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}

# qname.jar
for jar in %{name}.jar ; do
   vjar=$(echo $jar | sed s+.jar+-%{version}.jar+g)
   install -m 644 build/lib/$jar $RPM_BUILD_ROOT%{_javadir}/$vjar
   pushd $RPM_BUILD_ROOT%{_javadir}
      ln -fs $vjar $jar
   popd
done

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(0644,root,root,0755)
%doc license.html readme.txt
%{_javadir}/*
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}


