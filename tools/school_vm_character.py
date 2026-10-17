"""Original character27 template, layout/show and active presentation admission."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_vm_panel import ROOT,SOURCE,SOURCE_SHA256,SCRIPT,SCRIPT_SHA,BASE,TASK,TACT,WORK,VM,STACK,RETURN,BASE_SP,BANK,INPUT,MAIN,REGIONS,layout,data,typed,packet_project,ENTRY,source_contract as panel_source
from tools.school_vm_flow import call_protocol as flow_calls

PHASES=('template','handler','overlay','layer_entry');PREVIOUS=dict(zip(PHASES[1:],PHASES[:-1]))
START=dict(zip(PHASES,(ENTRY,0x4CC0F0,0x4CED48,0x4D024F)));STOP=dict(zip(PHASES,(0x4CC0F0,0x4CED48,0x4D024F,0x4CA600)))
TABLE=0x624520+4*38;LAYER=VM+0x6F60+7*0xE0;TEXT=VM+0x430+7*0xAB8
ADDED=(0x4CC600,0x4C9520,0x4CA060,0x4CA960,0x4CA130,0x4CA0B0,0x4CC0F0,0x4CA9B0,0x4CA9E0,0x4CAF10,0x4CAFF0,0x4C9610,0x4CC7D0,0x4CC810,0x4CA0F0,0x4CD850,0x4CA600)

@lru_cache(maxsize=1)
def source_contract():
 r=SOURCE.read_bytes();m=Cs(CS_ARCH_X86,CS_MODE_32)
 if hashlib.sha256(r).hexdigest()!=SOURCE_SHA256 or hashlib.sha256(SCRIPT.read_bytes()).hexdigest()!=SCRIPT_SHA:raise ValueError('VM character source/script SHA')
 template=r[TABLE-BASE:TABLE-BASE+38]
 if struct.unpack('<19H',template)!=(7,256,568,0,0,0,0,308,600,715,691,0,0,4,18,12,473,154,1):raise ValueError('VM character source template4')
 checks={0x4C5EE4:('call','0x4c1eb0'),0x4C5F61:('call','0x4cc600'),0x4C5F87:('call','0x4cc0f0'),0x4C5F99:('call','0x4cc7d0'),0x4C5FA8:('mov','eax, dword ptr [ebp + 0x10]'),0x4CC64E:('mov','word ptr [edx + 0x30], cx'),0x4CC177:('cmp','dword ptr [ebp + 0xc], -1'),0x4CC1C0:('je','0x4cc38e'),0x4CC39B:('mov','word ptr [ecx + 0x22], 1'),0x4CC89C:('call','0x4ca130'),0x4CA1F7:('jmp','dword ptr [eax*4 + 0x4ca5e3]'),0x4CA34A:('call','0x4cd850'),0x4CA375:('call','0x4ca600')};proof=[]
 for va,w in checks.items():
  i=next(m.disasm(r[va-BASE:va-BASE+16],va))
  if (i.mnemonic,i.op_str)!=w:raise ValueError('VM character source operand '+hex(va))
  proof.append(dict(va=hex(va),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
 if struct.unpack_from('<I',r,0x4C1F29-BASE+2*4)[0]!=0x4C1F0E or struct.unpack_from('<I',r,0x4CA5E3-BASE+4)[0]!=0x4CA330:raise ValueError('VM character literal/type3 source dispatch')
 functions=deepcopy(panel_source()['functions'])
 for a in ADDED:
  seq=[]
  for i in m.disasm(r[a-BASE:a-BASE+30000],a):
   seq.append(i)
   if i.mnemonic=='ret':break
  ret=seq[-1];b=ret.address+ret.size;local=next(i for i in seq[:18] if i.mnemonic=='sub' and i.op_str.startswith('esp, '))
  if ret.mnemonic!='ret':raise ValueError('VM character finite function')
  functions.append(dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(r[a-BASE:b-BASE]).hexdigest(),frame=4+int(local.op_str.split(', ')[1],0)+12,args=5 if a==0x4CA600 else int(ret.op_str,0)//4 if ret.op_str else 0,ret=hex(ret.address)))
 return dict(source_image_sha256=SOURCE_SHA256,script_sha256=SCRIPT_SHA,parent_source=panel_source(),functions=functions,instructions=proof,template=dict(pointer=TABLE,bytes=38,hex=template.hex(),index=4,layer=7),decoded_operands=[4,0xFFFFFFF,0xFFFFFFF],scope='Continuous retained character27 body and natural handler return, overlay cleanup, inactive0..6 and active7 interpolation to unexecuted4CA600; no new roots/OS responses, queue/GPU/dialogue or VM/task return')

def native_ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['functions'])

def cpu_expected(phase,inputs):
 v=layout()['vm']
 if phase=='parent':return dict(EIP=ENTRY,ESP=v-144,EBP=v-4,EAX=inputs['script_pointer']+660,ECX=VM)
 if phase=='template':return dict(EIP=STOP[phase],ESP=v-248,EBP=v-148,EAX=VM,ECX=VM)
 if phase=='handler':return dict(EIP=STOP[phase],ESP=v-128,EBP=v-4,EAX=1,ECX=0)
 if phase=='overlay':return dict(EIP=STOP[phase],ESP=v-128,EBP=v-4,EAX=0xCCCCCCCC,ECX=0)
 if phase=='layer_entry':return dict(EIP=STOP[phase],ESP=v-268,EBP=v-136,EAX=(LAYER&0xFFFF0000)|256,ECX=(LAYER&0xFFFF0000)|568)
 raise ValueError('VM character CPU phase')

def project(phase,inputs,before):
 contract=source_contract();d=data(before);v=d[VM];t=d[TACT];o=LAYER-VM
 if phase not in PHASES or inputs.get('driver')!='continuous_original_character_VM_task' or inputs.get('script_sha256')!=SCRIPT_SHA or inputs.get('template')!=contract['template'] or not inputs.get('script_pointer') or inputs.get('texture_record',{}).get('bytes')!=84:raise ValueError('VM character fixed phase/captured inputs')
 ptr=inputs['script_pointer'];pc=224 if phase=='layer_entry' else 208;wait=0 if pc==208 else 1
 if struct.unpack_from('<I',t,0x64)[0]!=ptr or struct.unpack_from('<I',t,0x60)[0]!=WORK or t[0x43]!=1 or t[0x44]!=2 or t[0x59]!=1 or struct.unpack_from('<I',t,0x48)[0]!=1 or v[4:6]!=b'\x01\x01' or struct.unpack_from('<I',v,0x10)[0]!=ptr+452 or struct.unpack_from('<I',v,0x1C)[0]!=pc or struct.unpack_from('<3H',v,0x20)!=(wait,27,16) or v[0x1CC]!=255 or v[0x1CD] or v[0x9228] or struct.unpack_from('<I',v,0x3C)[0]:raise ValueError('VM character actual retained VM/task')
 if any(d[0]) or any(d[TASK+0xB28E]) or any(d[WORK+0x2434]) or v[0x92E0] or v[0x92E1] or v[0x93E2]:raise ValueError('VM character captured disabled renderer/menu/pose guard')
 for i in range(10):
  if i!=7 and any(v[0x6F60+i*0xE0+j] for j in (2,3,4,5,0x22,0x23,0x30,0x31)):raise ValueError('VM character other inactive layers')
 if phase=='template':
  if any(v[o+j] for j in (2,3,4,5,0x22,0x23,0x30,0x31)):raise ValueError('VM character captured initial layer7')
  struct.pack_into('<3I',v,0x9250,4,0xFFFFFFF,0xFFFFFFF)
  for offset,value in ((0x30,0),(0,1),(0xC,256),(0xE,568),(0x1E,308),(0x20,600),(0x4C,0),(0x16,18),(0x18,12),(0x1A,473),(0x1C,154),(2,1),(6,0),(8,1),(0x10,8)):struct.pack_into('<H',v,o+offset,value)
 else:
  if struct.unpack_from('<3I',v,0x9250)!=(4,0xFFFFFFF,0xFFFFFFF):raise ValueError('VM character original decoded scratch operands')
  if phase=='handler':
   if struct.unpack_from('<H',v,o+2)[0]!=1:raise ValueError('VM character actual template setup state')
   q=TEXT-VM;struct.pack_into('<H',v,q,24);v[q+4]=0;struct.pack_into('<H',v,q+6,12);v[q+10]=0
   for offset,value in ((0x40,36),(0x42,37),(0x26,8),(0x22,1),(0x24,0),(0x10,45),(0x12,0),(0x14,0),(2,3),(6,0)):struct.pack_into('<H',v,o+offset,value)
  else:
   if struct.unpack_from('<H',v,o+2)[0]!=3 or struct.unpack_from('<H',v,o+6)[0] or struct.unpack_from('<H',v,o+0x10)[0]!=45 or struct.unpack_from('<H',v,o+0x22)[0]!=1:raise ValueError('VM character actual show/interpolation state')
   if phase=='overlay':struct.pack_into('<IH',v,0x1C,224,1)
   else:
    for i in range(7):a=0x6F60+i*0xE0;v[a+4:a+6]=v[a+2:a+4]
 out=deepcopy(before)
 for r in out:r['hex']=d[r['pointer']].hex()
 cpu=cpu_expected(phase,inputs);pending=None
 if phase in ('template','layer_entry'):
  va,ret,recv,args=(0x4CC0F0,0x4C5F8C,VM,[4,0xFFFFFFF,0xFFFFFFF]) if phase=='template' else (0x4CA600,0x4CA37A,cpu['ECX'],[(LAYER&0xFFFF0000)|256,(LAYER&0xFFFF0000)|568,1,0,66])
  pending=dict(va=hex(va),return_va=hex(ret),sp=cpu['ESP'],receiver=recv,args=args,first_instruction_executed=False)
 tex=inputs['texture_record'];packet=dict(pointer=layout()['packet'],bytes=128,hex=packet_project(0xC0,tex,int.from_bytes(d[TASK+0xB210],'little'))) if phase=='overlay' else None
 return dict(after=out,CPU=cpu,packet=packet,pending=pending,PC=struct.unpack_from('<I',v,0x1C)[0],wait=struct.unpack_from('<H',v,0x20)[0],character_returned=phase!='template',character_return=None if phase=='template' else 1,VM_returned=False,task_returned=False,GPU_executed=False,graphics_list_executed=False,dialogue_executed=False,full_outer_frame_executed=False,persistent_write_authority=False)

def call_protocol(phase,inputs,before):
 l=layout();a=TABLE&0xFFFF0000;b=LAYER&0xFFFF0000
 if phase=='template':return [(ENTRY,0x4CED48,VM,[0,inputs['script_pointer']+660,1])]+[(0x4C1EB0,ret,VM,[0,2,val]) for ret,val in ((0x4C5EE9,4),(0x4C5F17,0xFFFFFFF),(0x4C5F45,0xFFFFFFF))]+[(0x4CC600,0x4C5F66,VM,[4]),(0x4C9520,0x4CC65A,LAYER,[]),(0x4CA060,0x4CC672,LAYER,[a|256,b|568]),(0x4CA960,0x4CC68A,LAYER,[a|308,600]),(0x4CA130,0x4CC72D,LAYER,[1,0,1,0xFFFFFFFF]),(0x4CA0B0,0x4CC737,LAYER,[8]),(0x4CC0F0,0x4C5F8C,VM,[4,0xFFFFFFF,0xFFFFFFF])]
 if phase=='handler':return [(0x4CC0F0,0x4C5F8C,VM,[4,0xFFFFFFF,0xFFFFFFF]),(0x4CA9B0,0x4CC155,LAYER,[]),(0x4CA9E0,0x4CC160,LAYER,[]),(0x4CAF10,0x4CC16D,TEXT,[24]),(0x4CAFF0,0x4CC177,TEXT,[12]),(0x4C9610,0x4CC398,LAYER,[8]),(0x4CC7D0,0x4C5F9E,VM,[4]),(0x4CC810,0x4CC7FB,VM,[4,0]),(0x4CA0B0,0x4CC87E,LAYER,[45]),(0x4CA0F0,0x4CC88B,LAYER,[(LAYER&0xFFFF0000)|0]),(0x4CA130,0x4CC8A1,LAYER,[3,0,0xFFFFFFFF,0xFFFFFFFF])]
 if phase=='overlay':return flow_calls('wait',inputs,before,False)[17:40]
 if phase=='layer_entry':
  from tools.school_vm_draw import call_protocol as maintenance
  return maintenance('vm')[:21]+[(0x4CA1B0,0x4D028E,LAYER,[]),(0x4CD850,0x4CA34F,VM,[LAYER&0xFFFF0000,45,255]),(0x4CA600,0x4CA37A,(LAYER&0xFFFF0000)|568,[(LAYER&0xFFFF0000)|256,(LAYER&0xFFFF0000)|568,1,0,66])]
 raise ValueError('VM character call phase')
