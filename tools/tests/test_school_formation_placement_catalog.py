import hashlib,json,unittest
from copy import deepcopy
from tools.school_formation_placement_catalog import (
 source_catalog,native_fixture,expected_placement,appearance_grid,ROOT,EVIDENCE,EVIDENCE_SHA256)
from tools.school_formation_placement_emulation import SchoolFormationPlacementEmulator,UNITCTRL,MAPCTRL,STACK,ROTATION,RESERVATION

class FormationSourceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.rules=source_catalog();cls.fixture=native_fixture()

 def test_independent_original_grid_map_terrain_and_exports(self):
  self.assertEqual(hashlib.sha256(appearance_grid()).hexdigest(),'902e81f8eff318965e9f61f592a5a7c0541be0529ab5871e4dc6b6c4cbfbe4fd')
  self.assertEqual(len(bytes.fromhex(self.rules['terrain_hex'])),7600)
  self.assertEqual(len(bytes.fromhex(self.rules['map_hex'])),36880)
  for name,data in [('rules',self.rules),('evidence',self.fixture)]:
   self.assertEqual(json.loads((ROOT/f'prototype/data/school_formation_placement_{name}.json').read_text('utf-8')),data)

 def test_every_actual_selected_unselected_and_cell_byte(self):
  for c in self.fixture['cases'][:3]:
   p=c['formation_placement'];original=deepcopy((p['inputs'],p['units']))
   expected=expected_placement(p['inputs'],p['units'],self.rules)
   for key in ('selected_indices','rotation','reservation_hex','cm_hex'):self.assertEqual(expected[key],p[key],(c['name'],key))
   self.assertEqual(expected['positions'],[v['xy'] for v in p['positions']])
   for a,b in zip(expected['units'],p['units']):
    for key in ('index','work_hex','record_hex'):self.assertEqual(a[key],b[key],(c['name'],b['index'],key))
   self.assertEqual(original,(p['inputs'],p['units']))

 def test_bad_header_source_bytes_slot_ownership_and_order_refused(self):
  p=self.fixture['cases'][0]['formation_placement']
  mutations=[('scene_id',98),('selected_class',True),('selected_class',5),('formation_radius',-1),
   ('formation_radius',33),('origin',[64,0]),('before_rotation',5),('grid_dimensions',[64,65]),
   ('map_hex','00'),('grid_hex','00'),('formation_sizes_hex','00'),('terrain_hex','00'),
   ('before_cm_hex','00'),('before_reservation_hex','00')]
  for key,value in mutations:
   with self.subTest(key=key,value=value):
    inputs=deepcopy(p['inputs']);inputs[key]=value
    with self.assertRaises(ValueError):expected_placement(inputs,p['units'],self.rules)
  for key,value in [('work_pointer',0),('record_pointer',0),('before_work_hex','00'),('before_record_hex','00')]:
   units=deepcopy(p['units']);units[0][key]=value
   with self.assertRaises(ValueError):expected_placement(p['inputs'],units,self.rules)
  with self.assertRaises(ValueError):expected_placement(p['inputs'],list(reversed(p['units'])),self.rules)

 def test_no_space_failure_and_return_ownership(self):
  p=deepcopy(self.fixture['cases'][0]['formation_placement'])
  cm=bytearray.fromhex(p['inputs']['before_cm_hex']);cm[1::2]=bytes([1])*6144;p['inputs']['before_cm_hex']=cm.hex()
  with self.assertRaises(ValueError):expected_placement(p['inputs'],p['units'],self.rules)
  p=self.fixture['cases'][0]['formation_placement'];a=expected_placement(p['inputs'],p['units'],self.rules)
  a['units'][0]['record_hex']='changed'
  self.assertNotEqual(a,expected_placement(p['inputs'],p['units'],self.rules))

 def test_declared_five_rotations_match_independent_first_candidate(self):
  p=deepcopy(self.fixture['cases'][0]['formation_placement']);inputs=p['inputs'];inputs['origin']=[32,48];inputs['formation_radius']=4
  unit=p['units'][0];record=bytearray.fromhex(unit['before_record_hex']);record[48]=4;unit['before_record_hex']=record.hex()
  inputs['selected_class']=record[164]
  e=SchoolFormationPlacementEmulator();header,wrapper,cm,grid,terrain=0x13000000,0x13009020,0x1300A000,0x1F000000,0x1F010000
  for at,key in ((header,'map_hex'),(grid,'grid_hex'),(terrain,'terrain_hex')):e.uc.mem_write(at,bytes.fromhex(self.rules[key]))
  for at,value in ((UNITCTRL+0x2A304,header),(UNITCTRL+0x2A308,wrapper),(wrapper,cm),(MAPCTRL+0x263B8,grid),(MAPCTRL+0x8C,terrain)):e.write(at,value)
  e.write(MAPCTRL+0x263C0,65,'h');e.write(MAPCTRL+0x263C2,65,'h')
  e.placement_loading=True;e.placement_selected=[];e.placement_cells=set()
  try:
   for initial in range(5):
    inputs['before_rotation']=initial;expected=expected_placement(inputs,[unit],self.rules)
    e.write(ROTATION,initial,'h');e.uc.mem_write(RESERVATION,bytes(164))
    self.assertEqual(e.call(0x43D660,receiver=MAPCTRL,args=(32,48,4,4,STACK+0x100,STACK+0x104)),1)
    self.assertEqual([e.read(STACK+o,'h') for o in (0x100,0x104)],expected['positions'][0])
    self.assertEqual(e.read(ROTATION,'h'),expected['rotation'])
    self.assertEqual(bytes(e.uc.mem_read(RESERVATION,164)).hex(),expected['reservation_hex'])
  finally:e.placement_loading=False

if __name__=='__main__':unittest.main()
