import hashlib,json,unittest
from tools.school_deployment_tail_emulation import *
EVIDENCE_SHA256='82812542fc02b448d33bd3c743da973935949d37475f9676ba20b9c2b1e09132'
class DeploymentNativeTests(unittest.TestCase):
 def test_actual_checkpoint_tail_natural_return_and_refusal_provenance(self):
  path=ROOT/'analysis/school-deployment-tail-v1-20261011.json';raw=path.read_bytes()
  self.assertEqual(digest(raw),EVIDENCE_SHA256);data=json.loads(raw)
  for index,c in enumerate(data['cases']):
   self.assertEqual(c['name'],CHECKPOINTS[index][0]);self.assertEqual(c['provenance']['checkpoint_sha256'],CHECKPOINTS[index][1])
   self.assertTrue(c['provenance']['complete_placement_equal']);self.assertFalse(c['provenance']['upstream_rerun'])
   p=c['deployment_tail'];self.assertTrue(p['deployment_completed']);self.assertTrue(p['natural_stack_verified'])
   self.assertTrue(p['retained_ranges_unchanged']);self.assertGreater(p['retained_bytes'],100000000)
   self.assertEqual(p['stop_va'],'0x4534a1');self.assertEqual(p['return_value'],0)
   self.assertFalse(p['scene_vm_executed']);self.assertFalse(p['next_467aa0_executed'])
   self.assertEqual(len(p['allocations']),7);self.assertEqual(sum(a['bytes'] for a in p['allocations']),589824)
   self.assertEqual(len(p['calls']),8);self.assertEqual(len(p['clears']),10)
  self.assertEqual([c['name'] for c in data['inherited_refusals']],['teacher_only','teacher_waiting'])
  for c in data['inherited_refusals']:
   self.assertFalse(c['ready']);self.assertFalse(c['suffix_executed']);self.assertEqual(c['evidence_origin'],'immutable_parent_not_rerun')

 def test_finite_guard_exact_allocation_and_entry_refusal(self):
  e=SchoolDeploymentTailEmulator();e.deployment_loading=True;e.deployment_allowed=[(STACK,STACK+65536)]
  for at in (0,UNITCTRL,UNITCTRL+WORK_OFFSET,POOL,0x7F4491):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,1,0,None)
  e.deployment_allocations=[]
  for args in ((172031,0x437AAC),(172032,0x44E88C),(0,0x437AAC)):
   with self.assertRaises(RuntimeError):e._allocate(*args)
  self.assertEqual(e.deployment_allocations,[]);e.deployment_loading=False
  with self.assertRaises(RuntimeError):e.run_deployment_tail()
  self.assertFalse(e.deployment_loading)

 def test_pinned_parent_identity(self):
  parent=parent_evidence();self.assertEqual(len(parent['cases']),5)
  self.assertEqual([c['name'] for c in parent['cases'][:3]],[c[0] for c in CHECKPOINTS])
  for c in parent['cases'][:3]:self.assertEqual(c['formation_placement']['stop_va'],'0x468a49')

if __name__=='__main__':unittest.main()
