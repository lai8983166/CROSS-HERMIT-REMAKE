"""Actual fifth-school pending16, outer task and startup resource boundary.

Graphics/UnitCtrl subconstructors and platform handles remain explicit boundaries.
No resource loader, map, enemy or event world is substituted or executed.
"""
import argparse
from copy import deepcopy
import hashlib
import json
import struct
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_ECX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_combat_records_emulation import SchoolCombatRecordsEmulator,UNITS,CHAR_BASE
from tools.school_adventure_handoff_emulation import GROUP_TASK
from tools.adv_return_state_emulation import CONTROLLER
from tools.tactics_exit_emulation import BASE,ROOT,SOURCE,SOURCE_SHA256,TASK,STACK,RETURN,ExitEmulator,report_text
from tools.school_course_unlock_emulation import AUTHORITY

TACT,TACT_SIZE,SCRIPT_WORK = 0xE000000,0x1194F0,0xE200000
FONT_API = 0xE300000
NATIVE=((0x451080,0x451170),(0x451170,0x451480),(0x439EF0,0x439F90),
 (0x422290,0x4222D0),(0x420990,0x4209C0),(0x425090,0x4250D0),(0x425150,0x4251A0),
 (0x496AF0,0x496B30),(0x496B30,0x496BC0),(0x496BC0,0x496C70),
 (0x455310,0x4553A0),(0x4553E0,0x455420),(0x455810,0x4558A0),(0x4558A0,0x4558E0),
 (0x455C20,0x455CB0),(0x455D00,0x455D40),(0x4562F0,0x456350),
 (0x465F90,0x466000),(0x4E26E0,0x4E2730),(0x451670,0x4519B0),
 (0x451D40,0x451D80),(0x496390,0x4963D0),(0x496490,0x4964F0),
 (0x452040,0x452130),(0x452130,0x452CF0),(0x452CF0,0x452F10),
 (0x456B20,0x456B60),(0x451B10,0x451BF0),(0x451BF0,0x451D10),(0x451D10,0x451D40))
# Boundary entries are checked by receiver/caller; none initializes game worlds.
BOUNDARIES={0x4075E0:('graphics_subconstructor',0),0x4653D0:('unitctrl_subconstructor',0),
 0x56DDA0:('cpp_graphics_vector_constructor',20),0x4077C0:('render_context_binding',4),
 0x409480:('font_binding',4),0x4251E0:('chat_render_binding',12),0x425420:('chat_render_mode',4),
 0x42B2D0:('debug_log',0),0x415480:('render_mode',8),0x415420:('render_flush',0),
 0x451E20:('loading_screen_render',0),0x422360:('scheduler_yield',4),
 0x49E540:('dispatch_followup',0)}
EVIDENCE=ROOT/'analysis/school-tactical-startup-v1-20261009.json'
EVIDENCE_SHA256='1fdd162c0db9e02970c65fcf372375861ff028078f5d585217100154d29c3339'


def cstring(e,address,limit=260):
    raw=bytes(e.uc.mem_read(address,limit))
    if b'\0' not in raw:raise RuntimeError('unterminated bounded resource name')
    return raw.split(b'\0',1)[0].decode('ascii')


