"""Independent EXE/script rules for preflight execution and selected binding."""
import argparse,hashlib,json,struct
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.tactics_exit_emulation import SOURCE,SOURCE_SHA256,BASE,TASK
from tools.school_tactical_startup_emulation import TACT
from tools.school_deployment_tail_emulation import ROOT,UNITCTRL,AUTHORITY,report_text

VM=0x7D7C28;WORK=0xE200000;CONTROL=UNITCTRL+0x108B3E
SCRIPT=ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/SCRIPT/T0005.BIN'
SCRIPT_SHA='44ca546b5ea90ec23a4bc7d8dffeac6547a44bfd035383c91983f7c13ae72a52'
EVIDENCE=ROOT/'analysis/school-script-preflight-v1-20261011.json'
EVIDENCE_SHA256='b3de8be5e282c4d2e00c2acca5722f7536746aa62c8aff1d6f58d32988ce7c42'
REGIONS=((TACT,400),(CONTROL,18),(WORK,3),(VM,0x9400),(0x7A4E18,8))+tuple((VM+0x446+i*0xAB8,2) for i in range(14,56))
RANGES=((0x4551C0,0x455301),(0x455060,0x455160),(0x4214F0,0x421538),
 (0x497720,0x497794),(0x496D80,0x496E65),(0x4CE460,0x4CE6E0),
 (0x4CE090,0x4CE144),(0x4CD8D0,0x4CDBE0),(0x4CD700,0x4CD75B),
 (0x4CE030,0x4CE08E),(0x4CE8F0,0x4D03B7),(0x42FBE0,0x42FCCA),
 (0x4C1EB0,0x4C1FC0),(0x4C2060,0x4C2120),(0x4C23F0,0x4C2500),(0x4C2610,0x4C2670),
 (0x4CE800,0x4CE86A),(0x4D0790,0x4D0854),(0x4549D0,0x454AB0),
 (0x49A0D4,0x49A114),(0x49A146,0x49A159))

def package_offsets(raw,start=0):
 """Validate the two-dword sized package header used by 455060/4214F0."""
 if not isinstance(raw,bytes) or type(start)!=int or start<0 or start+8>len(raw):raise ValueError('script package bounds')
 size,count=struct.unpack_from('<2I',raw,start)
 if not count or size<8+count*4 or start+size>len(raw):raise ValueError('script package size/count')
 offsets=list(struct.unpack_from(f'<{count}I',raw,start+8))
 if offsets!=sorted(offsets) or offsets[0]<8+count*4 or offsets[-1]>size:raise ValueError('script package offsets')
 return size,offsets

def vm_offsets(raw,start,end):
 if not isinstance(raw,bytes) or type(start)!=int or type(end)!=int or not 0<=start<end<=len(raw) or start+4>end:raise ValueError('script VM bounds')
 count=struct.unpack_from('<I',raw,start)[0]
 if not count or start+4+count*4>end:raise ValueError('script VM header')
 offsets=list(struct.unpack_from(f'<{count}I',raw,start+4))
 if offsets!=sorted(offsets) or offsets[0]<4+count*4 or offsets[-1]>end-start:raise ValueError('script VM offsets')
 return offsets

@lru_cache(maxsize=1)
def script_layout():
 raw=SCRIPT.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SCRIPT_SHA:raise ValueError('preflight script identity')
 size,groups=package_offsets(raw);group=groups[0];group_size,subs=package_offsets(raw,group)
 start,end=group+subs[1],group+subs[2];offsets=vm_offsets(raw,start,end)
 if size!=len(raw) or group+group_size!=groups[1]:raise ValueError('preflight group span')
 return raw,{'source_script_sha256':SCRIPT_SHA,'file_size':size,'groups':groups,'group_size':group_size,
  'sub_count':len(subs),'selected_sub':1,'selected_span':[start,end],'vm_offsets':offsets,
  'code_span':[start+offsets[0],start+offsets[1]]}

