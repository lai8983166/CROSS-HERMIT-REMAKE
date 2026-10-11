import hashlib,json,struct,unittest
from unittest.mock import patch
from tools.school_scene_batch_emulation import (
 SchoolSceneBatchEmulator,ROOT,UNITCTRL,WORK_OFFSET,WORK_BYTES,RECORD_OFFSET,CACHE_OFFSET,COUNTER_OFFSET,
 BATCH_ANIM,BATCH_ANIM_BYTES,BATCH_CONTROLLERS,STACK)

EVIDENCE=ROOT/'analysis/school-scene-batch-v1-20261011.json'
EVIDENCE_SHA256='e3cd62002440f9d1a91eb0ddb35cc0fc987a964995c9ee94fd3b52ea756fd706'
PREVIOUS=ROOT/'analysis/school-scene-second-constructor-v1-20261011.json'
PREVIOUS_SHA='4a73435783457dca57f928b71f5421458824828b6b43611275c822b3b231c0a6'

class SceneBatchNativeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.full=json.loads(EVIDENCE.read_text('utf-8'));cls.previous=json.loads(PREVIOUS.read_text('utf-8'))

 def test_actual_eight_constructor_returns_and_two_refusals(self):
  self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
  self.assertEqual([c['scene_batch_completed'] for c in self.full['cases']],[True,True,True,False,False])
  for c in self.full['cases'][:3]:
   b=c['scene_batch'];self.assertEqual((b['count'],b['cache_hits'],b['new_resources'],b['constructors_completed_total'],b['remaining_templates']),(8,6,2,10,25))
   self.assertEqual([u['ordinal'] for u in b['units']],list(range(2,10)))
   self.assertEqual([u['index'] for u in b['units']],list(range(247,239,-1)))
   self.assertEqual(c['stop_reason'],'after_scene_ordinal9_constructor_return')
   for u in b['units']:
    t=u['tail'];self.assertEqual((t['return_va'],t['return_eax']),('0x453630',0));self.assertTrue(t['constructor_completed'])
    self.assertFalse(t['scene_placement_executed']);self.assertFalse(t['scene_vm_executed'])
    prior=bytearray.fromhex(t['before_record_hex'])
    if u['job']==393:prior[159]=2
    self.assertEqual(t['record_hex'],prior.hex());self.assertEqual(struct.unpack_from('<H',bytes.fromhex(t['work_hex']),1278)[0],600)
  for c in self.full['cases'][3:]:self.assertIsNone(c['scene_batch'])

 def test_actual_six_hits_retain_controller_without_file_allocation_or_cache_writes(self):
  for c in self.full['cases'][:3]:
   units=c['scene_batch']['units'];self.assertEqual([u['cache_hit'] for u in units],[False,False,True,True,True,True,True,True])
   for u,count in zip(units[:2],(109,43)):
    a=u['animation'];self.assertEqual(len(a['entries']),count)
    self.assertEqual(a['vector']['native_constructors_completed'],count);self.assertTrue(a['vector']['iteration_outside_instruction_hook'])
    self.assertEqual([x['freed'] for x in a['allocations']],[True,False,False])
    self.assertEqual([e['name'] for e in u['file_events']],['GetCurrentDirectoryA','CreateFileA','GetFileSize','ReadFile','CloseHandle'])
    self.assertEqual(u['counter_after'],u['counter_before']+1)
   controller=units[1]['controller']
   for u in units[2:]:
    self.assertEqual(u['controller'],controller);self.assertIsNone(u['animation']);self.assertIsNone(u['allocation'])
    self.assertEqual(u['file_events'],[]);self.assertEqual(u['cache_before_hex'],u['cache_after_hex']);self.assertEqual(u['counter_before'],u['counter_after'])
    self.assertEqual(struct.unpack_from('<I',bytes.fromhex(u['tail']['work_hex']),68)[0],controller)

 def test_prior_current_npc_resource_bytes_and_all_other_memory_retained(self):
  self.assertEqual(hashlib.sha256(PREVIOUS.read_bytes()).hexdigest(),PREVIOUS_SHA)
  for c,old in zip(self.full['cases'],self.previous['cases']):
   self.assertTrue(c['persistent_ranges_unchanged']);self.assertFalse(c['battle_world_constructed']);self.assertFalse(c['live_witness'])
   if not c['ready']:continue
   for key in ('scene_unit_constructor','second_scene_constructor','second_scene_animation'):
    for field in ('work_hex','record_hex','shared_hex','cm_hex','controller_hex','metadata_hex'):
     if field in old[key]:self.assertEqual(c[key][field],old[key][field],(key,field))
   extra=[event for u in c['scene_batch']['units'] for event in u['file_events']]
   self.assertEqual(c['file_events'],old['file_events']+extra)
   for u in c['scene_batch']['units']:
    for record in (u,u['tail'],u['record_derivation']):
     self.assertTrue(record['retained_ranges_unchanged']);self.assertGreater(record['retained_bytes'],100000000)
     self.assertEqual(sum(x['bytes'] for x in record['retained_ranges']),record['retained_bytes'])

 def test_cache_hit_and_tail_write_guards_reject_previous_objects_and_new_resources(self):
  e=SchoolSceneBatchEmulator();e.batch_loading=True;e.batch_phase='prefix';e.controller=BATCH_CONTROLLERS
  w=UNITCTRL+WORK_OFFSET+245*WORK_BYTES;r=UNITCTRL+RECORD_OFFSET+245*176
  e.batch_work={'work_pointer':w,'record_pointer':r,'cache_hit':True,'role':383}
  for at,size in ((UNITCTRL+CACHE_OFFSET,1),(UNITCTRL+COUNTER_OFFSET,4),(BATCH_CONTROLLERS,1),(BATCH_ANIM,1),(w-1,1),(w+WORK_BYTES,1)):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,size,0,None)
  e.batch_phase='tail';e.scene_phase='tail';e.scene_complete_loading=True;e.constructor_cell=0x1A001001;e.active_index=245
  for at,size in ((r+159,1),(r,1),(BATCH_CONTROLLERS,1),(BATCH_ANIM,1),(e.constructor_cell,2)):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,size,0,None)
  for at in (0x428A40,0x428AD0,0x4500B0,0x468910,0x424F80):
   with self.assertRaises(RuntimeError):e._hook(e.uc,at,1,None)
  e.batch_phase='animation';e.active_index=245;e.batch_animation_cursor=BATCH_ANIM;e.animation_allocations=[]
  for count in (0,-1,BATCH_ANIM_BYTES+1):
   with self.assertRaises(RuntimeError):e.animation_allocate(count,'unit_metadata',0)

 def test_failed_batch_restores_parent_controller_and_phase_flags(self):
  e=SchoolSceneBatchEmulator();before=e.next_controller
  def fail(*args,**kwargs):
   e.next_controller=BATCH_CONTROLLERS
   raise RuntimeError('declared failure during batch')
  with patch.object(e.uc,'emu_start',side_effect=fail):
   with self.assertRaisesRegex(RuntimeError,'declared failure'):e.run_batch()
  self.assertEqual(e.next_controller,before)
  self.assertFalse(e.batch_loading);self.assertFalse(e.enemy_loading);self.assertFalse(e.scene_complete_loading)

if __name__=='__main__':unittest.main()
