import hashlib, json, struct, unittest
from tools.school_text_preparation_emulation import *
EVIDENCE=ROOT/'analysis/school-text-preparation-v1-20261012.json'
EVIDENCE_SHA256='fca8be507e3fa52273cf14db51f325c2fa70395e31b4a8b855a664112e50856a'

class TextNativeTests(unittest.TestCase):
 def test_actual_activation_split_record_and_unexecuted_font_entry(self):
  raw=EVIDENCE.read_bytes();self.assertEqual(hashlib.sha256(raw).hexdigest(),EVIDENCE_SHA256);data=json.loads(raw)
  self.assertEqual(len(data['cases']),3)
  for index,c in enumerate(data['cases']):
   self.assertEqual((c['name'],c['provenance']['checkpoint_sha256']),CHECKPOINTS[index])
   self.assertEqual(c['provenance']['parent_board_sha256'],PARENT_SHA)
   self.assertTrue(c['provenance']['complete_parent_stages_equal']);self.assertFalse(c['provenance']['upstream_rerun'])
   p=c['text_preparation'];self.assertEqual(p['activated']['pc'],232);self.assertEqual(p['activated']['target'],7)
   self.assertEqual(p['first_text']['decoded_big5'],'瑟希莉絲、伊里安。');self.assertEqual(p['split']['count'],1)
   self.assertEqual(p['split']['lines'][0]['hex'],p['first_text']['hex'])
   font=p['pending_font'];self.assertEqual(font['args'],[0,0,0,0,400,0,0,0,1,5,0,0,0,0x5BF62C])
   self.assertEqual(font['return_va'],'0x4cad09');self.assertTrue(font['natural_stack_verified']);self.assertFalse(font['first_instruction_executed'])
   self.assertEqual(p['presentation_calls'],54);self.assertTrue(p['retained_ranges_unchanged']);self.assertGreater(p['retained_bytes'],100000000)
   for stage in ('before','after'):self.assertEqual([(r['pointer'],r['bytes']) for r in p[stage]],list(REGIONS))
   for k in ('text_activation_executed','text_lookup_executed','line_split_executed','initial_text_record_prepared'):self.assertTrue(p[k])
   for k in ('font_api_executed','text_handler_completed','synthetic_font_handle','text_layout_completed','text_readiness_executed','dialogue_playback_completed','waves_executed','full_task_wrapper_executed','world_update_loop_executed','live_rendering','live_audio'):self.assertFalse(p[k])
  self.assertEqual(data['inherited_refusals'],read_parent()['inherited_refusals'])

 def test_actual_pending_cpu_and_finite_writes_required(self):
  e=SchoolTextPreparationEmulator()
  with self.assertRaises(RuntimeError):e.run_text_preparation()
  self.assertFalse(e.text_loading);e.text_loading=True;e.text_allowed=[(a,a+n) for a,n in OWNED]
  for at in (0,TACT,WORK,CONTROL,NODE+10,OBJECT+2,OBJECT+22,VM+0x925C):
   with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,at,1,0,None)
  e._write_hook(e.uc,0,OBJECT+24,2,1,None)
  with self.assertRaises(RuntimeError):e._write_hook(e.uc,0,OBJECT+38,3,1,None)

 def test_wrong_native_callers_nonempty_text_and_font_execution_refused(self):
  e=SchoolTextPreparationEmulator();e.text_loading=True;e.board_loading=True;e.text_inputs={'script_pointer':0xE741BD0};e.text_calls=[]
  sp=STACK+0xFF00;e.uc.reg_write(UC_X86_REG_ESP,sp);e.uc.mem_write(sp,struct.pack('<17I',RETURN,*([0]*16)));e.uc.reg_write(UC_X86_REG_ECX,VM)
  for va in (0x4C4DC0,0x4C4B80,0x4C2120,0x4CABD0,0xE300000,0x454CF0,0x46B470):
   with self.assertRaises(RuntimeError):e._hook(e.uc,va,1,None)
  e.uc.reg_write(UC_X86_REG_ECX,OBJECT);e.write(sp,0x4C4D04);e.write(OBJECT+22,1,'H')
  with self.assertRaises(RuntimeError):e._hook(e.uc,0x4CABD0,1,None)
  self.assertNotIn(0xE300000,CODE)

if __name__=='__main__':unittest.main()
