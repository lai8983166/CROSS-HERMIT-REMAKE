"""Bounded original source and per-creation identity guards for multiline."""
import contextlib,copy,gzip,io,json,struct,tempfile,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from tools import terminal_last_dialogue_emulation as e
from tools import terminal_last_dialogue_gdi as gdi

class TerminalLastDialogueSourceTests(unittest.TestCase):
 def test_original_both_multiline_command_windows(self):
  from tools import terminal_next_dialogue_verification as v
  raw=(e.ROOT/e.terminal.SCRIPT_PATH).read_bytes();segments=v.previous.dialogue.script_commands(raw)['segments']
  for name,final in [('neutral_running',320),('timeout_before_combat',350)]:
   b=e.branch(name);s=next(s for s in segments if s['index']==b['segment']);pc=b['first_PC'];ops=[]
   while pc<final:
    op,n=struct.unpack_from('<HH',raw,s['code_start']+pc);ops.append((pc,op,n));pc+=n
   self.assertEqual(pc,final);self.assertEqual(ops[-2:],[(final-8,50,4),(final-4,51,4)])
   for line in b['lines']:self.assertIn((line['PC'],17,6),ops);self.assertEqual(struct.unpack_from('<H',raw,s['code_start']+line['PC']+4)[0],line['text_index'])
   self.assertEqual(struct.unpack_from('<H',raw,s['code_start']+final)[0],44)
 def test_three_original_records_and_cross_layer_records(self):
  self.assertEqual([(x['layer'],x['record_index']) for x in e.branch('neutral_running')['lines']],[(4,0)])
  self.assertEqual([(x['layer'],x['record_index']) for x in e.branch('timeout_before_combat')['lines']],[(7,0),(7,1),(7,2)])
 def test_invalid_branch_refused(self):
  with self.assertRaises(ValueError):e.branch('neutral_running ')
 def test_projection_ordinal_bounds(self):
  for i in (-1,3,True,'0'):
   with self.assertRaises(ValueError):e.projection_domain(i)
 def test_original_code_range_and_guard_unchanged(self):
  self.assertIs(e.ALLOWED,e.parent.ALLOWED);self.assertIs(e.LastDialogueMachine.source_code,e.parent.MultilineMachine.source_code);self.assertEqual(e.EXTRA_RANGES,())
 def test_recorder_keeps_frozen_instruction_algorithm(self):
  for name in ('mark','capture','prefix_counts','observe','prepare','gdi','segment','frame','resume_frame','font','finish_resource','actual_root'):
   old=getattr(e.followup.FollowupMachine,'fu_'+name);new=getattr(e.LastDialogueMachine,'ld_'+name);self.assertEqual(old.__code__.co_code,new.__code__.co_code);self.assertIs(old.__globals__,new.__globals__)
  self.assertEqual(e.LastDialogueMachine._ld_gpu_api.__code__.co_code,e.followup.FollowupMachine.gpu_api.__code__.co_code)
 def test_bounded_namespace_and_separate_rasters(self):
  self.assertEqual(len(set(e.RASTERS)),3);self.assertTrue(all(a%4096==0 for a in e.RASTERS));self.assertLess(e.LAST_DIALOGUE_NEXT_MAX,e.GDI_GUEST_START);self.assertEqual(e.LAST_DIALOGUE_NEXT_MAX-e.GPU_GUEST_START,21*e.PROJECTION_STRIDE)
 def projection(self,index=0):
  b=e.branch('timeout_before_combat');line=b['lines'][index];r=dict(kind='text',record=e.record_at(line['layer'],line['record_index']),creation_index=index,projection_domain=e.projection_domain(index));p=object.__new__(e.LastDialogueProjection);p.machine=SimpleNamespace(ld_current=r,ld_branch=b);p.prefix=[dict(domain='overlay',native=1,guest=0x64001000)]
  class Space:
   def __init__(self):self.rows=copy.deepcopy(p.prefix);self.next=e.GPU_GUEST_START
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
  p,r=self.projection();r['projection_domain']='overlay-last-dialogue-2'
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
  with tempfile.TemporaryDirectory() as tmp,patch.dict(e.save_source.__globals__,ROOT=Path(tmp)):
   value=dict(raw='aa'*10000,text='夏朧',cases=[1,None]);e.save_source('source.json.gz',value);p=Path(tmp)/'source.json.gz';self.assertEqual(json.loads(gzip.decompress(p.read_bytes())),value);self.assertEqual(p.read_bytes()[4:8],bytes(4))
   with self.assertRaises(ValueError):e.save_source('source.json.gz',value)

 def machine(self,regions=None):
  space=e.overlay.AddressSpace();space.next=0x64001000;space.guest('overlay',1);return SimpleNamespace(space=space,live_input=dict(name='neutral_running'),uc=SimpleNamespace(mem_regions=lambda:regions if regions is not None else [(0x400000,0x401FFF,5)]))
 def test_new_namespace_preserves_all_parent_bindings(self):
  m=self.machine();before=m.space.ledger();oldnext=m.space.next;p=e.LastDialogueProjection(m);self.assertEqual(m.space.ledger(),before);self.assertEqual(p.prefix_next,oldnext);self.assertEqual(m.space.next,e.GPU_GUEST_START);self.assertTrue(p.namespace['all_before_mappings_disjoint']);self.assertEqual(m.space.guest.__func__.__code__,e.overlay.AddressSpace.guest.__code__)
 def test_new_namespace_refuses_any_existing_mapped_byte(self):
  for region in [(e.GPU_GUEST_START-4096,e.GPU_GUEST_START,7),(e.LAST_DIALOGUE_NEXT_MAX-1,e.LAST_DIALOGUE_NEXT_MAX+4096,7)]:
   with self.subTest(region=region),self.assertRaises(ValueError):e.LastDialogueProjection(self.machine([region]))
 def test_new_namespace_refuses_retired_parent_identity(self):
  m=self.machine();m.space.native_to_guest[('overlay',2)]=e.GPU_GUEST_START
  with self.assertRaises(ValueError):e.LastDialogueProjection(m)
 def test_exact_current_helper_capacity_contract(self):
  c=e.experimental_helper_contract();self.assertEqual((c['max_textures'],c['max_creates']),(11,32));self.assertTrue(c['only_live_capacity_changed']);self.assertTrue(c['duplicate_live_address_still_rejected'])

