"""Actual six-case independent replay plus rejection of altered source evidence."""
import copy,gzip,json,unittest
from tools import school_retained_keyboard_verification as proof


class RetainedKeyboardTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.report=json.loads(gzip.decompress((proof.ROOT/'analysis/school-retained-keyboard-v1-20261022.json.gz').read_bytes()));cls.contract=proof.inputs()
 def test_00_all_six_source_connections(self):
  checked=proof.verify(self.report);self.assertTrue(checked['six_retained_keyboard_connections_verified']);self.assertEqual(len(checked['cases']),6)
  for c in checked['cases']:
   self.assertEqual(c['complete_original_tasks'],23);self.assertEqual(c['source_keyboard_updates'],3);self.assertEqual(c['independent_VM_roots'],0);self.assertFalse(c['R3_complete'])
 def reject_protocol(self,edit):
  c=copy.deepcopy(self.report['cases'][0]);edit(c)
  with self.assertRaises((ValueError,KeyError)):proof.protocol(c,self.contract)
 def reject_replay(self,edit):
  c=copy.deepcopy(self.report['cases'][0]);edit(c)
  with self.assertRaises((ValueError,KeyError,RuntimeError)):proof.verify_case(c,self.contract)
 def test_foreign_capture(self):self.reject_protocol(lambda c:c['stream'].update(report_sha256='0'*64))
 def test_forged_current_key(self):self.reject_protocol(lambda c:c['bindings'][1].update(after_hex=c['bindings'][1]['before_hex']))
 def test_raw_binding_changes_derived_field(self):
  def edit(c):
   b=bytearray.fromhex(c['bindings'][0]['bound_hex']);b[0x4b9]=128;c['bindings'][0]['bound_hex']=b.hex()
  self.reject_protocol(edit)
 def test_binding_outside_raw_output(self):self.reject_protocol(lambda c:c['bindings'][1]['only_device_output_written'].update(pointer=proof.VM+28))
 def test_independent_VM_root(self):self.reject_protocol(lambda c:c['steps'][1]['root'].update(va=0x4ce8f0))
 def test_missing_task_interval(self):self.reject_protocol(lambda c:c['steps'].pop(2))
 def test_false_no_input_release(self):self.reject_protocol(lambda c:c['no_input_controls'][0].update(wait=0))
 def test_false_confirmation(self):self.reject_protocol(lambda c:c['confirmation'].update(wait=1))
 def test_claimed_next_handler_execution(self):self.reject_protocol(lambda c:c['next_handler'].update(first_instruction_executed=True))
 def test_wrong_source_instruction_digest(self):self.reject_replay(lambda c:c['steps'][0].update(instruction_sha256='0'*64))
 def test_wrong_complete_write_digest(self):self.reject_replay(lambda c:c['steps'][0].update(write_sha256='0'*64))
 def test_wrong_source_CPU(self):self.reject_replay(lambda c:c['steps'][0]['cpu'].update(EAX=c['steps'][0]['cpu']['EAX']^1))
 def test_wrong_final_full_memory(self):self.reject_replay(lambda c:c['final_memory'][0].update(sha256='0'*64))
 def test_wrong_architectural_CPU(self):self.reject_replay(lambda c:c['final_architectural_cpu'].update(MXCSR=c['final_architectural_cpu']['MXCSR']^1))
 def test_wrong_natural_next_stack(self):self.reject_replay(lambda c:c['next_handler'].update(args=[0,1,1]))
 def test_fake_recorded_platform_result(self):
  def edit(c):
   s=next(s for s in c['steps'] if s['platform_replays']);s['platform_replays'][0]['result']=1
  self.reject_replay(edit)
 def test_whole_R3_overclaim(self):
  r=copy.deepcopy(self.report);r['R3_complete']=True
  with self.assertRaisesRegex(ValueError,'honest offline scope'):proof.verify(r)


if __name__=='__main__':unittest.main()
