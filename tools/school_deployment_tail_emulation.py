"""Original deployment tail on SHA-pinned private actual school checkpoints.

Checkpoints are trusted local diagnostic pickles, never external input/save files.
Placement is replayed and compared completely before suffix execution. The full
upstream pipeline and refusals are inherited evidence, not rerun claims.
"""
import argparse, hashlib, json, pickle, struct
from copy import deepcopy
from pathlib import Path
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EBP
from tools.school_formation_placement_emulation import (
 SchoolFormationPlacementEmulator,ROOT,SOURCE_SHA256,UNITCTRL,STACK,RETURN,WORK_OFFSET,WORK_BYTES,
 ExitEmulator,AUTHORITY,report_text)

PARENT=ROOT/'analysis/school-formation-placement-v1-20261011.json'
PARENT_SHA='49539eef42ffb378a48935a0509675a2412fd5c2649956fb93c4f69df973d383'
CHECKPOINTS=(('initial','cd8557993b86b8e15fef05ccc6790231ace041ac4ae27b975ba899c293fce1d2'),
 ('student9_waiting','4d889869c4fb608af8901a4c9b201e6e723dc1d0c74fa892dd9ac830c31d1607'),
 ('fifth_class','7a38d635e84508024fafd5ad87f1d6219852262591fabea193aecd44f82aea10'))
POOL,POOL_BYTES=0x22000000,0x100000
NATIVE=((0x468A49,0x468BAB),(0x437A70,0x437C0C),(0x44E850,0x44E992),
 (0x439550,0x4396D7),(0x439790,0x439813),(0x427650,0x427799),
 (0x427890,0x42798C),(0x427990,0x427A77),(0x427CD0,0x427D13),
 (0x46D860,0x46D96B),(0x49AA60,0x49AB58),(0x46B210,0x46B2B7),
 (0x46A430,0x46A4BD),(0x46A4C0,0x46A54D),(0x468D10,0x468D7D),
 (0x468E10,0x468EA5),(0x493ED0,0x493FD6),(0x427D60,0x427DE0),
 (0x427E30,0x427E6C),(0x427C40,0x427C83),(0x496450,0x49648C),(0x48CD30,0x48CD54))
CODE=frozenset(a for lo,hi in NATIVE for a in range(lo,hi))
REGIONS=((0x2A634,0xA4),(0x2A55C,0x9C),(0xDB814,84),(0xDB868,2724),
 (0x108B30,2),(0x108B50,4),(0x108B60,1000),(0x2F150,20))
TOP_CALLS={0x437A70:0x468A91,0x44E850:0x468AD9,0x46D860:0x468AE1,
 0x49AA60:0x468AE9,0x46B210:0x468AF1,0x493ED0:0x468B71,0x496450:0x468B79,0x48CD30:0x468B98}

def digest(raw):return hashlib.sha256(raw).hexdigest()
def parent_evidence():
 raw=PARENT.read_bytes()
 if digest(raw)!=PARENT_SHA:raise ValueError('deployment parent evidence identity')
 return json.loads(raw)

