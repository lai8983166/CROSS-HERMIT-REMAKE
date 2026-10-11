"""Actual scene5 ordinals10–34 constructors and final progress; GPU declared."""
import argparse,hashlib,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_ECX,UC_X86_REG_EAX
from tools.school_scene_batch_emulation import SchoolSceneBatchEmulator
from tools.school_scene_next_input_emulation import CACHE_OFFSET,CACHE_COUNT,COUNTER_OFFSET,SCRATCH,SchoolEnemyRecordsEmulator
from tools.school_scene_unit_constructor_emulation import (
 ROOT,SOURCE,SOURCE_SHA256,UNITCTRL,TACT,TASK,STACK,RETURN,WORK_OFFSET,WORK_BYTES,
 RECORD_OFFSET,ExitEmulator,AUTHORITY,report_text,cstring,FILE_API,FILE_IMPORTS,
 SchoolTacticalResourcesEmulator,SHARED_OFFSET,SHARED_BYTES)
from tools.school_scene_unit_work_catalog import source_catalog as prefix_catalog
from tools.dxanim_lib import parse_dxanim,parse_container

REMAINING_CONTROLLERS,REMAINING_CONTROLLER_BYTES=0x1E000000,0x1000
REMAINING_ANIM,REMAINING_ANIM_BYTES=0x1F000000,0x400000
ORDINALS=tuple(range(10,35))

def remaining_resource(job,variant,rules=None):
 if type(job) is not int or type(variant) is not int or (job,variant) not in ((452,0),(301,1),(316,2),(317,3),(337,1),(406,0)):
  raise ValueError('unsupported scene remaining job/variant')
 r=prefix_catalog() if rules is None else rules;j=r['jobs'][str(job)];identity=r['archives'][j['relative_path']]
 raw=(ROOT/identity['path']).read_bytes()
 if len(raw)!=identity['bytes'] or hashlib.sha256(raw).hexdigest()!=identity['sha256']:
  raise ValueError('scene remaining archive identity')
 o=parse_dxanim(raw);image_bytes,count,_=parse_container(raw,o[6]);_,palettes,entries=parse_container(raw,o[7])
 if count!={452:122,301:98,316:118,317:118,337:47,406:29}[job] or palettes!={452:4,301:6,316:4,317:4,337:6,406:4}[job] or o[8]+((count+3)&~3)!=len(raw):
  raise ValueError('scene remaining archive shape')
 return raw,{'relative_path':j['relative_path'],'local_file':identity['path'],'bytes':len(raw),'sha256':identity['sha256']},  {'offsets':o,'metadata_bytes':o[6],'image_bytes':image_bytes,'count':count,'variant':variant,
   'palette_offset':o[7]+entries[variant-1] if variant else None}

