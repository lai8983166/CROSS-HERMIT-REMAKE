"""Native logical UnitCtrl and natural scene5 logical-map initialization.

Original generic appearance-grid code runs in a statically checked batch on the
same CPU with forbidden-write guards. Graphics/fonts/audio remain boundaries.
"""
import argparse
from copy import deepcopy
import hashlib
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_32, CS_GRP_CALL, CS_GRP_JUMP
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_ECX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_tactical_resources_emulation import (
    SchoolTacticalResourcesEmulator, RESOURCE_NAMES, FILE_API, FILE_IMPORTS, POOL, POOL_SIZE)
from tools.school_tactical_startup_emulation import TACT,TACT_SIZE,SCRIPT_WORK,cstring
from tools.school_combat_records_emulation import CHAR_BASE
from tools.school_course_unlock_emulation import AUTHORITY
from tools.school_adventure_handoff_emulation import GROUP_TASK
from tools.tactics_exit_emulation import ROOT,SOURCE,SOURCE_SHA256,BASE,TASK,STACK,RETURN,report_text

UNITCTRL=TACT+0x190
UHEAP,UHEAP_SIZE=0xF000000,0x100000
MAP_BIN='data\\tactics\\map\\map05.bin'
MAP_GRAPHICS='data\\tactics\\map\\map05.map'
MAP_HASHES={'map05.bin':'bb8ef4d51cc3228cf38cda21435030a5dd6d9955a303ef445d46508c5fa11c45',
 'map05.map':'30365cb526d2b6ebef2b3609f69cc09eca8569dfdd03ba67dbf4a65a1c9f362e',
 'map05.bmp':'123ae60bdf213a0e70b51112f6795923eab29979f9cd83aaf5c0ea1a43fc7b2e',
 'map05.vpt':'99004441c0bf2780623d7f9e7da82c77e255fb78261eb22eb90c6cabbda0b53f'}
NATIVE=((0x4653D0,0x465AB3),(0x4649C0,0x464A32),(0x464A40,0x464A79),
 (0x464B70,0x464C13),(0x4646E0,0x464776),(0x464780,0x4647B9),(0x4648D0,0x464973),
 (0x43A060,0x43A262),(0x43AB10,0x43B101),(0x43B110,0x43B245),
 (0x44E280,0x44E323),(0x4378D0,0x43793D),(0x40BA20,0x40BA92),
 (0x40BAA0,0x40BAD9),(0x40BBD0,0x40BC86),(0x439380,0x43940D),
 (0x427530,0x4275AE),(0x427650,0x427799),(0x427890,0x42798C),
 (0x427CD0,0x427D13),(0x427990,0x427A77),(0x465AC0,0x465AF9),(0x465B40,0x465B7C),
 (0x466AB0,0x466AF6),(0x492E90,0x492EF1),(0x492F00,0x492F40),
 (0x494CF0,0x494D14),(0x494D20,0x494D66),(0x467DB0,0x467E00),(0x467D50,0x467D74),
 (0x437A30,0x437A62),(0x44E810,0x44E842),(0x49CC10,0x49CC5D),
 (0x493DC0,0x493E59),(0x4935F0,0x49362F),(0x4519C0,0x451A58),
 (0x451F50,0x45203C),(0x451A60,0x451B0F),(0x4538D0,0x453922),
 (0x467E70,0x467EA3),(0x4DB010,0x4DB05D))
MAP_NATIVE=((0x452FC0,0x453527),(0x466B00,0x466B32),(0x499C90,0x499D98),
 (0x43B250,0x43B338),(0x43A640,0x43A920),(0x43A920,0x43AB05),
 (0x43CE10,0x43CF10),(0x43CF10,0x43CFD1),(0x43CFE0,0x43D0BC),(0x43D0C0,0x43D122))
CODE=frozenset(a for start,end in NATIVE for a in range(start,end))
VECTORS=((0xDB86C,0x88,20,0x465AC0,0x465B00),(0xDE460,0x28,2,0x427530,0x4275B0),
 (0xDE7B0,0x80,3,0x4075E0,0x407710),(0xDE930,0x80,64,0x4075E0,0x407710),
 (0xE0930,0x80,512,0x4075E0,0x407710),(0xF0930,0x80,512,0x4075E0,0x407710),
 (0x100930,0x80,256,0x4075E0,0x407710),(0x108930,0x80,4,0x4075E0,0x407710),
 (0x116098,0x2C,10,0x465B40,0x465B80))


