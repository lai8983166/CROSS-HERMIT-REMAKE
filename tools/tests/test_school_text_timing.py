import json,struct,unittest
from tools.school_text_timing_catalog import *
from tools.school_text_timing_emulation import run_timing,record

class TextTimingTests(unittest.TestCase):
 def test_every_original_isolated_update_draw_and_readiness_matches(self):
  self.assertGreater(len(source_catalog()['code_inputs']),18)
  report=native_fixture();self.assertEqual(len(report['cases']),8)
  rules=json.loads((ROOT/'prototype/data/school_text_timing_rules.json').read_text('utf-8'))
  evidence=json.loads((ROOT/'prototype/data/school_text_timing_evidence.json').read_text('utf-8'))
  self.assertEqual(rules,source_catalog());self.assertNotIn('cases',rules)
  self.assertEqual(evidence['cases'],report['cases']);self.assertFalse(evidence['runtime_fixture'])
  for c in report['cases']:
   p=c['timing'];raw=bytes.fromhex(p['before_hex'])
   self.assertFalse(p['native_VM_continuation_executed']);self.assertFalse(p['GPU_executed'])
   for frame in p['updates']:
    for key,value in expected_update(raw,p['origin'],p['object_pointer']).items():self.assertEqual(value,frame[key],(c['name'],frame['update'],key))
    raw=bytes.fromhex(frame['after_hex'])

 def test_first_frame_activation_then_24_fades_and_next_threshold(self):
  p=run_timing([record()],26)
  self.assertFalse(p['initial_readiness']);self.assertEqual(p['updates'][0]['draws'],[])
  self.assertEqual(p['updates'][1]['draws'][0]['args'][4],10)
  self.assertEqual(p['updates'][24]['draws'][0]['args'][4],255);self.assertFalse(p['updates'][24]['readiness'])
  self.assertTrue(p['updates'][25]['readiness'])
  r=bytes.fromhex(p['updates'][12]['after_hex']);self.assertEqual(struct.unpack_from('<H',r,34)[0],1)
  self.assertFalse(p['updates'][12]['readiness'])

 def test_multiline_cadence_y_wrap_and_pending_state4(self):
  p=run_timing([record(delay=0),record()],26,[715,65530])
  self.assertEqual([d['args'][2] for d in p['updates'][1]['draws']],[65530,18]);self.assertTrue(p['updates'][-1]['readiness'])
  p=run_timing([record(mode=4)],2);self.assertFalse(p['updates'][-1]['readiness']);self.assertEqual(p['updates'][-1]['draws'],[])

 def test_malformed_records_update_caps_and_origin_refused(self):
  for records in ([],[record()]*11,[{**record(),'mode':0}],[{**record(),'fade_limit':0}],[{**record(),'fade_count':True}],['text']):
   with self.assertRaises(ValueError):run_timing(records,1)
  for count in (True,0,257):
   with self.assertRaises(ValueError):run_timing([record()],count)
  for origin in ([False,0],[-1,0],[0]):
   with self.assertRaises(ValueError):run_timing([record()],1,origin)

if __name__=='__main__':unittest.main()
