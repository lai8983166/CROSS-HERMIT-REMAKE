import copy,gzip,json,unittest
from tools.school_native_scene_verification import ROOT,verify_report

class NativeSceneEvidenceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.reports={s:json.loads(gzip.decompress((ROOT/f'analysis/school-native-scene-{s}-v{v}-20261021.json.gz').read_bytes())) for s,v in [(76,7),(77,3)]}
 def report(self):return copy.deepcopy(self.reports[76])
 def reject(self,r,why):
  with self.assertRaisesRegex(ValueError,why):verify_report(r)
 def test_both_actual_scene_contexts_scripts_worlds_and_lifetimes(self):
  for scene,r in self.reports.items():
   p=verify_report(r);self.assertEqual(p['scene'],scene);self.assertTrue(p['actual_original_outer_scheduler']);self.assertGreater(len(p['script']['observed_positive_PCs']),1);self.assertFalse(p['R3_complete'])
 def test_early_world_loop_is_rejected_even_when_process_closed_normally(self):
  r=json.loads(gzip.decompress((ROOT/'analysis/school-native-scene-76-v6-20261021.json.gz').read_bytes()))
  with self.assertRaises((ValueError,KeyError)):verify_report(r)
 def test_incomplete_failed_capture_is_rejected(self):
  r=json.loads(gzip.decompress((ROOT/'analysis/school-native-scene-76-v1-20261021.json.gz').read_bytes()));self.reject(r,'successful native scene probe')
 def test_no_missing_source_ranges_or_graph_operands(self):
  r=self.report();r['source_contract']['ranges'].pop();self.reject(r,'fixed native source')
  r=self.report();r['source_contract']['instructions'].pop();self.reject(r,'source graph operands')
 def test_IAT_change_is_rejected(self):
  r=self.report();r['case']['probe']['source_after']['IAT'][0]['hex']='01000000';self.reject(r,'code/vtable/IAT unchanged')
 def test_no_direct_VM_or_factory_root_substitution(self):
  r=self.report();r['case']['probe']['calls'][2]['va']=0x451080;self.reject(r,'no task or VM shortcut')
 def test_complete_stack_cleanup_is_required(self):
  r=self.report();c=r['case']['probe']['calls'][1];b=bytearray.fromhex(c['parameter_after_hex']);b[36]^=4;c['parameter_after_hex']=b.hex();self.reject(r,'native call input/ESP/exit')
 def test_private_writes_and_frees_are_exact(self):
  r=self.report();r['case']['probe']['writes'].append(copy.deepcopy(r['case']['probe']['writes'][-1]));self.reject(r,'every process write')
  r=self.report();r['case']['probe']['frees'][0]['released']=False;self.reject(r,'private allocation cleanup')
 def test_selected_scenario_cannot_be_fabricated(self):
  r=self.report();b=bytearray.fromhex(r['case']['probe']['scenario_selected_hex']);b[20]^=1;r['case']['probe']['scenario_selected_hex']=b.hex();self.reject(r,'scenario output')
 def test_loaded_script_memory_must_match_original_file(self):
  r=self.report();b=bytearray.fromhex(r['case']['probe']['script_file']['loaded_memory_hex']);b[-1]^=1;r['case']['probe']['script_file']['loaded_memory_hex']=b.hex();self.reject(r,'loaded native script')
 def test_original_scene_must_be_in_complete_native_registry(self):
  r=self.report();s=next(s for s in r['case']['probe']['samples'] if s['scene_global']);s['registered_tasks'].pop();self.reject(r,'registered graph|task links')
 def test_actual_context_and_ordinary_wait_ancestry_are_required(self):
  r=self.report();s=next(s for s in r['case']['probe']['samples'] if s.get('ordinary_scene_loop_wait'));f=next(f for f in s['frames'] if f['tid']==r['case']['probe']['worker']['thread_id']);f['EIP']^=1;self.reject(r,'WOW64 frame scalars')
  r=self.report();s=next(s for s in r['case']['probe']['samples'] if s.get('ordinary_scene_loop_wait'));s['ordinary_scene_loop_wait']=False;self.reject(r,'CRT callback/wait ancestry')
 def test_PC_command_bytes_are_checked_against_source(self):
  r=self.report();s=next(s for s in r['case']['probe']['samples'] if 'VM_current_bytes' in s);s['VM_current_bytes']['hex']='00'*32;self.reject(r,'PC/command byte')
 def test_full_scene_state_must_match_sampled_windows(self):
  r=self.report();obj=r['case']['probe']['full_objects'][-1];b=bytearray.fromhex(obj['hex']);b[0x108cb0]^=1;obj['hex']=b.hex();self.reject(r,'complete object agrees')
 def test_worker_exit_is_not_natural_callback_completion(self):
  r=self.report();r['case']['worker_after_close'][0]['callback_natural_return_claimed']=True;self.reject(r,'no natural-return claim')
 def test_forced_job_exit_is_not_original_cleanup(self):
  r=self.report();r['case']['lifecycle']['lifetime']['forced_termination']=True;self.reject(r,'forced termination')
 def test_clock_can_share_tick_but_cannot_go_backwards(self):
  r=self.report();s=r['case']['probe']['samples'];s[2]['elapsed']=s[1]['elapsed'];verify_report(r)
  r=self.report();s=r['case']['probe']['samples'];s[2]['elapsed']=s[0]['elapsed']-1;self.reject(r,'ordered actual native')
 def test_no_promoting_native_new_game_to_retained_resume_or_R3_completion(self):
  r=self.report();r['case']['retained_checkpoint_rehydrated']=True;self.reject(r,'scene/scope integrity')
  r=self.report();r['R3_complete']=True;self.reject(r,'milestone envelope')

if __name__=='__main__':unittest.main()
