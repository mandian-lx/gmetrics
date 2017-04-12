%{?_javapackages_macros:%_javapackages_macros}
%global oname GMetrics

Name:          gmetrics
Version:       0.7
Release:       2%{?dist}
Summary:       Groovy library that provides reports and metrics for Groovy code
Group:         Development/Java
License:       ASL 2.0
Url:           http://gmetrics.sourceforge.net/
Source0:       http://downloads.sourceforge.net/%{name}/%{oname}-%{version}-bin.tar.gz

BuildRequires: maven-local
BuildRequires: mvn(junit:junit)
BuildRequires: mvn(log4j:log4j:12)
BuildRequires: mvn(org.apache.ant:ant)
BuildRequires: mvn(org.codehaus.gmavenplus:gmavenplus-plugin)
BuildRequires: mvn(org.codehaus.groovy:groovy)
BuildRequires: mvn(org.codehaus.groovy:groovy-ant)
BuildRequires: mvn(org.codehaus.groovy:groovy-xml)
BuildRequires: mvn(org.codehaus.groovy:groovy-test)
BuildRequires: mvn(org.sonatype.oss:oss-parent:pom:)

BuildArch:     noarch

%description
GMetrics provides calculation and reporting of size and
complexity metrics for Groovy source code, by scanning the
code with an Ant Task, applying a set of metrics, and
generating an HTML or XML report of the results.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q -n %{oname}-%{version}
# Cleanup
find . -name "*.jar" -delete
find . -name "*.class" -delete
rm -rf docs/*

%pom_remove_plugin :maven-assembly-plugin
%pom_remove_plugin :maven-javadoc-plugin
%pom_remove_plugin :maven-release-plugin
%pom_remove_plugin :maven-site-plugin

%pom_remove_plugin :gmaven-plugin
%pom_add_plugin org.codehaus.gmavenplus:gmavenplus-plugin:1.5 . "
 <executions>
  <execution>
   <goals>
    <goal>generateStubs</goal>
    <goal>testGenerateStubs</goal>
   </goals>
  </execution>
 </executions>"

%pom_remove_dep :CodeNarc
%pom_change_dep :log4j ::12

# package org.apache.tools.ant does not exist
%pom_add_dep org.apache.ant:ant:1.9.6 . "<optional>true</optional>"

#sed -i "s|pom.version|project.version|" pom.xml

chmod 644 README.txt

# Convert from dos to unix line ending
for file in CHANGELOG.txt LICENSE.txt NOTICE.txt README.txt ; do
 sed -i.orig 's|\r||g' $file
 touch -r $file.orig $file
 rm $file.orig
done

%mvn_file :%{oname} %{name} %{oname}

%build

# test skipped require Codenarc, circular deps
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc CHANGELOG.txt README.txt
%doc LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt

%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Aug 16 2016 gil cattaneo <puntogil@libero.it> 0.7-1
- update to 0.7

* Tue Jun 21 2016 gil cattaneo <puntogil@libero.it> 0.6-15
- add missing build requires

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 23 2015 gil cattaneo <puntogil@libero.it> 0.6-13
- fix FTBFS
- use groovy 2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 30 2015 gil cattaneo <puntogil@libero.it> 0.6-11
- introduce license macro
- re-base for use groovy 2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 0.6-9
- Use Requires: java-headless rebuild (#1067528)

* Thu Nov 14 2013 gil cattaneo <puntogil@libero.it> 0.6-8
- use objectweb-asm3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 08 2013 gil cattaneo <puntogil@libero.it> 0.6-6
- switch to XMvn
- minor changes to adapt to current guideline

* Thu Mar 14 2013 gil cattaneo <puntogil@libero.it> 0.6-5
- Use maven-antrun-plugin instead of gmaven

* Fri Feb 15 2013 gil cattaneo <puntogil@libero.it> 0.6-4
- build fix for f19

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 0.6-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Mon Sep 24 2012 gil cattaneo <puntogil@libero.it> 0.6-1
- update to 0.6
- enable gmaven support

* Mon Aug 06 2012 gil cattaneo <puntogil@libero.it> 0.5-2
- fixed the permissions and encoding issues on *.txt files
- change with_gmaven to 0 (only for now)
- generate javadocs with ant support

* Sat Mar 03 2012 gil cattaneo <puntogil@libero.it> 0.5-1
- initial rpm
