import copy,gzip,json,struct,unittest
from unicorn import UC_PROT_READ,UC_PROT_WRITE
from tools import battle_terminal_selection_emulation as e
from tools import battle_terminal_selection_model as m
from tools import battle_terminal_selection_verification as v

REPORT='analysis/battle-terminal-selection-source-v3-20261025.json.gz'
REPORT_SHA='8818a465255f3b1ae96e4bc80a725f07ceec5653e459ba0154da59cbb7a0f01f'


class TerminalTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  raw=(e.ROOT/REPORT).read_bytes();assert e.sha(raw)==REPORT_SHA;cls.data=json.loads(gzip.decompress(raw));cls.rows=cls.data['cases']

 def row(self,index=0):return copy.deepcopy(self.rows[index])
 def reject(self,edit,index=0,full=False):
  r=self.row(index);edit(r)
  with self.assertRaises(ValueError):
   if full:v.verify_case(r,False)
   else:m.verify(r)

 def test_all_eight_independent_contracts(self):
  for r in self.rows:
   with self.subTest(case=r['input']['name']):self.assertEqual(v.verify_case(r,False)['selector'],m.outcome(r['input'])['selector'])

 def test_original_condition_reads_and_sets_five_commands(self):
  for sub in (2,5,8,11,14):
   commands,result,span=m.program(sub);self.assertEqual([c['opcode'] for c in commands],[167,8,166,11,19]);self.assertEqual(result,1);self.assertLess(span[0],span[1])

 def test_real_enemy_death_selects_one(self):self.assertEqual([m.verify(r)['selector'] for r in self.rows[:2]],[1,1])
 def test_player_death_and_timeout_priority(self):self.assertEqual([m.verify(r)['selector'] for r in self.rows[2:4]],[5,4])
 def test_survival_threshold_is_not_premature_defeat(self):self.assertEqual([m.verify(r)['selector'] for r in self.rows[4:6]],[0,4])
 def test_neutral_living_enemy_is_not_hostile(self):
  for r in self.rows[6:]:self.assertEqual(m.verify(r)['selector'],1);self.assertEqual(bytes.fromhex(r['event']['before']['records'][0])[15],1)
 def test_actual_casualty_and_contribution_preserved(self):
  self.assertEqual(m.verify(self.rows[0])['player_contribution'],20);self.assertEqual(m.verify(self.rows[2])['player_deaths'],1)
 def test_task_embeds_the_actual_controller(self):
  fixture=e.TerminalMachine(e.corpus()[0]);self.assertEqual(e.TASK+0x190,e.CTRL);self.assertEqual(fixture.get(e.CTRL+0x117C38),e.TASK)
 def test_guard_and_call_algorithm_remain_frozen(self):
  self.assertIs(e.TerminalMachine.source_code.__code__,e.parent.LethalMachine.source_code.__code__);self.assertIs(e.TerminalMachine.base_call.__code__,e.parent.LethalMachine.base_call.__code__)
 def test_all_regions_disjoint(self):
  ordered=sorted(e.REGIONS);self.assertEqual(len(ordered),45)
  for (a,n),(b,k) in zip(ordered,ordered[1:]):self.assertLessEqual(a+n,b)
 def test_unknown_case_rejected(self):
  c=dict(e.corpus()[0],name='unknown')
  with self.assertRaises(ValueError):e.TerminalMachine(c)
 def test_boolean_time_rejected(self):
  with self.assertRaises(ValueError):e.validate(dict(e.corpus()[1],remaining=False))
 def test_unknown_PC_rejected(self):
  f=e.TerminalMachine(e.corpus()[0])
  with self.assertRaises(ValueError):f.source_code(f.uc,0x401000,1,None)
 def test_assertion_PC_rejected(self):
  f=e.TerminalMachine(e.corpus()[0]);code=e.SOURCE.read_bytes();at=next(a for a in e.ALLOWED if code[a-0x400000]==0xCC)
  with self.assertRaises(ValueError):f.source_code(f.uc,at,1,None)
 def test_forbidden_game_write_rejected(self):
  f=e.TerminalMachine(e.corpus()[0])
  with self.assertRaises(ValueError):f.write_hook(f.uc,0,e.SCRIPT,4,0,None)
 def test_IAT_patch_rejected(self):
  f=e.TerminalMachine(e.corpus()[0]);f.uc.mem_protect(0x592000,0x1000,UC_PROT_READ|UC_PROT_WRITE);f.uc.mem_write(0x592278,bytes(4))
  with self.assertRaises(ValueError):f.image_identity()
 def test_selected_script_tamper_rejected(self):self.reject(lambda r:r['calls'][next(i for i,x in enumerate(r['calls']) if x['entry']==0x454AF0)]['args'].__setitem__(0,5))
 def test_original_caller_tamper_rejected(self):self.reject(lambda r:r['calls'][next(i for i,x in enumerate(r['calls']) if x['entry']==0x4551C0)].__setitem__('caller',0))
 def test_condition_result_tamper_rejected(self):self.reject(lambda r:r['calls'][next(i for i,x in enumerate(r['calls']) if x['entry']==0x4551C0)].__setitem__('result',0))
 def test_VM_opcode_tamper_rejected(self):self.reject(lambda r:r['commands'][0].__setitem__('opcode',166))
 def test_VM_jump_tamper_rejected(self):self.reject(lambda r:r['commands'][4].__setitem__('pc',0))
 def test_VM_work_tamper_rejected(self):self.reject(lambda r:r['commands'][2].__setitem__('work','010001'))
 def test_request_fields_tamper_rejected(self):self.reject(lambda r:r['calls'][next(i for i,x in enumerate(r['calls']) if x['entry']==0x4549D0)]['args'].__setitem__(3,0))
 def test_result_page_tamper_rejected(self):
  def edit(r):
   s=bytearray.fromhex(r['finalization']['after']['result']);s[0x50C]^=1;r['finalization']['after']['result']=s.hex()
  self.reject(edit)
 def test_task_selector_tamper_rejected(self):
  def edit(r):
   s=bytearray.fromhex(r['event']['after']['task']);s[0x174]=2;r['event']['after']['task']=s.hex()
  self.reject(edit)
 def test_combat_record_rewrite_rejected(self):
  def edit(r):
   s=bytearray.fromhex(r['event']['after']['records'][1]);s[0x16]^=1;r['event']['after']['records'][1]=s.hex()
  self.reject(edit)
 def test_no_request_control_rejects_forged_request(self):self.reject(lambda r:r['calls'].append(dict(entry=0x454AF0)),4)
 def test_initial_byte_tamper_rejected(self):
  def edit(r):
   b=bytearray.fromhex(r['initial'][0]['hex']);b[0]^=1;r['initial'][0]['hex']=b.hex()
  self.reject(edit,full=True)
 def test_PC_trace_tamper_rejected(self):self.reject(lambda r:r['code_trace'].__setitem__(0,0),full=True)
 def test_missing_write_rejected(self):self.reject(lambda r:r['write_trace'].pop(),full=True)
 def test_cpu_flags_tamper_rejected_by_full_replay(self):
  r=self.row(4);r['event']['call']['cpu_after']['EFLAGS']^=1
  with self.assertRaises(ValueError):v.verify_case(r,True)
 def test_false_API_provenance_rejected(self):self.reject(lambda r:r['APIs'][0].__setitem__('actual_API_executed',False),full=True)
 def test_root_API_arguments_rejected(self):self.reject(lambda r:r['event']['call']['args'].append(1),full=True)
 def test_unlock_claim_rejected(self):self.reject(lambda r:r.__setitem__('OS_input_submitted',True),full=True)


if __name__=='__main__':unittest.main()
