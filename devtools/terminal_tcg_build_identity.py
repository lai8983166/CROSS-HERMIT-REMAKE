"""Authenticate pinned source objects, without claiming a reproducible binary build."""
import hashlib
import json
import subprocess
from pathlib import Path

PIN = 'e470268ff446ec56728215a987ed166d5ed8fb64'
TREE = 'f7f8eccd4e165c6c448946419cfbdb48f9e3db28'
FILES = ['VERSION', 'make-installers-all', 'configure', 'target/i386/cpu.h',
         'target/i386/gdbstub.c', 'target/i386/cpu-dump.c', 'target/i386/machine.c',
         'target/i386/tcg/translate.c', 'target/i386/tcg/fpu_helper.c',
         'target/i386/tcg/system/bpt_helper.c', 'accel/tcg/tcg-accel-ops.c',
         'target/i386/xsave_helper.c']


def object_id(kind, raw):
    return hashlib.sha1(kind.encode()+b' '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def inspect(repo):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(repo), *args], timeout=30)
    if git('rev-parse', 'FETCH_HEAD').decode().strip() != PIN:
        raise ValueError('unexpected source commit')
    commit = git('cat-file', 'commit', PIN)
    if object_id('commit', commit) != PIN or commit.splitlines()[0] != ('tree '+TREE).encode():
        raise ValueError('commit identity mismatch')
    rows = []
    for name in FILES:
        oid = git('rev-parse', PIN+':'+name).decode().strip()
        raw = git('cat-file', 'blob', oid)
        if object_id('blob', raw) != oid:
            raise ValueError('blob identity mismatch: '+name)
        rows.append(dict(path=name, git_blob=oid, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    return dict(schema='tcg-source-identity-v1', commit=PIN, tree=TREE,
                source_objects_verified=True, binary_build_reproduced=False,
                exact_build_provenance_complete=False, files=rows,
                gaps=['Publisher build recipe does not pin compiler or MSYS2 package versions.',
                      'No publisher per-build configure log, dependency lock or dirty-tree attestation.',
                      'Version string and source commit match; byte-identical rebuild has not been made.'],
                scope='Pinned source content authentication only, not binary-to-source equivalence or full-state acceptance.')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('repository', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    result = inspect(args.repository)
    with args.output.open('x', encoding='utf8') as stream:
        json.dump(result, stream, indent=2)
    print(json.dumps({k:v for k,v in result.items() if k!='files'}, indent=2))
