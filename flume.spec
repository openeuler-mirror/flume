Name:          flume
Version:       1.10.0
Release:       1
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
%setup -q -n apache-flume-1.10.0-src
mvn install:install-file -DgroupId=ua_parser -DartifactId=ua-parser -Dversion=1.3.0 -Dpackaging=jar -Dfile=%{SOURCE1}
mvn install:install-file -DgroupId=org.pentaho -DartifactId=pentaho-aggdesigner-algorithm -Dversion=5.1.5-jhyde -Dpackaging=jar -Dfile=%{SOURCE2}
mvn install:install-file -DgroupId=eigenbase -DartifactId=eigenbase-properties -Dversion=1.1.4 -Dpackaging=jar -Dfile=%{SOURCE4}
mvn install:install-file -DgroupId=net.hydromatic -DartifactId=linq4j -Dversion=0.4 -Dpackaging=jar -Dfile=%{SOURCE5}
mvn install:install-file -DgroupId=net.hydromatic -DartifactId=quidem -Dversion=0.1.1 -Dpackaging=jar -Dfile=%{SOURCE6}
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
* Fri Aug 12 2022 xiexing <xiexing4@hisilicon.com> - 1.10.1-1
- fix cve problem

* Wed May 18 2022 liukuo <liukuo@kylinos.cn> - 1.9.0-2
- License compliance rectification

* Tue Apr 13 2021 Ge Wang <wangge20@huawei.com> 1.9.0-1
- Init package