def resource_identity(relative):
    if relative not in ('data\\Tactics\\common.bin','data\\Tactics\\TactStart\\TactStart05.bin'):
        raise ValueError('resource outside current source subset')
    path=ROOT/'CROSS HERMIT/CROSS HERMIT'/relative.upper().replace('\\','/')
    raw=path.read_bytes()
    return {'relative_path':relative,'local_file':path.relative_to(ROOT).as_posix(),
        'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'loader_executed':False}


class SchoolTacticalStartupEmulator(SchoolCombatRecordsEmulator):
    def __init__(self):
        super().__init__();self._function_ranges+=NATIVE
        self.uc.mem_map(TACT,0x11A000);self.uc.mem_map(SCRIPT_WORK,0x3000);self.uc.mem_map(FONT_API,0x1000)
        self.startup_events=[];self.tactical_allocations=[];self.resource_request=None
        self.startup_writes=[];self.probe_kind=None

    def _write_hook(self,uc,access,address,size,value,context):
        if not getattr(self,'stage','').startswith('tactical_'):
            return super()._write_hook(uc,access,address,size,value,context)
        if STACK<=address and address+size<=STACK+0x10000:return
        ranges=[(0,4),(TACT,TACT+TACT_SIZE),(SCRIPT_WORK,SCRIPT_WORK+0x24C4),
            (0x7A4174,0x7A4178),(0x7A49F4,0x7A49FC),(CONTROLLER+0x2C,CONTROLLER+0x34),
            (0x809348,0x8093F8),(0x5FF720,0x5FF724)]
        if self.stage=='tactical_startup':
            ranges+=[(UNITS,UNITS+len(self.combat_records)*176),(0x7A4394,0x7A4398)]
        if not any(a<=address and address+size<=b for a,b in ranges):
            raise RuntimeError(f'tactical finite guard: {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        self.writes.append((address,size,value & ((1<<(size*8))-1)))
        self.startup_writes.append((address,size))

    def _hook(self,uc,address,size,context):
        if not getattr(self,'stage','').startswith('tactical_'):
            return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);receiver=uc.reg_read(UC_X86_REG_ECX)
        if address==0x428A40:
            count=self.read(sp+4)
            expected=[(TACT_SIZE,TACT),(0x24C4,SCRIPT_WORK)]
            index=len(self.tactical_allocations)
            if index>=2 or count!=expected[index][0]:raise RuntimeError('undeclared tactical allocation')
            pointer=expected[index][1]
            self.tactical_allocations.append({'size':count,'pointer':hex(pointer),'caller_return_va':hex(self.read(sp)),
                'isolated_initial_bytes':'zero_mapped_memory_not_native_heap_contents'})
            self._stub_return(pointer,0);return
        if address==FONT_API:
            self.startup_events.append({'kind':'CreateFontA_boundary','return_handle':1,'argument_count':14})
            self._stub_return(1,56);return
        if address==0x4216C0:
            if [self.read(sp+i) for i in (4,8,12)]!=[TACT,0,0] or self.read(TACT)!=0x59A430 or self.read(TACT+0x28,'B')!=1:
                raise RuntimeError('native tactical registration mismatch')
            self.startup_events.append({'kind':'scheduler_registration_boundary','vtable':'0x59a430','active':1})
            self._stub_return(0,0);return
        if address==0x56CEC0:
            target,byte,count=[self.read(sp+i) for i in (4,8,12)]
            allowed=[(TACT+0x117DD8,0x140),(TACT+0x44,0x1C),(SCRIPT_WORK,0x24C4),
                (SCRIPT_WORK+0x20EC,0x80),(SCRIPT_WORK+0x2170,0xC0),(SCRIPT_WORK+0x2234,0x200),
                (SCRIPT_WORK+0x2434,0x1C),(0x809348,0xB0)]
            if byte!=0 or (target,count) not in allowed:raise RuntimeError('tactical memset outside exact ranges')
            uc.mem_write(target,bytes(count));self.writes.extend((target+i,1,0) for i in range(count))
            self.startup_writes.append((target,count));self._stub_return(target,0);return
        if address in BOUNDARIES:
            name,pop=BOUNDARIES[address]
            if address==0x4075E0 and receiver not in (TACT+0x68,TACT+0xF0):raise RuntimeError('graphics constructor receiver')
            if address==0x4653D0 and receiver!=TACT+0x190:raise RuntimeError('unitctrl constructor receiver')
            self.startup_events.append({'kind':'subcomponent_boundary','name':name,'va':hex(address),
                'receiver':hex(receiver),'caller_return_va':hex(self.read(sp))})
            self._stub_return(receiver if address in (0x4075E0,0x4653D0) else 0,pop);return
        if address==0x4500B0:
            relative=cstring(self,self.read(sp+4))
            self.resource_request={'kind':'resource_loader_boundary','va':hex(address),
                'caller_return_va':hex(self.read(sp)),'receiver':hex(receiver),
                'probe_kind':self.probe_kind,'resource':resource_identity(relative)}
            self.stop_reason='tactical_resource_loader_boundary'
            uc.emu_stop();return
        if address==0x56D810:
            # Exact source cdecl %s formatter used by the independent scene probe.
            target,fmt,text=[self.read(sp+i) for i in (4,8,12)]
            if self.stage!='tactical_resource_probe' or cstring(self,fmt)!='data\\Tactics\\TactStart\\%s' \
                or not STACK<=target<=STACK+0xFF00:raise RuntimeError('undeclared source format primitive')
            value=('data\\Tactics\\TactStart\\'+cstring(self,text)).encode('ascii')
            if len(value)>=260:raise RuntimeError('source format overflow')
            uc.mem_write(target,value+b'\0');self._stub_return(len(value),0);return
        if any(a<=address<b for a,b in NATIVE):return ExitEmulator._hook(self,uc,address,size,context)
        return super()._hook(uc,address,size,context)

    def task_snapshot(self):
        return {'vtable':hex(self.read(TACT)),'active':self.read(TACT+0x28,'B'),
            'phase':self.read(TACT+0x34),'script_work_pointer':hex(self.read(TACT+0x60)),
            'field_180':self.read(TACT+0x180),'world_task_pointer':hex(self.read(0x7A49F4)),
            'script_global_pointer':hex(self.read(0x7A49F8)),'unitctrl_task_pointer':hex(self.read(TACT+0x190+0x117C38)),
            'unitctrl_mode':self.read(TACT+0x190+0x117C3C,'B'),
            'script_indices':[{'slot':self.read(SCRIPT_WORK+0x18+4*i,'B'),
                'active':self.read(SCRIPT_WORK+0x19+4*i,'B'),'unit':self.read(SCRIPT_WORK+0x1A+4*i,'h')} for i in range(100)],
            'script_counts':[self.read(SCRIPT_WORK+x,'B') for x in (0x20E8,0x216C,0x2230)],
            'loading_color':list(self.uc.mem_read(TACT+0x40,3))}

    def startup(self,name,commands=()):
        self.stage='departure_checkpoint'
        handoff=self.handoff(name,commands)
        self.startup_events=[];self.tactical_allocations=[];self.resource_request=None;self.startup_writes=[]
        phases=[];after=None;common=start=None;normalized=[]
        protected=[(CHAR_BASE,0x7F4488-CHAR_BASE),(0x7CF34C,45*0x124),(0x7A528E,4)]
        before=[bytes(self.uc.mem_read(a,n)) for a,n in protected]
        if handoff['ready']:
            self.write(0x5920A0,FONT_API) # Declared import binding only for this new stage.
            self.clear_trace('tactical_dispatch');self.call(0x49E2B0)
            phases.append({'phase':'dispatch16','coverage':self.coverage()})
            if self.read(CONTROLLER+0x2C)!=0:raise RuntimeError('pending16 not consumed natively')
            self.clear_trace('tactical_startup');self.probe_kind='natural_startup_first_resource'
            self._thread(0x451670,TACT,timeout=20_000_000)
            if self.uc.reg_read(UC_X86_REG_EIP)!=0x4500B0:raise RuntimeError('startup missed exact resource boundary')
            common=deepcopy(self.resource_request);phases.append({'phase':'startup_prefix','coverage':self.coverage()})
            after=self.task_snapshot()
            for r in self.combat_records:
                at=r['destination'];normalized.append({'character_id':r['input']['character_id'],
                    'raw_record_hex':bytes(self.uc.mem_read(at,176)).hex(),
                    'level':self.read(at+14,'B'),'hp':self.read(at+22,'H'),'mp':self.read(at+28,'H')})
            # The natural pipeline stopped before loading common.bin. This probe
            # separately invokes original selection under the same actual scene.
            self.clear_trace('tactical_resource_probe');self.probe_kind='independent_current_scene_selection'
            self.resource_request=None;self._thread(0x451BF0,TACT,timeout=1_000_000)
            if self.uc.reg_read(UC_X86_REG_EIP)!=0x4500B0:raise RuntimeError('scene selection missed boundary')
            start=deepcopy(self.resource_request);phases.append({'phase':'independent_start_selection','coverage':self.coverage()})
        if before!=[bytes(self.uc.mem_read(a,n)) for a,n in protected]:raise RuntimeError('startup changed persistent roles/MVP/calendar')
        return {'name':name,'commands':handoff['commands'],'ready':handoff['ready'],'handoff':handoff,
            'allocations':deepcopy(self.tactical_allocations),'task_after':after,'normalized_students':normalized,
            'common_request':common,'independent_start_request':start,'phases':phases,'events':deepcopy(self.startup_events),
            'pending_flag':self.read(CONTROLLER+0x2C),'pending_state':self.read(CONTROLLER+0x30),
            'persistent_ranges_unchanged':True,'outer_task_constructed':handoff['ready'],
            'subcomponents_constructed':False,'resources_loaded':False,'battle_world_constructed':False,**AUTHORITY}


def source_rules():
    data=SOURCE.read_bytes()
    if hashlib.sha256(data).hexdigest()!=SOURCE_SHA256:raise ValueError('source image differs')
    pointer=struct.unpack_from('<I',data,0x60C2B8-BASE+5*4)[0]
    raw=data[pointer-BASE:pointer-BASE+260].split(b'\0',1)[0]
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'scene_id':5,
        'start_table_va':'0x60c2b8','selected_pointer':hex(pointer),'selected_name':raw.decode('ascii'),
        'task_size':TACT_SIZE,'script_work_size':0x24C4,'task_vtable':'0x59a430',
        'resources':[resource_identity('data\\Tactics\\common.bin'),
            resource_identity('data\\Tactics\\TactStart\\'+raw.decode('ascii'))],**AUTHORITY}


