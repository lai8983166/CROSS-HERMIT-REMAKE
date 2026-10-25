"""Freeze the complete live-terminal predecessor and recursively audit originals."""
import argparse,json
from tools.battle_live_terminal_preservation import audit as previous_audit
from tools.terminal_route_catalog import ROOT,PARENT,PARENT_SHA,need,sha


def audit():
 previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed live-terminal acceptance')
 frozen=[];updates=[]
 for r in json.loads(raw)['artifact_manifest']:
  data=(ROOT/r['path']).read_bytes()
  if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=sha(data),reason='terminal route source coverage and pending playback handoff'))
  else:
   need(len(data)==r['bytes'] and sha(data)==r['sha256'],'frozen live-terminal artifact '+r['path']);frozen.append(r['path'])
 need(len(frozen)==43,'all 43 live-terminal predecessor artifacts preserved')
 return dict(schema_version=1,previous_acceptance=dict(path=PARENT,sha256=PARENT_SHA),frozen_artifact_count=43,frozen_artifacts=frozen,
  authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True)


if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 need(not out.exists(),'fresh terminal route preservation output')
 out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n');print('43 predecessor artifacts and recursive originals preserved')
