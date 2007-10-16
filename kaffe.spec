%define with_ecj        1
%define section         free

%define origin          kaffe
%define originver       1.1.8
%define libver          %{originver}
%define priority        1500
%define javaver         1.5.0
%define buildver        00

%define javaname        java-%{javaver}-%{origin}
%define javaversion     %{javaver}.%{buildver}
%define release         %mkrel 1

%define toplevel_dir    j2sdk%{javaver}_%{buildver}
%define sdklnk          java-%{javaver}-%{origin}
%define jrelnk          jre-%{javaver}-%{origin}
%define sdkdir          %{javaname}-%{javaversion}
%define jredir          %{sdkdir}/jre
%define sdkbindir       %{_jvmdir}/%{sdklnk}/bin
%define jrebindir       %{_jvmdir}/%{jrelnk}/bin
%define jvmjardir       %{_jvmjardir}/%{javaname}-%{javaversion}

# Define target architecture we are building for
%define target_cpu %{_target_cpu}
%ifarch %{ix86}
%define target_cpu i386
%endif
%ifarch amd64
%define target_cpu x86_64
%endif
%ifarch ppc
%define target_cpu powerpc
%endif

%define kaffedir        %{_jvmdir}/%{sdkdir}

Name:           kaffe
Version:        %{originver}
Release:        %mkrel 1
Epoch:          0
Summary:        Free virtual machine for running Java(TM) code
License:        GPL
Group:          Development/Java
Url:            http://www.kaffe.org/
Source0:        ftp://ftp.kaffe.org/pub/kaffe/v1.1.x-development/kaffe-%{version}.tar.bz2
Source1:        ftp://ftp.kaffe.org/pub/kaffe/v1.1.x-development/kaffe-%{version}.tar.bz2.sig
Patch1:         kaffe-20070217-warning-fix.patch
Patch2:         kaffe-20070217-generics.patch
Requires:       classpath
Obsoletes:      %{javaname}        
Provides:       %{javaname} = %{epoch}:%{javaversion}-%{release}
Provides:       jre-%{javaver}-%{origin} = %{epoch}:%{javaversion}-%{release}
Provides:       jre-%{origin} = %{epoch}:%{javaversion}-%{release}
Provides:       jre-%{javaver}, java-%{javaver}, jre = %{epoch}:%{javaver}
Provides:       java-%{origin} = %{epoch}:%{javaversion}-%{release}
Provides:       java = %{epoch}:%{javaver}
Provides:       jndi = %{epoch}:%{javaversion}, jndi-ldap = %{epoch}:%{javaversion}
Provides:       jsse = %{epoch}:%{javaversion}
Provides:       jce = %{epoch}:%{javaversion}
Provides:       jdbc-stdext = %{epoch}:3.0, jdbc-stdext = %{epoch}:%{javaversion}
BuildRequires:  alsa-lib-devel
BuildRequires:  bcel
BuildRequires:  chrpath
BuildRequires:  classpath-devel
BuildRequires:  esound-devel
BuildRequires:  fastjar
BuildRequires:  gmp-devel
BuildRequires:  libjpeg-devel
%if !%{with_ecj}
BuildRequires:  jikes > 0:1.22
%else
BuildRequires:  ecj
%endif
BuildRequires:  jpackage-utils >= 0:1.5
BuildRequires:  gcc-java
BuildRequires:  libungif-devel
BuildRequires:  zip
BuildRequires:  zlib-devel
BuildRequires:  libgdk_pixbuf2.0-devel
BuildRequires:  libgtk+2.0-devel
BuildRequires:  libglib2-devel
BuildRequires:  libxtst-devel
BuildRequires:  libGConf2-devel
ExclusiveArch:  %{ix86} ppc x86_64 amd64 ia64
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
AutoReq:        no

