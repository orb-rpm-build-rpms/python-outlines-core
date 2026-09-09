Name:           python-outlines-core
Version:        0.2.14
Release:        %autorelease
# Fill in the actual package summary to submit package to Fedora
Summary:        Structured Text Generation in Rust

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        Apache-2.0
URL:            https://github.com/dottxt-ai/outlines-core
Source0:        %{pypi_source outlines_core}
# Vendored Rust dependencies. outlines-core pins pyo3 0.27, hf-hub 0.4.1 and
# tokenizers 0.22.2 -- all present in Fedora only at other versions. Rather than
# build each on a release branch, the whole crate graph is built offline from a
# vendor tarball. It is not shipped in a lookaside cache: rust-sources.sh
# regenerates it with `cargo vendor` at build time (see that script). Building
# against the real upstream pyo3 0.27 also means the manifest's serde-pyobject
# and pyo3/generate-import-lib both resolve, so no manifest patch is needed.
Source1:        outlines_core-%{version}-vendor.tar.xz

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
# -a1 unpacks the vendor tarball (Source1) into the source tree as ./vendor.
%autosetup -p1 -n outlines_core-%{version} -a1
# Build the Rust crate graph from the vendored sources, fully offline. This
# replaces the cargo buildrequires generator: no per-crate BuildRequires are
# needed because every dependency is supplied by ./vendor.
%cargo_prep -v vendor


%generate_buildrequires
# No extras: the "test" extra pulls heavy, unpackaged benchmark deps (asv,
# numba, torch, ...) and %check only imports the module. The Rust deps come from
# the vendor tree, so the cargo buildrequires generator is intentionally absent.
%pyproject_buildrequires


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
