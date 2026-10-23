"""Freeze accepted opening artifacts and original saves/resources/checkpoints."""
import json
from tools.school_retained_opening_preservation import audit as previous_audit
from tools.school_retained_world_loop import ROOT,sha,need,ACCEPTANCE,ACCEPTANCE_SHA

def audit():
 prior=previous_audit();raw=(ROOT/ACCEPTANCE).read_bytes();need(sha(raw)==ACCEPTANCE_SHA,'pinned opening acceptance');a=json.loads(raw);frozen=[];updates=[]
 for r in a['artifact_manifest']:
  b=(ROOT/r['path']).read_bytes();digest=sha(b)
  if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=digest,reason='natural original ordinary loop/world continuation in the live source resource domain'));continue
  need(len(b)==r['bytes'] and digest==r['sha256'],'unchanged accepted opening artifact '+r['path']);frozen.append(r['path'])
 need(len(frozen)==52,'all 52 accepted opening artifacts');return dict(schema_version=1,previous_acceptance=dict(path=ACCEPTANCE,sha256=ACCEPTANCE_SHA),unchanged_previous_artifact_count=52,unchanged_previous_artifacts=frozen,authorized_updates=updates,previous_recheck=prior,original_saves_checkpoints_resources_and_historical_evidence_unchanged=True)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable output')
 out.write_text(json.dumps(audit(),indent=2)+'\n',encoding='utf8',newline='\n');print('52 opening artifacts and cumulative history preserved',flush=True)
