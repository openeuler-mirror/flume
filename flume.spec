Name:          flume
Version:       1.10.0
Release:       3
Summary:       Apache Flume is a distributed, reliable, and availble service for efficiently collecting, aggregating, and moving large amounts of log data.

License:       Public Domain and MIT and Apache 2.0
URL:           https://github.com/apache/flume

Source0:       https://dlcdn.apache.org/flume/1.10.0/apache-flume-1.10.0-src.tar.gz
Source1:       ua-parser-1.3.0.jar
Source2:       pentaho-aggdesigner-algorithm-5.1.5-jhyde.jar
Source3:       xmvn-reactor
Source4:       eigenbase-properties-1.1.4.jar
Source5:       linq4j-0.4.jar
Source6:       quidem-0.1.1.jar
# Maven dependencies we use to speedup build on OBS.
# We don't upstream this.
Source7:       icu4j.tar.gz
Source8:       zstd-jni.tar.gz
Source9:       tomcat-embed-core.tar.gz
Source10:      hadoop-hdfs-client.tar.gz
Source11:      hbase-protocol.tar.gz
Source12:      hadoop-hdfs.tar.gz
Source13:      hbase-server.tar.gz
Source14:      hbase-protocol-shaded.tar.gz
Source15:      lucene-analyzers-kuromoji.tar.gz
Source16:      lucene-test-framework.tar.gz
Source17:      pdfbox.tar.gz
Source18:      poi-ooxml-schemas.tar.gz
Source19:      Saxon-HE.tar.gz
Source20:      org.restlet-2.1.1.jar
Source21:      org.restlet.ext.servlet-2.1.1.jar
Source22:      hbase-shaded-netty.tar.gz
Source23:      ant.tar.gz
Source24:      apache-log4j-extras.tar.gz
Source25:      commons-httpclient.tar.gz
Source26:      hive-ant.tar.gz
Source27:      ST4.tar.gz
Source28:      velocity.tar.gz
Source29:      zstd-jni.tar.gz
Source30:      calcite-core.tar.gz
Source31:      groovy-all.tar.gz
Source32:      hive-exec.tar.gz
Source33:      hive-metastore.tar.gz
Source34:      hadoop-yarn-api.tar.gz
Source35:      curator-client.tar.gz

Patch6000:     backport-CVE-2022-34916.patch

BuildRequires: java-1.8.0-openjdk-devel maven xmvn xmvn-install gradle-local maven-local 
Requires: java-1.8.0-openjdk

BuildArch:     noarch

%description
Apache Flume is a distributed, reliable, and available service for efficiently collecting, 
aggregating, and moving large amounts of log data. It has a simple and flexible architecture 
based on streaming data flows. It is robust and fault tolerant with tunable reliability
mechanisms and many failover and recovery mechanisms. The system is centrally managed and 
allows for intelligent dynamic management. It uses a simple extensible data model that allows
for online analytic application.

%prep
%autosetup -n apache-flume-1.10.0-src -p1
mvn install:install-file -DgroupId=ua_parser -DartifactId=ua-parser -Dversion=1.3.0 -Dpackaging=jar -Dfile=%{SOURCE1}
mvn install:install-file -DgroupId=org.pentaho -DartifactId=pentaho-aggdesigner-algorithm -Dversion=5.1.5-jhyde -Dpackaging=jar -Dfile=%{SOURCE2}
mvn install:install-file -DgroupId=eigenbase -DartifactId=eigenbase-properties -Dversion=1.1.4 -Dpackaging=jar -Dfile=%{SOURCE4}
mvn install:install-file -DgroupId=net.hydromatic -DartifactId=linq4j -Dversion=0.4 -Dpackaging=jar -Dfile=%{SOURCE5}
mvn install:install-file -DgroupId=net.hydromatic -DartifactId=quidem -Dversion=0.1.1 -Dpackaging=jar -Dfile=%{SOURCE6}
mvn install:install-file -DgroupId=org.restlet.jee -DartifactId=org.restlet -Dversion=2.1.1 -Dpackaging=jar -Dfile=%{SOURCE20}
mvn install:install-file -DgroupId=org.restlet.jee -DartifactId=org.restlet.ext.servlet -Dversion=2.1.1 -Dpackaging=jar -Dfile=%{SOURCE21}

