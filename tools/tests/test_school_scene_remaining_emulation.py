import hashlib,json,struct,unittest
from unittest.mock import patch
from tools.school_scene_remaining_emulation import (
 SchoolSceneRemainingEmulator,ROOT,UNITCTRL,WORK_OFFSET,WORK_BYTES,RECORD_OFFSET,CACHE_OFFSET,COUNTER_OFFSET,
 REMAINING_ANIM,REMAINING_ANIM_BYTES,REMAINING_CONTROLLERS,STACK)

EVIDENCE=ROOT/'analysis/school-scene-remaining-v1-20261011.json'
EVIDENCE_SHA256='8ad911442a5835c9c98b5d279068e10956be955c606227cc1de1b380b0eab820'
PREVIOUS=ROOT/'analysis/school-scene-batch-v1-20261011.json'
PREVIOUS_SHA='e3cd62002440f9d1a91eb0ddb35cc0fc987a964995c9ee94fd3b52ea756fd706'

class SceneRemainingNativeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.full=json.loads(EVIDENCE.read_text('utf-8'));cls.previous=json.loads(PREVIOUS.read_text('utf-8'))

 def test_actual_remaining_constructor_returns_and_two_refusals(self):
  self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
  self.assertEqual([c['scene_remaining_completed'] for c in self.full['cases']],[True,True,True,False,False])
  for c in self.full['cases'][:3]:
   b=c['scene_remaining'];self.assertEqual((b['count'],b['cache_hits'],b['new_resources'],b['constructors_completed_total'],b['remaining_templates']),(25,19,6,35,0))
   self.assertEqual([u['ordinal'] for u in b['units']],list(range(10,35)))
   self.assertEqual([u['index'] for u in b['units']],list(range(239,214,-1)))
   self.assertEqual(c['stop_reason'],'after_all_scene_constructors_and_progress')
   for u in b['units']:
    t=u['tail'];self.assertEqual((t['return_va'],t['return_eax']),('0x453630',0));self.assertTrue(t['constructor_completed'])
    self.assertFalse(t['scene_placement_executed']);self.assertFalse(t['scene_vm_executed'])
    prior=bytearray.fromhex(t['before_record_hex'])
    if u['job']==406:prior[159]=2
    self.assertEqual(t['record_hex'],prior.hex());self.assertEqual(struct.unpack_from('<H',bytes.fromhex(t['work_hex']),1278)[0],600)
  for c in self.full['cases'][3:]:self.assertIsNone(c['scene_remaining'])

 def test_actual_nineteen_hits_and_six_finite_resources(self):
  for c in self.full['cases'][:3]:
   units=c['scene_remaining']['units'];owned={};loads=[]
   for u in units:
    if not u['cache_hit']:
     a=u['animation'];count={452:122,301:98,316:118,317:118,337:47,406:29}[u['job']]
     loads.append(u['job']);owned[u['controller']]=u['job']
     self.assertEqual(len(a['entries']),count)
     self.assertEqual(a['vector']['native_constructors_completed'],count);self.assertTrue(a['vector']['iteration_outside_instruction_hook'])
     self.assertEqual([x['freed'] for x in a['allocations']],[True,False,False])
     self.assertEqual([e['name'] for e in u['file_events']],['GetCurrentDirectoryA','CreateFileA','GetFileSize','ReadFile','CloseHandle'])
     self.assertEqual(u['counter_after'],u['counter_before']+1)
    else:
     self.assertEqual(owned[u['controller']],u['job']);self.assertIsNone(u['animation']);self.assertIsNone(u['allocation'])
     self.assertEqual(u['file_events'],[]);self.assertEqual(u['cache_before_hex'],u['cache_after_hex']);self.assertEqual(u['counter_before'],u['counter_after'])
     self.assertEqual(struct.unpack_from('<I',bytes.fromhex(u['tail']['work_hex']),68)[0],u['controller'])
   self.assertEqual(loads,[452,301,316,317,337,406])
   self.assertEqual(sum(len(u['animation']['entries']) for u in units if u['animation']),532)
   self.assertEqual(len(c['scene_remaining']['progress']),26)

 def test_prior_current_npc_resource_bytes_and_all_other_memory_retained(self):
  self.assertEqual(hashlib.sha256(PREVIOUS.read_bytes()).hexdigest(),PREVIOUS_SHA)
  for c,old in zip(self.full['cases'],self.previous['cases']):
   self.assertTrue(c['persistent_ranges_unchanged']);self.assertFalse(c['battle_world_constructed']);self.assertFalse(c['live_witness'])
   if not c['ready']:continue
   for key in ('scene_unit_constructor','second_scene_constructor','second_scene_animation'):
    for field in ('work_hex','record_hex','shared_hex','cm_hex','controller_hex','metadata_hex'):
     if field in old[key]:self.assertEqual(c[key][field],old[key][field],(key,field))
   self.assertEqual(c['scene_batch']['count'],8)
   for unit,prior in zip(c['scene_batch']['units'],old['scene_batch']['units']):
    for field in ('ordinal','job','controller','prefix_work_hex','prefix_record_hex','cache_before_hex','cache_after_hex','counter_before','counter_after'):
     self.assertEqual(unit[field],prior[field],(unit['ordinal'],field))
    for field in ('work_hex','record_hex','shared_hex','cm_hex'):
     self.assertEqual(unit['tail'][field],prior['tail'][field],(unit['ordinal'],field))
    if prior['animation']:
     for field in ('controller_hex','metadata_hex','entries','allocations','binding','file_release'):
      self.assertEqual(unit['animation'][field],prior['animation'][field],(unit['ordinal'],field))
   extra=[event for u in c['scene_remaining']['units'] for event in u['file_events']]
   self.assertEqual(c['file_events'],old['file_events']+extra)
   for u in c['scene_remaining']['units']:
    for record in (u,u['tail'],u['record_derivation']):
     self.assertTrue(record['retained_ranges_unchanged']);self.assertGreater(record['retained_bytes'],100000000)
     self.assertEqual(sum(x['bytes'] for x in record['retained_ranges']),record['retained_bytes'])

 def test_cache_hit_and_tail_write_guards_reject_previous_objects_and_new_resources(self):
  e=SchoolSceneRemainingEmulator();e.remaining_loading=True;e.remaining_phase='prefix';e.controller=REMAINING_CONTROLLERS
  w=UNITCTRL+WORK_OFFSET+245*WORK_BYTES;r=UNITCTRL+RECORD_OFFSET+245*176
  e.remaining_work={'work_pointer':w,'record_pointer':r,'cache_hit':True,'role':301,'job':301}
  for at,size in ((UNITCTRL+CACHE_OFFSET,1),(UNITCTRL+COUNTER_OFFSET,4),(REMAINING_CONTROLLERS,1),(REMAINING_ANIM,1),(w-1,1),(w+WORK_BYTES,1)):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,size,0,None)
  e.remaining_phase='tail';e.scene_phase='tail';e.scene_complete_loading=True;e.constructor_cell=0x1A001001;e.active_index=245
  for at,size in ((r+159,1),(r,1),(REMAINING_CONTROLLERS,1),(REMAINING_ANIM,1),(e.constructor_cell,1),(e.constructor_cell,2)):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,size,0,None)
  for at in (0x428A40,0x428AD0,0x4500B0,0x468910,0x424F80):
   with self.assertRaises(RuntimeError):e._hook(e.uc,at,1,None)
  e.remaining_phase='animation';e.active_index=245;e.remaining_animation_cursor=REMAINING_ANIM;e.animation_allocations=[]
  for count in (0,-1,REMAINING_ANIM_BYTES+1):
   with self.assertRaises(RuntimeError):e.animation_allocate(count,'unit_metadata',0)

 def test_failed_remaining_restores_parent_controller_and_phase_flags(self):
  e=SchoolSceneRemainingEmulator();before=e.next_controller
  def fail(*args,**kwargs):
   e.next_controller=REMAINING_CONTROLLERS
   raise RuntimeError('declared failure during remaining')
  with patch.object(e.uc,'emu_start',side_effect=fail):
   with self.assertRaisesRegex(RuntimeError,'declared failure'):e.run_remaining()
  self.assertEqual(e.next_controller,before)
  self.assertFalse(e.remaining_loading);self.assertFalse(e.enemy_loading);self.assertFalse(e.scene_complete_loading)

if __name__=='__main__':unittest.main()
