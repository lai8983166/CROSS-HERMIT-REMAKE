"""Retained dependency gap, source continuity and honest provenance rejection."""
import copy,gzip,json,unittest
from tools import school_retained_crt as proof

class RetainedCrtTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.r=json.loads(gzip.decompress((proof.ROOT/'analysis/school-retained-crt-boundary-v1-20261022.json.gz').read_bytes()))
 def reject(self,edit,full=False):
  c=copy.deepcopy(self.r['cases'][-1]);edit(c)
  with self.assertRaises((ValueError,RuntimeError,KeyError)):(proof.verify_case if full else proof.protocol)(c)
 def test_00_all_protocols_and_full_last_source_replay(self):
  for c in self.r['cases']:proof.protocol(c)
  c=proof.verify_case(self.r['cases'][-1]);self.assertEqual(c['original_instructions_replayed'],73);self.assertFalse(c['retained_heap_restored'])
 def test_added_root(self):self.reject(lambda c:c['step'].update(root={}))
 def test_added_platform_reply(self):self.reject(lambda c:c['step']['platform_replays'].append({}))
 def test_executed_lock_claim(self):self.reject(lambda c:c['pending_lock'].update(first_instruction_executed=True))
 def test_patched_ledger(self):self.reject(lambda c:c['after']['globals'].update(debug_first=0))
 def test_false_mapped_node(self):self.reject(lambda c:c['before']['debug_chain_nodes'][0].update(mapped=True))
 def test_forged_missing_node(self):self.reject(lambda c:c['before']['debug_chain_nodes'][0].update(pointer=0))
 def test_parent_provenance(self):self.reject(lambda c:c['parent_boundary'].update(scene_capture=0),True)
 def test_source_digest(self):self.reject(lambda c:c['step'].update(instruction_sha256='0'*64),True)
 def test_write_digest(self):self.reject(lambda c:c['step'].update(write_sha256='0'*64),True)
 def test_complete_memory(self):self.reject(lambda c:c['final_memory'][0].update(sha256='0'*64),True)
 def test_complete_CPU(self):self.reject(lambda c:c['final_architectural_cpu'].update(MXCSR=c['final_architectural_cpu']['MXCSR']^1),True)
 def test_retained_restore_overclaim(self):
  r=copy.deepcopy(self.r);r['retained_heap_restored']=True
  with self.assertRaises(ValueError):proof.verify(r)

if __name__=='__main__':unittest.main()
