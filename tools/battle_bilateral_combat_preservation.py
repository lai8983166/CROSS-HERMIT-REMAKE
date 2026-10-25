"""Freeze accepted pursuit artifacts and recursively audit original data."""
import argparse
import json
from tools.battle_enemy_pursuit_preservation import audit as previous_audit
from tools.battle_bilateral_combat_emulation import ROOT,need,sha

PARENT='analysis/battle-enemy-pursuit-acceptance-v1-20261025.json'
PARENT_SHA='1c4429e8062a1659a41e7be22477292289c0c289afd8e1af38505f3c5141f4a8'


def audit():
    previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted original pursuit evidence')
    frozen=[];updates=[]
    for r in json.loads(raw)['artifact_manifest']:
        data=(ROOT/r['path']).read_bytes()
        if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
            updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(data),reason='original bilateral combat research'))
        else:
            need(len(data)==r['bytes'] and sha(data)==r['sha256'],'frozen pursuit '+r['path']);frozen.append(r['path'])
    need(len(frozen)==32,'all 32 pursuit artifacts frozen')
    return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=len(frozen),frozen_artifacts=frozen,
                authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh bilateral preservation');out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n')
    print('32 frozen pursuit artifacts and recursive originals preserved')
