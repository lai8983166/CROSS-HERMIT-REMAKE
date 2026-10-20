"""Read-only raw historical/save/checkpoint integrity audit for R2."""
import hashlib,json
from concurrent.futures import ThreadPoolExecutor
from tools.school_retained_rendering import ROOT

def sha_file(path):
 h=hashlib.sha256()
 with path.open('rb') as stream:
  for b in iter(lambda:stream.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def require(v,msg):
 if not v:raise ValueError(msg)
def retained(path):
 r=json.loads((ROOT/path).read_text(encoding='utf8'))
 if 'retained_files' in r:return {x['path']:x for x in r['retained_files']}
 p=r['parent_preservation'];require(sha_file(ROOT/p['path'])==p['sha256'],'parent preservation identity')
 rows=retained(p['path'])
 for at in r.get('excluded_parent_paths',[]):rows.pop(at,None)
 for before,after in r.get('archive_relocations',{}).items():
  if before in rows:row=rows.pop(before);rows[after]=dict(row,path=after)
 for row in r.get('additional_retained',[]):rows[row['path']]=row
 require(len(rows)==r['retained_file_count'],'historical retention count '+path)
 return rows
def audit():
 parent='analysis/school-startup-lifetime-preservation-20261020.json';p=json.loads((ROOT/parent).read_text())
 rows=retained(parent)
 def check(row):require(sha_file(ROOT/row['path'])==row['sha256'],'historical raw bytes '+row['path'])
 with ThreadPoolExecutor(max_workers=8) as pool:list(pool.map(check,rows.values()))
 relocations={}
 for row in p['unchanged_previous_unit_artifacts']:
  path=row['path']
  if path.startswith('openspec/changes/close-original-startup/'):
   path=path.replace('openspec/changes/close-original-startup/','openspec/changes/archive/2026-10-20-close-original-startup/',1);relocations[row['path']]=path
  require(sha_file(ROOT/path)==row['sha256'],'R1 frozen previous artifact '+path)
 for row in p['unchanged_private_checkpoints']:
  f=ROOT/row['path'];require(f.stat().st_size==row['bytes'] and sha_file(f)==row['sha256'],'private original VM checkpoint '+row['path'])
 for row in p['save_rules'].values():require(sha_file(ROOT/row['path'])==row['sha256'],'prototype rule bytes '+row['path'])
 saves=json.loads((ROOT/'analysis/school-startup-lifetime-save-recheck-20261020.json').read_text())
 for row in saves['after']:
  f=ROOT/row['path'];require(f.stat().st_size==row['bytes'] and f.stat().st_mtime_ns==row['mtime_ns'] and sha_file(f)==row['sha256'],'original installed save bytes/time '+row['path'])
 require(sha_file(ROOT/'analysis/downloaded_saves/atwiki-all-characters.SAV')==saves['downloaded_original_sha256'],'original downloaded save')
 acceptance=json.loads((ROOT/'analysis/school-startup-lifetime-acceptance-20261020.json').read_text())
 exceptions=[]
 for row in acceptance['artifact_manifest']:
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   exceptions.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=sha_file(ROOT/row['path']),reason='R2 attributes or master roadmap update'));continue
  require(sha_file(ROOT/row['path'])==row['sha256'],'R1 final acceptance frozen artifact '+row['path'])
 return dict(schema_version=1,parent_preservation=dict(path=parent,sha256=sha_file(ROOT/parent)),historical_raw_files=len(rows),previous_unit_frozen_artifacts=len(p['unchanged_previous_unit_artifacts']),R1_archive_relocations=relocations,private_original_VM_checkpoints=len(p['unchanged_private_checkpoints']),prototype_rules=len(p['save_rules']),installed_save_inventory=saves['after'],downloaded_original_sha256=saves['downloaded_original_sha256'],authorized_R1_manifest_updates=exceptions,historical_bytes_unchanged=True,original_saves_bytes_and_times_unchanged=True,original_private_checkpoints_unchanged=True)
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',required=True);a=parser.parse_args()
 result=audit();(ROOT/a.out).write_text(json.dumps(result,indent=2)+'\n',encoding='utf8',newline='\n');print('Preserved',result['historical_raw_files'],'historical raw files,',result['private_original_VM_checkpoints'],'private VM checkpoints and original saves')
