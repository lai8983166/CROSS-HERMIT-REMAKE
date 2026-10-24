"""Freeze scheduler acceptance and recursively recheck original research history."""
import argparse
import json
from tools.school_retained_scheduler_preservation import audit as previous_audit
from tools.battle_pathfinding_emulation import ROOT, sha, need

PARENT = 'analysis/school-retained-scheduler-acceptance-v1-20261024.json'
PARENT_SHA = '8f08b27b921584b6a73f03e585754a575a51c46cd57a2c76916117df7b631a3e'


def audit():
    previous = previous_audit()
    raw = (ROOT/PARENT).read_bytes(); need(sha(raw) == PARENT_SHA, 'accepted original scheduler evidence identity')
    frozen, updates = [], []
    for row in json.loads(raw)['artifact_manifest']:
        data = (ROOT/row['path']).read_bytes()
        if row['path'] in ('.gitattributes', 'openspec/specs/reverse-engineering/completion/spec.md'):
            updates.append(dict(path=row['path'], previous_sha256=row['sha256'], current_sha256=sha(data), reason='isolated original pathfinding rule evidence'))
        else:
            need(len(data) == row['bytes'] and sha(data) == row['sha256'], 'unchanged accepted scheduler artifact '+row['path'])
            frozen.append(row['path'])
    need(len(frozen) == 59, 'all 59 frozen parent artifacts')
    return dict(schema_version=1, previous_acceptance=dict(path=PARENT, sha256=PARENT_SHA), frozen_artifact_count=len(frozen),
                frozen_artifacts=frozen, authorized_updates=updates, previous_recheck=previous,
                original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--out', required=True); a = p.parse_args()
    out = ROOT/a.out; need(not out.exists(), 'fresh immutable preservation report')
    out.write_text(json.dumps(audit(), indent=2)+'\n', encoding='utf8', newline='\n')
    print('59 parent artifacts and recursive original history preserved')
