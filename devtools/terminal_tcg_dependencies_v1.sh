#!/bin/bash
set -euo pipefail
w=/mnt/f/project/chaomofa/.venv-audit/native-worker/tcg-build-v1
export TMPDIR="$w/tmp" XDG_CACHE_HOME="$w/cache" PIP_CACHE_DIR="$w/cache/pip" PYTHONDONTWRITEBYTECODE=1
cd "$w/source/subprojects"
for pair in berkeley-softfloat-3:b64af41c3276f97f0e181920400ee056b9c88037 berkeley-testfloat-3:e7af9751d9f9fd3b47911f51a5cfd08af256a9ab; do
    name=${pair%%:*}
    revision=${pair#*:}
    git init "$name"
    timeout 60 git -C "$name" fetch --depth=1 "https://gitlab.com/qemu-project/$name.git" "$revision" > "$w/logs/$name-fetch.log" 2>&1
    git -C "$name" checkout --detach FETCH_HEAD
    cp -r "packagefiles/$name/." "$name/"
done
