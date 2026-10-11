import hashlib,json,struct,unittest
from tools.school_scene_second_constructor_emulation import (
 SchoolSceneSecondConstructorEmulator,ROOT,UNITCTRL,WORK_OFFSET,WORK_BYTES,RECORD_OFFSET,
 SCENE_CONTROLLER,SECOND_ANIM,SECOND_PATH,SECOND_SHA,TASK,STACK,UC_X86_REG_ESP)
from tools.school_scene_next_input_catalog import EVIDENCE as PREVIOUS,EVIDENCE_SHA256 as PREVIOUS_SHA

EVIDENCE=ROOT/'analysis/school-scene-second-constructor-v1-20261011.json'
EVIDENCE_SHA256='4a73435783457dca57f928b71f5421458824828b6b43611275c822b3b231c0a6'

class SceneSecondConstructorNativeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.full=json.loads(EVIDENCE.read_text('utf-8'));cls.previous=json.loads(PREVIOUS.read_text('utf-8'))

 def test_actual_second_constructor_natural_return_and_refusal(self):
  self.assertEqual(hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),EVIDENCE_SHA256)
  self.assertEqual([c['second_scene_constructor_completed'] for c in self.full['cases']],[True,True,True,False,False])
  for c in self.full['cases'][:3]:
   p,a,t=c['second_scene_work'],c['second_scene_animation'],c['second_scene_constructor']
   self.assertEqual((p['index'],p['role'],p['job'],p['category'],a['variant']),(248,387,387,0,0))
   self.assertEqual(c['stop_reason'],'after_second_scene_unit_constructor_return')
   self.assertEqual((t['return_va'],t['return_eax']),('0x453630',0))
   self.assertTrue(t['constructor_completed']);self.assertFalse(t['scene_vm_executed'])
   work=bytes.fromhex(t['work_hex']);before=bytearray.fromhex(t['before_record_hex'])
   before[159]=2;self.assertEqual(bytes.fromhex(t['record_hex']),bytes(before))
   self.assertEqual(struct.unpack_from('<H',work,86)[0],1)
   self.assertEqual(struct.unpack_from('<H',work,1278)[0],900)
   self.assertEqual(struct.unpack_from('<I',work,68)[0],SCENE_CONTROLLER+96)
   self.assertEqual(work[650],3);self.assertEqual(work[656],2)
  for c in self.full['cases'][3:]:
   self.assertIsNone(c['second_scene_animation']);self.assertIsNone(c['second_scene_constructor'])

 def test_mode0_file_vector_gpu_and_allocation_ownership(self):
  for c in self.full['cases'][:3]:
   a=c['second_scene_animation']
   self.assertEqual(a['request']['source']['relative_path'],SECOND_PATH)
   self.assertEqual(a['request']['loaded_sha256'],SECOND_SHA)
   self.assertEqual(a['request']['args'][1:],[0,0,0])
   self.assertEqual([e['name'] for e in a['file_events']][-4:],['CreateFileA','GetFileSize','ReadFile','CloseHandle'])
   self.assertEqual([x['bytes'] for x in a['allocations']],[1552728,9016,126*84+4])
   self.assertEqual([x['freed'] for x in a['allocations']],[True,False,False])
   self.assertEqual(a['vector']['native_constructors_completed'],126)
   self.assertTrue(a['vector']['iteration_outside_instruction_hook'])
   self.assertEqual(len(a['entries']),126)
   self.assertEqual(a['binding']['args'][4:],[0,0,0])
   for entry in a['entries']:self.assertEqual(entry['palette_pointer'],0)
   for kind in ('texture_creation','pixel_upload'):
    self.assertEqual(sum(b['kind']==kind for b in a['boundaries']),126)
   for b in a['boundaries']:
    if b['kind']=='pixel_upload':self.assertEqual(b['args'][3],0)
   self.assertEqual(struct.unpack('<II',bytes.fromhex(a['texture_slot_hex'])),(a['allocations'][2]['pointer']+4,126))

 def test_previous_objects_and_all_other_mapped_memory_retained(self):
  self.assertEqual(hashlib.sha256(PREVIOUS.read_bytes()).hexdigest(),PREVIOUS_SHA)
  for c,old in zip(self.full['cases'],self.previous['cases']):
   self.assertTrue(c['persistent_ranges_unchanged']);self.assertFalse(c['battle_world_constructed'])
   self.assertFalse(c['live_witness'])
   if not c['ready']:continue
   for key in ('second_scene_work','second_scene_record','scene_progress'):
    for field in ('work_hex','record_hex','cache_hex','controller_hex','counter','after_hex'):
     if field in old[key]:self.assertEqual(c[key][field],old[key][field],(c['name'],key,field))
   for key in ('scene_unit_animation','scene_unit_constructor'):
    for field in ('work_hex','record_hex','shared_hex','cm_hex','controller_hex','metadata_hex'):
     if field in old[key]:self.assertEqual(c[key][field],old[key][field])
   extra=c['second_scene_animation']['file_events']
   self.assertEqual(c['file_events'],old['file_events']+extra)
   for n in (c['second_scene_animation'],c['second_scene_constructor']):
    self.assertTrue(n['retained_ranges_unchanged']);self.assertGreater(n['retained_bytes'],100_000_000)
    self.assertEqual(sum(x['bytes'] for x in n['retained_ranges']),n['retained_bytes'])
    self.assertFalse(n['scene_placement_executed'])

 def test_finite_guard_rejects_previous_units_wrong_fields_and_resources(self):
  e=SchoolSceneSecondConstructorEmulator();e.second_loading=True;e.scene_complete_loading=True;e.scene_phase='tail'
  e.active_index=248;e.constructor_cell=0x1000100;e.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00)
  w=UNITCTRL+WORK_OFFSET+248*WORK_BYTES;r=UNITCTRL+RECORD_OFFSET+248*176
  for at,size in ((w-1,1),(w+WORK_BYTES,1),(r+158,1),(r+160,1),(r+159,2),(SCENE_CONTROLLER,1),(SECOND_ANIM,1)):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,size,0,None)
  for at in (0x424F80,0x428A40,0x428AD0,0x4500B0,0x468910):
   with self.assertRaises(RuntimeError):e._hook(e.uc,at,1,None)
  e.scene_phase='animation';e.controller=SCENE_CONTROLLER+96;e.texture_table=TASK+0x844
  e.scene_texture_slot=114;e.animation_allocations=[];e.scene_animation_cursor=SECOND_ANIM
  for at in (w,SCENE_CONTROLLER,TASK+0x844+113*8,SECOND_ANIM):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,1,0,None)
  with self.assertRaises(RuntimeError):e.animation_allocate(0,'unit_file_buffer',0)
  with self.assertRaises(RuntimeError):e.animation_allocate(0x400001,'unit_file_buffer',0)

if __name__=='__main__':unittest.main()
