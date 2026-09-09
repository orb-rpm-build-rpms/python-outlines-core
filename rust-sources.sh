#!/bin/sh
# rust-sources.sh - assemble the Rust "vendor" tarball for an offline build.
#
# rpm-build-assist runs every *sources.sh in the checked-out package directory
# after spectool has downloaded the online sources (here the PyPI sdist). This
# project has no lookaside cache, so rather than have a maintainer run
# `cargo vendor` by hand and upload the result, we regenerate the vendor
# tarball on demand at build time.
#
# It extracts the upstream sdist, runs `cargo vendor` against the Cargo.lock the
# sdist ships, and packs the result as <crate>-<version>-vendor.tar.xz. That is
# the Source1 the spec unpacks; `%cargo_prep -v vendor` then builds the whole
# crate graph from it with `[net] offline = true`, so no dependency crate has to
# be packaged for Fedora separately.
set -eu

# The PyPI sdist spectool just fetched, e.g. "llguidance-1.7.6.tar.gz". Exclude
# a previously generated "*-vendor.tar.*" so re-runs don't pick it as the sdist.
sdist=$(ls -1 ./*.tar.gz 2>/dev/null | grep -v -- '-vendor\.tar\.' | head -n1)
[ -n "$sdist" ] || { echo "rust-sources.sh: no sdist tarball found" >&2; exit 1; }

# "llguidance-1.7.6.tar.gz" -> "llguidance-1.7.6": the dir the sdist unpacks to
# and the stem for the vendor tarball name the spec's Source1 expects.
stem=$(basename "$sdist" .tar.gz)
vendor_tarball="${stem}-vendor.tar.xz"

# Idempotent: nothing to do if a previous run already produced the tarball.
[ -e "$vendor_tarball" ] && { echo "rust-sources.sh: $vendor_tarball already present"; exit 0; }

# Work under the checkout dir (mounted, ample space) rather than /tmp; the
# vendor tree is large (hundreds of MB uncompressed).
workdir=$(mktemp -d "$PWD/.rust-vendor.XXXXXX")
trap 'rm -rf "$workdir"' EXIT

tar xzf "$sdist" -C "$workdir"
# cargo vendor must run from inside the crate (needs its Cargo.toml/Cargo.lock).
# --locked pins the exact versions the sdist shipped, keeping builds reproducible.
( cd "$workdir/$stem" && cargo vendor --locked "$workdir/vendor" >/dev/null )

# Pack vendor/ at the archive root; %prep unpacks it into the source dir and
# %cargo_prep -v vendor points cargo at ./vendor.
tar -C "$workdir" -cf - vendor | xz -T0 -3 > "$vendor_tarball"
echo "rust-sources.sh: wrote $vendor_tarball"
