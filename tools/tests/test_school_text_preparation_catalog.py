import json, struct, unittest
from copy import deepcopy
from tools.school_text_preparation_catalog import *

class TextSourceTests(unittest.TestCase):
 def test_complete_actual_memory_stack_and_raw_terminal_arguments(self):
  for c in native_fixture()['cases']:
   p=c['text_preparation']
   for key,value in expected_preparation(p['inputs'],p['before']).items():self.assertEqual(value,p[key],(c['name'],key))
   self.assertEqual(p['before'][:3],p['after'][:3])
   self.assertTrue(any(r['args'][2]>255 for r in p['presentation'] if r['va']=='0x4cbdb0'))

 def test_source_text_table_order_encoding_and_bad_spans(self):
  rules=source_catalog();self.assertGreater(len(rules['code_inputs']),30)
  self.assertEqual(rules['face']['decoded_cp932'],'ＭＳ ゴシック')
  self.assertEqual([r['text_index'] for r in rules['text_sequence']],list(range(10)))
  self.assertEqual(rules['entries'][9]['text'],'那麼，就開始吧。')
  script,layout=script_layout()
  for at,raw in ((948,struct.pack('<I',9)),(952,struct.pack('<I',(20<<20)|65535)),(1009,b'\0'),(992,b'\xff\xff'),(688,struct.pack('<H',10))):
   changed=bytearray(script);changed[at:at+len(raw)]=raw
   with self.assertRaises(ValueError):decode_opening(bytes(changed),layout)
  with self.assertRaises(ValueError):decode_opening(script,{**layout,'selected_span':[432,1000]})

 def test_native_pair_copy_and_supported_line_separators(self):
  raw='瑟希莉絲'.encode('cp950');self.assertEqual(split_original(raw+b'\\n'+raw),[raw,raw])
  self.assertEqual(split_original(b'\\n'),[b'',b'']);self.assertEqual(split_original(b'AB'*127),[b'AB'*127])
  for malformed in (b'A',b'\0\0',b'AB'*128,b'\\x',b'\\n'*10,'text'):
   with self.assertRaises(ValueError):split_original(malformed)

 def test_unsupported_driver_and_memory_shapes_refused(self):
  p=native_fixture()['cases'][0]['text_preparation']
  for key,value in (('script_pointer',True),('script_pointer',VM),('completed_updates',True),('completed_updates',2),('overlay_origin',[False,0]),('driver','full_world'),('font_api',1)):
   inputs=deepcopy(p['inputs']);inputs[key]=value
   with self.assertRaises(ValueError):expected_preparation(inputs,p['before'])
  for offset,value in ((4,0),(0x1C,0),(0x20,1),(NODE_OFFSET,0),(OBJECT_OFFSET+22,1),(OBJECT_OFFSET,12),(0x92E0,1)):
   before=deepcopy(p['before']);v=next(r for r in before if r['pointer']==VM);b=bytearray.fromhex(v['hex']);b[offset]=value;v['hex']=b.hex()
   with self.assertRaises(ValueError):expected_preparation(p['inputs'],before)
  for mutate in (lambda r:r.pop(),lambda r:r[0].update({'bytes':399}),lambda r:r[3].update({'hex':'bad'})):
   before=deepcopy(p['before']);mutate(before)
   with self.assertRaises(ValueError):expected_preparation(p['inputs'],before)

 def test_exports_separate_audit_evidence_from_read_only_dialogue(self):
  rules=json.loads((ROOT/'prototype/data/school_text_preparation_rules.json').read_text('utf-8'))
  evidence=json.loads((ROOT/'prototype/data/school_text_preparation_evidence.json').read_text('utf-8'))
  runtime=json.loads((ROOT/'prototype/data/school_opening_dialogue.json').read_text('utf-8'))
  self.assertEqual(rules,source_catalog());self.assertNotIn('cases',rules)
  self.assertEqual(evidence['cases'],native_fixture()['cases']);self.assertFalse(evidence['runtime_fixture'])
  self.assertEqual(evidence['native_report_sha256'],EVIDENCE_SHA256)
  self.assertEqual(runtime,dialogue_catalog());self.assertEqual(len(runtime['pages']),10);self.assertNotIn('cases',runtime)

if __name__=='__main__':unittest.main()