def report():
    e=SchoolTacticalStartupEmulator();up=e.run_planning('tactical_startup_upstream')
    if not up['school_data_prepared']:raise RuntimeError('missing actual fifth-school prefix')
    ranges=[(BASE,(SOURCE.stat().st_size+0xFFF)&~0xFFF),(TASK,0x120000),(GROUP_TASK,0x60000),
        (STACK,0x10000),(TACT,0x11A000),(SCRIPT_WORK,0x3000)]
    checkpoint=[(a,bytes(e.uc.mem_read(a,n))) for a,n in ranges];cpu=e.uc.context_save();cases=[]
    for name,commands in [('initial',()),('student9_waiting',[('student',9,-1)]),
        ('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1),('student',9,-1)]),
        ('teacher_only',[('student',3,-1),('student',4,-1),('student',9,-1)]),('teacher_waiting',[('teacher',101,-1)])]:
        for a,data in checkpoint:e.uc.mem_write(a,data)
        e.uc.context_restore(cpu);e.stop_reason=None;cases.append(e.startup(name,commands))
        print('Native tactical startup '+name+': '+str(cases[-1]['outer_task_constructed']),flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'source_rules':source_rules(),
        'cases':cases,'limitations':['Actual school->pending10->records->pending16 dispatch in one isolated CPU.',
            'Outer task and script work execute; graphics/UnitCtrl subconstructors, vector/font/scheduler are explicit boundaries.',
            'Natural startup stops at first common resource request; separate start-resource selection probe is explicitly labelled.',
            'Files are hashed read-only; resource loader/VM, map, enemies, events and battlefield remain unexecuted.'],**AUTHORITY}


def fixture(data):
    if hashlib.sha256(EVIDENCE.read_bytes()).hexdigest()!=EVIDENCE_SHA256 \
        or hashlib.sha256(report_text(data).encode()).hexdigest()!=EVIDENCE_SHA256:raise ValueError('frozen startup evidence differs')
    keys=('name','commands','ready','task_after','normalized_students','common_request','independent_start_request',
        'pending_flag','pending_state','outer_task_constructed','subcomponents_constructed','resources_loaded','battle_world_constructed')
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,
        'cases':[{k:deepcopy(c[k]) for k in keys} for c in data['cases']],**AUTHORITY}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);args=p.parse_args()
    path=ROOT/args.out
    if path.exists():p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
