"""Original next dialogue, actual lifetime ownership and independent replay guards."""
import copy,gzip,hashlib,json,os,struct,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from tools import terminal_next_dialogue_emulation as e
from tools import terminal_next_dialogue_verification as v
from tools import terminal_next_dialogue_preservation as preservation

REPORT=os.environ.get('TERMINAL_NEXT_DIALOGUE_REPORT','analysis/terminal-next-dialogue-source-v3-20261028.json.gz')

class TerminalNextDialogueStaticTests(unittest.TestCase):
 @staticmethod
 def fixture(name):
  raw=(e.ROOT/e.terminal.SCRIPT_PATH).read_bytes();cfg=v.branch(name);s=next(s for s in v.previous.dialogue.script_commands(raw)['segments'] if s['index']==cfg['segment']);code=raw[s['code_start']:s['code_end']];base=0xE000000;vm=bytearray(0x9400);struct.pack_into('<I',vm,16,base);pc=cfg['first_PC'];commands=[]
  while pc<cfg['final_PC']:
   op,n=struct.unpack_from('<HH',code,pc);commands.append(dict(PC=pc,opcode=op,bytes=n,source_pointer=base+pc));pc+=n
  return dict(input=dict(name=name),terminal_next_dialogue=dict(before=dict(memory=[dict(pointer=e.VM,bytes=len(vm),hex=vm.hex()),dict(pointer=base,bytes=len(code),hex=code.hex())]),commands=commands))
 def test_both_original_next_groups(self):
  for n,pc,i in [('neutral_running',256,5),('timeout_before_combat',268,7)]:
   s=v.source(self.fixture(n));self.assertEqual((s['final_PC'],s['text']['index'],s['configuration'][0]),(pc,i,4))
 def test_complete_role_command_required(self):
  r=self.fixture('timeout_before_combat');r['terminal_next_dialogue']['commands'][0]['bytes']=12
  with self.assertRaises(ValueError):v.source(r)
 def test_successor_dispatch_rejected(self):
  r=self.fixture('neutral_running');r['terminal_next_dialogue']['commands'].append(dict(PC=256,opcode=43,bytes=8,source_pointer=0))
  with self.assertRaises(ValueError):v.source(r)
 def test_unknown_branch_rejected(self):
  with self.assertRaises(ValueError):v.branch('neutral_running ')
 def test_no_new_guest_code(self):self.assertIs(e.ALLOWED,e.parent.ALLOWED);self.assertIs(e.NextDialogueMachine.source_code,e.parent.ReplacementMachine.source_code)
 def test_independent_engine_retains_instruction_algorithm(self):
  for name in ('__init__','execute'):
   before=getattr(v.previous_stage.previous_stage.Replay,name).__code__;after=getattr(v.Replay,'_initialize' if name=='__init__' else name).__code__;self.assertEqual(before.co_code,after.co_code)
   self.assertEqual(tuple('SC002_SHA' if name=='__init__' and n=='SC001_SHA' else n for n in before.co_names),after.co_names)
 def test_capture_inventory_excludes_old_local_clocks(self):
  old=dict(create_wire_index=2,**{k:{} for k in v.CAPTURE_KEYS});new=dict(create_wire_index=10,**{k:{} for k in v.CAPTURE_KEYS});d=dict(prefix=dict(GPU_wire=10),resources=[old,new],resources_before=[old],before={k:{} for k in v.CAPTURE_KEYS})
  self.assertEqual([p for p,c in v.capture_list(d)],['/resources/1','/before']);self.assertEqual(d['resources_before'],[old])
 def test_native_reissue_in_distinct_domains_allowed(self):
  r=dict(typed_GPU_projection=[dict(domain='overlay',native=1,guest=100),dict(domain='overlay-next-dialogue-text',native=1,guest=200)]);self.assertEqual(v.gpu_mappings(r)['overlay-next-dialogue-text'][1],200)
 def test_guest_alias_rejected(self):
  r=dict(typed_GPU_projection=[dict(domain='overlay',native=1,guest=100),dict(domain='overlay-next-dialogue-text',native=2,guest=100)])
  with self.assertRaises(ValueError):v.gpu_mappings(r)
 def test_unknown_domain_rejected(self):
  with self.assertRaises(ValueError):v.gpu_mappings(dict(typed_GPU_projection=[dict(domain='guessed',native=1,guest=100)]))
 def test_same_domain_duplicate_rejected(self):
  with self.assertRaises(ValueError):v.gpu_mappings(dict(typed_GPU_projection=[dict(domain='overlay',native=1,guest=100),dict(domain='overlay',native=1,guest=200)]))
 def bridge_fixture(self):
  return dict(input=dict(name='timeout_before_combat'),terminal_next_dialogue=dict(prefix=dict(GPU_wire=120)),terminal_replacement=dict(prefix=dict(GPU_wire=87))),dict(kind='text',record=v.text_record(5),label='followup_text',create_wire_index=66,native_pointer=123)
 def test_historical_pointer_bridge_preserves_shared_interface_context(self):
  row,r=self.bridge_fixture();c=v.resource_context(row,r,{'overlay':{123:100,456:200},v.FOLLOWUP_POINTER_DOMAIN:{123:300}});self.assertEqual(c,{123:300,456:200})
 def test_sealed_parent_context_without_new_stage(self):
  row,r=self.bridge_fixture();row.pop('terminal_next_dialogue');self.assertEqual(v.resource_context(row,r,{'overlay':{123:100}}),{123:100})
 def surface_fixture(self):
  raw='00'*8192;record=v.text_record(5)
  old=dict(label='text5',kind='text',generation=1,record=record,alive=False,create_wire_index=0,release_wire_index=2,native_pointer=101,size=[128,32],lock=dict(bits=1000,pitch=256,hex=raw))
  new=dict(label='followup_text',kind='text',generation=4,record=record,alive=True,create_wire_index=3,native_pointer=202,size=[128,32],lock=dict(bits=1000,pitch=256,hex=raw))
  trace=[dict(request=dict(op='create')),dict(request=dict(op='lock',pointer=101),reply=dict(result=dict(bits=111,pitch=256,hex=raw))),dict(request=dict(op='release',pointer=101),reply=dict(result=dict(count=0))),dict(request=dict(op='create',width=128,height=32),reply=dict(result=dict(texture=dict(pointer=202)))),dict(request=dict(op='lock',pointer=202),reply=dict(result=dict(bits=303,pitch=256,hex=raw)))]
  alias=dict(domain=v.FOLLOWUP_BITS_DOMAIN,native=303,guest=1000,retired_surface_identity=dict(native=111),retired_generation=1,record=record,pitch=256,bytes=8192,size=[128,32],retired_release_wire_index=2,current_create_wire_index=3)
  return dict(input=dict(name='timeout_before_combat'),terminal_followup=dict(resources=[old,new],forward_wire_end=5),terminal_next_dialogue=dict(historical_surface_alias=alias),GPU_trace=trace,typed_GPU_projection=[dict(domain='overlay',native=111,guest=1000),dict(domain=v.FOLLOWUP_BITS_DOMAIN,native=303,guest=1000)])
 def test_declared_surface_alias_matches_actual_retired_ownership(self):
  row=self.surface_fixture();self.assertEqual(v.legacy_surface_binding(row),row['terminal_next_dialogue']['historical_surface_alias']);self.assertEqual(v.gpu_mappings(row)[v.FOLLOWUP_BITS_DOMAIN],{303:1000})
 def test_reissued_and_new_native_bits_have_same_declared_guest(self):
  row=self.surface_fixture();row['GPU_trace'][4]['reply']['result']['bits']=111;row['terminal_next_dialogue']['historical_surface_alias']['native']=111;row['typed_GPU_projection'][1]['native']=111;self.assertEqual(v.legacy_surface_binding(row)['guest'],1000)
 def test_surface_alias_requires_original_release(self):
  row=self.surface_fixture();row['terminal_followup']['resources'][0]['alive']=True
  with self.assertRaises(ValueError):v.legacy_surface_binding(row)
 def test_surface_alias_requires_actual_zero_reference_release(self):
  row=self.surface_fixture();row['GPU_trace'][2]['reply']['result']['count']=1
  with self.assertRaises(ValueError):v.legacy_surface_binding(row)
 def test_surface_alias_requires_actual_same_extent_creation(self):
  row=self.surface_fixture();row['GPU_trace'][3]['request']['width']=256
  with self.assertRaises(ValueError):v.legacy_surface_binding(row)
 def test_surface_alias_refuses_overlap_with_other_live_resource(self):
  row=self.surface_fixture();row['terminal_followup']['resources'].append(dict(label='other',alive=True,lock=dict(bits=1001,hex='00'*8192)))
  with self.assertRaises(ValueError):v.legacy_surface_binding(row)
 def test_surface_alias_requires_same_full_extent(self):
  row=self.surface_fixture();row['terminal_followup']['resources'][1]['lock']['hex']='00'
  with self.assertRaises(ValueError):v.legacy_surface_binding(row)
 def test_surface_alias_cannot_claim_other_actual_native_buffer(self):
  row=self.surface_fixture();row['terminal_next_dialogue']['historical_surface_alias']['native']=999
  with self.assertRaises(ValueError):v.legacy_surface_binding(row)
 def test_surface_alias_cannot_allocate_new_guest_slot(self):
  row=self.surface_fixture();row['typed_GPU_projection'][1]['guest']=2000
  with self.assertRaises(ValueError):v.gpu_mappings(row)
 def test_only_one_declared_surface_alias_allowed(self):
  row=self.surface_fixture();row['typed_GPU_projection'].append(dict(domain=v.FOLLOWUP_BITS_DOMAIN,native=999,guest=1000))
  with self.assertRaises(ValueError):v.gpu_mappings(row)
 def test_alias_cannot_target_a_replacement_interface(self):
  row=self.surface_fixture();row['typed_GPU_projection'][0]['domain']='overlay-replacement-0'
  with self.assertRaises(ValueError):v.gpu_mappings(row)
 def test_historical_pointer_domain_has_one_actual_pointer(self):
  row,r=self.bridge_fixture()
  with self.assertRaises(ValueError):v.resource_context(row,r,{'overlay':{123:100},v.FOLLOWUP_POINTER_DOMAIN:{999:300}})
 def test_other_resource_does_not_use_bridge(self):
  row,r=self.bridge_fixture();r['label']='text5';self.assertEqual(v.resource_context(row,r,{'overlay':{123:100},v.FOLLOWUP_POINTER_DOMAIN:{123:300}}),{123:100})
 def test_projection_role_view_preserves_all_guest_entries(self):
  row=dict(terminal_replacement=dict(leaves=[],GPU_APIs=[],forward_wire_end=0,GPU_projection_before=dict(next=200,ledger=[dict(domain=v.FOLLOWUP_POINTER_DOMAIN,native=123,guest=100)])),replacement_cleanup=[dict(leaves=[0,0])]);before=copy.deepcopy(row)
  view=v.fixed_projection_role_view(row);self.assertEqual(view['GPU_projection_before']['ledger'],[dict(domain='overlay',native=123,guest=100)]);self.assertEqual(row,before)
 def test_partial_memory_rejected(self):
  with self.assertRaises(ValueError):v.equal([dict(pointer=0,bytes=2,hex='00')],[dict(pointer=0,bytes=2,hex='00')],'partial')
 def test_report_reader_preserves_long_hex_unicode_and_nested_values(self):
  value=dict(cases=[dict(owner='00'*9000,text='夏朧'*5000),dict(owner='00'*9000,text='夏朧'*5000)],flags=[True,None,17])
  with tempfile.TemporaryDirectory() as folder:
   p=Path(folder)/'report.json.gz'
   with gzip.open(p,'wt',encoding='utf8') as f:json.dump(value,f,ensure_ascii=False)
   self.assertEqual(v.load_report(p),value)
 def image_partitions(self):
  start=v.SOURCE_IMAGE_BASE;end=start+len(e.CODE);points={start,end}
  for p,n in v.SOURCE_IMAGE_WRITABLE:points.update((p,p+n))
  points=sorted(points);return [dict(pointer=a,bytes=b-a) for a,b in zip(points,points[1:])]
 def test_source_image_partition_values_and_permissions(self):
  parts=v.source_image_partitions(self.image_partitions());self.assertEqual(sum(n for p,n,flags in parts),len(e.CODE));self.assertTrue(all(flags in (3,5) for p,n,flags in parts))
 def test_source_image_gap_rejected(self):
  with self.assertRaises(ValueError):v.source_image_partitions(self.image_partitions()[1:])
 def test_source_image_permission_boundary_cannot_be_merged(self):
  with self.assertRaises(ValueError):v.source_image_partitions([dict(pointer=v.SOURCE_IMAGE_BASE,bytes=len(e.CODE))])
 def test_source_image_is_mapped_first_once(self):
  engine=v.source_image_uc(v.UC_ARCH_X86,v.UC_MODE_32);initial=list(engine.mem_regions());engine.mem_map(0x500000,4096);self.assertEqual(list(engine.mem_regions()),initial);self.assertEqual(initial,[(v.SOURCE_IMAGE_BASE,v.SOURCE_IMAGE_BASE+len(e.CODE)-1,7)])
 def test_parent_trace_checked_before_expensive_replay(self):
  r=dict(input=dict(name='timeout_before_combat'),terminal_next_dialogue=dict(before=dict(trace={})))
  with self.assertRaises(ValueError):v.prefix_trace(r)
 def local(self,edit=None):
  with tempfile.TemporaryDirectory() as t:
   root=Path(t)/'project';root.mkdir();p=root/'source';p.write_bytes(b'actual raw');backup=Path(t)/'backup';backup.write_bytes(p.read_bytes());r=dict(path='source',bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),backup_path=str(backup))
   if edit:edit(r,backup)
   catalog=root/'catalog.json';catalog.write_text(json.dumps(dict(schema_version=1,files=[r])),encoding='utf8')
   with patch.object(preservation,'ROOT',root):return preservation.verify_local(catalog)
 def test_local_and_external_evidence_verified(self):self.assertTrue(self.local()['local_and_external_backup_SHA256_match'])
 def test_local_hash_tamper_rejected(self):
  with self.assertRaises(ValueError):self.local(lambda r,b:r.update(sha256='0'*64))
 def test_backup_tamper_rejected(self):
  with self.assertRaises(ValueError):self.local(lambda r,b:b.write_bytes(b'changed'))
 def test_relative_path_escape_rejected(self):
  with self.assertRaises(ValueError):self.local(lambda r,b:r.update(path='../backup'))

class TerminalNextDialogueTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.data=v.load_report(e.ROOT/REPORT)
  cls.rows=cls.data['cases'];cls.refs={r['input']['name']:v.pixels(r)[1] for r in cls.rows}
 @staticmethod
 def changed(obj,path,value):
  if not path:return value
  out=copy.copy(obj);out[path[0]]=TerminalNextDialogueTests.changed(obj[path[0]],path[1:],value);return out
 def reject(self,path,value,check,index=0):
  row=self.changed(self.rows[index],path,value)
  with self.assertRaises((ValueError,KeyError,IndexError,StopIteration,AssertionError)):check(row)
 def stage(self,path,value,check,index=0):self.reject(('terminal_next_dialogue',)+tuple(path),value,check,index)
 def test_complete_original_branches(self):
  self.assertEqual(self.data['source_contract'],e.source_contract())
  for row in self.rows:v.prefix_trace(row)
  for row,pc in zip(self.rows,[256,268]):
   with self.subTest(case=row['input']['name']):self.assertEqual(v.verify_case(row)['timing']['VM_PC'],pc)
 def test_next_dispatch_rejected(self):self.stage(('commands',0,'PC'),256,v.source)
 def test_wrong_layer_rejected(self):self.stage(('branch','layer'),7,v.protocol)
 def test_old_keyboard_cycle_rejected(self):self.stage(('bindings',0,'cycle'),'replacement_confirmation',v.protocol)
 def test_truncated_keyboard_raw_rejected(self):self.stage(('bindings',0,'capture','raw_device_hex'),'00',v.protocol)
 def test_derived_keyboard_byte_rejected(self):self.stage(('bindings',0,'after_hex'),'00',v.protocol)
 def test_keyboard_bridge_owner_rejected(self):self.stage(('bindings',0,'after','state','owner'),'00',v.protocol)
 def test_frame_after_metadata_rejected(self):self.stage(('frames',0,'after','remaining'),-1,v.protocol)
 def test_frame_queue_metadata_rejected(self):self.stage(('frames',0,'queue_after'),{},v.protocol)
 def test_clear_cannot_release_texture(self):self.stage(('clear','GPU_wire_after'),-1,v.protocol)
 def test_original_replacement_required(self):self.stage(('replacements',),[],v.protocol)
 def test_old_generation_identity_rejected(self):self.stage(('replacements',0,'generation'),0,v.protocol)
 def test_replacement_caller_rejected(self):self.stage(('replacements',0,'caller'),0,v.protocol)
 def test_role2_identity_rejected(self):self.stage(('role','role'),1,v.protocol,1)
 def test_wrong_portrait_slot_rejected(self):self.stage(('role','pending_image','args',1),32,v.protocol,1)
 def test_wrong_portrait_side_rejected(self):self.stage(('role','pending_image','side_byte'),1,v.protocol,1)
 def test_wrong_role_file_rejected(self):self.stage(('role','pending_image','path'),'data/adv/bin/sc001.bin',v.protocol,1)
 def test_role_strict_readiness_rejected(self):self.stage(('role','ready','state','VM'),self.rows[1]['terminal_next_dialogue']['before']['state']['VM'],v.protocol,1)
 def test_text_index_rejected(self):self.stage(('resources',10,'text_index'),99,v.pixels)
 def test_font_abi_rejected(self):self.stage(('resources',10,'pending_font','args',0),99,v.pixels)
 def test_raster_stage_rejected(self):self.stage(('resources',10,'raster','stages',1,'hex'),'00',v.pixels)
 def test_conversion_geometry_rejected(self):self.stage(('resources',10,'conversions',0,'point'),[99,99],v.pixels)
 def test_upload_texel_rejected(self):self.stage(('resources',10,'upload_hex'),'00',v.pixels)
 def test_portrait_pixel_rejected(self):self.stage(('resources',11,'upload_hex'),'00',v.pixels,1)
 def test_portrait_copy_row_rejected(self):self.stage(('resources',11,'copy_rows',0,'args',2),511,v.pixels,1)
 def test_creation_count_rejected(self):self.reject(('next_dialogue_resources_after_cleanup',),[],v.native)
 def test_dead_prefix_generation_rejected(self):self.stage(('resources_before',3,'alive'),True,v.native,1)
 def test_native_observer_required(self):self.stage(('readback_observers',),[],v.native)
 def test_resource_domain_rejected(self):self.stage(('resources',10,'projection_domain'),'overlay',v.native)
 def test_prefix_projection_next_rejected(self):self.stage(('GPU_projection_before','next'),0,v.native)
 def test_legacy_pointer_cannot_claim_different_native(self):
  row=self.rows[1];index=next(i for i,r in enumerate(row['typed_GPU_projection']) if r['domain']==v.FOLLOWUP_POINTER_DOMAIN);self.reject(('typed_GPU_projection',index,'native'),123,v.native,1)
 def test_parent_projection_native_metadata_rejected(self):self.reject(('terminal_replacement','GPU_projection_before','ledger',0,'native'),123,v.native,1)
 def test_historical_surface_guest_metadata_rejected(self):self.stage(('historical_surface_alias','guest'),0,v.native,1)
 def test_historical_surface_native_metadata_rejected(self):self.stage(('historical_surface_alias','native'),123,v.native,1)
 def test_source_preflight_metadata_rejected(self):self.stage(('prefix_preflight','actual'),{},v.prefix_trace,1)
 def test_new_projection_identity_rejected(self):self.stage(('GPU_projection',0,'guest'),0,v.native)
 def test_release_generation_rejected(self):self.stage(('GPU_APIs',-1,'generation'),0,v.native)
 def test_native_wire_format_rejected(self):
  i=v.new_resources(self.rows[0])[0]['create_wire_index'];self.reject(('GPU_trace',i,'request','format'),0,v.native)
 def replay(self,row):return v.Replay(row,self.refs[row['input']['name']]).execute()
 def test_replay_cpu_rejected(self):self.stage(('segments',0,'CPU','EAX'),0xDEADBEEF,self.replay)
 def test_replay_digest_rejected(self):self.stage(('segments',0,'local_after','code_sha256'),'0'*64,self.replay)
 def test_replay_region_hash_rejected(self):self.stage(('frames',0,'capture','memory',0,'sha256'),'0'*64,self.replay)
 def test_parent_entire_cpu_rejected(self):self.stage(('before','CPU','EAX'),0xDEADBEEF,lambda r:v.prefix(r,replay=False))

if __name__=='__main__':unittest.main()
