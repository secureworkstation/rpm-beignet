%define commit f3d62504422a956cbc366fa2e4a44771c698516b
Name:           beignet
Version:        1.3.2.1
Release:        0.1.gitf3d6250%{?dist}
Summary:        Open source implementation of the OpenCL for Intel GPUs

License:        LGPLv2+
URL:            https://01.org/beignet/
# Source0:        https://01.org/sites/default/files/%%{name}-%%{version}-source.tar.gz
Source0:	https://github.com/linnaea/beignet/archive/%{commit}.tar.gz#/%{name}-%{commit}.tar.gz
# https://cgit.freedesktop.org/beignet/commit/?id=033464f4b8045a49dbcc1a84cde5c05986ca11c2
#Patch1:         0001-Add-AppStream-metadata.patch
# Sent to ignatenkobrain by Debian maintainers via email
#Patch2:         beignet-llvm6.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  llvm7.0-devel
# Custom clang7.0 build yields a clang7.0 package
BuildRequires:  clang7.0
BuildRequires:  clang7.0-devel
BuildRequires:  ncurses-devel
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libdrm_intel) >= 2.4.52
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(egl) >= 11.0.0
BuildRequires:  ocl-icd-devel
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libva-x11)
BuildRequires:  %{_bindir}/appstream-util

BuildRequires:  python3-devel

Requires:       opencl-filesystem

ExclusiveArch:  x86_64 %{ix86}

%description
Beignet is an open source implementation of the OpenCL specification - a generic
compute oriented API. This code base contains the code to run OpenCL programs
on Intel GPUs which basically defines and implements the OpenCL host functions
required to initialize the device, create the command queues, the kernels and
the programs and run them on the GPU. 

%package devel
Summary:        Development files for %{name}
Requires:       opencl-headers
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
%{summary}.

%prep
%autosetup -p1 -n %{name}-%{commit}
mkdir %{_target_platform}

%build
pushd %{_target_platform}
  %cmake .. \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DLLVM_INSTALL_DIR=%{_libdir}/llvm7.0/bin/    \
    -DENABLE_GL_SHARING=ON            \
    -DEXPERIMENTAL_DOUBLE=ON          \
    %{nil}
popd
%make_build -C %{_target_platform}

%install
%make_install -C %{_target_platform}
find %{buildroot}%{_includedir}/CL/ -not -name "cl_intel.h" -type f -print -delete

%check
#appstream-util validate-relax --nonet %%{buildroot}%%{_datadir}/metainfo/com.intel.beignet.metainfo.xml || :
:

%files
%license COPYING
%doc README.md
%{_libdir}/beignet/
%{_sysconfdir}/OpenCL/vendors/intel-beignet.icd
#%%{_datadir}/metainfo/com.intel.beignet.metainfo.xml

%files devel
%doc docs/*
%{_includedir}/CL/cl_intel.h

%changelog
* Thu Mar 12 2020 secureworkstation - 1.3.2.1-0.1.gitf3d6250
- Compile with clang-7.0
- Rebase to linnaea's branch: https://github.com/linnaea/beignet/

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3.2-4
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 13 2017 Tom Stellard <tstellar@redhat.com> - 1.3.2-2
- Rebuild for LLVM 5.0

* Wed Nov 01 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.2-1
- Update to 1.3.2

* Tue Oct 24 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.1-7
- Rebuild for LLVM 5.0

* Wed Oct 04 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.1-6
- Sync with 1.3 branch

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-5.git20170622.36f6a8b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-4.git20170622.36f6a8b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 14 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.3.1-3.git20170622.36f6a8b
- rebase to latest git, otherwise it is completely broken

* Tue Mar 21 2017 Tom Stellard <tstellar@redhat.com> - 1.3.1-2
- Fix build with LLVM 4.0

* Mon Mar 13 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.3.1-1
- Update to 1.3.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 22 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.3.0-3
- Update patch for OCL 2.0

* Sat Jan 21 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.3.0-2
- Enable OpenCL 2.0

* Fri Jan 20 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.3.0-1
- Update to 1.3.0 (RHBZ #1415148)

* Tue Nov 08 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.2.1-1
- Update to 1.2.1 (RHBZ #1392639)

* Thu Oct 27 2016 Dave Airlie <airlied@redhat.com> - 1.2.0-2
- rebase to llvm 3.9

* Tue Aug 30 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.2.0-1
- Update to 1.2.0 (RHBZ #1328527)
- Drop virtual Provides for ocl-icd

* Tue Jun 28 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.1.2-1
- Update to 1.1.2 (RHBZ #1328527)

* Fri Apr 08 2016 Björn Esser <fedora@besser82.io> - 1.1.1-5
- add virtual Provides for ocl-icd (RHBZ #1317603)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Nov 05 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.1.1-2
- Backport patch from upstream against "failed to release userptr" (RHBZ #1277925)

* Fri Oct 09 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1 (#1249611)

* Tue Oct 06 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.0-2
- Make beignet compiling and working with LLVM 3.7

* Mon Aug 03 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.1.0-1
- Update to 1.1.0 (RHBZ #1249611)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 19 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0.3-2
- Fix licensing issues with not compatipble LGPL code
- use python3-devel for fedora23+
- use license macro
- use make_build macro

* Fri May 08 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0.3-1
- Update to 1.0.3 (RHBZ #1202329)

* Mon Jan 19 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0.1-1
- 1.0.1 (RHBZ #1183497)

* Mon Nov 17 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.0.0-1
- 1.0.0 (RHBZ #1142892)

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 28 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.9.2-1
- 0.9.2 upstream release (RHBZ #1123941)

* Sun Jul 06 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.9.1-1
- 0.9.1 upstream release (RHBZ #1116622)

* Fri Jul 04 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.9.0-1
- Update ot 0.9.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 13 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.8-2
- Update LLVM/Terminfo patch from upstream maillist

* Wed Feb 12 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.8-1
- 0.8 upstream release

* Mon Jan 20 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.3-9.48f8e5b
- We need opencl-filesystem as requires

* Thu Jan 16 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.3-8.48f8e5b
- Latest master branch

* Wed Jan 15 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.3-7.984d680
- Fix libdir

* Wed Jan 15 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.3-6.984d680
- Update to latest master + apply patches from upstream list

* Tue Jan 14 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.3-5.e427b3e
- spec: trivial fix

* Mon Jan 13 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.3-4.e427b3e
- Build only on x86 arches, because only Intel GPUs supported here
- Fix license
- Update description

* Mon Jan 13 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.3-3.e427b3e
- Update to latest master

* Fri Jan 10 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.3-2.991e0d7
- Git from OpenCL-1.2 branch

* Fri Jan 10 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.3-1
- Initial package
