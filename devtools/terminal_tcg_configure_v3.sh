#!/bin/bash
set -euo pipefail
w=/mnt/f/project/chaomofa/.venv-audit/native-worker/tcg-build-v1
export TMPDIR="$w/tmp" XDG_CACHE_HOME="$w/cache" PIP_CACHE_DIR="$w/cache/pip" PYTHONDONTWRITEBYTECODE=1
cd "$w/source/subprojects"
git init keycodemapdb
timeout 45 git -C keycodemapdb fetch --depth=1 https://gitlab.com/qemu-project/keycodemapdb.git f5772a62ec52591ff6870b7e8ef32482371f22c6 > "$w/logs/keycodemap-fetch.log" 2>&1
git -C keycodemapdb checkout --detach FETCH_HEAD
cd "$w/build"
timeout 180 nice -n 10 ../source/configure --target-list=x86_64-softmmu \
 --without-default-features --enable-tcg --enable-system --enable-pixman \
 --disable-docs --disable-werror --disable-debug-info --disable-download \
 --disable-guest-agent --disable-tools > ../logs/configure-v3.log 2>&1
