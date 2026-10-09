"""Natural current-school scene texture/minimap/pathfinding initialization.

GPU and embedded graphics bootstrap remain declared external boundaries.
Stops before the following unit-art reset, without fabricating VM/placements.
"""
import argparse
from copy import deepcopy
import hashlib
import struct
from unicorn.x86_const import UC_X86_REG_ECX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_unitctrl_map_emulation import (SchoolUnitCtrlMapEmulator, map_resource,
    MAP_GRAPHICS,UHEAP,UHEAP_SIZE,UNITCTRL)
from tools.school_tactical_resources_emulation import FILE_API,FILE_IMPORTS,POOL,POOL_SIZE
from tools.school_tactical_startup_emulation import TACT,TACT_SIZE,SCRIPT_WORK,cstring
from tools.school_adventure_handoff_emulation import GROUP_TASK
from tools.school_combat_records_emulation import CHAR_BASE,UNITS
from tools.school_course_unlock_emulation import AUTHORITY
from tools.tactics_exit_emulation import ROOT,SOURCE,SOURCE_SHA256,BASE,TASK,STACK,RETURN,report_text

SCENE_POOL,SCENE_POOL_SIZE=0xF100000,0x900000
SCENE_NAMES=(MAP_GRAPHICS,'data\\tactics\\map\\map05.bmp','data\\tactics\\map\\map05.vpt')
NATIVE=((0x44E440,0x44E4C0),(0x44E4C0,0x44E5D0),(0x44E5D0,0x44E64C),
 (0x4404A0,0x4406E7),(0x440A10,0x440AEE),(0x440AF0,0x440C0A),(0x440C10,0x440D31),
 (0x43D1A0,0x43D1CD),(0x43D200,0x43D22D),(0x4142B0,0x4142DD),
 (0x42AE70,0x42AEBD),(0x404870,0x4048C2),(0x404B40,0x404B8A),(0x404B90,0x404C16),
 (0x4077C0,0x407823),(0x56CFCC,0x56CFF3))
CODE=frozenset(a for start,end in NATIVE for a in range(start,end))


