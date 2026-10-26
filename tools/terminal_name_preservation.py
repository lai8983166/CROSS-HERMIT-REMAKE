"""Freeze the completed terminal fade unit and recursively preserve originals."""
import argparse,json
from tools.terminal_after_fade_preservation import audit as previous_audit
from tools.terminal_name_emulation import ROOT,need,sha,terminal
PARENT='analysis/terminal-after-fade-acceptance-v1-20261026.json'
PARENT_SHA='d74d2fc7d423319dc92f7dc2b5cb4c10ed8bad7dba10fccc35c9c0fba944065f'

def audit():
 previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted terminal fade unit')
 frozen=[];updates=[]
 for row in json.loads(raw)['artifact_manifest']:
  data=(ROOT/row['path']).read_bytes()
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=sha(data),reason='actual terminal name GDI and current texture unit'))
  else:
   need(len(data)==row['bytes'] and sha(data)==row['sha256'],'frozen terminal fade artifact '+row['path']);frozen.append(row['path'])
 return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=len(frozen),frozen_artifacts=frozen,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();r=audit();terminal.save(a.out,r);print(r['frozen_artifact_count'],'predecessor artifacts and recursive originals preserved')
