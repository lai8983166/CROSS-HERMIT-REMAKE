"""Freeze accepted world combat artifacts and recursively preserve originals."""
import argparse
import json
from tools.battle_world_combat_preservation import audit as previous_audit
from tools.battle_enemy_engagement_emulation import ROOT,need,sha

PARENT='analysis/battle-world-combat-acceptance-v1-20261025.json'
PARENT_SHA='1a701bb99ec94fdc0612e1e151c9e6d17e7c1153a948725b8ec8ae7a45c42b77'


def audit():
    previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted world combat evidence')
    frozen=[];updates=[]
    for r in json.loads(raw)['artifact_manifest']:
        data=(ROOT/r['path']).read_bytes()
        if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
            updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(data),reason='one original combat cycle through continuous world combats'))
        else:
            need(len(data)==r['bytes'] and sha(data)==r['sha256'],'frozen world combat evidence '+r['path']);frozen.append(r['path'])
    need(len(frozen)==52,'all 52 accepted world combat artifacts frozen')
    return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=len(frozen),frozen_artifacts=frozen,
                authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh enemy engagement preservation');out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n')
    print('52 frozen world combat artifacts and recursive originals preserved')
