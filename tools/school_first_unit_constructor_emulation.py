"""Complete exactly the first native current-unit constructor on school CPU.

GPU and exact CRT clears remain declared; original logical/action code executes.
Constructor coordinates precede scene placement and are not spawn evidence.
"""
import argparse
from copy import deepcopy
import hashlib
import struct
from unicorn.x86_const import UC_X86_REG_ECX,UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EAX,UC_X86_REG_EBP
from tools.school_first_unit_animation_emulation import (
    SchoolFirstUnitAnimationEmulator,UNIT_POOL,UNIT_POOL_SIZE,WORK_OFFSET,WORK_BYTES,
    RECORD_OFFSET,CACHE_OFFSET,CACHE_COUNT,COUNTER_OFFSET,MAP_POOL,MAP_POOL_SIZE,
    ASSET_POOL,ASSET_POOL_SIZE,SCENE_POOL,SCENE_POOL_SIZE,UHEAP,UHEAP_SIZE,
    UNITCTRL,POOL,POOL_SIZE,TACT,SCRIPT_WORK,GROUP_TASK,CHAR_BASE,UNITS,
    ROOT,SOURCE,SOURCE_SHA256,BASE,TASK,STACK,RETURN,report_text,ExitEmulator,
    AUTHORITY,WORK_GROUPS,ANIM_POOL,ANIM_POOL_SIZE)

SHARED_OFFSET,SHARED_BYTES = 0x108F48,42
NATIVE = ((0x467147,0x4671E4),(0x4682C9,0x468645),(0x468690,0x468805),
    (0x46BCC0,0x46BD30),(0x46BD30,0x46BE16),(0x465040,0x465139),
    (0x46B2C0,0x46B430),(0x43C470,0x43C5E0),(0x480F50,0x480FCB),
    (0x437C90,0x437D05),(0x466FC0,0x467020),(0x492E60,0x492ED0),
    (0x469AD0,0x469D30))


