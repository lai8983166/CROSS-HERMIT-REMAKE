"""Freeze accepted terminal portraits and recursively preserve original evidence."""
import argparse,json
from tools.terminal_portrait_preservation import audit as previous_audit
from tools.terminal_portrait_emulation import ROOT,need,sha,terminal

PARENT='analysis/terminal-portrait-acceptance-v1-20261026.json'
PARENT_SHA='d19e69c7b0bfe788ad8456d28ee8129d058e75b3caa0c9e16bbb937a37b80319'


def audit():
 previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted terminal portrait unit')
 frozen=[];updates=[]
 for r in json.loads(raw)['artifact_manifest']:
  data=(ROOT/r['path']).read_bytes()
  if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(data),reason='current terminal first dialogue and no-input confirmation wait'))
  else:
   need(len(data)==r['bytes'] and sha(data)==r['sha256'],'frozen terminal portrait artifact '+r['path']);frozen.append(r['path'])
 need(len(frozen)==46,'all46 terminal portrait predecessor artifacts')
 return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=46,frozen_artifacts=frozen,
  authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();terminal.save(a.out,audit());print('46 predecessor artifacts and recursive originals preserved')
