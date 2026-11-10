#!/bin/bash
set -euo pipefail
root=/mnt/f/project/chaomofa
work="$root/.venv-audit/native-worker/tcg-build-v1"
export TMPDIR="$work/tmp" XDG_CACHE_HOME="$work/cache" PYTHONDONTWRITEBYTECODE=1
cd "$work/source"
git apply --check "$root/devtools/patches/terminal-tcg-selectors-v3.patch"
git apply "$root/devtools/patches/terminal-tcg-selectors-v3.patch"
cd "$work/build"
timeout 180 nice -n 10 ninja -j2 qemu-system-x86_64 > "$work/logs/build-v5.log" 2>&1
mkdir "$root/.venv-audit/native-worker/tcg-runtime-v3"
cp qemu-system-x86_64 "$root/.venv-audit/native-worker/tcg-runtime-v3/"
sha256sum "$root/.venv-audit/native-worker/tcg-runtime-v3/qemu-system-x86_64"
