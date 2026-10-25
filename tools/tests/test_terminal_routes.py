"""Terminal source routes: branch differences, unresolved reads and forged claims."""
import copy,gzip,json,struct,unittest
from tools import terminal_route_catalog as c
from tools import terminal_route_verification as v

REPORT='analysis/terminal-routes-source-v2-20261025.json.gz'


class TerminalRoutesTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.report=json.loads(gzip.decompress((c.ROOT/REPORT).read_bytes()))
 def route(self,report=None,name='T0004.BIN',sub=2):
  return next(r for s in (report or self.report)['scripts'] if s['name']==name for r in s['routes'] if r['sub']==sub)
 def reject(self,edit):
  d=copy.deepcopy(self.report);edit(d)
  with self.assertRaises((ValueError,KeyError)):v.verify(d)
 def test_complete_independent_atlas(self):
  d=v.verify(self.report);self.assertTrue(d['independent_raw_container_and_CFG']);self.assertFalse(d['new_runtime_execution'])
  s=d['summary'];self.assertEqual([s[k] for k in ('script_files','candidate_slots','present','empty_dmf','commands','opcode_classes')],[45,225,195,30,15568,48])
 def test_source_rebuild_equal(self):self.assertEqual(c.build(),self.report)
 def test_thirteen_condition_refusals(self):
  pairs={(s['name'],r['sub']) for s in self.report['scripts'] for r in s['routes'] if r['status']=='present' and r['modes'].get('condition_accepts') is False}
  expected={('T0022.BIN',n) for n in c.SLOTS}|{(name,n) for name in ('T0037.BIN','T0048.BIN') for n in (2,5,8)}|{('T0045.BIN',n) for n in (11,14)}
  self.assertEqual(pairs,expected)
 def test_t4_mode0_and_mode1_diverge(self):
  for sub in c.SLOTS:
   r=self.route(sub=sub);m=r['modes'];self.assertTrue(m['condition_accepts']);self.assertEqual(m['condition_path'][:4],[0,8,28,36])
   self.assertEqual(m['playback_entry'],44);self.assertNotIn(28,m['playback_reachable'])
   first=next(x for x in r['commands'] if x['PC']==44);self.assertEqual((first['opcode'],first['hex']), (117,'750008003c000020'))
 def test_seven_nonstandard_candidates(self):
  pairs={(s['name'],r['sub']) for s in self.report['scripts'] for r in s['routes'] if r['status']=='present' and r['modes']['kind']=='nonstandard_unresolved'}
  self.assertEqual(pairs,{('T0080.BIN',8),('T0082.BIN',8),('T0086.BIN',5),('T0086.BIN',8),('T0090.BIN',2),('T0090.BIN',5),('T0090.BIN',8)})
 def test_short_handlers_keep_unresolved_edges(self):
  rows=[(s['name'],r,x) for s in self.report['scripts'] for r in s['routes'] if r['status']=='present' for x in r['commands'] if x['short_handler_read']]
  self.assertEqual(len(rows),7)
  for name,r,x in rows:
   self.assertLess(x['bytes'],x['handler_required_bytes']);self.assertEqual(len(bytes.fromhex(x['hex'])),x['bytes'])
   self.assertFalse(any(e['source']==x['PC'] for e in r['edges']))
   self.assertIn(dict(PC=x['PC'],kind='handler_reads_beyond_declared_command'),r['issues'])
 def test_end_only_candidates_not_standard(self):
  for sub in (5,8):
   r=self.route(name='T0086.BIN',sub=sub);self.assertEqual([x['opcode'] for x in r['commands']],[19]);self.assertEqual(r['edges'],[])
 def test_original_animation_is_stateful_update(self):
  f=next(f for f in self.report['source']['functions'] if f['start']==0x499910)
  self.assertEqual([i['target'] for i in f['direct_calls']],[0x415040,0x456B20,0x415070,0x49AD50,0x49AD50,0x415040,0x415040,0x56CE80])
  self.assertGreater(f['end']-f['start'],500)
 def test_prior_evidence_not_new_execution(self):
  h=self.report['handoff'];self.assertEqual(len(h['cases']),7);self.assertFalse(h['new_runtime_execution']);self.assertFalse(h['task_exit_complete']);self.assertEqual(h['cases'][4]['selector'],0)
 def test_missing_script_refused(self):self.reject(lambda d:d['scripts'].pop())
 def test_missing_candidate_refused(self):self.reject(lambda d:d['scripts'][0]['routes'].pop())
 def test_forged_dynamic_reachability_refused(self):self.reject(lambda d:self.route(d).update(dynamic_scene_reachability_proven=True))
 def test_changed_script_hash_refused(self):self.reject(lambda d:d['scripts'][0]['source'].update(sha256='0'*64))
 def test_missing_command_refused(self):self.reject(lambda d:self.route(d)['commands'].pop())
 def test_changed_command_bytes_refused(self):self.reject(lambda d:self.route(d)['commands'][0].update(hex='0000000000000000'))
 def test_omitted_branch_refused(self):self.reject(lambda d:self.route(d)['edges'].pop(1))
 def test_false_mode_path_refused(self):self.reject(lambda d:self.route(d)['modes'].update(playback_reachable=[0]))
 def test_false_condition_accept_refused(self):self.reject(lambda d:self.route(d,name='T0022.BIN')['modes'].update(condition_accepts=True))
 def test_hidden_short_read_refused(self):self.reject(lambda d:self.route(d,name='T0080.BIN',sub=8)['commands'][0].update(short_handler_read=False))
 def test_forged_summary_refused(self):self.reject(lambda d:d['summary'].update(CFG_issues=0))
 def test_missing_function_instruction_refused(self):self.reject(lambda d:d['source']['functions'][0]['instructions'].pop())
 def test_changed_finalizer_call_refused(self):self.reject(lambda d:next(i for i in d['source']['key_instructions'] if i['va']==0x454793).update(operands='0x401000'))
 def test_phase20_false_return_refused(self):self.reject(lambda d:d['source']['task_phase_table']['targets'].__setitem__(20,0x4547A8))
 def test_changed_dispatch_refused(self):self.reject(lambda d:d['dispatch'][0].update(entry=0))
 def test_forged_task_exit_refused(self):self.reject(lambda d:d['handoff'].update(task_exit_complete=True))
 def test_forged_R6_refused(self):self.reject(lambda d:d.update(R6_complete=True))
 def test_unknown_report_field_refused(self):self.reject(lambda d:d.update(real_game_finished=True))
 def test_malformed_independent_container_refused(self):
  for raw in (b'',bytes(8),struct.pack('<II',8,100),struct.pack('<IIII',16,2,16,12)):
   with self.assertRaises((ValueError,struct.error)):v.scan(raw)
 def test_jump_into_payload_is_unknown(self):
  row=dict(PC=0,opcode=11,bytes=8,hex=struct.pack('<HHI',11,8,6).hex(),short_handler_read=False)
  edges,issues=v.control([row],8);self.assertEqual(edges,[]);self.assertEqual(issues,[dict(PC=0,kind='invalid_target',target=6)])
 def test_falloff_is_not_END(self):
  row=dict(PC=0,opcode=21,bytes=4,hex='15000400',short_handler_read=False)
  edges,issues=v.control([row],4);self.assertEqual(edges,[]);self.assertEqual(issues,[dict(PC=0,kind='falloff',target=4)])


if __name__=='__main__':unittest.main()