def map_resource(name):
    if name not in MAP_HASHES:raise ValueError('map outside original scene5 table')
    path=ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/MAP'/name.upper()
    raw=path.read_bytes();sha=hashlib.sha256(raw).hexdigest()
    if sha!=MAP_HASHES[name]:raise ValueError('original scene map identity differs')
    return raw,{'filename':name,'local_file':path.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':sha}


def checked_grid_code():
    """Prove all static calls/jumps in this fixed function pair are declared."""
    image=SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest()!=SOURCE_SHA256:raise ValueError('source image differs')
    cs=Cs(CS_ARCH_X86,CS_MODE_32);cs.detail=True
    ranges=((0x43AB10,0x43B101),(0x43B110,0x43B245))
    instructions=[i for a,b in ranges for i in cs.disasm(image[a-BASE:b-BASE],a)]
    starts={i.address for i in instructions};calls=[]
    primitives={0x428A40,0x428AD0,0x56CEC0,0x56CE80,0x56DB00,0x424F80}
    for i in instructions:
        if i.group(CS_GRP_CALL) or i.group(CS_GRP_JUMP):
            if len(i.operands)!=1 or i.operands[0].type!=2:raise ValueError('indirect grid control flow')
            target=i.operands[0].imm
            if target not in starts and not (i.group(CS_GRP_CALL) and target in primitives):
                raise ValueError('grid branch/call outside fixed source graph')
            if i.group(CS_GRP_CALL):calls.append([hex(i.address),hex(target)])
    return {'source_ranges':[[hex(a),hex(b)] for a,b in ranges],
            'source_code_sha256':hashlib.sha256(b''.join(image[a-BASE:b-BASE] for a,b in ranges)).hexdigest(),
            'instruction_count':len(instructions),'direct_calls':calls,'no_indirect_transfers':True}


class SchoolUnitCtrlMapEmulator(SchoolTacticalResourcesEmulator):
    def __init__(self):
        self.logical=False;self.map_stage=False
        super().__init__();self._function_ranges+=NATIVE+MAP_NATIVE
        self.map_native=MAP_NATIVE
        self.uc.mem_map(UHEAP,UHEAP_SIZE)
        self.reset_logical()

    def reset_logical(self):
        self.unit_allocations=[];self.unit_cursor=UHEAP;self.logical_events=[]
        self.grid_report=None;self.mapctrl=None;self.logic_snapshot=None
        self.graphics_request=None;self.map_allocations=[]

    def _write_hook(self,uc,access,address,size,value,context):
        if not getattr(self,'logical',False) and not getattr(self,'map_stage',False):
            return super()._write_hook(uc,access,address,size,value,context)
        if STACK<=address and address+size<=STACK+0x10000:return
        allowed=[(0,4),(TACT,TACT+TACT_SIZE),(0x7A49EC,0x7A49F0)]
        allowed += [(a['pointer'],a['pointer']+a['bytes']) for a in self.unit_allocations if not a['freed']]
        if self.map_stage:
            allowed += [(0x7F4504,0x7F450C),(0x7F448E,0x7F448F)]
            allowed += [(a['pointer'],a['pointer']+a['bytes']) for a in self.map_allocations]
        if any(a<=address and address+size<=b for a,b in allowed):
            self.writes.append((address,size,value & ((1<<(size*8))-1)))
            self.startup_writes.append((address,size));return
        if self.map_stage:return super()._write_hook(uc,access,address,size,value,context)
        raise RuntimeError(f'UnitCtrl finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')

    def _unit_allocate(self,count,caller):
        expected={0x43AB5E:8450,0x43ABA8:25350,0x43ABFD:8450}
        if caller==0x4276E1:
            if count not in (3600,6144,3000,240):raise RuntimeError('unknown UnitCtrl list capacity')
            kind='linked_list'
        elif caller in expected and count==expected[caller]:kind='appearance_grid'
        else:raise RuntimeError(f'UnitCtrl allocation caller/size {caller:#x}/{count}')
        pointer=self.unit_cursor;self.unit_cursor+=(count+15)&~15
        if self.unit_cursor>UHEAP+UHEAP_SIZE:raise RuntimeError('UnitCtrl heap overflow')
        self.unit_allocations.append({'pointer':pointer,'bytes':count,'kind':kind,
                                      'caller_return_va':hex(caller),'freed':False})
        return pointer

    def _hook(self,uc,address,size,context):
        if address==0x4653D0 and getattr(self,'stage','')=='tactical_dispatch':
            if uc.reg_read(UC_X86_REG_ECX)!=UNITCTRL:raise RuntimeError('logical UnitCtrl receiver')
            self.logical=True
        if self.logical:
            sp=uc.reg_read(UC_X86_REG_ESP);receiver=uc.reg_read(UC_X86_REG_ECX)
            if address==0x43A060:self.mapctrl=receiver
            if address==0x43AB10:
                self.stop_reason='unitctrl_grid_batch';uc.emu_stop();return
            if address==0x428A40:
                self._stub_return(self._unit_allocate(self.read(sp+4),self.read(sp)),0);return
            if address==0x428AD0:
                pointer=self.read(sp+4);matches=[a for a in self.unit_allocations if a['pointer']==pointer and not a['freed']]
                if len(matches)!=1 or matches[0]['caller_return_va']!='0x43ab5e':raise RuntimeError('UnitCtrl free ownership')
                matches[0]['freed']=True;self._stub_return(0,0);return
            if address==0x56CEC0:
                target,byte,count=[self.read(sp+i) for i in (4,8,12)]
                if byte!=0 or count>0x50140:raise RuntimeError('UnitCtrl clear primitive bounds')
                self.primitive_write(target,bytes(count));self._stub_return(target,0);return
            if address==0x56DDA0:
                args=tuple(self.read(sp+i) for i in (4,8,12,16,20))
                expected=[(UNITCTRL+off,stride,count,ctor,dtor) for off,stride,count,ctor,dtor in VECTORS]
                if args not in expected:raise RuntimeError('UnitCtrl vector bounds')
                self.logical_events.append({'kind':'vector','target':hex(args[0]),'stride':args[1],'count':args[2],
                                            'ctor':hex(args[3]),'graphics_boundary':args[3]==0x4075E0})
                if args[3]==0x4075E0:self._stub_return(0,20);return
                self.vector_pending=args[:4];self.stop_reason='unitctrl_vector';uc.emu_stop();return
            if address==0x4075E0:
                if not TACT<=receiver<=TACT+TACT_SIZE-128:raise RuntimeError('UnitCtrl graphics receiver')
                self.logical_events.append({'kind':'graphics_boundary','receiver':hex(receiver)})
                self._stub_return(receiver,0);return
            if address==0x465AB2:self.logical=False
            if address in CODE:self.visited.add(address);return
        if self.map_stage:
            sp=uc.reg_read(UC_X86_REG_ESP)
            if address==0x4500B0:
                if uc.reg_read(UC_X86_REG_ECX)!=TASK+0x80000:raise RuntimeError('map manager receiver')
                name=cstring(self,self.read(sp+4))
                if name==MAP_GRAPHICS:
                    _,identity=map_resource('map05.map')
                    self.graphics_request={'relative_path':name,'source':identity,'caller_return_va':hex(self.read(sp))}
                    self.stop_reason='scene_graphics_resource_boundary';uc.emu_stop();return
                if name==MAP_BIN and len(self.requests)==4:
                    _,identity=map_resource('map05.bin')
                    self.requests.append({'source':{'relative_path':name,**identity},'entry_count':0,
                                          'caller_return_va':hex(self.read(sp))})
                    self.visited.add(address);return
                raise RuntimeError('unknown next map resource')
            if address==0x56D810 and cstring(self,self.read(sp+8))=='%s%s' and STACK<=self.read(sp+4)<STACK+0xFF00:
                target,left,right=[self.read(sp+i) for i in (4,12,16)]
                value=(cstring(self,left)+cstring(self,right)).encode('ascii')
                if value.decode() not in (MAP_BIN,MAP_GRAPHICS):raise RuntimeError('map source format differs')
                self.primitive_write(target,value+b'\0');self._stub_return(len(value),0);return
            if address==0x428A40 and self.read(sp)!=0x42AD54:
                count=self.read(sp+4);cells=struct.unpack_from('<2H',map_resource('map05.bin')[0],4)
                expected={0x43A7A5:4,0x43A828:cells[0]*cells[1]*2,0x43D050:cells[0]*cells[1]}
                if expected.get(self.read(sp))!=count:raise RuntimeError('map scratch allocation caller/count')
                pointer=self.pool_cursor;self.pool_cursor+=(count+15)&~15
                if self.pool_cursor>POOL+POOL_SIZE:raise RuntimeError('map heap bounds')
                self.map_allocations.append({'pointer':pointer,'bytes':count,'caller_return_va':hex(self.read(sp))})
                self._stub_return(pointer,0);return
            if address==0x56CEC0:
                target,byte,count=[self.read(sp+i) for i in (4,8,12)]
                if byte!=0:raise RuntimeError('map nonzero clear')
                self.primitive_write(target,bytes(count));self._stub_return(target,0);return
            if address==0x570FE0:
                self.logical_events.append({'kind':'declared_CRT_rand','return_value':0})
                self._stub_return(0,0);return
            if address==0x4DB010:
                self.logical_events.append({'kind':'audio_bgm_boundary','source_index':self.read(sp+4)})
                self._stub_return(0,0);return
            if address==0x407780:
                self.logical_events.append({'kind':'map_graphics_cleanup_boundary'})
                self._stub_return(0,0);return
            if address in CODE or any(a<=address<b for a,b in self.map_native):
                self.visited.add(address);return
        return super()._hook(uc,address,size,context)

    def _file_api(self,address,sp):
        index=(address-FILE_API)//16;slot,(name,pop)=list(FILE_IMPORTS.items())[index]
        if self.map_stage and name=='CreateFileA':
            args=[self.read(sp+4+i*4) for i in range(7)]
            if cstring(self,args[0])!=MAP_BIN or args[1:]!=[0x80000000,1,0,3,1,0]:raise RuntimeError('map read-only API arguments')
            raw,identity=map_resource('map05.bin');handle=0x805
            self.handles[handle]={'raw':raw,'identity':identity}
            self.file_events.append({'name':name,'import_va':hex(slot),'args':args,'result':handle})
            self._stub_return(handle,pop);return
        return super()._file_api(address,sp)

    def call(self,address,args=(),*,receiver=TASK):
        if address!=0x49E2B0 or getattr(self,'stage','')!='tactical_dispatch':
            return super().call(address,args,receiver=receiver)
        sp=STACK+0xFF00;self.write(sp,RETURN)
        self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,receiver)
        self.stop_reason=None;self.uc.emu_start(address,RETURN,timeout=30_000_000,count=3_000_000)
        while self.stop_reason in ('unitctrl_grid_batch','unitctrl_vector'):
            if self.stop_reason=='unitctrl_grid_batch':self.run_grid_batch()
            else:
                target,stride,count,ctor=self.vector_pending
                cpu=self.uc.context_save();stack=bytes(self.uc.mem_read(STACK,0x10000))
                for i in range(count):self.call(ctor,receiver=target+i*stride)
                self.uc.mem_write(STACK,stack);self.uc.context_restore(cpu);self._stub_return(0,20)
            self.stop_reason=None
            self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30_000_000,count=3_000_000)
        if self.uc.reg_read(UC_X86_REG_EIP)!=RETURN or self.uc.reg_read(UC_X86_REG_ESP)!=sp+4:
            raise RuntimeError('logical tactical dispatch did not return')
        self.logic_snapshot=self.unitctrl_snapshot()
        return self.uc.reg_read(UC_X86_REG_EAX)

    def run_grid_batch(self):
        graph=checked_grid_code();sp=self.uc.reg_read(UC_X86_REG_ESP);caller=self.read(sp)
        before=len(self.unit_allocations);temporary=[]
        self.uc.hook_del(self._audit_code_hook)
        for hook in self._audit_write_hooks:self.uc.hook_del(hook)
        # No writes outside current task, bounded heap, stack and SEH cell.
        allowed=sorted([(0,4),(STACK,STACK+0x10000),(TACT,TACT+TACT_SIZE),(UHEAP,UHEAP+UHEAP_SIZE)])
        def forbidden(uc,access,address,size,value,context):
            raise RuntimeError(f'appearance grid forbidden write {address:#x}/{size}')
        cursor=0
        for a,b in allowed:
            if cursor<a:temporary.append(self.uc.hook_add(UC_HOOK_MEM_WRITE,forbidden,begin=cursor,end=a-1))
            cursor=b
        temporary.append(self.uc.hook_add(UC_HOOK_MEM_WRITE,forbidden,begin=cursor,end=0xFFFFFFFF))
        def primitive(uc,address,size,context):
            if address==0x424F80:raise RuntimeError('native appearance grid assertion')
            if address==0x56DB00:
                value=self.read(uc.reg_read(UC_X86_REG_ESP)+4,'i');self._stub_return(abs(value),0);return
            # Grid entry stop belongs to its caller; primitives stay native-bound.
            self._hook(uc,address,size,context)
        for address in (0x428A40,0x428AD0,0x56CEC0,0x56CE80,0x56DB00,0x424F80):
            temporary.append(self.uc.hook_add(UC_HOOK_CODE,primitive,begin=address,end=address))
        try:
            self.write(sp,RETURN)
            for batch in range(12):
                self.uc.emu_start(0x43AB10 if batch==0 else self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30_000_000,count=1_500_000_000)
                if self.uc.reg_read(UC_X86_REG_EIP)==RETURN:break
                print(f'Native appearance grid batch {batch+1}: {self.uc.reg_read(UC_X86_REG_EIP):#x}',flush=True)
            if self.uc.reg_read(UC_X86_REG_EIP)!=RETURN or self.uc.reg_read(UC_X86_REG_ESP)!=sp+4:
                raise RuntimeError('native appearance grid exceeded batch bounds')
            self.write(sp,caller);self.uc.reg_write(UC_X86_REG_EIP,caller)
        finally:
            for hook in temporary:self.uc.hook_del(hook)
            self._audit_code_hook=self.uc.hook_add(UC_HOOK_CODE,self._hook)
            self._audit_write_hooks=[self.uc.hook_add(UC_HOOK_MEM_WRITE,self._write_hook) for _ in self._audit_write_hooks]
        grid=self.unit_allocations[before:]
        if len(grid)!=3 or not grid[0]['freed']:raise RuntimeError('native grid ownership differs')
        raw=bytes(self.uc.mem_read(grid[1]['pointer'],grid[1]['bytes']))
        rows=[list(struct.unpack_from('<bbHH',raw,i*6)) for i in range(4225)]
        if {tuple(r[:2]) for r in rows}!={(x,y) for y in range(-32,33) for x in range(-32,33)} \
            or any(r[2]!=abs(r[0])+abs(r[1]) or r[3]!=i for i,r in enumerate(rows)):
            raise RuntimeError('native grid postconditions differ')
        self.grid_report={'static_graph':graph,'rows':rows,'sha256':hashlib.sha256(raw).hexdigest(),
            'execution':'original_code_same_CPU_guarded_batch','guard':'forbidden-write hooks and final ownership/grid postconditions',
            'per_instruction_trace':False,'batch_limits':{'max_batches':12,'timeout_seconds_each':30,'max_instructions_each':1500000000}}
        self.visited.update([0x43AB10,0x43B110])

    def unitctrl_snapshot(self):
        return {'receiver':hex(UNITCTRL),'mapctrl':hex(self.mapctrl),'mode':self.read(UNITCTRL+0x117C3C,'B'),
            'task_backpointer':hex(self.read(UNITCTRL+0x117C38)),
            'font_handles':[self.read(UNITCTRL+i) for i in (0xDB80C,0xDB810)],
            'sentinel':hex(self.read(UNITCTRL+0x2E70C)),
            'map_size':[self.read(self.mapctrl+i,'H') for i in (0x263C0,0x263C2)],
            'allocation_sizes':[a['bytes'] for a in self.unit_allocations],
            'zero_counts':[self.read(UNITCTRL+i) for i in (0xDC30C,0x108B50,0x117C40)]}

    def resources(self,name,commands=()):
        self.logical=False;self.map_stage=False;self.reset_logical()
        result=super().resources(name,commands)
        result.update({'unitctrl_constructed':result['ready'],'graphics_subcomponents_constructed':False,
            'logical_unitctrl':deepcopy(self.logic_snapshot),'unitctrl_allocations':deepcopy(self.unit_allocations),
            'appearance_grid':deepcopy(self.grid_report),'logical_map':None,'scene_graphics_request':None,
            'logical_map_loaded':False,'logical_events':deepcopy(self.logical_events)})
        if result['ready']:
            protected=[(CHAR_BASE,0x7F4488-CHAR_BASE),(0x7CF34C,45*0x124),(0x7A528E,4)]
            protected.append((0x7F4518,len(self.combat_records)*176))
            before=[bytes(self.uc.mem_read(a,n)) for a,n in protected]
            self.map_stage=True;self.loading=True;self.stop_reason=None;self.clear_trace('tactical_startup')
            self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30_000_000,count=3_000_000)
            if self.stop_reason!='scene_graphics_resource_boundary' or self.handles:
                raise RuntimeError('logical map missed scene graphics boundary')
            at=self.mapctrl;pointer=self.read(at+0x2659C);cm=self.read(at+0x265A0)
            raw,identity=map_resource('map05.bin')
            if bytes(self.uc.mem_read(pointer,len(raw)))!=raw:raise RuntimeError('native logical map bytes differ')
            scratch=[self.read(cm)]+[self.read(at+i) for i in (0x98,0x9C,0xA0)]
            sizes=[12288,6144,6144,6144]
            if any(any(self.uc.mem_read(p,n)) for p,n in zip(scratch,sizes)):raise RuntimeError('native map scratch not clear')
            result['logical_map']={'source':identity,'pointer':pointer,'cm_pointer':cm,
                'header':list(struct.unpack_from('<8H',raw)),'scratch':[{'pointer':p,'bytes':n,'sha256':hashlib.sha256(bytes(self.uc.mem_read(p,n))).hexdigest()} for p,n in zip(scratch,sizes)],
                'scene_id':self.read(at+0x265A4,'H'),'phase':self.read(TACT+0x34),'initial_unit_work':self.read(UNITCTRL+0x2E6F0),
                'map_allocations':deepcopy(self.map_allocations)}
            result['logical_map_loaded']=True
            for key in ('requests','file_events','resource_allocations'):result[key]=deepcopy(getattr(self,key))
            result['task_after_map']=self.task_snapshot()
            result['current_combat_records_unchanged']=True
            result['scene_graphics_request']=deepcopy(self.graphics_request)
            result['phases'].append({'phase':'natural_logical_scene_map','coverage':self.coverage()})
            result['logical_events']=deepcopy(self.logical_events)
            if before!=[bytes(self.uc.mem_read(a,n)) for a,n in protected]:raise RuntimeError('logical map changed roles/date/MVP')
            result['stop_reason']=self.stop_reason
            self.map_stage=False;self.loading=False
        return result