class GDILifetimeProjectionTests(unittest.TestCase):
 def projection(self,steps,plan=None,allow_new=True):
  class Service:
   actual=100
   def __init__(self):self.steps=copy.deepcopy(steps);self.observed=[]
   def call(self,machine,name,args,ret):
    expected_name,expected_args,response=self.steps.pop(0)
    if (name,args)!=(expected_name,expected_args):raise AssertionError((name,args,expected_name,expected_args))
    self.observed.append((name,list(args),ret));return response
   def close(self):return dict(measurement_DC=100,deleted=True)
  platform=SimpleNamespace(service=Service(),trace=[],measure=0x6A001000)
  case=dict(initial_measurement_dc=dict(guest=platform.measure,role='measurement_dc'),calls=plan or [])
  return gdi.LifetimeGDI(platform,case,dict(test=True),lambda:allow_new)
 def response(self,value):return dict(result=value,memory_outputs=[dict(pointer=123,hex='aaff00')],padding_hex='ee',native_bits=456,dc_translated_args=[789])
 def entry(self,n,name,args=(),result=None):
  out=dict(ordinal=n,name=name,argument_handles=[dict(index=i,guest=guest,role=role) for i,guest,role in args])
  if result is not None:out['result_handle']=dict(guest=result[0],role=result[1])
  return out
 def create_delete_plan(self):
  return [self.entry(0,'CreateFontA',result=(0x6A101000,'owned_font_0')),self.entry(1,'DeleteObject',[(0,0x6A101000,'owned_font_0')]),self.entry(2,'CreateFontA',result=(0x6A301000,'owned_font_1'))]
 def test_native_reissue_and_nonreissue_project_same_parent_guests(self):
  for second in (200,300):
   steps=[('CreateFontA',[20],self.response(200)),('DeleteObject',[200],self.response(1)),('CreateFontA',[20],self.response(second))]
   p=self.projection(steps,self.create_delete_plan());first=p.call(None,'CreateFontA',[20],0);p.call(None,'DeleteObject',[first['result']],0);last=p.call(None,'CreateFontA',[20],0)
   self.assertEqual((first['result'],last['result']),(0x6A101000,0x6A301000));self.assertFalse(p.lifetimes[1]['alive']);self.assertEqual(p.lifetimes[2]['native'],second);self.assertNotEqual(p.calls[0]['result_binding']['lifetime'],p.calls[2]['result_binding']['lifetime'])
 def test_new_creation_is_fresh_even_when_native_number_reissued(self):
  p=self.projection([('CreateFontA',[20],self.response(200)),('DeleteObject',[200],self.response(1)),('CreateFontA',[20],self.response(200))])
  a=p.call(None,'CreateFontA',[20],0)['result'];p.call(None,'DeleteObject',[a],0);b=p.call(None,'CreateFontA',[20],0)['result'];self.assertNotEqual(a,b)
  with self.assertRaises(ValueError):p.native('GDI',a)
  self.assertEqual(p.native('GDI',b),200);self.assertEqual(len([r for r in p.ledger() if r['native']==200]),2)
 def test_native_payload_and_memory_outputs_remain_unmodified(self):
  observed=self.response(200);p=self.projection([('CreateFontA',[20],observed)]);r=p.call(None,'CreateFontA',[20],1234)
  self.assertEqual(p.trace[0]['native_result'],observed);self.assertEqual(r['memory_outputs'],observed['memory_outputs']);self.assertEqual(r['padding_hex'],'ee');self.assertEqual(p.trace[0]['native_args'],[20]);self.assertEqual(p.service.observed,[('CreateFontA',[20],1234)])
 def test_two_live_owned_native_aliases_are_rejected(self):
  p=self.projection([('CreateFontA',[20],self.response(200)),('CreateFontA',[20],self.response(200))]);p.call(None,'CreateFontA',[20],0)
  with self.assertRaisesRegex(ValueError,'native GDI handle already'):p.call(None,'CreateFontA',[20],0)
 def test_two_live_guest_aliases_are_rejected(self):
  plan=[self.entry(0,'CreateFontA',result=(0x6A101000,'owned_font_0')),self.entry(1,'CreateFontA',result=(0x6A101000,'owned_font_1'))]
  p=self.projection([('CreateFontA',[20],self.response(200)),('CreateFontA',[20],self.response(300))],plan);p.call(None,'CreateFontA',[20],0)
  with self.assertRaisesRegex(ValueError,'guest GDI handle already'):p.call(None,'CreateFontA',[20],0)
 def test_failed_deletion_cannot_retire_or_allow_native_reuse(self):
  p=self.projection([('CreateFontA',[20],self.response(200)),('DeleteObject',[200],self.response(0)),('CreateFontA',[20],self.response(200))]);a=p.call(None,'CreateFontA',[20],0)['result'];self.assertEqual(p.call(None,'DeleteObject',[a],0)['result'],0)
  self.assertTrue(p.lifetimes[1]['alive']);self.assertIsNone(p.calls[1]['deleted_lifetime'])
  with self.assertRaises(ValueError):p.call(None,'CreateFontA',[20],0)
 def test_stock_and_selectobject_follow_actual_active_owner(self):
  p=self.projection([('CreateFontA',[20],self.response(200)),('SelectObject',[100,200],self.response(500)),('SelectObject',[100,500],self.response(200)),('GetStockObject',[4],self.response(600)),('GetStockObject',[4],self.response(600))])
  font=p.call(None,'CreateFontA',[20],0)['result'];stock=p.call(None,'SelectObject',[0x6A001000,font],0)['result'];old=p.call(None,'SelectObject',[0x6A001000,stock],0)['result'];self.assertEqual(old,font);self.assertEqual(p.calls[1]['result_binding']['role'],'default_font')
  a=p.call(None,'GetStockObject',[4],0)['result'];b=p.call(None,'GetStockObject',[4],0)['result'];self.assertEqual(a,b);self.assertEqual(p.calls[-1]['result_binding']['role'],'stock_object_4')
 def test_selectobject_cannot_pin_wrong_native_previous_owner(self):
  p=self.projection([('CreateFontA',[20],self.response(200)),('SelectObject',[100,200],self.response(500)),('SelectObject',[100,500],self.response(999))]);font=p.call(None,'CreateFontA',[20],0)['result'];stock=p.call(None,'SelectObject',[0x6A001000,font],0)['result']
  with self.assertRaisesRegex(ValueError,'previously selected live owner'):p.call(None,'SelectObject',[0x6A001000,stock],0)
 def test_new_stage_call_before_prefix_consumed_is_rejected(self):
  p=self.projection([],allow_new=False)
  with self.assertRaisesRegex(ValueError,'prefix fully consumed'):p.call(None,'CreateFontA',[20],0)
 def test_deleted_planned_guest_slot_may_have_a_new_lifetime(self):
  plan=self.create_delete_plan();plan[2]['result_handle']['guest']=0x6A101000;p=self.projection([('CreateFontA',[20],self.response(200)),('DeleteObject',[200],self.response(1)),('CreateFontA',[20],self.response(300))],plan)
  a=p.call(None,'CreateFontA',[20],0)['result'];p.call(None,'DeleteObject',[a],0);self.assertEqual(p.call(None,'CreateFontA',[20],0)['result'],a);self.assertEqual(p.native('GDI',a),300);self.assertEqual(len([r for r in p.ledger() if r['guest']==a]),1);self.assertEqual(len(p.lifetimes),3)
 def test_owner_cleanup_reports_measurement_dc_retirement_once(self):
  p=self.projection([]);p.close();p.close();r=p.report();self.assertEqual(r['owner_cleanup']['retired_lifetimes'],[0]);self.assertEqual(r['lifetimes'][0]['created_call'],-1);self.assertEqual(r['lifetimes'][0]['retired_by'],'service.close');self.assertFalse(r['lifetimes'][0]['alive'])
 def test_fixed_plan_contains_only_opaque_handle_positions(self):
  plan=gdi.fixed_plan(e.ROOT)
  for case in plan['cases']:
   for i,r in enumerate(case['calls']):
    self.assertEqual(r['ordinal'],i);self.assertEqual([a['index'] for a in r['argument_handles']],list(gdi.handle_indices(r['name'])));self.assertEqual('result_handle' in r,r['name'] in gdi.HANDLE_RESULTS);self.assertEqual(set(r),{'ordinal','name','argument_handles'}|({'result_handle'} if r['name'] in gdi.HANDLE_RESULTS else set()))

if __name__=='__main__':unittest.main()
