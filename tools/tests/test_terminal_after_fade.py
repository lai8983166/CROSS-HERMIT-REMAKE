"""Refuse shortened waits, fabricated timer/role progress and false native receipts."""
import copy,gzip,json,struct,unittest
from types import SimpleNamespace
from unittest.mock import patch
from tools import terminal_after_fade_emulation as e
from tools import terminal_after_fade_model as m
from tools import terminal_after_fade_verification as v
REPORT='analysis/terminal-after-fade-source-v5-20261026.json.gz'

class TerminalAfterFadeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=json.loads(gzip.decompress((e.ROOT/REPORT).read_bytes()));cls.rows=cls.report['cases']
 def fixture(self):
  r=self.rows[0];return e.FadeMachine(e.parent.parent.corpus()[0],SimpleNamespace(hello=r['current_CRT_hello']),SimpleNamespace(hello=r['current_GPU_hello'],device=r['current_GPU_hello']['device']))
 def reject(self,edit,whole=False):
  row=copy.deepcopy(self.rows[0]);edit(row)
  with self.assertRaises((ValueError,KeyError,StopIteration)):(v.verify_case(row) if whole else m.verify(row))
 def mutate(self,r,index,field,offset,value,fmt='I'):
  s=r['after_fade']['frames'][index]['task']['after'];b=bytearray.fromhex(s[field]);struct.pack_into('<'+fmt,b,offset,value);s[field]=b.hex()
 def test_both_source_contracts(self):
  self.assertEqual(self.report['source_contract'],e.source_contract())
  for row in self.rows:
   with self.subTest(name=row['input']['name']):self.assertFalse(v.verify_case(row)['all_owned_memory_CPU_and_trace_replayed'])
 def test_two_distinct_source_roles(self):
  self.assertEqual([m.verify(r)['role'] for r in self.rows],[2,1])
 def test_original_wait_endpoint_and_timer_boundary(self):
  for r in self.rows:
   x=m.verify(r);self.assertEqual((x['fade_updates'],x['fade_value'],x['timer_polls'],x['timer_count'],x['VM_PC']),(59,38880,31,31,76));self.assertFalse(x['font_executed'])
 def test_original_complete_roots_only(self):
  for r in self.rows:
   f=r['after_fade'];self.assertEqual(sum(x['task']['returned'] for x in f['frames']),95)
   self.assertTrue(all(x['task']['root']['entry']==0x454CF0 for x in f['frames']));self.assertEqual(e.source_contract()['new_VM_or_work_update_roots'],0)
 def test_guard_and_root_algorithms_preserved(self):
  self.assertIs(e.FadeMachine.source_code.__code__,e.parent.OverlayMachine.source_code.__code__);self.assertIs(e.FadeMachine.base_call.__code__,e.parent.OverlayMachine.base_call.__code__)
 def test_no_snapshot_loader(self):
  with patch.object(e.terminal,'combat',side_effect=AssertionError('snapshot forbidden')),patch.object(e.terminal,'accepted',side_effect=AssertionError('snapshot forbidden')):self.assertEqual(self.fixture().get(e.VM+28),0)
 def test_unknown_PC_rejected(self):
  f=self.fixture()
  with self.assertRaises(ValueError):f.source_code(f.uc,0x401000,1,None)
 def test_source_write_rejected(self):
  f=self.fixture()
  with self.assertRaises(ValueError):f.write_hook(f.uc,0,e.SCRIPT,4,0,None)
 def test_missing_fade_frame(self):self.reject(lambda r:r['after_fade']['frames'].pop(20))
 def test_early_work_clear(self):self.reject(lambda r:self.mutate(r,57,'VM',0x92E0,0,'B'))
 def test_normalized_endpoint(self):self.reject(lambda r:self.mutate(r,58,'work',0x2490,38912))
 def test_wrong_last_remaining(self):self.reject(lambda r:self.mutate(r,58,'work',0x249C,1))
 def test_wrong_status(self):self.reject(lambda r:self.mutate(r,58,'work',0x249A,1,'B'))
 def test_wrong_step(self):self.reject(lambda r:self.mutate(r,0,'work',0x2490,1297))
 def test_skipped_vm_work_poll(self):self.reject(lambda r:self.mutate(r,58,'VM',0x20,0,'H'))
 def test_skipped_display_wait(self):self.reject(lambda r:self.mutate(r,60,'VM',0x20,0,'H'))
 def test_fake_text_mode(self):self.reject(lambda r:self.mutate(r,62,'VM',0x9228,1,'B'))
 def test_timer_shortened(self):self.reject(lambda r:self.mutate(r,63,'VM',0x2A,29,'H'))
 def test_timer_early_clear(self):self.reject(lambda r:self.mutate(r,93,'VM',0x20,0,'H'))
 def test_timer_normalized_count(self):self.reject(lambda r:self.mutate(r,94,'VM',0x28,30,'H'))
 def test_fake_role(self):self.reject(lambda r:self.mutate(r,95,'VM',0x9254,5))
 def test_wrong_config(self):self.reject(lambda r:self.mutate(r,95,'VM',0x73D0,9,'H'))
 def test_fake_completed_PC(self):self.reject(lambda r:self.mutate(r,95,'VM',28,96))
 def test_wrong_source_command(self):self.reject(lambda r:r['after_fade']['commands'][0].update(source_offset=0))
 def test_lost_original_work_write(self):
  def edit(r):
   i=next(i for i,x in enumerate(r['after_fade']['writes']) if x['address']==e.WORK+0x2490);r['after_fade']['writes'][i]['pc']=0
  self.reject(edit)
 def test_fake_queue_head(self):self.reject(lambda r:r['after_fade']['frames'][0]['queue_after'].update(heads=bytes(32768).hex()))
 def test_host_arena_clear(self):self.reject(lambda r:r['after_fade']['frames'][-1]['queue_after'].update(unused_tail_sha256=e.sha(bytes(65536))))
 def test_wrong_font_args(self):self.reject(lambda r:r['after_fade']['pending']['args'].__setitem__(0,24))
 def test_false_font_executed(self):self.reject(lambda r:r['after_fade']['pending'].update(first_instruction_executed=True))
 def test_false_root_return(self):self.reject(lambda r:r['after_fade']['frames'][-1]['task'].update(returned=True))
 def test_wrong_raw_stack(self):self.reject(lambda r:r['after_fade']['pending'].update(stack=bytes(0x20000).hex()))
 def test_wrong_SEH(self):self.reject(lambda r:r['after_fade']['pending'].update(SEH='01000000'))
 def test_false_nested_return(self):
  def edit(r):
   f=r['after_fade'];f['calls'][f['pending']['open_calls'][0]]['cpu_after']={}
  self.reject(edit)
 def test_wrong_root_kind(self):self.reject(lambda r:r['after_fade']['frames'][0]['task']['root'].update(entry=0x4CE8F0),True)
 def test_missing_native_query(self):self.reject(lambda r:r['task_APIs'][9].update(actual_API_executed=False),True)
 def test_changed_IME_module(self):self.reject(lambda r:r['IME_identity'].update(sha256='0'*64),True)
 def test_fake_native_receipt(self):self.reject(lambda r:r['GPU_trace'][0]['reply']['result'].update(hr=-1),True)
 def test_broken_digest(self):self.reject(lambda r:r['after_fade']['frames'][3]['trace_before'].update(instructions=0))
 def test_host_runtime_put_only_root_stack(self):
  ch,gh,_=e.helpers();live=e.parent.platform.crt.Live(ch);gpu=e.parent.platform.OverlayGPU(gh)
  try:
   f=e.FadeMachine(e.parent.parent.corpus()[0],live,gpu);old=f.put
   def put(p,*a):self.assertTrue(e.STACK<=p<e.STACK+0x20000);return old(p,*a)
   f.put=put;r=f.run();self.assertEqual(m.verify(r)['VM_PC'],76);self.assertTrue(live.close()['all_owned_resources_released']);self.assertTrue(gpu.close()['all_owned_resources_released'])
  finally:
   if not live.closed:live._terminate()
   if not gpu.closed:gpu._terminate()

if __name__=='__main__':unittest.main()
