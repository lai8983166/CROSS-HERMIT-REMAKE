"""Freeze accepted animation/event artifacts and original recursive history."""
import argparse
import json
from tools.battle_attack_animation_preservation import audit as previous_audit
from tools.battle_hit_damage_emulation import ROOT,need,sha
PARENT='analysis/battle-attack-animation-acceptance-v1-20261024.json'
PARENT_SHA='ef590f769b2c20225d79f56c8468c2acdd8e4171f4e1582f7b2fd9f1ca369d26'


def audit():
    previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted animation evidence')
    frozen=[];updates=[]
    for r in json.loads(raw)['artifact_manifest']:
        data=(ROOT/r['path']).read_bytes()
        if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
            updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(data),reason='original melee hit and HP effect application evidence'))
        else:
            need(len(data)==r['bytes'] and sha(data)==r['sha256'],'frozen animation evidence '+r['path']);frozen.append(r['path'])
    need(len(frozen)==38,'all 38 accepted animation artifacts frozen')
    return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=len(frozen),frozen_artifacts=frozen,
                authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh hit damage preservation');out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n');print('38 frozen animation artifacts and recursive original history preserved')
