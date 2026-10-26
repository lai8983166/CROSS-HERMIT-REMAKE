"""Reject fabricated terminal dialogue source, pixels, ABI or task progress."""
import copy,gzip,json,struct,unittest
from types import SimpleNamespace
from tools import terminal_dialogue_emulation as e
from tools import terminal_dialogue_verification as v

REPORT='analysis/terminal-dialogue-source-v3-20261026.json.gz'

class TerminalDialogueTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.report=json.loads(gzip.decompress((e.ROOT/REPORT).read_bytes()));cls.rows=cls.report['cases'];cls.reference,cls.geometry,_=v.pixels(cls.rows[0])
 def reject(self,edit,check):
  r=copy.deepcopy(self.rows[0]);edit(r)
  with self.assertRaises((ValueError,KeyError,IndexError,StopIteration)):check(r)
 def replay(self,r):return v.Replay(r,self.reference,self.geometry).execute()
 def vm(self,r,index,offset,value,fmt='H'):
  s=r['terminal_dialogue']['frames'][index]['after'];b=bytearray.fromhex(s['VM']);struct.pack_into('<'+fmt,b,offset,value);s['VM']=b.hex()
 def test_two_full_original_source_contracts(self):
  self.assertEqual(self.report['source_contract'],e.source_contract())
  self.assertEqual([r['input'] for r in self.rows],e.parent.overlay.parent.corpus())
  for r in self.rows:
   with self.subTest(name=r['input']['name']):
    checked=v.verify_case(r);self.assertEqual((checked['VM_PC'],checked['VM_wait']),(118,1))
 def test_two_distinct_original_sentences(self):self.assertNotEqual(v.source(self.rows[0])[0],v.source(self.rows[1])[0])
 def test_original_ANSI_punctuation_may_be_blank(self):
  self.assertEqual(v.source(self.rows[0])[0],bytes.fromhex('a14ba14ba14ba14b'));self.assertEqual(self.reference['ACP'],936);self.assertEqual(self.reference['nonzero_bytes'],0)
 def test_original_instruction_guard_is_inherited(self):self.assertIs(e.DialogueMachine.source_code.__code__,e.parent.PortraitMachine.source_code.__code__)
 def test_runtime_host_and_source_guards(self):
  r=self.rows[0];g=e.DialogueMachine(e.parent.overlay.parent.corpus()[0],SimpleNamespace(hello=r['current_CRT_hello']),SimpleNamespace(hello=r['current_GPU_hello'],device=r['current_GPU_hello']['device']))
  try:
   for p in (e.VM+28,e.VM+0x20,e.OBJECT,e.TEXTURE,e.MAIN+0xB208):
    with self.assertRaises(ValueError):g.put(p,0)
   g.put(e.STACK+0xF000,e.RETURN)
   with self.assertRaises(ValueError):g.source_code(g.uc,0x401000,1,None)
   with self.assertRaises(ValueError):g.write_hook(g.uc,0,0x5920A0,4,0,None)
  finally:g.name_platform.close()
 def test_wrong_script_command_pointer(self):self.reject(lambda r:r['terminal_dialogue']['commands'][0].update(source_pointer=0),v.source)
 def test_wrong_script_selection(self):self.reject(lambda r:r['terminal_dialogue']['commands'][0].update(PC=104),v.source)
 def test_wrong_font_weight(self):self.reject(lambda r:r['terminal_dialogue']['pending_font']['args'].__setitem__(4,700),v.source)
 def test_font_entry_already_executed(self):self.reject(lambda r:r['terminal_dialogue']['pending_font'].update(first_instruction_executed=True),v.source)
 def test_font_CPU_changed(self):self.reject(lambda r:r['terminal_dialogue']['pending_font']['CPU'].update(EAX=0x12345678),v.source)
 def test_missing_shadow_stage(self):self.reject(lambda r:r['terminal_dialogue']['raster']['stages'].pop(1),v.pixels)
 def test_wrong_shadow_pixels(self):self.reject(lambda r:r['terminal_dialogue']['raster']['stages'][1].update(hex='00'),v.pixels)
 def test_wrong_final_raster(self):self.reject(lambda r:r['terminal_dialogue']['raster'].update(raster_hex='00'),v.pixels)
 def test_wrong_ANSI_measurement(self):self.reject(lambda r:r['terminal_dialogue']['raster']['measured'].__setitem__(0,1),v.pixels)
 def test_missing_conversion_band(self):self.reject(lambda r:r['terminal_dialogue']['conversions'].pop(),v.pixels)
 def test_wrong_conversion_origin(self):self.reject(lambda r:r['terminal_dialogue']['conversions'][0]['point'].__setitem__(0,1),v.pixels)
 def test_nonzero_new_lock(self):self.reject(lambda r:r['terminal_dialogue']['lock'].update(hex='ff'),v.pixels)
 def test_wrong_converted_pixels(self):self.reject(lambda r:r['terminal_dialogue'].update(upload_hex='00'),v.pixels)
 def test_wrong_native_readback(self):self.reject(lambda r:r['terminal_dialogue']['readback'].update(hex='00'),v.pixels)
 def test_changed_retained_portrait(self):self.reject(lambda r:r['terminal_dialogue']['portrait_readback'].update(hex='00'),v.pixels)
 def test_changed_retained_name(self):self.reject(lambda r:r['terminal_dialogue']['name_readback'].update(hex='00'),v.pixels)
 def test_changed_retained_GYBC(self):self.reject(lambda r:r['terminal_dialogue']['GYBC_readback'].update(hex='00'),v.pixels)
 def test_wrong_native_protocol_order(self):self.reject(lambda r:r['GPU_trace'][18]['reply'].update(id=999),v.native)
 def test_fake_GPU_receipt(self):self.reject(lambda r:r['terminal_dialogue']['GPU_APIs'][0].update(actual_API_executed=False),v.native)
 def test_wrong_native_texture_identity(self):self.reject(lambda r:r['GPU_trace'][20]['request'].update(pointer=1),v.native)
 def test_missing_original_release(self):self.reject(lambda r:r['dialogue_cleanup']['GPU_APIs'].pop(),v.native)
 def test_helper_fallback_release(self):self.reject(lambda r:r['GPU_cleanup'].update(texture_releases=[1]),v.native)
 def test_wrong_native_GDI_argument(self):self.reject(lambda r:r['terminal_dialogue']['GDI_trace'][1]['native_args'].__setitem__(0,0),v.native)
 def test_fake_GDI_receipt(self):self.reject(lambda r:r['terminal_dialogue']['calls'][0].update(actual_API_executed=False),v.native)
 def test_foreign_measurement_DC(self):self.reject(lambda r:r['terminal_dialogue']['GDI_handle_projection'][0].update(guest=1),v.native)
 def test_missing_actual_task_query(self):self.reject(lambda r:r['task_APIs'].pop(),v.native)
 def test_unclassified_original_raw_CRT_operation(self):self.reject(lambda r:r['CRT_APIs'][0].update(wire_end=0),lambda r:v.previous.native(v.prefix_view(r)))
 def test_early_configuration_advance(self):self.reject(lambda r:self.vm(r,0,28,110,'I'),v.timing)
 def test_early_text_fade(self):self.reject(lambda r:self.vm(r,2,0x430+5*0xAB8+26,99),v.timing)
 def test_early_confirmation_clear(self):self.reject(lambda r:self.vm(r,-1,0x20,0),v.timing)
 def test_next_opcode_executed(self):self.reject(lambda r:self.vm(r,-1,28,134,'I'),v.timing)
 def test_missing_no_input_hold(self):self.reject(lambda r:r['terminal_dialogue']['frames'].pop(),v.timing)
 def test_wrong_complete_task_root(self):self.reject(lambda r:r['terminal_dialogue']['segments'][3]['root'].update(receiver=e.VM),self.replay)
 def test_changed_original_PC_digest(self):self.reject(lambda r:r['terminal_dialogue']['segments'][0]['local_after'].update(code_sha256='0'*64),self.replay)
 def test_changed_original_write_digest(self):self.reject(lambda r:r['terminal_dialogue']['segments'][0]['local_after'].update(write_sha256='0'*64),self.replay)
 def test_changed_whole_queue(self):self.reject(lambda r:r['terminal_dialogue']['frames'][0]['queue_after'].update(heads='00'),self.replay)
 def test_changed_full_frame_CPU(self):self.reject(lambda r:r['terminal_dialogue']['frames'][0]['capture']['CPU'].update(EAX=0x12345678),self.replay)
 def test_changed_query_observation(self):self.reject(lambda r:r['terminal_dialogue']['queries'][0].update(receiver=0),self.replay)
 def test_changed_conversion_stack(self):self.reject(lambda r:r['terminal_dialogue']['conversions'][0]['args'].__setitem__(0,0),self.replay)
 def test_changed_source_API_stack(self):self.reject(lambda r:r['terminal_dialogue']['leaves'][0]['call']['args'].__setitem__(0,1),self.replay)
 def test_changed_supplemental_destructor_CPU(self):self.reject(lambda r:r['dialogue_cleanup']['CPU'].update(EAX=0x12345678),self.replay)
 def test_changed_destroyed_record(self):self.reject(lambda r:r['dialogue_cleanup'].update(record_hex='00'),self.replay)

if __name__=='__main__':unittest.main()
