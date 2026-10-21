"""Real x86 key-query ABI, stable waits and honest native input evidence."""
import copy,gzip,json,struct,tempfile,unittest
from pathlib import Path
from tools import school_native_dialogue as producer
from tools import school_native_dialogue_verification as proof

class SourceTests(unittest.TestCase):
 def test_original_contract(self):proof.source_contract(producer.input_source_contract())
 def test_original_all_key_modes(self):
  query=proof.OriginalKeyQuery()
  for mode,offset in enumerate((0x480,0x580,0x680,0x380,0x780)):
   for key in range(256):
    body=bytearray(0xa00);body[offset+key]=(0,0x7f,0x80,0xff)[key%4]
    self.assertEqual(query.query(bytes(body),key,mode),int(key%4>=2),(mode,key))
 def test_key_masks_to_byte(self):
  b=bytearray(0xa00);b[0x4b9]=0x80;self.assertEqual(proof.OriginalKeyQuery().query(bytes(b),0x10039,0),1)
 def test_invalid_query_mode_returns_zero(self):self.assertEqual(proof.OriginalKeyQuery().query(bytes([255])*0xa00,57,5),0)
 def test_reject_short_input_before_cpu(self):
  with self.assertRaises(ValueError):proof.OriginalKeyQuery().query(bytes(10))
 def test_original_complete_post_device_update(self):
  r=proof.keyboard_experiment();self.assertEqual(len(r['cases']),9);self.assertTrue(all(c['independent_full_object_equal'] for c in r['cases']))
 def test_keyboard_model_preserves_unrelated_bytes(self):
  b=bytes(0xa00);self.assertEqual(proof.keyboard_update(b),proof.predict_keyboard(b))
 def test_source_experiment_not_native_input(self):
  p=proof.ROOT/'analysis/school-native-dialogue-keyboard-source-v1-20261021.json';r=json.loads(p.read_text());self.assertFalse(r['system_input_transition_verified'])
  for case in r['cases']:
   before=bytes.fromhex(case['before_hex']);self.assertEqual(proof.predict_keyboard(before).hex(),case['after_hex'])
 def test_stable_wait_gate_and_press_release(self):
  with tempfile.TemporaryDirectory() as tmp:
   notice=Path(tmp)/'ready.json';b=producer.DialogueBoundary(notice);h=bytearray(0x200);h[0x43]=h[0x59]=1;h[0x44]=2;v=bytearray(128);v[4]=1;struct.pack_into('<IHH',v,28,1164,1,51)
   def step(index,now,key=0,pc=1164):
    body=bytearray(0xa00);body[0x4b9]=key;struct.pack_into('<I',v,28,pc);return b.observe(h,v,dict(index=index,elapsed=now,input=dict(game=1,hex=body.hex())),now)
   self.assertEqual(step(0,0),(True,False));self.assertFalse(notice.exists());step(1,1);self.assertTrue(notice.exists());self.assertEqual(step(2,1.1,128),(True,False));self.assertEqual(step(3,1.2,0,1180),(True,False));self.assertEqual(step(4,1.8,0,1184),(True,True));self.assertEqual(b.summary(),dict(wait_PC=1164,no_input_start=0,ready_index=1,press_index=2,release_index=3,advanced_index=3))
 def test_non_confirmation_does_not_publish_ready(self):
  with tempfile.TemporaryDirectory() as tmp:
   b=producer.DialogueBoundary(Path(tmp)/'ready.json');h=bytearray(512);v=bytearray(128);h[0x43]=h[0x59]=1;h[0x44]=2;v[4]=1;struct.pack_into('<IHH',v,28,80,4,117);row=dict(index=0,elapsed=10,input=dict(game=1,hex=bytes(0xa00).hex()))
   self.assertEqual(b.observe(h,v,row,10),(True,False));self.assertIsNone(b.ready_index)

class EvidenceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=json.loads(gzip.decompress((proof.ROOT/'analysis/school-native-dialogue-76-v6-20261021.json.gz').read_bytes()))
 def test_real_no_input_native_wait(self):
  r=proof.verify_report(self.report);self.assertEqual(r['no_input_wait']['PC'],1164);self.assertFalse(r['system_input_transition_verified'])
 def test_second_native_scene_wait(self):
  r=json.loads(gzip.decompress((proof.ROOT/'analysis/school-native-dialogue-77-v1-20261021.json.gz').read_bytes()));result=proof.verify_report(r);self.assertEqual(result['no_input_wait']['PC'],152);self.assertFalse(result['system_input_transition_verified'])
 def test_cannot_accept_as_system_input(self):
  with self.assertRaises(ValueError):proof.verify_report(self.report,True)
 def reject(self,edit):
  r=copy.deepcopy(self.report);edit(r)
  with self.assertRaises((ValueError,KeyError)):proof.verify_report(r)
 def test_reject_fake_live_input_code(self):self.reject(lambda r:r['case']['probe']['source_after']['input_code'][0].update(sha256='0'*64))
 def test_reject_human_physical_claim(self):self.reject(lambda r:r.update(human_physical_input_claimed=True))
 def test_reject_short_owner(self):self.reject(lambda r:r['case']['probe']['samples'][0]['input'].update(hex='00'))
 def test_reject_unrelated_input_owner(self):self.reject(lambda r:r['case']['probe']['samples'][0]['input'].update(pointer=1))
 def test_reject_invented_input_event(self):self.reject(lambda r:r['case']['probe']['dialogue_boundary'].update(press_index=1005))
 def test_reject_wrong_confirmation_PC(self):self.reject(lambda r:r['case']['probe']['dialogue_boundary'].update(wait_PC=1168))
 def test_reject_zero_wait_duration(self):self.reject(lambda r:r['case']['probe']['dialogue_boundary'].update(no_input_start=1009))
 def test_reject_fake_pressed_no_input(self):
  def edit(r):
   p=r['case']['probe'];s=p['samples'][p['dialogue_boundary']['ready_index']];b=bytearray.fromhex(s['input']['hex']);b[0x4b9]=128;s['input']['hex']=b.hex()
  self.reject(edit)
 def test_reject_changed_original_function_operand(self):self.reject(lambda r:r['input_source_contract']['instructions'][0].update(operands='0x4ce8f0'))
 def test_reject_extra_existing_object_write(self):self.reject(lambda r:r['case']['probe']['writes'].append(dict(pointer=0x7d7c28,bytes=4,sha256='0'*64)))
 def test_reject_fake_wait_phase(self):
  def edit(r):
   p=r['case']['probe'];s=p['samples'][p['dialogue_boundary']['ready_index']];b=bytearray.fromhex(s['VM_hex']);struct.pack_into('<H',b,32,0);s['VM_hex']=b.hex()
  self.reject(edit)

if __name__=='__main__':unittest.main()
