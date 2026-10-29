"""Small next-dialogue recorder guards; no native instance or large source decode."""
import copy,gzip,json,struct,tempfile,types,unittest
from pathlib import Path
from unittest.mock import patch
from tools import terminal_next_dialogue_emulation as e

class TerminalNextDialogueSourceTests(unittest.TestCase):
 def test_unchanged_guest_code_and_host_write_guards(self):
  self.assertIs(e.NextDialogueMachine.source_code,e.parent.ReplacementMachine.source_code)
  self.assertIs(e.NextDialogueMachine.put,e.parent.ReplacementMachine.put)
  self.assertIs(e.ALLOWED,e.parent.ALLOWED);self.assertIs(e.RANGES,e.parent.RANGES);self.assertIs(e.REFERENCE,e.parent.REFERENCE)
  self.assertEqual(e.EXTRA_RANGES,())
 def test_exact_two_script_boundaries(self):
  for name,first,role,text,pc,ready,final,scene,segment in (('neutral_running',230,None,5,242,252,256,76,2),('timeout_before_combat',226,2,7,254,264,268,77,11)):
   b=e.branch(name);self.assertEqual((b['first_PC'],b['role'],b['text_index'],b['text_PC'],b['ready_PC'],b['final_PC'],b['scene_capture'],b['segment']),(first,role,text,pc,ready,final,scene,segment))
   self.assertEqual((b['configuration'],b['layer'],b['object'],b['node']),(7,4,e.OBJECT,e.NODE))
 def test_unknown_branch_rejected(self):
  for n in ('fake','neutral_running ','timeout'):
   with self.subTest(name=n),self.assertRaises(ValueError):e.branch(n)
 def test_recorder_namespace_changes_only_code_names(self):
  for target,source in (('nd_mark','fu_mark'),('nd_capture','fu_capture'),('nd_prefix_counts','fu_prefix_counts'),('nd_observe','fu_observe'),('_nd_prepare','fu_prepare'),('nd_gdi','fu_gdi'),('nd_segment','fu_segment'),('nd_frame','fu_frame'),('nd_resume_frame','fu_resume_frame'),('nd_font','fu_font'),('nd_finish_resource','fu_finish_resource'),('_nd_captured','fu_captured'),('_nd_gpu_api','gpu_api'),('_nd_api_crt','api_crt'),('nd_actual_root','fu_actual_root')):
   old=getattr(e.parent.parent.FollowupMachine,source);new=getattr(e.NextDialogueMachine,target)
   self.assertIs(new.__globals__,old.__globals__);self.assertIs(new.__closure__,old.__closure__)
   self.assertEqual(new.__code__.replace(co_names=old.__code__.co_names),old.__code__)
   self.assertFalse(any(n.startswith(('fu_','followup_')) for n in new.__code__.co_names))
 def test_parent_admission_keeps_original_code_and_closure(self):
  old=e.parent.ReplacementMachine.admission;new=e.NextDialogueMachine._nd_parent_admission
  self.assertIs(new.__code__,old.__code__);self.assertIs(new.__closure__,old.__closure__)
  self.assertIs(new.__globals__['ReplacementProjection'],e.ReplacementProjection)
  self.assertEqual({k:v for k,v in new.__globals__.items() if k!='ReplacementProjection'},{k:v for k,v in old.__globals__.items() if k!='ReplacementProjection'})
  self.assertIs(e.ReplacementProjection.result,e.parent.ReplacementProjection.result)
 def test_new_gpu_uses_only_next_dialogue_projection(self):
  names=e.NextDialogueMachine._nd_gpu_api.__code__.co_names
  self.assertIn('nd_space',names);self.assertNotIn('space',names)
 def test_unknown_raster_rejected_before_native_access(self):
  m=e.NextDialogueMachine.__new__(e.NextDialogueMachine)
  for p in (0,*e.parent.RASTERS,e.RASTERS[0]+4):
   with self.subTest(pointer=p),self.assertRaises(ValueError):m.nd_set_raster(p)
 def test_separate_new_DIB_addresses(self):
  self.assertEqual(e.RASTERS,(0x3EC00000,0x3ED00000));self.assertTrue(set(e.RASTERS).isdisjoint(e.parent.RASTERS))
 def test_unknown_or_overlapping_resource_rejected(self):
  m=e.NextDialogueMachine.__new__(e.NextDialogueMachine);m.nd_current=None
  with self.assertRaises(ValueError):m.nd_prepare('fake','x',0)
  m.nd_current={}
  with self.assertRaises(ValueError):m.nd_prepare('text','x',0)
 def test_prepare_derives_domain_from_kind(self):
  m=e.NextDialogueMachine.__new__(e.NextDialogueMachine);m.nd_current=None
  r=m.nd_prepare('text','declared',e.TEXTURE)
  self.assertEqual(r['projection_domain'],'overlay-next-dialogue-text');self.assertIs(m.nd_current,r)
 @staticmethod
 def release_fixture(generation=7,record=e.TEXTURE):
  a=dict(generation=7,record=e.TEXTURE,texture=dict(pointer=1234),alive=True);b=copy.deepcopy(a)
  m=types.SimpleNamespace(next_dialogue_ready=True,nd_gpu=[],nx_resources=[a],nx_live={1234:a},fu_resources=[b],fu_live={1234:b})
  m._nd_gpu_api=lambda at:m.nd_gpu.append(dict(op='release',generation=generation,record=record,wire_index=81,phase='forward'))
  return m,a,b
 def test_release_synchronizes_both_parent_ledgers_exact_generation(self):
  m,a,b=self.release_fixture();e.NextDialogueMachine.gpu_api(m,0)
  self.assertFalse(a['alive']);self.assertFalse(b['alive']);self.assertEqual(m.nx_live,{});self.assertEqual(m.fu_live,{})
  self.assertEqual(a['release_wire_index'],81);self.assertEqual(b['released_phase'],'next_dialogue_forward')
 def test_new_generation_pointer_reuse_does_not_release_parent_twice(self):
  m,a,b=self.release_fixture(generation=99);before=copy.deepcopy((a,b));e.NextDialogueMachine.gpu_api(m,0)
  self.assertEqual((a,b),before);self.assertEqual(list(m.nx_live),[1234]);self.assertEqual(list(m.fu_live),[1234])
 def test_parent_wrong_live_generation_rejected(self):
  m,a,b=self.release_fixture();m.nx_live[1234]=dict(a)
  with self.assertRaises(ValueError):e.NextDialogueMachine.gpu_api(m,0)
 def test_parent_wrong_record_rejected(self):
  m,a,b=self.release_fixture(record=e.NAME_RECORD)
  with self.assertRaises(ValueError):e.NextDialogueMachine.gpu_api(m,0)
 def test_already_retired_parent_generation_rejected(self):
  m,a,b=self.release_fixture();a['alive']=False
  with self.assertRaises(ValueError):e.NextDialogueMachine.gpu_api(m,0)
 def test_current_cleanup_routes_both_parent_root_entrypoints(self):
  events=[];m=types.SimpleNamespace(next_dialogue_ready=True,nd_actual_root=lambda *a,**k:events.append((a,k)))
  e.NextDialogueMachine.fu_actual_root(m,'old-root',1);e.NextDialogueMachine.nx_actual_root(m,'old-extra',2)
  self.assertEqual(events,[(('old-root',1),{}),(('old-extra',2),{})])
 def test_no_cleanup_history_replacement(self):
  self.assertIn('super',e.NextDialogueMachine.run.__code__.co_names);self.assertIn('run',e.NextDialogueMachine.run.__code__.co_names)
  self.assertNotIn('nx_cleanup',e.NextDialogueMachine.nx_actual_root.__code__.co_names)
  self.assertNotIn('fu_cleanup',e.NextDialogueMachine.fu_actual_root.__code__.co_names)
 def test_frozen_clock_provider(self):
  self.assertEqual(e.fixed_parent_times.__code__.co_names,('parent','fixed_parent_times'))
 def test_same_native_helpers_and_capacity(self):
  self.assertEqual(e.helper_contract(),e.parent.helper_contract());self.assertEqual(e.helper_contract.__code__.co_names,('parent','helper_contract'))
 @staticmethod
 def prefix_space():
  s=e.overlay.AddressSpace();s.next=0x64001000
  for i,domain in enumerate(('overlay',)+e.parent.PROJECTION_DOMAINS):
   s.result(domain,dict(texture=dict(pointer=0x10000+i*0x1000,vtable=0x20000+i*0x1000,methods={'8':0x20100+i*0x1000,'56':0x20200+i*0x1000,'64':0x20300+i*0x1000,'68':0x20400+i*0x1000})))
   s.result(domain,dict(bits=0x30000+i*0x1000))
  return s
 @classmethod
 def marshal_fixture(cls,reuse):
  s=cls.prefix_space();prefix=copy.deepcopy(s.ledger());m=types.SimpleNamespace(space=s,nd_current=None,get=lambda p:0x12340000,live_input=dict(name='neutral_running'));projection=e.NextDialogueProjection(m);out=[];native=[]
  for i,kind in enumerate(('name','portrait','text')):
   record=e.NAME_RECORD if kind=='name' else e.TEXTURE if kind=='text' else 0x12340000
   m.nd_current=dict(kind=kind,record=record,projection_domain=e.projection_domain(kind))
   p=0x10000 if reuse else 0x11000+i*0x1000;bits=0x30000 if reuse else 0x31000+i*0x1000
   create=dict(hr=0,texture=dict(pointer=p,vtable=0x20000,methods={'8':0x20100,'56':0x20200,'64':0x20300,'68':0x20400}))
   lock=dict(hr=0,pitch=8,bits=bits,locked_hex=struct.pack('<II',8,bits).hex(),hex='a500ff8001020304')
   native.append((copy.deepcopy(create),copy.deepcopy(lock)));out.append((projection.result('overlay',create),projection.result('overlay',lock)))
   cls().assertEqual((create,lock),native[-1])
  return out,s.ledger(),prefix,native
 def test_each_creation_domain_eliminates_retired_native_reuse_dependency(self):
  reused=self.marshal_fixture(True);fresh=self.marshal_fixture(False);self.assertEqual(reused[0],fresh[0])
  for result in (reused,fresh):
   self.assertEqual(result[1][:len(result[2])],result[2]);self.assertEqual([sum(r['domain']==d for r in result[1]) for d in e.PROJECTION_DOMAINS],[7,7,7])
 def test_projection_keeps_every_surface_byte(self):
  out,ledger,prefix,native=self.marshal_fixture(True)
  for (_,lock),(_,original) in zip(out,native):
   self.assertEqual(lock['hex'],original['hex']);self.assertEqual(bytes.fromhex(lock['locked_hex'])[:4],bytes.fromhex(original['locked_hex'])[:4]);self.assertEqual(struct.unpack('<II',bytes.fromhex(lock['locked_hex'])),(lock['pitch'],lock['bits']))
 def test_three_domains_have_distinct_live_interfaces_and_surfaces(self):
  out,*_=self.marshal_fixture(True)
  for key in ('pointer','vtable'):
   self.assertEqual(len({a['texture'][key] for a,b in out}),3)
  self.assertEqual(len({b['bits'] for a,b in out}),3)
 def test_finite_creation_domain_before_access(self):
  for kind in (-1,2,True,'0',None,'text ',[] ):
   with self.subTest(kind=kind),self.assertRaises(ValueError):e.projection_domain(kind)
 def test_wrong_creation_domain_or_record_rejected(self):
  m=types.SimpleNamespace(space=self.prefix_space(),nd_current=dict(kind='text',record=e.TEXTURE,projection_domain=e.PROJECTION_DOMAINS[0]),live_input=dict(name='neutral_running'));p=e.NextDialogueProjection(m)
  with self.assertRaises(ValueError):p.result('overlay',dict(bits=0x40000))
  m.nd_current.update(record=e.TEXTURE+0x110,projection_domain=e.PROJECTION_DOMAINS[2])
  with self.assertRaises(ValueError):p.result('overlay',dict(bits=0x40000))
 def test_wrong_prefix_domain_rejected(self):
  s=self.prefix_space();s.result('unowned',dict(bits=0x40000))
  with self.assertRaises(ValueError):e.NextDialogueProjection(types.SimpleNamespace(space=s))
 def test_namespace_capacity_stays_below_existing_GDI(self):
  self.assertEqual(e.PREFIX_NEXT_MAX+3*7*e.PROJECTION_STRIDE,e.NEXT_DIALOGUE_NEXT_MAX)
  self.assertEqual(e.NEXT_DIALOGUE_NEXT_MAX,0x67B01000);self.assertLess(e.NEXT_DIALOGUE_NEXT_MAX,e.GDI_GUEST_START)
  s=self.prefix_space();s.next=e.PREFIX_NEXT_MAX+e.PROJECTION_STRIDE
  with self.assertRaises(ValueError):e.NextDialogueProjection(types.SimpleNamespace(space=s))
 def test_CLI_gzip_changes_only_compression_not_JSON_bytes(self):
  data=dict(text='原始資料',raw='a500ff80',values=[1,2])
  with tempfile.TemporaryDirectory() as directory:
   p=Path(directory)/'source.json.gz'
   with patch.object(e.json,'dumps',side_effect=AssertionError('whole JSON buffering forbidden')):e.save_source(p,data)
   raw=p.read_bytes();self.assertEqual(raw[3],0)
   self.assertEqual(gzip.decompress(raw),(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n').encode());self.assertEqual(raw[4:8],bytes(4))
   with self.assertRaises(ValueError):e.save_source(p,dict(changed=True))
   self.assertEqual(p.read_bytes(),raw)
 def test_streaming_plain_JSON_has_identical_UTF8_bytes(self):
  data=dict(text='原始資料😀',values=list(range(100)))
  with tempfile.TemporaryDirectory() as directory:
   p=Path(directory)/'source.json'
   with patch.object(e.json,'dumps',side_effect=AssertionError('whole JSON buffering forbidden')):e.save_source(p,data)
   self.assertEqual(p.read_bytes(),(json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n').encode('utf8'))
   with self.assertRaises(ValueError):e.save_source(p,{})
 def test_streaming_open_refuses_racing_existing_output(self):
  with tempfile.TemporaryDirectory() as directory:
   p=Path(directory)/'source.json.gz';p.write_bytes(b'immutable')
   with patch.object(Path,'exists',return_value=False),self.assertRaises(FileExistsError):e.save_source(p,{})
   self.assertEqual(p.read_bytes(),b'immutable')
 @staticmethod
 def pointer_fixture(native_pointer=0x10000):
  s=e.overlay.AddressSpace();s.next=0x64001000
  old=dict(pointer=0x10000,vtable=0x20000,methods={'8':0x20100,'56':0x20200,'64':0x20300,'68':0x20400})
  s.result('overlay',dict(texture=old));s.result('overlay',dict(bits=0x30000))
  current=dict(kind='text',label='followup_text',record=e.parent.parent.OLD_TEXT_RECORD,alive=True,size=[128,32],native_pointer=native_pointer,create_wire_index=1)
  old_resource=dict(kind='text',label='text5',record=current['record'],alive=False,size=[128,32],native_pointer=0x10000,release_wire_index=0,generation=1,lock=dict(bits=s.guest('overlay',0x30000),pitch=256,hex='a5'*8192))
  gpu=types.SimpleNamespace(trace=[dict(request=dict(op='release',pointer=0x10000),reply=dict(result=dict(count=0))),dict(request=dict(op='create',width=128,height=32),reply=dict(result=dict(texture=dict(pointer=native_pointer))))])
  m=types.SimpleNamespace(space=s,fu_current=current,fu_resources=[old_resource,current],gpu=gpu,followup_active=True,live_input=dict(name='timeout_before_combat'),replacement_ready=False,next_dialogue_ready=False)
  bridge=e.FollowupPointerProjection(m);s.result=bridge.result
  native=dict(hr=0,texture=dict(old,pointer=native_pointer));lock=dict(hr=0,pitch=256,bits=0x30000,locked_hex=struct.pack('<II',256,0x30000).hex(),hex='5a'*8192)
  return m,bridge,native,lock
 def test_pointer_bridge_reused_and_fresh_native_addresses_give_same_guest(self):
  outputs=[]
  for pointer in (0x10000,0x11000):
   m,bridge,native,lock=self.pointer_fixture(pointer);original=copy.deepcopy((native,lock));before=m.space.next
   outputs.append((m.space.result('overlay',native),m.space.result('overlay',lock)))
   self.assertEqual(outputs[-1][0]['texture']['pointer'],before);self.assertEqual(m.space.next,before+0x100000)
   self.assertEqual([r for r in m.space.ledger() if r['domain']==e.FOLLOWUP_POINTER_DOMAIN],[dict(domain=e.FOLLOWUP_POINTER_DOMAIN,native=pointer,guest=before)])
   self.assertEqual((native,lock),original)
  self.assertEqual(outputs[0],outputs[1])
 def test_pointer_bridge_keeps_original_shared_interfaces_and_surface_domain(self):
  m,bridge,native,lock=self.pointer_fixture();prefix=copy.deepcopy(m.space.ledger());texture=m.space.result('overlay',native)['texture'];projected=m.space.result('overlay',lock)
  expected=dict(pointer=0x64001000,vtable=0x64101000,methods={'8':0x64201000,'56':0x64301000,'64':0x64401000,'68':0x64501000})
  self.assertEqual({k:v for k,v in texture.items() if k!='pointer'},{k:v for k,v in expected.items() if k!='pointer'})
  self.assertEqual(projected['bits'],0x64601000);self.assertEqual(projected['hex'],lock['hex']);self.assertEqual(m.space.ledger()[:len(prefix)],prefix)
  self.assertEqual(len([r for r in m.space.ledger() if r['domain']==e.FOLLOWUP_POINTER_DOMAIN]),1)
 def test_pointer_bridge_is_limited_to_timeout_FU_text_creation(self):
  for scope in ('victory','inactive','portrait','replacement_domain'):
   m,bridge,native,lock=self.pointer_fixture();before=m.space.next;domain='overlay';value=native
   if scope=='victory':m.live_input['name']='neutral_running'
   if scope=='inactive':m.followup_active=False
   if scope=='portrait':m.fu_current['kind']='portrait'
   if scope=='replacement_domain':domain=e.parent.PROJECTION_DOMAINS[0]
   m.space.result(domain,value)
   self.assertIsNone(bridge.bound);self.assertFalse(any(r['domain']==e.FOLLOWUP_POINTER_DOMAIN for r in m.space.ledger()))
 def test_pointer_bridge_rejects_wrong_text_record_label_and_late_phase(self):
  for mutation in ('record','label','texture','replacement_ready','next_dialogue_ready'):
   m,bridge,native,lock=self.pointer_fixture()
   if mutation=='record':m.fu_current['record']=e.TEXTURE
   elif mutation=='label':m.fu_current['label']='forged'
   elif mutation=='texture':m.fu_current['texture']={"pointer":1}
   else:setattr(m,mutation,True)
   with self.subTest(mutation=mutation),self.assertRaises(ValueError):m.space.result('overlay',native)
   self.assertIsNone(bridge.bound)
 def test_pointer_bridge_rejects_second_creation_and_wrong_interface_shape(self):
  m,bridge,native,lock=self.pointer_fixture();m.space.result('overlay',native)
  with self.assertRaises(ValueError):m.space.result('overlay',native)
  m,bridge,native,lock=self.pointer_fixture();native['texture']['extra']=1
  with self.assertRaises(ValueError):m.space.result('overlay',native)
 def test_compatible_prefix_accepts_only_actual_timeout_pointer_creation(self):
  m,bridge,native,lock=self.pointer_fixture();texture=m.space.result('overlay',native)['texture'];projected=m.space.result('overlay',lock)
  m.fu_current.update(texture=texture,lock=projected,GPU_APIs=[dict(op='lock',native_result=lock)])
  prefix=e.ReplacementProjection(m);self.assertEqual(prefix.prefix,m.space.ledger())
  self.assertEqual(e.NextDialogueProjection(m).prefix,prefix.prefix)
  m.fu_current['native_pointer']+=4
  with self.assertRaises(ValueError):e.ReplacementProjection(m)
 def test_bridge_prefix_rejects_missing_duplicate_or_victory_domain(self):
  m,bridge,native,lock=self.pointer_fixture();m.fu_resources=[]
  with self.assertRaises(ValueError):e.ReplacementProjection(m)
  m.space.result('overlay',native);m.fu_resources=[dict(label='followup_text',native_pointer=native['texture']['pointer'],texture=dict(pointer=bridge.bound['guest']))]
  m.live_input['name']='neutral_running'
  with self.assertRaises(ValueError):e.ReplacementProjection(m)
  m.live_input['name']='timeout_before_combat';m.space.guest(e.FOLLOWUP_POINTER_DOMAIN,0x12000)
  with self.assertRaises(ValueError):e.ReplacementProjection(m)
 def test_bits_reused_or_new_native_address_uses_same_retired_guest_without_allocation(self):
  outputs=[]
  for native_bits in (0x30000,0x39000):
   m,bridge,native,lock=self.pointer_fixture();m.space.result('overlay',native);lock['bits']=native_bits;lock['locked_hex']=struct.pack('<II',lock['pitch'],native_bits).hex();original=copy.deepcopy(lock);before=m.space.next
   outputs.append(m.space.result('overlay',lock));guest=m.fu_resources[0]['lock']['bits']
   self.assertEqual(outputs[-1]['bits'],guest);self.assertEqual(m.space.next,before);self.assertEqual(lock,original)
   self.assertEqual(m.space.native_to_guest[(e.FOLLOWUP_BITS_DOMAIN,native_bits)],guest);self.assertEqual(m.space.guest_to_native[guest],(e.FOLLOWUP_BITS_DOMAIN,native_bits))
   self.assertEqual(bridge.bits_bound['retired_surface_identity'],dict(native=0x30000))
  self.assertEqual(outputs[0],outputs[1])
 def test_bits_alias_preserves_all_raw_current_surface_bytes(self):
  m,bridge,native,lock=self.pointer_fixture();m.space.result('overlay',native);lock['hex']=(bytes(range(256))*32).hex();original=copy.deepcopy(lock)
  projected=m.space.result('overlay',lock);self.assertEqual(projected['hex'],original['hex']);self.assertEqual(projected['pitch'],original['pitch']);self.assertEqual(lock,original)
  self.assertEqual(struct.unpack('<II',bytes.fromhex(projected['locked_hex'])),(256,projected['bits']))
 def test_bits_alias_rejects_live_old_resource_or_unreleased_native_creation(self):
  for mutation in ('old_alive','release_order','release_pointer','release_count','release_opcode'):
   m,bridge,native,lock=self.pointer_fixture();m.space.result('overlay',native);old=m.fu_resources[0]
   if mutation=='old_alive':old['alive']=True
   if mutation=='release_order':old['release_wire_index']=1
   if mutation=='release_pointer':m.gpu.trace[0]['request']['pointer']=0x99000
   if mutation=='release_count':m.gpu.trace[0]['reply']['result']['count']=1
   if mutation=='release_opcode':m.gpu.trace[0]['request']['op']='describe'
   with self.subTest(mutation=mutation),self.assertRaises(ValueError):m.space.result('overlay',lock)
   self.assertIsNone(bridge.bits_bound)
 def test_bits_alias_rejects_wrong_record_kind_label_or_late_phase(self):
  for mutation in ('old_record','old_kind','current_record','current_label','replacement_ready','next_dialogue_ready','existing_lock','not_alive'):
   m,bridge,native,lock=self.pointer_fixture();m.space.result('overlay',native)
   if mutation=='old_record':m.fu_resources[0]['record']=e.NAME_RECORD
   elif mutation=='old_kind':m.fu_resources[0]['kind']='portrait'
   elif mutation=='current_record':m.fu_current['record']=e.TEXTURE
   elif mutation=='current_label':m.fu_current['label']='forged'
   elif mutation=='existing_lock':m.fu_current['lock']=dict(bits=123)
   elif mutation=='not_alive':m.fu_current['alive']=False
   else:setattr(m,mutation,True)
   with self.subTest(mutation=mutation),self.assertRaises(ValueError):m.space.result('overlay',lock)
   self.assertIsNone(bridge.bits_bound)
 def test_bits_alias_rejects_different_size_pitch_or_span(self):
  for mutation in ('old_size','current_size','native_size','old_pitch','new_pitch','old_bytes','new_bytes'):
   m,bridge,native,lock=self.pointer_fixture();m.space.result('overlay',native)
   if mutation=='old_size':m.fu_resources[0]['size']=[64,32]
   if mutation=='current_size':m.fu_current['size']=[64,32]
   if mutation=='native_size':m.gpu.trace[1]['request']['width']=64
   if mutation=='old_pitch':m.fu_resources[0]['lock']['pitch']=128
   if mutation=='new_pitch':lock['pitch']=128
   if mutation=='old_bytes':m.fu_resources[0]['lock']['hex']='00'
   if mutation=='new_bytes':lock['hex']='00'
   with self.subTest(mutation=mutation),self.assertRaises(ValueError):m.space.result('overlay',lock)
   self.assertIsNone(bridge.bits_bound)
 def test_bits_alias_rejects_any_other_alive_overlapping_guest_span(self):
  for delta in (-4,0,8191):
   m,bridge,native,lock=self.pointer_fixture();m.space.result('overlay',native);guest=m.fu_resources[0]['lock']['bits'];m.fu_resources.append(dict(label='declared_overlap',alive=True,lock=dict(bits=guest+delta,hex='ff'*8)))
   with self.subTest(delta=delta),self.assertRaises(ValueError):m.space.result('overlay',lock)
   self.assertIsNone(bridge.bits_bound)
 def test_bits_alias_rejects_second_lock_or_unbound_bits_scalar(self):
  m,bridge,native,lock=self.pointer_fixture();m.space.result('overlay',native);m.space.result('overlay',lock)
  with self.assertRaises(ValueError):m.space.result('overlay',lock)
  m,bridge,native,lock=self.pointer_fixture()
  with self.assertRaises(ValueError):m.space.result('overlay',lock['bits'],'bits')
 def test_bits_alias_is_limited_to_actual_timeout_FU_lock(self):
  for scope in ('victory','inactive','portrait','replacement_domain'):
   m,bridge,native,lock=self.pointer_fixture();m.space.result('overlay',native);domain='overlay'
   if scope=='victory':m.live_input['name']='neutral_running'
   if scope=='inactive':m.followup_active=False
   if scope=='portrait':m.fu_current['kind']='portrait'
   if scope=='replacement_domain':domain=e.parent.PROJECTION_DOMAINS[0]
   m.space.result(domain,lock);self.assertIsNone(bridge.bits_bound)
   self.assertFalse(any(r['domain']==e.FOLLOWUP_BITS_DOMAIN for r in m.space.ledger()))
 def test_alias_prefix_rejects_an_unrelated_duplicate_guest_identity(self):
  m,bridge,native,lock=self.pointer_fixture();texture=m.space.result('overlay',native)['texture'];projected=m.space.result('overlay',lock)
  m.fu_current.update(texture=texture,lock=projected,GPU_APIs=[dict(op='lock',native_result=lock)])
  m.space.native_to_guest[('overlay',0x99000)]=texture['pointer']
  with self.assertRaises(ValueError):e.NextDialogueProjection(m)
 def test_actual_fixed_proof_has_two_pinned_parent_summaries(self):
  summaries=e.fixed_parent_forward_summaries();self.assertEqual(set(summaries),{'neutral_running','timeout_before_combat'})
  for summary in summaries.values():self.assertEqual(set(summary),{'instructions','writes','code_sha256','write_sha256'})
 def test_prefix_preflight_compares_all_four_fields_and_logs_success(self):
  expected=dict(instructions=1,writes=2,code_sha256='abc',write_sha256='def');m=types.SimpleNamespace(live_input=dict(name='declared'),mark=lambda:dict(expected))
  with patch.object(e,'fixed_parent_forward_summaries',return_value=dict(declared=expected)),patch('builtins.print') as log:
   result=e.validate_parent_prefix(m);self.assertEqual(result['expected'],result['actual']);log.assert_called_once()
   for key in expected:
    actual=dict(expected);actual[key]='changed';m.mark=lambda:actual
    with self.subTest(key=key),self.assertRaisesRegex(ValueError,'declared expected=.*actual='):e.validate_parent_prefix(m)
 def test_prefix_preflight_rejects_changed_small_proof_before_decode(self):
  e.fixed_parent_forward_summaries.cache_clear()
  try:
   with patch.object(Path,'read_bytes',return_value=b'changed proof'),self.assertRaisesRegex(ValueError,'fixed replacement proof'):e.fixed_parent_forward_summaries()
  finally:e.fixed_parent_forward_summaries.cache_clear()
 def test_new_cycle_is_explicitly_labelled(self):
  m=types.SimpleNamespace(_nd_captured=lambda value:dict(capture=value));result=e.NextDialogueMachine.nd_captured(m,dict(label='idle'))
  self.assertEqual(result['cycle'],'next_dialogue_confirmation')

if __name__=='__main__':unittest.main()
