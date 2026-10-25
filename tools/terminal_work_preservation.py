"""Freeze the accepted terminal route audit and recursively recheck originals."""
import argparse,json
from tools.terminal_route_preservation import audit as previous_audit
from tools.terminal_work_emulation import ROOT,need,sha,terminal

PARENT='analysis/terminal-routes-acceptance-v1-20261025.json'
PARENT_SHA='4718e09cf769fe22d98634162198e1f6914c77277454a543e57aef142c2fa6aa'


def audit():
 previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted terminal route audit')
 frozen=[];updates=[]
 for r in json.loads(raw)['artifact_manifest']:
  data=(ROOT/r['path']).read_bytes()
  if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(data),reason='actual original terminal work wait and pause contracts'))
  else:
   need(len(data)==r['bytes'] and sha(data)==r['sha256'],'frozen terminal route artifact '+r['path']);frozen.append(r['path'])
 need(len(frozen)==26,'all 26 terminal route predecessor artifacts')
 return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=26,frozen_artifacts=frozen,
  authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();terminal.save(a.out,audit());print('26 predecessor artifacts and recursive originals preserved')
