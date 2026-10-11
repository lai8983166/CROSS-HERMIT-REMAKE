import hashlib, json, struct, unittest
from tools.school_board_opening_emulation import *
EVIDENCE=ROOT/'analysis/school-board-opening-v1-20261012.json'
EVIDENCE_SHA256='de8fec0fa15b30f61bd737cdbf9ae59963d53073d181c6430f086d16a958f40e'

class BoardNativeTests(unittest.TestCase):
 def test_actual_board_returns_readiness_and_natural_text_boundary(self):
  raw=EVIDENCE.read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),EVIDENCE_SHA256);data=json.loads(raw)
  self.assertEqual(len(data['cases']),3)
  for index,c in enumerate(data['cases']):
   self.assertEqual((c['name'],c['provenance']['checkpoint_sha256']),CHECKPOINTS[index])
   self.assertEqual(c['provenance']['parent_opening_sha256'],PARENT_SHA)
   self.assertTrue(c['provenance']['complete_parent_stages_equal']);self.assertFalse(c['provenance']['upstream_rerun'])
   p=c['board_opening'];self.assertEqual(len(p['updates']),47);self.assertEqual(p['presentation_calls'],2538)
   self.assertEqual(p['readiness'],[{'update':i,'return_value':int(i==46)} for i in range(1,47)])
   self.assertEqual(p['updates'][44]['after']['animation_count'],45)
   self.assertEqual((p['updates'][45]['after']['layer_mode'],p['updates'][45]['after']['wait']),(2,1))
   self.assertEqual(p['updates'][46]['after']['wait'],0)
   self.assertEqual(p['pending_call']['args'],[0,p['inputs']['script_pointer']+676,0])
   self.assertEqual(p['pending_call']['return_va'],'0x4cef42')
   self.assertTrue(p['pending_call']['natural_stack_verified']);self.assertFalse(p['pending_call']['first_instruction_executed'])
   self.assertTrue(p['retained_ranges_unchanged']);self.assertGreater(p['retained_bytes'],100000000)
   for stage in ('before','after'):self.assertEqual([(r['pointer'],r['bytes']) for r in p[stage]],list(REGIONS))
   for k in ('board_handler_executed','active_layer_updates_executed','readiness_predicate_executed'):self.assertTrue(p[k])
   for k in ('synthetic_readiness','text_activation_executed','dialogue_executed','waves_executed','full_task_wrapper_executed','world_update_loop_executed','live_rendering','live_audio'):self.assertFalse(p[k])
  self.assertEqual(data['inherited_refusals'],read_parent()['inherited_refusals'])

 def test_pending_cpu_and_finite_owned_bytes_required(self):
  e=SchoolBoardOpeningEmulator()
  with self.assertRaises(RuntimeError):e.run_board_opening()
  self.assertFalse(e.board_loading);e.board_loading=True;e.board_allowed=[(a,a+n) for a,n in OWNED]
  for at in (0,TACT,WORK,CONTROL,NODE+10,OBJECT+2,OBJECT+22,VM+0x925C):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,1,0,None)
  e._write_hook(e.uc,0,NODE+6,2,1,None)
  with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,NODE+6,3,1,None)

 def test_terminal_draw_callers_and_shapes_required(self):
  e=SchoolBoardOpeningEmulator();e.board_loading=True;e.board_index=0;e.board_inputs={'overlay_origin':[0,0],'script_pointer':0xE741BD0};e.board_records=[]
  sp=STACK+0xFF00;e.uc.reg_write(UC_X86_REG_ESP,sp);e.uc.mem_write(sp,struct.pack('<17I',RETURN,*([0]*16)));e.uc.reg_write(UC_X86_REG_ECX,VM)
  for va in (0x4CBDB0,0x410310,0x4CD060,0x4C5EA0,0x4D29E0):
   with self.assertRaises(RuntimeError):e._hook(e.uc,va,1,None)
  e.write(sp,0x4CA6FC);e.uc.mem_write(sp+4,struct.pack('<11I',256,568,0,0xFFFFFFFF,65,100,0,26,176,20,0))
  with self.assertRaises(RuntimeError):e._hook(e.uc,0x4CBDB0,1,None)

 def test_active_logic_runs_but_fonts_nonempty_text_and_world_refused(self):
  e=SchoolBoardOpeningEmulator();e.board_loading=True;sp=STACK+0xFF00;e.uc.reg_write(UC_X86_REG_ESP,sp);e.write(sp,RETURN)
  e.uc.reg_write(UC_X86_REG_ECX,NODE);e.write(NODE,1,'H');e.write(NODE+2,3,'H');e.write(NODE+34,1,'H')
  e._hook(e.uc,0x4CA1B0,1,None);e._hook(e.uc,0x4C99E0,1,None)
  e.write(NODE+2,7,'H')
  with self.assertRaises(RuntimeError):e._hook(e.uc,0x4CA1B0,1,None)
  e.uc.reg_write(UC_X86_REG_ECX,OBJECT);e.write(OBJECT+22,1,'H')
  with self.assertRaises(RuntimeError):e._hook(e.uc,0x4CB220,1,None)
  for va in (0x4CA770,0x4CDF80,0x454CF0,0x46B470,0x4C4DC0):
   self.assertNotIn(va,CODE)
   with self.assertRaises(RuntimeError):e._hook(e.uc,va,1,None)

if __name__=='__main__':unittest.main()
