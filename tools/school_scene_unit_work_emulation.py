"""Original scene-unit work prefixes; stop before natural archive loading."""
import argparse
from copy import deepcopy
import hashlib
import struct
from unicorn.x86_const import UC_X86_REG_ECX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_enemy_records_emulation import (
    SchoolEnemyRecordsEmulator,ROOT,SOURCE,SOURCE_SHA256,BASE,TACT,UNITCTRL,
    RECORD_OFFSET,WORK_OFFSET,WORK_BYTES,STACK,RETURN,ExitEmulator,AUTHORITY,report_text)
from tools.school_first_unit_work_emulation import NATIVE,CACHE_OFFSET,CACHE_COUNT,COUNTER_OFFSET,cstring
from tools.school_current_units_emulation import TASK

SCENE_CONTROLLER,SCENE_CONTROLLER_BYTES=0x18000000,0x10000
PREFIX_RANGES=NATIVE+((0x4DA710,0x4DA7E8),(0x409900,0x4099E8),
    (0x41EAD0,0x41EB25),(0x464C60,0x464CC0),(0x464D70,0x464DD4),(0x420990,0x4209B7),
    (0x46C290,0x46C33C),(0x46A950,0x46AA22))


class SchoolSceneUnitWorkEmulator(SchoolEnemyRecordsEmulator):
    def __init__(self):
        self.scene_work_loading=False
        super().__init__()
        self.uc.mem_map(SCENE_CONTROLLER,SCENE_CONTROLLER_BYTES)
        self._function_ranges+=((0x4DA710,0x4DA7E8),(0x46C290,0x46C33C),(0x46A950,0x46AA22))
        self.scene_work_code=frozenset(a for s,t in PREFIX_RANGES for a in range(s,t))
        self.scene_work=None

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.scene_work_loading:return super()._write_hook(uc,access,address,size,value,context)
        s=self.scene_work
        allowed=[(STACK,STACK+0x10000),(0,4)]
        if s:
            allowed += [(s['work_pointer'],s['work_pointer']+WORK_BYTES),
                (s['record_pointer'],s['record_pointer']+176),
                (s['cache_pointer'],s['cache_pointer']+8),
                (UNITCTRL+COUNTER_OFFSET,UNITCTRL+COUNTER_OFFSET+4)]
            if s.get('allocation'):allowed.append((SCENE_CONTROLLER,SCENE_CONTROLLER+84))
        if not any(a<=address and address+size<=b for a,b in allowed):
            raise RuntimeError(f'scene work finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        if not STACK<=address<STACK+0x10000:self.writes.append((address,size,value&((1<<(size*8))-1)))

    def capture_scene_retained(self):
        s=self.scene_work
        excluded=[(STACK,STACK+0x10000),(0,4),(s['work_pointer'],s['work_pointer']+WORK_BYTES),
            (s['record_pointer'],s['record_pointer']+176),(s['cache_pointer'],s['cache_pointer']+8),
            (UNITCTRL+COUNTER_OFFSET,UNITCTRL+COUNTER_OFFSET+4),(SCENE_CONTROLLER,SCENE_CONTROLLER+84)]
        spans=[]
        for start,end,_ in self.uc.mem_regions():
            pieces=[(start,end+1)]
            for left,right in excluded:
                pieces=[p for a,b in pieces for p in ((a,min(b,left)),(max(a,right),b)) if p[0]<p[1]]
            spans.extend((a,bytes(self.uc.mem_read(a,b-a))) for a,b in pieces)
        return spans

    def begin_scene_work(self,ordinal,kind):
        index=249-ordinal;record=UNITCTRL+RECORD_OFFSET+index*176;work=UNITCTRL+WORK_OFFSET+index*WORK_BYTES
        raw=bytes(self.uc.mem_read(record,176));role,job=struct.unpack_from('<H',raw,2)[0],struct.unpack_from('<H',raw,12)[0]
        template=bytes.fromhex(self.enemy_inputs['templates'][ordinal])
        if role!=struct.unpack_from('<h',template)[0] or not 0<=ordinal<35 or any(self.uc.mem_read(work,WORK_BYTES)):
            raise RuntimeError('scene prefix original record/work ownership')
        group=self.read(0x61053C+job*8,'h');mode=self.read(0x61053E+job*8,'B')
        if group!=job or mode not in (0,1,2):raise RuntimeError('scene prefix unsupported source job')
        variant=0 if mode==0 else self.read(0x61053F+job*8,'b') if mode==1 else self.read(0x618090+job*40+role,'b')+1
        if not 0<=variant<=40:raise RuntimeError('scene prefix unsupported palette')
        cache=bytes(self.uc.mem_read(UNITCTRL+CACHE_OFFSET,CACHE_COUNT*8))
        matches=[i for i in range(CACHE_COUNT) if cache[i*8]==1 and cache[i*8+1]==variant and struct.unpack_from('<H',cache,i*8+2)[0]==group]
        empty=[i for i in range(CACHE_COUNT) if cache[i*8]==0]
        if matches or not empty:raise RuntimeError('scene prefix requires original uncached group')
        slot=empty[0]
        self.scene_work={'ordinal':ordinal,'index':index,'role':role,'job':job,'category':raw[0xA4],
            'evidence_kind':kind,'template_pointer':self.enemy_inputs['pointer']+ordinal*84,'template_hex':template.hex(),
            'work_pointer':work,'record_pointer':record,'before_work_hex':bytes(WORK_BYTES).hex(),
            'before_record_hex':raw.hex(),'cache_before_hex':cache.hex(),'cache_slot':slot,
            'cache_pointer':UNITCTRL+CACHE_OFFSET+slot*8,'counter_before':self.read(UNITCTRL+COUNTER_OFFSET),
            'renderer':self.read(0x7A49FC),'classification_selector':self.read(UNITCTRL+0x2EF44,'B'),
            'relation_hex':bytes(self.uc.mem_read(UNITCTRL+0x115AAC,256)).hex(),
            'group':group,'mode':mode,'variant':variant,
            'calls':[],'clears':[],'primitives':[],'allocation':None,'resource_request':None}
        self.scene_work['retained_before']=self.capture_scene_retained()

    def finish_scene_work(self):
        s=self.scene_work;retained=s.pop('retained_before')
        if any(bytes(self.uc.mem_read(a,len(raw)))!=raw for a,raw in retained):raise RuntimeError('scene prefix changed retained memory')
        if not s['resource_request'] or not s['allocation'] or self.handles:raise RuntimeError('scene prefix missed natural empty-handle request')
        s.update({'work_hex':bytes(self.uc.mem_read(s['work_pointer'],WORK_BYTES)).hex(),
            'record_hex':bytes(self.uc.mem_read(s['record_pointer'],176)).hex(),
            'cache_hex':bytes(self.uc.mem_read(UNITCTRL+CACHE_OFFSET,CACHE_COUNT*8)).hex(),
            'counter':self.read(UNITCTRL+COUNTER_OFFSET),'controller_hex':bytes(self.uc.mem_read(SCENE_CONTROLLER,84)).hex(),
            'retained_ranges_unchanged':True,'retained_bytes':sum(len(raw) for _,raw in retained),
            'retained_ranges':[{'pointer':a,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()} for a,raw in retained],
            'constructor_completed':False,'animation_loaded':False,'scene_placement_executed':False,'scene_vm_executed':False,
            'coverage':self.coverage()})
        return deepcopy(s)

    def _hook(self,uc,address,size,context):
        if not self.scene_work_loading:return super()._hook(uc,address,size,context)
        s=self.scene_work;sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX)
        if address==0x4680B0:
            caller=0x453630 if s['evidence_kind']=='actual_school_first_scene_unit' else RETURN
            if (recv,self.read(sp),self.read(sp+4))!=(UNITCTRL,caller,s['index']):raise RuntimeError('scene prefix natural constructor input')
            s['constructor_entry']={'receiver':recv,'caller_return_va':hex(self.read(sp)),'index':self.read(sp+4)}
        if address==0x4DA710:
            args=[self.read(sp+4),self.read(sp+8)]
            if args!=[s['template_pointer'],s['work_pointer']] or self.read(sp)!=0x475121:raise RuntimeError('scene prefix exact status overlay')
            s['calls'].append({'va':hex(address),'args':args,'caller_return_va':hex(self.read(sp))})
        if address==0x56CEC0:
            target,byte,count=[self.read(sp+i) for i in (4,8,12)]
            allowed=[(s['work_pointer'],WORK_BYTES,0x46815A),(s['work_pointer']+0x290,92,0x474FE5)]
            if byte or (target,count,self.read(sp)) not in allowed:raise RuntimeError('scene prefix exact clear')
            self.primitive_write(target,bytes(count));s['clears'].append({'pointer':target,'bytes':count,'caller_return_va':hex(self.read(sp))})
            self._stub_return(target,0);return
        if address==0x428A40:
            if s['allocation'] or (self.read(sp+4),self.read(sp))!=(84,0x466BB8) or any(uc.mem_read(SCENE_CONTROLLER,84)):
                raise RuntimeError('scene prefix exact controller allocation')
            s['allocation']={'pointer':SCENE_CONTROLLER,'bytes':84,'freed':False,'caller_return_va':hex(self.read(sp))}
            s['primitives'].append({'kind':'heap_allocation',**s['allocation']});self._stub_return(SCENE_CONTROLLER,0);return
        if address==0x42B2D0:
            args=[self.read(sp+i) for i in (8,12,16)]
            if self.read(sp)!=0x467134 or cstring(self,self.read(sp+4))!='char:%03d, job:%03d : palette:%03d\n' or args!=[s['role'],s['job'],s['variant']-1]:
                raise RuntimeError('scene prefix exact debug output')
            s['primitives'].append({'kind':'debug_log','args':args});self._stub_return(0,0);return
        if address==0x466C80:
            args=[self.read(sp+i) for i in (4,8,12)]
            if recv!=UNITCTRL or args!=[s['cache_pointer'],s['group'],s['variant']]:raise RuntimeError('scene prefix exact cache binding')
            s['calls'].append({'va':hex(address),'receiver':recv,'args':args})
        if address==0x464D70:
            if recv!=SCENE_CONTROLLER or [self.read(sp+4),self.read(sp+8)]!=[s['renderer'],s['group']+8]:raise RuntimeError('scene prefix source animation binding')
        if address==0x4500B0:
            args=[self.read(sp+4+i*4) for i in range(4)]
            expected=[self.read(0x610538+s['group']*8),s['variant'],int(s['variant']!=0),0]
            if recv!=s['renderer']+0x80000 or self.read(sp)!=0x464F1F or args!=expected or s['resource_request']:
                raise RuntimeError('scene prefix exact source animation request')
            s['resource_request']={'receiver':recv,'caller_return_va':hex(self.read(sp)),'args':args,
                'relative_path':cstring(self,args[0]),'loaded':False}
            self.stop_reason='before_first_scene_unit_animation_load';uc.emu_stop();return
        if address in self.scene_work_code:self.visited.add(address);return
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        raise RuntimeError(f'undeclared scene prefix code {address:#x}')

    def run_scene_prefix(self):
        self.clear_trace('tactical_startup');self.stop_reason=None;self.scene_work_loading=True
        try:
            self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=3_000_000,count=200_000)
            if self.stop_reason!='before_first_scene_unit_animation_load':raise RuntimeError('scene prefix missed exact stop')
            return self.finish_scene_work()
        finally:self.scene_work_loading=False

    def resources(self,name,commands=()):
        self.scene_work_loading=False;self.scene_work=None
        result=super().resources(name,commands)
        result.update({'scene_unit_work_prefix_initialized':False,'scene_unit_work':None})
        if not result['ready']:return result
        self.begin_scene_work(0,'actual_school_first_scene_unit')
        snapshot=self.run_scene_prefix()
        result.update({'scene_unit_work_prefix_initialized':True,'scene_unit_work':snapshot,'stop_reason':self.stop_reason})
        result['phases'].append({'phase':'native_first_scene_unit_work_prefix','coverage':self.coverage()})
        return result

    def declared_scene_prefixes(self):
        derived=self.declared_templates();outputs=[]
        self.write(0x7F4488,5,'h');self.write(0x7A49FC,TASK)
        for r in derived['records']:
            self.uc.mem_write(UNITCTRL+CACHE_OFFSET,bytes(CACHE_COUNT*8));self.write(UNITCTRL+COUNTER_OFFSET,110)
            self.uc.mem_write(SCENE_CONTROLLER,bytes(84));self.uc.mem_write(r['record_pointer'],bytes.fromhex(r['record_hex']))
            self.begin_scene_work(r['ordinal'],'declared_isolated_scene_unit_prefix')
            sp=STACK+0xFF00;self.write(sp,RETURN);self.write(sp+4,r['index'])
            self.uc.reg_write(UC_X86_REG_ECX,UNITCTRL);self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_EIP,0x4680B0)
            outputs.append(self.run_scene_prefix())
        return {'evidence_kind':'declared_scene5_isolated_work_prefix_driver','units':outputs,
            'declared_inputs':{'empty_cache':True,'counter':110,'renderer':TASK,'zero_controller_allocation':True,
                'classification_selector':0,'relation_hex':bytes(256).hex()},
            'school_enemy_loop_executed':False,'constructor_tails_executed':False,'archives_loaded':False,**AUTHORITY}