class SchoolDeploymentTailEmulator(SchoolFormationPlacementEmulator):
 def __init__(self):
  self.deployment_loading=False
  super().__init__()

 def _write_hook(self,uc,access,address,size,value,context):
  if not self.deployment_loading:return super()._write_hook(uc,access,address,size,value,context)
  if not any(a<=address and address+size<=b for a,b in self.deployment_allowed):
   raise RuntimeError(f'deployment finite guard {address:#x}/{size} at{uc.reg_read(UC_X86_REG_EIP):#x}')
  if not STACK<=address<STACK+65536:self.writes.append((address,size,value&((1<<(size*8))-1)))

 def _allocate(self,count,caller):
  ordinal=len(self.deployment_allocations)
  expected=[(172032,0x437AAC,'search_nodes'),(73728,0x4276E1,'search_free_nodes'),
   (24576,0x43962A,'search_cells'),(49152,0x437B41,'search_pairs'),
   (172032,0x44E88C,'search_nodes'),(73728,0x4276E1,'search_free_nodes'),(24576,0x43962A,'search_cells')]
  if ordinal>=len(expected) or (count,caller)!=expected[ordinal][:2]:raise RuntimeError('deployment allocation order/size')
  at=POOL+sum(a['bytes'] for a in self.deployment_allocations)
  if at+count>POOL+POOL_BYTES:raise RuntimeError('deployment allocation budget')
  self.deployment_allocations.append({'pointer':at,'bytes':count,'kind':expected[ordinal][2],'return_va':hex(caller)})
  self.deployment_allowed.append((at,at+count))
  # Declared malloc contents are poison, not a replacement search output.
  self.primitive_write(at,bytes([0xCD])*count)
  return at

 def _hook(self,uc,address,size,context):
  if not self.deployment_loading:return super()._hook(uc,address,size,context)
  sp,recv=uc.reg_read(UC_X86_REG_ESP),uc.reg_read(UC_X86_REG_ECX)
  if address==0x4534A1:
   if uc.reg_read(UC_X86_REG_EAX)!=0 or sp!=self.deployment_frame+8 or uc.reg_read(UC_X86_REG_EBP)!=self.deployment_outer_frame:
    raise RuntimeError('deployment natural zero return/stack')
   self.stop_reason='deployment_return_before_467aa0';uc.emu_stop();return
  if address in TOP_CALLS:
   expected_recv=UNITCTRL+(0x2A634 if address==0x437A70 else 0x2A55C if address==0x44E850 else 0)
   if recv!=expected_recv or self.read(sp)!=TOP_CALLS[address]:raise RuntimeError('deployment natural helper caller')
   args=[self.read(sp+4+i*4) for i in range(3)] if address in (0x437A70,0x44E850) else []
   if args and args!=[64,96,6144]:raise RuntimeError('deployment source map dimensions')
   self.deployment_calls.append({'va':hex(address),'receiver':recv,'args':args,'return_va':hex(self.read(sp))})
  if address==0x428A40:
   self._stub_return(self._allocate(self.read(sp+4),self.read(sp)),0);return
  if address==0x56CEC0:
   at,byte,count=[self.read(sp+i) for i in (4,8,12)];caller=self.read(sp)
   allocation_clears={0x437B0D:0,0x42774C:None,0x4397FF:None,0x44E8ED:4}
   fixed={0x46D88F:(UNITCTRL+0xDB818,80),0x49AA92:(UNITCTRL+0xDB86C,2720),
    0x468B1E:(UNITCTRL+0x108B60,1000),0x468B34:(UNITCTRL+0x2F150,20)}
   if caller in allocation_clears:
    candidates=[a for a in self.deployment_allocations if (a['pointer'],a['bytes'])==(at,count)]
    if len(candidates)!=1:raise RuntimeError('deployment clear allocation ownership')
    a=candidates[0];idx=allocation_clears[caller]
    if idx is not None and a is not self.deployment_allocations[idx]:raise RuntimeError('deployment clear source caller')
    if caller==0x42774C and a['kind']!='search_free_nodes':raise RuntimeError('deployment free-node clear')
    if caller==0x4397FF and a['kind']!='search_cells':raise RuntimeError('deployment cell clear')
   elif fixed.get(caller)!=(at,count):raise RuntimeError('deployment exact fixed clear')
   if byte:raise RuntimeError('deployment nonzero clear')
   self.primitive_write(at,bytes(count));self.deployment_clears.append({'target':at,'bytes':count,'return_va':hex(caller)})
   self._stub_return(at,0);return
  if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
  if address==0x424F80:raise RuntimeError(f'deployment original assertion return{self.read(sp):#x}')
  if address in CODE:self.visited.add(address);return
  raise RuntimeError(f'deployment undeclared instruction {address:#x}')

 def run_deployment_tail(self):
  if self.uc.reg_read(UC_X86_REG_EIP)!=0x468A49:raise RuntimeError('deployment requires actual placement boundary')
  self.deployment_frame=self.uc.reg_read(UC_X86_REG_EBP);self.deployment_outer_frame=self.read(self.deployment_frame)
  if self.read(self.deployment_frame+4)!=0x4534A1 or self.read(0x7F4491,'B'):raise RuntimeError('deployment original frame/branch')
  header=self.read(UNITCTRL+0x2A304)
  if [self.read(header+i,'h') for i in (4,6)]!=[64,96]:raise RuntimeError('deployment map shape')
  self.uc.mem_map(POOL,POOL_BYTES)
  slots=[];selected=[]
  category=self.read(UNITCTRL+0x2EF44,'B')
  for i in range(250):
   w=UNITCTRL+WORK_OFFSET+i*WORK_BYTES
   if not self.read(w,'h'):continue
   r=self.read(w+600);raw=bytes(self.uc.mem_read(r,176))
   s={'index':i,'work_pointer':w,'record_pointer':r,'record_hex':raw.hex(),'before_work_hex':bytes(self.uc.mem_read(w,WORK_BYTES)).hex()}
   slots.append(s)
   if raw[164]==category and 1<=struct.unpack_from('<H',raw,2)[0]<=45:selected.append(s)
  if len(selected)>20:raise RuntimeError('deployment current index capacity')
  regions=[{'pointer':UNITCTRL+off,'bytes':count,'before_hex':bytes(self.uc.mem_read(UNITCTRL+off,count)).hex()} for off,count in REGIONS]
  lists=[]
  for i in range(10):
   at=UNITCTRL+0x116098+i*44;nodes=self.read(at+8)
   owned=[a for a in self.unit_allocations if a['pointer']==nodes and a['bytes']==240 and not a['freed']]
   if self.read(at+4)!=20 or len(owned)!=1:raise RuntimeError('deployment category-list original ownership')
   lists.append({'category':i,'pointer':at,'nodes_pointer':nodes,'before_hex':bytes(self.uc.mem_read(at,44)).hex(),
    'before_nodes_hex':bytes(self.uc.mem_read(nodes,240)).hex()})
  self.deployment_allocations=[];self.deployment_calls=[];self.deployment_clears=[]
  self.deployment_allowed=[(STACK,STACK+65536)]+[(r['pointer'],r['pointer']+r['bytes']) for r in regions]
  for s in selected:
   w=s['work_pointer'];self.deployment_allowed += [(w+0x501,w+0x502),(w+604,w+608)]
  for item in lists:self.deployment_allowed += [(item['pointer'],item['pointer']+44),(item['nodes_pointer'],item['nodes_pointer']+240)]
  retained=self.capture_scene_memory(self.deployment_allowed[1:]+[(POOL,POOL+589824)])
  # The parent capture excludes null ownership; explicitly retain it here too.
  null_before=bytes(self.uc.mem_read(0,4))
  self.deployment_loading=True;self.stop_reason=None;self.clear_trace('tactical_startup')
  try:
   self.uc.emu_start(0x468A49,RETURN,timeout=30_000_000,count=4_000_000)
   if self.stop_reason!='deployment_return_before_467aa0' or len(self.deployment_allocations)!=7 or len(self.deployment_calls)!=8:
    raise RuntimeError('deployment finite suffix incomplete')
   for a in self.deployment_allocations:a['hex']=bytes(self.uc.mem_read(a['pointer'],a['bytes'])).hex()
   for r in regions:r['hex']=bytes(self.uc.mem_read(r['pointer'],r['bytes'])).hex()
   for s in slots:s['work_hex']=bytes(self.uc.mem_read(s['work_pointer'],WORK_BYTES)).hex()
   for item in lists:
    item['hex']=bytes(self.uc.mem_read(item['pointer'],44)).hex();item['nodes_hex']=bytes(self.uc.mem_read(item['nodes_pointer'],240)).hex()
   if bytes(self.uc.mem_read(0,4))!=null_before:raise RuntimeError('deployment null memory retention')
   return {'inputs':{'dimensions':[64,96],'category':category,'mode':self.read(UNITCTRL+0x117C3C,'B'),
    'malloc_fill_byte':205,'pool':POOL,'pool_bytes':POOL_BYTES},'units':slots,'selected_indices':[s['index'] for s in selected],
    'regions':regions,'category_lists':lists,'allocations':deepcopy(self.deployment_allocations),
    'calls':deepcopy(self.deployment_calls),'clears':deepcopy(self.deployment_clears),
    'stop_va':'0x4534a1','return_value':0,'natural_stack_verified':True,'deployment_completed':True,
    'next_467aa0_executed':False,'scene_vm_executed':False,**self.verify_scene_memory(retained)}
  finally:self.deployment_loading=False

