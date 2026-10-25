"""Freeze accepted work waits and recursively recheck all original evidence."""
import argparse,json
from tools.terminal_work_preservation import audit as previous_audit
from tools.terminal_task_emulation import ROOT,need,sha,terminal

PARENT='analysis/terminal-work-acceptance-v1-20261025.json'
PARENT_SHA='bdf3b1674be00190bf580549664d5671692b0479be32fa70cf5c94b6ce5f32aa'


def audit():
 previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted original work wait audit')
 frozen=[];updates=[]
 for r in json.loads(raw)['artifact_manifest']:
  data=(ROOT/r['path']).read_bytes()
  if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(data),reason='actual original terminal task admission and pending resource boundary'))
  else:
   need(len(data)==r['bytes'] and sha(data)==r['sha256'],'frozen original work wait artifact '+r['path']);frozen.append(r['path'])
 need(len(frozen)==29,'all 29 original work wait predecessor artifacts')
 return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=29,frozen_artifacts=frozen,
  authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();terminal.save(a.out,audit());print('29 predecessor artifacts and recursive originals preserved')