class SchoolFirstUnitConstructorEmulator(SchoolFirstUnitAnimationEmulator):
    def __init__(self):
        self.constructor_loading = False
        super().__init__()
        self._function_ranges += NATIVE
        self.constructor_entries = ({a for a,b in NATIVE}-{0x467147,0x4682C9})|{0x409EF0,0x409FF0,0x40A520}
        self.constructor_code = frozenset(a for s,t in self._function_ranges for a in range(s,t))-self.constructor_entries
        self.constructor_calls = []
        self.constructor_clears = []
        self.constructor_return_sp = None

    def _write_hook(self,uc,access,address,size,value,context):
        if not getattr(self,'constructor_loading',False):
            return super()._write_hook(uc,access,address,size,value,context)
        work = UNITCTRL+WORK_OFFSET+self.active_index*WORK_BYTES
        allowed = [(STACK,STACK+0x10000),(0,4),(work,work+WORK_BYTES),
                   (UNITCTRL+SHARED_OFFSET,UNITCTRL+SHARED_OFFSET+SHARED_BYTES),
                   (self.constructor_cell,self.constructor_cell+1)]
        if not any(a<=address and address+size<=b for a,b in allowed):
            raise RuntimeError(f'first constructor finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        if not STACK<=address<STACK+0x10000:
            self.writes.append((address,size,value & ((1<<(size*8))-1)))
            self.startup_writes.append((address,size))

    def _hook(self,uc,address,size,context):
        if not getattr(self,'constructor_loading',False):
            return super()._hook(uc,address,size,context)
        if address==0x4533FA:
            if uc.reg_read(UC_X86_REG_EAX)!=0 or uc.reg_read(UC_X86_REG_ESP)!=self.constructor_return_sp:
                raise RuntimeError('first constructor original return/stack differs')
            self.stop_reason = 'after_first_unit_constructor_return'
            uc.emu_stop()
            return
        if address in (0x424F80,0x428A40,0x428AD0,0x56DDA0,0x4500B0):
            raise RuntimeError(f'unexpected first constructor assertion/allocation/resource at {address:#x}')
        if address in self.constructor_code:
            self.visited.add(address)
            return
        sp,receiver = uc.reg_read(UC_X86_REG_ESP),uc.reg_read(UC_X86_REG_ECX)
        work = UNITCTRL+WORK_OFFSET+self.active_index*WORK_BYTES
        if address==0x56CEC0:
            target,byte,count = [self.read(sp+i) for i in (4,8,12)]
            allowed = [(work+o,88,0x409F1A) for o in [0x48,*[0xA0+i*88 for i in range(5)]]]
            allowed += [(work+o,236,0x437CBD) for o in (0x2F4,0x3E0)]
            allowed += [(UNITCTRL+SHARED_OFFSET,SHARED_BYTES,0x480F85)]
            if byte!=0 or (target,count,self.read(sp)) not in allowed:
                raise RuntimeError('first constructor exact owned clear')
            self.primitive_write(target,bytes(count))
            self.constructor_clears.append({'target':target,'bytes':count,'caller_return_va':hex(self.read(sp))})
            self._stub_return(target,0)
            return
        if address in self.constructor_entries:
            argc = {0x465040:3,0x409FF0:4,0x468690:3,0x43C470:3,0x46BCC0:2}.get(address,1)
            self.constructor_calls.append({'va':hex(address),'receiver':receiver,
                'args':[self.read(sp+4+i*4) for i in range(argc)],'caller_return_va':hex(self.read(sp))})
            self.visited.add(address)
            return
        return ExitEmulator._hook(self,uc,address,size,context)

    def prepare_constructor(self):
        work = UNITCTRL+WORK_OFFSET+self.active_index*WORK_BYTES
        record = UNITCTRL+RECORD_OFFSET+self.active_index*176
        header,cm = self.read(UNITCTRL+0x2A304),self.read(UNITCTRL+0x2A308)
        width,height = self.read(header+4,'H'),self.read(header+6,'H')
        x,y = self.read(record+0x9B,'B'),self.read(record+0x9C,'B')
        if not (0<=x<width and 0<=y<height) or (width,height)!=(64,96):
            raise RuntimeError('first constructor source logical coordinates/bounds')
        self.constructor_cm = self.read(cm)
        self.constructor_cell = self.constructor_cm+2*(y*width+x)+1
        self.constructor_calls,self.constructor_clears = [],[]
        #467147 is inside467020, whose caller4682C9 is inside4680B0.
        outer_frame = self.read(self.uc.reg_read(UC_X86_REG_EBP))
        if self.read(outer_frame+4)!=0x4533FA:
            raise RuntimeError('first constructor actual outer frame/caller')
        self.constructor_return_sp = outer_frame+12
        return {'work_pointer':work,'record_pointer':record,'index':self.active_index,
            'before_work_hex':bytes(self.uc.mem_read(work,WORK_BYTES)).hex(),
            'record_hex':bytes(self.uc.mem_read(record,176)).hex(),
            'shared_pointer':UNITCTRL+SHARED_OFFSET,
            'before_shared_hex':bytes(self.uc.mem_read(UNITCTRL+SHARED_OFFSET,SHARED_BYTES)).hex(),
            'cm_pointer':cm,'cm_data_pointer':self.constructor_cm,'cm_bytes':width*height*2,
            'before_cm_hex':bytes(self.uc.mem_read(self.constructor_cm,width*height*2)).hex(),
            'cell_counter_pointer':self.constructor_cell,'constructor_coordinates':[x,y],
            'logical_dimensions':[width,height],'return_sp':self.constructor_return_sp}

    def run_constructor(self):
        self.constructor_loading = True
        self.clear_trace('tactical_startup')
        self.stop_reason = None
        self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30_000_000,count=500_000)
        self.constructor_loading = False
        if self.stop_reason!='after_first_unit_constructor_return' or self.handles:
            raise RuntimeError(f'first constructor missed natural return at {self.uc.reg_read(UC_X86_REG_EIP):#x}')

    def resources(self,name,commands=()):
        self.constructor_loading = False
        result = super().resources(name,commands)
        result.update({'first_unit_constructor_completed':False,'first_unit_constructor':None})
        if not result['ready']:
            return result
        snap = self.prepare_constructor()
        logical = result['logical_map']
        if snap['cm_pointer']!=logical['cm_pointer'] or (snap['cm_data_pointer'],snap['cm_bytes'])!=(logical['scratch'][0]['pointer'],logical['scratch'][0]['bytes']) \
            or self.read(UNITCTRL+0x2A304)!=logical['pointer']:
            raise RuntimeError('first constructor logical map/scratch ownership')
        protected = [(CHAR_BASE,0x7F4488-CHAR_BASE),(0x7CF34C,45*0x124),(0x7A528E,4),
            (0x7F4488,UNITS-0x7F4488),(UNITS,len(self.combat_records)*176),(MAP_POOL,69368),
            (snap['record_pointer'],176),(UNIT_POOL,84),(UNITCTRL+CACHE_OFFSET,CACHE_COUNT*8),
            (UNITCTRL+COUNTER_OFFSET,4)]
        protected += [(a['pointer'],a['bytes']) for a in self.asset_allocations+self.animation_allocations if not a['freed']]
        protected += [(self.texture_table+slot*8,8) for slot in (100,110)]
        protected += [(UNITCTRL+o,n*s) for o,n,s,p in WORK_GROUPS]
        protected += [(p['pointer'],p['bytes']) for p in result['logical_map']['scratch'][1:]]
        before = [bytes(self.uc.mem_read(a,n)) for a,n in protected]
        self.run_constructor()
        if before!=[bytes(self.uc.mem_read(a,n)) for a,n in protected]:
            raise RuntimeError('first constructor changed copied/current/persistent/resources')
        prior = bytes.fromhex(snap['before_cm_hex'])
        after = bytes(self.uc.mem_read(snap['cm_data_pointer'],snap['cm_bytes']))
        at = snap['cell_counter_pointer']-snap['cm_data_pointer']
        expected = bytearray(prior)
        if self.read(snap['record_pointer']+0xF,'B')==1:
            expected[at] = (expected[at]+1)&255
        if after!=bytes(expected):
            raise RuntimeError('first constructor unexpected logical cell accounting')
        snap.update({'work_hex':bytes(self.uc.mem_read(snap['work_pointer'],WORK_BYTES)).hex(),
            'shared_hex':bytes(self.uc.mem_read(snap['shared_pointer'],SHARED_BYTES)).hex(),
            'cm_hex':after.hex(),'cm_sha256':hashlib.sha256(after).hexdigest(),
            'calls':deepcopy(self.constructor_calls),'clears':deepcopy(self.constructor_clears),
            'return_va':'0x4533fa','return_eax':self.uc.reg_read(UC_X86_REG_EAX),
            'constructor_completed':True,'unit_animation_work_bound':True,
            'retained_ranges_unchanged':True,'scene_placement_executed':False})
        result.update({'first_unit_constructor_completed':True,'first_unit_constructor':snap,'stop_reason':self.stop_reason})
        result['phases'].append({'phase':'natural_first_unit_constructor_return','coverage':self.coverage()})
        return result


