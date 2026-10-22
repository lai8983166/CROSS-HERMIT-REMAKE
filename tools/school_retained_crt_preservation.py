"""Freeze the accepted portrait-file unit and complete historical evidence chain."""
import json
from tools import school_retained_crt as work
from tools.school_retained_portrait_file_preservation import audit as previous_audit

def audit():
 previous=previous_audit();a=json.loads(work.base.pinned(work.ACCEPTANCE,work.ACCEPTANCE_SHA));unchanged=[];updates=[]
 for row in a['artifact_manifest']:
  p=work.ROOT/row['path'];digest=work.sha(p.read_bytes())
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=digest,reason='new CRT dependency and separate original function fixture evidence, honest master status'));continue
  work.need(p.stat().st_size==row['bytes'] and digest==row['sha256'],'frozen accepted portrait-file artifact '+row['path']);unchanged.append(row['path'])
 work.need(len(unchanged)==30,'complete frozen previous unit')
 return dict(schema_version=1,pinned_previous_acceptance=dict(path=work.ACCEPTANCE,sha256=work.ACCEPTANCE_SHA),unchanged_previous_artifact_count=len(unchanged),unchanged_previous_artifacts=unchanged,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_historical_evidence_unchanged=True)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=work.ROOT/a.out
 if out.exists():p.error('fresh immutable preservation output required')
 r=audit();out.write_text(json.dumps(r,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('preserved 30 previous artifacts and entire historical/save/checkpoint/resource chain',flush=True)
