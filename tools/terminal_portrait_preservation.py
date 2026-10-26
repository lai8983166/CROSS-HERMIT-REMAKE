"""Freeze terminal name acceptance and recursively preserve originals and history."""
import argparse,json
from tools.terminal_name_preservation import audit as previous_audit
from tools.terminal_portrait_emulation import ROOT,need,sha,terminal
PARENT='analysis/terminal-name-acceptance-v1-20261026.json'
PARENT_SHA='2019425978432bffbc92dbed4cdadae65fa025496d8129e00e0766e69820e0fe'
def audit():
 previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted terminal name unit');frozen=[];updates=[]
 for row in json.loads(raw)['artifact_manifest']:
  data=(ROOT/row['path']).read_bytes()
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=sha(data),reason='current terminal portraits and role readiness'))
  else:need(len(data)==row['bytes'] and sha(data)==row['sha256'],'frozen terminal name artifact '+row['path']);frozen.append(row['path'])
 return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=len(frozen),frozen_artifacts=frozen,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();r=audit();terminal.save(a.out,r);print(r['frozen_artifact_count'],'predecessor artifacts and recursive originals preserved')
