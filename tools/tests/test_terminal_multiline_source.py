"""Bounded original source and per-creation identity guards for multiline."""
import contextlib,copy,gzip,io,json,struct,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from tools import terminal_multiline_emulation as e

class TerminalMultilineSourceTests(unittest.TestCase):
 def test_original_both_multiline_command_windows(self):
  from tools import terminal_next_dialogue_verification as v
  raw=(e.ROOT/e.terminal.SCRIPT_PATH).read_bytes();segments=v.previous.dialogue.script_commands(raw)['segments']
  for name,final in [('neutral_running',294),('timeout_before_combat',312)]:
   b=e.branch(name);s=next(s for s in segments if s['index']==b['segment']);pc=b['first_PC'];ops=[]
   while pc<final:
    op,n=struct.unpack_from('<HH',raw,s['code_start']+pc);ops.append((pc,op,n));pc+=n
   self.assertEqual(pc,final);self.assertEqual(ops[-2:],[(final-8,50,4),(final-4,51,4)])
   for line in b['lines']:self.assertIn((line['PC'],17,6),ops);self.assertEqual(struct.unpack_from('<H',raw,s['code_start']+line['PC']+4)[0],line['text_index'])
   self.assertEqual(struct.unpack_from('<H',raw,s['code_start']+final)[0],43)
 def test_three_original_records_and_cross_layer_records(self):
  self.assertEqual([(x['layer'],x['record_index']) for x in e.branch('neutral_running')['lines']],[(7,0),(7,1),(7,2)])
  self.assertEqual([(x['layer'],x['record_index']) for x in e.branch('timeout_before_combat')['lines']],[(7,0),(5,0)])
 def test_invalid_branch_refused(self):
  with self.assertRaises(ValueError):e.branch('neutral_running ')
 def test_projection_ordinal_bounds(self):
  for i in (-1,3,True,'0'):
   with self.assertRaises(ValueError):e.projection_domain(i)
 def test_original_code_range_and_guard_unchanged(self):
  self.assertIs(e.ALLOWED,e.parent.ALLOWED);self.assertIs(e.MultilineMachine.source_code,e.parent.NextDialogueMachine.source_code);self.assertEqual(e.EXTRA_RANGES,())
 def test_recorder_keeps_frozen_instruction_algorithm(self):
  for name in ('mark','capture','prefix_counts','observe','prepare','gdi','segment','frame','resume_frame','font','finish_resource','actual_root'):
   old=getattr(e.followup.FollowupMachine,'fu_'+name);new=getattr(e.MultilineMachine,'ml_'+name);self.assertEqual(old.__code__.co_code,new.__code__.co_code);self.assertIs(old.__globals__,new.__globals__)
  self.assertEqual(e.MultilineMachine._ml_gpu_api.__code__.co_code,e.followup.FollowupMachine.gpu_api.__code__.co_code)
 def test_bounded_namespace_and_separate_rasters(self):
  self.assertEqual(len(set(e.RASTERS)),3);self.assertTrue(all(a%4096==0 for a in e.RASTERS));self.assertLess(e.MULTILINE_NEXT_MAX,e.GDI_GUEST_START);self.assertEqual(e.MULTILINE_NEXT_MAX-e.PREFIX_NEXT_MAX,21*e.PROJECTION_STRIDE)
 def projection(self,index=0):
  b=e.branch('neutral_running');line=b['lines'][index];r=dict(kind='text',record=e.record_at(line['layer'],line['record_index']),creation_index=index,projection_domain=e.projection_domain(index));p=object.__new__(e.MultilineProjection);p.machine=SimpleNamespace(ml_current=r,ml_branch=b);p.prefix=[dict(domain='overlay',native=1,guest=0x64001000)]
  class Space:
   def __init__(self):self.rows=copy.deepcopy(p.prefix);self.next=0x64101000
   def ledger(self):return copy.deepcopy(self.rows)
   def result(self,domain,value,key=None):
    for i in range(6 if 'texture' in value else 1):self.rows.append(dict(domain=domain,native=10+len(self.rows),guest=self.next));self.next+=e.PROJECTION_STRIDE
    return copy.deepcopy(value)
  p.space=Space();return p,r
 def test_projected_actual_creation_and_surface_have_seven_keys(self):
  p,r=self.projection();p.result('overlay',dict(texture={}));p.result('overlay',dict(bits=123));self.assertEqual(len(p.space.rows),8);self.assertEqual(p.space.rows[0],p.prefix[0])
 def test_projection_requires_exact_original_record(self):
  p,r=self.projection();r['record']+=4
  with self.assertRaises(ValueError):p.result('overlay',dict(texture={}))
 def test_projection_requires_creation_domain(self):
  p,r=self.projection();r['projection_domain']='overlay-multiline-2'
  with self.assertRaises(ValueError):p.result('overlay',dict(texture={}))
 def test_projection_refuses_parent_ledger_rewrite(self):
  p,r=self.projection();p.space.rows[0]['guest']+=4
  with self.assertRaises(ValueError):p.result('overlay',dict(texture={}))
 def test_projection_refuses_extra_identity(self):
  p,r=self.projection();p.result('overlay',dict(texture={}));p.result('overlay',dict(bits=123))
  with self.assertRaises(ValueError):p.result('overlay',dict(bits=456))
 def test_projection_refuses_other_native_domain(self):
  p,r=self.projection()
  with self.assertRaises(ValueError):p.result('guessed',dict(texture={}))
 def prefix(self,change=False):
  want=dict(instructions=10,writes=5,code_sha256='a'*64,write_sha256='b'*64);actual=dict(want,instructions=11) if change else want;m=SimpleNamespace(live_input=dict(name='neutral_running'),mark=lambda:actual)
  with patch.object(e,'fixed_parent_forward_summaries',return_value=dict(neutral_running=want)),contextlib.redirect_stdout(io.StringIO()):return e.validate_parent_prefix(m)
 def test_fixed_parent_preflight_records_all_four_fields(self):self.assertEqual(self.prefix()['expected'],self.prefix()['actual'])
 def test_fixed_parent_preflight_rejects_extra_original_event(self):
  with self.assertRaises(ValueError):self.prefix(True)
 def test_original_helper_capacity_and_ABI_unchanged(self):self.assertTrue(e.helper_contract()['capacity_and_ABI_unchanged'])
 def test_stream_writer_preserves_values_and_refuses_overwrite(self):
  with tempfile.TemporaryDirectory() as tmp,patch.object(e.parent,'ROOT',Path(tmp)):
   value=dict(raw='aa'*10000,text='夏朧',cases=[1,None]);e.save_source('source.json.gz',value);p=Path(tmp)/'source.json.gz';self.assertEqual(json.loads(gzip.decompress(p.read_bytes())),value);self.assertEqual(p.read_bytes()[4:8],bytes(4))
   with self.assertRaises(ValueError):e.save_source('source.json.gz',value)

if __name__=='__main__':unittest.main()