def report():
    e=SchoolUnitCtrlMapEmulator()
    up=e.run_planning('unitctrl_scene_map_upstream')
    if not up['school_data_prepared']:raise RuntimeError('missing actual fifth-school prefix')
    ranges=[(BASE,(SOURCE.stat().st_size+0xFFF)&~0xFFF),(TASK,0x120000),(GROUP_TASK,0x60000),
        (STACK,0x10000),(TACT,0x11A000),(SCRIPT_WORK,0x3000),(POOL,POOL_SIZE),(UHEAP,UHEAP_SIZE)]
    checkpoint=[(a,bytes(e.uc.mem_read(a,n))) for a,n in ranges];cpu=e.uc.context_save();cases=[]
    for name,commands in [('initial',()),('student9_waiting',[('student',9,-1)]),
        ('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1),('student',9,-1)]),
        ('teacher_only',[('student',3,-1),('student',4,-1),('student',9,-1)]),('teacher_waiting',[('teacher',101,-1)])]:
        for a,data in checkpoint:e.uc.mem_write(a,data)
        e.uc.context_restore(cpu);e.stop_reason=None;cases.append(e.resources(name,commands))
        print('Native logical UnitCtrl/map '+name+': '+str(cases[-1]['logical_map'] is not None),flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
        'boundary':'Logical constructors/map loaded; graphics/font/audio/CRT inputs declared; VM/enemies/events/placement unexecuted.',**AUTHORITY}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);args=p.parse_args()
    path=ROOT/args.out
    if path.exists():p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
