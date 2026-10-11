"""Independent source rules for selected school VM startup and fade waits."""
import argparse,hashlib,json,struct
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.school_script_preflight_catalog import ROOT,SOURCE,SOURCE_SHA256,BASE,TASK,TACT,UNITCTRL,VM,WORK,CONTROL,script_layout,AUTHORITY,report_text

EVIDENCE=ROOT/'analysis/school-script-opening-v1-20261012.json'
EVIDENCE_SHA256='b76eaae2a083ea1f71ea525778aac9e6e0ea978941e149705c6057773362521f'
REGIONS=((TACT,400),(CONTROL,18),(WORK,0x24A0),(VM,0x9400),(0x809348,0xA0),(0x7A4E18,8),(TASK+0x196C,2),(TASK+0x1970,2))
RANGES=((0x4CE8F0,0x4D03B7),(0x42D460,0x42D512),(0x42D960,0x42D9E4),(0x42E9E0,0x42EBB4),
 (0x42F910,0x42F9FC),(0x42FAF0,0x42FBDC),(0x42FC60,0x42FCCA),(0x496DC0,0x496DE7),
 (0x497210,0x497349),(0x4977A0,0x497980),(0x497AA0,0x497C43),(0x499560,0x499752),
 (0x4C1E20,0x4C1FAD),(0x4C2060,0x4C2106),(0x4C23F0,0x4C24F3),(0x4C2670,0x4C2723),
 (0x4C3F40,0x4C3FF9),(0x4C5430,0x4C5586),(0x4C76B0,0x4C7756),(0x4C7AB0,0x4C7B17),
 (0x4CCB90,0x4CCE1C),(0x4E29E0,0x4E2C1F),(0x56CFCC,0x56CFF3))