%description
Kaffe is a free virtual machine designed to execute Java(TM) bytecode. 
Kaffe can be configured in two modes. In the first mode, it operates as 
a pure bytecode interpreter (not unlike Javasoft's machine). In the 
second mode, it performs "Just-In-Time" code conversion from the 
abstract code to the host machine's native code.  The second mode will 
ultimately allow execution of Java code at the same speed as standard 
compiled code, while also maintaining the advantages and flexibility of 
code independence.

Note that Sun's Swing 1.1.1 implementation also works with Kaffe.

Install the kaffe package if you need a Java virtual machine.

%package devel
Summary:        Development package with static libs and headers for kaffe
Group:          Development/Java
Obsoletes:      %{javaname}-devel < 0:%{javaversion}-%{release}
Provides:       %{javaname}-devel = 0:%{javaversion}-%{release}
%if !%{with_ecj}
Requires:       jikes > 0:1.22
%else
Requires:       ecj
%endif
Requires:       %{origin} = %{epoch}:%{originver}-%{release}
Requires:       update-alternatives
Provides:       java-sdk-%{javaver}-%{origin} = %{epoch}:%{javaversion}-%{release}
Provides:       java-sdk-%{origin} = %{epoch}:%{javaversion}-%{release}
Provides:       java-sdk-%{javaver}, java-sdk = %{epoch}:%{javaver}
Provides:       java-devel-%{origin} = %{epoch}:%{javaversion}-%{release}
Provides:       java-%{javaver}-devel, java-devel = %{epoch}:%{javaver}
Requires:       %{javaname} = %{epoch}:%{javaversion}-%{release}

%description devel
This package contains the static libraries, header files and documentation
necessary for development of programs that will use kaffe.

You should install this package if you need to develop programs which
will use kaffe functions.

You'll also need to install kaffe package.

%prep
%setup -q
%patch1 -p1 -b .chdir
%patch2 -p1 -b .generics

%{__perl} -pi -e 's|\@JIKESPROG\@|%{_bindir}/ecj|' kaffe/scripts/compat/javac.in

%build
%ifarch %{ix86}
export CFLAGS="%{optflags} -fno-omit-frame-pointer"
%endif
export CFLAGS="${CFLAGS} `pkg-config --cflags pangoft2`"
export LIBS="${LIBS} `pkg-config --libs pangoft2`"
%{configure2_5x} \
           --prefix=%{kaffedir} \
           --bindir=%{kaffedir}/bin \
           --datadir=%{kaffedir}/share \
           --libdir=%{kaffedir}/lib \
           --includedir=%{kaffedir}/include \
           --mandir=%{kaffedir}/man \
           --disable-rpath \
%if %{with_ecj}
           --with-ecj=%{_bindir}/ecj \
%endif
           --with-glibj-zip=%{_datadir}/classpath/glibj.zip \
           --with-system-classpath \
           --with-classpath-prefix=%{_prefix} \
           --with-classpath-classes=%{_datadir}/classpath/glibj.zip \
           --with-classpath-libdir=%{_libdir}/classpath \
           --with-classpath-includedir=%{_includedir} \
           --enable-gcj \
           --enable-gjdoc \
           --with-bcel=%{_javadir}/bcel.jar \
           --enable-jvmpi \
           --without-kaffe-x-awt \
           --without-kaffe-qt-awt \
           --with-qt-libraries=%{_prefix}/lib/qt3/%{_lib} \
           --with-qt-binaries=%{_prefix}/lib/qt3/bin \
           --with-qtdir=%{_prefix}/lib/qt3 \
           --with-jni-library-path=%{_jnidir} \
           --disable-Werror
%{make} JAVAC="%{_bindir}/ecj -1.5"

%check
%if 0
%{make} check
%endif

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}

(cd %{buildroot}%{kaffedir}/jre/lib && %{__ln_s} glibj.zip rt.jar)

(cd %{buildroot}%{_jvmdir}/%{sdkdir}/lib && %{__ln_s} %{_jvmdir}/%{jredir}/lib/rt.jar tools.jar)

# extensions handling
install -d -m 755 %{buildroot}%{jvmjardir}
pushd %{buildroot}%{jvmjardir}
   ln -sf %{_jvmdir}/%{jredir}/lib/rt.jar jsse-%{javaversion}.jar
   ln -sf %{_jvmdir}/%{jredir}/lib/rt.jar jce-%{javaversion}.jar
   ln -sf %{_jvmdir}/%{jredir}/lib/rt.jar jndi-%{javaversion}.jar
   ln -sf %{_jvmdir}/%{jredir}/lib/rt.jar jndi-ldap-%{javaversion}.jar
   ln -sf %{_jvmdir}/%{jredir}/lib/rt.jar jdbc-stdext-%{javaversion}.jar
   ln -sf jdbc-stdext-%{javaversion}.jar jdbc-stdext-3.0.jar
   for jar in *-%{javaversion}.jar ; do
      ln -sf ${jar} $(echo $jar | sed "s|-%{javaversion}.jar|-%{javaver}.jar|g")
      ln -sf ${jar} $(echo $jar | sed "s|-%{javaversion}.jar|.jar|g")
   done
popd

# versionless symlinks
pushd %{buildroot}%{_jvmdir}
ln -sf %{jredir} %{jrelnk}
ln -sf %{sdkdir} %{sdklnk}
popd

pushd %{buildroot}%{_jvmjardir}
ln -sf %{sdkdir} %{jrelnk}
ln -sf %{sdkdir} %{sdklnk}
popd

