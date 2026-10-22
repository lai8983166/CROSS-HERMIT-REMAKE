"""Freeze accepted cold CRT origin and the complete original evidence/save chain."""
import json
from tools.school_crt_init_preservation import audit as previous_audit
from tools.school_retained_crt_image import ROOT,sha,need

ACCEPTANCE='analysis/school-crt-init-acceptance-v1-20261022.json'
ACCEPTANCE_SHA='0f09fdaacef49c70dad86697bd4647a3e793223f1cce8fccf310c75f2025399c'

def audit():
 prior=previous_audit();raw=(ROOT/ACCEPTANCE).read_bytes();need(sha(raw)==ACCEPTANCE_SHA,'accepted original CRT cold source and lifecycle');accepted=json.loads(raw);frozen=[];updates=[]
 for row in accepted['artifact_manifest']:
  p=ROOT/row['path'];digest=sha(p.read_bytes())
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=digest,reason='retained source CRT domain and continuous IMAGE evidence/master update'));continue
  need(p.stat().st_size==row['bytes'] and digest==row['sha256'],'unchanged accepted cold CRT artifact '+row['path']);frozen.append(row['path'])
 need(len(frozen)==76,'all accepted previous cold CRT artifacts')
 return dict(schema_version=1,previous_acceptance=dict(path=ACCEPTANCE,sha256=ACCEPTANCE_SHA),unchanged_previous_artifact_count=len(frozen),unchanged_previous_artifacts=frozen,authorized_updates=updates,previous_recheck=prior,original_saves_checkpoints_resources_and_historical_evidence_unchanged=True)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable preservation report')
 out.write_text(json.dumps(audit(),indent=2)+chr(10),encoding='utf8',newline=chr(10));print('76 accepted CRT artifacts and original save/checkpoint/resource chain preserved',flush=True)