class SchoolSceneResourcesEmulator(SchoolUnitCtrlMapEmulator):
    def __init__(self):
        self.scene_loading=False
        super().__init__();self._function_ranges+=NATIVE
        self.uc.mem_map(SCENE_POOL,SCENE_POOL_SIZE);self.reset_scene()

    def reset_scene(self):
        self.scene_requests=[];self.scene_allocations=[];self.scene_cursor=SCENE_POOL
        self.scene_boundaries=[];self.lock_buffer=None;self.scene_graphics_input=None;self.pathctrl=None

    def _write_hook(self,uc,access,address,size,value,context):
        if not getattr(self,'scene_loading',False):return super()._write_hook(uc,access,address,size,value,context)
        if STACK<=address and address+size<=STACK+0x10000:return
        allowed=[(0,4),(TACT,TACT+TACT_SIZE),(0x7A0EBC,0x7A0FC0),
            (TASK+0x808E8,TASK+0x809EC),(self.texture_table+92*8,self.texture_table+93*8)]
        allowed += [(a['pointer'],a['pointer']+a['bytes']) for a in self.scene_allocations if not a['freed']]
        if not any(a<=address and address+size<=b for a,b in allowed):
            raise RuntimeError(f'scene finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        self.writes.append((address,size,value & ((1<<(size*8))-1)));self.startup_writes.append((address,size))

    def scene_allocate(self,count,kind,caller):
        if count<=0:raise RuntimeError('empty scene allocation')
        pointer=self.scene_cursor;next_pointer=pointer+((count+15)&~15)
        if next_pointer>SCENE_POOL+SCENE_POOL_SIZE:raise RuntimeError('scene allocation bounds')
        self.scene_cursor=next_pointer
        self.scene_allocations.append({'pointer':pointer,'bytes':count,'kind':kind,
            'caller_return_va':hex(caller),'freed':False})
        return pointer

    def _file_api(self,address,sp):
        index=(address-FILE_API)//16;slot,(name,pop)=list(FILE_IMPORTS.items())[index]
        if self.scene_loading and name=='CreateFileA':
            args=[self.read(sp+4+i*4) for i in range(7)];relative=cstring(self,args[0])
            if relative!=SCENE_NAMES[len(self.scene_requests)-1] or args[1:]!=[0x80000000,1,0,3,1,0]:
                raise RuntimeError('scene read-only file arguments')
            raw,identity=map_resource(relative.rsplit('\\',1)[-1]);handle=0x900+len(self.scene_requests)
            self.handles[handle]={'raw':raw,'identity':identity}
            self.file_events.append({'name':name,'import_va':hex(slot),'args':args,'result':handle})
            self._stub_return(handle,pop);return
        if self.scene_loading and name=='ReadFile':
            handle,target,count,written,overlapped=[self.read(sp+4+i*4) for i in range(5)]
            if handle not in self.handles or overlapped!=0:raise RuntimeError('scene read handle')
            raw=self.handles[handle]['raw']
            if count!=len(raw) or self.scene_allocations[-1]['pointer']!=target:raise RuntimeError('scene read length/allocation')
            self.primitive_write(target,raw);self.primitive_write(written,struct.pack('<I',len(raw)))
            self.scene_requests[-1].update({'buffer_pointer':target,'loaded_bytes':len(raw),'loaded_sha256':hashlib.sha256(raw).hexdigest()})
            self.file_events.append({'name':name,'import_va':hex(slot),'args':[handle,target,count,written,overlapped],'result':1})
            self._stub_return(1,pop);return
        return super()._file_api(address,sp)

    def _hook(self,uc,address,size,context):
        if not getattr(self,'scene_loading',False):return super()._hook(uc,address,size,context)
        if address in CODE and address!=0x44E4C0:
            self.visited.add(address);return
        sp=uc.reg_read(UC_X86_REG_ESP);receiver=uc.reg_read(UC_X86_REG_ECX)
        if address==0x44E4C0:self.pathctrl=receiver
        if address==0x467EB0:
            self.stop_reason='before_unit_art_reset';uc.emu_stop();return
        if address==0x4500B0:
            name=cstring(self,self.read(sp+4))
            if len(self.scene_requests)>=3 or name!=SCENE_NAMES[len(self.scene_requests)] or receiver!=TASK+0x80000:
                raise RuntimeError('natural scene resource order/receiver')
            raw,identity=map_resource(name.rsplit('\\',1)[-1]);offset=0x404 if name==MAP_GRAPHICS else 0
            count=self.read_container_count(raw[offset:]) if name!=SCENE_NAMES[1] else 0
            entry={'source':{'relative_path':name,**identity},'entry_count':count,
                'container_file_offset':offset,'caller_return_va':hex(self.read(sp))}
            self.scene_requests.append(entry);self.requests.append(entry);self.visited.add(address);return
        if address==0x56D810 and cstring(self,self.read(sp+8))=='%s%s' and STACK<=self.read(sp+4)<STACK+0xFF00:
            target,left,right=[self.read(sp+i) for i in (4,12,16)]
            value=(cstring(self,left)+cstring(self,right)).encode('ascii')
            if value.decode() not in SCENE_NAMES:raise RuntimeError('scene formatter inputs')
            self.primitive_write(target,value+b'\0');self._stub_return(len(value),0);return
        if address==0x428A40:
            count,caller=self.read(sp+4),self.read(sp)
            if caller==0x42AD54:
                if len(self.handles)!=1 or count!=len(next(iter(self.handles.values()))['raw']):raise RuntimeError('scene file allocation size')
                kind='file_buffer'
            elif caller==0x41F142 and count==48*84+4 and self.scene_requests[-1]['source']['relative_path']==MAP_GRAPHICS:kind='texture_array'
            elif caller==0x4405C1 and count==172*128*2:kind='fog_buffer'
            else:raise RuntimeError(f'scene allocation caller/count {caller:#x}/{count}')
            self._stub_return(self.scene_allocate(count,kind,caller),0);return
        if address==0x428AD0:
            pointer=self.read(sp+4);match=[a for a in self.scene_allocations if a['pointer']==pointer and not a['freed']]
            if len(match)!=1 or match[0]['kind']!='file_buffer':raise RuntimeError('scene free ownership')
            match[0]['freed']=True;self._stub_return(0,0);return
        if address==0x56DDA0:
            args=tuple(self.read(sp+i) for i in (4,8,12,16,20));a=self.scene_allocations[-1]
            if a['kind']!='texture_array' or args!=(a['pointer']+4,84,48,0x41F830,0x41F890):raise RuntimeError('scene texture vector')
            self.vector_pending=args[:4];self.stop_reason='scene_texture_vector';uc.emu_stop();return
        if address==0x56CEC0:
            target,byte,count=[self.read(sp+i) for i in (4,8,12)]
            if byte!=0 or count!=4:raise RuntimeError('scene clear primitive bounds')
            self.primitive_write(target,bytes(count));self._stub_return(target,0);return
        if address==0x56D4D0:
            target,source,count=[self.read(sp+i) for i in (4,8,12)]
            if self.lock_buffer is None or count!=344 or not self.read(self.mapctrl+0x2658C)<=source<self.read(self.mapctrl+0x2658C)+44032:
                raise RuntimeError('fog upload memcpy source/count')
            self.primitive_write(target,bytes(uc.mem_read(source,count)));self._stub_return(target,0);return
        if address==0x41F340:
            _,buffer,index,record,_,_=[self.read(sp+i) for i in (4,8,12,16,20,24)];request=self.scene_requests[-1]
            if request['source']['relative_path']!=MAP_GRAPHICS or buffer!=request['buffer_pointer']+0x404 \
                or index!=sum(e['resource']==len(self.requests)-1 for e in self.texture_entries):raise RuntimeError('map texture container/index')
            offset=self.read(buffer+8+index*4);end=self.read(buffer+8+(index+1)*4) if index<47 else request['loaded_bytes']-0x404
            self.active_texture={'resource':len(self.requests)-1,'index':index,'offset':offset,'file_offset':offset+0x404,
                'bytes':end-offset,'header_hex':bytes(uc.mem_read(buffer+offset,16)).hex(),'record_pointer':record+index*84}
            self.texture_entries.append(self.active_texture);self.visited.add(address);return
        if address==0x4048D0:
            request=self.scene_requests[-1]
            if request['source']['relative_path']!=SCENE_NAMES[1] or self.read(sp+12)!=request['buffer_pointer']:
                raise RuntimeError('minimap bitmap source')
            self.active_texture={'resource':len(self.requests)-1,'index':0,'offset':0,'file_offset':0,
                'bytes':request['loaded_bytes'],'header_hex':bytes(uc.mem_read(request['buffer_pointer'],16)).hex(),'record_pointer':receiver}
            self.texture_entries.append(self.active_texture)
        if address in (0x403BD0,0x404150,0x403910,0x403990) and receiver==self.mapctrl+0x2650C:
            if address==0x403BD0:
                self.scene_boundaries.append({'kind':'fog_texture_creation','receiver':hex(receiver),
                    'width':self.read(receiver+0x38,'H'),'height':self.read(receiver+0x3A,'H'),'format':self.read(receiver+0x34)})
                self._stub_return(0,8);return
            if address==0x403910:
                if self.lock_buffer is not None:raise RuntimeError('duplicate fog lock')
                self.lock_buffer=self.scene_allocate(44032,'GPU_lock_staging',0x403910)
                self.primitive_write(self.read(sp+4),struct.pack('<II',344,self.lock_buffer))
                self.scene_boundaries.append({'kind':'fog_GPU_lock','pitch':344,'pointer':self.lock_buffer});self._stub_return(0,4);return
            if address==0x403990:
                self.scene_boundaries.append({'kind':'fog_GPU_unlock','sha256':hashlib.sha256(bytes(uc.mem_read(self.lock_buffer,44032))).hexdigest()})
                self._stub_return(0,0);return
            raise RuntimeError('unexpected fog bitmap upload')
        if address in (0x407780,0x4077C0):
            if address==0x407780:
                self.scene_boundaries.append({'kind':'graphics_cleanup','receiver':hex(receiver)})
                self._stub_return(0,0);return
            # Simple source renderer-binding body executes below.
        if address in CODE or any(a<=address<b for a,b in self.map_native):self.visited.add(address);return
        return super()._hook(uc,address,size,context)

    def bind_scene(self):
        self.scene_loading=True;self.loading=True
        prior=bytes(self.uc.mem_read(self.texture_table+92*8,8))
        self.scene_graphics_input={'declared_empty_texture_slot':92,'previous_slot_hex':prior.hex(),
            'embedded_graphics_bootstrap':'source403620 called independently for minimap/fog records; prior full graphics ctor was a boundary'}
        self.uc.mem_write(self.texture_table+92*8,bytes(8))
        cpu=self.uc.context_save();stack=bytes(self.uc.mem_read(STACK,0x10000))
        for offset in (0x2648C,0x2650C):self.call(0x403620,receiver=self.mapctrl+offset)
        self.uc.mem_write(STACK,stack);self.uc.context_restore(cpu)

    def run_scene_thread(self):
        iterations=0;self.stop_reason=None
        while True:
            self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30_000_000,count=12_000_000)
            if self.stop_reason!='scene_texture_vector':break
            iterations+=1
            if iterations>1:raise RuntimeError('unexpected scene vectors')
            target,stride,count,ctor=self.vector_pending;cpu=self.uc.context_save();stack=bytes(self.uc.mem_read(STACK,0x10000))
            for i in range(count):self.call(ctor,receiver=target+i*stride)
            self.uc.mem_write(STACK,stack);self.uc.context_restore(cpu);self._stub_return(0,20);self.stop_reason=None
        if self.stop_reason!='before_unit_art_reset' or self.handles:raise RuntimeError('scene resources missed unit-art boundary')

    def scene_snapshot(self):
        at=self.mapctrl;fog=self.read(at+0x2658C);vpt=self.pathctrl
        for entry in self.texture_entries:
            if entry['resource']>=5:
                p=entry['record_pointer'];entry.update({'width':self.read(p+0x38,'H'),'height':self.read(p+0x3A,'H'),'format':self.read(p+0x34)})
        pointer=self.read(vpt+0xB0)
        return {'minimap':{'record_pointer':at+0x2648C,'width':self.read(at+0x264C4,'H'),'height':self.read(at+0x264C6,'H')},
            'fog':{'pointer':fog,'bytes':44032,'width':self.read(at+0x26544,'H'),'height':self.read(at+0x26546,'H'),
                'sha256':hashlib.sha256(bytes(self.uc.mem_read(fog,44032))).hexdigest(),
                'values':sorted(set(struct.unpack('<22016H',self.uc.mem_read(fog,44032))))},
            'pathfinding':{'receiver':vpt,'pointer':pointer,'section_pointers':[self.read(vpt+0xB4+i*4) for i in range(8)],
                'relocated_sha256':hashlib.sha256(bytes(self.uc.mem_read(pointer,100888))).hexdigest()}}

    def resources(self,name,commands=()):
        self.scene_loading=False;self.reset_scene();result=super().resources(name,commands)
        result.update({'scene_resources_loaded':False,'scene_resources':None,'scene_requests':[]})
        if result['ready']:
            protected=[(CHAR_BASE,0x7F4488-CHAR_BASE),(0x7CF34C,45*0x124),(0x7A528E,4),(UNITS,len(self.combat_records)*176)]
            before=[bytes(self.uc.mem_read(a,n)) for a,n in protected]
            self.bind_scene();self.clear_trace('tactical_startup');self.run_scene_thread()
            result.update({'scene_resources_loaded':True,'scene_resources':self.scene_snapshot(),
                'scene_requests':deepcopy(self.scene_requests),'scene_allocations':deepcopy(self.scene_allocations),
                'scene_boundaries':deepcopy(self.scene_boundaries),'scene_graphics_input':deepcopy(self.scene_graphics_input),
                'texture_entries':deepcopy(self.texture_entries),'gpu_boundaries':deepcopy(self.gpu_events),
                'requests':deepcopy(self.requests),'file_events':deepcopy(self.file_events),'stop_reason':self.stop_reason})
            result['phases'].append({'phase':'natural_scene_resources','coverage':self.coverage()})
            if before!=[bytes(self.uc.mem_read(a,n)) for a,n in protected]:raise RuntimeError('scene resources changed roles/current records/date/MVP')
            self.scene_loading=False;self.loading=False
        return result


