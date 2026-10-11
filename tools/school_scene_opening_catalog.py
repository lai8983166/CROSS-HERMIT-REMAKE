"""Independent EXE-derived initialization, signed timer and opening rules.

Input memory is captured before execution. Expected stores and every ordered
rectangle argument are derived without reading the observed native outputs.
"""
import argparse,hashlib,json,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.tactics_exit_emulation import SOURCE,SOURCE_SHA256,BASE,TASK
from tools.school_tactical_startup_emulation import TACT
from tools.school_deployment_tail_emulation import ROOT,UNITCTRL,AUTHORITY,report_text

EVIDENCE=ROOT/'analysis/school-scene-opening-v1-20261011.json'
EVIDENCE_SHA256='90b4896db16f17e321bd9ea362a92e75fd8b0fb0f1a19dccd8614c7c69aebd31'
REGIONS=((TACT,400),(UNITCTRL+0x2E6F4,24),(TACT+0x108CC2,2),(0x7A417C,2),(0x7A4184,2))
RANGES=((0x4534A1,0x453527),(0x467AA0,0x467B57),(0x41F710,0x41F822),
 (0x456B20,0x456B58),(0x4077C0,0x407823),(0x451A16,0x451A18),(0x451A45,0x451A58),
 (0x453F10,0x453F77),(0x45413B,0x454290),(0x4547A8,0x4547C2),(0x415040,0x415069))

