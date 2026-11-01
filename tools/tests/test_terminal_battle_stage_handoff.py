"""Independent late battle stage source model, schedule and guard rejections."""
import copy,os,unittest
from unittest.mock import patch
from tools import terminal_battle_stage_handoff_emulation as e
from tools import terminal_battle_stage_handoff_verification as v
REPORT=os.environ.get('TERMINAL_BATTLE_STAGE_HANDOFF_REPORT','analysis/terminal-battle-stage-handoff-source-v3-20261101.json.gz')

class BattleStageStaticTests(unittest.TestCase):
 def test_exact_source_extents_and_mutable_writes(self):
  self.assertEqual(e.EXTRA_RANGES,((0x4998B0,0x499901),(0x499910,0x499B5D),(0x49AD50,0x49AD8C),(0x4DB2B0,0x4DB2F4),(0x4116A4,0x411CE2),(0x4DAAE0,0x4DAB06)))
  self.assertEqual(e.NEW_MUTABLE,((e.TASK+0x38,e.TASK+0x3C),(e.TASK+0x108CC2,e.TASK+0x108CC4),(0x7A417C,0x7A4186),(0x5FF720,0x5FF724),(e.ANIM,e.ANIM+0x14),(0x7F44BE,0x7F44CE),(0x7F4518,0x7F7C18)))
  self.assertEqual(v.source({})['frames'],349)
 def test_guard_extension_cannot_be_widened(self):
  with patch.object(e,'EXTRA_RANGES',e.EXTRA_RANGES+((0x400000,0x592000),)):
   with self.assertRaises(ValueError):v.source({})
 def test_only_accepted_input_endpoints_are_connected(self):
  self.assertEqual(v.TEXT_APIS,{0x76182A80:('ImmGetOpenStatus',0x5920EC,0x425C99),0x770206E0:('lstrlenA',0x5922C4,None)})
  self.assertEqual(v.source({})['text_APIs'],[('ImmGetOpenStatus',0x5920EC,0x425C99),('lstrlenA',0x5922C4,None)])
  guard=__import__('inspect').getsource(v.protocol)
  self.assertIn("want=[s for i in range(TOTAL_FRAMES) for s in ('input_'+str(i),'task_'+str(i))]",guard)
  self.assertIn("need([r['segment'] for r in text]==want,'input endpoints stay in each frame own input and task segment')",guard)
  self.assertIn("need([r['name'] for r in text]==['ImmGetOpenStatus','lstrlenA']*TOTAL_FRAMES,'three captured gateway segments add no text endpoint')",guard)
 def test_selector_schedule_is_exact(self):
  self.assertEqual(v.TOTAL_FRAMES,349);self.assertEqual(v.expected_phases()[0:2],['selector5','selector15']);self.assertEqual(v.expected_phases()[-2:],['result_rectangles_214','selector20'])
  self.assertEqual(len([p for p in v.expected_phases() if p.startswith('result_rectangles_')]),214)
  self.assertEqual(len([p for p in v.expected_phases() if p.startswith('fade_in_')]),64)
  self.assertEqual(len([p for p in v.expected_phases() if p.startswith('animation_progress_')]),31)
  self.assertEqual(len([p for p in v.expected_phases() if p.startswith('animation_fade_')]),32)
 def test_result_dispatch_table_and_mode_words(self):
  self.assertEqual(v.RESULT_TYPE_CONFIGURATION,{1:2,2:3,3:4,4:5,5:6});self.assertEqual(v.RESULT_MODES,{1:0,2:1,3:1,4:2,5:2})
  self.assertEqual(v.source({})['result_types'],{1:(2,0),2:(3,1),3:(4,1),4:(5,2),5:(6,2)})
 def test_original_action_sites_derive_declared_words(self):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  declared={}
  for offset,value in e.ACTION_CODES:declared.setdefault(offset,set()).add(value)
  self.assertEqual(v.derive_action_codes(Cs(CS_ARCH_X86,CS_MODE_32)),declared)
 def test_source_guard_algorithm_unchanged(self):
  self.assertIs(e.BattleStageMachine.source_code.__code__,e.parent.TaskCompletionMachine.source_code.__code__)
  self.assertEqual(e.REFERENCE.__code__,e.parent.REFERENCE.__code__)
 def test_parent_completion_boundary_still_refused(self):
  source=__import__('inspect').getsource(e.parent.TaskCompletionMachine.code)
  self.assertIn("at not in (0x453F10,0x454793,0x473860,0x4CE9C5)",source)
  mine=__import__('inspect').getsource(e.BattleStageMachine.code)
  for want in ("at not in (0x424F80,0x4CE9C5,0x454E18)","self.get(slot)==at","self.get(sp)==0x454798 and self.getreg('ECX')==CTRL","entry=at,kind='result_handoff'"):self.assertIn(want,mine)
 def test_result_mode_word_page_is_original_writable_data(self):
  import struct
  pe=struct.unpack_from('<I',e.CODE,0x3C)[0];n=struct.unpack_from('<H',e.CODE,pe+6)[0];o=struct.unpack_from('<H',e.CODE,pe+20)[0];page=0x5FF720-0x400000;hits=[]
  for i in range(n):
   h=pe+o+24+i*40;vsize,va,rsize,roff=struct.unpack_from('<IIII',e.CODE,h+8);ch=struct.unpack_from('<I',e.CODE,h+36)[0]
   if roff<=page<roff+rsize:hits.append((e.CODE[h:h+8].rstrip(b'\0'),ch))
  self.assertEqual(len(hits),1);self.assertTrue(hits[0][0].startswith(b'.data'));self.assertEqual(hits[0][1],0xC0000040)
  inspect=__import__('inspect')
  machine=inspect.getsource(e.BattleStageMachine.bsh_expose_animation_mode)
  self.assertIn('self.uc.mem_protect(0x5FF000,0x1000,UC_PROT_READ|UC_PROT_WRITE)',machine)
  admission=inspect.getsource(e.BattleStageMachine.admission)
  self.assertLess(admission.index('self.bsh_before=self.bsh_capture()'),admission.index('self.bsh_expose_animation_mode()'))
  verify=inspect.getsource(v.execute_stage)
  self.assertIn('u.mem_protect(0x5FF000,0x1000,UC_PROT_READ|UC_PROT_WRITE)',verify)
  self.assertNotIn('mem_protect',inspect.getsource(v.Replay.__init__))
 def test_result_dispatch_requires_advanced_stage_word(self):
  source=__import__('inspect').getsource(e.BattleStageMachine.code)
  self.assertIn("self.get(TASK+0x38)==17 and configuration in (2,3,4,5,6)",source)
  self.assertIn("original result animation dispatch on the controller",source)
 def test_natural_result_handoff_bytes(self):
  import struct
  off=lambda a:a-0x400000
  self.assertEqual(e.CODE[off(0x454793):off(0x454798)],b'\xe8'+struct.pack('<i',0x473860-0x454798))
  self.assertEqual(e.CODE[off(0x454798):off(0x45479d)],b'\xb8\x01\x00\x00\x00')
 def test_action_word_frame_follows_original_prologue(self):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  md=Cs(CS_ARCH_X86,CS_MODE_32);off=lambda a:a-0x400000
  seq=[(i.mnemonic,i.op_str) for i in md.disasm(e.CODE[off(0x4112ad):off(0x4112ba)],0x4112ad)]
  self.assertEqual(seq,[('mov','eax, dword ptr [ebp - 4]'),('add','eax, 0x890'),('mov','dword ptr [ebp - 8], eax')])
  machine=__import__('inspect').getsource(e.BattleStageMachine.bsh_captured)
  self.assertIn('self.put(bp-8,KEYBOARD+0x890)',machine)
  self.assertIn('action_word_slot=bp-8,action_word_pointer=KEYBOARD+0x890',machine)
  replay=__import__('inspect').getsource(v.bind_keyboard)
  self.assertIn("u.mem_write(e.STACK+0xF800-8,struct.pack('<I',e.KEYBOARD+0x890))",replay)
 def test_input_write_capture_is_bounded_to_the_owned_block(self):
  source=__import__('inspect').getsource(e.BattleStageMachine.write_hook)
  self.assertIn('INPUT<=at<INPUT+0x680',source)
  self.assertIn('KEYBOARD<=at and at+size<=KEYBOARD+0xA00',source)
 def test_streamed_report_equals_one_complete_object(self):
  import json,shutil,tempfile
  name='analysis/terminal-battle-stage-handoff-stream-test-'+str(os.getpid())+'.json.gz';work=tempfile.mkdtemp();rows=[{'input':{'name':'neutral_running'},'hex':'a'*5000},{'input':{'name':'timeout_before_combat'},'hex':'b'*5000}]
  encoder=json.JSONEncoder(ensure_ascii=False,separators=(',',':'));paths=[]
  for index,row in enumerate(rows):
   path=os.path.join(work,'case-'+str(index)+'.json');paths.append(path)
   with open(path,'xb') as stream:
    for block in encoder.iterencode(row):stream.write(block.encode('utf8'))
  head=dict(schema_version=1,source_contract={'declared':True},helper_build={'GPU':{'source':'tools/terminal_followup_d3d8_platform.cs','source_sha256':'x','machine':0x14C}});footer=dict(R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False)
  try:
   e.save_source_cases(name,head,paths,footer);parts=list(v.stream_report(e.ROOT/name));self.assertEqual([k for k,_ in parts],['header','case','case','footer'])
   self.assertEqual(parts[0][1],head);self.assertEqual([r for k,r in parts[1:3]],rows);self.assertEqual(parts[3][1],dict(head,**footer))
   whole=v.load_report(e.ROOT/name);self.assertEqual(whole, dict(head,cases=rows,**footer))
  finally:
   (e.ROOT/name).unlink(missing_ok=True);shutil.rmtree(work,ignore_errors=True)
 def test_parent_guards_use_the_accepted_script_exit_ancestor(self):
  src=__import__('inspect').getsource(v.verify_case)
  self.assertIn("need(all(d['before'][k]==fixed[k] for k in ('memory','CPU','queue','trace'))",src)
  self.assertIn("need(all(d['prefix'][k]==old['counts'][k] for k in ('task_APIs','task_calls','task_writes','APIs'))",src)
  self.assertIn("fixed=old['final']",src)
  witness=__import__('inspect').getsource(v.accepted_case_witness)
  self.assertIn("task_completion_report.cache_clear()",witness)
  self.assertIn("'terminal_task_completion']['final']",witness)
  self.assertIn("witness=accepted_case_witness()",__import__('inspect').getsource(v.verify))
  self.assertIn('base=previous_stage.parent_case(row)',src)
  self.assertIn('previous_stage.native(row,base)',src)
  self.assertIn('platform=native(row,base)',src)
  self.assertNotIn('previous_stage.prefix(row,old',src)
 def test_cumulative_entry_hits_are_bound_to_the_independent_stage(self):
  src=__import__('inspect').getsource(v.verify_case)
  self.assertIn("pc_counts=counts.pop('stage_pc_counts')",src)
  self.assertIn("added={k:int(v)-int(old['entries'].get(k,0))",src)
  self.assertIn("need(all(v>0 for v in added.values()),'accepted parent entry counts only grow during the original result stage')",src)
  self.assertIn("need(all(pc_counts.get(int(k,16),0)==v for k,v in added.items()),'every added original entry is entered exactly by the independent stage execution')",src)
  self.assertIn("boundary['entries']=old['entries']",src)
  self.assertIn('previous_stage.prefix(boundary,base,replay=False)',src)
  self.assertNotIn('previous_stage.prefix(row,base',src)
  executed=__import__('inspect').getsource(v.execute_stage)
  self.assertIn('pc_counts[at]=pc_counts.get(at,0)+1',executed)
  self.assertIn('stage_pc_counts=pc_counts',executed)
  witness=__import__('inspect').getsource(v.accepted_case_witness)
  self.assertIn("entries=dict(r['entries'])",witness)
 def test_stage_separates_battle_exit_and_rewards(self):
  c=e.source_contract();self.assertTrue(c['terminal_battle_stage_handoff_executed']);self.assertFalse(c['terminal_battle_exit_executed']);self.assertFalse(c['rewards_or_school_executed']);self.assertFalse(c['terminal_presentation_complete'])

class BattleStageReportTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  path=e.ROOT/REPORT
  if not path.exists():raise unittest.SkipTest('battle stage source report not present')
  cls.data=v.load_report(path);cls.rows=cls.data['cases']
 @staticmethod
 def changed(obj,path,value):
  if not path:return value
  out=copy.copy(obj);out[path[0]]=BattleStageReportTests.changed(obj[path[0]],path[1:],value);return out
 def reject(self,path,value,check,index=0):
  with self.assertRaises((ValueError,KeyError,IndexError,StopIteration,AssertionError)):check(self.changed(self.rows[index],('terminal_battle_stage_handoff',)+tuple(path),value))
 def test_both_complete_original_battle_stage_handoffs(self):
  # The contract's new_mutable write_PCs are the original write sites collected
  # while the source emulation actually ran; a fresh call in the test process
  # has executed nothing, so the run-time lists are removed for the contract
  # comparison and checked on their own against the original mapped code below.
  def static(c):
   out=copy.deepcopy(c)
   for m in out['new_mutable']:m.pop('write_PCs')
   return out
  self.assertEqual(static(self.data['source_contract']),static(e.source_contract()))
  pcs=[m['write_PCs'] for m in self.data['source_contract']['new_mutable']]
  self.assertTrue(all(p and p==sorted(set(p)) for p in pcs))
  self.assertEqual(len({tuple(p) for p in pcs}),1)
  written=sorted({w['pc'] for row in self.rows for w in row['terminal_battle_stage_handoff']['writes']})
  self.assertEqual(pcs[0],written)
  self.assertLessEqual(set(written),e.ALLOWED)
  for row in self.rows:
   with self.subTest(case=row['input']['name']):
    p=v.protocol(row);self.assertEqual(p['complete_frames'],349);self.assertEqual(p['result_handoff'],'0x454793->0x473860->0x454798');self.assertFalse(p['battle_exit_consumer_executed'])
 def test_no_extra_frame_allowed(self):self.reject(('frames',),self.rows[0]['terminal_battle_stage_handoff']['frames']+[{}],v.protocol)
 def test_exact_selector_phase_order_required(self):self.reject(('frames',0,'phase'),'selector6',v.protocol)
 def test_completion_flag_consumption_required(self):self.reject(('frames',0,'after','stage_word'),1,v.protocol)
 def test_substage_word_accepts_only_its_own_two_values(self):
  self.reject(('before','state','stage_word'),2,v.protocol)
 def test_no_stage_platform_counter_may_move(self):
  for key in e.STAGE_PLATFORM_COUNTS:self.reject(('counts_after',key),self.rows[0]['terminal_battle_stage_handoff']['prefix'][key]+1,v.protocol)
 def test_only_accepted_text_endpoint_receipts(self):
  self.reject(('text_APIs',0,'name'),'Other',v.protocol)
 def test_fade_must_complete_at_0x100(self):self.reject(('frames',65,'after','fade'),0xFC,v.protocol)
 def test_result_configuration_required(self):self.reject(('frames',65,'after','animation','configuration'),3,v.protocol)
 def test_recorded_result_dispatch_required(self):
  self.reject(('result_configuration',),3,v.protocol);self.reject(('animation_mode',),1,v.protocol)
 def test_animation_start_step_required(self):self.reject(('frames',66,'after','animation','progress'),0,v.protocol)
 def test_animation_progress_required(self):self.reject(('frames',67,'after','animation','progress'),0x400,v.protocol)
 def test_gate_control_requires_no_input(self):self.reject(('frames',98,'after','held'),0x8000,v.protocol)
 def test_gate_press_required(self):self.reject(('frames',99,'after','held'),0,v.protocol)
 def test_animation_fade_required(self):self.reject(('frames',100,'after','animation','progress'),0xFF00,v.protocol)
 def test_499910_must_return_once(self):self.reject(('frames',132,'after','selector'),17,v.protocol)
 def test_countdown_armed_at_0x4ff(self):self.reject(('frames',133,'after','countdown'),0x4FE,v.protocol)
 def test_every_rectangle_frame_required(self):self.reject(('frames',200,'rectangles'),127,v.protocol)
 def test_result_handoff_frame_required(self):self.reject(('result','frame'),346,v.protocol)
 def test_stage20_must_return_one(self):self.reject(('frames',348,'result'),0,v.protocol)
 def test_frozen_identity_is_final_task_state(self):self.reject(('identity_after','VM_PC'),405,v.protocol)
 def test_capture_samples_bound_only_at_gate(self):self.reject(('frames',99,'capture'),'other',v.protocol)
 def test_raw_device_sample_sequence_required(self):
  b=copy.deepcopy(self.rows[0]['terminal_battle_stage_handoff']['bindings']);b[1]['after_hex']='00';self.reject(('bindings',),b,v.protocol)
 def test_natural_473860_call_site_required(self):
  calls=copy.deepcopy(self.rows[0]['terminal_battle_stage_handoff']['calls']);next(r for r in calls if r['kind']=='result_handoff')['return_address']=0x45479D;self.reject(('calls',),calls,v.protocol)
 def test_473860_entered_once_from_its_own_call_site(self):
  ev=copy.deepcopy(self.rows[0]['terminal_battle_stage_handoff']['events']);ev[0]['before']['selector']=19;self.reject(('events',),ev,v.protocol)
 def test_all_frame_segments_partition_the_five_roots(self):
  seg=self.rows[0]['terminal_battle_stage_handoff']['segments'];self.reject(('segments',),seg[:-1],v.protocol)
 def test_no_stage_platform_calls_outside_two_input_endpoints(self):
  # The parent native summary's current_GDI_calls is the number of recorded GDI
  # calls over the complete prefix block list, so it is rebuilt here from the
  # rows' own frozen GDI receipts instead of replaying the parent report.
  from tools import terminal_last_dialogue_verification as gdi
  for row in self.rows:
   blocks=gdi.gdi_prefix_blocks(row)+gdi.new_resources(row)
   prior=dict(current_GDI_calls=sum(len(b['GDI_trace']) for b in blocks))
   self.assertTrue(v.no_new_platform_calls(row,prior)['no_new_platform_calls'])
 def test_complete_final_memory_must_match_terminal_pages(self):
  mem=self.rows[0]['terminal_battle_stage_handoff']['final']['memory'];i=next(j for j,r in enumerate(mem) if r['pointer']<=e.TASK<r['pointer']+r['bytes']);old=mem[i]['hex'];k=2*(e.TASK-mem[i]['pointer'])
  self.reject(('final','memory',i,'hex'),old[:k]+('00' if old[k:k+2]!='00' else 'ff')+old[k+2:],v.final_summary)

if __name__=='__main__':unittest.main()