def restored_case(index,parent=None):
 parent=parent or parent_evidence();name,sha=CHECKPOINTS[index]
 path=ROOT/f'.venv-audit/formation-actual-checkpoint-{index}.pkl';raw=path.read_bytes()
 if digest(raw)!=sha:raise ValueError('deployment trusted checkpoint identity')
 payload=pickle.loads(raw)
 if payload['source_sha']!=SOURCE_SHA256 or payload['evidence_kind']!='private_actual_cpu_after_full35_before_placement':
  raise ValueError('deployment checkpoint provenance')
 e=SchoolDeploymentTailEmulator()
 e.__dict__.update({k:v for k,v in payload['state'].items() if not k.startswith('_audit_') and k!='uc'})
 for at,data in payload['memory']:e.uc.mem_write(at,data)
 e.uc.context_restore(payload['cpu'])
 placement=e.run_placement();previous=parent['cases'][index]
 if previous['name']!=name or placement!=previous['formation_placement']:raise ValueError('deployment full original placement mismatch')
 return e,{'name':name,'provenance':{'checkpoint_sha256':sha,'checkpoint_kind':payload['evidence_kind'],
  'parent_report_sha256':PARENT_SHA,'complete_placement_equal':True,'upstream_rerun':False}}

def report():
 parent=parent_evidence();cases=[]
 for index in range(3):
  e,item=restored_case(index,parent);item['deployment_tail']=e.run_deployment_tail();cases.append(item)
  print('Actual checkpoint deployment '+item['name']+': natural4534A1',flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
  'inherited_refusals':[{'name':c['name'],'ready':c['ready'],'placement_executed':False,'suffix_executed':False,
   'evidence_origin':'immutable_parent_not_rerun','parent_report_sha256':PARENT_SHA} for c in parent['cases'][3:]],
  'boundary':'Original468910 now returns4534A1; next467AA0, scene VM, event waves and graphical battle remain pending.',**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use a new immutable evidence path')
 path.write_text(report_text(report()),encoding='utf-8',newline='\n')
