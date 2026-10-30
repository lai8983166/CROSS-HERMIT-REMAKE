"""Preserve the accepted script-exit artifacts and all original ancestors."""
import argparse,json
from tools.terminal_script_exit_preservation import audit as previous_audit,file_identity,verify_local,ROOT,need,sha,terminal
PARENT='analysis/terminal-script-exit-acceptance-v1-20261030.json'
PARENT_SHA='2223c1d28e459805547be409cb669219392b73f6a73d0f02617c8e441a6e9d2d'
def audit():
 previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted script-exit self');accepted=json.loads(raw);frozen=[];updates=[]
 for row in accepted['artifact_manifest']:
  current=file_identity(row['path'])
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=current['sha256'],reason='current source-backed original terminal task completion handshake'))
  else:need(current=={k:row[k] for k in ('path','bytes','sha256')},'frozen script-exit artifact '+row['path']);frozen.append(current)
 need(len(frozen)==69,'all69 accepted script-exit artifacts');return dict(schema_version=1,previous_acceptance=dict(path=PARENT,bytes=len(raw),sha256=PARENT_SHA),frozen_artifact_count=len(frozen),frozen_artifacts=frozen,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True,local_large_evidence_bytes_checked=True,historical_acceptance_Git_equalities_refer_to_original_bundled_history=True)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out');p.add_argument('--local-evidence');a=p.parse_args();need(bool(a.out) or bool(a.local_evidence),'explicit preservation output or local catalog')
 if a.local_evidence:print(json.dumps(verify_local(ROOT/a.local_evidence)))
 if a.out:need(not(ROOT/a.out).exists(),'fresh immutable task-completion preservation');terminal.save(a.out,audit());print('69 predecessor artifacts, acceptance self and recursive originals preserved')
