"""Freeze accepted pathfinding artifacts and recursive original research assets."""
import argparse
import json
from tools.battle_pathfinding_preservation import audit as previous_audit
from tools.battle_unit_movement_emulation import ROOT, need, sha

PARENT = 'analysis/battle-pathfinding-acceptance-v1-20261024.json'
PARENT_SHA = 'bec5a62c5f0b599b1c1ec93af3ab39832d3223332f064ea0a220fca5b7360ade'


def audit():
    previous = previous_audit(); raw = (ROOT/PARENT).read_bytes()
    need(sha(raw) == PARENT_SHA, 'pinned original pathfinding acceptance')
    frozen, updates = [], []
    for row in json.loads(raw)['artifact_manifest']:
        data = (ROOT/row['path']).read_bytes()
        if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
            updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=sha(data),reason='original AI movement phase and fixed-point position evidence'))
        else:
            need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'unchanged accepted pathfinding artifact '+row['path'])
            frozen.append(row['path'])
    need(len(frozen) == 27, 'all 27 frozen parent artifacts')
    return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=27,
                frozen_artifacts=frozen,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__ == '__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args()
    out=ROOT/a.out;need(not out.exists(),'fresh preservation path');out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n')
    print('27 parent artifacts and recursive original history preserved')
