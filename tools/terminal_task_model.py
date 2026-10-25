"""Independent input/task admission, one VM instruction and pending source stack."""
import copy,struct,types
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools import terminal_task_emulation as e
from tools import battle_live_terminal_model as combat
from tools.battle_lethal_combat import expand
from tools.school_vm_present import packet_project as old_packet

packet_project=types.FunctionType(old_packet.__code__,dict(old_packet.__globals__,TASK=e.MAIN),argdefs=old_packet.__defaults__)


def num(b,o,f='I'):return struct.unpack_from('<'+f,b,o)[0]


def source_rules():
 raw=e.SOURCE.read_bytes();md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
 checks={0x425E3F:('mov','byte ptr [ecx + 0x630], 0'),0x425F34:('mov','byte ptr [ecx + 0x630], 0xff'),
  0x454D65:('mov','byte ptr [ecx], al'),0x454D76:('mov','byte ptr [ecx], al'),0x454D8B:('call','0x4ce8f0'),
  0x4D024A:('call','0x4d29e0'),0x4D2A78:('call','0x4d2ca0'),0x4D2D52:('call','0x407870')}
 for va,want in checks.items():
  i=next(md.disasm(raw[va-0x400000:va-0x400000+16],va,count=1));e.need((i.mnemonic,i.op_str)==want,'exact original task source '+hex(va));proof.append(dict(va=va,hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
 frames={}
 for start,seh in ((0x454CF0,0),(0x4CE8F0,0),(0x4D29E0,0),(0x4D2CA0,12)):
  rows=list(md.disasm(raw[start-0x400000:start-0x400000+100],start));local=next(i for i in rows[:18] if i.mnemonic=='sub' and i.op_str.startswith('esp, '));frames[start]=4+12+seh+int(local.op_str.split(', ')[1],0)
 return dict(instructions=proof,source_frame_sizes={hex(k):v for k,v in frames.items()}),frames


def verify(row):
 rules,frames=source_rules();a=row['admission'];e.need(len(a['frames'])==2,'two complete original task/phase/world/event frames')
 expected=copy.deepcopy(a['frames'][0][0]['before']);event=expand(row['events'][-1]['after'],row['blobs'])
 e.need(all(expected[k]==event[k] for k in ('VM','task','units','remaining','elapsed')) and expected['work'][:6]==event['work'],'natural terminal request enters task admission')
 e.need(bytes.fromhex(expected['owner'])==bytes(0x10000) and expected['SEH']=='00000000','declared empty owner/input and SEH head')
 task=bytes.fromhex(expected['task']);e.need(task[0x43]==task[0x59]==1 and task[0x44]==0 and num(task,0x38)==5 and num(task,0x60)==e.WORK,'actual terminal selected-task layout')
 def check(step,edits=(),returned=True):
  nonlocal expected
  e.need(step['before']==expected,'continuous independently predicted task input')
  for field,o,value,fmt in edits:
   b=bytearray.fromhex(expected[field]);struct.pack_into('<'+fmt,b,o,value);expected[field]=b.hex()
  e.need(step['after']==expected,'entire input/owner/work/VM/task/units/clock boundary')
  if returned and 'call' in step:e.need(step['call']['result']==0,'natural original reset/task/phase/world return')
 def reset(step):
  owner=bytes.fromhex(expected['owner']);flag=owner[0x180+0x630];e.need(flag in (0,255),'actual pending IME request flag domain')
  check(step,[('owner',0x180+0x630,0,'B')] if flag else [])
 def prepare():
  edits=[('owner',0x180+0x630,255,'B'),('task_input_flag',0,0,'B')]
  # task_input_flag is a scalar observation; its original write must retain zero.
  e.need(expected['task_input_flag']==0,'declared empty per-task input flag');edits.pop()
  return edits
 for i,frame in enumerate(a['frames']):
  e.need(len(frame)==5,'declared reset/task/phase/world/event sequence');reset(frame[0])
  edits=prepare()+[('task',0x44,i+1,'B')]
  if i==0:edits += [('task',o,0,'B') for o in range(0x5C,0x60)]
  check(frame[1],edits);check(frame[2])
  edits=[]
  if i==0:
   edits=[('gates',j,0,'B') for j in (2,3,4,6,7,8)]+[('gates',9,255,'B'),('gates',10,255,'B')]+[('owner_flags',j,1,'B') for j in range(4)]
   edits += [('work',o,0,'B') for o in (0x20E8,0x216C,0x2230)]
  check(frame[3],edits);check(frame[4])
  e.need(frame[4]['event']['call']['result']==0,'busy terminal event does not request another script')
 reset(a['reset']);partial=a['partial'];s0=partial['root']['ESP_before'];vm=s0-frames[0x454CF0]-4
 overlay=vm-frames[0x4CE8F0]-16*4-4;kind=overlay-frames[0x4D29E0]-9*4-4
 packet=kind-4-0x90;seh=kind-4-12;sp=kind-frames[0x4D2CA0]-8-4;ebp=kind-4
 vmraw=bytes.fromhex(expected['VM']);e.need(num(vmraw,0x1C)==0 and vmraw[0x92E0]==vmraw[0x92E1]==vmraw[0x93E2]==0,'original bound and normally admitted VM, no render-suppression flag')
 instruction=num(vmraw,0x10);raw=(e.ROOT/e.terminal.SCRIPT_PATH).read_bytes();offset=instruction-e.SCRIPT
 e.need(raw[offset:offset+8]==struct.pack('<HHI',167,8,0),'real first selected terminal command')
 count=num(bytes.fromhex(expected['VM_counter']),0)
 edits=prepare()+[('VM',0x3C,1,'I'),('VM',0x1C,8,'I'),('VM',0x22,167,'H'),('VM',0x24,8,'H'),('VM_counter',0,(count+1)&0xFFFFFFFF,'I'),('VM_counter',4,0,'I'),('SEH',0,seh,'I')]
 check(partial,edits,False);p=partial['pending'];cpu=p['CPU']
 e.need((p['entry'],p['first_instruction_executed'],p['receiver'],p['caller'],p['args'])==(e.STOP,False,packet,0x4D2D57,[20,0]),'actual first original resource lookup input boundary')
 e.need((cpu['EIP'],cpu['ESP'],cpu['EBP'],cpu['ECX'],cpu['EAX'])==(e.STOP,sp,ebp,packet,0),'independent original nested CPU/stack layout')
 stack=bytes.fromhex(p['stack']);e.need(len(stack)==0x20000,'whole pending original stack retained')
 def stackword(at):return num(stack,at-e.STACK)
 for at,value in ((s0,e.RETURN),(vm,0x454D90),(overlay,0x4D024F),(kind,0x4D2A7D),(sp,0x4D2D57),(sp+4,20),(sp+8,0),(seh,0),(seh+4,0x59081C),(seh+8,0)):
  e.need(stackword(at)==value,'original return/argument/SEH stack word '+hex(at))
 expected_packet=packet_project(0x40);e.need(p['packet']==expected_packet and stack[packet-e.STACK:packet-e.STACK+128].hex()==expected_packet,'complete source-projected overlay packet before resource query')
 e.need(partial['root']['returned'] is False and row['pending_CPU']==cpu,'partial task stays at genuine boundary, never reported returned')
 opened=[row['task_calls'][i] for i in p['open_calls']]
 e.need([x['entry'] for x in opened]==[0x454CF0,0x4CE8F0,0x4D29E0,0x4D2CA0] and all('after' not in x for x in opened),'four actual outstanding original frames')
 return dict(task_roots_returned=2,pending_task_roots=1,normal_VM_instructions=1,VM_PC=8,resource_entry=e.STOP,packet_pointer=packet,SEH_head=seh,
  task_frames=frames,source_rules=rules,remaining=expected['remaining'],elapsed=expected['elapsed'])
