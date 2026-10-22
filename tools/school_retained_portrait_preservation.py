"""Freeze the entire accepted retained-keyboard unit plus all older evidence."""
import json
from tools.school_retained_portrait import ROOT,ACCEPTANCE,ACCEPTANCE_SHA
from tools.school_retained_keyboard import pinned
from tools.school_retained_keyboard_preservation import audit as previous_audit
from tools.school_retained_render_preservation import sha_file,require


def audit():
 previous=previous_audit();r=json.loads(pinned(ACCEPTANCE,ACCEPTANCE_SHA));unchanged=[];updates=[]
 for row in r['artifact_manifest']:
  p=ROOT/row['path'];actual=sha_file(p)
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=actual,reason='new portrait catalog evidence and honest master completion boundary'));continue
  require(actual==row['sha256'] and p.stat().st_size==row['bytes'],'frozen retained keyboard artifact '+row['path']);unchanged.append(row['path'])
 return dict(schema_version=1,pinned_retained_keyboard_acceptance=dict(path=ACCEPTANCE,sha256=ACCEPTANCE_SHA),unchanged_retained_keyboard_artifact_count=len(unchanged),unchanged_retained_keyboard_artifacts=unchanged,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_historical_evidence_unchanged=True)


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable preservation output required')
 r=audit();out.write_text(json.dumps(r,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('preserved',r['unchanged_retained_keyboard_artifact_count'],'retained keyboard artifacts and full earlier source/save/runtime chain')
