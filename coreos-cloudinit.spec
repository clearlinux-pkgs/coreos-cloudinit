Name     : coreos-cloudinit
Version  : 1.9.3
Release  : 3
URL      : https://github.com/coreos/coreos-cloudinit/archive/v1.9.3.tar.gz
Source0  : https://github.com/coreos/coreos-cloudinit/archive/v1.9.3.tar.gz
Summary  : No detailed summary available
Group    : Development/Tools
License  : Apache-2.0 BSD-2-Clause BSD-3-Clause GPL-3.0 LGPL-3.0 MIT

requires : coreos-cloudinit-bin
Requires : coreos-cloudinit-config

BuildRequires : go

%description
minimal support for parsing OVF environment

%package bin
Summary: bin components for the coreos-cloudinit package.
Group: Binaries
Requires: coreos-cloudinit-config

%description bin
bin components for the coreos-cloudinit package.

%package config
Summary: config components for the coreos-cloudinit package.
Group: Default

%description config
config components for the coreos-cloudinit package.

%prep
%setup -q

%build
export GOROOT="/usr/lib/golang"
export GOPATH="%{buildroot}/usr/lib/golang:$(pwd)"
cp -R Godeps/_workspace/src src
mkdir -p src/github.com/coreos
ln -s ../../../ src/github.com/coreos/coreos-cloudinit
go build -v -x ./...

%install
export GOROOT="/usr/lib/golang"
export GOPATH="%{buildroot}/usr/lib/golang:$(pwd)"
export GOBIN="%{buildroot}%{_bindir}"
mkdir -p "%{buildroot}%{_bindir}"
go install -x -v ./

mv %{buildroot}%{_bindir}/coreos-cloudinit-%{version} %{buildroot}%{_bindir}/coreos-cloudinit

# units
mkdir -p %{buildroot}/usr/lib/systemd/system
install -m0644 units/media-configdrive.mount \
		units/media-configvirtfs.mount \
		units/media-ovfenv.mount \
		units/system-cloudinit@.service \
		units/system-config.target \
		units/user-cloudinit-proc-cmdline.service \
		units/user-cloudinit@.path \
		units/user-cloudinit@.service \
		units/user-config-ovfenv.service \
		units/user-config.target \
		units/user-configdrive.service \
		units/user-configvirtfs.service \
	%{buildroot}/usr/lib/systemd/system/

mkdir -p %{buildroot}/usr/lib/udev/rules.d
install -m0644 units/90-ovfenv.rules \
	%{buildroot}/usr/lib/udev/rules.d/

mkdir -p %{buildroot}/usr/lib/systemd/system/default.target.wants
ln -sf ../system-config.target \
	%{buildroot}/usr/lib/systemd/system/default.target.wants/system-config.target
ln -sf ../user-config.target \
	%{buildroot}/usr/lib/systemd/system/default.target.wants/user-config.target

%check
export GOROOT="/usr/lib/golang"
export GOPATH="%{buildroot}/usr/lib/golang:$(pwd)"
go test -x -v ./

%files

%files bin
/usr/bin/coreos-cloudinit

%files config
/usr/lib/systemd/system/default.target.wants/system-config.target
/usr/lib/systemd/system/default.target.wants/user-config.target
/usr/lib/systemd/system/media-configdrive.mount
/usr/lib/systemd/system/media-configvirtfs.mount
/usr/lib/systemd/system/media-ovfenv.mount
/usr/lib/systemd/system/system-cloudinit@.service
/usr/lib/systemd/system/system-config.target
/usr/lib/systemd/system/user-cloudinit-proc-cmdline.service
/usr/lib/systemd/system/user-cloudinit@.path
/usr/lib/systemd/system/user-cloudinit@.service
/usr/lib/systemd/system/user-config-ovfenv.service
/usr/lib/systemd/system/user-config.target
/usr/lib/systemd/system/user-configdrive.service
/usr/lib/systemd/system/user-configvirtfs.service
/usr/lib/udev/rules.d/90-ovfenv.rules

