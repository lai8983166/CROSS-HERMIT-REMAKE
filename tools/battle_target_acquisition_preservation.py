"""Freeze accepted region-routing evidence and recursive original history."""
import argparse
import json
from tools.battle_region_routing_preservation import audit as previous_audit
from tools.battle_target_acquisition_emulation import ROOT,need,sha
PARENT='analysis/battle-region-routing-acceptance-v1-20261024.json'
PARENT_SHA='fe78229f499bd7b6c0c0e9bf4f2110f1b4c73d5749c1a4f7b62c777e405ba59a'


def audit():
    previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'accepted region routing manifest')
    frozen=[];updates=[]
    for row in json.loads(raw)['artifact_manifest']:
        data=(ROOT/row['path']).read_bytes()
        if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
            updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=sha(data),reason='normal target selection and movement command handoff evidence'))
        else:
            need(len(data)==row['bytes'] and sha(data)==row['sha256'],'unchanged accepted region artifact '+row['path']);frozen.append(row['path'])
    need(len(frozen)==29,'all 29 frozen region artifacts')
    return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=29,frozen_artifacts=frozen,
                authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh preservation output');out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n');print('29 frozen region artifacts and recursive original history preserved')
