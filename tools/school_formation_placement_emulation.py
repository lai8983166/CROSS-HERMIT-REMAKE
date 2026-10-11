"""Actual school formation placement; stops before search workspace and scene VM."""
import argparse,hashlib,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EBP
from tools.school_scene_remaining_emulation import SchoolSceneRemainingEmulator
from tools.school_scene_unit_constructor_emulation import (
 ROOT,SOURCE_SHA256,UNITCTRL,TACT,STACK,RETURN,WORK_OFFSET,WORK_BYTES,RECORD_OFFSET,
 ExitEmulator,AUTHORITY,report_text)

MAPCTRL=UNITCTRL+0x3D68
RESERVATION=MAPCTRL+0x263C8
ROTATION=MAPCTRL+0x263C4
NATIVE=((0x45363D,0x45364E),(0x453493,0x4534A1),(0x468910,0x468A49),
 (0x456B20,0x456B58),(0x49A480,0x49A5F7),(0x43D4E0,0x43D526),
 (0x43D530,0x43D5AD),(0x43D5B0,0x43D655),(0x43D660,0x43D970),
 (0x468D10,0x468D7D),(0x468E10,0x468EA5),(0x46AB20,0x46ABBB),
 (0x43BE60,0x43BF95),(0x468690,0x468805),(0x46B2C0,0x46B346),(0x43C470,0x43C52B))
CODE=frozenset(a for lo,hi in NATIVE for a in range(lo,hi))

