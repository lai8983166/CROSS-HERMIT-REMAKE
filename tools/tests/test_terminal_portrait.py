"""Reject fabricated terminal portrait loading, pixels, task progress or lifetime."""
import copy,gzip,json,struct,unittest
from types import SimpleNamespace
from tools import terminal_portrait_emulation as e
from tools import terminal_portrait_verification as v
REPORT='analysis/terminal-portrait-source-v6-20261026.json.gz'
class TerminalPortraitTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=json.loads(gzip.decompress((e.ROOT/REPORT).read_bytes()));cls.rows=cls.report['cases']
 def reject(self,edit,check=v.verify_case):
  r=copy.deepcopy(self.rows[0]);edit(r)
  with self.assertRaises((ValueError,KeyError,IndexError,StopIteration)):check(r)
 def vm(self,r,index,off,val,fmt='H'):
  s=r['terminal_portrait']['frames'][index]['after'];b=bytearray.fromhex(s['VM']);struct.pack_into('<'+fmt,b,off,val);s['VM']=b.hex()
 def test_two_full_source_contracts(self):
  self.assertEqual(self.report['source_contract'],e.source_contract())
  for row in self.rows:
   with self.subTest(name=row['input']['name']):self.assertEqual(v.verify_case(row)['VM_PC'],96)
 def test_distinct_original_assets(self):
  raw=[v.pixels(r) for r in self.rows];self.assertNotEqual(raw[0],raw[1]);self.assertEqual([r['terminal_portrait']['role'] for r in self.rows],[2,1])
 def test_original_guard_and_root_algorithms(self):self.assertIs(e.PortraitMachine.source_code.__code__,e.parent.NameMachine.source_code.__code__)
 def test_runtime_host_and_source_guards(self):
  r=self.rows[0];g=e.PortraitMachine(e.overlay.parent.corpus()[0],SimpleNamespace(hello=r['current_CRT_hello']),SimpleNamespace(hello=r['current_GPU_hello'],device=r['current_GPU_hello']['device']))
  try:
   for p in (e.VM+28,e.VM+0x20,e.NODE,e.MAIN+0x844+32*8):
    with self.assertRaises(ValueError):g.put(p,0)
   g.put(e.STACK+0xF000,e.RETURN)
   with self.assertRaises(ValueError):g.source_code(g.uc,0x401000,1,None)
   with self.assertRaises(ValueError):g.write_hook(g.uc,0,0x5920A0,4,0,None)
  finally:g.name_platform.close()
 def test_wrong_asset_identity(self):self.reject(lambda r:r['terminal_portrait']['source'].update(image_sha256='0'*64),v.pixels)
 def test_wrong_portrait_path(self):self.reject(lambda r:r['terminal_portrait'].update(path='data/adv/bin/sc009.bin'),v.pixels)
 def test_incomplete_original_file(self):self.reject(lambda r:r['terminal_portrait']['constructed'].update(file_hex='00'),v.pixels)
 def test_missing_pixel_row(self):self.reject(lambda r:r['terminal_portrait']['copy_rows'].pop(),v.pixels)
 def test_wrong_memcpy_extent(self):self.reject(lambda r:r['terminal_portrait']['copy_rows'][0]['args'].__setitem__(2,256),v.pixels)
 def test_wrong_memcpy_source(self):self.reject(lambda r:r['terminal_portrait']['copy_rows'][0]['args'].__setitem__(1,0),v.pixels)
 def test_wrong_pixel_conversion(self):self.reject(lambda r:r['terminal_portrait'].update(upload_hex='00'),v.pixels)
 def test_wrong_native_readback(self):self.reject(lambda r:r['terminal_portrait']['readback'].update(hex='00'),v.pixels)
 def test_prior_name_changed(self):self.reject(lambda r:r['terminal_portrait']['name_readback'].update(hex='00'),v.pixels)
 def test_prior_GYBC_changed(self):self.reject(lambda r:r['terminal_portrait']['GYBC_readback'].update(hex='00'),v.pixels)
 def test_wrong_native_sequence(self):self.reject(lambda r:r['GPU_trace'][11]['reply'].update(id=999),v.native)
 def test_fake_GPU_receipt(self):self.reject(lambda r:r['terminal_portrait']['GPU_APIs'][0].update(actual_API_executed=False),v.native)
 def test_missing_original_GPU_release(self):self.reject(lambda r:r['portrait_cleanup']['GPU_APIs'].pop(),v.native)
 def test_helper_fallback_release(self):self.reject(lambda r:r['GPU_cleanup'].update(texture_releases=[1]),v.native)
 def test_wrong_native_buffer_readback(self):self.reject(lambda r:r['terminal_portrait']['constructed']['native_allocation_readbacks'][0]['result'].update(hex='00'),v.native)
 def test_unclassified_CRT_operation(self):self.reject(lambda r:r['CRT_APIs'][0].update(wire_end=0),v.native)
 def test_lost_bank_clear(self):self.reject(lambda r:r['portrait_cleanup'].update(bank_hex='00'*4),v.native)
 def test_shortened_readiness(self):self.reject(lambda r:r['terminal_portrait']['frames'].pop(),v.animation)
 def test_early_fade_finish(self):self.reject(lambda r:self.vm(r,74,e.NODE-e.VM+2,2),v.animation)
 def test_wrong_delay_counter(self):self.reject(lambda r:self.vm(r,0,e.NODE-e.VM+18,1),v.animation)
 def test_early_background_finish(self):self.reject(lambda r:self.vm(r,59,e.NODE-e.VM+34,2),v.animation)
 def test_early_wait_clear(self):self.reject(lambda r:self.vm(r,75,0x20,0),v.animation)
 def test_next_script_command_executed(self):self.reject(lambda r:self.vm(r,76,28,104,'I'),v.animation)
 def test_original_CPU_changed(self):self.reject(lambda r:r['terminal_portrait']['final']['CPU'].update(EAX=0x1234))
 def test_original_PC_digest_changed(self):self.reject(lambda r:r['terminal_portrait']['segments'][0]['local_after'].update(code_sha256='0'*64))
 def test_original_write_digest_changed(self):self.reject(lambda r:r['terminal_portrait']['segments'][0]['local_after'].update(write_sha256='0'*64))
 def test_original_IAT_contract_changed(self):self.reject(lambda r:r['terminal_portrait']['leaves'][0]['call'].update(import_slot=0x5920A0))
 def test_source_file_size_changed(self):
  def edit(r):next(x['call'] for x in r['terminal_portrait']['leaves'] if x['kind']=='CRT' and x['call']['name']=='GetFileSize')['value']=4
  self.reject(edit)
 def test_wrong_full_task_root(self):self.reject(lambda r:r['terminal_portrait']['segments'][6]['root'].update(receiver=e.VM))
 def test_wrong_full_queue(self):self.reject(lambda r:r['terminal_portrait']['frames'][0]['queue_after'].update(heads='00'))
 def test_wrong_seh(self):self.reject(lambda r:r['terminal_portrait']['completion']['state'].update(SEH='ffffffff'))
 def test_native_whitelist_and_stale_handle_rejection(self):
  ch,gh,b=e.helpers('terminal-portrait-test');live=e.overlay.platform.crt.Live(ch)
  try:
   flags=dict(access=0x80000000,share=1,security=0,disposition=3,attributes=1,template=0)
   with self.assertRaises(ValueError):live.request('open',path='data/adv/bin/sc003.bin',**flags)
   path='data'+chr(92)+'adv'+chr(92)+'bin'+chr(92)+'sc002.bin';h=live.request('open',path=path,**flags)['handle'];self.assertEqual(live.request('size',handle=h,high=0)['value'],262168);live.request('file_close',handle=h)
   with self.assertRaises(ValueError):live.request('size',handle=h,high=0)
  finally:self.assertTrue(live.close()['all_owned_resources_released'])
if __name__=='__main__':unittest.main()
