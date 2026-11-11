"""Independent bounded mutations of v9 evidence, no native execution."""
import copy,hashlib,json
from pathlib import Path
from devtools.terminal_tcg_context_wait_verify_v2 import verify
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'.venv-audit/native-worker/tcg-wait-native-v9/observation.json';OUT=ROOT/'analysis/terminal-wait-tcg-context-review-mutations-v1-20261111.json'
def main():
 t=json.loads(P.read_bytes());plan=json.loads((ROOT/t['plan_source']['path']).read_bytes());rows=[]
 def test(name,change):
  x=copy.deepcopy(t);change(x);r=verify(x,plan);rows.append(dict(name=name,rejected=not r['same_wait_writes_verified'],failed=[c['name']for c in r['checks']if not c['passed']],errors=r['errors']))
 def point(x,n):return next(p for p in x['points']if p['label']==n)
 def step(x,n):return next(p for p in x['steps']if p['label']==n)
 test('ret_cpu0_rax',lambda x:point(x,'ret32')['states'][0]['gpr'].__setitem__(0,'0000000000000001'))
 test('point_teb_owner',lambda x:point(x,'kernel-clear-before').__setitem__('owner_teb_client_id_hex','00'*8))
 test('pxor_bytes',lambda x:step(x,'pxor-3').__setitem__('bytes_hex','90'*16))
 test('duplicate_point',lambda x:x['points'].append(copy.deepcopy(x['points'][0])))
 test('CR2_digest',lambda x:x['ledger_end'].__setitem__('events_sha256','0'*64))
 test('filter_poison',lambda x:x['context_filter'][3].__setitem__('poisoned',True))
 test('syscall_wrong_stop_thread',lambda x:step(x,'syscall').__setitem__('reply','T05thread:02;'))
 test('ret12_wrong_stop_thread',lambda x:step(x,'ret12').__setitem__('reply','T05thread:02;'))
 test('remove_selector13_point',lambda x:x.__setitem__('points',[p for p in x['points']if p['label']!='selector13']))
 test('reverse_point_chronology',lambda x:x['points'].reverse())
 test('kernel_entry_signature_corrupt',lambda x:point(x,'kernel-entry')['extra'].__setitem__('signature','00'*64))
 test('filter_negative_rejection_count',lambda x:x['context_filter'][-1].__setitem__('rejected',-1))
 test('filter_empty_points',lambda x:x['context_filter'][3].__setitem__('points',[]))
 report=dict(accepted=False,source=dict(path=str(P),bytes=P.stat().st_size,sha256=hashlib.sha256(P.read_bytes()).hexdigest()),baseline=verify(t,plan)['same_wait_writes_verified'],mutations=rows)
 with OUT.open('x')as f:json.dump(report,f,indent=2)
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
