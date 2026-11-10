#!/bin/bash
# Explicit F-backed WSL build; no package install or host configuration changes.
set -euo pipefail
root=/mnt/f/project/chaomofa
work="$root/.venv-audit/native-worker/tcg-build-v1"
repo="$root/.venv-audit/native-worker/tcg-source-identity-v1/source.git"
pin=e470268ff446ec56728215a987ed166d5ed8fb64
mkdir -p "$work"/{tmp,cache,source,build,logs}
export TMPDIR="$work/tmp" XDG_CACHE_HOME="$work/cache" PIP_CACHE_DIR="$work/cache/pip"
export PYTHONDONTWRITEBYTECODE=1
cd "$work"
if test -e source/configure; then
    echo 'Source already materialized; refusing implicit replacement' >&2
    exit 1
fi
git --git-dir="$repo" archive "$pin" | tar -x -C source
{
    uname -a
    gcc --version
    g++ --version
    ninja --version
    python3 --version
    pkg-config --modversion glib-2.0 pixman-1
    dpkg-query -W gcc g++ libc6-dev libglib2.0-dev libpixman-1-dev ninja-build python3
    sha256sum /usr/bin/gcc /usr/bin/g++ /usr/bin/ninja /usr/bin/python3
} > logs/toolchain.txt
cd build
timeout 180 nice -n 10 ../source/configure --target-list=x86_64-softmmu \
    --without-default-features --enable-tcg --enable-system --enable-pixman \
    --disable-docs --disable-werror --disable-debug-info --disable-download \
    --disable-guest-agent --disable-tools > ../logs/configure-v1.log 2>&1
