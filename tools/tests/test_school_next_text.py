import hashlib, json, struct, unittest
from copy import deepcopy
from tools.school_next_text_catalog import *


class NextTextTests(unittest.TestCase):
 def test_three_actual_captures_match_complete_independent_source(self):
  data=native_fixture()
  self.assertEqual(len(data['cases']),3)
  for case in data['cases']:
   self.assertEqual(case['provenance']['helper_sha256'],data['bridge_build']['helper_sha256'])
   self.assertEqual(case['provenance']['complete_parent_stages'],8)
   self.assertTrue(case['provenance']['complete_parent_stages_equal'])
   result=compare_case(case)
   self.assertEqual(result['complete_regions_compared'],8)
   self.assertEqual(result['pending_stack_arguments'],14)
   self.assertEqual(result['actual_texture_bytes'],16384)
   self.assertGreater(result['retained_bytes'],120000000)
   p=case['next_text'];vm=bytes.fromhex(next(r['hex'] for r in p['after'] if r['pointer']==VM))
   self.assertEqual(len(p['first_readiness']['CPU_registers_sha256']),64)
   self.assertEqual(p['first_readiness']['CPU_register_count'],51)
   self.assertEqual(struct.unpack_from('<I',vm,0x1C)[0],238)
   self.assertEqual(struct.unpack_from('<H',vm,OBJECT_OFFSET+22)[0],1)
   self.assertEqual(struct.unpack_from('<3H',vm,OBJECT_OFFSET+24),(3,0,24))
   self.assertEqual(struct.unpack_from('<3H',vm,OBJECT_OFFSET+0x110+24),(2,0,24))
   self.assertFalse(p['second_font_executed']);self.assertFalse(p['first_fade_completed'])

 def test_consecutive_commands_are_not_a_wait_for_first_fade(self):
  rules=source_catalog()
  self.assertEqual([r['opcode'] for r in rules['commands']],[17,17])
  self.assertEqual([r['text_index'] for r in rules['commands']],[0,1])
  self.assertEqual([r['pc'] for r in rules['commands']],[232,238])
  self.assertGreaterEqual(len(rules['code_inputs']),12)
  self.assertEqual(rules['second_text']['offset'],1012)
  self.assertEqual(len(split_original(bytes.fromhex(rules['second_text']['hex']))),1)

 def test_unsupported_parent_binding_counter_and_region_shape_refused(self):
  p=native_fixture()['cases'][0]['next_text']
  for key,value in (('script_pointer',True),('script_pointer',VM),('font_api',1),('font_api',True),('driver','delayed first fade')):
   inputs=deepcopy(p['inputs']);inputs[key]=value
   with self.assertRaises(ValueError):expected_next(inputs,p['before'])
  for offset,value in ((4,0),(0x1C,244),(0x20,1),(0x1CC,0),(OBJECT_OFFSET+22,2),(OBJECT_OFFSET+24,1),(OBJECT_OFFSET+26,24),(NODE_OFFSET+2,3)):
   before=deepcopy(p['before']);region=next(r for r in before if r['pointer']==VM);b=bytearray.fromhex(region['hex']);b[offset]=value;region['hex']=b.hex()
   with self.assertRaises(ValueError):expected_next(p['inputs'],before)
  for change in (lambda r:r.pop(),lambda r:r[0].update({'bytes':399}),lambda r:r[3].update({'hex':'bad'})):
   before=deepcopy(p['before']);change(before)
   with self.assertRaises(ValueError):expected_next(p['inputs'],before)

 def test_first_pixels_false_completion_and_extra_row_writes_detected(self):
  original=native_fixture()['cases'][0]
  c=deepcopy(original);p=c['next_text'];raw=bytearray.fromhex(p['first_actual_readback']['hex']);raw[0]^=1;p['first_actual_readback']['hex']=raw.hex()
  with self.assertRaises(ValueError):compare_case(c)
  for key in ('second_font_executed','second_texture_created','first_fade_completed','GPU_draw_or_present_executed','waves_executed'):
   c=deepcopy(original);c['next_text'][key]=True
   with self.assertRaises(ValueError):compare_case(c)
  c=deepcopy(original);p=c['next_text'];r=next(r for r in p['after'] if r['pointer']==VM);b=bytearray.fromhex(r['hex']);b[OBJECT_OFFSET+0x110+38]^=1;r['hex']=b.hex()
  with self.assertRaises(ValueError):compare_case(c)
  c=deepcopy(original);c['next_text']['first_readiness']['original_VM_called_predicate']=True
  with self.assertRaises(ValueError):compare_case(c)


if __name__=='__main__':unittest.main()
