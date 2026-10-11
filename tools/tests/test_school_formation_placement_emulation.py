import hashlib,json,struct,unittest
from tools.school_formation_placement_emulation import (
 SchoolFormationPlacementEmulator,ROOT,UNITCTRL,MAPCTRL,STACK,ROTATION,RESERVATION,WORK_OFFSET,WORK_BYTES,RECORD_OFFSET)
from tools.school_unitctrl_map_emulation import map_resource
from tools.school_map_common_emulation import map_common_resource
from tools.school_tactical_resource_catalog import container_sections
EVIDENCE=ROOT/'analysis/school-formation-placement-v1-20261011.json'
EVIDENCE_SHA256='49539eef42ffb378a48935a0509675a2412fd5c2649956fb93c4f69df973d383'

class FormationNativeTests(unittest.TestCase):
 def test_actual_ready_refusal_natural_caller_and_prior_bytes(self):
  data=json.loads(EVIDENCE.read_text('utf-8'))
  self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
  previous=json.loads((ROOT/'analysis/school-scene-remaining-v1-20261011.json').read_text('utf-8'))
  for c,old in zip(data['cases'],previous['cases']):
   self.assertEqual(c['scene_remaining'],old['scene_remaining'])
   self.assertEqual(c['scene_batch'],old['scene_batch'])
   for key in ('current_units','scene_unit_constructor','second_scene_constructor'):self.assertEqual(c[key],old[key])
   self.assertTrue(c['persistent_ranges_unchanged']);self.assertFalse(c['live_witness']);self.assertFalse(c['authorizes_persistent_write'])
  for c in data['cases'][:3]:
   p=c['formation_placement'];self.assertTrue(c['formation_placement_completed']);self.assertTrue(p['retained_ranges_unchanged'])
   self.assertEqual(p['stop_va'],'0x468a49');self.assertFalse(p['deployment_completed']);self.assertFalse(p['scene_vm_executed'])
   self.assertEqual(p['calls'][0]['return_va'],'0x468a49');self.assertEqual(len(p['calls']),1)
   self.assertEqual(len(p['clears']),1);self.assertEqual(p['clears'][0]['bytes'],164)
   self.assertEqual(len(p['positions']),len(p['selected_indices']))
  for c in data['cases'][3:]:self.assertFalse(c['formation_placement_completed']);self.assertIsNone(c['formation_placement'])

 def test_finite_guard_and_cpu_boundary_refusal(self):
  e=SchoolFormationPlacementEmulator();e.placement_loading=True;e.placement_selected=[];e.placement_cells=set()
  for address in (UNITCTRL+RECORD_OFFSET,UNITCTRL+WORK_OFFSET,RESERVATION+164,ROTATION+2,0x7F4490):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,address,1,0,None)
  e._write_hook(e.uc,0,ROTATION,2,0,None);e._write_hook(e.uc,0,RESERVATION,164,0,None)
  e.placement_loading=False
  with self.assertRaises(RuntimeError):e.run_placement()
  self.assertFalse(e.placement_loading)

 def test_declared_original_rotation_and_reservation_candidates(self):
  # Reuse a separately frozen native generic-grid fixture for declared calls.
  old=json.loads((ROOT/'analysis/school-unitctrl-map-v1-20261009.json').read_text('utf-8'))
  rows=old['cases'][0]['appearance_grid']['rows'];logical,_=map_resource('map05.bin');common,_=map_common_resource();section=container_sections(common)[1]
  r={'grid_hex':b''.join(struct.pack('<bbHH',*v) for v in rows).hex(),'map_hex':logical.hex(),
   'terrain_hex':common[section['offset']:section['offset']+section['bytes']].hex()}
  e=SchoolFormationPlacementEmulator();header,wrapper,cm,grid,terrain=0x13000000,0x13009020,0x1300A000,0x1F000000,0x1F010000
  for at,key in ((header,'map_hex'),(grid,'grid_hex'),(terrain,'terrain_hex')):e.uc.mem_write(at,bytes.fromhex(r[key]))
  for at,value in ((UNITCTRL+0x2A304,header),(UNITCTRL+0x2A308,wrapper),(wrapper,cm),(MAPCTRL+0x263B8,grid),(MAPCTRL+0x8C,terrain)):e.write(at,value)
  e.write(MAPCTRL+0x263C0,65,'h');e.write(MAPCTRL+0x263C2,65,'h')
  e.placement_loading=True;e.placement_selected=[];e.placement_cells=set()
  observed=[];original_ranges=e._function_ranges
  for initial in range(5):
   e.write(ROTATION,initial,'h');e.uc.mem_write(RESERVATION,bytes(164))
   # Declared mode4 bypass and radius4, separate from actual school evidence.
   value=e.call(0x43D660,receiver=MAPCTRL,args=(32,48,4,4,STACK+0x100,STACK+0x104))
   self.assertEqual(value,1);self.assertEqual(e.read(ROTATION,'h'),(initial+1)%5)
   xy=(e.read(STACK+0x100,'h'),e.read(STACK+0x104,'h'));observed.append(xy)
   self.assertEqual(e.read(RESERVATION),1);self.assertEqual([e.read(RESERVATION+i,'h') for i in (4,6)],list(xy))
   value=e.call(0x43D660,receiver=MAPCTRL,args=(32,48,4,4,STACK+0x100,STACK+0x104))
   self.assertEqual(value,1);self.assertNotEqual((e.read(STACK+0x100,'h'),e.read(STACK+0x104,'h')),xy)
  self.assertGreater(len(set(observed)),1);self.assertEqual(e._function_ranges,original_ranges);e.placement_loading=False

if __name__=='__main__':unittest.main()
