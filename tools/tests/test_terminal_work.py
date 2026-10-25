"""Real pause/fade completion, truncation endpoints and tamper refusal."""
import copy,gzip,json,struct,unittest
from unittest.mock import patch
from tools import terminal_work_emulation as e
from tools import terminal_work_model as m
from tools import terminal_work_verification as v

REPORT='analysis/terminal-work-source-v2-20261025.json.gz'


class TerminalWorkTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=json.loads(gzip.decompress((e.ROOT/REPORT).read_bytes()));cls.rows=cls.report['cases']
 def reject(self,edit,complete=False):
  r=copy.deepcopy(self.rows[0]);edit(r)
  with self.assertRaises((ValueError,KeyError)):(v.verify_case(r,False) if complete else m.verify_work(r))
 def test_both_complete_original_contracts(self):
  for r in self.rows:
   with self.subTest(name=r['input']['name']):self.assertFalse(v.verify_case(r,False)['all_owned_memory_CPU_and_trace_replayed'])
 def test_fresh_constructor_has_no_snapshot_loader(self):
  with patch.object(e.terminal,'combat',side_effect=AssertionError('snapshot forbidden')),patch.object(e.terminal,'accepted',side_effect=AssertionError('snapshot forbidden')):
   f=e.WorkMachine(e.corpus()[0]);self.assertEqual(f.get(e.TASK+0x60),e.WORK);self.assertEqual(f.get(e.VM+0x1C),0)
 def test_runtime_host_put_is_root_stack_only(self):
  f=e.WorkMachine(e.corpus()[0]);old=f.put
  def guarded(at,*args):self.assertTrue(0x12000000<=at<0x12020000);return old(at,*args)
  f.put=guarded;r=f.run();self.assertEqual(len(r['work']['experiments'][0]['ticks']),61)
 def test_frozen_guard_and_root_ABI_algorithms(self):
  self.assertIs(e.WorkMachine.source_code.__code__,e.parent.LiveMachine.source_code.__code__);self.assertIs(e.WorkMachine.base_call.__code__,e.parent.LiveMachine.base_call.__code__)
 def test_precise_fade_residuals(self):
  for row in self.rows:
   result=m.verify_work(row);self.assertEqual([(x['final_value'],x['delta'],x['remaining'],x['VM_wait']) for x in result],[(38880,648,0,0),(32,648,0,0)])
 def test_wait_and_query_are_different(self):
  r=self.rows[0];a,b=r['work']['experiments']
  self.assertEqual(a['ticks'][59][2]['call']['result'],1);self.assertEqual(b['ticks'][59][2]['call']['result'],0)
  self.assertEqual(bytes.fromhex(a['ticks'][59][0]['after']['VM'])[0x92E0],0)
 def test_final_successor_is_inactive(self):
  for exp in self.rows[0]['work']['experiments']:
   s=exp['ticks'][60][0];self.assertEqual(s['before'],s['after']);self.assertEqual(s['writes'][0],s['writes'][1]);self.assertEqual(s['call']['result'],1)
 def test_actual_pause_freezes_clock(self):
  for r in self.rows:
   a,b=r['work']['pause']['before'],r['work']['after'];self.assertEqual((a['remaining'],a['elapsed']),(b['remaining'],b['elapsed']))
 def test_source_handler_positions_not_VM_progress(self):
  for r in self.rows:
   self.assertEqual([x['source_command']['PC'] for x in r['work']['experiments']],[44,396] if r['input']['name']=='neutral_running' else [44,426])
   self.assertEqual(struct.unpack_from('<I',bytes.fromhex(r['work']['after']['VM']),0x1C)[0],0)
 def test_regions_disjoint(self):
  a=sorted(e.REGIONS);self.assertEqual(len(a),46)
  for (p,n),(q,k) in zip(a,a[1:]):self.assertLessEqual(p+n,q)
 def test_unknown_case_rejected(self):
  with self.assertRaises(ValueError):e.WorkMachine(e.parent.corpus()[0])
 def test_unknown_PC_rejected(self):
  f=e.WorkMachine(e.corpus()[0])
  with self.assertRaises(ValueError):f.source_code(f.uc,0x401000,1,None)
 def test_source_script_write_rejected(self):
  f=e.WorkMachine(e.corpus()[0])
  with self.assertRaises(ValueError):f.write_hook(f.uc,0,e.SCRIPT,4,0,None)
 def test_wrong_task_work_owner_rejected(self):
  def edit(r):
   b=bytearray.fromhex(r['initialization']['before']['task']);struct.pack_into('<I',b,0x60,e.VM);r['initialization']['before']['task']=b.hex()
  self.reject(edit)
 def test_hidden_pause_gate_rejected(self):
  def edit(r):
   b=bytearray.fromhex(r['work']['pause']['after']['gates']);b[8]=1;r['work']['pause']['after']['gates']=b.hex()
  self.reject(edit)
 def test_forged_pause_clock_rejected(self):self.reject(lambda r:r['work']['pause']['after'].update(remaining=1))
 def test_normalized_fade_end_rejected(self):
  def edit(r):
   s=r['work']['experiments'][0]['ticks'][59][0]['after'];b=bytearray.fromhex(s['work']);struct.pack_into('<i',b,0x2490,38912);s['work']=b.hex()
  self.reject(edit)
 def test_early_wait_release_rejected(self):
  def edit(r):
   s=r['work']['experiments'][0]['ticks'][0][0]['after'];b=bytearray.fromhex(s['VM']);b[0x92E0]=0;s['VM']=b.hex()
  self.reject(edit)
 def test_fake_VM_PC_rejected(self):
  def edit(r):
   s=r['work']['experiments'][0]['handler']['after'];b=bytearray.fromhex(s['VM']);struct.pack_into('<I',b,0x1C,52);s['VM']=b.hex()
  self.reject(edit)
 def test_missing_tick_rejected(self):self.reject(lambda r:r['work']['experiments'][0]['ticks'].pop())
 def test_wrong_source_command_rejected(self):self.reject(lambda r:r['work']['experiments'][0]['source_command'].update(PC=0))
 def test_host_wait_store_PC_rejected(self):self.reject(lambda r:next(x for x in r['key_writes'] if x['pc']==0x4977B8).update(pc=0))
 def test_missing_write_rejected(self):self.reject(lambda r:r['key_writes'].pop(0))
 def test_missing_complete_world_slot_rejected(self):self.reject(lambda r:r['world_frames'][0]['scanned_slots'].pop(),True)
 def test_fake_original_caller_rejected(self):self.reject(lambda r:r['work_calls'][2].update(caller=0),True)
 def test_missing_work_return_CPU_rejected(self):self.reject(lambda r:r['work_calls'][0].pop('cpu_after'),True)
 def test_fake_x87_control_restore_rejected(self):self.reject(lambda r:next(x for x in r['work_calls'] if x['entry']==0x56CFCC)['cpu_after'].update(FPCW=0),True)
 def test_digest_interval_forgery_rejected(self):self.reject(lambda r:r['work']['experiments'][0]['handler']['trace_before'].update(instructions=0),True)
 def test_extra_host_command_rejected(self):self.reject(lambda r:r['world_frames'][0]['controls'].append(dict(command=6)),True)
 def test_actual_native_leaf_claim_rejected(self):self.reject(lambda r:r['APIs'][0].update(actual_API_executed=False),True)


if __name__=='__main__':unittest.main()
