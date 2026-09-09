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
# Trim the python-bindings feature: drop the unused/unpackaged serde-pyobject
# crate and pyo3/generate-import-lib (a Windows-only pyo3 feature Fedora strips).
Patch:          drop-serde-pyobject.patch

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

# The "test" extra is the upstream benchmark/test suite (torch, numba, scipy,
# asv, pre-commit, ...); none of it is packaged here and %check only does an
# import check, so the extra is not built as a subpackage.


%prep
%autosetup -p1 -n outlines_core-%{version}
# Rust bindings: resolve crates against Fedora's packaged registry (offline).
%cargo_prep


%generate_buildrequires
# No extras: the "test" extra pulls heavy, unpackaged benchmark deps (asv,
# numba, torch, ...) and %check only imports the module.
%pyproject_buildrequires
# pyo3 is an *optional* crate, pulled in only by the "python-bindings" feature
# that [tool.maturin] builds with. Pass -f so its crate BuildRequires (and
# pyo3's own deps) are emitted and installed before maturin runs cargo metadata.
%cargo_generate_buildrequires -f python-bindings


%build
export RUSTFLAGS='%{build_rustflags}'
%pyproject_wheel


%install
%pyproject_install
# Automatically extracted from wheel
%pyproject_save_files -l outlines_core


%check
# The kernels.{mlx,numpy,torch} submodules are optional accelerator backends
# that import mlx / numba / torch respectively; those frameworks are only
# present when the user has installed that backend, so skip them in the
# build-time import check.
%pyproject_check_import -e 'outlines_core.kernels.*'


%files -n python3-outlines-core -f %{pyproject_files}


%changelog
%autochangelog
