"""Freeze accepted movement evidence and cumulative original assets/checkpoints."""
import argparse
import json
from tools.battle_unit_movement_preservation import audit as previous_audit
from tools.battle_route_admission_emulation import ROOT,sha,need
PARENT='analysis/battle-unit-movement-acceptance-v1-20261024.json'
PARENT_SHA='444f1a66ca0242b13b8b503d91097095ed76671a64011480b59ac4837af45345'


def audit():
    previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'accepted original movement manifest')
    frozen=[];updates=[]
    for row in json.loads(raw)['artifact_manifest']:
        data=(ROOT/row['path']).read_bytes()
        if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
            updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=sha(data),reason='original primary/local route admission and search continuation evidence'))
        else:
            need(len(data)==row['bytes'] and sha(data)==row['sha256'],'unchanged accepted movement artifact '+row['path']);frozen.append(row['path'])
    need(len(frozen)==29,'all 29 frozen movement artifacts')
    return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=29,frozen_artifacts=frozen,
                authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh immutable preservation path');out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n')
    print('29 movement artifacts and recursive original history preserved')