class SchoolFormationPlacementEmulator(SchoolSceneRemainingEmulator):
 def __init__(self):
  self.placement_loading=False
  super().__init__()

 def call(self,address,args=(),receiver=None):
  if not self.placement_loading:return super().call(address,args,receiver=receiver)
  previous=self._function_ranges
  try:
   self._function_ranges=previous+NATIVE
   return super().call(address,args,receiver=receiver)
  finally:self._function_ranges=previous

 def _write_hook(self,uc,access,address,size,value,context):
  if not self.placement_loading:return super()._write_hook(uc,access,address,size,value,context)
  allowed=[(STACK,STACK+65536),(ROTATION,ROTATION+2),(RESERVATION,RESERVATION+164)]
  for s in self.placement_selected:
   w,r=s['work_pointer'],s['record_pointer']
   allowed += [(r+155,r+157),(w+748,w+756),(w+1255,w+1259)]
  # A cell write is admitted only after its original43C470 input is validated.
  allowed += [(a,a+1) for a in self.placement_cells]
  if not any(a<=address and address+size<=b for a,b in allowed):
   raise RuntimeError(f'formation finite guard {address:#x}/{size} at{uc.reg_read(UC_X86_REG_EIP):#x}')
  if not STACK<=address<STACK+65536:self.writes.append((address,size,value&((1<<(size*8))-1)))

 def _hook(self,uc,address,size,context):
  if not self.placement_loading:return super()._hook(uc,address,size,context)
  sp,recv=uc.reg_read(UC_X86_REG_ESP),uc.reg_read(UC_X86_REG_ECX)
  if address==0x468A49:
   if len(self.placement_calls)!=1 or self.read(uc.reg_read(UC_X86_REG_EBP)+4)!=0x4534A1:raise RuntimeError('formation natural caller/return')
   self.stop_reason='after_school_formation_before_search_workspace';uc.emu_stop();return
  if address==0x453493:
   if self.read(uc.reg_read(UC_X86_REG_EBP)-4)!=TACT:raise RuntimeError('formation original outer caller frame')
  if address==0x468910:
   if (recv,self.read(sp))!=(UNITCTRL,0x4534A1):raise RuntimeError('formation original deployment call')
  if address==0x49A480:
   args=[self.read(sp+4+i*4) for i in range(4)]
   if recv!=UNITCTRL or self.read(sp)!=0x468A49 or args[0]!=self.placement_input['selected_class']:
    raise RuntimeError('formation original single-school branch')
   self.placement_calls.append({'va':hex(address),'receiver':recv,'args':args,'return_va':hex(self.read(sp))})
  if address==0x468690:
   w=self.read(sp+4);xy=[self.read(sp+8,'h'),self.read(sp+12,'h')]
   if recv!=UNITCTRL or self.read(sp)!=0x49A5AE or w not in {s['work_pointer'] for s in self.placement_selected}:
    raise RuntimeError('formation selected coordinate input')
   self.placement_positions.append({'work_pointer':w,'xy':xy})
  if address==0x43C470:
   x,y,on=[self.read(sp+4+i*4) for i in range(3)]
   if recv!=MAPCTRL or self.read(sp) not in (0x4687A8,0x4687DC) or on not in (0,1) or not (0<=x<64 and 0<=y<96):
    raise RuntimeError('formation exact occupancy input')
   self.placement_cells.add(self.placement_cm+2*(y*64+x)+1)
  if address==0x56CEC0:
   target,byte,count=[self.read(sp+i) for i in (4,8,12)]
   if (target,byte,count,self.read(sp))!=(RESERVATION,0,164,0x43D512):raise RuntimeError('formation exact reservation clear')
   self.primitive_write(target,bytes(count));self.placement_clears.append({'target':target,'bytes':count,'return_va':'0x43d512'})
   self._stub_return(target,0);return
  if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
  if address==0x424F80:raise RuntimeError(f'formation original assertion return{self.read(sp):#x}')
  if address in CODE:self.visited.add(address);return
  raise RuntimeError(f'formation undeclared instruction {address:#x}')

 def run_placement(self):
  if self.uc.reg_read(UC_X86_REG_EIP)!=0x45363D:raise RuntimeError('formation requires actual completed scene loop')
  scene=self.read(0x7F4488,'h');selected=self.read(0x7F4490,'B')
  if scene!=5 or self.read(0x7F4491,'B') or self.read(0x7F448F,'b'):raise RuntimeError('unsupported formation scene/branch')
  self.placement_selected=[];self.placement_calls=[];self.placement_positions=[];self.placement_clears=[];self.placement_cells=set()
  header=self.read(UNITCTRL+0x2A304);self.placement_cm=self.read(self.read(UNITCTRL+0x2A308))
  if [self.read(header+i,'H') for i in (4,6)]!=[64,96]:raise RuntimeError('formation map shape')
  slots=[]
  for i in range(250):
   w=UNITCTRL+WORK_OFFSET+i*WORK_BYTES;raw=bytes(self.uc.mem_read(w,WORK_BYTES))
   if struct.unpack_from('<h',raw)[0]==0:continue
   r=self.read(w+600);expected=UNITCTRL+RECORD_OFFSET+i*176
   if r!=expected:raise RuntimeError('formation record ownership')
   record=bytes(self.uc.mem_read(r,176));role=struct.unpack_from('<H',record,2)[0]
   s={'index':i,'work_pointer':w,'record_pointer':r,'before_work_hex':raw.hex(),'before_record_hex':record.hex()}
   slots.append(s)
   if 1<=role<=45 and record[164]==selected and record[15]==1:self.placement_selected.append(s)
  grid=self.read(MAPCTRL+0x263B8);gw,gh=[self.read(MAPCTRL+i,'h') for i in (0x263C0,0x263C2)]
  terrain=self.read(MAPCTRL+0x8C)
  self.placement_input={'scene_id':scene,'selected_class':selected,'origin':[self.read(0x7F4492,'h'),self.read(0x7F4494,'h')],
   'formation_radius':self.read(0x7F44A2,'b'),'grid_dimensions':[gw,gh],'grid_hex':bytes(self.uc.mem_read(grid,gw*gh*6)).hex(),
   'formation_sizes_hex':bytes(self.uc.mem_read(0x59558C,66)).hex(),'terrain_pointer':terrain,'terrain_hex':bytes(self.uc.mem_read(terrain,7600)).hex(),
   'map_hex':bytes(self.uc.mem_read(header,16+64*96*6)).hex(),'before_cm_hex':bytes(self.uc.mem_read(self.placement_cm,12288)).hex(),
   'before_rotation':self.read(ROTATION,'h'),'before_reservation_hex':bytes(self.uc.mem_read(RESERVATION,164)).hex()}
  excluded=[(ROTATION,ROTATION+2),(RESERVATION,RESERVATION+164),(self.placement_cm,self.placement_cm+12288)]
  for s in self.placement_selected:
   w,r=s['work_pointer'],s['record_pointer'];excluded += [(r+155,r+157),(w+748,w+756),(w+1255,w+1259)]
  retained=self.capture_scene_memory(excluded)
  self.placement_loading=True;self.stop_reason=None;self.clear_trace('tactical_startup')
  try:
   self.uc.emu_start(0x45363D,RETURN,timeout=30_000_000,count=3_000_000)
   if self.stop_reason!='after_school_formation_before_search_workspace':raise RuntimeError('formation finite budget incomplete')
   if len(self.placement_positions)!=len(self.placement_selected):raise RuntimeError('formation selected units incomplete')
   for s in slots:
    s['work_hex']=bytes(self.uc.mem_read(s['work_pointer'],WORK_BYTES)).hex();s['record_hex']=bytes(self.uc.mem_read(s['record_pointer'],176)).hex()
   return {'inputs':deepcopy(self.placement_input),'units':slots,'selected_indices':[s['index'] for s in self.placement_selected],
    'positions':deepcopy(self.placement_positions),'calls':deepcopy(self.placement_calls),'clears':deepcopy(self.placement_clears),
    'rotation':self.read(ROTATION,'h'),'reservation_hex':bytes(self.uc.mem_read(RESERVATION,164)).hex(),
    'cm_hex':bytes(self.uc.mem_read(self.placement_cm,12288)).hex(),'stop_va':'0x468a49','stop_reason':self.stop_reason,
    'formation_placement_executed':True,'deployment_completed':False,'scene_vm_executed':False,
    **self.verify_scene_memory(retained)}
  finally:self.placement_loading=False

 def resources(self,name,commands=()):
  self.placement_loading=False;result=super().resources(name,commands)
  result.update(formation_placement_completed=False,formation_placement=None)
  if result['ready']:
   result['formation_placement']=self.run_placement();result['formation_placement_completed']=True;result['stop_reason']=self.stop_reason
  return result

def report():
 e=SchoolFormationPlacementEmulator()
 if not e.run_planning('formation_upstream')['school_data_prepared']:raise RuntimeError('school prefix missing')
 checkpoint=[(a,bytes(e.uc.mem_read(a,b-a+1))) for a,b,_ in e.uc.mem_regions()];cpu=e.uc.context_save();cases=[]
 for name,commands in [('initial',()),('student9_waiting',[('student',9,-1)]),
  ('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1),('student',9,-1)]),
  ('teacher_only',[('student',3,-1),('student',4,-1),('student',9,-1)]),('teacher_waiting',[('teacher',101,-1)])]:
  for at,raw in checkpoint:e.uc.mem_write(at,raw)
  e.uc.context_restore(cpu);e.placement_loading=False;e.stop_reason=None
  cases.append(e.resources(name,commands));print('Actual formation '+name+': '+str(cases[-1]['formation_placement_completed']),flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
  'boundary':'Actual school formation positions at468A49; later search workspace, deployment completion, VM and GPU remain unexecuted/declared.',**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use a new immutable evidence path')
 path.write_text(report_text(report()),encoding='utf-8',newline='\n')