%clean
%{__rm} -rf %{buildroot}

%post
update-alternatives --install %{_bindir}/java java %{jrebindir}/java %{priority} \
--slave %{_jvmdir}/jre                     jre                         %{_jvmdir}/%{jrelnk} \
--slave %{_jvmjardir}/jre                  jre_exports                 %{_jvmjardir}/%{jrelnk} \
--slave %{_bindir}/rmiregistry             rmiregistry                 %{jrebindir}/rmiregistry \
--slave %{_bindir}/keytool                 keytool                     %{jrebindir}/gkeytool

update-alternatives --install %{_jvmdir}/jre-%{origin} jre_%{origin} %{_jvmdir}/%{jrelnk} %{priority} \
--slave %{_jvmjardir}/jre-%{origin}        jre_%{origin}_exports     %{_jvmjardir}/%{jrelnk}

update-alternatives --install %{_jvmdir}/jre-%{javaver} jre_%{javaver} %{_jvmdir}/%{jrelnk} %{priority} \
--slave %{_jvmjardir}/jre-%{javaver}       jre_%{javaver}_exports      %{_jvmjardir}/%{jrelnk}

%post devel
update-alternatives --install %{_bindir}/javac javac %{sdkbindir}/javac %{priority} \
--slave %{_jvmdir}/java                     java_sdk                    %{_jvmdir}/%{sdklnk} \
--slave %{_jvmjardir}/java                  java_sdk_exports            %{_jvmjardir}/%{sdklnk} \
--slave %{_bindir}/appletviewer             appletviewer                %{sdkbindir}/gappletviewer \
--slave %{_bindir}/jar                      jar                         %{sdkbindir}/jar \
--slave %{_bindir}/jarsigner                jarsigner                   %{sdkbindir}/gjarsigner \
--slave %{_bindir}/javadoc                  javadoc                     %{sdkbindir}/javadoc \
--slave %{_bindir}/javah                    javah                       %{sdkbindir}/javah \
--slave %{_bindir}/javap                    javap                       %{sdkbindir}/javap \
--slave %{_bindir}/jdb                      jdb                         %{sdkbindir}/jdb \
--slave %{_bindir}/native2ascii             native2ascii                %{sdkbindir}/native2ascii \
--slave %{_bindir}/rmic                     rmic                        %{sdkbindir}/rmic \
--slave %{_bindir}/serialver                serialver                   %{sdkbindir}/serialver

update-alternatives --install %{_jvmdir}/java-%{origin} java_sdk_%{origin} %{_jvmdir}/%{sdklnk} %{priority} \
--slave %{_jvmjardir}/java-%{origin}        java_sdk_%{origin}_exports     %{_jvmjardir}/%{sdklnk}

update-alternatives --install %{_jvmdir}/java-%{javaver} java_sdk_%{javaver} %{_jvmdir}/%{sdklnk} %{priority} \
--slave %{_jvmjardir}/java-%{javaver}       java_sdk_%{javaver}_exports      %{_jvmjardir}/%{sdklnk}

%postun
if [ $1 -eq 0 ]; then
  update-alternatives --remove java %{jrebindir}/java
fi

%postun devel
if [ $1 -eq 0 ]; then
  update-alternatives --remove javac %{sdkbindir}/javac
  update-alternatives --remove java_sdk_%{origin}  %{_jvmdir}/%{sdklnk}
  update-alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdklnk}
fi

%files
%defattr(-,root,root)
%doc AUTHORS license* README RELEASE-NOTES THIRDPARTY TODO WHATSNEW
%dir %{kaffedir}
%dir %{kaffedir}/bin
%{kaffedir}/bin/java
%{kaffedir}/bin/kaffe
%{kaffedir}/jre
%{kaffedir}/lib
%{kaffedir}/man
%{kaffedir}/share
%{_jvmdir}/%{jrelnk}
%{_jvmjardir}/%{jrelnk}
%{jvmjardir}/*.jar

%files devel
%defattr(-,root,root)
%doc ABOUT-NLS BUILD_ENVIRONMENT ChangeLog.* developers FAQ
%{kaffedir}/bin/install-jar
%{kaffedir}/bin/jar
%{kaffedir}/bin/javadoc
%{kaffedir}/bin/javac
%{kaffedir}/bin/javah
%{kaffedir}/bin/javap
%{kaffedir}/bin/jdb
%{kaffedir}/bin/kaffeh
%{kaffedir}/bin/native2ascii
%{kaffedir}/bin/rmic
%{kaffedir}/bin/rmiregistry
%{kaffedir}/bin/serialver
%{kaffedir}/include
%{_jvmdir}/%{sdklnk}
%{_jvmjardir}/%{sdklnk}
