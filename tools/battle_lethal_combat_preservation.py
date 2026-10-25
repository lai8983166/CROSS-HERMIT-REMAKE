"""Freeze the accepted bilateral milestone and recursively audit originals."""
import argparse,json
from tools.battle_bilateral_combat_preservation import audit as previous_audit
from tools.battle_lethal_combat_emulation import ROOT,need,sha

PARENT='analysis/battle-bilateral-combat-acceptance-v1-20261025.json'
PARENT_SHA='075c385c3827a91cefc7d3f3d9a428dcc9dffbac62145e1ea594df785f0ccd9a'


def audit():
    previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed bilateral acceptance')
    frozen=[];updates=[]
    for r in json.loads(raw)['artifact_manifest']:
        b=(ROOT/r['path']).read_bytes()
        if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
            updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(b),reason='autonomous lethal combat and real result-input research'))
        else:
            need(len(b)==r['bytes'] and sha(b)==r['sha256'],'frozen bilateral artifact '+r['path']);frozen.append(r['path'])
    need(len(frozen)==51,'all 51 bilateral artifacts frozen')
    return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=51,frozen_artifacts=frozen,authorized_updates=updates,
        previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out;need(not out.exists(),'fresh lethal preservation')
    out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n');print('51 bilateral artifacts and recursive originals preserved')
