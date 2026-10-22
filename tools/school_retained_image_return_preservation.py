"""Protect accepted retained CRT construction and all prior original evidence."""
import json
from tools.school_retained_crt_image_preservation import audit as previous_audit
from tools.school_retained_image_return import ROOT,sha,need,ACCEPTANCE,ACCEPTANCE_SHA

def audit():
 prior=previous_audit();raw=(ROOT/ACCEPTANCE).read_bytes();need(sha(raw)==ACCEPTANCE_SHA,'accepted retained CRT/IMAGE construction');a=json.loads(raw);frozen=[];updates=[]
 for row in a['artifact_manifest']:
  p=ROOT/row['path'];digest=sha(p.read_bytes())
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=digest,reason='original retained IMAGE return and source container teardown evidence/master update'));continue
  need(p.stat().st_size==row['bytes'] and digest==row['sha256'],'unchanged retained CRT artifact '+row['path']);frozen.append(row['path'])
 need(len(frozen)==29,'all previously accepted retained CRT construction artifacts')
 return dict(schema_version=1,previous_acceptance=dict(path=ACCEPTANCE,sha256=ACCEPTANCE_SHA),unchanged_previous_artifact_count=29,unchanged_previous_artifacts=frozen,authorized_updates=updates,previous_recheck=prior,original_saves_checkpoints_resources_and_historical_evidence_unchanged=True)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable preservation output')
 out.write_text(json.dumps(audit(),indent=2)+chr(10),encoding='utf8',newline=chr(10));print('29 accepted retained CRT construction artifacts and complete historical/save chain preserved',flush=True)
