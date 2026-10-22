"""Real continuous six-branch replay and altered resource-boundary evidence."""
import copy,gzip,json,unittest
from tools import school_retained_portrait_verification as proof


class PortraitTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=json.loads(gzip.decompress((proof.ROOT/'analysis/school-retained-portrait-v1-20261022.json.gz').read_bytes()))
 def test_00_six_original_task_continuations(self):
  r=proof.verify(self.report);self.assertTrue(r['six_continuous_portrait_prefixes_verified'])
  for c in r['cases']:self.assertEqual((c['configuration'],c['layer'],c['role'],c['font_height'],c['font_weight']),(8,5,4,20,700));self.assertFalse(c['font_API_executed']);self.assertFalse(c['R3_complete'])
 def reject(self,edit):
  c=copy.deepcopy(self.report['cases'][-1]);edit(c)
  with self.assertRaises((ValueError,KeyError,RuntimeError)):proof.verify_case(c)
 def test_changed_font_height(self):self.reject(lambda c:c['pending_font']['args'].__setitem__(0,24))
 def test_changed_natural_stack(self):self.reject(lambda c:c['pending_font']['frames'][2].update(return_va=1))
 def test_wrong_source_instruction_digest(self):self.reject(lambda c:c['step'].update(instruction_sha256='0'*64))
 def test_wrong_complete_write_digest(self):self.reject(lambda c:c['step'].update(write_sha256='0'*64))
 def test_changed_predicted_layer(self):
  def edit(c):
   row=next(r for r in c['after'] if r['pointer']==proof.VM);b=bytearray.fromhex(row['hex']);b[0x6f60+5*0xe0]^=1;row['hex']=b.hex()
  self.reject(edit)
 def test_wrong_full_memory(self):self.reject(lambda c:c['final_memory'][0].update(sha256='0'*64))
 def test_wrong_full_CPU(self):self.reject(lambda c:c['final_architectural_cpu'].update(MXCSR=c['final_architectural_cpu']['MXCSR']^1))
 def test_new_root_disallowed(self):self.reject(lambda c:c['step'].update(root=dict(va=0x4c61c0)))
 def test_font_API_overclaim(self):
  r=copy.deepcopy(self.report);r['font_API_executed']=True
  with self.assertRaisesRegex(ValueError,'honest prefix scope'):proof.verify(r)
 def test_fake_platform_response(self):self.reject(lambda c:c['step']['platform_replays'].append(dict(result=0)))


if __name__=='__main__':unittest.main()
