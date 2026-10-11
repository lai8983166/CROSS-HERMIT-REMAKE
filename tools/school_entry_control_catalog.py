"""Independent original entry-control dispatch, camera and wait-store rules."""
import argparse,hashlib,json,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.tactics_exit_emulation import SOURCE,SOURCE_SHA256,BASE,TASK
from tools.school_tactical_startup_emulation import TACT
from tools.school_deployment_tail_emulation import ROOT,UNITCTRL,AUTHORITY,report_text

MAPCTRL=UNITCTRL+0x3D68
REGIONS=((TACT,400),(UNITCTRL+0x108B30,50),(MAPCTRL+0x265A6,4))
EVIDENCE=ROOT/'analysis/school-entry-control-v1-20261011.json'
EVIDENCE_SHA256='8d6640db841aaa25905022a711fc1f0aa9f1c6700a89b3c6dffdec78b794e8b8'
RANGES=((0x499DA0,0x499E6B),(0x499ECE,0x499ED3),(0x49A02F,0x49A114),(0x49A2B3,0x49A2CF),
 (0x43B400,0x43B524),(0x415070,0x415099),(0x456B20,0x456B58),
 (0x453F10,0x453F4A),(0x454290,0x4542B9),(0x4547A8,0x4547C2))

@lru_cache(maxsize=1)
def source_catalog():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('entry source identity')
 expected={0x46B4C3:('call','0x499da0'),0x499DFC:('jmp','dword ptr [ecx*4 + 0x49a2cf]'),
  0x499E0A:('shl','eax, 5'),0x499E0D:('add','eax, 0x10'),0x499E1B:('shl','edx, 4'),
  0x499E1E:('add','edx, 8'),0x499E38:('call','0x43b400'),
  0x499E46:('movsx','ecx, byte ptr [eax + 0x170]'),0x499E65:('mov','byte ptr [ecx + 0xc], 4'),
  0x43B420:('sub','eax, 0x200'),0x43B42B:('sub','ecx, 0x11d'),
  0x43B483:('mov','dword ptr [ebp + 8], 0'),0x43B49A:('sub','edx, 0x400'),
  0x43B4C4:('mov','dword ptr [ebp + 0xc], 0'),0x43B4DB:('sub','edx, 0x238'),
  0x43B506:('mov','word ptr [eax + 0x265a6], cx'),0x43B514:('mov','word ptr [edx + 0x265a8], ax'),
  0x49A038:('mov','byte ptr [edx + 0x170], 0'),
  0x49A042:('mov','byte ptr [eax + 0x108b34], 1'),
  0x49A058:('push','0xb4'),0x49A063:('call','0x415070'),
  0x41508D:('mov','eax, dword ptr [ebp + 8]'),
  0x49A06B:('mov','word ptr [ecx + 0xe], ax'),
  0x49A082:('mov','byte ptr [ecx + 0x108b34], 0'),
  0x49A0A0:('sub','ax, 1'),0x49A0B9:('call','0x456b20'),
  0x49A0C2:('push','1'),0x49A0C4:('push','0'),0x49A0CF:('call','0x4551c0'),
  0x454293:('movsx','edx, byte ptr [ecx + 0x171]'),0x45429C:('je','0x4542b4')}
 md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
 for va,pair in expected.items():
  i=next(md.disasm(raw[va-BASE:va-BASE+16],va,count=1))
  if (i.mnemonic,i.op_str)!=pair:raise ValueError(f'entry source instruction {va:#x}')
  proof.append({'va':hex(va),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
 table=struct.unpack_from('<14I',raw,0x49A2CF-BASE)
 if [table[i] for i in (0,4,5,6)]!=[0x499E03,0x49A02F,0x49A074,0x49A0B0]:raise ValueError('entry source dispatch')
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'code_inputs':proof,
  'native_ranges':[[hex(a),hex(b)] for a,b in RANGES],
  'native_code_sha256':hashlib.sha256(b''.join(raw[a-BASE:b-BASE] for a,b in RANGES)).hexdigest(),
  'jump_table':[hex(v) for v in table],'controller_states':[0,4,5,6],'native_delay':180,
  'completed_controller_updates':183,'waiting_calls':183,'preflight_args':[0,1],
  'preflight_entry':'0x4551c0','preflight_return':'0x49a0d4',
  'request170_meaning':'entry_control_request','completion171_meaning':'entry_completion',
  'scope':'Declared entry updates stop before first preflight instruction; VM and world scheduling pending.',**AUTHORITY}

def memory_regions(regions):
 if not isinstance(regions,list) or len(regions)!=3:raise ValueError('entry region count')
 memory={}
 for item,(at,n) in zip(regions,REGIONS):
  if not isinstance(item,dict) or type(item.get('pointer'))!=int or type(item.get('bytes'))!=int or (item['pointer'],item['bytes'])!=(at,n):raise ValueError('entry region ownership')
  value=item.get('hex')
  if not isinstance(value,str):raise ValueError('entry region encoding')
  try:raw=bytes.fromhex(value)
  except ValueError as error:raise ValueError('entry region encoding') from error
  if len(raw)!=n:raise ValueError('entry region size')
  memory[at]=bytearray(raw)
 return memory

def expected_control(inputs,before):
 source_catalog()
 if not isinstance(inputs,dict) or set(inputs)!={'origin','dimensions','mode','driver','completed_updates'}:raise ValueError('entry input shape')
 for name in ('mode','completed_updates'):
  if type(inputs[name])!=int:raise ValueError('entry input types')
 for name in ('origin','dimensions'):
  if not isinstance(inputs[name],list) or len(inputs[name])!=2 or any(type(v)!=int for v in inputs[name]):raise ValueError('entry input types')
 if inputs!={'origin':[9,16],'dimensions':[64,96],'mode':0,'driver':'declared_499da0_and_phase5_wait_calls','completed_updates':183}:raise ValueError('entry unsupported driver')
 memory=memory_regions(before);task=memory[TACT];control=memory[UNITCTRL+0x108B30];camera=memory[MAPCTRL+0x265A6]
 if struct.unpack_from('<I',task,0x38)[0]!=5 or task[0x43] or task[0x170]!=1 or task[0x171]:raise ValueError('entry unsupported task/VM state')
 if control[4] or control[14] or control[24]!=1 or control[26] or struct.unpack_from('<h',control,28)[0]:raise ValueError('entry unsupported controller state')
 if list(struct.unpack_from('<2h',control,16))!=inputs['origin']:raise ValueError('entry origin binding')
 def state():return {'state':control[26],'delay':struct.unpack_from('<h',control,28)[0],
  'request':task[0x170],'completion':task[0x171],'busy':control[4],'task_phase':struct.unpack_from('<I',task,0x38)[0]}
 calls=[];updates=[]
 for index in range(183):
  previous=state();phase,delay=previous['state'],previous['delay']
  if phase==0:
   x,y=inputs['origin'];width,height=inputs['dimensions']
   cx=min(max(x*32+16-512,0),width*32-1024)
   cy=min(max(y*16+8-285,0),height*16-568)
   struct.pack_into('<2h',camera,0,cx,cy);control[26]=4
   calls.append({'va':'0x43b400','receiver':MAPCTRL,'args':[x*32+16,y*16+8],'return_va':'0x499e3d'})
  elif phase==4:
   task[0x170]=0;control[4]=1;control[26]=5;struct.pack_into('<h',control,28,180)
   calls.append({'va':'0x415070','receiver':TASK,'args':[180],'return_va':'0x49a068'})
  elif phase==5:
   if delay:struct.pack_into('<h',control,28,delay-1)
   else:control[4]=0;control[26]=6
  else:raise ValueError('entry unsupported update phase')
  updates.append({'index':index,'before':previous,'after':state(),'return_value':0,'waiting_return':0})
 return {'after':[{'pointer':at,'bytes':n,'hex':memory[at].hex()} for at,n in REGIONS],'updates':updates,'calls':calls,
  'pending_call':{'va':'0x4551c0','receiver':TACT,'args':[0,1],'return_va':'0x49a0d4','root_return_va':'0x3000000',
   'natural_stack_verified':True,'first_instruction_executed':False}}

@lru_cache(maxsize=1)
def native_fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('entry evidence identity')
 return json.loads(raw)

def export():
 rules=source_catalog();data=native_fixture()
 evidence={'schema_version':1,'native_report':EVIDENCE.relative_to(ROOT).as_posix(),'native_report_sha256':EVIDENCE_SHA256,
  'cases':data['cases'],'inherited_refusals':data['inherited_refusals'],'runtime_fixture':False}
 for name,value in (('rules',rules),('evidence',evidence)):
  (ROOT/f'prototype/data/school_entry_control_{name}.json').write_text(report_text(value),encoding='utf-8',newline='\n')

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--export',action='store_true');a=p.parse_args()
 if a.export:export()
