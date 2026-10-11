import hashlib, json, unittest
from copy import deepcopy
from tools.school_board_opening_catalog import *

class BoardSourceTests(unittest.TestCase):
 def test_complete_actual_bytes_updates_readiness_and_raw_drawings(self):
  for c in native_fixture()['cases']:
   p=c['board_opening'];expected=expected_board(p['inputs'],p['before'])
   for key,value in expected.items():self.assertEqual(value,p[key],(c['name'],key))
   self.assertEqual(p['before'][:3],p['after'][:3])

 def test_original_config_frame_and_script_inputs_are_independent(self):
  rules=source_catalog();self.assertEqual((rules['board_id'],rules['layer'],rules['animation_limit']),(4,7,45))
  self.assertEqual(len(rules['frame_pieces']['rows']),4);self.assertGreater(len(rules['code_inputs']),30)
  self.assertEqual(rules['operands'],[4,0xFFFFFFF,0xFFFFFFF])
  raw=SOURCE.read_bytes();at=int(rules['configuration']['va'],16)-BASE
  self.assertEqual(raw[at:at+38].hex(),rules['configuration']['hex'])
  p=native_fixture()['cases'][0]['board_opening'];expected=expected_board(p['inputs'],p['before'])
  altered=deepcopy(p);vm=next(r for r in altered['after'] if r['pointer']==VM);b=bytearray.fromhex(vm['hex']);b[NODE_OFFSET+6]=1;vm['hex']=b.hex()
  self.assertNotEqual(expected['after'],altered['after'])
  self.assertTrue(any(r['args'][2]>255 for r in p['presentation_first_update'] if r['va']=='0x4cbdb0'))

 def test_malformed_driver_and_active_input_states_are_rejected(self):
  p=native_fixture()['cases'][0]['board_opening']
  for key,value in (('script_pointer',True),('script_pointer',VM),('completed_updates',True),('completed_updates',46),('overlay_origin',[0]),('overlay_origin',[False,0]),('driver','full_world'),('pending_handler','0x4c5ea0')):
   inputs=deepcopy(p['inputs']);inputs[key]=value
   with self.assertRaises(ValueError):expected_board(inputs,p['before'])
  for offset,value in ((4,0),(0x1C,0),(0x20,1),(NODE_OFFSET,1),(OBJECT_OFFSET+22,1),(0x92E0,1)):
   before=deepcopy(p['before']);v=next(r for r in before if r['pointer']==VM);b=bytearray.fromhex(v['hex']);b[offset]=value;v['hex']=b.hex()
   with self.assertRaises(ValueError):expected_board(p['inputs'],before)
  for mutate in (lambda r:r.pop(),lambda r:r[0].update({'bytes':399}),lambda r:r[3].update({'hex':'bad'})):
   before=deepcopy(p['before']);mutate(before)
   with self.assertRaises(ValueError):expected_board(p['inputs'],before)

 def test_original_unsigned_interpolation_and_clamp_boundaries(self):
  self.assertEqual([interpolate(n,45,255) for n in (0,1,44,45,46)],[0,5,249,255,255])
  self.assertEqual([interpolate(n,45,204) for n in (0,1,44,45,46)],[0,4,199,204,204])
  self.assertEqual(interpolate(65535,65535,65535),65534)
  for args in ((0,0,255),(-1,45,255),(True,45,255),(0,65536,255)):
   with self.assertRaises(ValueError):interpolate(*args)

 def test_exported_rules_and_evidence_remain_separate(self):
  rules=json.loads((ROOT/'prototype/data/school_board_opening_rules.json').read_text('utf-8'))
  evidence=json.loads((ROOT/'prototype/data/school_board_opening_evidence.json').read_text('utf-8'))
  self.assertEqual(rules,source_catalog());self.assertNotIn('cases',rules)
  self.assertEqual(evidence['cases'],native_fixture()['cases']);self.assertFalse(evidence['runtime_fixture'])
  self.assertEqual(evidence['native_report_sha256'],EVIDENCE_SHA256)

if __name__=='__main__':unittest.main()
