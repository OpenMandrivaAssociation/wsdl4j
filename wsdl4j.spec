%define section         free
%define gcj_support     1
%define cvsver          1_6_2

Summary:        Web Services Description Language Toolkit for Java
Name:           wsdl4j
Version:        1.6.2
Release:        0.0.1
Epoch:                0
Group:          Development/Java
License:        CPL
URL:            http://sourceforge.net/projects/wsdl4j
Source0:        http://downloads.sourceforge.net/wsdl4j/wsdl4j-src-%{version}.zip
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:       jaxp_parser_impl
BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  junit

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
%setup -q -n %{name}-%{cvsver}

%build
export CLASSPATH=
export OPT_JAR_LIST="ant/ant-junit junit"
%{ant} -Dbuild.compiler=modern compile javadocs

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
(cd $RPM_BUILD_ROOT%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

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

%files
%defattr(0644,root,root,0755)
%doc license.html
%{_javadir}/*
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}
