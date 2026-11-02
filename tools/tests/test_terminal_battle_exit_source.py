"""Static source/ABI guards for the original exit-prefix dependency contract."""
import ast,inspect,struct,textwrap,unittest
from types import SimpleNamespace
from unittest.mock import patch
from tools import terminal_battle_exit_emulation as e

class TerminalBattleExitSourceTests(unittest.TestCase):
 def test_original_guard_algorithm_inherited(self):
  self.assertIs(e.BattleExitMachine.source_code.__code__,e.parent.BattleStageMachine.source_code.__code__)
  self.assertIs(e.BattleExitMachine.source_code.__globals__['ALLOWED'],e.ALLOWED)
  self.assertEqual(e.REFERENCE.__code__,e.parent.REFERENCE.__code__)
  self.assertEqual(e.RANGES,e.parent.RANGES+e.EXTRA_RANGES)
 def test_extra_extents_are_complete_original_functions(self):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  md=Cs(CS_ARCH_X86,CS_MODE_32)
  for a,b in e.EXTRA_RANGES:
   ins=list(md.disasm(e.CODE[a-0x400000:b-0x400000],a));self.assertEqual(ins[0].mnemonic,'push');self.assertEqual(ins[0].op_str,'ebp');self.assertEqual(ins[-1].mnemonic,'ret');self.assertEqual(ins[-1].address+ins[-1].size,b)
 def test_bmp8_stride_and_unwritten_padding_are_preserved(self):
  b=bytearray(54+1024+4);b[:2]=b'BM';struct.pack_into('<I',b,10,1078);struct.pack_into('<ii',b,18,3,1);b[54+4:54+8]=bytes((0,0,255,0));b[54+8:54+12]=bytes((0,255,0,0));b[1078:1082]=bytes((1,2,0,1));before=bytes((0xA5,))*32
  out=e.bmp8_upload(bytes(b),before,16,2,1);self.assertEqual(struct.unpack_from('<4H',out),(0xFC00,0x83E0,0,0xFC00));self.assertEqual(out[8:],before[8:])
 def test_bmp8_color_key_and_index0_remain_zero(self):
  b=bytearray(54+1024+4);struct.pack_into('<I',b,10,1078);struct.pack_into('<ii',b,18,1,1);b[54:58]=bytes((3,4,5,0));b[58:62]=b[54:58];b[1078]=1
  self.assertEqual(e.bmp8_upload(bytes(b),bytes((0x7F,))*8,4,2,1)[:2],bytes(2));b[1078]=0
  self.assertEqual(e.bmp8_upload(bytes(b),bytes((0x7F,))*8,4,2,0)[:2],bytes(2))
 def test_original_loader_black_palette_normalization_precedes_key(self):
  b=bytearray(54+1024+4);struct.pack_into('<I',b,10,1078);struct.pack_into('<ii',b,18,1,1);b[54:58]=bytes((0,0,255,0));b[1078]=1
  before=bytes((0xA5,))*8;self.assertEqual(e.bmp8_upload(bytes(b),before,4,2,1,1)[:2],bytes(2));self.assertEqual(struct.unpack_from('<H',e.bmp8_upload(bytes(b),before,4,2,0,1))[0],0xFC00);self.assertEqual(struct.unpack_from('<H',e.bmp8_upload(bytes(b),before,4,2,1,0))[0],0x8000)
 def test_loader_normalization_respects_effective_palette_count(self):
  b=bytearray(54+1024+4);struct.pack_into('<I',b,10,1078);struct.pack_into('<ii',b,18,1,1);struct.pack_into('<I',b,46,2);b[54:58]=bytes((0,0,255,0));b[1078]=3
  self.assertEqual(struct.unpack_from('<H',e.bmp8_upload(bytes(b),bytes(8),4,2,1,1))[0],0x8000)
  struct.pack_into('<I',b,46,0)
  self.assertEqual(struct.unpack_from('<H',e.bmp8_upload(bytes(b),bytes(8),4,2,1,1))[0],0)
 def test_common_path_is_original_static_bytes(self):
  self.assertEqual(e.COMMON_PATH_PTR,0x59A438);a=e.COMMON_PATH_PTR-0x400000;self.assertEqual(e.CODE[a:a+len(e.COMMON_NAME)+1],e.COMMON_NAME.encode()+bytes((0,)))
  self.assertNotIn('mem_write',inspect.getsource(e.CommonResourceMixin.initialize_common))
 def test_common_complete_original_identity_and_count(self):
  b,rows=e.common_resource();self.assertEqual((len(b),len(rows),sum(x['marker'] for x in rows)),(1793036,580,119));self.assertEqual(e.sha(b),e.COMMON_SHA)
  self.assertEqual([r['index'] for r in rows],list(range(580)))
  self.assertEqual(sum(r['texture_size'][0]*r['texture_size'][1]*2 for r in rows if not r['marker']),5634560)
 def test_helper_differences_are_exact_and_bounded(self):
  h=e.helper_contract();self.assertEqual((h['GPU']['max_textures'],h['GPU']['max_creates']),(500,512));self.assertEqual((h['GPU']['peak_required'],h['GPU']['total_creates_required']),(469,479));self.assertEqual(h['CRT']['additional_path'],e.COMMON_NAME)
  source=(e.ROOT/'tools/terminal_battle_exit_crt_platform.cs').read_text();self.assertIn('common.bin',source);self.assertIn('1793036u',source)
 def test_transport_only_bound_constants_differ(self):
  old=e.overlay.platform.crt.Live
  for name,limit in (('_read',16777216),('request',5000000)):
   fn=getattr(e.CommonCRTLive,name);original=getattr(old,name);self.assertEqual(fn.__code__.co_code,original.__code__.co_code);self.assertEqual(fn.__code__.co_consts,tuple(limit if v==3000000 else v for v in original.__code__.co_consts))
 def test_exact_original_call_order(self):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  md=Cs(CS_ARCH_X86,CS_MODE_32);s=list(md.disasm(e.CODE[0x4539e9-0x400000:0x453a27-0x400000],0x4539e9));self.assertEqual([int(x.op_str,16) for x in s if x.mnemonic=='call'],[0x454CF0,0x453F10,0x46B470,0x432100,0x457AA0])
  self.assertEqual(e.CODE[0x453cb0-0x400000:0x453cb5-0x400000],bytes((0xe8,))+struct.pack('<i',0x422360-0x453cb5))
 def test_actual_stage_result_saved_then_consumed_after_wait(self):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  md=Cs(CS_ARCH_X86,CS_MODE_32)
  want={0x453A00:('mov','dword ptr [ebp - 8], eax'),0x453CB5:('cmp','dword ptr [ebp - 8], 0'),0x453CB9:('je','0x453ce4'),0x451AB7:('call','0x4539b0'),0x451ABC:('mov','dword ptr [ebp - 8], eax')}
  for at,expected in want.items():i=next(md.disasm(e.CODE[at-0x400000:at-0x400000+12],at));self.assertEqual((i.mnemonic,i.op_str),expected)
 def strict_machine(self,caller=0x425A7E,arg=None,data=bytes((0,))):
  arg=e.INPUT+0x528 if arg is None else arg;values={0x5922C4:0x770206E0,100:caller,104:arg};return SimpleNamespace(getreg=lambda n:100,get=lambda p,*a:values[p],read=lambda p,n:data)
 def test_strict_original_task_text(self):
  d=e.BattleExitMachine.strict_text(self.strict_machine(),0x770206E0);self.assertEqual(d['caller'],0x425A7E);self.assertEqual(d['args'],[e.INPUT+0x528]);self.assertEqual(d['string_hex'],'')
 def test_unrelated_text_caller_refused(self):
  with self.assertRaises(ValueError):e.BattleExitMachine.strict_text(self.strict_machine(caller=0x41F416),0x770206E0)
 def test_different_input_buffer_refused(self):
  with self.assertRaises(ValueError):e.BattleExitMachine.strict_text(self.strict_machine(arg=e.INPUT+0x529),0x770206E0)
 def test_nonempty_input_buffer_refused(self):
  with self.assertRaises(ValueError):e.BattleExitMachine.strict_text(self.strict_machine(data=b'x'),0x770206E0)
 def test_marker_is_separate_real_leaf(self):
  receipts=[];returns=[];values={100:0x41F416,104:0x594734,0x5922C4:0x770206E0}
  m=SimpleNamespace(common_active=True,getreg=lambda n:100,get=lambda p:values[p],read=lambda p,n:b'Dm-No-MakeTex'+bytes((0,)),kernel=SimpleNamespace(lstrlenA=lambda s:len(s)),common_leaves=receipts,return_api=lambda *a:returns.append(a))
  self.assertTrue(e.CommonResourceMixin.common_text(m,0x770206E0));self.assertEqual(receipts[0]['kind'],'COMMON_STRING');self.assertEqual(receipts[0]['call']['value'],13);self.assertEqual(returns,[(100,13,4)])
 def test_prefix_dispatcher_handles_common_before_task_text(self):
  s=inspect.getsource(e.BattleExitMachine.code);self.assertLess(s.index('self.common_text(at)'),s.index('row=self.strict_text(at)'))
 def test_common_new_domains_do_not_alias_retired_parent(self):
  s=inspect.getsource(e.CommonResourceMixin.gpu_api);self.assertIn("domain='overlay-battle-exit-common-'",s);self.assertIn("self.space.result(r['projection_domain'],native)",s);self.assertNotIn("self.space.result('overlay',native)",s)
 def test_common_projection_preserves_parent_cursor_and_prefix(self):
  p=e.CommonAddressSpace();p.next=0x6E001000;old=p.guest('overlay',123);cursor=p.next;ledger=list(p.ledger())
  a=p.guest('overlay-battle-exit-common-0',123);b=p.guest('overlay-battle-exit-common-579',123)
  bits=p.result('overlay-battle-exit-common-579',999,'bits');self.assertEqual((a,b,bits),(0x20001000,0x32181000,0x321A0000));self.assertEqual(p.next,cursor);self.assertEqual(p.ledger()[:len(ledger)],ledger);self.assertNotEqual(old,a)
 def test_common_projection_reuses_only_same_lifetime_identity(self):
  p=e.CommonAddressSpace();a=p.guest('overlay-battle-exit-common-1',456);self.assertEqual(a,p.guest('overlay-battle-exit-common-1',456));self.assertNotEqual(a,p.guest('overlay-battle-exit-common-2',456))
 def test_common_projection_refuses_out_of_catalog_domain(self):
  with self.assertRaises(ValueError):e.CommonAddressSpace().guest('overlay-battle-exit-common-580',123)
 def test_packet_has_original_constructor_before_owner_binding(self):
  s=inspect.getsource(e.BattleExitMachine.admission);self.assertLess(s.index("'original_scene_packet_constructor'"),s.index("'original_scene_packet_owner_binding'"));off=lambda a:a-0x400000
  self.assertEqual(e.CODE[off(0x4511B7):off(0x4511BC)],bytes((0xE8,))+struct.pack('<i',0x4075E0-0x4511BC))
 def test_no_derived_state_host_writes(self):
  for fn in (e.BattleExitMachine.admission,e.CommonResourceMixin.initialize_common):
   t=ast.parse(textwrap.dedent(inspect.getsource(fn)));calls=[x for x in ast.walk(t) if isinstance(x,ast.Call) and isinstance(x.func,ast.Attribute) and x.func.attr=='mem_write']
   for c in calls:self.assertEqual(ast.unparse(c.args[0]),'COMMON_PATH_PTR')
  s=inspect.getsource(e.BattleExitMachine.admission);self.assertIn('self.bex_before=self.bex_capture()',s);self.assertLess(s.index('self.bex_before='),s.index('self.initialize_common('));self.assertLess(s.index('self.bex_final='),s.index('self.destroy_common('))
 def test_source_has_finite_wait_boundary_and_truthful_scope(self):
  s=inspect.getsource(e.BattleExitMachine.admission)+inspect.getsource(e.BattleExitMachine.capture_frontier);self.assertIn('first_instruction_executed=False',s);self.assertIn('terminal_battle_exit_executed=False',s);self.assertIn('outer_result_consumed=False',s);self.assertIn('original_outer_thread_restored=False',s)
 def test_sorting_pages_exposed_only_after_preserved_parent_capture(self):
  calls=[];m=SimpleNamespace(uc=SimpleNamespace(mem_protect=lambda *args:calls.append(args)))
  e.BattleExitMachine.expose_sorting_scratch(m);self.assertEqual(calls,[(0x791000,0x3000,3)])
  source=inspect.getsource(e.BattleExitMachine.admission);self.assertLess(source.index('self.bex_before='),source.index('self.expose_sorting_scratch()'));self.assertLess(source.index('self.expose_sorting_scratch()'),source.index('self.initialize_common('))
 def test_actual_original_sort_clear_reproduces_write_protection_and_exact_fix(self):
  from unicorn import Uc,UcError,UC_ARCH_X86,UC_MODE_32,UC_HOOK_MEM_WRITE,UC_ERR_WRITE_PROT
  u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x56C000,4096,7);u.mem_write(0x56C000,e.CODE[0x56C000-0x400000:0x56D000-0x400000]);u.mem_protect(0x56C000,4096,5)
  u.mem_map(0x791000,0x3000,3);u.mem_write(0x791000,bytes((0xA5,))*0x3000);u.mem_protect(0x792000,0x2000,1)
  for name,value in [('EDI',0x791730),('ECX',0x2004//4),('EAX',0),('EFLAGS',0x202)]:u.reg_write(getattr(e.x86,'UC_X86_REG_'+name),value)
  ctx=u.context_save()
  with self.assertRaises(UcError) as error:u.emu_start(0x56CF01,0x56CF03,count=3000)
  self.assertEqual(error.exception.errno,UC_ERR_WRITE_PROT);self.assertEqual(u.reg_read(e.x86.UC_X86_REG_EDI),0x792000);self.assertEqual(u.reg_read(e.x86.UC_X86_REG_ECX),1485)
  e.BattleExitMachine.expose_sorting_scratch(SimpleNamespace(uc=u));u.mem_write(0x791000,bytes((0xA5,))*0x3000);u.context_restore(ctx);writes=[]
  token=u.hook_add(UC_HOOK_MEM_WRITE,lambda uc,kind,at,size,value,data:writes.append((at,size,value)));u.emu_start(0x56CF01,0x56CF03,count=3000);u.hook_del(token)
  self.assertEqual(writes,[(p,4,0) for p in range(0x791730,0x793734,4)]);self.assertEqual(bytes(u.mem_read(0x791730,0x2004)),bytes(0x2004));self.assertEqual(bytes(u.mem_read(0x791000,0x730)),bytes((0xA5,))*0x730);self.assertEqual(bytes(u.mem_read(0x793734,0x8CC)),bytes((0xA5,))*0x8CC)

 def test_original_zero_MP_instruction_stops_before_CPU_exception_only_in_scene(self):
  import hashlib
  from unicorn import Uc,UcError,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_ERR_EXCEPTION
  for denominator,label,stopped,current in [(0,'original_scene_loop',True,0),(1,'original_scene_loop',False,0),(0,'common_register',False,0),(0,'original_scene_loop',True,1000000)]:
   with self.subTest(denominator=denominator,label=label,current=current):
    u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x46D000,4096,7);u.mem_write(0x46D000,e.CODE[0x46D000-0x400000:0x46E000-0x400000]);u.reg_write(e.x86.UC_X86_REG_ECX,denominator)
    m=e.BattleExitMachine.__new__(e.BattleExitMachine);m.uc=u;m.battle_stage_active=False;m.bex_active=True;m.bex_pending=[];m.bex_stop=e.STOP;m.bex_actual_stop=None;m.bex_label=label;m.common_text=lambda at:False;m.common_code=lambda at:None;m.gdi_targets=set();m.bex_entries={};m.bex_count=current;m.bex_slice_first=0;m.bex_ih=hashlib.sha256()
    u.hook_add(UC_HOOK_CODE,m.code)
    with patch.object(e.parent.BattleStageMachine,'code',lambda *args:None):
     if denominator==0 and not stopped:
      with self.assertRaises(UcError) as error:u.emu_start(e.MP_STOP,e.MP_STOP+2,count=1)
      self.assertEqual(error.exception.errno,UC_ERR_EXCEPTION)
     else:u.emu_start(e.MP_STOP,e.MP_STOP+2,count=1)
    self.assertEqual(m.bex_actual_stop==e.MP_STOP,stopped);self.assertEqual(m.bex_count,current if stopped else current+1)

 def test_failed_case_serialization_retains_completed_private_case(self):
  import tempfile
  from pathlib import Path
  work=Path(tempfile.mkdtemp(prefix='bex-cases-retention-test-',dir=e.ROOT/'.venv-audit'));file=work/'case-0.json';file.write_bytes(b'original completed case')
  try:e.finish_case_files(work,False);self.assertEqual(file.read_bytes(),b'original completed case')
  finally:e.finish_case_files(work,True)
 def test_successful_source_removes_only_owned_private_cases(self):
  import tempfile
  from pathlib import Path
  work=Path(tempfile.mkdtemp(prefix='bex-cases-success-test-',dir=e.ROOT/'.venv-audit'));(work/'case-0.json').write_bytes(b'complete case');e.finish_case_files(work,True);self.assertFalse(work.exists())
 def test_private_case_root_cannot_be_recursively_removed(self):
  with self.assertRaises(ValueError):e.finish_case_files(e.ROOT/'.venv-audit',True)

 def test_all_complete_tasks_are_counted_at_original_ret(self):
  s=inspect.getsource(e.BattleExitMachine.code);self.assertIn('at==0x454CF0',s);self.assertIn('at==0x454EC1',s);self.assertIn('self.completed_task_observations.append(ev)',s)
 def test_common_forward_and_cleanup_lifetimes_both_recorded(self):
  s=inspect.getsource(e.BattleExitMachine.admission);self.assertIn('common_resources=self.bex_resources_forward',s);self.assertIn('common_resources_after_cleanup=copy.deepcopy(self.common_resources)',s)

if __name__=='__main__':unittest.main()
