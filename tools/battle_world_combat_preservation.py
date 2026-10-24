"""Freeze accepted world update artifacts and recursively preserve originals."""
import argparse
import json
from tools.battle_world_update_preservation import audit as previous_audit
from tools.battle_world_combat_emulation import ROOT,need,sha

PARENT='analysis/battle-world-update-acceptance-v1-20261024.json'
PARENT_SHA='99cd1fa421254158149d085d36fb6f27f69ac38007576307f904bdfa72377d7e'


def audit():
    previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted world scheduling evidence')
    frozen=[];updates=[]
    for r in json.loads(raw)['artifact_manifest']:
        data=(ROOT/r['path']).read_bytes()
        if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
            updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(data),reason='one original combat cycle through continuous world updates'))
        else:
            need(len(data)==r['bytes'] and sha(data)==r['sha256'],'frozen world update evidence '+r['path']);frozen.append(r['path'])
    need(len(frozen)==46,'all 46 accepted world update artifacts frozen')
    return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=len(frozen),frozen_artifacts=frozen,
                authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh world combat preservation');out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n')
    print('46 frozen world scheduling artifacts and recursive originals preserved')
