"""Original four-piece frame graphics and retained null-renderer-owner read boundary."""
import hashlib,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_vm_character import ROOT,SOURCE,SOURCE_SHA256,SCRIPT,SCRIPT_SHA,BASE,TASK,TACT,WORK,VM,STACK,RETURN,BASE_SP,BANK,REGIONS,layout,data,packet_project,LAYER,source_contract as character_source,cpu_expected as character_cpu

PHASES=('graphics','rectangle','owner_read');PREVIOUS=dict(zip(PHASES[1:],PHASES[:-1]))
START=dict(zip(PHASES,(0x4CA600,0x4CA37A,0x40E2A0)));STOP=dict(zip(PHASES,(0x4CA37A,0x40E2A0,0x40E2D0)))
FRAME=0x624734;MANAGER=TASK+0x1058;ADDED=(0x4CBDB0,0x410310,0x40E2A0)
RECT=[274,580,473,154,67,0x223438,1]

def positions():
 v=layout()['vm'];return dict(frame=v-268,sprite=v-404,packet=v-552,seh=v-420,rectangle=v-276,clip=v-384)

@lru_cache(maxsize=1)
def source_contract():
 r=SOURCE.read_bytes();m=Cs(CS_ARCH_X86,CS_MODE_32)
 if hashlib.sha256(r).hexdigest()!=SOURCE_SHA256 or hashlib.sha256(SCRIPT.read_bytes()).hexdigest()!=SCRIPT_SHA:raise ValueError('VM graphics source/script SHA')
 if struct.unpack_from('<I',r,0x624834-BASE+4)[0]!=FRAME:raise ValueError('VM graphics style1 source table')
 rows=[list(struct.unpack_from('<6h',r,FRAME-BASE+i*12)) for i in range(4)]
 if rows!=[[0,0,100,0,26,176],[487,0,126,0,26,176],[25,0,0,224,462,22],[25,154,0,246,462,22]] or struct.unpack_from('<h',r,FRAME-BASE+48)[0]!=-1:raise ValueError('VM graphics complete four rows/sentinel')
 checks={0x4CA6F7:('call','0x4cbdb0'),0x4CBDEE:('call','0x4075e0'),0x4CBE64:('call','0x407870'),0x4CBEAB:('call','0x4079c0'),0x4CBECE:('call','0x407710'),0x4CA397:('call','0x4cd850'),0x4CA404:('call','0x410310'),0x410340:('call','0x40e2a0'),0x40E2CE:('mov','ecx, dword ptr [eax]'),0x40E2D0:('mov','edx, dword ptr [ecx + 0xb278]'),0x40D993:('mov','dword ptr [eax], ecx'),0x40D99A:('call','0x4142b0'),0x413500:('call','0x40d970')};proof=[]
 for va,w in checks.items():
  i=next(m.disasm(r[va-BASE:va-BASE+16],va))
  if (i.mnemonic,i.op_str)!=w:raise ValueError('VM graphics source operand '+hex(va))
  proof.append(dict(va=hex(va),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
 functions=deepcopy(character_source()['functions'])
 for a in ADDED:
  seq=[]
  for i in m.disasm(r[a-BASE:a-BASE+30000],a):
   seq.append(i)
   if i.mnemonic=='ret':break
  ret=seq[-1];b=ret.address+ret.size;local=next(i for i in seq[:18] if i.mnemonic=='sub' and i.op_str.startswith('esp, '))
  if ret.mnemonic!='ret':raise ValueError('VM graphics finite function')
  functions.append(dict(va=hex(a),end=hex(b),sha256=hashlib.sha256(r[a-BASE:b-BASE]).hexdigest(),frame=4+int(local.op_str.split(', ')[1],0)+12+(12 if a==0x4CBDB0 else 0),args=int(ret.op_str,0)//4 if ret.op_str else 0,ret=hex(ret.address)))
 return dict(source_image_sha256=SOURCE_SHA256,script_sha256=SCRIPT_SHA,parent_source=character_source(),functions=functions,instructions=proof,frame_table=dict(pointer=FRAME,bytes=50,hex=r[FRAME-BASE:FRAME-BASE+50].hex(),rows=rows),renderer_prerequisite=dict(initializer='0x40d970',owner_store='0x40d993',device_call='0x40d99a',original_caller='0x413500',captured_owner=0,first_read='0x40e2d0',effective_address='0xb278'),scope='Four full native frame sprites and natural list return, rectangle admission and clip prefix to unexecuted owner0 read; no owner/gate repair, target read, clipping/queue/debug/GPU/VM-task/dialogue completion')

def native_ranges():return tuple((int(r['va'],16),int(r['end'],16)) for r in source_contract()['functions'])

def cpu_expected(phase,inputs):
 v=layout()['vm']
 if phase=='parent':return character_cpu('layer_entry',inputs)
 if phase=='graphics':return dict(EIP=STOP[phase],ESP=v-264,EBP=v-136,EAX=24,ECX=FRAME)
 if phase=='rectangle':return dict(EIP=STOP[phase],ESP=v-384,EBP=v-280,EAX=274,ECX=MANAGER)
 if phase=='owner_read':return dict(EIP=STOP[phase],ESP=v-484,EBP=v-388,EAX=MANAGER,ECX=0)
 raise ValueError('VM graphics CPU phase')

def sprite_args(row):return [256+row[0],568+row[1],(FRAME&0xFFFF0000),0xFFFFFFFF,66,*row[2:],20,0]

def sprite_packet(row,inputs,before):
 d=data(before);p=bytearray.fromhex(packet_project(0xC0,inputs['texture_record'],int.from_bytes(d[TASK+0xB210],'little')))
 struct.pack_into('<HH',p,0x38,row[4],row[5]);struct.pack_into('<4H',p,0x78,row[2],row[3],row[2]+row[4],row[3]+row[5]);struct.pack_into('<H',p,0x76,66);p[0x67]=0
 # Original4079C0 stores signed32 destination coordinates;407A50 receives0/0.
 struct.pack_into('<2i',p,0x68,256+row[0],568+row[1])
 return dict(pointer=positions()['packet'],bytes=128,hex=p.hex())

def project(phase,inputs,before):
 c=source_contract();d=data(before);v=d[VM];o=LAYER-VM
 if phase not in PHASES or inputs.get('driver')!='continuous_original_graphics_VM_task' or inputs.get('script_sha256')!=SCRIPT_SHA or inputs.get('frame_table')!=c['frame_table'] or inputs.get('manager_owner')!=0:raise ValueError('VM graphics fixed phase/captured inputs')
 tex=inputs.get('texture_record');ptr=inputs.get('script_pointer')
 if not tex or tex['pointer']!=int.from_bytes(d[BANK][:4],'little') or tex['bytes']!=84 or len(bytes.fromhex(tex['hex']))!=84 or struct.unpack_from('<I',d[BANK],4)[0]!=1 or struct.unpack_from('<I',d[TACT],0x64)[0]!=ptr or struct.unpack_from('<I',v,0x10)[0]!=ptr+452:raise ValueError('VM graphics actual script/texture binding')
 if struct.unpack_from('<I3H',v,0x1C)!=(224,1,27,16) or v[0x1CC]!=255 or struct.unpack_from('<H',v,o+2)[0]!=3 or struct.unpack_from('<H',v,o+6)[0] or struct.unpack_from('<H',v,o+0x10)[0]!=45 or any(d[0]) or any(d[TASK+0xB28E]) or any(d[WORK+0x2434]):raise ValueError('VM graphics retained active layer/disabled renderer')
 packets=[dict(**sprite_packet(row,inputs,before),seh=positions()['seh']) for row in c['frame_table']['rows']] if phase=='graphics' else []
 pending=dict(va='0x40e2a0',return_va='0x410345',sp=cpu_expected(phase,inputs)['ESP'],receiver=MANAGER,args=RECT[:4],first_instruction_executed=False) if phase=='rectangle' else None
 read=dict(va='0x40e2d0',base_register='ECX',base=0,offset=0xB278,effective_address=0xB278,bytes=4,instruction_executed=False,target_read=False,requires_original_renderer_initialization=True) if phase=='owner_read' else None
 return dict(after=deepcopy(before),CPU=cpu_expected(phase,inputs),packets=packets,packet={k:val for k,val in packets[-1].items() if k!='seh'} if packets else None,pending=pending,blocked_read=read,PC=224,wait=1,graphics_list_returned=True,graphics_list_return=24,clipping_returned=False,queue_executed=False,debug_response_executed=False,GPU_executed=False,dialogue_executed=False,VM_returned=False,task_returned=False,full_outer_frame_executed=False,persistent_write_authority=False)

def sprite_calls(row):
 p=positions()['packet'];x,y=sprite_args(row)[:2]
 return [(0x4CBDB0,0x4CA6FC,VM,sprite_args(row)),(0x4075E0,0x4CBDF3,p,[]),(0x403620,0x40761A,p,[]),(0x41F930,0x403645,p,[]),(0x420990,0x41F955,p,[]),(0x56CEC0,0x41F9BE,None,[p+0x24,0,4]),(0x408C00,0x40762C,p+0x50,[]),(0x4077C0,0x4CBE0B,p,[TASK]),(0x407870,0x4CBE69,p,[20,0]),(0x41F5A0,0x407904,TASK+0x844,[20,0]),(0x4142B0,0x4079A5,TASK,[]),(0x4079C0,0x4CBEB0,p,[x,y]),(0x407A50,0x4079FB,p,[0,0]),(0x407AD0,0x407AB0,p,[0,0]),(0x407710,0x4CBED3,p,[]),(0x407780,0x407751,p,[]),(0x403730,0x4077A5,p,[]),(0x4036C0,0x407760,p,[]),(0x403730,0x403701,p,[]),(0x41F9E0,0x403710,p,[]),(0x41FA50,0x41FA21,p,[]),(0x4209C0,0x41FA30,p,[])]

def call_protocol(phase,inputs,before):
 if phase=='graphics':return [(0x4CA600,0x4CA37A,(LAYER&0xFFFF0000)|568,[(LAYER&0xFFFF0000)|256,(LAYER&0xFFFF0000)|568,1,0,66])]+[c for row in source_contract()['frame_table']['rows'] for c in sprite_calls(row)]
 if phase=='rectangle':return [(0x4CD850,0x4CA39C,VM,[LAYER&0xFFFF0000,0xFFFF002D,204]),(0x410310,0x4CA409,MANAGER,RECT),(0x40E2A0,0x410345,MANAGER,RECT[:4])]
 if phase=='owner_read':return [(0x40E2A0,0x410345,MANAGER,RECT[:4])]
 raise ValueError('VM graphics call phase')
