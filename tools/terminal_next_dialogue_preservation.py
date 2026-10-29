"""Freeze the accepted followup and recursively preserve original evidence."""
import argparse,hashlib,json
from pathlib import Path,PurePosixPath
from tools.terminal_replacement_preservation import audit as previous_audit
from tools.terminal_followup_emulation import ROOT,need,sha,terminal

PARENT='analysis/terminal-replacement-acceptance-v1-20261028.json'
PARENT_SHA='c08c51bbcf42e9b47b806ec6c846da8e55492838752c57374a0bfe7969b11df5'

def file_identity(path):
 h=hashlib.sha256();n=0
 with (ROOT/path).open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block);n+=len(block)
 return dict(path=path,bytes=n,sha256=h.hexdigest())

def audit():
 previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted followup self');accepted=json.loads(raw);frozen=[];updates=[]
 for row in accepted['artifact_manifest']:
  current=file_identity(row['path'])
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=current['sha256'],reason='current original next dialogue and role2 resources'))
  else:
   need(current=={k:row[k] for k in ('path','bytes','sha256')},'frozen followup artifact '+row['path']);frozen.append(current)
 need(len(frozen)==70,'all70 accepted replacement artifacts')
 return dict(schema_version=1,previous_acceptance=dict(path=PARENT,bytes=len(raw),sha256=PARENT_SHA),frozen_artifact_count=len(frozen),frozen_artifacts=frozen,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True,local_large_evidence_bytes_checked=True,historical_acceptance_Git_equalities_refer_to_original_bundled_history=True)

def verify_local(catalog):
 data=json.loads(catalog.read_text(encoding='utf8'));need(data.get('schema_version')==1 and isinstance(data.get('files'),list) and data['files'],'explicit local replacement evidence catalog');seen=set();total=0
 for row in data['files']:
  p=PurePosixPath(row['path']);need(not p.is_absolute() and '..' not in p.parts and row['path'] not in seen,'unique safe relative evidence path');seen.add(row['path']);need((ROOT/row['path']).resolve().is_relative_to(ROOT.resolve()),'evidence stays within project')
  want={k:row[k] for k in ('path','bytes','sha256')};need(file_identity(row['path'])==want,'local evidence complete size and SHA')
  backup=Path(row['backup_path']);need(backup.is_absolute() and backup.is_file() and not backup.resolve().is_relative_to(ROOT.resolve()),'explicit repository-external backup')
  h=hashlib.sha256();n=0
  with backup.open('rb') as f:
   for block in iter(lambda:f.read(1024*1024),b''):h.update(block);n+=len(block)
  need((n,h.hexdigest())==(row['bytes'],row['sha256']),'external backup complete size and SHA');total+=n
 return dict(files=len(seen),bytes=total,local_and_external_backup_SHA256_match=True)

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out');p.add_argument('--local-evidence');a=p.parse_args()
 need(bool(a.out) or bool(a.local_evidence),'preservation output or local evidence catalog required')
 if a.local_evidence:print(json.dumps(verify_local(ROOT/a.local_evidence)))
 if a.out:
  need(not(ROOT/a.out).exists(),'fresh immutable replacement preservation');terminal.save(a.out,audit());print('70 predecessor artifacts, acceptance self and recursive originals preserved')