@lru_cache(maxsize=1)
def source_catalog():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('normal opening source identity')
 expected={0x4C20A4:('sete','cl'),0x4C24CC:('mov','edx, dword ptr [edx + 0x10]'),
  0x4C3FD4:('call','0x4c1f40'),0x42FB98:('mov','dword ptr [ecx + 0x9258], eax'),
  0x42FBB2:('push','3'),0x42F9D2:('push','1'),0x4E2A74:('mov','dword ptr [ebp - 4], 0x809348'),
  0x4E2B04:('mov','word ptr [edx + ecx*2 + 0x28], ax'),
  0x4E2BBC:('mov','dword ptr [edx + ecx*4 + 0x78], eax'),
  0x497290:('mov','byte ptr [eax + edx*4 + 0x19], cl'),0x497331:('mov','word ptr [eax + edx*4 + 0x1a], cx'),
  0x499637:('call','0x4972b0'),0x49973A:('call','0x4977a0'),0x4977B8:('mov','byte ptr [0x7e0f08], 0'),
  0x49790B:('mov','dword ptr [ecx + 0x2490], 0'),0x497937:('mov','dword ptr [ecx + 0x249c], edx'),
  0x497942:('mov','byte ptr [eax + 0x2499], 1'),0x497955:('fdivr','dword ptr [0x59e8bc]'),
  0x49795E:('call','0x56cfcc'),0x497969:('mov','dword ptr [edx + 0x2494], eax'),
  0x497B41:('add','edx, dword ptr [eax + 0x2494]'),0x497B59:('cmp','dword ptr [edx + 0x2490], 0x9800'),
  0x497BB7:('mov','dword ptr [edx + 0x249c], ecx'),0x497BC9:('jne','0x497c1d'),
  0x497BD1:('mov','byte ptr [ecx + 0x2499], 0'),0x497C0A:('mov','byte ptr [edx + 0x249a], 2'),
  0x497C11:('call','0x4977a0'),0x4C76D4:('mov','word ptr [eax + 2], cx'),
  0x4C76EC:('mov','word ptr [ecx + 6], 0x10'),0x4C771A:('mov','word ptr [eax], 0'),
  0x4C7AD9:('mov','al, 1'),0x4C555E:('mov','byte ptr [edx + 0x9228], cl'),
  0x4C26FC:('call','0x4c1e20'),0x4C1E40:('mov','byte ptr [eax + 0x1cd], 1'),
  0x4C1E57:('mov','word ptr [edx + ecx + 0x26], ax'),0x4C1E6C:('mov','word ptr [edx + ecx + 0x28], ax'),
  0x4C1E81:('mov','word ptr [edx + ecx + 0x2a], ax'),0x4C1E95:('mov','dword ptr [edx + ecx + 0x2c], eax'),
  0x4CCC08:('sub','esi, 1'),0x4CCC2C:('mov','word ptr [edi + ecx + 0x28], ax'),
  0x4CCC33:('jle','0x4ccc39'),0x4CCDFF:('mov','byte ptr [ecx + 0x1cd], 0'),
  0x4CFF41:('mov','word ptr [edx + ecx + 0x20], 0'),0x4CFF53:('mov','dword ptr [0x7a4e18], 0'),
  0x4CFF66:('mov','dword ptr [0x7a4e1c], ecx'),0x4D0133:('call','0x4c7ab0'),
  0x4D01B5:('mov','word ptr [eax + edx + 0x20], 0'),0x4CED43:('call','0x4c5ea0'),
  0x4D0228:('mov','dx, word ptr [ecx + 0x1970]'),0x4D0235:('mov','cx, word ptr [eax + 0x196c]')}
 md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
 for va,pair in expected.items():
  i=next(md.disasm(raw[va-BASE:va-BASE+16],va,count=1))
  if (i.mnemonic,i.op_str)!=pair:raise ValueError(f'normal opening source instruction {va:#x}: {i.mnemonic} {i.op_str}')
  proof.append({'va':hex(va),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
 selector=raw[0x4997A8-BASE+20];group_target=struct.unpack_from('<I',raw,0x499750-BASE+selector*4)[0]
 if group_target!=0x49962E:raise ValueError('normal opening group20 dispatch')
 fade_limit=struct.unpack_from('<f',raw,0x59E8BC-BASE)[0]
 if fade_limit!=38912.0:raise ValueError('normal opening fade source constant')
 _,layout=script_layout()
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'code_inputs':proof,'script':layout,
  'native_ranges':[[hex(a),hex(b)] for a,b in RANGES],
  'native_code_sha256':hashlib.sha256(b''.join(raw[a-BASE:b-BASE] for a,b in RANGES)).hexdigest(),
  'group20_target':hex(group_target),'fade_limit':int(fade_limit),'fade_counts':60,'delay_counts':30,
  'completed_updates':107,'presentation_calls_per_update':52,'pending_handler':'0x4c5ea0',
  'scope':'Declared normal VM/fade; full task/audio/world/dialogue/waves/rendering remain boundaries.',**AUTHORITY}

def memory_regions(regions):
 if not isinstance(regions,list) or len(regions)!=len(REGIONS):raise ValueError('normal opening region count')
 memory={}
 for item,(at,n) in zip(regions,REGIONS):
  if not isinstance(item,dict) or set(item)!={'pointer','bytes','hex'} or type(item['pointer'])!=int or type(item['bytes'])!=int or (item['pointer'],item['bytes'])!=(at,n):raise ValueError('normal opening region ownership')
  if not isinstance(item['hex'],str):raise ValueError('normal opening region encoding')
  try:value=bytes.fromhex(item['hex'])
  except ValueError as error:raise ValueError('normal opening region encoding') from error
  if len(value)!=n:raise ValueError('normal opening region size')
  memory[at]=bytearray(value)
 return memory

def presentation_records(origin):
 def call(va,receiver,args,ret):return {'va':hex(va),'receiver':receiver,'args':args,'return_va':hex(ret),'return_value':0}
 x,y=origin;records=[call(0x4D29E0,VM+0x94E8,[20,0,1,51,(TASK&0xFFFF0000)|x,(VM&0xFFFF0000)|y,424,24,20,30,100,100,255,128,128,128],0x4D024F)]
 for i in range(10):
  node=VM+0x6F60+i*0xE0;obj=VM+0x430+i*0xAB8
  records.extend((call(0x4CA1B0,node,[],0x4D028E),call(0x4C99E0,node,[],0x4D02AB),call(0x4CD4D0,VM,[node,obj],0x4D02E7)))
 records.append(call(0x4C7770,VM+0x9248,[],0x4D0354))
 records.extend(call(0x4CBA60,VM+0x228+i*0x1A,[],0x4D0391) for i in range(20))
 return records

def trace_bytes(records):return b''.join((json.dumps(r,sort_keys=True,separators=(',',':'))+'\n').encode() for r in records)

def expected_opening(inputs,before):
 rules=source_catalog();script,layout=script_layout()
 if not isinstance(inputs,dict) or set(inputs)!={'script_pointer','overlay_origin','completed_updates','driver','pending_handler'}:raise ValueError('normal opening input shape')
 if type(inputs['script_pointer'])!=int or type(inputs['completed_updates'])!=int or not isinstance(inputs['overlay_origin'],list) or len(inputs['overlay_origin'])!=2 or any(type(v)!=int or not 0<=v<=65535 for v in inputs['overlay_origin']):raise ValueError('normal opening input types')
 pointer=inputs['script_pointer']
 if not 0xE000000<=pointer<=0xF000000-len(script) or inputs!={'script_pointer':pointer,'overlay_origin':inputs['overlay_origin'],'completed_updates':107,'driver':'declared_original_vm_then_fade_calls','pending_handler':'0x4c5ea0'}:raise ValueError('normal opening unsupported driver')
 mem=memory_regions(before);vm=mem[VM];work=mem[WORK];task=mem[TACT];control=mem[CONTROL];global_flags=mem[0x809348];counter=mem[0x7A4E18]
 def get(offset,fmt='I'):return struct.unpack_from('<'+fmt,vm,offset)[0]
 def put(offset,value,fmt='I'):struct.pack_into('<'+fmt,vm,offset,value)
 def wg(offset,fmt='i'):return struct.unpack_from('<'+fmt,work,offset)[0]
 def wp(offset,value,fmt='i'):struct.pack_into('<'+fmt,work,offset,value)
 if vm[4:6]!=b'\x01\x01' or get(0x1C) or get(0x20,'H') or vm[0x92E0] or vm[0x92E1] or wg(0x2499,'B'):raise ValueError('normal opening selected VM/fade state')
 if struct.unpack_from('<I',task,0x64)[0]!=pointer or get(0x10)!=pointer+layout['code_span'][0] or work[:3]!=b'\x01\x01\x01':raise ValueError('normal opening script/work binding')
 if control[12]!=7 or struct.unpack_from('<I',task,0x38)[0]!=5 or task[0x43]!=1 or task[0x171]:raise ValueError('normal opening parent task')
 if inputs['overlay_origin']!=[struct.unpack('<H',mem[TASK+o])[0] for o in (0x196C,0x1970)]:raise ValueError('normal overlay origin binding')
 if any(get(0x6F60+i*0xE0,'H') for i in range(10)) or any(vm[0x228+i*0x1A] for i in range(20)) or get(0x9248,'H') or any(vm[0x1CF+i*0x12] for i in range(5)):raise ValueError('normal opening active presentation refused')
 if any(a<pointer+len(script) and pointer<a+n for a,n in REGIONS):raise ValueError('normal opening script ownership')
 def operand(raw):
  kind,index=raw>>28,raw&0xFFFFFFF
  if kind==0 and index<50:return get(0x3C+index*4)
  if kind==2:return index
  raise ValueError('normal opening unsupported operand')
 def temps(values):
  for i,value in enumerate(values):put(0x9250+i*4,value)
 def state():return {'pc':get(0x1C),'wait':get(0x20,'H'),'wait_opcode':get(0x26,'H'),'wait_count':get(0x28,'H'),
  'wait_limit':get(0x2A,'H'),'work_wait':vm[0x92E0],'variable0':get(0x3C),'fade_value':wg(0x2490),
  'fade_delta':wg(0x2494),'fade_active':wg(0x2499,'B'),'fade_status':wg(0x249A,'B'),'fade_remaining':wg(0x249C)}
 commands=[];updates=[]
 def vm_update(index,pending=False):
  vm[0x93E2]=0;wait=get(0x20,'H')
  if wait==4:
   if not vm[0x92E0]:put(0x20,0,'H')
   return
  if wait==1:
   struct.pack_into('<2I',counter,0,0,(struct.unpack_from('<I',counter,4)[0]+1)&0xFFFFFFFF)
   if get(0x22,'H')==56:
    if get(0x9248,'H'):raise ValueError('normal opening active presentation wait')
    put(0x20,0,'H')
   elif get(0x22,'H')==12:
    old,limit=get(0x28,'H'),get(0x2A,'H');put(0x28,(old+1)&65535,'H')
    if old>limit-1:put(0x20,0,'H');vm[0x1CD]=0
   else:raise ValueError('normal opening unsupported wait')
   return
  if wait:raise ValueError('normal opening unsupported wait state')
  at=layout['code_span'][0]+get(0x1C)
  if not 452<=at<=660:raise ValueError('normal opening script bounds')
  op,n=struct.unpack_from('<2H',script,at)
  commands.append({'update':index,'offset':at,'opcode':op,'advance':n});put(0x22,op,'H');put(0x24,n,'H')
  struct.pack_into('<2I',counter,0,(struct.unpack_from('<I',counter)[0]+1)&0xFFFFFFFF,0)
  if pending:
   if (op,at)!=(27,660):raise ValueError('normal opening pending handler mismatch')
   return
  cells=list(struct.unpack_from('<'+'I'*((n-4)//4),script,at+4));result=0
  if op==167:put(0x3C+cells[0]*4,work[0])
  elif op==8:
   operator,left,right,target=cells
   if operator!=1:raise ValueError('normal opening comparison')
   a,b=operand(left),operand(right);value=int(a==b);temps([a,b,value])
   if value:put(0x1C,target);put(0x24,0,'H')
  elif op==5:
   dest,value=cells;value=operand(value);temps([value])
   if dest>>28 or dest>=50:raise ValueError('normal opening variable target')
   put(0x3C+dest*4,value)
  elif op in (165,163):
   values=list(map(operand,cells));temps(values)
   if values!=[0,65535,0]:raise ValueError('normal opening global setter')
   if op==165:struct.pack_into('<I',global_flags,0x78,struct.unpack_from('<I',global_flags,0x78)[0]&0x7FFFFFFF)
   else:struct.pack_into('<H',global_flags,0x28,0)
  elif op==113:
   group,value=map(operand,cells);temps([group,value])
   if group not in (1,2) or value:raise ValueError('normal opening group setter')
   wp(0x19+group*4,value,'B')
  elif op==136:
   values=list(map(operand,cells));temps(values)
   if values[0]!=20 or values[1] not in (1,2) or values[2:]!=[1,0,0,0,0]:raise ValueError('normal opening group20')
   wp(0x1A+values[1]*4,values[2],'H');vm[0x92E0]=0;result=4
  elif op==117:
   count=operand(cells[0]);temps([count])
   if count!=60:raise ValueError('normal opening fade count')
   wp(0x2490,0);wp(0x2494,int(rules['fade_limit']/count));wp(0x2498,1,'B');wp(0x2499,1,'B');wp(0x249A,1,'B');wp(0x249C,count);vm[0x92E0]=1;result=4
  elif op==56:
   mode=operand(cells[0]);temps([mode])
   if mode!=2:raise ValueError('normal opening presentation mode')
   struct.pack_into('<4H',vm,0x9248,0,mode,0,16);result=1
  elif op==20:vm[0x9228]=operand(cells[0])&255;temps([vm[0x9228]])
  elif op==12:
   count=operand(cells[0]);temps([count]);vm[0x1CD]=1;struct.pack_into('<3HI',vm,0x26,12,0,count,0);result=1
  else:raise ValueError('normal opening unsupported command')
  put(0x1C,get(0x1C)+get(0x24,'H'));put(0x20,result,'H')
 def fade_update():
  if not wg(0x2499,'B'):return 1
  if wg(0x2498,'B')!=1:raise ValueError('normal opening unsupported fade direction')
  wp(0x2490,min(wg(0x2490)+wg(0x2494),rules['fade_limit']));wp(0x249C,wg(0x249C)-1)
  if not wg(0x249C):wp(0x2499,0,'B');wp(0x249A,2,'B');vm[0x92E0]=0;return 1
  wp(0x249A,1,'B');return 0
 for index in range(107):
  previous=state();vm_update(index);fade=fade_update();updates.append({'index':index,'before':previous,'after':state(),'vm_return':1,'fade_return':fade})
 vm_update(107,True);records=presentation_records(inputs['overlay_origin']);digest=hashlib.sha256(trace_bytes(records)).hexdigest()
 return {'after':[{'pointer':a,'bytes':n,'hex':mem[a].hex()} for a,n in REGIONS],'updates':updates,'commands':commands,
  'presentation_frames':[{'update':i,'calls':52,'sha256':digest} for i in range(107)],
  'presentation_calls':5564,'presentation_sha256':hashlib.sha256(trace_bytes(records)*107).hexdigest(),'presentation_first_update':records,
  'pending_call':{'va':'0x4c5ea0','receiver':VM,'args':[0,pointer+660,1],'return_va':'0x4ced48','root_return_va':'0x3000000','natural_stack_verified':True,'first_instruction_executed':False}}

@lru_cache(maxsize=1)
def native_fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('normal opening evidence identity')
 return json.loads(raw)

def export():
 rules=source_catalog();data=native_fixture()
 evidence={'schema_version':1,'native_report':EVIDENCE.relative_to(ROOT).as_posix(),'native_report_sha256':EVIDENCE_SHA256,
  'cases':data['cases'],'inherited_refusals':data['inherited_refusals'],'runtime_fixture':False}
 for name,value in (('rules',rules),('evidence',evidence)):
  (ROOT/f'prototype/data/school_script_opening_{name}.json').write_text(report_text(value),encoding='utf-8',newline='\n')

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--export',action='store_true');a=p.parse_args()
 if a.export:export()
