"""Extend frozen scheduler/task-frame/R1/R2/history/save/checkpoint preservation."""
import json,subprocess
from tools.school_scheduler_preservation import audit as previous_audit
from tools.school_retained_render_preservation import sha_file,require
from tools.school_scene_bootstrap_verification import ROOT,sha

def audit():
 previous=previous_audit();parent='analysis/school-scheduler-lifetime-acceptance-v1-20261021.json';expected=subprocess.check_output(['git','show','f5a28bc:'+parent],cwd=ROOT);require(sha_file(ROOT/parent)==sha(expected),'pinned scheduler acceptance itself');r=json.loads(expected);unchanged=[];updates=[]
 for row in r['artifact_manifest']:
  path=ROOT/row['path'];actual=sha_file(path)
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=actual,reason='scene bootstrap evidence LF rules or honest R3 prerequisite/remaining scene bridge'));continue
  require(actual==row['sha256'] and path.stat().st_size==row['bytes'],'frozen scheduler artifact '+row['path']);unchanged.append(row['path'])
 return dict(schema_version=1,parent_scheduler_acceptance=dict(path=parent,baseline_commit='f5a28bc',sha256=sha(expected)),previous_recheck=previous,unchanged_scheduler_artifacts=unchanged,unchanged_scheduler_artifact_count=len(unchanged),authorized_updates=updates,original_saves_checkpoints_historical_sources_and_reports_unchanged=True)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable preservation report required')
 r=audit();out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf8',newline='\n');print('Preserved frozen scheduler artifacts',r['unchanged_scheduler_artifact_count'],'and previous source/reports/checkpoints/original saves')