class SchoolSceneRemainingEmulator(SchoolSceneBatchEmulator):
 def __init__(self):
  self.remaining_loading=False
  super().__init__();self.uc.mem_map(REMAINING_CONTROLLERS,REMAINING_CONTROLLER_BYTES);self.uc.mem_map(REMAINING_ANIM,REMAINING_ANIM_BYTES)
  self.remaining_rules=prefix_catalog()

 def reset_remaining(self):
  self.remaining_phase='loop';self.remaining_units=[];self.remaining_progress=[];self.remaining_ordinal=10
  self.remaining_controller_cursor=REMAINING_CONTROLLERS;self.remaining_animation_cursor=REMAINING_ANIM
  self.remaining_work=None;self.enemy_record=None;self.current=None;self.remaining_owned={}

 def _write_hook(self,uc,access,address,size,value,context):
  if not self.remaining_loading:return super()._write_hook(uc,access,address,size,value,context)
  allowed=[(STACK,STACK+0x10000),(0,4)]
  if self.remaining_phase=='loop':allowed.append((TACT+0x40,TACT+0x42))
  if self.remaining_phase=='record' and self.enemy_record:
   p=self.enemy_record['record_pointer'];allowed.append((p,p+176))
   if self.enemy_record['identity']<200:allowed.append((SCRATCH,SCRATCH+48))
  s=self.remaining_work
  if s and self.remaining_phase in ('prefix','animation','tail'):
   w,r=s['work_pointer'],s['record_pointer'];allowed.append((w,w+WORK_BYTES))
   if self.remaining_phase=='prefix':
    allowed.append((r,r+176))
    if not s['cache_hit']:
     p=s['cache_pointer'];allowed += [(p,p+8),(UNITCTRL+COUNTER_OFFSET,UNITCTRL+COUNTER_OFFSET+4)]
     if s['allocation']:allowed.append((self.controller,self.controller+84))
   if self.remaining_phase=='animation':
    slot=self.read(self.controller+40)
    allowed += [(self.controller,self.controller+84),(TASK+0x808E8,TASK+0x809EC),(0x7A0EBC,0x7A0FC0),
     (self.texture_table+slot*8,self.texture_table+(slot+1)*8)]
    allowed += [(a['pointer'],a['pointer']+a['bytes']) for a in self.animation_allocations if not a['freed']]
   if self.remaining_phase=='tail':
    allowed.append((UNITCTRL+SHARED_OFFSET,UNITCTRL+SHARED_OFFSET+SHARED_BYTES))
    if s['job']==406:allowed.append((self.constructor_cell,self.constructor_cell+1))
    if s['role']==406:allowed.append((r+159,r+160))
  if not any(a<=address and address+size<=b for a,b in allowed):
   raise RuntimeError(f'scene remaining finite guard {address:#x}/{size} at{uc.reg_read(UC_X86_REG_EIP):#x} phase{self.remaining_phase}')
  if not STACK<=address<STACK+0x10000:self.writes.append((address,size,value&((1<<(size*8))-1)))

 def begin_remaining_work(self,sp):
  ordinal=self.remaining_ordinal;index=249-ordinal
  if (self.uc.reg_read(UC_X86_REG_ECX),self.read(sp),self.read(sp+4))!=(UNITCTRL,0x453630,index):
   raise RuntimeError('scene remaining constructor natural input')
  record=self.finish_record();r=record['record_pointer'];w=UNITCTRL+WORK_OFFSET+index*WORK_BYTES
  raw=bytes.fromhex(record['record_hex']);role,job=struct.unpack_from('<H',raw,2)[0],struct.unpack_from('<H',raw,12)[0]
  if any(self.uc.mem_read(w,WORK_BYTES)) or job not in (452,301,316,317,337,406):raise RuntimeError('scene remaining original work/job ownership')
  group=self.read(0x61053C+job*8,'h');mode=self.read(0x61053E+job*8,'B')
  variant=0 if mode==0 else self.read(0x61053F+job*8,'b')
  _,self.unit_identity,self.unit_inputs=remaining_resource(job,variant,self.remaining_rules);self.unit_path=self.unit_identity['relative_path']
  cache=bytes(self.uc.mem_read(UNITCTRL+CACHE_OFFSET,4096))
  matches=[i for i in range(512) if cache[i*8]!=0 and struct.unpack_from('<b',cache,i*8+1)[0]==variant and struct.unpack_from('<h',cache,i*8+2)[0]==group]
  empty=[i for i in range(512) if cache[i*8]==0]
  if len(matches)>1 or not matches and not empty:raise RuntimeError('scene remaining cache ownership')
  slot=matches[0] if matches else empty[0]
  self.controller=struct.unpack_from('<I',cache,slot*8+4)[0] if matches else self.remaining_controller_cursor
  if matches and self.controller not in self.remaining_owned:raise RuntimeError('scene remaining cache hit lacks owned resource')
  template=self.enemy_inputs['templates'][ordinal]
  s={'ordinal':ordinal,'index':index,'role':role,'job':job,'category':raw[164],'record_derivation':record,
   'evidence_kind':'actual_school_scene_remaining','template_pointer':self.enemy_inputs['pointer']+ordinal*84,'template_hex':template,
   'work_pointer':w,'record_pointer':r,'before_work_hex':bytes(WORK_BYTES).hex(),'before_record_hex':raw.hex(),
   'cache_before_hex':cache.hex(),'cache_slot':slot,'cache_pointer':UNITCTRL+CACHE_OFFSET+slot*8,'cache_hit':bool(matches),
   'counter_before':self.read(UNITCTRL+COUNTER_OFFSET),'renderer':self.read(0x7A49FC),
   'classification_selector':self.read(UNITCTRL+0x2EF44,'B'),'relation_hex':bytes(self.uc.mem_read(UNITCTRL+0x115AAC,256)).hex(),
   'group':group,'mode':mode,'variant':variant,'calls':[],'clears':[],'primitives':[],'allocation':None,'resource_request':None,
   'file_event_start':len(self.file_events)}
  self.remaining_work=self.scene_work=self.current=s;self.active_index=index;self.next_controller=self.controller
  self.reset_animation();self.remaining_phase='prefix';self.scene_phase='prefix'
  excluded=[(w,w+WORK_BYTES),(r,r+176),(UNITCTRL+SHARED_OFFSET,UNITCTRL+SHARED_OFFSET+SHARED_BYTES)]
  header=self.read(UNITCTRL+0x2A308);cm=self.read(header);x,y=raw[155:157]
  if x>=64 or y>=96:raise RuntimeError('scene remaining logical coordinates')
  cell=cm+2*(y*64+x)+1
  if raw[15]==1:excluded += [(cell,cell+1),(UNITCTRL+SHARED_OFFSET,UNITCTRL+SHARED_OFFSET+SHARED_BYTES)]
  if not matches:excluded += [(s['cache_pointer'],s['cache_pointer']+8),(UNITCTRL+COUNTER_OFFSET,UNITCTRL+COUNTER_OFFSET+4),
   (self.controller,self.controller+84),(TASK+0x808E8,TASK+0x809EC),(0x7A0EBC,0x7A0FC0),
   (self.texture_table+s['counter_before']*8,self.texture_table+(s['counter_before']+1)*8),
   (self.remaining_animation_cursor,REMAINING_ANIM+REMAINING_ANIM_BYTES)]
  s['retained_before']=self.capture_scene_memory(excluded)

 def enter_remaining_tail(self):
  s=self.remaining_work
  if self.handles or self.read(self.controller+64)!=1 or self.uc.reg_read(UC_X86_REG_EAX)!=s['cache_pointer']:
   raise RuntimeError('scene remaining native resource/cache result')
  if not s['cache_hit']:
   if len(self.animation_entries)!=self.unit_inputs['count'] or self.animation_vector['native_constructors_completed']!=self.unit_inputs['count']:
    raise RuntimeError('scene remaining incomplete archive')
   for e in self.animation_entries:e['raw_record_hex']=bytes(self.uc.mem_read(e['record_pointer'],84)).hex()
   animation={'controller':self.controller,'before_controller_hex':s['before_controller_hex'],
    'controller_hex':bytes(self.uc.mem_read(self.controller,84)).hex(),'metadata_pointer':self.read(self.controller),
    'metadata_hex':bytes(self.uc.mem_read(self.read(self.controller),self.unit_inputs['metadata_bytes'])).hex(),
    'texture_slot':self.read(self.controller+40),'texture_table':self.texture_table,'request':deepcopy(self.animation_request),
    'entries':deepcopy(self.animation_entries),'allocations':deepcopy(self.animation_allocations),'binding':deepcopy(self.animation_binding),
    'vector':deepcopy(self.animation_vector),'boundaries':deepcopy(self.animation_boundaries),'file_release':deepcopy(self.animation_file_release)}
   self.remaining_owned[self.controller]=deepcopy(animation)
  else:animation=None
  snap=self._prepare_scene_constructor()
  snap['relation_selector']=s['classification_selector'];snap['relation_hex']=s['relation_hex']
  s.update({'prefix_work_hex':snap['before_work_hex'],'prefix_record_hex':snap['record_hex'],
   'cache_after_hex':bytes(self.uc.mem_read(UNITCTRL+CACHE_OFFSET,4096)).hex(),'counter_after':self.read(UNITCTRL+COUNTER_OFFSET),
   'controller':self.controller,'animation':animation,'tail':snap})
  s['tail_retained']=self.capture_scene_memory([(snap['work_pointer'],snap['work_pointer']+WORK_BYTES),
   (UNITCTRL+SHARED_OFFSET,UNITCTRL+SHARED_OFFSET+SHARED_BYTES),*([(self.constructor_cell,self.constructor_cell+1)] if s['job']==406 else []),
   *([(s['record_pointer']+159,s['record_pointer']+160)] if s['role']==406 else [])])
  self.remaining_phase=self.scene_phase='tail';self.scene_complete_loading=True

 def finish_remaining_work(self):
  s=self.remaining_work;t=s['tail']
  if self.uc.reg_read(UC_X86_REG_ESP)!=self.constructor_return_sp or self.uc.reg_read(UC_X86_REG_EAX)!=0:
   raise RuntimeError('scene remaining natural return/stack')
  preservation=self.verify_scene_memory(s.pop('retained_before'))
  tail_preservation=self.verify_scene_memory(s.pop('tail_retained'))
  after=bytes(self.uc.mem_read(self.constructor_cm,12288));prior=bytearray.fromhex(t['before_cm_hex'])
  at=self.constructor_cell-self.constructor_cm
  if s['job']==406:prior[at]=(prior[at]+1)&255
  if after!=bytes(prior):raise RuntimeError('scene remaining exact map cell accounting')
  t.update({'before_record_hex':t['record_hex'],'record_hex':bytes(self.uc.mem_read(t['record_pointer'],176)).hex(),
   'work_hex':bytes(self.uc.mem_read(t['work_pointer'],WORK_BYTES)).hex(),
   'shared_hex':bytes(self.uc.mem_read(t['shared_pointer'],SHARED_BYTES)).hex(),'cm_hex':after.hex(),
   'cm_sha256':hashlib.sha256(after).hexdigest(),'calls':deepcopy(self.constructor_calls),'clears':deepcopy(self.constructor_clears),
   'return_va':'0x453630','return_eax':0,'constructor_completed':True,'scene_placement_executed':False,'scene_vm_executed':False,
   **tail_preservation})
  s.update({'file_events':deepcopy(self.file_events[s.pop('file_event_start'):]),'coverage':self.coverage(),**preservation})
  if s['cache_hit'] and (s['file_events'] or s['allocation'] or s['cache_before_hex']!=s['cache_after_hex'] or s['counter_before']!=s['counter_after']):
   raise RuntimeError('scene remaining cache hit performed new resource/cache work')
  self.remaining_units.append(deepcopy(s));self.remaining_work=self.current=None;self.scene_complete_loading=False
  self.remaining_phase='loop';self.remaining_ordinal+=1
  

 def _hook(self,uc,address,size,context):
  if not self.remaining_loading:return super()._hook(uc,address,size,context)
  sp,recv=uc.reg_read(UC_X86_REG_ESP),uc.reg_read(UC_X86_REG_ECX)
  if self.remaining_phase=='tail':
   if address==0x453630:self.finish_remaining_work();return
   return self._scene_tail_hook(uc,address,size,context)
  if self.remaining_phase in ('prefix','animation'):
   if address==0x467147:self.enter_remaining_tail();self.visited.add(address);return
   if self.remaining_phase=='animation':return self._animation_hook(uc,address,size,context)
   if address==0x4500B0:
    s=self.remaining_work
    if s['cache_hit'] or not s['allocation']:raise RuntimeError('scene remaining cached resource request')
    s['before_controller_hex']=bytes(uc.mem_read(self.controller,84)).hex()
    slot=self.read(self.controller+40)
    if slot!=s['counter_before'] or any(uc.mem_read(self.texture_table+slot*8,8)):raise RuntimeError('scene remaining source empty slot')
    s['resource_request']={'relative_path':self.unit_path,'args':[self.read(sp+4+i*4) for i in range(4)]}
    self.remaining_phase=self.scene_phase='animation'
    return self._animation_hook(uc,address,size,context)
   return self._remaining_prefix_hook(uc,address,size,context)
  if address==0x45363D:
   if self.remaining_phase!='loop' or self.remaining_ordinal!=35:raise RuntimeError('scene remaining loop exit before all constructors')
   self.stop_reason='after_all_scene_constructors_and_progress';self.visited.add(address);uc.emu_stop();return
  if address==0x4680B0:self.begin_remaining_work(sp);self.visited.add(address);return
  if address==0x451D80:
   if self.remaining_phase!='loop' or (recv,self.read(sp))!=(TACT,0x453638):raise RuntimeError('scene remaining progress input')
   self.remaining_progress.append({'ordinal_completed':self.remaining_ordinal-1,'before_hex':bytes(uc.mem_read(TACT+64,2)).hex(),'primitives':[]})
   self.visited.add(address);return
  if address in (0x451E20,0x415420,0x422360):
   expected={0x451E20:(TACT,0x451DF1,0),0x415420:(TASK,0x451DFC,0),0x422360:(TACT,0x451E06,4)}
   receiver,caller,pop=expected[address]
   if (recv,self.read(sp))!=(receiver,caller) or pop and self.read(sp+4)!=0:raise RuntimeError('scene remaining progress primitive')
   if address==0x451E20:self.remaining_progress[-1]['after_hex']=bytes(uc.mem_read(TACT+64,2)).hex()
   self.remaining_progress[-1]['primitives'].append({'va':hex(address),'receiver':recv,'caller_return_va':hex(caller)})
   self._stub_return(0,pop);return
  if 0x451D80<=address<0x451E19:self.visited.add(address);return
  if address==0x4DA450:self.enemy_ordinal=self.remaining_ordinal;self.enemy_mode='actual_school';self.enemy_loading=True;self.remaining_phase='record'
  if self.remaining_phase=='record':return SchoolEnemyRecordsEmulator._hook(self,uc,address,size,context)
  if address in self.enemy_code:self.visited.add(address);return
  if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
  raise RuntimeError(f'undeclared scene remaining code{address:#x}')

 def run_remaining(self):
  previous_next_controller=self.next_controller
  self.reset_remaining();self.remaining_loading=True;self.clear_trace('tactical_startup');self.stop_reason=None
  try:
   for remaining in range(32):
    self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30000000,count=2000000)
    if self.stop_reason=='first_unit_texture_vector':
     target,stride,count,ctor=self.vector_pending;cpu=self.uc.context_save();stack=bytes(self.uc.mem_read(STACK,65536))
     for i in range(count):self.call(ctor,receiver=target+i*stride);self.animation_vector['native_constructors_completed']+=1
     self.uc.mem_write(STACK,stack);self.uc.context_restore(cpu);self._stub_return(0,20);self.stop_reason=None
    elif self.stop_reason=='after_all_scene_constructors_and_progress':break
    elif self.stop_reason is not None:raise RuntimeError('scene remaining unexpected stop')
   else:raise RuntimeError('scene remaining finite instruction budget exhausted')
   if self.handles or [s['ordinal'] for s in self.remaining_units]!=list(ORDINALS):raise RuntimeError('scene remaining incomplete')
   return {'units':deepcopy(self.remaining_units),'progress':deepcopy(self.remaining_progress),'count':25,
    'cache_hits':sum(s['cache_hit'] for s in self.remaining_units),'new_resources':len(self.remaining_owned),
    'constructors_completed_total':35,'remaining_templates':0,'stop_reason':self.stop_reason,
    'scene_placement_executed':False,'scene_vm_executed':False}
  finally:
   self.remaining_loading=False;self.enemy_loading=False;self.scene_complete_loading=False
   self.next_controller=previous_next_controller

 def resources(self,name,commands=()):
  self.remaining_loading=False;result=super().resources(name,commands)
  result.update({'scene_remaining_completed':False,'scene_remaining':None})
  if result['ready']:
   result['scene_remaining']=self.run_remaining();result['scene_remaining_completed']=True
   result['stop_reason']=self.stop_reason;result['file_events']=deepcopy(self.file_events)
  return result
 def animation_allocate(self,count,kind,caller):
     if not self.remaining_loading:return super().animation_allocate(count,kind,caller)
     at,end = self.remaining_animation_cursor,self.remaining_animation_cursor+((count+15)&~15)
     if self.remaining_phase!='animation' or count<=0 or end>REMAINING_ANIM+REMAINING_ANIM_BYTES:raise RuntimeError('scene remaining finite animation allocation')
     self.remaining_animation_cursor = end
     a = {'pointer':at,'bytes':count,'kind':kind,'caller_return_va':hex(caller),'freed':False,'index':self.active_index}
     self.animation_allocations.append(a)
     return at

 def _file_api(self,address,sp):
     if not self.remaining_loading:return super()._file_api(address,sp)
     if self.remaining_phase!='animation':raise RuntimeError('current file API outside resource phase')
     _,(name,pop) = list(FILE_IMPORTS.items())[(address-FILE_API)//16]
     if name=='CreateFileA':
         args = [self.read(sp+4+i*4) for i in range(7)]
         if cstring(self,args[0])!=self.unit_path or args[1:]!=[0x80000000,1,0,3,1,0] or self.handles:
             raise RuntimeError('scene remaining exact read-only file arguments')
         raw,identity,_ = remaining_resource(self.current['job'],self.current['variant'],self.remaining_rules)
         handle = 0xD00+self.active_index
         self.handles[handle] = {'raw':raw,'identity':identity};self.file_events.append({'name':name,'args':args,'result':handle})
         self._stub_return(handle,pop);return
     if name=='ReadFile':
         handle,target,count,written,overlapped = [self.read(sp+4+i*4) for i in range(5)]
         owned = [a for a in self.animation_allocations if a['kind']=='unit_file_buffer' and not a['freed']]
         if handle not in self.handles or overlapped or len(owned)!=1 or (target,count)!=(owned[0]['pointer'],self.unit_identity['bytes']):
             raise RuntimeError('scene remaining exact file read ownership')
         self.primitive_write(target,self.handles[handle]['raw']);self.primitive_write(written,struct.pack('<I',count))
         self.animation_request.update({'buffer_pointer':target,'loaded_bytes':count,'loaded_sha256':hashlib.sha256(bytes(self.uc.mem_read(target,count))).hexdigest(),'loaded':True})
         self.file_events.append({'name':name,'args':[handle,target,count,written,overlapped],'result':1});self._stub_return(1,pop);return
     return SchoolTacticalResourcesEmulator._file_api(self,address,sp)

 def _animation_hook(self,uc,address,size,context):
     if not self.remaining_loading:return super()._animation_hook(uc,address,size,context)
     if address in self.animation_code:
         self.visited.add(address)
         return
     sp,receiver = uc.reg_read(UC_X86_REG_ESP),uc.reg_read(UC_X86_REG_ECX)
     if address in (0x424F80,0x41EFD0):
         raise RuntimeError(f'unexpected scene remaining animation assertion/dynamic slot at {address:#x}')
     if FILE_API<=address<FILE_API+len(FILE_IMPORTS)*16 and (address-FILE_API)%16==0:
         return self._file_api(address,sp)
     if address==0x4500B0:
         args = [self.read(sp+4+i*4) for i in range(4)]
         if self.animation_request or self.read(sp)!=0x464F1F or receiver!=TASK+0x80000 \
             or cstring(self,args[0])!=self.unit_path or args[1:]!=[self.current['variant'],int(self.current['variant']!=0),0]:
             raise RuntimeError('scene remaining animation source file request')
         _,identity,_ = remaining_resource(self.current['job'],self.current['variant'],self.remaining_rules)
         self.animation_request = {'receiver':receiver,'args':args,'source':identity,
                                   'caller_return_va':hex(self.read(sp)),'loaded':False}
         self.visited.add(address)
         return
     if address==0x4142B0:
         if receiver!=TASK or self.read(sp)!=0x464F2F:
             raise RuntimeError('scene remaining animation renderer device query')
         self.visited.add(address)
         return
     if address==0x428A40:
         count,caller = self.read(sp+4),self.read(sp)
         if caller==0x42AD54 and self.handles and count==len(next(iter(self.handles.values()))['raw']):
             kind = 'unit_file_buffer'
         elif caller==0x409C53 and count==self.unit_inputs['metadata_bytes']:
             kind = 'unit_metadata'
         elif caller==0x41F142 and count==self.unit_inputs['count']*84+4:
             kind = 'unit_texture_array'
         else:
             raise RuntimeError(f'scene remaining animation allocation caller/count {caller:#x}/{count}')
         self._stub_return(self.animation_allocate(count,kind,caller),0)
         return
     if address==0x56D810:
         target,fmt,left = [self.read(sp+i) for i in (4,8,12)]
         format_text = cstring(self,fmt)
         if format_text=='%s%s' and target==TASK+0x808E8 and self.read(sp)==0x4500EF:
             value = cstring(self,left)+cstring(self,self.read(sp+16))
         elif format_text=='%s' and target==0x7A0EBC and self.read(sp)==0x42ACB9:
             value = cstring(self,left)
         else:
             raise RuntimeError('scene remaining animation exact source path formatting')
         if value!=self.unit_path:
             raise RuntimeError('scene remaining animation formatted source path')
         self.primitive_write(target,value.encode('ascii')+b'\0')
         self._stub_return(len(value),0)
         return
     if address==0x56D4D0:
         target,source,count = [self.read(sp+i) for i in (4,8,12)]
         owned = {a['kind']:a for a in self.animation_allocations}
         if (target,source,count,self.read(sp))!=(owned['unit_metadata']['pointer'],owned['unit_file_buffer']['pointer'],self.unit_inputs['metadata_bytes'],0x409C84):
             raise RuntimeError('scene remaining animation metadata copy ownership')
         self.primitive_write(target,bytes(uc.mem_read(source,count)))
         self._stub_return(target,0)
         return
     if address==0x41EC40:
         args = [self.read(sp+4+i*4) for i in range(7)]
         file = next(a['pointer'] for a in self.animation_allocations if a['kind']=='unit_file_buffer')
         metadata = next(a['pointer'] for a in self.animation_allocations if a['kind']=='unit_metadata')
         if receiver!=self.controller+0x18 or args!=[0,self.texture_table,metadata+self.unit_inputs['offsets'][5],file+self.unit_inputs['metadata_bytes'],0,file+self.unit_inputs['palette_offset'] if self.current['variant'] else 0,file+self.unit_inputs['offsets'][8] if self.current['variant'] else 0]:
             raise RuntimeError(f'scene remaining animation palette/mask binding {args}')
         self.animation_binding = {'receiver':receiver,'args':args,'caller_return_va':hex(self.read(sp))}
         self.visited.add(address)
         return
     if address==0x56DDA0:
         args = tuple(self.read(sp+i) for i in (4,8,12,16,20))
         a = self.animation_allocations[-1]
         if a['kind']!='unit_texture_array' or args!=(a['pointer']+4,84,self.unit_inputs['count'],0x41F830,0x41F890):
             raise RuntimeError('scene remaining animation bounded texture vector')
         self.vector_pending = args[:4]
         self.animation_vector = {'target':args[0],'stride':args[1],'count':args[2],
             'constructor_va':hex(args[3]),'destructor_va':hex(args[4]),
             'native_constructors_completed':0,'iteration_outside_instruction_hook':True}
         self.stop_reason = 'first_unit_texture_vector'
         uc.emu_stop()
         return
     if address==0x56CEC0:
         target,byte,count = [self.read(sp+i) for i in (4,8,12)]
         a = next((a for a in self.animation_allocations if a['kind']=='unit_texture_array'),None)
         if not a or byte!=0 or count!=4 or self.read(sp)!=0x41F9BE \
             or not a['pointer']+4+0x24<=target<=a['pointer']+a['bytes']-4 or (target-a['pointer']-4-0x24)%84:
             raise RuntimeError('scene remaining animation exact texture clear primitive')
         self.primitive_write(target,bytes(count))
         self._stub_return(target,0)
         return
     if address==0x41F340:
         device,buffer,index,records,left,right = [self.read(sp+i) for i in (4,8,12,16,20,24)]
         owned = {a['kind']:a for a in self.animation_allocations}
         base = owned['unit_file_buffer']['pointer']
         selected = base+self.unit_inputs['palette_offset'] if self.current['variant'] and self.read(base+self.unit_inputs['offsets'][8]+index,'B')==0 else 0
         if device!=0 or buffer!=base+self.unit_inputs['metadata_bytes'] or index!=len(self.animation_entries) or index>=self.unit_inputs['count'] \
             or records!=owned['unit_texture_array']['pointer']+4 or (left,right)!=(0,selected):
             raise RuntimeError('scene remaining animation texture source/order/palette mask')
         offset = self.read(buffer+8+index*4)
         end = self.read(buffer+8+(index+1)*4) if index<self.unit_inputs['count']-1 else self.read(buffer)
         if not (8+4*self.unit_inputs['count'])<=offset<end<=self.unit_inputs['image_bytes']:
             raise RuntimeError('scene remaining animation texture entry bounds')
         self.active_texture = {'index':index,'offset':offset,'file_offset':self.unit_inputs['metadata_bytes']+offset,
             'bytes':end-offset,'header_hex':bytes(uc.mem_read(buffer+offset,16)).hex(),
             'record_pointer':records+index*84,'palette_pointer':selected,
             'mask_value':self.read(base+self.unit_inputs['offsets'][8]+index,'B')}
         self.animation_entries.append(self.active_texture)
         self.visited.add(address)
         return
     if address==0x403BD0:
         if not self.animation_entries or receiver!=self.active_texture['record_pointer'] or [self.read(sp+4),self.read(sp+8)]!=[0,0]:
             raise RuntimeError('scene remaining animation exact GPU creation boundary')
         self.animation_boundaries.append({'kind':'texture_creation','index':self.active_texture['index'],
             'width':self.read(receiver+0x38,'H'),'height':self.read(receiver+0x3A,'H'),'format':self.read(receiver+0x34)})
         self._stub_return(0,8)
         return
     if address==0x404150:
         args = [self.read(sp+4+i*4) for i in range(4)]
         if not self.animation_entries or receiver!=self.active_texture['record_pointer'] \
             or args!=[self.animation_request['buffer_pointer']+self.active_texture['file_offset'],1,0,self.active_texture['palette_pointer']]:
             raise RuntimeError(f'scene remaining animation exact GPU pixel/palette upload boundary: {receiver:#x} {args} entry {self.active_texture}')
         bmp = args[0]
         body = self.read(bmp+10)
         w,h = self.read(bmp+18),self.read(bmp+22)
         palette = args[3] or bmp+54
         self.active_texture.update({'pixel_sha256':hashlib.sha256(bytes(uc.mem_read(bmp+body,((w+3)&~3)*h))).hexdigest(),
             'upload_palette_pointer':palette,'upload_palette_hex':bytes(uc.mem_read(palette,1024)).hex(),
             'upload_palette_sha256':hashlib.sha256(bytes(uc.mem_read(palette,1024))).hexdigest()})
         self.animation_boundaries.append({'kind':'pixel_upload','index':self.active_texture['index'],'args':args,
             'palette_sha256':self.active_texture['upload_palette_sha256'],'pixel_sha256':self.active_texture['pixel_sha256']})
         self._stub_return(0,16)
         return
     if address==0x428AD0:
         pointer = self.read(sp+4)
         owned = next((a for a in self.animation_allocations if a['pointer']==pointer and not a['freed']),None)
         if not owned or owned['kind']!='unit_file_buffer' or self.read(sp)!=0x409E5D or len(self.animation_entries)!=self.unit_inputs['count']:
             raise RuntimeError('scene remaining animation source release ownership/order')
         self.animation_file_release = {'pointer':pointer,'bytes':owned['bytes'],'caller_return_va':hex(self.read(sp)),
             'sha256_at_release':hashlib.sha256(bytes(uc.mem_read(pointer,owned['bytes']))).hexdigest()}
         owned['freed'] = True
         self.animation_boundaries.append({'kind':'source_file_release',**self.animation_file_release})
         self._stub_return(0,0)
         return
     return ExitEmulator._hook(self,uc,address,size,context)

 def _remaining_prefix_hook(self, uc, address, size, context):
     s = self.scene_work
     sp = uc.reg_read(UC_X86_REG_ESP)
     recv = uc.reg_read(UC_X86_REG_ECX)
     if address == 4620464:
         caller = 4535856 if s['evidence_kind'] == 'actual_school_scene_remaining' else RETURN
         if (recv, self.read(sp), self.read(sp + 4)) != (UNITCTRL, caller, s['index']):
             raise RuntimeError('scene prefix natural constructor input')
         s['constructor_entry'] = {'receiver': recv, 'caller_return_va': hex(self.read(sp)), 'index': self.read(sp + 4)}
     if address == 5089040:
         args = [self.read(sp + 4), self.read(sp + 8)]
         if args != [s['template_pointer'], s['work_pointer']] or self.read(sp) != 4673825:
             raise RuntimeError('scene prefix exact status overlay')
         s['calls'].append({'va': hex(address), 'args': args, 'caller_return_va': hex(self.read(sp))})
     if address == 5689024:
         (target, byte, count) = [self.read(sp + i) for i in (4, 8, 12)]
         allowed = [(s['work_pointer'], WORK_BYTES, 4620634), (s['work_pointer'] + 656, 92, 4673509)]
         if byte or (target, count, self.read(sp)) not in allowed:
             raise RuntimeError('scene prefix exact clear')
         self.primitive_write(target, bytes(count))
         s['clears'].append({'pointer': target, 'bytes': count, 'caller_return_va': hex(self.read(sp))})
         self._stub_return(target, 0)
         return
     if address == 4360768:
         if s['allocation'] or (self.read(sp + 4), self.read(sp)) != (84, 4615096) or any(uc.mem_read(self.next_controller, 84)):
             raise RuntimeError('scene prefix exact controller allocation')
         s['allocation'] = {'pointer': self.next_controller, 'bytes': 84, 'freed': False, 'caller_return_va': hex(self.read(sp))}
         s['primitives'].append({'kind': 'heap_allocation', **s['allocation']})
         self.remaining_controller_cursor += 96
         if self.remaining_controller_cursor>REMAINING_CONTROLLERS+REMAINING_CONTROLLER_BYTES:raise RuntimeError('scene remaining controller pool exhausted')
         self._stub_return(self.next_controller, 0)
         return
     if address == 4371152:
         args = [self.read(sp + i) for i in (8, 12, 16)]
         if self.read(sp) != 4616500 or cstring(self, self.read(sp + 4)) != 'char:%03d, job:%03d : palette:%03d\n' or args != [s['role'], s['job'], s['variant'] - 1]:
             raise RuntimeError('scene prefix exact debug output')
         s['primitives'].append({'kind': 'debug_log', 'args': args})
         self._stub_return(0, 0)
         return
     if address == 4615296:
         args = [self.read(sp + i) for i in (4, 8, 12)]
         if recv != UNITCTRL or args != [s['cache_pointer'], s['group'], s['variant']]:
             raise RuntimeError('scene prefix exact cache binding')
         s['calls'].append({'va': hex(address), 'receiver': recv, 'args': args})
     if address == 4607344:
         if recv != self.next_controller or [self.read(sp + 4), self.read(sp + 8)] != [s['renderer'], s['group'] + 8]:
             raise RuntimeError('scene prefix source animation binding')
     if address == 4522160:
         args = [self.read(sp + 4 + i * 4) for i in range(4)]
         expected = [self.read(6358328 + s['group'] * 8), s['variant'], int(s['variant'] != 0), 0]
         if recv != s['renderer'] + 524288 or self.read(sp) != 4607775 or args != expected or s['resource_request']:
             raise RuntimeError('scene prefix exact source animation request')
         s['resource_request'] = {'receiver': recv, 'caller_return_va': hex(self.read(sp)), 'args': args, 'relative_path': cstring(self, args[0]), 'loaded': False}
         self.stop_reason = 'before_second_scene_unit_animation_load'
         uc.emu_stop()
         return
     if address in self.scene_work_code:
         self.visited.add(address)
         return
     if address == 5688960:
         return ExitEmulator._hook(self, uc, address, size, context)
     raise RuntimeError(f'undeclared scene prefix code {address:#x}')

def report():
 e=SchoolSceneRemainingEmulator()
 if not e.run_planning('scene_remaining_upstream')['school_data_prepared']:raise RuntimeError('school prefix missing')
 checkpoint=[(a,bytes(e.uc.mem_read(a,b-a+1))) for a,b,_ in e.uc.mem_regions()];cpu=e.uc.context_save();cases=[]
 for name,commands in [('initial',()),('student9_waiting',[('student',9,-1)]),
  ('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1),('student',9,-1)]),
  ('teacher_only',[('student',3,-1),('student',4,-1),('student',9,-1)]),('teacher_waiting',[('teacher',101,-1)])]:
  for at,raw in checkpoint:e.uc.mem_write(at,raw)
  e.uc.context_restore(cpu);e.remaining_loading=False;e.stop_reason=None
  cases.append(e.resources(name,commands));print('Actual scene remaining '+name+': '+str(cases[-1]['scene_remaining_completed']),flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
  'boundary':'Actual scene ordinals10–34 complete and final progress; total35/35. Deployment and VM unexecuted; GPU declared.',**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use a new immutable evidence path')
 path.write_text(report_text(report()),encoding='utf-8',newline='\n')
