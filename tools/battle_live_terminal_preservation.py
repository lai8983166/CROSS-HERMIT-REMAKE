"""Freeze the accepted terminal-selection milestone and recursive originals."""
import argparse,json
from tools.battle_terminal_selection_preservation import audit as previous_audit
from tools.battle_live_terminal_emulation import ROOT,need,sha

PARENT='analysis/battle-terminal-selection-acceptance-v1-20261025.json'
PARENT_SHA='765d93d74769ae229b85d739c09e2653647f3ac0abe4fbc5db4c26c3afec4670'


def audit():
 previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted terminal-selection parent')
 frozen=[];updates=[]
 for r in json.loads(raw)['artifact_manifest']:
  b=(ROOT/r['path']).read_bytes()
  if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(b),reason='same-instance world clock and terminal event integration status'))
  else:
   need(len(b)==r['bytes'] and sha(b)==r['sha256'],'frozen terminal-selection artifact '+r['path']);frozen.append(r['path'])
 need(len(frozen)==34,'all 34 terminal-selection artifacts preserved')
 return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=34,frozen_artifacts=frozen,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out;need(not out.exists(),'fresh live preservation output')
 out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n');print('34 accepted terminal artifacts and recursive originals preserved')
