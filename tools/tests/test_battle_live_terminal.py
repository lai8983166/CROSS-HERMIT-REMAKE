import copy,gzip,json,unittest
from unittest.mock import patch
from tools import battle_live_terminal_emulation as e
from tools import battle_live_terminal_model as m
from tools import battle_live_terminal_verification as v
from tools.battle_lethal_combat import expand

REPORT='analysis/battle-live-terminal-source-v2-20261025.json'
REPORT_SHA='83a0ef8627836c1aa839f2f1b73e4ab073bdb0646bdb99283e9bf672e6bb244e'


class LiveTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  raw=(e.ROOT/REPORT).read_bytes();assert REPORT_SHA is not None and e.sha(raw)==REPORT_SHA
  cls.bundle=json.loads(raw);cls.rows=[]
  for r in cls.bundle['case_reports']:
   raw=(e.ROOT/r['path']).read_bytes();assert len(raw)==r['bytes'] and e.sha(raw)==r['sha256'];cls.rows.append(json.loads(gzip.decompress(raw))['cases'][0])

 def row(self,i=6):return copy.deepcopy(self.rows[i])
 def test_all_seven_original_contracts(self):
  for r in self.rows:
   with self.subTest(case=r['input']['name']):self.assertFalse(v.verify_case(r,False)['all_owned_memory_CPU_trace_replayed'])
 def test_no_combat_snapshot_loader_called(self):
  with patch.object(e.terminal,'combat',side_effect=AssertionError('snapshot loader forbidden')),patch.object(e.terminal,'accepted',side_effect=AssertionError('snapshot acceptance loader forbidden')):
   f=e.LiveMachine(e.corpus()[6]);self.assertEqual(f.get(e.RECORD+0x116,'h'),70);self.assertEqual(f.get(e.CTRL+0x108B3A,'B'),1)
 def test_runtime_host_put_only_writes_root_stack(self):
  f=e.LiveMachine(e.corpus()[6]);original=f.put
  def guarded(at,*args):
   self.assertTrue(0x12000000<=at<0x12020000,'derived host write');return original(at,*args)
  f.put=guarded;r=f.run();self.assertEqual(len(r['world_frames']),3)
 def test_frozen_source_and_root_ABI_algorithm(self):
  self.assertIs(e.LiveMachine.source_code.__code__,e.terminal.TerminalMachine.source_code.__code__);self.assertIs(e.LiveMachine.base_call.__code__,e.terminal.TerminalMachine.base_call.__code__)
 def test_actual_timeout_clock(self):
  r=self.rows[6];self.assertEqual([(expand(s['before'],r['blobs'])['remaining'],expand(s['before'],r['blobs'])['elapsed']) for s in r['events']],[(2,1),(1,2),(0,3)])
 def test_timeout_before_any_attack(self):
  r=self.rows[6];self.assertFalse(r['hit']);self.assertEqual(m.event_contract(r,2)['selector'],4)
 def test_threshold_continues_without_terminal(self):
  r=self.rows[4];self.assertEqual(len(r['world_frames']),192);self.assertEqual(m.event_contract(r,191)['selector'],0);self.assertEqual(m.world_contracts(r)['HP'][1],1)
 def test_neutral_terminal_first_world(self):
  r=self.rows[5];self.assertEqual(len(r['world_frames']),1);self.assertEqual(m.event_contract(r,0)['selector'],1);self.assertFalse(r['hit'])
 def test_both_jobs_and_death_roles(self):
  for i,r in enumerate(self.rows[:4]):
   self.assertTrue(all(n>0 for n in m.world_contracts(r)['hits_by_side']));self.assertEqual(m.event_contract(r,len(r['events'])-1)['selector'],1 if i%2==0 else 5)
 def test_original_clock_function_not_stubbed(self):
  for f in self.rows[6]['world_frames']:
   self.assertEqual([x['args'] for x in f['gated_calls'] if x['entry']==0x415040 and x['caller']==0x467BD2],[[1]])
 def test_unknown_input_rejected(self):
  with self.assertRaises(ValueError):e.LiveMachine(dict(e.corpus()[0],budget=1))
 def test_boolean_limit_rejected(self):
  with self.assertRaises(ValueError):e.validate(dict(e.corpus()[6],limit=True))
 def test_unknown_PC_rejected(self):
  f=e.LiveMachine(e.corpus()[6])
  with self.assertRaises(ValueError):f.source_code(f.uc,0x401000,1,None)
 def test_forbidden_original_write_rejected(self):
  f=e.LiveMachine(e.corpus()[6])
  with self.assertRaises(ValueError):f.write_hook(f.uc,0,e.SCRIPT,4,0,None)
 def test_regions_disjoint(self):
  a=sorted(e.REGIONS);self.assertEqual(len(a),45)
  for (p,n),(q,k) in zip(a,a[1:]):self.assertLessEqual(p+n,q)
 def test_coupled_clock_tamper_rejected(self):
  r=self.row();r['events'][0]['before']['remaining']=1;r['events'][0]['after']['remaining']=1;r['world_frames'][0]['after']['terminal_state']['remaining']=1
  with self.assertRaises(ValueError):m.event_contract(r,0)
 def test_elapsed_tamper_rejected(self):
  r=self.row();r['events'][0]['after']['elapsed']=2
  with self.assertRaises(ValueError):m.event_contract(r,0)
 def test_gated_body_omission_rejected(self):
  r=self.row();r['world_frames'][0]['gated_calls'].pop()
  with self.assertRaises(ValueError):v.verify_case(r,False)
 def test_world_slot_scan_omission_rejected(self):
  r=self.row();r['world_frames'][0]['scanned_slots'].pop()
  with self.assertRaises(ValueError):v.verify_case(r,False)
 def test_explicit_attack_control_rejected(self):
  r=self.row();r['world_frames'][0]['controls'].append(dict(command=6))
  with self.assertRaises(ValueError):v.verify_case(r,False)
 def test_original_clock_call_site_rejected(self):
  r=self.row();r['world_frames'][0]['gated_calls'][0]['caller']=0
  with self.assertRaises(ValueError):v.verify_case(r,False)
 def test_missing_event_rejected(self):
  r=self.row();r['events'].pop()
  with self.assertRaises(ValueError):v.verify_case(r,False)
 def test_event_digest_chain_rejected(self):
  r=self.row();r['events'][0]['trace_before']['code_sha256']='0'*64
  with self.assertRaises(ValueError):v.verify_case(r,False)
 def test_root_instruction_interval_rejected(self):
  r=self.row();r['world_frames'][0]['call']['instructions']+=1
  with self.assertRaises(ValueError):v.verify_case(r,False)
 def test_HP_store_PC_tamper_rejected(self):
  r=self.row(0);r['both_hp_writes'][0]['pc']=0
  with self.assertRaises(ValueError):m.world_contracts(r)
 def test_random_stream_tamper_rejected(self):
  r=self.row();event=next(x for x in r['contracts'] if x['entry']==0x467E00);event['result']^=1
  with self.assertRaises(ValueError):m.world_contracts(r)
 def test_terminal_request_fields_rejected(self):
  r=self.row();event=next(x for x in r['calls'] if x['entry']==0x4549D0);event['args'][3]=0
  with self.assertRaises(ValueError):m.event_contract(r,2)
 def test_condition_opcode_rejected(self):
  r=self.row();r['commands'][0]['opcode']=166
  with self.assertRaises(ValueError):m.event_contract(r,2)
 def test_final_result_page_rejected(self):
  r=self.row();b=bytearray.fromhex(expand(r['finalization']['after'],r['blobs'])['result']);b[0x50C]^=1;r['finalization']['after']['result']=b.hex();o=m.event_contract(r,2)
  with self.assertRaises(ValueError):m.finalization_contract(r,o)
 def test_last_CPU_flags_rejected_by_fresh_replay(self):
  r=self.row();r['world_frames'][-1]['call']['cpu_after']['EFLAGS']^=1
  with self.assertRaises(ValueError):v.verify_case(r,True)
 def test_final_digest_rejected_by_fresh_replay(self):
  r=self.row();r['code_trace_sha256']='0'*64
  with self.assertRaises(ValueError):v.verify_case(r,True)
 def test_forged_input_claim_rejected(self):
  r=self.row();r['OS_input_submitted']=True
  with self.assertRaises(ValueError):v.verify_case(r,False)


if __name__=='__main__':unittest.main()