@lru_cache(maxsize=1)
def source_catalog():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('opening source identity')
 expected={
  0x4534A1:('mov','eax, dword ptr [0x7f44a8]'),0x4534B0:('call','0x467aa0'),
  0x4534C1:('call','0x41f710'),0x4534C9:('call','0x456b20'),
  0x4534D3:('call','0x422360'),0x4534DE:('call','0x415420'),
  0x4534E8:('call','0x422360'),0x4534F3:('call','0x415420'),
  0x4534FB:('mov','dword ptr [ecx + 0x38], 0'),0x45350F:('call','0x4077c0'),
  0x40780D:('mov','dword ptr [ecx + 0x4c], edx'),
  0x467AC3:('mov','dword ptr [eax + 0x2e6fc], ecx'),
  0x467ACF:('mov','dword ptr [edx + 0x2e6f4], eax'),
  0x467AD8:('mov','dword ptr [ecx + 0x2e6f8], 0'),
  0x467AEC:('mov','ecx, 0xc5c100'),0x467AF1:('idiv','ecx'),
  0x467AF6:('mov','ecx, 0x34bc0'),0x467AFB:('idiv','ecx'),
  0x467B00:('mov','dword ptr [edx + 0x2e700], eax'),
  0x467B10:('mov','ecx, 0x34bc0'),0x467B15:('idiv','ecx'),
  0x467B1A:('mov','ecx, 0xe10'),0x467B1F:('idiv','ecx'),
  0x467B24:('mov','dword ptr [edx + 0x2e704], eax'),
  0x467B34:('mov','ecx, 0xe10'),0x467B39:('idiv','ecx'),
  0x467B3E:('mov','ecx, 0x3c'),0x467B43:('idiv','ecx'),
  0x467B48:('mov','dword ptr [edx + 0x2e708], eax'),
  0x453F43:('jmp','dword ptr [edx*4 + 0x4547c2]'),
  0x453F4D:('mov','word ptr [eax + 0x108cc2], 1'),
  0x453F59:('mov','dword ptr [ecx + 0x38], 3'),
  0x453F60:('mov','word ptr [0x7a417c], 0xfc00'),
  0x453F69:('mov','word ptr [0x7a4184], 0'),0x4547AC:('jmp','0x45413b'),
  0x454171:('shl','ecx, 4'),0x454182:('mov','word ptr [ebp - 0x10], 0'),
  0x454193:('mov','word ptr [ebp - 0x10], 0xff'),
  0x4541A2:('sub','edx, ecx'),0x4541B3:('shl','eax, 0x18'),
  0x4541BB:('push','0x400'),0x4541C3:('imul','ecx, ecx, 6'),
  0x4541D5:('call','0x410310'),0x4541F3:('mov','eax, 0x3f'),
  0x4541FE:('add','eax, 0x180'),0x454212:('call','0x410310'),
  0x45421C:('push','6'),0x454224:('call','0x415040'),
  0x41505D:('mov','eax, dword ptr [ebp + 8]'),
  0x454230:('add','cx, ax'),0x454241:('cmp','edx, 0xff'),
  0x454269:('mov','byte ptr [eax + 0x170], 1'),
  0x454273:('mov','byte ptr [ecx + 0x171], 0'),
  0x451A16:('jmp','0x451a45'),0x451709:('call','0x4519c0'),
  0x451711:('call','0x451a60')}
 md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
 for va,pair in expected.items():
  i=next(md.disasm(raw[va-BASE:va-BASE+16],va,count=1))
  if (i.mnemonic,i.op_str)!=pair:raise ValueError(f'opening source instruction {va:#x}')
  proof.append({'va':hex(va),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
 table=struct.unpack_from('<21I',raw,0x4547C2-BASE)
 if (table[0],table[3],table[4])!=(0x453F4A,0x45413B,0x454266):raise ValueError('opening source dispatch')
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'code_inputs':proof,
  'native_ranges':[[hex(a),hex(b)] for a,b in RANGES],
  'native_code_sha256':hashlib.sha256(b''.join(raw[a-BASE:b-BASE] for a,b in RANGES)).hexdigest(),
  'jump_table':[hex(v) for v in table],'timer_divisors':[12960000,216000,3600,60],
  'timer_arithmetic':'signed32_idiv_truncates_toward_zero',
  'opening_phases':[0,3,4,5],'initial_fade':-1024,'native_increment':6,
  'rectangles_per_fade_update':128,'rectangle_width':1024,'rectangle_height':6,
  'natural_initializer_return':'0x45170e','opening_driver':'declared_original_calls',
  'scope':'Opening stops at script-work request; world loop, callbacks, VM and renderer remain pending.',**AUTHORITY}

def signed_timer(value):
 if type(value)!=int or not -(1<<31)<=value<(1<<31):raise ValueError('opening signed32 timer input')
 def div(a,b):return (abs(a)//b)*(-1 if a<0 else 1)
 def rem(a,b):return a-div(a,b)*b
 values=(value,0,value,div(rem(value,12960000),216000),div(rem(value,216000),3600),div(rem(value,3600),60))
 return struct.pack('<6I',*(v&0xFFFFFFFF for v in values)).hex(),values[-1]&0xFFFFFFFF

def region_memory(regions):
 if not isinstance(regions,list) or len(regions)!=len(REGIONS):raise ValueError('opening region count')
 memory={}
 for item,(at,count) in zip(regions,REGIONS):
  if not isinstance(item,dict) or type(item.get('pointer'))!=int or type(item.get('bytes'))!=int or (item['pointer'],item['bytes'])!=(at,count):raise ValueError('opening region ownership')
  value=item.get('hex')
  if not isinstance(value,str):raise ValueError('opening region encoding')
  try:raw=bytes.fromhex(value)
  except ValueError as error:raise ValueError('opening region encoding') from error
  if len(raw)!=count:raise ValueError('opening region size')
  memory[at]=bytearray(raw)
 return memory

def as_regions(memory):return [{'pointer':at,'bytes':n,'hex':memory[at].hex()} for at,n in REGIONS]

def expected_opening(inputs,before):
 source_catalog()
 if not isinstance(inputs,dict) or set(inputs)!={'timer_input','task_pointer','phase','driver','max_updates'}:raise ValueError('opening input shape')
 for key in ('timer_input','task_pointer','phase','max_updates'):
  if type(inputs[key])!=int:raise ValueError('opening input types')
 if (inputs['task_pointer'],inputs['phase'],inputs['driver'],inputs['max_updates'])!=(TASK,2,'declared_original_453f10_updates_on_actual_initialized_state',215):raise ValueError('opening unsupported driver')
 timer,_=signed_timer(inputs['timer_input']);memory=region_memory(before);task=memory[TACT]
 if struct.unpack_from('<I',task,0x34)[0]!=2 or task[0x43]:raise ValueError('opening unsupported scene/active VM')
 memory[UNITCTRL+0x2E6F4]=bytearray.fromhex(timer)
 struct.pack_into('<I',task,0x38,0);struct.pack_into('<I',task,0xB4,TASK)
 initialization_after=as_regions(memory)
 primitives=[{'va':hex(va),'receiver':recv,'args':args,'return_va':hex(ret)} for va,recv,args,ret in (
  (0x422360,TACT,[0],0x4534D8),(0x415420,TASK,[],0x4534E3),
  (0x422360,TACT,[0],0x4534ED),(0x415420,TASK,[],0x4534F8))]
 updates=[];phase=0;fade=struct.unpack('<h',memory[0x7A417C])[0]
 for index in range(215):
  before_phase,before_fade=phase,fade;stream=bytearray();count=0
  if phase==0:
   struct.pack_into('<H',memory[TACT+0x108CC2],0,1)
   phase=3;fade=-1024;memory[0x7A4184]=bytearray(2)
  if phase==3:
   for band in range(64):
    alpha=255-max(0,min(255,fade+band*16))
    for ret,y in ((0x4541DA,band*6),(0x454217,384+(63-band)*6)):
     stream.extend(struct.pack('<8I',ret,0,y,1024,6,5,alpha<<24,1));count+=1
   fade+=6
   if fade>=255:phase=4;memory[0x7A4184]=bytearray(2)
  elif phase==4:
   task[0x170]=1;task[0x171]=0;phase=5
  else:raise ValueError('opening unsupported update phase')
  struct.pack_into('<I',task,0x38,phase);struct.pack_into('<h',memory[0x7A417C],0,fade)
  updates.append({'index':index,'before_phase':before_phase,'before_fade':before_fade,'phase':phase,'fade':fade,
   'return_value':0,'rectangle_count':count,'rectangle_arguments_sha256':hashlib.sha256(stream).hexdigest()})
 return {'initialization_after':initialization_after,'primitives':primitives,
  'opening_before':deepcopy(initialization_after),'opening_after':as_regions(memory),
  'updates':updates,'native_increment_calls':214}

@lru_cache(maxsize=1)
def native_fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('opening evidence identity')
 return json.loads(raw)

def export():
 rules=source_catalog();data=native_fixture()
 evidence={'schema_version':1,'native_report':EVIDENCE.relative_to(ROOT).as_posix(),
  'native_report_sha256':EVIDENCE_SHA256,'cases':data['cases'],'inherited_refusals':data['inherited_refusals'],'runtime_fixture':False}
 for name,value in (('rules',rules),('evidence',evidence)):
  (ROOT/f'prototype/data/school_scene_opening_{name}.json').write_text(report_text(value),encoding='utf-8',newline='\n')

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--export',action='store_true');a=p.parse_args()
 if a.export:export()
