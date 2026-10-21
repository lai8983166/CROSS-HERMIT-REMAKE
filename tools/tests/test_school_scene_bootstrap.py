import copy,gzip,json,unittest
from types import SimpleNamespace
from tools.school_scene_bootstrap import ROOT,SceneCalls,source_contract
from tools.school_scene_bootstrap_verification import verify_report

class SceneBootstrapTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.reports={name:json.loads(gzip.decompress((ROOT/path).read_bytes())) for name,path in [('zero','analysis/school-scene-bootstrap-zero-v1-20261021.json.gz'),('dirty','analysis/school-scene-bootstrap-dirty-v1-20261021.json.gz'),('yield','analysis/school-scene-bootstrap-yield-v3-20261021.json.gz')]}
 def report(self,name='dirty'):return copy.deepcopy(self.reports[name])
 def reject(self,r,why):
  with self.assertRaisesRegex(ValueError,why):verify_report(r)
 def instance(self):
  c=SceneCalls.__new__(SceneCalls);c.pid=7;c.owned=SimpleNamespace(members=lambda:[7]);c.data=0x10000000;c.pending={};return c
 def test_original_factory_callback_and_state_graph(self):
  s=source_contract();self.assertEqual((s['thread_callback'],s['world_loop']),(0x451670,0x4539b0));self.assertFalse(s['original_scene_callback_executed'])
 def test_native_zero_and_dirty_objects(self):
  for name in ('zero','dirty'):
   r=verify_report(self.reports[name]);self.assertTrue(r['registry_disabled_unlink_and_destructor_full_byte_models']);self.assertFalse(r['whole_constructor_independently_replayed'])
 def test_actual_cooperative_source_wait_and_ticks(self):
  r=verify_report(self.reports['yield']);self.assertEqual(r['delay_sequence'],[2,1,0]);self.assertFalse(r['original_CRT_scene_callback'])
 def test_foreign_or_arbitrary_callback_calls_are_rejected(self):
  c=self.instance()
  for va in (0x451080,0x451670,0x4539b0,0x46b470):
   with self.assertRaisesRegex(ValueError,'entry/ABI'):c.validate(va,c.data+0x2000,())
  c.owned=SimpleNamespace(members=lambda:[])
  with self.assertRaisesRegex(ValueError,'owned Job'):c.validate(0x451170,c.data+0x2000,())
 def test_wrong_object_register_bucket_and_delay_are_rejected(self):
  c=self.instance()
  for va,recv,args,why in [(0x451170,0x7a4174,(),'private node'),(0x4216c0,c.data+0x1000,(c.data+0x2000,1,0),'private source scene registration'),(0x422360,c.data+0x2000,(0,),'bounded delay2')]:
   with self.assertRaisesRegex(ValueError,why):c.validate(va,recv,args)
 def test_overlapping_constructor_is_rejected_before_native_write(self):
  c=self.instance();c.pending={0:(None,dict(va=0x422360))}
  with self.assertRaisesRegex(ValueError,'only delay tick'):c.start(0x451170,c.data+0x2000,slot=256)
 def test_out_of_guard_write_is_rejected(self):
  r=self.report();s=r['case']['probe']['stages'][-1];b=bytearray.fromhex(s['node_hex']);b[-1]^=1;s['node_hex']=b.hex();self.reject(r,'tail guard')
 def test_source_range_or_instruction_omissions_are_rejected(self):
  r=self.report();r['source_contract']['ranges'].pop();self.reject(r,'complete fixed source ranges')
  r=self.report();r['source_contract']['instructions'].pop();self.reject(r,'all source graph instructions')
 def test_live_IAT_change_is_rejected(self):
  r=self.report();r['case']['probe']['source_after']['IAT'][0]['hex']='01000000';self.reject(r,'source/vtable/IAT identity')
 def test_disabled_scan_cannot_change_any_object_byte(self):
  r=self.report();s=r['case']['probe']['stages'][4];b=bytearray.fromhex(s['node_hex']);b[0x80000]^=1;s['node_hex']=b.hex();self.reject(r,'disabled scan')
 def test_destructor_cannot_change_unrelated_dirty_fields(self):
  r=self.report();s=r['case']['probe']['stages'][6];b=bytearray.fromhex(s['node_hex']);b[0x80000]^=1;s['node_hex']=b.hex();self.reject(r,'destructor byte model')
 def test_font_must_really_be_deleted(self):
  r=self.report();r['case']['probe']['font_states'][1]['bytes_returned']=60;self.reject(r,'actual font metadata')
 def test_stack_imbalance_is_rejected(self):
  r=self.report();c=r['case']['probe']['calls'][0];b=bytearray.fromhex(c['parameter_after_hex']);b[36]^=4;c['parameter_after_hex']=b.hex();self.reject(r,'ESP/actual exit')
 def test_unreleased_buffer_or_duplicate_write_is_rejected(self):
  r=self.report();r['case']['probe']['frees'][0]['released']=False;self.reject(r,'allocations freed')
  r=self.report();w=r['case']['probe']['writes'];w[-1]=copy.deepcopy(w[-2]);self.reject(r,'exact private constructor writes')
 def test_native_wait_context_and_countdown_are_required(self):
  r=self.report('yield');r['case']['probe']['tick_statuses'][0]['exit_code']=0;self.reject(r,'remains blocked')
  r=self.report('yield');r['case']['probe']['blocked_before_ticks']['frame']['chain']=[];self.reject(r,'WaitForSingleObject ancestry')
 def test_yield_event_cleanup_must_be_actual(self):
  r=self.report('yield');r['case']['probe']['node_event_after_supplemental_close']['duplicate_succeeded']=True;self.reject(r,'event handle invalidity')
 def test_no_promotion_to_original_CRT_scene_callback(self):
  r=self.report('yield');r['case']['probe']['original_CRT_callback']=True;self.reject(r,'isolated yield')
 def test_no_promotion_to_R3_completion(self):
  r=self.report();r['R3_complete']=True;self.reject(r,'honest R3 scope')
 def test_failed_capture_is_not_an_accepted_lifetime(self):
  p=ROOT/'analysis/school-scene-bootstrap-yield-v2-20261021.json.gz';r=json.loads(gzip.decompress(p.read_bytes()));self.assertIsNone(r['case']['probe']);self.reject(r,'accepted native probe')

if __name__=='__main__':unittest.main()
