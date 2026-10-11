"""Independent EXE tables and complete first board animation/readiness rules."""
import argparse, hashlib, json, struct
from functools import lru_cache
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from tools.school_script_opening_catalog import (
 ROOT, SOURCE, SOURCE_SHA256, BASE, VM, WORK, TACT, TASK, CONTROL, REGIONS,
 memory_regions, script_layout, presentation_records, trace_bytes, AUTHORITY, report_text)

EVIDENCE=ROOT/'analysis/school-board-opening-v1-20261012.json'
EVIDENCE_SHA256='de8fec0fa15b30f61bd737cdbf9ae59963d53073d181c6430f086d16a958f40e'
NODE_OFFSET=0x6F60+7*0xE0
OBJECT_OFFSET=0x430+7*0xAB8

@lru_cache(maxsize=1)
def source_catalog():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('board source identity')
 expected={
  0x4C5EEC:('mov','dword ptr [ecx + 0x9250], eax'),
  0x4C5F87:('call','0x4cc0f0'),0x4C5F99:('call','0x4cc7d0'),
  0x4CC110:('imul','eax, eax, 0x26'),0x4CC113:('add','eax, 0x624520'),
  0x4CC11E:('movsx','edx, word ptr [ecx]'),0x4CC121:('imul','edx, edx, 0xe0'),
  0x4CC168:('call','0x4caf10'),0x4CC172:('call','0x4caff0'),
  0x4CC390:('mov','ecx, dword ptr [ebp - 0xc]'),
  0x4CC398:('mov','ecx, dword ptr [ebp - 0xc]'),
  0x4CC39B:('mov','word ptr [ecx + 0x22], 1'),
  0x4CC879:('call','0x4ca0b0'),0x4CC886:('call','0x4ca0f0'),
  0x4CC89C:('call','0x4ca130'),0x4CA1CD:('mov','word ptr [ebp - 8], 0x42'),
  0x4CA1D3:('mov','word ptr [ebp - 0xc], 0x43'),
  0x4CA34A:('call','0x4cd850'),0x4CA397:('call','0x4cd850'),
  0x4CA42F:('jle','0x4ca443'),0x4CA43D:('mov','word ptr [eax + 2], 2'),
  0x4CA620:('mov','ecx, dword ptr [eax*4 + 0x624834]'),
  0x4CA6B9:('mov','cx, word ptr [ebp + 0x14]'),0x4CA6F7:('call','0x4cbdb0'),
  0x4CA404:('call','0x410310'),0x4CD54B:('mov','word ptr [ecx + 4], ax'),
  0x4CB287:('cmp','eax, ecx'),0x4CB289:('jge','0x4cb5c5'),
  0x4CD0EC:('jl','0x4cd102'),0x4CD0F2:('jle','0x4cd0f6'),
  0x4CD110:('mov','byte ptr [ebp - 8], 1'),
  0x4CD87E:('imul','eax, ecx'),0x4CD88B:('idiv','ecx'),0x4CD8B7:('jle','0x4cd8c1'),
  0x4D00CC:('call','0x4cd060'),0x4D01B5:('mov','word ptr [eax + edx + 0x20], 0'),
  0x4CEF3D:('call','0x4c4dc0')}
 md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
 for va,pair in expected.items():
  i=next(md.disasm(raw[va-BASE:va-BASE+16],va,count=1))
  if (i.mnemonic,i.op_str)!=pair:raise ValueError(f'board source instruction {va:#x}: {i.mnemonic} {i.op_str}')
  proof.append({'va':hex(va),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
 script,layout=script_layout();op,n=struct.unpack_from('<2H',script,660)
 operands=list(struct.unpack_from('<3I',script,664))
 if (op,n,operands)!=(27,16,[0x20000004,0x2FFFFFFF,0x2FFFFFFF]) or struct.unpack_from('<2HI',script,676)!=(43,8,0x20000004):raise ValueError('board script identity/operands')
 config_at=0x624520+4*38;config=raw[config_at-BASE:config_at-BASE+38]
 words=list(struct.unpack('<19h',config))
 if words[0]!=7 or words[3]!=0 or words[11]!=0:raise ValueError('board unsupported source configuration')
 frame_style=config[36];pieces_at=struct.unpack_from('<I',raw,0x624834-BASE+frame_style*4)[0];pieces=[]
 for index in range(16):
  row=list(struct.unpack_from('<6h',raw,pieces_at-BASE+index*12))
  if row[0]==-1:break
  pieces.append(row)
 else:raise ValueError('board frame sentinel')
 if len(pieces)!=4:raise ValueError('board frame count')
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'code_inputs':proof,'script':layout,
  'board_id':4,'operands':[4,0xFFFFFFF,0xFFFFFFF],'layer':7,'configuration':{'va':hex(config_at),'hex':config.hex(),'words':words},
  'frame_style':frame_style,'frame_pieces':{'va':hex(pieces_at),'rows':pieces},
  'animation_limit':45,'background_limit':8,'frame_resource':66,'rectangle_resource':67,
  'completed_updates':47,'presentation_calls_per_update':54,'pending_handler':'0x4c4dc0',
  'scope':'Original first board/readiness, exact terminal sprite/rectangle parameters; text/font/GPU/task/audio/world/waves remain boundaries.',**AUTHORITY}

def interpolate(count,limit,maximum):
 if any(type(v)!=int or not 0<=v<=65535 for v in (count,limit,maximum)) or limit==0:raise ValueError('board interpolation inputs')
 product=(count*maximum)&0xFFFFFFFF
 signed=product if product<0x80000000 else product-0x100000000
 quotient=(abs(signed)//limit)*(-1 if signed<0 else 1)
 return min(quotient&65535,maximum)

def expected_board(inputs,before):
 rules=source_catalog();script,layout=script_layout()
 if not isinstance(inputs,dict) or set(inputs)!={'script_pointer','overlay_origin','completed_updates','driver','pending_handler'}:raise ValueError('board input shape')
 pointer=inputs['script_pointer'];origin=inputs['overlay_origin']
 if type(pointer)!=int or not 0xE000000<=pointer<=0xF000000-len(script) or type(inputs['completed_updates'])!=int or inputs['completed_updates']!=47 or inputs['driver']!='natural_board_resume_then_declared_original_vm_calls' or inputs['pending_handler']!='0x4c4dc0':raise ValueError('board unsupported driver')
 if not isinstance(origin,list) or len(origin)!=2 or any(type(v)!=int or not 0<=v<=65535 for v in origin):raise ValueError('board overlay types')
 mem=memory_regions(before);vm=mem[VM];task=mem[TACT];control=mem[CONTROL];counter=mem[0x7A4E18];node=NODE_OFFSET;obj=OBJECT_OFFSET
 def get(o,fmt='H'):return struct.unpack_from('<'+fmt,vm,o)[0]
 def put(o,v,fmt='H'):struct.pack_into('<'+fmt,vm,o,v)
 if vm[4:6]!=b'\x01\x01' or vm[0x92E0] or vm[0x92E1] or (get(0x1C,'I'),get(0x20),get(0x22),get(0x24))!=(208,0,27,16):raise ValueError('board actual pending VM state')
 if get(0x10,'I')!=pointer+layout['code_span'][0] or struct.unpack_from('<I',task,0x64)[0]!=pointer or control[12]!=7 or struct.unpack_from('<I',task,0x38)[0]!=5 or task[0x171] or task[0x43]!=1:raise ValueError('board parent binding')
 if origin!=[struct.unpack('<H',mem[TASK+o])[0] for o in (0x196C,0x1970)]:raise ValueError('board overlay binding')
 if any(get(0x6F60+i*0xE0) for i in range(10)) or get(obj+22) or get(0x9248) or any(vm[0x228+i*0x1A] for i in range(20)) or any(vm[0x1CF+i*0x12] for i in range(5)):raise ValueError('board unsupported active/nonempty presentation')
 if any(a<pointer+len(script) and pointer<a+n for a,n in REGIONS):raise ValueError('board script ownership')
 def state():return {'pc':get(0x1C,'I'),'wait':get(0x20),'opcode':get(0x22),
  'layer_active':get(node),'layer_mode':get(node+2),'previous_mode':get(node+4),
  'animation_count':get(node+6),'animation_limit':get(node+16),'background_mode':get(node+34),'text_count':get(obj+22),
  'instruction_count':struct.unpack_from('<I',counter)[0],'waiting_count':struct.unpack_from('<I',counter,4)[0]}
 cfg=rules['configuration']['words']
 def setup():
  for i,v in enumerate(rules['operands']):put(0x9250+i*4,v,'I')
  # Native configuration, empty text object's dimensions, then visibility.
  stores={0:1,2:3,6:0,8:rules['frame_style'],12:cfg[1],14:cfg[2],16:rules['animation_limit'],18:0,20:0,
   22:cfg[14],24:cfg[15],26:cfg[16],28:cfg[17],30:cfg[7],32:cfg[8],34:1,36:0,38:rules['background_limit'],48:cfg[4],64:cfg[0]*2+22,66:cfg[0]*2+23,76:cfg[11]}
  for o,v in stores.items():put(node+o,v)
  put(obj,24);vm[obj+4]=0;put(obj+6,12);vm[obj+10]=0
  put(0x1C,224,'I');put(0x20,1)
 def call(va,receiver,args,ret):return {'va':hex(va),'receiver':receiver,'args':args,'return_va':hex(ret),'return_value':0}
 def drawings(index):
  records=presentation_records(origin);start=1+7*3
  records[start:start+3]=[]
  animated=get(node+2)==3;count=get(node+6)
  alpha=interpolate(count,get(node+16),255) if animated else 255
  color_alpha=interpolate(count,get(node+16),204) if animated else 204
  x,y=get(node+12,'h'),get(node+14,'h');table=int(rules['frame_pieces']['va'],16)
  draws=[call(0x4CBDB0,VM,[x+r[0],y+r[1],(table&0xFFFF0000)|alpha,0xFFFFFFFF,rules['frame_resource'],*r[2:],20,0],0x4CA6FC) for r in rules['frame_pieces']['rows']]
  resource=rules['rectangle_resource'] if animated else 0xFFFF0000|rules['rectangle_resource']
  draws.append(call(0x410310,TASK+0x1058,[x+get(node+22,'h'),y+get(node+24,'h'),get(node+26,'h'),get(node+28,'h'),resource,(color_alpha<<24)|0x223438,1],0x4CA409 if animated else 0x4CA319))
  records[start:start]=draws
  return records
 updates=[];frames=[];all_records=[];readiness=[]
 for index in range(47):
  previous=state()
  if index==0:setup()
  else:
   vm[0x93E2]=0;struct.pack_into('<2I',counter,0,0,(struct.unpack_from('<I',counter,4)[0]+1)&0xFFFFFFFF)
   ready=int(not any(get(0x6F60+i*0xE0) and 3<=get(0x6F62+i*0xE0)<=7 for i in range(10)))
   readiness.append({'update':index,'return_value':ready})
   if ready:put(0x20,0)
  records=drawings(index);all_records+=records
  if get(node+2)==3:
   count=get(node+6)+1;put(node+6,count)
   if count>get(node+16):put(node+6,0);put(node+2,2)
  put(node+4,get(node+2))
  frames.append({'update':index,'calls':len(records),'sha256':hashlib.sha256(trace_bytes(records)).hexdigest()})
  updates.append({'index':index,'before':previous,'after':state(),'vm_return':1})
 vm[0x93E2]=0;put(0x22,43);put(0x24,8);struct.pack_into('<2I',counter,0,1,0)
 return {'after':[{'pointer':a,'bytes':n,'hex':mem[a].hex()} for a,n in REGIONS],'updates':updates,'readiness':readiness,
  'presentation_frames':frames,'presentation_calls':len(all_records),'presentation_sha256':hashlib.sha256(trace_bytes(all_records)).hexdigest(),
  'presentation_first_update':all_records[:54],
  'pending_call':{'va':'0x4c4dc0','receiver':VM,'args':[0,pointer+676,0],'return_va':'0x4cef42','root_return_va':'0x3000000','natural_stack_verified':True,'first_instruction_executed':False}}

@lru_cache(maxsize=1)
def native_fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('board evidence identity')
 return json.loads(raw)

def export():
 rules=source_catalog();data=native_fixture()
 evidence={'schema_version':1,'native_report':EVIDENCE.relative_to(ROOT).as_posix(),'native_report_sha256':EVIDENCE_SHA256,
  'cases':data['cases'],'inherited_refusals':data['inherited_refusals'],'runtime_fixture':False}
 for name,value in (('rules',rules),('evidence',evidence)):
  (ROOT/f'prototype/data/school_board_opening_{name}.json').write_text(report_text(value),encoding='utf-8',newline='\n')

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--export',action='store_true');a=p.parse_args()
 if a.export:export()
