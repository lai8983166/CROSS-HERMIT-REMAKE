"""Preserve the complete accepted battle-stage evidence and all ancestors."""
import argparse,json
from tools.terminal_battle_stage_handoff_preservation import audit as previous_audit,file_identity,verify_local,ROOT,need,sha,terminal
PARENT='analysis/terminal-battle-stage-handoff-acceptance-v1-20261101.json'
PARENT_SHA='1b6f1d29bb50228546639be89fa715737f12edfa0d3eb54ab7434650481d3c2d'
def audit():
 previous=previous_audit();raw=(ROOT/PARENT).read_bytes();need(sha(raw)==PARENT_SHA,'fixed accepted battle-stage self');accepted=json.loads(raw);frozen=[];updates=[]
 for row in accepted['artifact_manifest']:
  current=file_identity(row['path'])
  if row['path'] in ('.gitattributes','openspec/specs/reverse-engineering/completion/spec.md'):
   updates.append(dict(path=row['path'],previous_sha256=row['sha256'],current_sha256=current['sha256'],reason='current original battle exit prefix and supplemental accounting correction'))
  else:
   need(current=={k:row[k] for k in ('path','bytes','sha256')},'frozen battle-stage artifact '+row['path']);frozen.append(current)
 need(len(frozen)==len(accepted['artifact_manifest'])-2,'every accepted battle-stage artifact except authorized running documents')
 return dict(schema_version=1,previous_acceptance=dict(path=PARENT,bytes=len(raw),sha256=PARENT_SHA),frozen_artifact_count=len(frozen),frozen_artifacts=frozen,authorized_updates=updates,previous_recheck=previous,original_saves_checkpoints_resources_and_history_unchanged=True,historical_acceptance_not_rewritten=True)
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out');p.add_argument('--local-evidence');a=p.parse_args();need(bool(a.out) or bool(a.local_evidence),'explicit immutable audit output')
 if a.local_evidence:print(json.dumps(verify_local(ROOT/a.local_evidence)))
 if a.out:need(not(ROOT/a.out).exists(),'fresh immutable exit-prefix preservation');terminal.save(a.out,audit())
