"""Freeze accepted route evidence and recursively recheck original history."""
import argparse
import json
from tools.battle_route_admission_preservation import audit as previous_audit
from tools.battle_nearest_free_emulation import ROOT,need,sha
PARENT='analysis/battle-route-admission-acceptance-v1-20261024.json'
PARENT_SHA='9bafbbaa0d7e6357e2bbfceae03e6d26c6afef96049a664ad8268d47d6e3b638'


def audit():
    previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'accepted route manifest')
    frozen=[];updates=[]
    for row in json.loads(raw)['artifact_manifest']:
        data=(ROOT/row['path']).read_bytes()
        if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
            updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=sha(data),reason='original nearest-free and rerouting research evidence'))
        else:
            need(len(data)==row['bytes'] and sha(data)==row['sha256'],'unchanged route artifact '+row['path']);frozen.append(row['path'])
    need(len(frozen)==26,'all 26 frozen route artifacts')
    return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=26,frozen_artifacts=frozen,
                authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh preservation output');out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n')
    print('26 route artifacts and recursive original history preserved')
