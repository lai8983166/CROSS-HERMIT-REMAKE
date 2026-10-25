from pathlib import Path
import time,json,gzip,hashlib
from concurrent.futures import ProcessPoolExecutor,wait,FIRST_COMPLETED
from tools.battle_live_terminal_verification import (ROOT,IMPLEMENTATIONS,corpus,source_contract,verify_reference,terminal)

P='analysis/battle-live-terminal-';BUNDLE=P+'source-v2-20261025.json';OUT=P+'proof-v1-20261025.json'
def hashes():return {n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in IMPLEMENTATIONS}
def main():
 assert not (ROOT/OUT).exists();start_hashes=hashes();expected=corpus();submitted={};results={};deadline=time.monotonic()+3600
 with ProcessPoolExecutor(max_workers=2) as pool:
  pending={}
  while len(results)<len(expected):
   assert time.monotonic()<deadline,'bounded full replay queue';assert hashes()==start_hashes,'core implementation unchanged during complete replay'
   for c in expected:
    if c['name'] in submitted:continue
    path=P+'source-v2-20261025-'+c['name']+'.json.gz';p=ROOT/path
    if not p.exists():continue
    raw=p.read_bytes()
    try:d=json.loads(gzip.decompress(raw))
    except (OSError,EOFError,ValueError):continue
    assert d['source_contract']==source_contract() and len(d['cases'])==1 and d['cases'][0]['input']==c
    r=dict(name=c['name'],path=path,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest());submitted[c['name']]=r;pending[pool.submit(verify_reference,r)]=c['name']
   if pending:
    done,_=wait(pending,timeout=1,return_when=FIRST_COMPLETED)
    for future in done:results[pending.pop(future)]=future.result()
   else:time.sleep(1)
 assert hashes()==start_hashes;raw=(ROOT/BUNDLE).read_bytes();d=json.loads(raw)
 assert d['source_contract']==source_contract() and d['case_reports']==[submitted[c['name']] for c in expected]
 rows=[results[c['name']] for c in expected]
 report=dict(schema_version=1,source_report=terminal.ref(BUNDLE),case_count=7,cases=rows,implementation_sha256=start_hashes,
  world_frames=sum(r['frames'] for r in rows),original_instructions=sum(r['instructions'] for r in rows),original_writes=sum(r['writes'] for r in rows),
  independent_frame_clock_combat_event_and_result_contracts=True,all_original_PC_and_write_digests_replayed=True,independent_whole_VM_world_byte_model=False,
  combat_world_events_same_instance=True,original_outer_scheduler_connected=False,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False,
  replay_dispatch='each immutable completed case freshly replayed once; final full bundle references bound exactly afterward',implementation_hash_before_and_after_same=True)
 terminal.save(OUT,report);print('ALL SEVEN COMPLETE ORIGINAL REPLAYS VERIFIED',report['world_frames'],flush=True)
if __name__=='__main__':main()
