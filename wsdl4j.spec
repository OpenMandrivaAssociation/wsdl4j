%define section         free
%define gcj_support     1
%define cvsver          1_6_2

Summary:        Web Services Description Language Toolkit for Java
Name:           wsdl4j
Version:        1.6.2
Release:        %mkrel 2.0.8
Epoch:          0
Group:          Development/Java
License:        CPL
URL:            http://sourceforge.net/projects/wsdl4j
Source0:        wsdl4j-%{version}-src.tar.gz
Source1:        wsdl4j-%{version}.pom
##cvs -d:pserver:anonymous@wsdl4j.cvs.sourceforge.net:/cvsroot/wsdl4j login
##cvs -z3 -d:pserver:anonymous@wsdl4j.cvs.sourceforge.net:/cvsroot/wsdl4j export -r wsdl4j-1_6_2 wsdl4j
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
BuildRequires:  java-rpmbuild >= 0:1.5
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
%setup -q -n %{name}
%remove_java_binaries

%build
export OPT_JAR_LIST="ant/ant-junit junit"
%{ant} -Dbuild.compiler=modern compile test javadocs

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}

install -m 644 build/lib/%{name}.jar \
      $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
install -m 644 build/lib/qname.jar \
      $RPM_BUILD_ROOT%{_javadir}/wsdl-qname-%{version}.jar
ln -sf $RPM_BUILD_ROOT%{_javadir}/wsdl-qname-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/qname.jar
#touch $RPM_BUILD_ROOT%{_javadir}/qname.jar # for %ghost

(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)


%add_to_maven_depmap wsdl4j wsdl4j %{version} JPP wsdl4j

# poms
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -pm 644 %{SOURCE1} \
    $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.wsdl4j.pom

# javadoc
install -d -m 0755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a build/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/
(cd $RPM_BUILD_ROOT%{_javadocdir} && %{__ln_s} %{name}-%{version} %{name})

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
/usr/sbin/update-alternatives --install %{_javadir}/qname.jar qname %{_javadir}/wsdl-qname.jar 00100
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
if [ "$1" = "0" ]; then
    /usr/sbin/update-alternatives --remove qname %{_javadir}/wsdl-qname.jar
fi
%update_maven_depmap
%if %{gcj_support}
%{clean_gcjdb}
%endif

%files
%defattr(0644,root,root,0755)
%doc license.html
%ghost %{_javadir}/qname.jar
%{_javadir}/*
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}
