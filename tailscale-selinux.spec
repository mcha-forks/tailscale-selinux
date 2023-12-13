%global selinuxtype targeted
%global modulename tailscaled

Name:           tailscale-selinux
Version:        0.0.2
Release:        2
Summary:        Tailscale SELinux policy
License:        BSD
URL:            https://github.com/mcha-forks/%{name}
BuildArch:      noarch

Source0:        %{modulename}.fc
Source1:        %{modulename}.if
Source2:        %{modulename}.te
Source3:        LICENSE

Requires:       selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}
BuildRequires:  selinux-policy-devel
%{?selinux_requires}

%description
Tailscale VPN SELinux policy.

%prep
mkdir -p %{name}-build
cp %{SOURCE3} .
cd %{name}-build
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} .

%build
make -f %{_datadir}/selinux/devel/Makefile %{modulename}.pp
bzip2 -9 %{modulename}.pp

%install
install -D -m 0644 %{modulename}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2

%pre
%selinux_relabel_pre -s %{selinuxtype}

%post
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.bz2

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{modulename}
fi

%posttrans
%selinux_relabel_post -s %{selinuxtype}

%files
%license LICENSE
%{_datadir}/selinux/packages/%{selinuxtype}/%{modulename}.pp.*
%ghost %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{modulename}

%changelog
%autochangelog
