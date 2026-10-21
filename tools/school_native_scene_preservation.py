"""Freeze prior native/bootstrap evidence and verify the complete runtime assets."""
import gzip,json,subprocess
from tools.school_scene_bootstrap_preservation import audit as previous_audit
from tools.school_retained_render_preservation import sha_file,require
from tools.school_native_scene import ROOT,runtime_audit,sha

def audit():
 previous=previous_audit();parent='analysis/school-scene-bootstrap-acceptance-v1-20261021.json';expected=subprocess.check_output(['git','show','6f10e22:'+parent],cwd=ROOT);require(sha_file(ROOT/parent)==sha(expected),'frozen bootstrap acceptance itself');r=json.loads(expected);unchanged=[];updates=[]
 for row in r['artifact_manifest']:
  path=ROOT/row['path'];actual=sha_file(path)
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=actual,reason='native scene evidence LF rules or native MAIN/CRT/script/world results and remaining input/retained boundaries'));continue
  require(actual==row['sha256'] and path.stat().st_size==row['bytes'],'frozen bootstrap artifact '+row['path']);unchanged.append(row['path'])
 runtime_path='analysis/school-native-scene-runtime-v1-20261021.json.gz';baseline=subprocess.check_output(['git','show','07dfb8f:'+runtime_path],cwd=ROOT);require(sha_file(ROOT/runtime_path)==sha(baseline),'pinned private runtime inventory');before=json.loads(gzip.decompress(baseline));after=runtime_audit();require(before['immutable_files']==after['immutable_files'] and before['immutable_bytes']==after['immutable_bytes'],'all original/private immutable asset bytes retained')
 return dict(schema_version=1,parent_bootstrap_acceptance=dict(path=parent,baseline_commit='6f10e22',sha256=sha(expected)),previous_recheck=previous,unchanged_bootstrap_artifacts=unchanged,unchanged_bootstrap_artifact_count=len(unchanged),authorized_updates=updates,runtime=dict(baseline_path=runtime_path,baseline_sha256=sha(baseline),immutable_files=len(after['immutable_files']),immutable_bytes=after['immutable_bytes'],separate_file_identity_verified=after['separate_file_identity_verified'],private_writable_files=after['private_writable_files'],immutable_original_and_private_assets_unchanged=True),original_saves_checkpoints_historical_sources_and_reports_unchanged=True)

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
 if out.exists():p.error('fresh immutable native preservation output required')
 r=audit();out.write_text(json.dumps(r,indent=2)+'\n',encoding='utf8',newline='\n');print('Preserved frozen bootstrap artifacts',r['unchanged_bootstrap_artifact_count'],'and',r['runtime']['immutable_files'],'original/private native assets; previous history/saves/checkpoints unchanged')
