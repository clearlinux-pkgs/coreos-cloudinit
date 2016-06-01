Name     : coreos-cloudinit
Version  : 1.9.3
Release  : 2
URL      : https://github.com/coreos/coreos-cloudinit/archive/v1.9.3.tar.gz
Source0  : https://github.com/coreos/coreos-cloudinit/archive/v1.9.3.tar.gz
Summary  : No detailed summary available
Group    : Development/Tools
License  : Apache-2.0 BSD-2-Clause BSD-3-Clause GPL-3.0 LGPL-3.0 MIT

requires : coreos-cloudinit-bin

BuildRequires : go

%description
minimal support for parsing OVF environment

%package bin
Summary: bin components for the coreos-cloudinit package.
Group: Binaries

%description bin
bin components for the coreos-cloudinit package.

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

%check
export GOROOT="/usr/lib/golang"
export GOPATH="%{buildroot}/usr/lib/golang:$(pwd)"
go test -x -v ./

%files

%files bin
/usr/bin/coreos-cloudinit
