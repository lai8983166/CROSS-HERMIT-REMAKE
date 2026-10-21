"""Read-only scheduler-unit audit extending all frozen R1/R2/task-frame evidence."""
import json
from tools.school_task_frame_preservation import audit as previous_audit
from tools.school_retained_render_preservation import sha_file,require
from tools.school_scheduler_lifetime_verification import ROOT

def audit():
 previous=previous_audit();parent='analysis/school-task-frame-acceptance-v1-20261021.json';report=json.loads((ROOT/parent).read_text(encoding='utf8'));unchanged=[];updates=[]
 for row in report['artifact_manifest']:
  path=ROOT/row['path'];actual=sha_file(path)
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=actual,reason='scheduler evidence LF rules or R3 scheduler prerequisite and remaining scene integration'));continue
  require(actual==row['sha256'] and path.stat().st_size==row['bytes'],'frozen task-frame artifact '+row['path']);unchanged.append(row['path'])
 return dict(schema_version=1,parent_task_frame_acceptance=dict(path=parent,sha256=sha_file(ROOT/parent)),previous_recheck=previous,unchanged_task_frame_artifact_count=len(unchanged),unchanged_task_frame_artifacts=unchanged,authorized_updates=updates,original_saves_checkpoints_historical_sources_and_reports_unchanged=True)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable audit output required')
 r=audit();out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf8',newline='\n');print('Preserved frozen task-frame artifacts',r['unchanged_task_frame_artifact_count'],'and all previous historical evidence, checkpoints and original saves')
