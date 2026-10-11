"""Independent EXE-derived search/list initialization and complete byte rules."""
import argparse,hashlib,json,struct
from copy import deepcopy
from functools import lru_cache
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from tools.tactics_exit_emulation import SOURCE,SOURCE_SHA256,BASE
from tools.school_deployment_tail_emulation import ROOT,UNITCTRL,POOL,POOL_BYTES,PARENT_SHA,NATIVE,AUTHORITY,report_text

EVIDENCE=ROOT/'analysis/school-deployment-tail-v1-20261011.json'
EVIDENCE_SHA256='82812542fc02b448d33bd3c743da973935949d37475f9676ba20b9c2b1e09132'

@lru_cache(maxsize=1)
def source_catalog():
 raw=SOURCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('deployment source identity')
 md=Cs(CS_ARCH_X86,CS_MODE_32)
 expected={0x468A8C:('call','0x437a70'),0x468AD4:('call','0x44e850'),
  0x437AA3:('imul','edx, edx, 0x1c'),0x437B38:('shl','edx, 3'),
  0x44E883:('imul','edx, edx, 0x1c'),0x4276D8:('imul','ecx, ecx, 0xc'),
  0x4395FA:('imul','eax, eax, 0x1c'),0x439621:('shl','edx, 2'),
  0x46A48C:('mov','cl, byte ptr [eax + 0xa4]'),0x46A497:('mov','al, byte ptr [edx + 0x2ef44]'),
  0x468E70:('cmp','ecx, 1'),0x468E84:('cmp','ecx, 0x2d'),
  0x46D913:('mov','byte ptr [ecx + eax + 0x80fed], dl'),
  0x49AB26:('mov','dword ptr [edx + ecx + 0x80d48], eax'),
  0x493EF9:('sub','eax, 1'),0x493F4E:('mov','dl, byte ptr [ecx + 0x98]'),
  0x493FA0:('call','0x427d60'),0x493FBB:('call','0x427e30'),0x468BAA:('ret','')}
 inputs=[]
 for va,pair in expected.items():
  i=next(md.disasm(raw[va-BASE:va-BASE+16],va,count=1))
  if (i.mnemonic,i.op_str)!=pair:raise ValueError(f'deployment source instruction {va:#x}')
  inputs.append({'va':hex(va),'hex':i.bytes.hex(),'mnemonic':i.mnemonic,'operands':i.op_str})
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'code_inputs':inputs,
  'native_ranges':[[hex(a),hex(b)] for a,b in NATIVE],
  'native_code_sha256':hashlib.sha256(b''.join(raw[a-BASE:b-BASE] for a,b in NATIVE)).hexdigest(),
  'dimensions':[64,96],'search_node_stride':28,'free_node_stride':12,'cell_stride':4,'pair_stride':8,
  'unit_index_capacity':20,'display_stride':136,'category_count':10,'category_capacity':20,
  'selected_role_range':[1,45],'selection_uses_record_state':False,
  'stop_va':'0x4534a1','scope':'Complete468910 tail; next467AA0, event VM and live GPU remain pending.',**AUTHORITY}

def unpack_hex(value,count,label):
 if not isinstance(value,str):raise ValueError(label+' encoding')
 try:raw=bytes.fromhex(value)
 except ValueError as error:raise ValueError(label+' encoding') from error
 if len(raw)!=count:raise ValueError(label+' size')
 return bytearray(raw)
def put(raw,off,value):struct.pack_into('<I',raw,off,value)
def get(raw,off):return struct.unpack_from('<I',raw,off)[0]

