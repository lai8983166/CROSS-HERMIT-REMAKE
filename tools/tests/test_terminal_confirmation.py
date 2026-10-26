"""Reject fabricated capture binding, panel transitions and next-font boundaries."""
import copy,gzip,json,os,struct,unittest
from types import SimpleNamespace
from tools import terminal_confirmation_emulation as e
from tools import terminal_confirmation_verification as v
REPORT=os.environ.get('TERMINAL_CONFIRMATION_REPORT','analysis/terminal-confirmation-source-v1-20261026.json.gz')
class TerminalConfirmationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=json.loads(gzip.decompress((e.ROOT/REPORT).read_bytes()));cls.rows=cls.report['cases']
 def reject(self,edit,check):
  row=dict(self.rows[0]);row['terminal_confirmation']=copy.deepcopy(row['terminal_confirmation']);edit(row)
  with self.assertRaises((ValueError,KeyError,IndexError,StopIteration)):check(row)
 def replay(self,r):return v.Replay(r).execute()
 def test_two_complete_independent_original_cases(self):
  self.assertEqual(self.report['source_contract'],e.source_contract())
  for r in self.rows:
   with self.subTest(name=r['input']['name']):self.assertEqual(v.verify_case(r)['VM_PC'],142)
 def test_runtime_rejects_nonoriginal_capture_before_memory_access(self):
  g=e.ConfirmationMachine.__new__(e.ConfirmationMachine);g.live_input=dict(name='neutral_running');g.confirm_bindings=[]
  with self.assertRaises(ValueError):g.captured(dict(label='fake',raw_device_hex='00'*256))
 def test_runtime_rejects_fourth_capture(self):
  g=e.ConfirmationMachine.__new__(e.ConfirmationMachine);g.live_input=dict(name='neutral_running');g.confirm_bindings=[{}, {}, {}]
  with self.assertRaises(ValueError):g.captured(dict(label='idle',raw_device_hex='00'*256))
 def test_source_guard_inherited(self):self.assertIs(e.ConfirmationMachine.source_code.__code__,e.parent.DialogueMachine.source_code.__code__)
 def test_runtime_host_and_code_guards(self):
  r=self.rows[0];g=e.ConfirmationMachine(r['input'],SimpleNamespace(hello=r['current_CRT_hello']),SimpleNamespace(hello=r['current_GPU_hello'],device=r['current_GPU_hello']['device']))
  try:
   for p in (e.VM+28,e.VM+32,e.KEYBOARD+0x4B9,e.NODE,e.OBJECT,e.TASK+0x190):
    with self.assertRaises(ValueError):g.put(p,0)
   g.put(e.STACK+0xF000,e.RETURN)
   with self.assertRaises(ValueError):g.source_code(g.uc,0x401000,1,None)
   with self.assertRaises(ValueError):g.write_hook(g.uc,0,0x5920A0,4,0,None)
   g.confirm_active=True;g.keyboard_fragment=True
   with self.assertRaises(ValueError):g.write_hook(g.uc,0,e.MAIN,4,0,None)
  finally:g.name_platform.close()
 def test_wrong_scene_capture(self):self.reject(lambda r:r['terminal_confirmation'].update(scene_capture=77),v.protocol)
 def test_missing_release(self):self.reject(lambda r:r['terminal_confirmation']['bindings'].pop(),v.protocol)
 def test_wrong_raw_platform_byte(self):self.reject(lambda r:r['terminal_confirmation']['bindings'][1]['capture'].update(raw_device_hex='00'*256),v.protocol)
 def test_derived_keyboard_byte(self):self.reject(lambda r:r['terminal_confirmation']['bindings'][1].update(after_hex='00'*0xA00),v.protocol)
 def test_wrong_raw_write_extent(self):self.reject(lambda r:r['terminal_confirmation']['bindings'][1]['only_device_output_written'].update(pointer=e.KEYBOARD+0x4B9),v.protocol)
 def test_wrong_keyboard_receiver(self):self.reject(lambda r:r['terminal_confirmation']['bindings'][1]['fragment'].update(receiver=e.KEYBOARD+4),v.protocol)
 def test_fake_pressed_boolean(self):self.reject(lambda r:r['terminal_confirmation']['bindings'][1].update(after_hex=r['terminal_confirmation']['bindings'][1]['after_hex'][:0x4B9*2]+'01'+r['terminal_confirmation']['bindings'][1]['after_hex'][0x4BA*2:]),v.protocol)
 def test_early_wait_clear(self):self.reject(lambda r:r['terminal_confirmation']['frames'][0]['after'].update(VM=r['terminal_confirmation']['confirmed']['state']['VM']),v.timing)
 def test_missing_no_input_frame(self):self.reject(lambda r:r['terminal_confirmation']['frames'].pop(0),v.timing)
 def test_missing_dispatch(self):self.reject(lambda r:r['terminal_confirmation']['commands'].pop(0),v.timing)
 def test_wrong_next_font_weight(self):self.reject(lambda r:r['terminal_confirmation']['pending_font']['args'].__setitem__(4,700),v.source)
 def test_next_font_executed(self):self.reject(lambda r:r['terminal_confirmation']['pending_font'].update(first_instruction_executed=True),v.source)
 def test_changed_current_readback(self):self.reject(lambda r:r['terminal_confirmation']['readbacks']['portrait'].update(hex='00'),v.protocol)
 def test_wrong_original_task_root(self):self.reject(lambda r:r['terminal_confirmation']['segments'][1]['root'].update(receiver=e.VM),self.replay)
 def test_wrong_keyboard_entry(self):self.reject(lambda r:r['terminal_confirmation']['segments'][0].update(entry=0x4113D6),self.replay)
 def test_early_root_stop(self):self.reject(lambda r:r['terminal_confirmation']['segments'][1].update(stop=0x40DB91),self.replay)
 def test_wrong_binding_CPU(self):self.reject(lambda r:r['terminal_confirmation']['segments'][0]['bound_CPU'].update(EAX=1),self.replay)
 def test_wrong_full_CPU(self):self.reject(lambda r:r['terminal_confirmation']['segments'][0]['CPU'].update(EAX=1),self.replay)
 def test_wrong_original_PC_digest(self):self.reject(lambda r:r['terminal_confirmation']['segments'][0]['local_after'].update(code_sha256='0'*64),self.replay)
 def test_wrong_original_write_digest(self):self.reject(lambda r:r['terminal_confirmation']['segments'][0]['local_after'].update(write_sha256='0'*64),self.replay)
 def test_wrong_whole_frame_memory(self):self.reject(lambda r:r['terminal_confirmation']['frames'][0]['capture']['memory'][0].update(sha256='0'*64),self.replay)
 def test_wrong_frame_CPU(self):self.reject(lambda r:r['terminal_confirmation']['frames'][0]['capture']['CPU'].update(EAX=1),self.replay)
 def test_wrong_complete_queue(self):self.reject(lambda r:r['terminal_confirmation']['frames'][0]['queue_after'].update(heads='00'),self.replay)
 def test_wrong_key_boundary_memory(self):self.reject(lambda r:r['terminal_confirmation']['bindings'][0]['after']['memory'][0].update(hex='00'),self.replay)
 def test_wrong_query_ABI(self):self.reject(lambda r:r['terminal_confirmation']['queries'][0].update(receiver=1),self.replay)
 def test_fake_task_API_mapping(self):self.reject(lambda r:r['terminal_confirmation']['leaves'][0]['call'].update(new_mappings=[dict(pointer=0x1000,bytes=4096)]),self.replay)
 def test_fake_task_API_result(self):self.reject(lambda r:r['terminal_confirmation']['leaves'][0]['call'].update(result=1),self.replay)
 def test_wrong_task_API_output(self):self.reject(lambda r:r['terminal_confirmation']['leaves'][0]['call'].update(value=1),self.replay)
 def test_wrong_original_store(self):self.reject(lambda r:r['terminal_confirmation']['writes'][0].update(value=0x1234),self.replay)
 def test_nonzero_repeat_counter_model(self):
  before=bytearray(0xA00);before[12+57]=128;before[0x480+57]=128;struct.pack_into('<4I',before,0x880,3,2,3,0);out=v.predict_keyboard(bytes(before));self.assertEqual(out[0x680+57],128);self.assertEqual(struct.unpack_from('<2I',out,0x888),(1,1))
 def test_low_device_bits_do_not_press(self):
  before=bytearray(0xA00);before[12+57]=127;self.assertEqual(v.predict_keyboard(bytes(before))[0x4B9],0)
 def test_wrong_raw_native_readback_owner(self):
  r=dict(self.rows[0]);r['GPU_trace']=copy.deepcopy(r['GPU_trace']);r['GPU_trace'][26]['request']['pointer']=1
  with self.assertRaises(ValueError):v.protocol(r)
 def test_wrong_raw_native_receipt_order(self):
  r=dict(self.rows[0]);r['GPU_trace']=copy.deepcopy(r['GPU_trace']);r['GPU_trace'][26]['reply']['id']=1
  with self.assertRaises(ValueError):v.protocol(r)
 def test_changed_raw_supplemental_destructor_CPU(self):
  r=dict(self.rows[0]);r['dialogue_cleanup']=copy.deepcopy(r['dialogue_cleanup']);r['dialogue_cleanup']['CPU']['EAX']=1
  replay=v.Replay(r);replay.execute();replay.d=dict(r['terminal_dialogue'],final=r['terminal_confirmation']['final']);replay.cfg=v.previous.geometry(r['terminal_dialogue']['raster']['measured'])
  with self.assertRaises(ValueError):v.previous.Replay.cleanup(replay)

if __name__=='__main__':unittest.main()
