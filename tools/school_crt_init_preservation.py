"""Protect the complete accepted CRT lifecycle and historical save/evidence chain."""
import json
from tools.school_crt_init_verification import ROOT,ACCEPTANCE,ACCEPTANCE_SHA,sha,need
from tools.school_retained_crt_preservation import audit as previous_audit

def audit():
 prior=previous_audit();raw=(ROOT/ACCEPTANCE).read_bytes();need(sha(raw)==ACCEPTANCE_SHA,'accepted prior CRT lifecycle');a=json.loads(raw);frozen=[];updates=[]
 for r in a['artifact_manifest']:
  p=ROOT/r['path'];digest=sha(p.read_bytes())
  if r['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):updates.append(dict(path=r['path'],previous_sha256=r['sha256'],current_sha256=digest,reason='native original cold CRT origin and source initialization evidence/master update'));continue
  need(p.stat().st_size==r['bytes'] and digest==r['sha256'],'unchanged prior accepted CRT artifact '+r['path']);frozen.append(r['path'])
 need(len(frozen)==40,'all prior lifecycle artifacts')
 return dict(schema_version=1,previous_acceptance=dict(path=ACCEPTANCE,sha256=ACCEPTANCE_SHA),unchanged_previous_artifact_count=40,unchanged_previous_artifacts=frozen,authorized_updates=updates,previous_recheck=prior,original_saves_checkpoints_resources_and_historical_evidence_unchanged=True)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable output')
 out.write_text(json.dumps(audit(),indent=2)+chr(10),encoding='utf8',newline=chr(10));print('40 previous CRT artifacts and complete historical/save/checkpoint/resource chain preserved',flush=True)
