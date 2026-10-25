"""Rehash accepted lethal artifacts and recursively audit original resources."""
import argparse,json
from tools.battle_lethal_combat_preservation import audit as previous_audit
from tools.battle_terminal_selection_emulation import ROOT,PARENT,PARENT_SHA,need,sha


def audit():
 previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed lethal parent acceptance')
 frozen=[];updates=[]
 for r in json.loads(raw)['artifact_manifest']:
  b=(ROOT/r['path']).read_bytes()
  if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(b),reason='source-backed terminal scene selection research status'))
  else:
   need(len(b)==r['bytes'] and sha(b)==r['sha256'],'frozen lethal artifact '+r['path']);frozen.append(r['path'])
 need(len(frozen)==32,'all 32 accepted lethal artifacts frozen')
 return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=32,frozen_artifacts=frozen,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out;need(not out.exists(),'fresh terminal preservation')
 out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n');print('32 accepted lethal artifacts and recursive original resources preserved')
