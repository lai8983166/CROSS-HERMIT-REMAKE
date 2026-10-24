"""Freeze accepted attack launch evidence and recursive original resources."""
import argparse
import json
from tools.battle_attack_launch_preservation import audit as previous_audit
from tools.battle_attack_animation_emulation import ROOT,need,sha
PARENT='analysis/battle-attack-launch-acceptance-v1-20261024.json'
PARENT_SHA='df33f03bdb1df1af7094495f13337bc3e7d315e04994a0c5226de5aad18ba5e2'


def audit():
    previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted launch evidence')
    frozen=[];updates=[]
    for row in json.loads(raw)['artifact_manifest']:
        data=(ROOT/row['path']).read_bytes()
        if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
            updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=sha(data),reason='original active attack animation and effect event frontier evidence'))
        else:
            need(len(data)==row['bytes'] and sha(data)==row['sha256'],'frozen launch evidence '+row['path']);frozen.append(row['path'])
    need(len(frozen)==40,'all 40 launch artifacts frozen')
    return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=len(frozen),frozen_artifacts=frozen,
                authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh animation preservation');out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n');print('40 frozen launch artifacts and recursive original history preserved')
