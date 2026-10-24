"""Freeze 47 accepted combat follow-up artifacts and recursively recheck originals."""
import argparse
import json
from tools.battle_combat_aftermath_preservation import audit as previous_audit
from tools.battle_world_update_emulation import ROOT,need,sha

PARENT='analysis/battle-combat-aftermath-acceptance-v1-20261024.json'
PARENT_SHA='c8b4894365e088ccc37218315f527422ed4760b555619a277db95ff8937c211f'


def audit():
    previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted full unit evidence')
    frozen=[];updates=[]
    for r in json.loads(raw)['artifact_manifest']:
        data=(ROOT/r['path']).read_bytes()
        if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
            updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(data),reason='complete finite original world update evidence'))
        else:
            need(len(data)==r['bytes'] and sha(data)==r['sha256'],'frozen full unit evidence '+r['path']);frozen.append(r['path'])
    need(len(frozen)==47,'all 47 accepted full unit artifacts frozen')
    return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=len(frozen),frozen_artifacts=frozen,
                authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh world preservation');out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n')
    print('47 frozen full unit artifacts and recursive original history preserved')
