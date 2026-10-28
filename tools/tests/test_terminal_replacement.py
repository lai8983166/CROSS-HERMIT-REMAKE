"""Original replacement bytes, independent replay and ownership tamper guards."""
import copy,gzip,hashlib,json,os,struct,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from tools import terminal_replacement_emulation as e
from tools import terminal_replacement_verification as v
from tools import terminal_replacement_preservation as preservation

REPORT=os.environ.get('TERMINAL_REPLACEMENT_REPORT','analysis/terminal-replacement-source-v2-20261028.json.gz')

class TerminalReplacementStaticTests(unittest.TestCase):
 @staticmethod
 def fixture(name):
  raw=(e.ROOT/e.terminal.SCRIPT_PATH).read_bytes();cfg=v.branch(name);s=next(s for s in v.previous.dialogue.script_commands(raw)['segments'] if s['index']==cfg['segment']);code=raw[s['code_start']:s['code_end']];base=0xE000000;vm=bytearray(0x9400);struct.pack_into('<I',vm,16,base);pc=cfg['first_PC'];commands=[]
  while pc<cfg['final_PC']:
   op,n=struct.unpack_from('<HH',code,pc);commands.append(dict(PC=pc,opcode=op,bytes=n,source_pointer=base+pc));pc+=n
  return dict(input=dict(name=name),terminal_replacement=dict(before=dict(memory=[dict(pointer=e.VM,bytes=len(vm),hex=vm.hex()),dict(pointer=base,bytes=len(code),hex=code.hex())]),commands=commands))
 def test_both_original_script_groups(self):
  for n,want,indices in [('neutral_running',230,[3,4]),('timeout_before_combat',226,[5,6])]:
   s=v.source(self.fixture(n));self.assertEqual(s['final_PC'],want);self.assertEqual([t['index'] for t in s['texts']],indices);self.assertEqual(s['configuration'][0],7)
 def test_short_dispatch_rejected(self):
  r=self.fixture('neutral_running');r['terminal_replacement']['commands'][2]['bytes']=4
  with self.assertRaises(ValueError):v.source(r)
 def test_next_dispatch_rejected(self):
  r=self.fixture('timeout_before_combat');r['terminal_replacement']['commands'].append(dict(PC=226,opcode=30,bytes=20,source_pointer=0))
  with self.assertRaises(ValueError):v.source(r)
 def test_unknown_branch_rejected(self):
  with self.assertRaises(ValueError):v.branch('neutral_running ')
 def test_no_guest_code_extension(self):
  self.assertIs(e.ALLOWED,e.parent.ALLOWED);self.assertIs(e.ReplacementMachine.source_code,e.parent.FollowupMachine.source_code)
 def test_independent_engine_changes_only_report_routing_constants(self):
  for name in ('__init__','execute'):
   before=getattr(v.previous_stage.Replay,name).__code__;after=getattr(v.Replay,name).__code__;self.assertEqual(before.co_code,after.co_code);self.assertEqual(before.co_names,after.co_names)
 def test_full_declared_memory_required(self):
  x=[dict(pointer=0,bytes=2,hex='00')]
  with self.assertRaises(ValueError):v.equal(x,x,'partial fixture')
 def test_capture_inventory_keeps_predecessor_clocks_outside_new_scope(self):
  old={k:{} for k in v.CAPTURE_KEYS};new={k:{} for k in v.CAPTURE_KEYS};old=dict(old,create_wire_index=2);new=dict(new,create_wire_index=10)
  d=dict(prefix=dict(GPU_wire=10),resources=[old,new],resources_before=[old],before={k:{} for k in v.CAPTURE_KEYS})
  self.assertEqual([p for p,c in v.capture_list(d)],['/resources/1','/before']);self.assertEqual(d['resources_before'],[old]);self.assertEqual(d['resources'][0],old)
 def test_native_address_reissue_has_distinct_projection_lifetimes(self):
  row=dict(typed_GPU_projection=[dict(domain='overlay',native=123,guest=0x64001000),dict(domain='overlay-replacement-0',native=123,guest=0x68001000),dict(domain='overlay-replacement-1',native=123,guest=0x69001000)])
  m=v.gpu_mappings(row);self.assertEqual([m[d][123] for d in ('overlay','overlay-replacement-0','overlay-replacement-1')],[0x64001000,0x68001000,0x69001000])
 def test_projection_guest_alias_across_lifetimes_rejected(self):
  row=dict(typed_GPU_projection=[dict(domain='overlay',native=123,guest=0x64001000),dict(domain='overlay-replacement-0',native=456,guest=0x64001000)])
  with self.assertRaises(ValueError):v.gpu_mappings(row)
 def test_projection_duplicate_native_within_lifetime_rejected(self):
  row=dict(typed_GPU_projection=[dict(domain='overlay',native=123,guest=0x64001000),dict(domain='overlay',native=123,guest=0x65001000)])
  with self.assertRaises(ValueError):v.gpu_mappings(row)
 def test_unknown_projection_lifetime_rejected(self):
  row=dict(typed_GPU_projection=[dict(domain='fake',native=123,guest=0x64001000)])
  with self.assertRaises(ValueError):v.gpu_mappings(row)
 def test_resource_lifetime_is_derived_from_record(self):
  row=dict(terminal_replacement=dict(prefix=dict(GPU_wire=100)));r=dict(create_wire_index=100,record_index=1,record=v.text_record(7,1),projection_domain='overlay-replacement-1');self.assertEqual(v.resource_domain(row,r),'overlay-replacement-1');r['projection_domain']='overlay-replacement-0'
  with self.assertRaises(ValueError):v.resource_domain(row,r)
 def test_zero_count_preserves_stale_records(self):
  b=bytearray([0xA5])*0xAB8;struct.pack_into('<H',b,22,0);self.assertEqual(v.text_update(bytes(b),[0,0],v.text_object(7))['after_hex'],b.hex())
 def check_local(self,edit=None):
  with tempfile.TemporaryDirectory() as tmp:
   base=Path(tmp);root=base/'project';root.mkdir();raw=b'local evidence original';(root/'raw.bin').write_bytes(raw);backup=base/'backup.bin';backup.write_bytes(raw);row=dict(path='raw.bin',bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),backup_path=str(backup));catalog=root/'catalog.json'
   if edit:edit(row,backup)
   catalog.write_text(json.dumps(dict(schema_version=1,files=[row])),encoding='utf8')
   with patch.object(preservation,'ROOT',root):return preservation.verify_local(catalog)
 def test_local_evidence_and_external_backup_verified(self):self.assertTrue(self.check_local()['local_and_external_backup_SHA256_match'])
 def test_local_evidence_wrong_hash_rejected(self):
  with self.assertRaises(ValueError):self.check_local(lambda r,b:r.update(sha256='0'*64))
 def test_external_backup_changed_byte_rejected(self):
  with self.assertRaises(ValueError):self.check_local(lambda r,b:b.write_bytes(b'altered'))
 def test_local_evidence_path_escape_rejected(self):
  with self.assertRaises(ValueError):self.check_local(lambda r,b:r.update(path='../backup.bin'))

class TerminalReplacementTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with gzip.open(e.ROOT/REPORT,'rt',encoding='utf8') as f:cls.data=json.load(f)
  cls.rows=cls.data['cases'];cls.refs={r['input']['name']:v.pixels(r)[1] for r in cls.rows}
 def reject(self,edit,check,index=0,fields=()):
  row=dict(self.rows[index]);row['terminal_replacement']=copy.deepcopy(row['terminal_replacement'])
  for key in fields:row[key]=copy.deepcopy(row[key])
  edit(row)
  with self.assertRaises((ValueError,KeyError,IndexError,StopIteration,AssertionError)):check(row)
 def test_complete_independent_original_branches(self):
  self.assertEqual(self.data['source_contract'],e.source_contract())
  for row,pc in zip(self.rows,[230,226]):
   with self.subTest(name=row['input']['name']):self.assertEqual(v.verify_case(row)['timing']['VM_PC'],pc)
 def test_next_opcode_not_dispatched(self):self.reject(lambda r:r['terminal_replacement']['commands'].append(dict(PC=230,opcode=43,bytes=8,source_pointer=0)),v.source)
 def test_configuration_index_cannot_be_layer(self):self.reject(lambda r:r['terminal_replacement']['branch'].update(layer=4),v.protocol)
 def test_reused_keyboard_cycle_rejected(self):self.reject(lambda r:r['terminal_replacement']['bindings'][0].update(cycle='followup_confirmation'),v.protocol)
 def test_raw_keyboard_truncation_rejected(self):self.reject(lambda r:r['terminal_replacement']['bindings'][0]['capture'].update(raw_device_hex='00'),v.protocol)
 def test_keyboard_derived_byte_rejected(self):self.reject(lambda r:r['terminal_replacement']['bindings'][0].update(after_hex='00'),v.protocol)
 def test_keyboard_bridge_owner_byte_rejected(self):
  def edit(r):
   b=r['terminal_replacement']['bindings'][0]['after']['state'];raw=bytearray.fromhex(b['owner']);raw[-1]^=1;b['owner']=raw.hex()
  self.reject(edit,v.protocol)
 def test_frame_after_metadata_rejected(self):self.reject(lambda r:r['terminal_replacement']['frames'][0]['after'].update(remaining=-1),v.protocol)
 def test_frame_queue_after_metadata_rejected(self):self.reject(lambda r:r['terminal_replacement']['frames'][0]['queue_after'].update(invented=1),v.protocol)
 def test_clear_cannot_release_textures(self):self.reject(lambda r:r['terminal_replacement']['clear'].update(GPU_wire_after=-1),v.protocol)
 def test_missing_old_replacement_rejected(self):self.reject(lambda r:r['terminal_replacement']['replacements'].clear(),v.protocol,index=1)
 def test_wrong_old_creation_rejected(self):self.reject(lambda r:r['terminal_replacement']['replacements'][0].update(generation=0),v.protocol)
 def test_replacement_caller_rejected(self):self.reject(lambda r:r['terminal_replacement']['replacements'][0].update(caller=0),v.protocol)
 def test_retained_third_texture_cannot_disappear(self):
  def edit(r):
   next(x for x in r['terminal_replacement']['resources'] if x['record']==v.text_record(7,2))['alive']=False
  self.reject(edit,v.protocol,index=1)
 def test_text_index_and_record_binding_rejected(self):self.reject(lambda r:v.new_resources(r)[0].update(text_index=99),v.pixels)
 def test_swapped_text_records_rejected(self):self.reject(lambda r:v.new_resources(r)[1].update(record=v.text_record(7)),v.pixels)
 def test_font_abi_rejected(self):self.reject(lambda r:v.new_resources(r)[0]['pending_font']['args'].__setitem__(0,99),v.pixels)
 def test_raster_stage_rejected(self):self.reject(lambda r:v.new_resources(r)[0]['raster']['stages'][1].update(hex='00'),v.pixels)
 def test_conversion_band_rejected(self):self.reject(lambda r:v.new_resources(r)[0]['conversions'][0].update(point=[99,99]),v.pixels)
 def test_upload_texel_rejected(self):self.reject(lambda r:v.new_resources(r)[0].update(upload_hex='00'),v.pixels)
 def test_native_generation_count_rejected(self):self.reject(lambda r:r['replacement_resources_after_cleanup'].pop(),v.native,fields=('replacement_resources_after_cleanup',))
 def test_native_prefix_dead_generation_cannot_revive(self):self.reject(lambda r:r['terminal_replacement']['resources_before'][3].update(alive=True),v.native,index=1)
 def test_missing_native_observer_rejected(self):self.reject(lambda r:r['terminal_replacement']['readback_observers'].pop(),v.native)
 def test_native_resource_cannot_claim_other_projection_domain(self):self.reject(lambda r:v.new_resources(r)[0].update(projection_domain='overlay-replacement-1'),v.native)
 def test_native_prefix_projection_next_rejected(self):self.reject(lambda r:r['terminal_replacement']['GPU_projection_before'].update(next=0),v.native)
 def test_native_new_projection_metadata_rejected(self):self.reject(lambda r:r['terminal_replacement']['GPU_projection'][0].update(guest=0),v.native)
 def test_native_release_cannot_claim_other_creation(self):self.reject(lambda r:r['terminal_replacement']['GPU_APIs'][-1].update(generation=0),v.native)
 def test_native_receipt_tamper_rejected(self):
  def edit(r):
   i=v.new_resources(r)[0]['create_wire_index'];r['GPU_trace'][i]['request']['format']=0
  self.reject(edit,v.native,fields=('GPU_trace',))
 def test_replay_all57_cpu_metadata_rejected(self):
  self.reject(lambda r:r['terminal_replacement']['segments'][0]['CPU'].__setitem__('EAX',0xDEADBEEF),lambda r:v.Replay(r,self.refs[r['input']['name']]).execute())
 def test_replay_trace_metadata_rejected(self):
  self.reject(lambda r:r['terminal_replacement']['segments'][0]['local_after'].__setitem__('code_sha256','0'*64),lambda r:v.Replay(r,self.refs[r['input']['name']]).execute())
 def test_replay_frame_full_region_hash_rejected(self):
  self.reject(lambda r:r['terminal_replacement']['frames'][0]['capture']['memory'][0].update(sha256='0'*64),lambda r:v.Replay(r,self.refs[r['input']['name']]).execute())
 def test_parent_entire_boundary_rejected(self):
  self.reject(lambda r:r['terminal_replacement']['before']['CPU'].__setitem__('EAX',0xDEADBEEF),lambda r:v.prefix(r,replay=False))

if __name__=='__main__':unittest.main()
