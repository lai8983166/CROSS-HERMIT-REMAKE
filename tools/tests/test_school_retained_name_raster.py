"""Source/API corruption, full replay and all-name offscreen corpus checks."""
import copy,gzip,json,unittest
from tools import school_retained_name_verification as proof


class NameRasterTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.report=json.loads(gzip.decompress((proof.ROOT/'analysis/school-retained-name-raster-v2-20261022.json.gz').read_bytes()));cls.names=json.loads(gzip.decompress((proof.ROOT/'analysis/school-retained-name-corpus-v2-20261022.json.gz').read_bytes()));cls.reference=next(c for c in cls.names['cases'] if c['role']==4)
 def reject(self,edit):
  c=copy.deepcopy(self.report['cases'][-1]);edit(c)
  with self.assertRaises((ValueError,RuntimeError,KeyError)):proof.verify_case(c,self.reference)
 def test_00_protocol_all_six_and_last_complete_source_replay(self):
  self.assertEqual(len(self.report['cases']),6)
  for c in self.report['cases']:proof.protocol(c,self.reference)
  r=proof.verify_case(self.report['cases'][-1],self.reference);self.assertEqual((r['new_original_instructions_replayed'],r['original_writes'],r['platform_calls'],r['natural_stack_layers']),(1461,536,23,7));self.assertEqual(r['full_memory_regions'],119)
 def test_missing_platform_call(self):self.reject(lambda c:c['step']['api_calls'].pop())
 def test_added_game_root(self):self.reject(lambda c:c['step'].update(root=dict(va=0x4ca770)))
 def test_IAT_rebinding_claim(self):self.reject(lambda c:c['step'].update(source_IAT_unchanged=False))
 def test_forged_full_memory_hash(self):self.reject(lambda c:c['final_memory'][0].update(sha256='0'*64))
 def test_forged_CPU(self):self.reject(lambda c:c['final_architectural_cpu'].update(MXCSR=c['final_architectural_cpu']['MXCSR']^1))
 def test_changed_instruction_digest(self):self.reject(lambda c:c['step'].update(instruction_sha256='0'*64))
 def test_changed_write_digest(self):self.reject(lambda c:c['step'].update(write_sha256='0'*64))
 def test_forged_font_caller(self):self.reject(lambda c:c['step']['api_calls'][0].update(return_va=0x4cad09))
 def test_foreign_measurement_translation(self):self.reject(lambda c:c['step']['api_calls'][2]['dc_translated_args'].__setitem__(0,99))
 def test_changed_DIB_output(self):
  self.reject(lambda c:next(a for a in c['step']['api_calls'] if a['name']=='CreateDIBSection')['memory_outputs'][0].update(hex='00000000'))
 def test_changed_glyph_API_output(self):
  self.reject(lambda c:next(a for a in c['step']['api_calls'] if a['name']=='TextOutA')['memory_outputs'][0].update(hex='00'))
 def test_unreleased_resources(self):self.reject(lambda c:c['cleanup'].update(all_resources_released=False))
 def test_old_DC_reused_as_fresh(self):self.reject(lambda c:c['offscreen'].update(fresh_owned_measurement_dc=c['offscreen']['logical_measurement_dc']))
 def test_changed_ANSI_code_page(self):self.reject(lambda c:c['offscreen'].update(ACP=950))
 def test_changed_raster_shape(self):self.reject(lambda c:c['raster'].update(bytes=4))
 def test_changed_natural_outer_stack(self):self.reject(lambda c:c['pending_texture']['frames'][-1].update(return_va=1))
 def test_claim_GPU_entry_executed(self):self.reject(lambda c:c['pending_texture'].update(first_instruction_executed=True))
 def test_all_21_corpus_native_repetition(self):
  r=proof.verify_corpus(self.names);self.assertTrue(r['all_three_pixel_stages_reproduced']);self.assertEqual(r['source_name_count'],21)
 def test_source_name_removed(self):
  r=copy.deepcopy(self.names);r['cases'].pop()
  with self.assertRaises(ValueError):proof.verify_corpus(r)
 def test_wrong_source_font_face(self):
  r=copy.deepcopy(self.names);r['face_hex']='41'
  with self.assertRaisesRegex(ValueError,'original raw ANSI font face'):proof.verify_corpus(r)
 def test_changed_raw_Big5_name(self):
  r=copy.deepcopy(self.names);r['cases'][0]['text_hex']='41'
  with self.assertRaisesRegex(ValueError,'exact original raw name'):proof.verify_corpus(r)
 def test_corpus_pixel_not_repeatable_even_with_rehashed_report(self):
  r=copy.deepcopy(self.names);c=r['cases'][0];raw=bytearray.fromhex(c['raster_hex']);raw[0]^=1;c['raster_hex']=raw.hex();c['raster_sha256']=proof.sha(raw);c['nonzero_bytes']=sum(bool(v) for v in raw);c['stages'][-1]['hex']=raw.hex()
  with self.assertRaisesRegex(ValueError,'fresh independently reproduced'):proof.verify_corpus(r)
 def test_no_same_lifetime_overclaim(self):
  r=copy.deepcopy(self.report);r['same_native_lifetime']=True
  with self.assertRaisesRegex(ValueError,'honest reconstructed'):proof.verify(r,self.names)
 def test_no_milestone_overclaim(self):
  r=copy.deepcopy(self.report);r['R3_complete']=True
  with self.assertRaisesRegex(ValueError,'honest reconstructed'):proof.verify(r,self.names)
 def test_no_game_function_substitution(self):
  r=copy.deepcopy(self.report);r['game_function_substitutions']=1
  with self.assertRaisesRegex(ValueError,'no source/stack'):proof.verify(r,self.names)


if __name__=='__main__':unittest.main()
