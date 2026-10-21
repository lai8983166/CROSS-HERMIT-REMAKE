"""Preserve frozen native scene evidence as well as the full integrity chain."""
import json,subprocess
from tools.school_native_scene_preservation import audit as previous_audit
from tools.school_native_scene import ROOT,sha
from tools.school_retained_render_preservation import sha_file,require

def audit():
 previous=previous_audit();name='analysis/school-native-scene-acceptance-v1-20261021.json';blob=subprocess.check_output(['git','show','5b7df94:'+name],cwd=ROOT);require(sha_file(ROOT/name)==sha(blob),'pinned native scene acceptance');unchanged=[];updates=[]
 for row in json.loads(blob)['artifact_manifest']:
  p=ROOT/row['path'];actual=sha_file(p)
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=actual,reason='dialogue evidence rules and honest R3 native input outcome'));continue
  require(actual==row['sha256'] and p.stat().st_size==row['bytes'],'frozen native scene artifact '+row['path']);unchanged.append(row['path'])
 parent_pin=dict(path=name,commit='5b7df94',sha256=sha(blob));dialogue={};pins=[]
 for commit,name in (('d8bbfc4','analysis/school-native-dialogue-progress-v1-20261021.json'),('aabd319','analysis/school-native-dialogue-progress-v2-20261022.json')):
  blob=subprocess.check_output(['git','show',commit+':'+name],cwd=ROOT);require((ROOT/name).read_bytes()==blob,'pinned dialogue progress '+name);pins.append(dict(path=name,commit=commit,sha256=sha(blob)))
  for row in json.loads(blob)['artifact_manifest']:
   if row['path'].startswith('analysis/'):
    p=ROOT/row['path'];require(sha_file(p)==row['sha256'] and p.stat().st_size==row['bytes'],'frozen dialogue evidence '+row['path']);dialogue[row['path']]=row['sha256']
 return dict(schema_version=1,parent_native_scene_acceptance=parent_pin,unchanged_native_scene_artifacts=unchanged,unchanged_native_scene_artifact_count=len(unchanged),pinned_dialogue_progress=pins,unchanged_dialogue_evidence=dialogue,unchanged_dialogue_evidence_count=len(dialogue),authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_historical_sources_and_reports_unchanged=True)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable preservation output required')
 r=audit();out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf8',newline='\n');print('preserved',r['unchanged_native_scene_artifact_count'],'native artifacts and prior full history/save/runtime inventory')
