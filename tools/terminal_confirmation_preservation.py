"""Freeze accepted terminal dialogue and recursively preserve original evidence."""
import argparse,json
from tools.terminal_dialogue_preservation import audit as previous_audit
from tools.terminal_dialogue_emulation import ROOT,need,sha,terminal

PARENT='analysis/terminal-dialogue-acceptance-v1-20261026.json'
PARENT_SHA='060848fe60cd0c8c110d8f6124404c9f2c4b48ad1aa5fc858553bbe892c52db6'

def audit():
 previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted terminal first dialogue')
 frozen=[];updates=[]
 for r in json.loads(raw)['artifact_manifest']:
  data=(ROOT/r['path']).read_bytes()
  if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(data),reason='current terminal captured confirmation and next-font handoff'))
  else:
   need(len(data)==r['bytes'] and sha(data)==r['sha256'],'frozen terminal dialogue artifact '+r['path']);frozen.append(r['path'])
 need(len(frozen)==52,'all52 accepted terminal dialogue predecessor artifacts')
 return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=52,frozen_artifacts=frozen,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();terminal.save(a.out,audit());print('52 predecessor artifacts and recursive originals preserved')
