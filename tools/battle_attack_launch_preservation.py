"""Freeze target-acquisition acceptance and recursively recheck original history."""
import argparse
import json
from tools.battle_target_acquisition_preservation import audit as previous_audit
from tools.battle_attack_launch_emulation import ROOT,need,sha
PARENT='analysis/battle-target-acquisition-acceptance-v1-20261024.json'
PARENT_SHA='438e771c044d2a72933da302c45de2c6a36fc605ff82f0b94d77dfeceefa585b'


def audit():
    previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted target evidence')
    frozen=[];updates=[]
    for row in json.loads(raw)['artifact_manifest']:
        data=(ROOT/row['path']).read_bytes()
        if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
            updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=sha(data),reason='ordinary attack launch evidence'))
        else:
            need(len(data)==row['bytes'] and sha(data)==row['sha256'],'frozen target evidence '+row['path']);frozen.append(row['path'])
    need(len(frozen)==38,'all 38 target artifacts frozen')
    return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=len(frozen),
                frozen_artifacts=frozen,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh attack preservation');out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n');print('38 frozen target artifacts and recursive original history preserved')