cp %{SOURCE3} ./.xmvn-reactor
echo `pwd` > absolute_prefix.log
sed -i 's/\//\\\//g' absolute_prefix.log
absolute_prefix=`head -n 1 absolute_prefix.log`
sed -i 's/absolute-prefix/'"$absolute_prefix"'/g' .xmvn-reactor

find -name "*.jar" -delete
find -name "*.cmd" -delete

%build
# for javadoc encoding
export LC_ALL=en_US.UTF-8

mkdir -p /home/abuild/.m2/repository/
tar -zxvf %{SOURCE7} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE8} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE9} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE10} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE11} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE12} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE13} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE14} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE15} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE16} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE17} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE18} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE19} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE22} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE23} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE24} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE25} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE26} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE27} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE28} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE29} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE30} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE31} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE32} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE33} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE34} -C /home/abuild/.m2/repository/
tar -zxvf %{SOURCE35} -C /home/abuild/.m2/repository/

mvn package -DskipTests -Pdist -Dtar

%install
%mvn_install -J build/dist/docs

install -d -m 0755 %{buildroot}%{_bindir}
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 0755 %{buildroot}%{_datadir}/%{name}/bin
install -d -m 0755 %{buildroot}%{_datadir}/%{name}/conf
install -d -m 0755 %{buildroot}%{_datadir}/%{name}/lib
install -d -m 0755 %{buildroot}%{_datadir}/%{name}/tools
install -d -m 0755 %{buildroot}%{_datadir}/doc/%{name}

pushd flume-ng-dist/target/apache-flume-1.10.0-bin/apache-flume-1.10.0-bin
  cp -arf bin/* %{buildroot}%{_datadir}/%{name}/bin
  cp -arf conf/* %{buildroot}%{_datadir}/%{name}/conf
  cp -arf lib/* %{buildroot}%{_datadir}/%{name}/lib
  cp -arf tools/* %{buildroot}%{_datadir}/%{name}/tools
  for f in DEVNOTES doap_Flume.rdf LICENSE NOTICE README.md RELEASE-NOTES;do
    cp -f ${f} %{buildroot}%{_datadir}/doc/%{name}
  done
popd

# /usr/bin
pushd flume-ng-dist/target/apache-flume-1.10.0-bin/apache-flume-1.10.0-bin/bin
  ls | awk '{print $1}' | for line in `xargs`;do
    ln -s %{_datadir}/%{name}/bin/${line} %{buildroot}%{_bindir}/${line}
  done
popd

# /usr/share/flume/lib
pushd flume-ng-dist/target/apache-flume-1.10.0-bin/apache-flume-1.10.0-bin/lib
  for f in `ls flume-* | grep -v tests | grep -v examples`
  do 
    pkgname=`echo $f | sed "s/-%{version}//"`
    rm -f %{buildroot}%{_datadir}/%{name}/lib/$f
    ln -s %{_datadir}/java/%{name}/${pkgname} %{buildroot}%{_datadir}/%{name}/lib/$f
  done
popd

%files -f .mfiles
%doc %{_datadir}/doc/%{name}/* 
%{_bindir}/*
%{_datadir}/%{name}/*
%{_sysconfdir}/%{name}
%dir %{_javadir}/%{name}

%changelog
* Thu Nov 24 2022 misaka00251 <liuxin@iscas.ac.cn> - 1.10.0-3
- Fix build on OBS

* Mon Aug 22 2022 yinyongkang <yinyongkang@kylinos.cn> - 1.10.0-2
- Type:CVE
- ID:CVE-2022-34916
- SUG:NA
- DESC:Fix CVE-2022-34916

* Wed Aug 3 2022 xiexing <xiexing4@hisilicon.com> - 1.10.0-1
- fix cve problem

* Wed May 18 2022 liukuo <liukuo@kylinos.cn> - 1.9.0-2
- License compliance rectification

* Tue Apr 13 2021 Ge Wang <wangge20@huawei.com> 1.9.0-1
- Init package
