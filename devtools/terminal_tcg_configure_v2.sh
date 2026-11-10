#!/bin/bash
set -euo pipefail
root=/mnt/f/project/chaomofa
work="$root/.venv-audit/native-worker/tcg-build-v1"
export TMPDIR="$work/tmp" XDG_CACHE_HOME="$work/cache" PIP_CACHE_DIR="$work/cache/pip"
export PYTHONDONTWRITEBYTECODE=1
cd "$work/source"
git init
printf '%s\n' "$root/.venv-audit/native-worker/tcg-source-identity-v1/source.git/objects" > .git/objects/info/alternates
git config core.filemode false
git update-ref refs/heads/pinned e470268ff446ec56728215a987ed166d5ed8fb64
git symbolic-ref HEAD refs/heads/pinned
cp "$root/.venv-audit/native-worker/tcg-source-identity-v1/source.git/shallow" .git/shallow
git read-tree HEAD
cd "$work/build"
timeout 180 nice -n 10 ../source/configure --target-list=x86_64-softmmu \
    --without-default-features --enable-tcg --enable-system --enable-pixman \
    --disable-docs --disable-werror --disable-debug-info --disable-download \
    --disable-guest-agent --disable-tools > ../logs/configure-v2.log 2>&1
