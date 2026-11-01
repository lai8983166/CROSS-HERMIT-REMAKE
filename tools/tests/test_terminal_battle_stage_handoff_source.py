"""Finite original battle stage handoff after the accepted completion flag."""
import ast,contextlib,inspect,io,struct,textwrap,unittest
from types import SimpleNamespace
from unittest.mock import patch
from tools import terminal_battle_stage_handoff_emulation as e

CAPSTONE=(0x454290,0x4542b4,0x45444b,0x454468,0x4544dc,0x4544fb,0x45451a,0x454536,0x454552,0x45462d,0x454653,0x454670,0x4547a1,0x4547b1,0x4547c1)

class TerminalBattleStageHandoffSourceTests(unittest.TestCase):
 def test_source_guard_algorithm_and_reference_unchanged(self):
  old=e.parent.TaskCompletionMachine.source_code;new=e.BattleStageMachine.source_code
  self.assertEqual(old.__code__,new.__code__);self.assertIs(new.__globals__['ALLOWED'],e.ALLOWED)
  self.assertEqual(e.REFERENCE.__code__,e.parent.REFERENCE.__code__)
  added=frozenset(a for lo,hi in e.EXTRA_RANGES for a in range(lo,hi))-e.parent.ALLOWED
  self.assertEqual(e.ALLOWED-e.parent.ALLOWED,added)
  self.assertTrue(all(lo in e.ALLOWED and hi-1 in e.ALLOWED for lo,hi in e.EXTRA_RANGES))
 def test_only_declared_original_extents(self):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  md=Cs(CS_ARCH_X86,CS_MODE_32)
  self.assertEqual(e.EXTRA_RANGES,((0x4998B0,0x499901),(0x499910,0x499B5D),(0x49AD50,0x49AD8C),(0x4DB2B0,0x4DB2F4),(0x4116A4,0x411CE2),(0x4DAAE0,0x4DAB06)))
  for lo,hi in e.EXTRA_RANGES:
   seq=list(md.disasm(e.CODE[lo-0x400000:hi-0x400000],lo));self.assertTrue(seq)
   if lo==0x4116A4:
    self.assertEqual((seq[-1].mnemonic,seq[-1].op_str,seq[-1].address,seq[-1].address+seq[-1].size),('xor','eax, eax',0x411CE0,hi))
    self.assertEqual(e.CODE[0x411CE2-0x400000],0x5F)
   else:
    self.assertEqual((seq[0].mnemonic,seq[0].op_str),('push','ebp'));self.assertEqual(seq[-1].mnemonic,'ret');self.assertEqual(seq[-1].address+seq[-1].size,hi)
 def test_selector_result_state_and_configuration_tables(self):
  off=lambda a:a-0x400000
  selectors=(0x453F4A,0x453F77,0x454063,0x45413B,0x454266,0x454290,0x4542B9,0x4542EC,0x454310,0x454336,0x45435A,0x454380,0x45439D,0x4543E9,0x45441D,0x45444B,0x454468,0x45462D,0x454653,0x454670,0x4547A1)
  types=(0x4544C8,0x4544DC,0x4544FB,0x45451A,0x454536,0x454552)
  states=(0x49999D,0x4999CF,0x499A50,0x499ABE,0x499AFD,0x499B35)
  self.assertEqual(struct.unpack_from('<21I',e.CODE,off(0x4547C2)),selectors)
  self.assertEqual(struct.unpack_from('<6I',e.CODE,off(0x454816)),types)
  self.assertEqual(struct.unpack_from('<6I',e.CODE,off(0x499B5D)),states)
  self.assertEqual(e.CODE[off(0x4547C1)],0xC3)
  self.assertTrue(all(x in e.ALLOWED for x in selectors+types+states))
  self.assertEqual(e.RESULT_TYPE_CONFIGURATION,{1:2,2:3,3:4,4:5,5:6});self.assertEqual(e.RESULT_MODES,{1:0,2:1,3:1,4:2,5:2})
  for i,want in enumerate(((0,2048,120,2048,512,336,1),(0,2048,16,2048,512,304,0),(0,2048,120,2048,512,304,1),(0,2048,120,2048,512,304,1),(0,2048,120,2048,512,304,1),(0,2048,120,2048,512,304,1),(0,2048,120,2048,512,304,1),(0,4096,60,4096,512,336,1))):
   self.assertEqual(struct.unpack_from('<7h',e.CODE,off(0x59EAA4+i*0xE)),want)
 def test_completion_flag_and_result_dispatch_exact_instructions(self):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  md=Cs(CS_ARCH_X86,CS_MODE_32)
  expected={0x454290:('mov','ecx, dword ptr [ebp - 4]'),0x454293:('movsx','edx, byte ptr [ecx + 0x171]'),0x45429a:('test','edx, edx'),0x45429c:('je','0x4542b4'),0x4542a1:('mov','word ptr [eax + 0x108cc2], 0'),0x4542ad:('mov','dword ptr [ecx + 0x38], 0xf'),
   0x453F4D:('mov','word ptr [eax + 0x108cc2], 1'),0x4543F6:('mov','word ptr [edx + 0x108cc2], 1'),0x45442E:('mov','word ptr [eax + 0x108cc2], 0'),
   0x45444b:('mov','word ptr [0x7a4184], 0'),0x454457:('mov','edx, dword ptr [ecx + 0x38]'),0x45445a:('add','edx, 1'),0x454460:('mov','dword ptr [eax + 0x38], edx'),
   0x454468:('push','4'),0x45446a:('mov','ecx, dword ptr [0x7a49fc]'),0x454470:('call','0x415040'),0x454475:('mov','cx, word ptr [0x7a4184]'),0x45447c:('add','cx, ax'),0x45447f:('mov','word ptr [0x7a4184], cx'),0x454486:('movsx','edx, word ptr [0x7a4184]'),0x45448d:('cmp','edx, 0xff'),0x454493:('jl','0x454628'),0x4544a5:('mov','dword ptr [edx + 0x38], ecx'),0x4544ab:('mov','ecx, dword ptr [eax + 0x174]'),0x4544b4:('cmp','dword ptr [ebp - 0x18], 5'),0x4544b8:('ja','0x45456e'),0x4544c1:('jmp','dword ptr [edx*4 + 0x454816]'),
   0x4544dc:('push','2'),0x4544de:('mov','ecx, dword ptr [ebp - 4]'),0x4544e1:('add','ecx, 0x190'),0x4544e7:('call','0x4998b0'),0x4544ec:('mov','dword ptr [0x5ff720], 0'),0x4544f6:('jmp','0x45459e'),
   0x4544fb:('push','3'),0x454506:('call','0x4998b0'),0x45450b:('mov','dword ptr [0x5ff720], 1'),0x45451a:('push','4'),0x454525:('call','0x4998b0'),0x45452a:('mov','dword ptr [0x5ff720], 1'),0x454536:('push','5'),0x454541:('call','0x4998b0'),0x454546:('mov','dword ptr [0x5ff720], 2'),0x454552:('push','6'),0x45455d:('call','0x4998b0'),0x454562:('mov','dword ptr [0x5ff720], 2'),
   0x45459e:('movsx','edx, word ptr [0x7f4488]'),0x4545a8:('cmp','dword ptr [ebp - 0x1c], 0x2d'),0x4545ac:('je','0x4545b0'),0x4545ae:('jmp','0x454628'),
   0x45462d:('mov','ecx, dword ptr [ebp - 4]'),0x454630:('add','ecx, 0x190'),0x454636:('call','0x499910'),0x45463b:('test','eax, eax'),0x45463d:('je','0x45464e'),0x45464b:('mov','dword ptr [ecx + 0x38], eax'),0x45464e:('jmp','0x4547a8'),
   0x454653:('mov','word ptr [0x7a417c], 0x4ff'),0x454668:('mov','dword ptr [ecx + 0x38], eax'),0x454670:('mov','dword ptr [ebp - 8], 0'),0x454677:('mov','dword ptr [ebp - 0xc], 0x3f'),0x4547a1:('mov','eax, 1'),0x4547a8:('xor','eax, eax'),0x4547b1:('pop','edi'),0x4547b4:('add','esp, 0x60'),0x4547c1:('ret','')}
  for at,want in expected.items():
   i=next(md.disasm(e.CODE[at-0x400000:at-0x400000+16],at));self.assertEqual((i.mnemonic,i.op_str),want,hex(at))
 def test_substage_word_stores_are_only_zero_or_one(self):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  md=Cs(CS_ARCH_X86,CS_MODE_32);off=lambda a:a-0x400000
  self.assertEqual([0x400000+i for i in range(len(e.CODE)-3) if e.CODE[i:i+4]==b'\xc2\x8c\x10\x00'],[0x453F50,0x4542A4,0x4543F9,0x454431])
  values={}
  for at in (0x453F4D,0x4542A1,0x4543F6,0x45442E):
   i=next(md.disasm(e.CODE[off(at):off(at)+12],at));values[at]=int(i.op_str.rsplit(', ',1)[1],0)
  self.assertEqual(values,{0x453F4D:1,0x4542A1:0,0x4543F6:1,0x45442E:0})
 def test_natural_result_handoff_call_site_bytes(self):
  off=lambda a:a-0x400000
  self.assertEqual(e.CODE[off(0x454793):off(0x454798)],b'\xe8'+struct.pack('<i',0x473860-0x454798))
  self.assertEqual(e.CODE[off(0x454798):off(0x45479d)],b'\xb8\x01\x00\x00\x00')
  self.assertEqual(e.CODE[off(0x45479d):off(0x45479f)],b'\xeb\x12')
 def test_animation_entry_and_state_machine_bytes(self):
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  md=Cs(CS_ARCH_X86,CS_MODE_32)
  expected={0x4998D0:('add','eax, 0x30998'),0x4998DB:('mov','dl, byte ptr [ebp + 8]'),0x4998DE:('mov','byte ptr [ecx + 2], dl'),0x4998E4:('mov','dword ptr [eax + 8], 0'),0x4998EE:('mov','byte ptr [ecx + 1], 0'),0x4998F5:('mov','byte ptr [edx], 1'),0x4998FE:('ret','4'),
   0x499938:('mov','ecx, dword ptr [ebp - 8]'),0x49993B:('movsx','edx, byte ptr [ecx + 2]'),0x49993F:('imul','edx, edx, 0xe'),0x499942:('add','edx, 0x59eaa4'),0x49995C:('mov','word ptr [eax + 0x10], dx'),0x49996A:('mov','word ptr [eax + 0x12], dx'),
   0x499971:('movsx','ecx, byte ptr [eax]'),0x499976:('jne','0x49997f'),0x499978:('xor','eax, eax'),0x499996:('jmp','dword ptr [ecx*4 + 0x499b5d]'),
   0x4999A0:('mov','dword ptr [edx + 8], 0'),0x4999B5:('call','0x415040'),0x4999BD:('mov','dword ptr [edx + 0xc], eax'),0x4999CC:('mov','byte ptr [edx + 1], cl'),
   0x4999D8:('add','ecx, dword ptr [edx + 0xc]'),0x4999E4:('cmp','dword ptr [ecx + 8], 0xff00'),0x4999EB:('jl','0x499a4b'),0x4999F0:('mov','dword ptr [edx + 8], 0xff00'),0x4999FA:('movsx','ecx, word ptr [eax + 0xc]'),0x499A0B:('call','0x456b20'),0x499A25:('mov','byte ptr [edx + 1], cl'),
   0x499A5C:('and','edx, 1'),0x499A6E:('and','ecx, 0x8000'),0x499A8F:('push','5'),0x499A91:('mov','ecx, dword ptr [ebp - 4]'),0x499A94:('call','0x49ad50'),0x499A9C:('mov','byte ptr [ecx + 1], 4'),0x499AAE:('call','0x415040'),0x499AB6:('mov','dword ptr [ecx + 0xc], eax'),
   0x499B03:('mov','ecx, dword ptr [edx + 8]'),0x499B06:('sub','ecx, dword ptr [eax + 0xc]'),0x499B12:('cmp','dword ptr [eax + 8], 0xff'),0x499B19:('jg','0x499b33'),0x499B1E:('mov','dword ptr [ecx + 8], 0'),0x499B2B:('add','al, 1'),0x499B30:('mov','byte ptr [ecx + 1], al'),
   0x499B38:('mov','byte ptr [edx], 0'),0x499B3B:('mov','dword ptr [ebp - 0x10], 1'),0x499B4C:('pop','edi')}
  for at,want in expected.items():
   i=next(md.disasm(e.CODE[at-0x400000:at-0x400000+16],at));self.assertEqual((i.mnemonic,i.op_str),want,hex(at))
 def test_only_declared_mutable_ranges_and_no_host_writes(self):
  self.assertEqual(e.NEW_MUTABLE,((e.TASK+0x38,e.TASK+0x3C),(e.TASK+0x108CC2,e.TASK+0x108CC4),(0x7A417C,0x7A4186),(0x5FF720,0x5FF724),(e.CTRL+0x30998,e.CTRL+0x30998+0x14),(0x7F44BE,0x7F44CE),(0x7F4518,0x7F7C18)))
  original=[(10,20),(40,50)];protections=[]
  def parent_init(m,*a,**k):
   m.mutable=list(original);m.uc=SimpleNamespace(mem_protect=lambda at,size,prot:protections.append((at,size,prot)))
  with patch.object(e.parent.TaskCompletionMachine,'__init__',parent_init):m=e.BattleStageMachine()
  self.assertEqual(m.mutable,original+list(e.NEW_MUTABLE))
  # The accepted parent lifetime keeps the unsplit RX image capture; only the
  # original .data mode-word page is re-exposed, and only when the stage starts.
  from unicorn import UC_PROT_READ,UC_PROT_WRITE
  self.assertEqual(protections,[])
  m.bsh_expose_animation_mode()
  self.assertEqual(protections,[(0x5FF000,0x1000,UC_PROT_READ|UC_PROT_WRITE)])
  self.assertEqual(e.NEW_MUTABLE[3],(0x5FF720,0x5FF724))
  admission=inspect.getsource(e.BattleStageMachine.admission)
  self.assertLess(admission.index('self.bsh_before=self.bsh_capture()'),admission.index('self.bsh_expose_animation_mode()'))
  tree=ast.parse(textwrap.dedent(inspect.getsource(e.BattleStageMachine.__init__)))
  self.assertFalse(any(isinstance(n,ast.Attribute) and n.attr in ('put','mem_write','reg_write','emu_start') for n in ast.walk(tree)))
 def test_stage_platform_counters_frozen_at_the_boundary(self):
  self.assertEqual(e.STAGE_PLATFORM_COUNTS,('CRT_APIs','CRT_wire','resource_steps','task_APIs','APIs','GPU_wire','GDI_trace','GDI_stages','overlay_commands'))
  source=inspect.getsource(e.BattleStageMachine.admission)
  self.assertIn("self.bsh_counts_after=self.bsh_prefix_counts()",source)
  self.assertIn("no new platform call during the original result stage",source)
  self.assertIn("counts_after=self.bsh_counts_after,text_APIs=self.bsh_text_APIs",source)
  self.assertNotIn('GDI_trace=len(row',inspect.getsource(__import__('tools.terminal_battle_stage_handoff_verification',fromlist=['no_new_platform_calls']).no_new_platform_calls))
 def test_parent_completion_and_successor_guards_not_relaxed(self):
  source=inspect.getsource(e.parent.TaskCompletionMachine.code)
  self.assertIn("at not in (0x453F10,0x454793,0x473860,0x4CE9C5)",source)
  mine=inspect.getsource(e.BattleStageMachine.code)
  for want in ("at not in (0x424F80,0x4CE9C5,0x454E18)","not 0x41F732<=at<0x41F811","self.battle_stage_result_call and self.get(sp)==0x454798","not self.battle_stage_result_seen","entry=at,kind='result_handoff'"):self.assertIn(want,mine)
 def test_action_word_model_matches_every_original_or_site(self):
  import re
  from capstone import Cs,CS_ARCH_X86,CS_MODE_32
  md=Cs(CS_ARCH_X86,CS_MODE_32);ins=list(md.disasm(e.CODE[0x4116A4-0x400000:0x411CE2-0x400000],0x4116A4))
  key=re.compile(r'^mov (al|cl|dl|bl), byte ptr \[[a-z0-9]+ \+ (0x[0-9a-f]+)\]$')
  bit=re.compile(r'^or (al|cl|dl|bl|ah|ch|dh|bh|eax|ecx|edx|ebx), (0x[0-9a-f]+|\d+)$')
  high={'ah','ch','dh','bh'};found={};pending=None
  for n in ins:
   text=n.mnemonic+' '+n.op_str
   m=key.match(text)
   if m:
    d=int(m.group(2),16);pending=d if 0x480<=d<0x780 else None;continue
   if pending is not None and n.mnemonic=='or':
    o=bit.match(text);self.assertIsNotNone(o,'unparsed original OR '+hex(n.address)+' '+text)
    reg,imm=o.group(1),int(o.group(2),0)
    value=imm.bit_length()-1+(8 if reg in high else 0)
    key_offset=pending-0x480 if pending<0x680 else pending-0x680
    found.setdefault(key_offset,set()).add(value);pending=None
  expected={}
  for offset,value in e.ACTION_CODES:expected.setdefault(offset,set()).add(value)
  self.assertEqual({k:sorted(v) for k,v in found.items()},{k:sorted(v) for k,v in expected.items()})
  self.assertEqual(sorted(e.ACTION_CODES),sorted(((0xC8,0),(0xD0,1),(0xCB,2),(0xCD,3),(0x52,4),(0x4F,5),(0x50,6),(0x51,7),(0x4B,8),(0x4C,9),(0x4D,10),(0x47,11),(0x48,12),(0x49,13),(0x1C,14),(0x39,15),(0x01,16),(0x2A,17),(0x36,17),(0x1D,18),(0x9D,18))))
 def test_keyboard_prediction_adds_original_action_words(self):
  before=bytearray(0xA00);before[12+0x39]=128
  after=e.predict_keyboard(bytes(before))
  self.assertEqual(struct.unpack_from('<5I',after,0x890),(0,0x8000,0x8000,0x8000,0))
  before2=bytearray(0xA00);struct.pack_into('<I',before2,0x894,0x8000)
  after2=e.predict_keyboard(bytes(before2))
  self.assertEqual(struct.unpack_from('<5I',after2,0x890),(0x8000,0,0,0,0x8000))
  self.assertEqual(bytes(after2)[0x380:0x480],bytes(before2)[0x380:0x480])
 def test_input_text_apis_are_the_accepted_predecessor_calls(self):
  from tools import terminal_task_emulation as task
  self.assertEqual(e.TEXT_APIS,{0x76182A80:('ImmGetOpenStatus',0x5920EC,0x425C99),0x770206E0:('lstrlenA',0x5922C4,None)})
  self.assertEqual(task.APIS,{0x76182A80:('ImmGetOpenStatus',0x5920EC,0x425C99),0x770206E0:('lstrlenA',0x5922C4,0x425A7E)})
  off=lambda a:a-0x400000
  self.assertEqual(struct.unpack_from('<I',e.CODE,off(0x5920EC))[0],0x76182A80)
  self.assertEqual(struct.unpack_from('<I',e.CODE,off(0x5922C4))[0],0x770206E0)
  self.assertEqual(e.CODE[off(0x425C94):off(0x425C99)].hex(),'e8b1701400')
  self.assertEqual(e.CODE[off(0x56CD4A):off(0x56CD50)].hex(),'ff25ec205900')
 def prefix(self,change=False):
  want=dict(instructions=10,writes=5,code_sha256='a'*64,write_sha256='b'*64)
  machine=SimpleNamespace(live_input=dict(name='neutral_running'),mark=lambda:dict(want,writes=6) if change else want)
  with patch.object(e,'fixed_parent_forward_summaries',return_value=dict(neutral_running=want)),contextlib.redirect_stdout(io.StringIO()):return e.validate_parent_prefix(machine)
 def test_all_four_parent_cumulative_fields_exact(self):self.assertEqual(self.prefix()['expected'],self.prefix()['actual'])
 def test_changed_parent_prefix_refused(self):
  with self.assertRaises(ValueError):self.prefix(True)
 def test_helpers_retain_original_capacity_and_ABI(self):self.assertTrue(e.helper_contract()['capacity_and_ABI_unchanged'])

if __name__=='__main__':unittest.main()
