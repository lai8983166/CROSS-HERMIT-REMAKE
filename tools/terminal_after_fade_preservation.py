"""Freeze current-overlay acceptance and recursively preserve original evidence."""
import argparse,json
from tools.terminal_overlay_preservation import audit as previous_audit
from tools.terminal_overlay_emulation import ROOT,need,sha,terminal
PARENT='analysis/terminal-overlay-acceptance-v1-20261026.json'
PARENT_SHA='d24b9e83354880c7e018858f0784da876c4b11bbb13bcfc5290f055697a447d9'

def audit():
 previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed current-overlay acceptance')
 frozen=[];updates=[]
 for row in json.loads(raw)['artifact_manifest']:
  data=(ROOT/row['path']).read_bytes()
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=sha(data),reason='actual original terminal tasks after fade wait'))
  else:
   need(len(data)==row['bytes'] and sha(data)==row['sha256'],'frozen overlay artifact '+row['path']);frozen.append(row['path'])
 need(len(frozen)==65,'all65 frozen predecessor artifacts')
 return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=len(frozen),frozen_artifacts=frozen,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();terminal.save(a.out,audit());print('65 predecessor artifacts and recursive originals preserved')
