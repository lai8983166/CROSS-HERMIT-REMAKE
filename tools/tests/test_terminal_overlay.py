"""Reject fabricated resources, disabled drawing, false VM progress and native receipts."""
import copy,gzip,json,struct,unittest
from types import SimpleNamespace
from unittest.mock import patch
from tools import terminal_overlay_emulation as e
from tools import terminal_overlay_model as m
from tools import terminal_overlay_verification as v
REPORT='analysis/terminal-overlay-source-v13-20261026.json.gz'

class TerminalOverlayTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=json.loads(gzip.decompress((e.ROOT/REPORT).read_bytes()));cls.rows=cls.report['cases']
 def reject(self,edit,whole=False):
  row=copy.deepcopy(self.rows[0]);edit(row)
  with self.assertRaises((ValueError,KeyError,StopIteration)):(v.verify_case(row) if whole else m.verify(row))
 def mutate(self,r,field,offset,value,fmt='I'):
  x=r['overlay_continuation']['after'];b=bytearray.fromhex(x[field]);struct.pack_into('<'+fmt,b,offset,value);x[field]=b.hex()
 def memory(self,rows,p,data):
  x=next(x for x in rows if x['pointer']<=p and p+len(data)<=x['pointer']+x['bytes']);b=bytearray.fromhex(x['hex']);b[p-x['pointer']:p-x['pointer']+len(data)]=data;x['hex']=b.hex()
 def test_two_complete_contracts(self):
  for r in self.rows:
   result=v.verify_case(r);self.assertEqual((result['selector'],result['VM_PC']),(1 if r['input']['name']=='neutral_running' else 4,52))
 def test_source_and_actual_pixel_identity(self):
  self.assertEqual(self.report['source_contract'],e.source_contract())
  for r in self.rows:self.assertEqual(bytes.fromhex(r['resource_loaded']['upload_hex']),e.RESOURCE[24:])
 def test_original_GYBC_loader_group20(self):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  md=Cs(CS_ARCH_X86,CS_MODE_32)
  expected={0x4548FD:('push','0x59a4c4'),0x45490E:('call','0x42ae20'),0x454943:('push','0x14'),0x45494F:('call','0x416790'),0x45495E:('call','0x428ad0')}
  for p,want in expected.items():
   i=next(md.disasm(e.CODE[p-0x400000:p-0x400000+16],p));self.assertEqual((i.mnemonic,i.op_str),want)
  self.assertEqual(e.CODE[0x19A4C4:0x19A4DC],e.RESOURCE_NAME.encode()+bytes(1))
 def test_five_tasks_three_queries_and_taken_branch(self):
  for r in self.rows:
   x=m.verify(r);self.assertEqual((x['complete_task_returns'],x['overlay_queries'],x['VM_commands'],x['WORK_remaining']),(5,3,3,59))
 def test_all_new_and_normal_native_resources(self):
  for r in self.rows:
   v.native(r);self.assertFalse(r['CRT_cleanup']['forced_cleanup']);self.assertEqual(r['cleanup_state']['bank'],bytes(8).hex())
 def test_no_snapshot_loader(self):
  r=self.rows[0];gpu=SimpleNamespace(hello=r['current_GPU_hello'],device=r['current_GPU_hello']['device']);live=SimpleNamespace(hello=r['current_CRT_hello'])
  with patch.object(e.terminal,'combat',side_effect=AssertionError('snapshot forbidden')),patch.object(e.terminal,'accepted',side_effect=AssertionError('snapshot forbidden')):
   f=e.OverlayMachine(e.parent.corpus()[0],live,gpu);self.assertEqual(f.get(e.VM+28),0);self.assertEqual(f.get(e.MAIN+0xB28E,'h'),1)
 def test_unknown_instruction_guard(self):
  r=self.rows[0];f=e.OverlayMachine(e.parent.corpus()[0],SimpleNamespace(hello=r['current_CRT_hello']),SimpleNamespace(hello=r['current_GPU_hello'],device=r['current_GPU_hello']['device']))
  with self.assertRaises(ValueError):f.source_code(f.uc,0x401000,1,None)
 def test_forbidden_game_code_write(self):
  r=self.rows[0];f=e.OverlayMachine(e.parent.corpus()[0],SimpleNamespace(hello=r['current_CRT_hello']),SimpleNamespace(hello=r['current_GPU_hello'],device=r['current_GPU_hello']['device']))
  with self.assertRaises(ValueError):f.write_hook(f.uc,0,0x407870,4,0,None)
 def test_fake_record(self):self.reject(lambda r:r['resource_loaded'].update(record_hex=bytes(84).hex()))
 def test_missing_bank(self):self.reject(lambda r:r['resource_loaded'].update(bank=bytes(8).hex()))
 def test_wrong_pixel(self):self.reject(lambda r:r['resource_loaded'].update(upload_hex='00'+r['resource_loaded']['upload_hex'][2:]))
 def test_wrong_native_readback(self):self.reject(lambda r:r['resource_loaded']['readback'].update(sha256='0'*64))
 def test_wrong_owner_device(self):self.reject(lambda r:r['resource_loaded']['owner_device'].update(pointer=0))
 def test_closed_render_gate(self):self.reject(lambda r:self.memory(r['resource_loaded']['memory'],e.MAIN+0xB28E,bytes(2)))
 def test_fake_query_pointer(self):self.reject(lambda r:r['overlay_continuation']['calls'][1].update(result=0))
 def test_fake_query_group(self):self.reject(lambda r:r['overlay_continuation']['calls'][0].update(args=[0,0]))
 def test_fake_query_packet(self):self.reject(lambda r:r['overlay_continuation']['calls'][0].update(packet_after=bytes(128).hex()))
 def test_missing_query(self):self.reject(lambda r:r['overlay_continuation']['calls'].pop())
 def test_wrong_nested_return(self):self.reject(lambda r:r['overlay_continuation']['calls'][0]['cpu_after'].update(ESP=0))
 def test_wrong_SEH(self):self.reject(lambda r:r['overlay_continuation']['after'].update(SEH='01000000'))
 def test_wrong_PC(self):self.reject(lambda r:self.mutate(r,'VM',28,44))
 def test_false_ready(self):self.reject(lambda r:self.mutate(r,'VM',0x92E0,0,'B'))
 def test_wrong_work_delta(self):self.reject(lambda r:self.mutate(r,'work',0x2494,649))
 def test_wrong_work_remaining(self):self.reject(lambda r:self.mutate(r,'work',0x249C,60))
 def test_wrong_work_value(self):self.reject(lambda r:self.mutate(r,'work',0x2490,0))
 def test_fake_branch(self):self.reject(lambda r:r['overlay_continuation']['commands'][1].update(PC=28))
 def test_fake_source_offset(self):self.reject(lambda r:r['overlay_continuation']['commands'][1].update(source_offset=0))
 def test_false_task_return(self):self.reject(lambda r:r['overlay_continuation']['first_task']['after_CPU'].update(EIP=e.parent.STOP))
 def test_clock_advanced(self):self.reject(lambda r:r['overlay_continuation']['after'].update(elapsed=5))
 def test_missing_queue_head(self):
  def edit(r):
   rows=r['overlay_continuation']['memory'];heads=m.queue(rows,r['resource_loaded']['record'])['heads'];self.memory(rows,heads+51*8,bytes(8))
  self.reject(edit)
 def test_fake_queue_record(self):
  def edit(r):
   rows=r['overlay_continuation']['memory'];arena=m.queue(rows,r['resource_loaded']['record'])['arena'];self.memory(rows,arena+0x50,bytes(4))
  self.reject(edit)
 def test_mutated_arena_tail(self):
  def edit(r):
   rows=r['overlay_continuation']['memory'];arena=m.queue(rows,r['resource_loaded']['record'])['arena'];self.memory(rows,arena+100,b'x')
  self.reject(edit)
 def test_lost_cleanup(self):self.reject(lambda r:r['CRT_cleanup'].update(all_owned_resources_released=False))
 def test_changed_accounting(self):self.reject(lambda r:r['cleanup_state'].update(game_bytes=0))
 def test_fake_GPU_leaf(self):self.reject(lambda r:r['GPU_APIs'][0].update(actual_API_executed=False))
 def test_fake_native_receipt(self):self.reject(lambda r:r['GPU_trace'][0]['reply']['result'].update(hr=-1),True)
 def test_missing_actual_read(self):self.reject(lambda r:r['CRT_APIs'].pop(10),True)
 def test_fake_task_API(self):self.reject(lambda r:r['task_APIs'][0].update(actual_API_executed=False),True)
 def test_changed_original_image(self):self.reject(lambda r:r['image_after'].update(code_sha256='0'*64),True)
 def test_wrong_final_memory(self):self.reject(lambda r:self.memory(r['final'],e.MAIN+0xB28E,bytes(2)),True)
 def test_host_runtime_put_only_root_stack(self):
  # Execute the actual current native path while forbidding every host put
  # outside explicit root-argument stack setup after construction.
  ch,gh,_=e.helpers();live=e.platform.crt.Live(ch);gpu=e.platform.OverlayGPU(gh)
  try:
   f=e.OverlayMachine(e.parent.corpus()[0],live,gpu);old=f.put
   def put(p,*a):self.assertTrue(e.STACK<=p<e.STACK+0x20000);return old(p,*a)
   f.put=put;r=f.run();self.assertEqual(m.verify(dict(r,CRT_cleanup=live.close(),GPU_cleanup=gpu.close(),CRT_exit=live.exit_code,GPU_exit=gpu.process.returncode))['VM_PC'],52)
  finally:
   if not live.closed:live._terminate()
   if not gpu.closed:gpu._terminate()

if __name__=='__main__':unittest.main()