def report():
    e = SchoolFirstUnitConstructorEmulator()
    if not e.run_planning('first_unit_constructor_upstream')['school_data_prepared']:
        raise RuntimeError('actual fifth-school prefix missing')
    ranges = [(BASE,(SOURCE.stat().st_size+0xFFF)&~0xFFF),(TASK,0x120000),(GROUP_TASK,0x60000),
        (STACK,0x10000),(TACT,0x11A000),(SCRIPT_WORK,0x3000),(POOL,POOL_SIZE),(UHEAP,UHEAP_SIZE),
        (SCENE_POOL,SCENE_POOL_SIZE),(ASSET_POOL,ASSET_POOL_SIZE),(MAP_POOL,MAP_POOL_SIZE),
        (UNIT_POOL,UNIT_POOL_SIZE),(ANIM_POOL,ANIM_POOL_SIZE)]
    checkpoint,cpu = [(a,bytes(e.uc.mem_read(a,n))) for a,n in ranges],e.uc.context_save()
    cases = []
    for name,commands in [('initial',()),('student9_waiting',[('student',9,-1)]),
        ('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1),('student',9,-1)]),
        ('teacher_only',[('student',3,-1),('student',4,-1),('student',9,-1)]),('teacher_waiting',[('teacher',101,-1)])]:
        for a,data in checkpoint:
            e.uc.mem_write(a,data)
        e.uc.context_restore(cpu)
        e.stop_reason = None
        cases.append(e.resources(name,commands))
        print('Native first unit constructor '+name+': '+str(cases[-1]['first_unit_constructor_completed']),flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
        'boundary':'Exactly first4680B0 constructor naturally returned at4533FA. Other current/enemy units, VM and scene placement unexecuted. GPU declared; constructor coordinates are not spawn positions.',**AUTHORITY}


if __name__=='__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',required=True)
    args = p.parse_args()
    path = ROOT/args.out
    if path.exists():
        p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
