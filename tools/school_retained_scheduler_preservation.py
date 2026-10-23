"""Freeze accepted fog evidence and cumulative original save/resource/checkpoint history."""
import json
from tools.school_retained_fog_preservation import audit as previous_audit
from tools.school_retained_scheduler import ROOT,sha,need,ACCEPTANCE,ACCEPTANCE_SHA

def audit():
 prior=previous_audit();b=(ROOT/ACCEPTANCE).read_bytes();need(sha(b)==ACCEPTANCE_SHA,'accepted current fog identity');a=json.loads(b);frozen=[];updates=[]
 for row in a['artifact_manifest']:
  raw=(ROOT/row['path']).read_bytes();digest=sha(raw)
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=digest,reason='original retained task registration/current events and exact CRT thread creation dependency'));continue
  need(len(raw)==row['bytes'] and digest==row['sha256'],'unchanged accepted fog artifact '+row['path']);frozen.append(row['path'])
 need(len(frozen)==53,'all 53 accepted frozen fog artifacts');return dict(schema_version=1,previous_acceptance=dict(path=ACCEPTANCE,sha256=ACCEPTANCE_SHA),unchanged_previous_artifact_count=53,unchanged_previous_artifacts=frozen,authorized_updates=updates,previous_recheck=prior,original_saves_checkpoints_resources_and_historical_evidence_unchanged=True)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable preservation output')
 out.write_text(json.dumps(audit(),indent=2)+chr(10),encoding='utf8',newline=chr(10));print('53 fog artifacts and cumulative original history preserved',flush=True)
