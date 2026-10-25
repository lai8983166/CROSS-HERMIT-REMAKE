"""Actual terminal task admission and refusal of manufactured pending state."""
import copy,gzip,json,struct,unittest
from unittest.mock import patch
from tools import terminal_task_emulation as e
from tools import terminal_task_model as m
from tools import terminal_task_verification as v

REPORT='analysis/terminal-task-source-v4-20261026.json.gz'


class TerminalTaskTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=json.loads(gzip.decompress((e.ROOT/REPORT).read_bytes()));cls.rows=cls.report['cases']
 def reject(self,edit,complete=False):
  r=copy.deepcopy(self.rows[0]);edit(r)
  with self.assertRaises((ValueError,KeyError)):(v.verify_case(r,False) if complete else m.verify(r))
 def mutate(self,r,step,field,offset,value,fmt='I'):
  s=step(r);b=bytearray.fromhex(s[field]);struct.pack_into('<'+fmt,b,offset,value);s[field]=b.hex()
 def test_both_source_contracts(self):
  for r in self.rows:
   with self.subTest(name=r['input']['name']):self.assertFalse(v.verify_case(r,False)['all_owned_memory_CPU_and_trace_replayed'])
 def test_no_snapshot_loader(self):
  with patch.object(e.terminal,'combat',side_effect=AssertionError('snapshot forbidden')),patch.object(e.terminal,'accepted',side_effect=AssertionError('snapshot forbidden')):
   f=e.TaskMachine(e.corpus()[0]);self.assertEqual(f.get(e.TASK+0x60),e.WORK);self.assertEqual(f.get(e.VM+0x1C),0)
 def test_host_runtime_put_only_root_stack(self):
  f=e.TaskMachine(e.corpus()[0]);old=f.put
  def guarded(at,*args):self.assertTrue(e.STACK<=at<e.STACK+0x20000);return old(at,*args)
  f.put=guarded;r=f.run();self.assertEqual(r['pending_CPU']['EIP'],e.STOP)
 def test_original_guard_and_root_ABI_algorithms(self):
  self.assertIs(e.TaskMachine.source_code.__code__,e.parent.WorkMachine.source_code.__code__);self.assertIs(e.TaskMachine.base_call.__code__,e.parent.WorkMachine.base_call.__code__)
 def test_two_returns_then_pending_VM(self):
  for r in self.rows:
   result=m.verify(r);self.assertEqual((result['task_roots_returned'],result['pending_task_roots'],result['normal_VM_instructions'],result['VM_PC']),(2,1,1,8))
 def test_real_null_IME_and_empty_text(self):
  for r in self.rows:
   self.assertEqual([x['name'] for x in r['task_APIs']],['lstrlenA','ImmGetOpenStatus','lstrlenA','ImmGetOpenStatus','lstrlenA'])
   self.assertTrue(all(x['actual_API_executed'] and x['result']==0 for x in r['task_APIs']));self.assertFalse(r['OS_input_submitted'])
 def test_packet_and_four_frames_remain_pending(self):
  for r in self.rows:
   p=r['admission']['partial']['pending'];self.assertFalse(p['first_instruction_executed']);self.assertEqual(p['args'],[20,0])
   self.assertEqual([r['task_calls'][i]['entry'] for i in p['open_calls']],[0x454CF0,0x4CE8F0,0x4D29E0,0x4D2CA0])
   self.assertEqual(p['packet'],m.packet_project(0x40))
 def test_clock_stays_frozen(self):
  for r in self.rows:
   a=r['admission'];self.assertEqual([(s['after']['remaining'],s['after']['elapsed']) for f in a['frames'] for s in f],[(a['partial']['after']['remaining'],a['partial']['after']['elapsed'])]*10)
 def test_50_disjoint_regions(self):
  a=sorted(e.REGIONS);self.assertEqual(len(a),50)
  for (p,n),(q,k) in zip(a,a[1:]):self.assertLessEqual(p+n,q)
 def test_unknown_case(self):
  with self.assertRaises(ValueError):e.TaskMachine(e.parent.parent.corpus()[0])
 def test_unknown_PC(self):
  f=e.TaskMachine(e.corpus()[0])
  with self.assertRaises(ValueError):f.source_code(f.uc,0x401000,1,None)
 def test_source_write(self):
  f=e.TaskMachine(e.corpus()[0])
  with self.assertRaises(ValueError):f.write_hook(f.uc,0,e.SCRIPT,4,0,None)
 def test_wrong_first_stage(self):self.reject(lambda r:self.mutate(r,lambda r:r['admission']['frames'][0][1]['after'],'task',0x44,2,'B'))
 def test_wrong_second_stage(self):self.reject(lambda r:self.mutate(r,lambda r:r['admission']['frames'][1][1]['after'],'task',0x44,1,'B'))
 def test_missing_input_reset(self):self.reject(lambda r:self.mutate(r,lambda r:r['admission']['frames'][1][0]['after'],'owner',0x7B0,255,'B'))
 def test_hidden_render_gate(self):self.reject(lambda r:self.mutate(r,lambda r:r['admission']['partial']['before'],'VM',0x93E2,1,'B'))
 def test_fake_VM_PC(self):self.reject(lambda r:self.mutate(r,lambda r:r['admission']['partial']['after'],'VM',0x1C,44))
 def test_fake_VM_variable(self):self.reject(lambda r:self.mutate(r,lambda r:r['admission']['partial']['after'],'VM',0x3C,0))
 def test_fake_SEH(self):self.reject(lambda r:r['admission']['partial']['after'].update(SEH='00000000'))
 def test_fake_packet(self):self.reject(lambda r:r['admission']['partial']['pending'].update(packet=bytes(128).hex()))
 def test_fake_original_stack(self):
  def edit(r):
   p=r['admission']['partial']['pending'];b=bytearray.fromhex(p['stack']);struct.pack_into('<I',b,p['CPU']['ESP']-e.STACK,0);p['stack']=b.hex()
  self.reject(edit)
 def test_fake_resource_args(self):self.reject(lambda r:r['admission']['partial']['pending'].update(args=[0,0]))
 def test_false_completed_root(self):self.reject(lambda r:r['admission']['partial']['root'].update(returned=True))
 def test_false_completed_nested_frame(self):self.reject(lambda r:r['task_calls'][r['admission']['partial']['pending']['open_calls'][0]].update(cpu_after={}),True)
 def test_fake_native_query(self):self.reject(lambda r:r['task_APIs'][1].update(actual_API_executed=False),True)
 def test_missing_native_query(self):self.reject(lambda r:r['task_APIs'].pop(1),True)
 def test_wrong_IME_identity(self):self.reject(lambda r:r['IME_identity'].update(sha256='0'*64),True)
 def test_fake_original_caller(self):self.reject(lambda r:r['task_calls'][0].update(caller=0),True)
 def test_missing_complete_world_slot(self):self.reject(lambda r:r['world_frames'][0]['scanned_slots'].pop(),True)
 def test_wrong_root_order(self):self.reject(lambda r:r['admission']['frames'][0][0]['call'].update(entry=0x454CF0),True)
 def test_missing_frame(self):self.reject(lambda r:r['admission']['frames'].pop())
 def test_wrong_clock(self):self.reject(lambda r:r['admission']['frames'][0][3]['after'].update(remaining=0))
 def test_digest_gap(self):self.reject(lambda r:r['admission']['frames'][0][0]['trace_before'].update(instructions=0),True)


if __name__=='__main__':unittest.main()
