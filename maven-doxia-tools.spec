%global pkg_name maven-doxia-tools
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

Name:		%{?scl_prefix}%{pkg_name}
Version:	1.4
Release:	14.10%{?dist}
Summary:	Maven Doxia Integration Tools

License:	ASL 2.0
URL:		http://maven.apache.org/shared/maven-doxia-tools/
Source0:	http://repo1.maven.org/maven2/org/apache/maven/shared/%{pkg_name}/%{version}/%{pkg_name}-%{version}-source-release.zip

BuildRequires:	%{?scl_prefix_java_common}apache-commons-io >= 1.4
BuildRequires:	%{?scl_prefix_java_common}apache-commons-logging
BuildRequires:	%{?scl_prefix}plexus-utils
BuildRequires:	%{?scl_prefix}plexus-interpolation
BuildRequires:	%{?scl_prefix}plexus-containers-container-default
BuildRequires:	%{?scl_prefix}plexus-i18n
BuildRequires:	%{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix}maven-doxia-logging-api
BuildRequires:	%{?scl_prefix}maven-doxia-sitetools
BuildRequires:	%{?scl_prefix}maven-resources-plugin
BuildRequires:	%{?scl_prefix}maven-plugin-testing-harness
BuildRequires:	%{?scl_prefix}maven-reporting-impl
BuildRequires:	%{?scl_prefix}maven-shared
BuildRequires:	%{?scl_prefix}plexus-containers-component-metadata

BuildArch:	noarch


%description
A collection of tools to help the integration of Doxia in Maven plugins.

%package javadoc
Summary:	Javadoc for %{pkg_name}

%description javadoc
API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
# use plexus-component-metadata instead of old plugin
%pom_remove_plugin :plexus-maven-plugin
%pom_add_plugin org.codehaus.plexus:plexus-component-metadata pom.xml "
         <executions>
           <execution>
             <id>create-component-descriptor</id>
             <goals>
              <goal>generate-metadata</goal>
             </goals>
           </execution>
         </executions>
"

%mvn_alias : org.apache.maven.doxia:doxia-integration-tools
%{?scl:EOF}

%build
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
# test failures due to guice/cglib
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl_java_common} %{scl_maven} %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%dir %{_mavenpomdir}/%{pkg_name}
%dir %{_javadir}/%{pkg_name}
%doc LICENSE NOTICE DEPENDENCIES

%files javadoc -f .mfiles-javadoc
%doc LICENSE

%changelog
* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-14.10
- Add directory ownership on %%{_mavenpomdir} subdir

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1.4-14.9
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 1.4-14.8
- Rebuild to regenerate requires from java-common

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1.4-14.7
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-14.6
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-14.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-14.4
- Mass rebuild 2014-02-18
- Add missing BR: maven-shared

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 1.4-14.3
- SCL-ize BR/R

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-14.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-14.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.4-14
- Mass rebuild 2013-12-27

* Fri Aug 16 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4-13
- Migrate away from mvn-rpmbuild (#997442)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-12
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Apr 10 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-11
- Remove test dependencies

* Mon Feb 18 2013 Tomas Radej <tradej@redhat.com> - 1.4-10
- Removed BR on maven-shared (unnecessary + blocking maven-shared retirement)

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.4-9
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 24 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-8
- Add extra depmap for doxia-integration-tools >= 1.5

* Thu Dec 20 2012 Michal Srb <msrb@redhat.com> - 1.4-7
- Migrated from maven-doxia to doxia subpackages (Resolves: #889146)

* Tue Dec 11 2012 Michal Srb <msrb@redhat.com> - 1.4-6
- Migrated to plexus-containers-container-default (Resolves: #878555)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 5 2011 Alexander Kurtakov <akurtako@redhat.com> 1.4-3
- Don't require post/postun jpackage-utils.

* Tue Sep 27 2011 Alexander Kurtakov <akurtako@redhat.com> 1.4-2
- Install license as doc.
- Use new package names.
- Merge and update patches.
- Use new macro

* Fri Jun 24 2011 Jaromir Capik <jcapik@redhat.com> 1.4-1
- Update to 1.4
- Migration from plexus-maven-plugin to plexus-containers-component-metadata
- Dependency maven-compat introduced
- Minor spec file changes according to the latest guidelines

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue May 11 2010 Mary Ellen Foster <mefoster at gmail.com> 1.2-4
- BuildRequire jakarta-commons-logging

* Mon May 10 2010 Mary Ellen Foster <mefoster at gmail.com> 1.2-3
- BuildRequire java >= 1:1.6.0
- Clean up changelog numbers

* Mon May 10 2010 Mary Ellen Foster <mefoster at gmail.com> 1.2-2
- Get (Build)Requirements right

* Wed Mar 31 2010 Mary Ellen Foster <mefoster at gmail.com> 1.2-1
- Initial version
- Don't run tests until maven-surefire is rebuilt
