"""Exact current build identity for bound native recovery; no process launch."""
from pathlib import Path
from devtools import terminal_display_native_v2 as native

ROOT=native.ROOT
BUILD=ROOT/'.venv-audit/terminal-display-owner-build-v6-20261114'
REPORT_SHA='53b3d744ea9e8ec9f6d11a8a68ef14b990d11edaa0df203b6b370c1873d0dafc'

def current_build():
    import json
    path=BUILD/'static-report.json';native.need(native.identity(path)['sha256']==REPORT_SHA,'fixed current strict-build report')
    r=json.loads(path.read_text('utf-8'))
    for key in ('generator','include','parent_generator','parent_include','generated_source','helper'):
        item=r[key];native.need(native.identity(ROOT/item['path'])==item,'unchanged actual build '+key)
    native.need((ROOT/r['generated_source']['path']).read_bytes()==native.source().encode(),'actual executable generated from current reviewed native extension')
    return r
