"""Freeze accepted terminal confirmation and recursively preserve original evidence."""
import argparse,json
from tools.terminal_confirmation_preservation import audit as previous_audit
from tools.terminal_confirmation_emulation import ROOT,need,sha,terminal

PARENT='analysis/terminal-confirmation-acceptance-v1-20261026.json'
PARENT_SHA='3d2a114f3120d1eff89984dfa13cfd6a17ab7d8f513267026a9255f5f6754529'

def audit():
 previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted terminal confirmation handoff')
 frozen=[];updates=[]
 for r in json.loads(raw)['artifact_manifest']:
  data=(ROOT/r['path']).read_bytes()
  if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(data),reason='current terminal layer7 complete dialogue group and natural confirmation wait'))
  else:
   need(len(data)==r['bytes'] and sha(data)==r['sha256'],'frozen terminal confirmation artifact '+r['path']);frozen.append(r['path'])
 need(len(frozen)==42,'all42 accepted terminal confirmation predecessor artifacts')
 return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=42,frozen_artifacts=frozen,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();terminal.save(a.out,audit());print('42 predecessor artifacts and recursive originals preserved')