def report():
    e=SchoolSceneResourcesEmulator();up=e.run_planning('scene_resources_upstream')
    if not up['school_data_prepared']:raise RuntimeError('actual fifth-school prefix missing')
    ranges=[(BASE,(SOURCE.stat().st_size+0xFFF)&~0xFFF),(TASK,0x120000),(GROUP_TASK,0x60000),
        (STACK,0x10000),(TACT,0x11A000),(SCRIPT_WORK,0x3000),(POOL,POOL_SIZE),
        (UHEAP,UHEAP_SIZE),(SCENE_POOL,SCENE_POOL_SIZE)]
    checkpoint=[(a,bytes(e.uc.mem_read(a,n))) for a,n in ranges];cpu=e.uc.context_save();cases=[]
    for name,commands in [('initial',()),('student9_waiting',[('student',9,-1)]),
        ('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1),('student',9,-1)]),
        ('teacher_only',[('student',3,-1),('student',4,-1),('student',9,-1)]),('teacher_waiting',[('teacher',101,-1)])]:
        for a,data in checkpoint:e.uc.mem_write(a,data)
        e.uc.context_restore(cpu);e.stop_reason=None;cases.append(e.resources(name,commands))
        print('Native scene resources '+name+': '+str(cases[-1]['scene_resources_loaded']),flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
        'boundary':'Scene resources initialized; GPU/embedded graphics bootstrap declared; unit art/reset, VM/enemies/events/placements unexecuted.',**AUTHORITY}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);args=p.parse_args();path=ROOT/args.out
    if path.exists():p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
