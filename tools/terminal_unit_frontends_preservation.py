"""Check the fixed predecessor and recursive inventory after explicit retirement."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PARENT='analysis/terminal-battle-exit-prefix-acceptance-v1-20261102.json'
PARENT_SHA='c4471be997485202327f99be3ad22655b5f9da5968b88d1e214377f1edaae106'
RETENTION='analysis/terminal-battle-exit-prefix-retention-result-v1-20261103.json'
RETENTION_SHA='93b0dae836c708460daacc4f537c529ff86d3deaf10deb69fa2f2e11f68802c9'
MAX_FRESH_HASH=50*1024*1024
ROLLING={'.gitattributes','analysis/.gitignore','openspec/specs/reverse-engineering/completion/spec.md'}


def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()


def references(value):
    if isinstance(value,dict):
        if (isinstance(value.get('path'),str) and type(value.get('bytes')) is int
                and isinstance(value.get('sha256'),str) and len(value['sha256'])==64):
            yield {k:value[k] for k in ('path','bytes','sha256')}
        for child in value.values():yield from references(child)
    elif isinstance(value,list):
        for child in value:yield from references(child)


def audit():
    parent_path=ROOT/PARENT
    if sha(parent_path)!=PARENT_SHA:raise ValueError('fixed accepted parent changed')
    if sha(ROOT/RETENTION)!=RETENTION_SHA:raise ValueError('fixed authorized retirement ledger changed')
    parent=json.loads(parent_path.read_bytes())
    previous=json.loads((ROOT/parent['preservation']['path']).read_bytes())
    retirement=json.loads((ROOT/RETENTION).read_bytes())
    retired={Path(r['path']).resolve():r for r in retirement['deleted_files']}
    for path in retired:
        if path.exists():raise ValueError('previously retired path unexpectedly present '+str(path))
    expected={}
    superseded=[]
    for row in references([parent['artifact_manifest'],previous,parent['source_report']]):
        path=(ROOT/row['path']).resolve()
        if path in expected and expected[path]!=row:
            relative=path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
            if relative not in ROLLING:raise ValueError('conflicting frozen identities '+relative)
            superseded.append(row)
        else:expected[path]=row
    checked=[];large=[];rolling=[];retired_refs=[]
    for path,row in sorted(expected.items(),key=lambda item:str(item[0])):
        if path in retired:
            old=retired[path]
            if (row['bytes'],row['sha256'])!=(old['bytes'],old['sha256']):
                raise ValueError('retirement identity does not match old inventory '+str(path))
            retired_refs.append(row)
            continue
        relative=path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)
        if relative in ROLLING:
            rolling.append(dict(path=relative,previous=row,current_bytes=path.stat().st_size,
                                current_sha256=sha(path),reason='current change additions to rolling inventory'))
            continue
        if not path.is_file() or path.stat().st_size!=row['bytes']:
            raise ValueError('missing or wrong-size frozen predecessor '+str(path))
        if row['bytes']>MAX_FRESH_HASH:
            large.append(dict(**row,current_size_checked=True,current_SHA_freshly_rehashed=False,
                              SHA_identity_basis='immutable accepted predecessor inventory'))
        else:
            if sha(path)!=row['sha256']:raise ValueError('frozen predecessor SHA differs '+str(path))
            checked.append(row)
    retained=[]
    source=retirement['retained_full_source']
    for location in (source['path'],source['backup_path']):
        path=Path(location)
        if not path.is_absolute():path=ROOT/path
        if not path.is_file() or path.stat().st_size!=source['bytes_each']:
            raise ValueError('accepted retained parent source/copy missing '+str(path))
        retained.append(dict(path=str(path),bytes=source['bytes_each'],prior_full_SHA256=source['sha256'],
                             current_size_checked=True,current_SHA_freshly_rehashed=False))
    return dict(schema_version=1,accepted_parent=dict(path=PARENT,bytes=parent_path.stat().st_size,
        sha256=PARENT_SHA),small_frozen_full_SHA_count=len(checked),small_frozen_full_SHA=checked,
        large_frozen_size_only=large,large_fresh_hash_threshold_bytes=MAX_FRESH_HASH,
        retired_inventory_references=retired_refs,retirement_ledger=dict(path=RETENTION,sha256=sha(ROOT/RETENTION)),
        retired_paths_confirmed_absent=len(retired),retained_parent_source_and_copy=retained,
        authorized_rolling_updates=rolling,older_rolling_identities=superseded,
        historical_acceptances_rewritten=False,new_native_proof_executed_by_this_audit=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True)
    args=parser.parse_args()
    result=audit()
    with (ROOT/args.out).open('x',encoding='utf8',newline='\n') as f:
        json.dump(result,f,separators=(',',':'));f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if not isinstance(v,list)}))