def report():
    e=SchoolSceneUnitWorkEmulator()
    if not e.run_planning('scene_work_upstream')['school_data_prepared']:raise RuntimeError('scene work school prefix missing')
    checkpoint=[(a,bytes(e.uc.mem_read(a,b-a+1))) for a,b,_ in e.uc.mem_regions()];cpu=e.uc.context_save()
    declared=e.declared_scene_prefixes();cases=[]
    for name,commands in [('initial',()),('student9_waiting',[('student',9,-1)]),
        ('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1),('student',9,-1)]),
        ('teacher_only',[('student',3,-1),('student',4,-1),('student',9,-1)]),('teacher_waiting',[('teacher',101,-1)])]:
        for at,raw in checkpoint:e.uc.mem_write(at,raw)
        e.uc.context_restore(cpu);e.scene_work_loading=False;e.enemy_loading=False;e.stop_reason=None
        cases.append(e.resources(name,commands));print('Native scene work '+name+': '+str(cases[-1]['scene_unit_work_prefix_initialized']),flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'scene_inputs':e.enemy_inputs,
        'declared_scene_prefix_diagnostic':declared,'cases':cases,
        'boundary':'Actual first scene-unit prefix; separately declared35 isolated prefixes. No archive loading, constructor tail, full scene loop, deployment or VM.',**AUTHORITY}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);args=p.parse_args();path=ROOT/args.out
    if path.exists():p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
