"""Extend the frozen R2 integrity audit without changing its implementation."""
import json
from tools.school_retained_render_preservation import audit as historical_audit,sha_file,require
from tools.school_task_frame import ROOT

def audit():
 historical=historical_audit();parent='analysis/school-retained-render-acceptance-v1-20261021.json';p=json.loads((ROOT/parent).read_text(encoding='utf8'))
 updates=[];unchanged=[]
 for row in p['artifact_manifest']:
  path=ROOT/row['path'];actual=sha_file(path)
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=actual,reason='R3 task-frame evidence attributes or roadmap/corrected pending-request interpretation'));continue
  require(actual==row['sha256'] and path.stat().st_size==row['bytes'],'R2 frozen artifact '+row['path']);unchanged.append(row['path'])
 return dict(schema_version=1,parent_R2_acceptance=dict(path=parent,sha256=sha_file(ROOT/parent)),historical_recheck=historical,unchanged_R2_artifact_count=len(unchanged),unchanged_R2_artifacts=unchanged,authorized_updates=updates,R2_sources_native_helpers_reports_and_images_unchanged=True)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable preservation path required')
 result=audit();out.write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n');print('Historical raw files',result['historical_recheck']['historical_raw_files'],'; frozen R2 artifacts',result['unchanged_R2_artifact_count'],'; original saves/private checkpoints unchanged')