def expected_tail(inputs,units,regions,category_lists):
 source_catalog()
 if not isinstance(inputs,dict) or any(type(inputs.get(k))!=int for k in ('category','mode','malloc_fill_byte','pool','pool_bytes')):
  raise ValueError('deployment input types')
 if inputs!={'dimensions':[64,96],'category':0,'mode':0,'malloc_fill_byte':205,'pool':POOL,'pool_bytes':POOL_BYTES}:
  raise ValueError('deployment unsupported current-scene input')
 n=64*96;specs=((28,0x437AAC,'search_nodes'),(12,0x4276E1,'search_free_nodes'),(4,0x43962A,'search_cells'),
  (8,0x437B41,'search_pairs'),(28,0x44E88C,'search_nodes'),(12,0x4276E1,'search_free_nodes'),(4,0x43962A,'search_cells'))
 allocations=[];cursor=POOL
 for stride,caller,kind in specs:
  size=n*stride;allocations.append({'pointer':cursor,'bytes':size,'kind':kind,'return_va':hex(caller),
   'hex':(bytes([205])*size if kind=='search_pairs' else bytes(size)).hex()});cursor+=size
 expected_regions=((0x2A634,164),(0x2A55C,156),(0xDB814,84),(0xDB868,2724),
  (0x108B30,2),(0x108B50,4),(0x108B60,1000),(0x2F150,20))
 if [(r.get('pointer'),r.get('bytes')) for r in regions]!=[(UNITCTRL+a,b) for a,b in expected_regions]:raise ValueError('deployment region ownership')
 raw_regions={a:unpack_hex(r['before_hex'],b,'deployment region') for (a,b),r in zip(expected_regions,regions)}
 for off,inner,indices in ((0x2A634,24,(0,1,2)),(0x2A55C,16,(4,5,6))):
  raw=raw_regions[off];node,free,cell=(allocations[i] for i in indices)
  put(raw,0,n);put(raw,4,n);put(raw,8,node['pointer'])
  if off==0x2A634:put(raw,12,allocations[3]['pointer'])
  put(raw,inner+0x30,64);put(raw,inner+0x34,96);put(raw,inner+0x2C,n)
  li=inner+0x60
  if get(raw,li)!=0 or any(raw[li:li+40]):raise ValueError('deployment search list must be original empty constructor')
  put(raw,li,n);put(raw,li+4,free['pointer']);put(raw,li+0x1C,free['pointer']+(n-1)*12)
  put(raw,inner+0x88,cell['pointer'])
  nodes=bytearray(n*12);sentinel=UNITCTRL+off+li+24
  for i in range(n):
   put(nodes,i*12,free['pointer']+(i+1)*12 if i<n-1 else sentinel)
   put(nodes,i*12+4,free['pointer']+(i-1)*12 if i else 0)
   put(nodes,i*12+8,node['pointer']+i*28)
  free['hex']=nodes.hex()
 slots=deepcopy(units);selected=[];count=0;last=-1
 for s in slots:
  i=s.get('index')
  if type(i)!=int or not last<i<250:raise ValueError('deployment ordered unique work index')
  last=i;w=UNITCTRL+0x80AEC+i*1312;r=UNITCTRL+0xD0C2C+i*176
  if (s.get('work_pointer'),s.get('record_pointer'))!=(w,r):raise ValueError('deployment unit ownership')
  work=unpack_hex(s['before_work_hex'],1312,'deployment work');record=unpack_hex(s['record_hex'],176,'deployment record')
  if not struct.unpack_from('<h',work)[0] or get(work,600)!=r:raise ValueError('deployment unit record binding')
  if record[164]==0:count+=1
  if record[164]==0 and 1<=struct.unpack_from('<H',record,2)[0]<=45:selected.append(s)
  s['work_hex']=work.hex()
 if len(selected)>20:raise ValueError('deployment unit capacity')
 raw_regions[0xDB814]=bytearray(84);put(raw_regions[0xDB814],0,len(selected))
 raw_regions[0xDB868]=bytearray(2724);put(raw_regions[0xDB868],0,len(selected))
 for ordinal,s in enumerate(selected):
  work=bytearray.fromhex(s['work_hex']);work[0x501]=ordinal;put(work,604,UNITCTRL+0xDB86C+ordinal*136);s['work_hex']=work.hex()
  put(raw_regions[0xDB814],4+ordinal*4,s['work_pointer'])
 struct.pack_into('<H',raw_regions[0x108B30],0,count)
 raw_regions[0x108B50]=bytearray(4);raw_regions[0x108B60]=bytearray(1000)
 raw_regions[0x2F150]=bytearray(20);raw_regions[0x2F150][12:16]=bytes([255])*4
 if len(category_lists)!=10:raise ValueError('deployment category list count')
 lists=deepcopy(category_lists);memory={};owned=[]
 for i,item in enumerate(lists):
  at=UNITCTRL+0x116098+i*44;p=item.get('nodes_pointer')
  if item.get('category')!=i or item.get('pointer')!=at or type(p)!=int or not 0xF000000<=p<=0xF100000-240 or p in owned:raise ValueError('deployment category node ownership')
  if any(p<q+240 and q<p+240 for q in owned):raise ValueError('deployment category node overlap')
  owned.append(p);raw=unpack_hex(item['before_hex'],44,'deployment category');nodes=unpack_hex(item['before_nodes_hex'],240,'deployment category nodes')
  if get(raw,4)!=20 or get(raw,8)!=p or get(raw,32)!=p+19*12 or get(raw,20)!=0:raise ValueError('deployment category original free head')
  for j in range(20):
   if (get(nodes,j*12),get(nodes,j*12+4),get(nodes,j*12+8))!=(p+(j+1)*12 if j<19 else at+28,p+(j-1)*12 if j else 0,0):raise ValueError('deployment category original free chain')
  memory[at]=raw;memory[p]=nodes
 def locate(address):
  for base,raw in memory.items():
   if base<=address<=base+len(raw)-4:return raw,address-base
  raise ValueError('deployment linked-list pointer outside ownership')
 def read(address):raw,off=locate(address);return get(raw,off)
 def write(address,value):raw,off=locate(address);put(raw,off,value)
 for s in reversed(selected):
  category=bytes.fromhex(s['record_hex'])[152]
  if category>=10:raise ValueError('deployment record category outside list table')
  at=UNITCTRL+0x116098+category*44;entry=read(at+32)
  if not entry:raise ValueError('deployment category capacity exhausted')
  write(at+32,read(entry+4));write(entry+8,s['work_pointer'])
  sentinel=at+16;head=read(sentinel+4)
  if head:write(head,entry)
  write(entry,sentinel);write(entry+4,head);write(sentinel+4,entry)
 for item in lists:item['hex']=memory[item['pointer']].hex();item['nodes_hex']=memory[item['nodes_pointer']].hex()
 out_regions=deepcopy(regions)
 for (off,_),item in zip(expected_regions,out_regions):item['hex']=raw_regions[off].hex()
 return {'allocations':allocations,'regions':out_regions,'units':slots,'category_lists':lists,'selected_indices':[s['index'] for s in selected]}

@lru_cache(maxsize=1)
def native_fixture():
 raw=EVIDENCE.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=EVIDENCE_SHA256:raise ValueError('deployment evidence identity')
 return json.loads(raw)

def export():
 rules=source_catalog();evidence={'schema_version':1,'native_report':EVIDENCE.relative_to(ROOT).as_posix(),
  'native_report_sha256':EVIDENCE_SHA256,'parent_report_sha256':PARENT_SHA,'cases':native_fixture()['cases'],
  'inherited_refusals':native_fixture()['inherited_refusals'],'runtime_fixture':False}
 for name,value in (('rules',rules),('evidence',evidence)):
  path=ROOT/f'prototype/data/school_deployment_tail_{name}.json';path.write_text(report_text(value),encoding='utf-8',newline='\n')

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--export',action='store_true');a=p.parse_args()
 if a.export:export()
