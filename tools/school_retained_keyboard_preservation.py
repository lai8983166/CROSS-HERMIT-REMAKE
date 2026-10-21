"""Freeze the accepted native input unit and the complete earlier integrity chain."""
import json
from tools.school_retained_keyboard import ROOT,PINS,pinned
from tools.school_native_dialogue_preservation import audit as previous_audit
from tools.school_retained_render_preservation import sha_file,require


def audit():
 previous=previous_audit();name='analysis/school-native-dialogue-acceptance-v1-20261022.json';acceptance=json.loads(pinned(name,PINS[name]));unchanged=[];updates=[]
 for row in acceptance['artifact_manifest']:
  p=ROOT/row['path'];actual=sha_file(p)
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=actual,reason='new offline retained keyboard evidence and honest master R3 outcome'));continue
  require(actual==row['sha256'] and p.stat().st_size==row['bytes'],'accepted native input artifact '+row['path']);unchanged.append(row['path'])
 return dict(schema_version=1,pinned_native_dialogue_acceptance=dict(path=name,sha256=PINS[name]),unchanged_native_input_artifact_count=len(unchanged),unchanged_native_input_artifacts=unchanged,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_historical_evidence_unchanged=True)


if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable preservation output required')
 result=audit();out.write_text(json.dumps(result,indent=2)+chr(10),encoding='utf8',newline=chr(10));print('preserved',result['unchanged_native_input_artifact_count'],'accepted native input artifacts and complete prior save/resource/evidence chain')
