"""Freeze accepted rerouting evidence and recursively preserve original history."""
import argparse
import json
from tools.battle_nearest_free_preservation import audit as previous_audit
from tools.battle_region_routing_emulation import ROOT,need,sha
PARENT='analysis/battle-nearest-free-acceptance-v1-20261024.json'
PARENT_SHA='7145f01e6046ab85dc7a95dc3db5c741cd180836d9cae02ed8d0cc7b00d0956a'


def audit():
    previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'accepted rerouting manifest')
    frozen=[];updates=[]
    for row in json.loads(raw)['artifact_manifest']:
        data=(ROOT/row['path']).read_bytes()
        if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
            updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=sha(data),reason='original MAP05 region graph and complete AI main route evidence'))
        else:
            need(len(data)==row['bytes'] and sha(data)==row['sha256'],'unchanged accepted rerouting artifact '+row['path']);frozen.append(row['path'])
    need(len(frozen)==29,'all 29 frozen rerouting artifacts')
    return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=29,frozen_artifacts=frozen,
                authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh preservation output');out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n');print('29 frozen rerouting artifacts and original history preserved')
