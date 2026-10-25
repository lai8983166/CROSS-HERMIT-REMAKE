"""Freeze terminal VM-entry acceptance and recursively protect original evidence."""
import argparse,json
from tools.terminal_task_preservation import audit as previous_audit
from tools.terminal_task_emulation import ROOT,need,sha,terminal
PARENT='analysis/terminal-task-acceptance-v1-20261026.json'
PARENT_SHA='b8a5abc9594c1f2f33cdb14856a74d958f94a19fa6053be907d50e5655c01521'

def audit():
 previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted terminal task entry')
 frozen=[];updates=[]
 for r in json.loads(raw)['artifact_manifest']:
  data=(ROOT/r['path']).read_bytes()
  if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(data),reason='actual current overlay resource and terminal VM continuation'))
  else:
   need(len(data)==r['bytes'] and sha(data)==r['sha256'],'frozen terminal task artifact '+r['path']);frozen.append(r['path'])
 return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=len(frozen),frozen_artifacts=frozen,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();r=audit();terminal.save(a.out,r);print(r['frozen_artifact_count'],'predecessor artifacts and recursive originals preserved')
