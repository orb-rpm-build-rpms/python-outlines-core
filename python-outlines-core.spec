Name:           python-outlines-core
Version:        0.2.14
Release:        %autorelease
# Fill in the actual package summary to submit package to Fedora
Summary:        Structured Text Generation in Rust

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        Apache-2.0
URL:            https://github.com/dottxt-ai/outlines-core
Source:         %{pypi_source outlines_core}

BuildRequires:  python3-devel
BuildRequires:  gcc
BuildRequires:  cargo-rpm-macros


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'outlines-core' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-outlines-core
Summary:        %{summary}

%description -n python3-outlines-core %_description

# For official Fedora packages, review which extras should be actually packaged
# See: https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#Extras
%pyproject_extras_subpkg -n python3-outlines-core test


%prep
%autosetup -p1 -n outlines_core-%{version}
# Rust bindings: resolve crates against Fedora's packaged registry (offline).
%cargo_prep


%generate_buildrequires
# Keep only those extras which you actually want to package or use during tests
%pyproject_buildrequires -x test
%cargo_generate_buildrequires


%build
export RUSTFLAGS='%{build_rustflags}'
%pyproject_wheel


%install
%pyproject_install
# Automatically extracted from wheel
%pyproject_save_files -l outlines_core


%check
%pyproject_check_import


%files -n python3-outlines-core -f %{pyproject_files}


%changelog
%autochangelog
