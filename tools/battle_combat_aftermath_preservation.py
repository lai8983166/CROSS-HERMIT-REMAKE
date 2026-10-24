"""Freeze the accepted hit/HP artifacts and recursively preserve originals."""
import argparse
import json
from tools.battle_hit_damage_preservation import audit as previous_audit
from tools.battle_combat_aftermath_emulation import ROOT,need,sha

PARENT='analysis/battle-hit-damage-acceptance-v1-20261024.json'
PARENT_SHA='636e768e23fe121de8f96765ae925a86f9754f6aafa12cd5717d8c4fef33e5ce'


def audit():
    previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted hit/HP evidence')
    frozen=[];updates=[]
    for r in json.loads(raw)['artifact_manifest']:
        data=(ROOT/r['path']).read_bytes()
        if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
            updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(data),reason='complete original unit follow-up, reactions and death evidence'))
        else:
            need(len(data)==r['bytes'] and sha(data)==r['sha256'],'frozen hit/HP evidence '+r['path']);frozen.append(r['path'])
    need(len(frozen)==37,'all 37 accepted hit/HP artifacts frozen')
    return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=len(frozen),frozen_artifacts=frozen,
                authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh combat aftermath preservation');out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n')
    print('37 frozen hit/HP artifacts and recursive original history preserved')
