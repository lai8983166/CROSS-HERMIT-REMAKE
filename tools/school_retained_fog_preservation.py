"""Freeze accepted ordinary-loop artifacts and cumulative original source history."""
import json
from tools.school_retained_world_loop_preservation import audit as previous_audit
from tools.school_retained_fog import ROOT,sha,need,ACCEPTANCE,ACCEPTANCE_SHA

def audit():
 prior=previous_audit();raw=(ROOT/ACCEPTANCE).read_bytes();need(sha(raw)==ACCEPTANCE_SHA,'accepted ordinary-loop frontier identity');accepted=json.loads(raw);frozen=[];updates=[]
 for row in accepted['artifact_manifest']:
  b=(ROOT/row['path']).read_bytes();digest=sha(b)
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=digest,reason='original current fog creation/upload and natural first pre-wait boundary'));continue
  need(len(b)==row['bytes'] and digest==row['sha256'],'unchanged accepted ordinary-loop artifact '+row['path']);frozen.append(row['path'])
 need(len(frozen)==52,'all 52 accepted original world-loop frozen artifacts');return dict(schema_version=1,previous_acceptance=dict(path=ACCEPTANCE,sha256=ACCEPTANCE_SHA),unchanged_previous_artifact_count=52,unchanged_previous_artifacts=frozen,authorized_updates=updates,previous_recheck=prior,original_saves_checkpoints_resources_and_historical_evidence_unchanged=True)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable preservation output')
 out.write_text(json.dumps(audit(),indent=2)+chr(10),encoding='utf8',newline=chr(10));print('52 world-loop artifacts and cumulative original history preserved',flush=True)
