"""Freeze accepted layer7 dialogue and recursively preserve original evidence."""
import argparse,json
from tools.terminal_panel_dialogue_preservation import audit as previous_audit
from tools.terminal_panel_dialogue_emulation import ROOT,need,sha,terminal

PARENT='analysis/terminal-panel-dialogue-acceptance-v1-20261027.json'
PARENT_SHA='ac1937ef900d1ebb2bae5d70ca60f6ea7ae0949e8fc093af867fb6fcea27beab'

def audit():
 previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted layer7 complete dialogue group')
 frozen=[];updates=[]
 for row in json.loads(raw)['artifact_manifest']:
  data=(ROOT/row['path']).read_bytes()
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=sha(data),reason='current terminal followup role and replacement dialogue group'))
  else:
   need(len(data)==row['bytes'] and sha(data)==row['sha256'],'frozen terminal panel dialogue artifact '+row['path']);frozen.append(row['path'])
 need(len(frozen)==65,'all65 accepted terminal panel dialogue artifacts')
 return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=65,frozen_artifacts=frozen,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();need(not(ROOT/a.out).exists(),'fresh immutable terminal followup preservation');terminal.save(a.out,audit());print('65 predecessor artifacts and recursive originals preserved')
