%define cvsver          %(echo %version |sed -e 's,\.,_,g')

Summary:        Web Services Description Language Toolkit for Java
Name:           wsdl4j
Version:        1.6.2
Release:        3
Epoch:          0
Group:          Development/Java
License:        CPL
URL:            http://sourceforge.net/projects/wsdl4j
Source0:        wsdl4j-%{version}-src.tar.gz
Source1:        wsdl4j-%{version}.pom
##cvs -d:pserver:anonymous@wsdl4j.cvs.sourceforge.net:/cvsroot/wsdl4j login
##cvs -z3 -d:pserver:anonymous@wsdl4j.cvs.sourceforge.net:/cvsroot/wsdl4j export -r wsdl4j-1_6_2 wsdl4j
BuildArch:      noarch
Requires:       jaxp_parser_impl
BuildRequires:  java-1.6.0-openjdk-devel
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
ln -sf wsdl-qname-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/qname.jar
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

%post
%update_maven_depmap
/usr/sbin/update-alternatives --install %{_javadir}/qname.jar qname %{_javadir}/wsdl-qname.jar 00100

%postun
if [ "$1" = "0" ]; then
    /usr/sbin/update-alternatives --remove qname %{_javadir}/wsdl-qname.jar
fi
%update_maven_depmap

%files
%defattr(0644,root,root,0755)
%doc license.html
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


%changelog
* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.6.2-2.0.7mdv2011.0
+ Revision: 608174
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:1.6.2-2.0.6mdv2010.1
+ Revision: 524358
- rebuilt for 2010.1

* Fri Jan 09 2009 Jérôme Soyer <saispo@mandriva.org> 0:1.6.2-2.0.5mdv2009.1
+ Revision: 327438
- Link qname to wsdl-qname

* Wed Mar 19 2008 Nicolas Vigier <nvigier@mandriva.com> 0:1.6.2-2.0.4mdv2008.1
+ Revision: 189036
- fix /etc/alternatives/qname link

* Wed Mar 19 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.6.2-2.0.3mdv2008.1
+ Revision: 188956
- qname.jar should be a ghost

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Dec 16 2007 Anssi Hannula <anssi@mandriva.org> 0:1.6.2-2.0.2mdv2008.1
+ Revision: 121047
- buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Wed Dec 12 2007 Alexander Kurtakov <akurtakov@mandriva.org> 0:1.6.2-2.0.1mdv2008.1
+ Revision: 118626
- add maven poms (jpp sync)

* Sun Dec 09 2007 David Walluck <walluck@mandriva.org> 0:1.6.2-0.0.1mdv2008.1
+ Revision: 116631
- fix release tag
- 1.6.2
- fix javadocs

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:1.5.2-3.3mdv2008.0
+ Revision: 87259
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat


* Fri Mar 16 2007 Christiaan Welvaart <spturtle@mandriva.org> 1.5.2-3.2mdv2007.1
+ Revision: 144754
- rebuild for 2007.1

  + David Walluck <walluck@mandriva.org>
    - Import wsdl4j

* Sun Jul 23 2006 David Walluck <walluck@mandriva.org> 0:1.5.2-3.1mdv2007.0
- bump release

* Fri Jun 09 2006 David Walluck <walluck@mandriva.org> 0:1.5.2-2mdv2007.0
- remove qname.jar as it is provided by geronimo-specs

* Sat Jun 03 2006 David Walluck <walluck@mandriva.org> 0:1.5.2-1mdv2007.0
- 1.5.2
- rebuild for libgcj.so.7

* Sun Sep 11 2005 David Walluck <walluck@mandriva.org> 0:1.5.1-1.1mdk
- release

* Fri Jun 17 2005 Gary Benson <gbenson@redhat.com> 0:1.5.1-1jpp_1fc
- Build into Fedora.

* Sat Jun 11 2005 Gary Benson <gbenson@redhat.com>
- Remove.tar.bz2files from the tarball.

* Tue Jun 07 2005 Gary Benson <gbenson@redhat.com>
- Add build dependency on ant-junit.

* Fri Jun 03 2005 Fernando Nasser <fnasser@redhat.com> 0:1.5.1-1jpp_1rh
- Merge with upstream for update to 1.5.1

* Fri Jun 03 2005 Fernando Nasser <fnasser@redhat.com> 0:1.5.1-1jpp
- update to 1.5.1

* Fri Mar 11 2005 Ralph Apel <r.apel at r-apel.de> 0:1.5-1jpp
- update to 1.5

* Wed Nov 03 2004 Fernando Nasser <fnasser@redhat.com> 0:4.1.29-2jpp_2rh
- Rebuild

* Tue Aug 31 2004 Ralph Apel <r.apel at r-apel.de> 0:1.4-3jpp
- Build with ant-1.6.2