@lru_cache(maxsize=1)
def source_catalog():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('preflight EXE identity')
 expected={0x4551DD:('call','0x497720'),0x455216:('call','dword ptr [0x592278]'),
  0x455276:('call','0x4ce460'),0x455280:('call','0x4ce030'),0x455287:('call','dword ptr [0x592210]'),
  0x4552A5:('call','0x4ce8f0'),0x4552B9:('call','0x4d0790'),0x4552C3:('call','0x4ce060'),
  0x4552C8:('call','0x496e30'),0x4552DB:('mov','eax, 1'),
  0x49777F:('mov','byte ptr [ecx + 2], 1'),0x496DAD:('mov','byte ptr [ecx], dl'),
  0x496E1D:('mov','byte ptr [ecx + 1], dl'),0x4CE0C5:('cmp','byte ptr [ebp - 0xc], 2'),
  0x4CE120:('mov','byte ptr [edx + ecx + 4], 0'),0x4CE12A:('call','0x4cd8d0'),
  0x4CD931:('mov','byte ptr [ecx + eax + 5], 0'),0x4CD957:('jge','0x4cd9a3'),
  0x4CD968:('mov','byte ptr [edx + ecx + 0x1cf], 0'),
  0x4CD97E:('mov','word ptr [ecx + eax + 0x1dc], 0xffff'),0x4CD997:('mov','word ptr [eax + edx + 0x1de], 0xffff'),
  0x4CD9DA:('mov','word ptr [ecx + eax + 0x6f60], 0'),0x4CD9F6:('mov','word ptr [eax + edx + 0x6f94], 0xffff'),
  0x4CDA12:('mov','word ptr [edx + ecx + 0x6f96], 0xffff'),0x4CDA2D:('mov','word ptr [ecx + eax + 0x6f62], 0'),
  0x4CDA49:('mov','word ptr [eax + edx + 0x6f82], 0'),0x4CDA85:('mov','byte ptr [ecx + eax + 0x92a0], 0'),
  0x4CDAB9:('imul','ecx, ecx, 0xab8'),0x4CDAC2:('mov','word ptr [edx + ecx + 0x446], 0'),
  0x4CDB75:('mov','byte ptr [edx + ecx + 0x228], 0'),0x4CDB82:('mov','word ptr [eax + 0x9248], 0'),
  0x4CE503:('mov','dword ptr [eax + edx + 8], ecx'),0x4CE51C:('mov','dword ptr [eax + edx + 0xc], ecx'),
  0x4CE532:('mov','byte ptr [eax + edx + 5], 1'),0x4CE580:('mov','byte ptr [eax + 0x1cc], 0xff'),
  0x4CE58A:('mov','byte ptr [ecx + 0x9228], 1'),0x4CE648:('mov','byte ptr [eax + edx + 4], 1'),
  0x4CE65F:('mov','dword ptr [edx + ecx + 0x1c], 0'),0x4CE678:('mov','word ptr [ecx + eax + 0x20], 0'),
  0x4CE6AF:('mov','dword ptr [edx + eax*4 + 0x38], 0'),0x4CE6C5:('mov','dword ptr [ecx + 0x92dc], edx'),
  0x4CE91A:('mov','byte ptr [0x7e100a], 0'),0x4CEA19:('cmp','eax, 0x13'),
  0x4CEA2D:('call','0x4ce090'),0x4CEA32:('call','0x4ce800'),0x4CEA45:('mov','dword ptr [0x7a4e18], edx'),
  0x4CEA4B:('mov','dword ptr [0x7a4e1c], 0'),0x4C20A4:('sete','cl'),
  0x4C24A8:('je','0x4c24d3'),0x4C24CC:('mov','edx, dword ptr [edx + 0x10]'),
  0x4C263F:('mov','word ptr [edx + ecx + 0x24], 0'),0x4C2658:('mov','dword ptr [ecx + eax + 0x1c], edx'),
  0x4CFED2:('mov','si, word ptr [ecx + eax + 0x24]'),0x4CFEF2:('mov','dword ptr [eax + edx + 0x1c], ecx'),
  0x42FC83:('call','0x496dc0'),0x42FCAF:('call','0x4c1f40'),0x42FC3C:('call','0x496df0'),
  0x49A0EF:('call','0x4549d0'),0x454A3C:('mov','byte ptr [ecx + 0x43], 1'),
  0x454A63:('call','0x56cec0'),0x454A71:('mov','dword ptr [eax + 0x48], ecx'),
  0x454A7A:('mov','dword ptr [edx + 0x4c], eax'),0x454A83:('mov','dword ptr [ecx + 0x50], edx'),
  0x454A89:('mov','byte ptr [eax + 0x59], 1'),0x454A90:('mov','byte ptr [ecx + 0x58], 0'),
  0x454A9A:('mov','dword ptr [edx + 0x54], eax')}
 md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
 for va,pair in expected.items():
  i=next(md.disasm(raw[va-BASE:va-BASE+16],va,count=1))
  if (i.mnemonic,i.op_str)!=pair:raise ValueError(f'preflight source instruction {va:#x}: {i.mnemonic} {i.op_str}')
  proof.append({'va':hex(va),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
 dispatch={str(op):hex(struct.unpack_from('<I',raw,0x4D03CF-BASE+(op-5)*4)[0]) for op in (8,11,166,167)}
 if dispatch!={'8':'0x4ceaf6','11':'0x4ceb35','166':'0x4cfe03','167':'0x4cfe22'}:raise ValueError('preflight opcode dispatch')
 if struct.unpack_from('<I',raw,0x4C2106-BASE)[0]!=0x4C209C:raise ValueError('preflight equality operator')
 _,layout=script_layout()
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'code_inputs':proof,'script':layout,
  'native_ranges':[[hex(a),hex(b)] for a,b in RANGES],
  'native_code_sha256':hashlib.sha256(b''.join(raw[a-BASE:b-BASE] for a,b in RANGES)).hexdigest(),
  'opcode_dispatch':dispatch,'comparison_operator1':'equal','outside_vm_reset_words':42,
  'selected_binding_args':[0,0,1,0,1,1,0],
  'scope':'Natural preflight VM and selected binding; normal playback/world scheduling/rendering/audio pending.',**AUTHORITY}

def memory_regions(regions):
 if not isinstance(regions,list) or len(regions)!=len(REGIONS):raise ValueError('preflight region count')
 memory={}
 for item,(at,n) in zip(regions,REGIONS):
  if not isinstance(item,dict) or set(item)!={'pointer','bytes','hex'} or type(item['pointer'])!=int or type(item['bytes'])!=int or (item['pointer'],item['bytes'])!=(at,n):raise ValueError('preflight region ownership')
  if not isinstance(item['hex'],str):raise ValueError('preflight region encoding')
  try:value=bytes.fromhex(item['hex'])
  except ValueError as error:raise ValueError('preflight region encoding') from error
  if len(value)!=n:raise ValueError('preflight region size')
  memory[at]=bytearray(value)
 return memory

def expected_preflight(inputs,before):
 source_catalog();script,layout=script_layout()
 fields={'script_pointer','script_sha256','selector','sub','strcmp_import','tick_import','main_owner','tick_value','driver'}
 if not isinstance(inputs,dict) or set(inputs)!=fields:raise ValueError('preflight input shape')
 for field in fields-{'script_sha256','driver'}:
  if type(inputs[field])!=int:raise ValueError('preflight input types')
 pointer=inputs['script_pointer']
 if not 0xE000000<=pointer<=0xF000000-len(script) or inputs!={'script_pointer':pointer,'script_sha256':SCRIPT_SHA,
  'selector':0,'sub':1,'strcmp_import':0x7000000,'tick_import':0x7000010,'main_owner':0x1080000,
  'tick_value':0,'driver':'natural_pending_preflight_and_caller_return'}:raise ValueError('preflight unsupported inputs')
 memory=memory_regions(before);task=memory[TACT];control=memory[CONTROL];vm=memory[VM];work=memory[WORK];counter=memory[0x7A4E18]
 if struct.unpack_from('<I',task,0x64)[0]!=pointer:raise ValueError('preflight script binding')
 if struct.unpack_from('<I',task,0x38)[0]!=5 or task[0x43] or task[0x170] or task[0x171]:raise ValueError('preflight task state')
 if control[12]!=6 or struct.unpack_from('<h',control,14)[0] or vm[4] or vm[5] not in (0,1):raise ValueError('preflight controller/owned VM state')
 if any(at<pointer+len(script) and pointer<at+n for at,n in REGIONS):raise ValueError('preflight script ownership overlap')
 def put(offset,value,fmt='I'):struct.pack_into('<'+fmt,vm,offset,value)
 def capture():return [{'pointer':at,'bytes':n,'hex':memory[at].hex()} for at,n in REGIONS]
 def reset():
  vm[4]=vm[5]=0
  for i in range(5):
   put(0x1CF+i*0x12,0,'B');put(0x1DC+i*0x12,0xFFFF,'H');put(0x1DE+i*0x12,0xFFFF,'H')
  for i in range(10):
   for offset,value in ((0x6F60,0),(0x6F94,0xFFFF),(0x6F96,0xFFFF),(0x6F62,0),(0x6F82,0)):put(offset+i*0xE0,value,'H')
  vm[0x92A0:0x92D8]=bytes(56)
  for i in range(56):
   offset=0x446+i*0xAB8
   if offset+2<=len(vm):put(offset,0,'H')
   else:memory[VM+offset][:]=bytes(2)
  for i in range(20):put(0x228+i*0x1A,0,'B')
  put(0x9248,0,'H')
 start,end=layout['selected_span'];offsets=layout['vm_offsets'];code_start,code_end=layout['code_span']
 def bind():
  reset();put(8,end-start);put(0xC,pointer+start);vm[5]=1
  vm[0x1CC]=255;vm[0x9228]=1
  for at,index in ((0x10,0),(0x14,1),(0x18,2)):put(at,pointer+start+offsets[index])
  vm[4]=1;put(0x1C,0);put(0x20,0,'H');vm[0x3C:0x104]=bytes(200);put(0x92DC,0xFFFFFFFF)
 def operand(value):
  kind,index=value>>28,value&0xFFFFFFF
  if kind==0 and index<50:return struct.unpack_from('<I',vm,0x3C+index*4)[0]
  if kind==2:return index
  raise ValueError('preflight unsupported script operand')
 work[:]=bytes((0,0,1));bind();vm[0x92E1]=1;commands=[];pc=0
 for _ in range(5):
  at=code_start+pc
  if not code_start<=at<=code_end-4:raise ValueError('preflight command bounds')
  op,advance=struct.unpack_from('<2H',script,at)
  if advance<4 or at+advance>code_end:raise ValueError('preflight command size')
  commands.append({'offset':at,'opcode':op,'advance':advance});vm[0x93E2]=0;put(0x22,op,'H');put(0x24,advance,'H')
  if op==19:
   reset();break
  struct.pack_into('<2I',counter,0,(struct.unpack_from('<I',counter)[0]+1)&0xFFFFFFFF,0)
  if op==167 and advance==8:
   target=struct.unpack_from('<I',script,at+4)[0]
   if target>>28 or (target&0xFFFFFFF)>=50:raise ValueError('preflight variable target')
   put(0x3C+target*4,work[0])
  elif op==8 and advance==20:
   operator,left,right,target=struct.unpack_from('<4I',script,at+4)
   if operator!=1:raise ValueError('preflight unsupported comparison')
   a,b=operand(left),operand(right);result=int(a==b)
   put(0x9250,a);put(0x9254,b);put(0x9258,result)
   if result:pc=target;put(0x24,0,'H')
  elif op==166 and advance==8:
   value=operand(struct.unpack_from('<I',script,at+4)[0]);put(0x9250,value);work[1]=int(value!=0)
  elif op==11 and advance==8:pc=struct.unpack_from('<I',script,at+4)[0];put(0x24,0,'H')
  else:raise ValueError('preflight unsupported command')
  pc+=struct.unpack_from('<H',vm,0x24)[0];put(0x1C,pc);put(0x20,0,'H')
 else:raise ValueError('preflight command budget')
 vm[0x92E1]=0;result=int(work[1]!=0);work[0]=result
 if result!=1:raise ValueError('preflight unsupported selected branch')
 intermediate=capture();bind();task[0x43]=1;task[0x44:0x60]=bytes(28)
 struct.pack_into('<3I',task,0x48,1,0,1);task[0x59]=1;control[12]=7
 native=SOURCE.read_bytes();marker=native[0x59A60C-BASE:].split(b'\0',1)[0];left=script[start:].split(b'\0',1)[0]
 difference=next((a-b for a,b in zip(left+b'\0',marker+b'\0') if a!=b),0)&0xFFFFFFFF
 def primitive(va,receiver,args,ret,value):return {'va':hex(va),'receiver':receiver,'args':args,'return_va':hex(ret),'return_value':value}
 primitives=[primitive(inputs['strcmp_import'],pointer+start,[pointer+start,0x59A60C],0x45521C,difference),
  primitive(inputs['tick_import'],VM,[],0x45528D,0),primitive(0x42B2D0,0,[0x5C2FF0],0x4CE822,0),
  primitive(0x41E500,TASK+0x8F00,[],0x4CE84C,0),primitive(0x42B2D0,TASK+0x8F00,[0x5C2FD8],0x4CE856,0),
  primitive(0x40D120,TASK+0x1A98,[2],0x4D083F,0),primitive(0x56CEC0,TACT,[TACT+0x44,0,28],0x454A68,TACT+0x44)]
 return {'preflight_after':intermediate,'after':capture(),'commands':commands,'primitives':primitives,
  'binding_calls':[{'va':'0x4549d0','receiver':TACT,'args':[0,0,1,0,1,1,0],'return_va':'0x49a0f4'}],
  'preflight_return':result,'controller_return':0,'natural_returns':['0x49a0d4','0x3000000'],
  'natural_stack_verified':True,'selected_vm_bound':True,'preflight_vm_executed':True,
  'playback_vm_executed':False,'world_update_loop_executed':False,'live_rendering':False,'live_audio':False}

@lru_cache(maxsize=1)
def native_fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('preflight evidence identity')
 return json.loads(raw)

def export():
 rules=source_catalog();data=native_fixture()
 evidence={'schema_version':1,'native_report':EVIDENCE.relative_to(ROOT).as_posix(),'native_report_sha256':EVIDENCE_SHA256,
  'cases':data['cases'],'inherited_refusals':data['inherited_refusals'],'runtime_fixture':False}
 for name,value in (('rules',rules),('evidence',evidence)):
  (ROOT/f'prototype/data/school_script_preflight_{name}.json').write_text(report_text(value),encoding='utf-8',newline='\n')

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--export',action='store_true');a=p.parse_args()
 if a.export:export()
