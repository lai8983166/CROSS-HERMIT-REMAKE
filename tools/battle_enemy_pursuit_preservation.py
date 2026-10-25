"""Freeze accepted enemy engagements and recursively preserve original data."""
import argparse,json
from tools.battle_enemy_engagement_preservation import audit as previous_audit
from tools.battle_enemy_pursuit_emulation import ROOT,need,sha

PARENT='analysis/battle-enemy-engagement-acceptance-v1-20261025.json'
PARENT_SHA='667e598b154f02b1351f1ff3a4258c4cbc743e1a0e5ff3957a0719c83a6218cd'


def audit():
    previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted enemy engagement evidence')
    frozen=[];updates=[]
    for r in json.loads(raw)['artifact_manifest']:
        data=(ROOT/r['path']).read_bytes()
        if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
            updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(data),reason='world-driven enemy pursuit integration'))
        else:
            need(len(data)==r['bytes'] and sha(data)==r['sha256'],'frozen enemy engagement '+r['path']);frozen.append(r['path'])
    need(len(frozen)==35,'all 35 accepted enemy engagement artifacts frozen')
    return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=len(frozen),frozen_artifacts=frozen,
                authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh pursuit preservation');out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n')
    print('35 frozen enemy engagement artifacts and recursive originals preserved')
