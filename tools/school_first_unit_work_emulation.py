"""First current-unit work/status/cache prefix on the actual school CPU.

Stop at the original unit-art request: no constructor success or unit appearance.
"""
import argparse
from copy import deepcopy
import hashlib
import struct
from unicorn.x86_const import UC_X86_REG_ECX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_map_common_emulation import (
    SchoolMapCommonEmulator,MAP_POOL,MAP_POOL_SIZE,MAP_OWNER,WORK_GROUPS,
    ASSET_POOL,ASSET_POOL_SIZE,SCENE_POOL,SCENE_POOL_SIZE,UHEAP,UHEAP_SIZE,
    UNITCTRL,POOL,POOL_SIZE,TACT,TACT_SIZE,SCRIPT_WORK,GROUP_TASK,CHAR_BASE,
    UNITS,ROOT,SOURCE,SOURCE_SHA256,BASE,TASK,STACK,RETURN,report_text,
    ExitEmulator,AUTHORITY,cstring)

UNIT_POOL,UNIT_POOL_SIZE = 0x14000000,0x10000
WORK_OFFSET,WORK_BYTES,RECORD_OFFSET = 0x80AEC,0x520,0xD0C2C
CACHE_OFFSET,CACHE_COUNT,COUNTER_OFFSET = 0x2A6F0,512,0x2E6F0
NATIVE = ((0x4680B0,0x4682C9),(0x46C040,0x46C0F4),
    (0x474FB0,0x4750AA),(0x4750B0,0x475137),(0x475370,0x4753E6),
    (0x475650,0x475694),(0x468D10,0x468D7D),(0x468D80,0x468E03),
    (0x468E10,0x468EA5),(0x468EB0,0x468F3D),(0x437D10,0x437D83),
    (0x437D90,0x437E3E),(0x467020,0x467147),(0x46A430,0x46A4BD),
    (0x466E20,0x466E90),(0x466E90,0x466F00),(0x466DA0,0x466E20),
    (0x466B40,0x466C78),(0x466C80,0x466D4E),(0x464EB0,0x464F1F))


class SchoolFirstUnitWorkEmulator(SchoolMapCommonEmulator):
    def __init__(self):
        self.first_unit_loading = False
        super().__init__()
        self._function_ranges += NATIVE
        observed = {0x4680B0,0x467020,0x466C80,0x464D70,0x4500B0,
                    0x56CEC0,0x428A40,0x424F80,0x56DDA0}
        self.first_unit_code = frozenset(a for start,end in self._function_ranges
                                        for a in range(start,end)) - observed
        self.uc.mem_map(UNIT_POOL,UNIT_POOL_SIZE)
        self.reset_first_unit()

    def reset_first_unit(self):
        self.active_index = None
        self.unit_allocation = None
        self.unit_cache_input = None
        self.unit_request = None
        self.unit_calls = []
        self.unit_boundaries = []

    def _write_hook(self,uc,access,address,size,value,context):
        if not getattr(self,'first_unit_loading',False):
            return super()._write_hook(uc,access,address,size,value,context)
        allowed = [(STACK,STACK+0x10000),(0,4)]
        if self.active_index is not None:
            work = UNITCTRL+WORK_OFFSET+self.active_index*WORK_BYTES
            record = UNITCTRL+RECORD_OFFSET+self.active_index*176
            allowed += [(work,work+WORK_BYTES),(record,record+176),
                        (UNITCTRL+CACHE_OFFSET,UNITCTRL+CACHE_OFFSET+8),
                        (UNITCTRL+COUNTER_OFFSET,UNITCTRL+COUNTER_OFFSET+4)]
        if self.unit_allocation and not self.unit_allocation['freed']:
            a = self.unit_allocation
            allowed.append((a['pointer'],a['pointer']+a['bytes']))
        if not any(a <= address and address+size <= b for a,b in allowed):
            raise RuntimeError(f'first unit finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        if not STACK <= address < STACK+0x10000:
            self.writes.append((address,size,value & ((1<<(size*8))-1)))
            self.startup_writes.append((address,size))

    def _hook(self,uc,address,size,context):
        if not getattr(self,'first_unit_loading',False):
            return super()._hook(uc,address,size,context)
        if address in self.first_unit_code:
            self.visited.add(address)
            return
        sp,receiver = uc.reg_read(UC_X86_REG_ESP),uc.reg_read(UC_X86_REG_ECX)
        if address in (0x424F80,0x56DDA0):
            raise RuntimeError(f'unexpected first unit assertion/vector at {address:#x}')
        work = UNITCTRL+WORK_OFFSET+self.active_index*WORK_BYTES
        record = UNITCTRL+RECORD_OFFSET+self.active_index*176
        if address == 0x4680B0:
            if receiver != UNITCTRL or self.read(sp+4) != self.active_index or self.read(work,'H') != 0:
                raise RuntimeError('first current work constructor ownership/input')
            self.unit_calls.append({'va':hex(address),'receiver':receiver,'index':self.active_index,'caller_return_va':hex(self.read(sp))})
            self.visited.add(address)
            return
        if address == 0x56CEC0:
            target,byte,count = [self.read(sp+i) for i in (4,8,12)]
            if byte != 0 or (target,count,self.read(sp)) not in ((work,WORK_BYTES,0x46815A),(work+0x290,0x5C,0x474FE5)):
                raise RuntimeError('first unit exact clear primitive')
            self.primitive_write(target,bytes(count))
            self.unit_boundaries.append({'kind':'clear','target':target,'bytes':count,'caller_return_va':hex(self.read(sp))})
            self._stub_return(target,0)
            return
        if address == 0x428A40:
            if self.unit_allocation or (self.read(sp+4),self.read(sp)) != (84,0x466BB8):
                raise RuntimeError('first unit cache/controller allocation')
            self.unit_allocation = {'pointer':UNIT_POOL,'bytes':84,'kind':'unit_animation_controller','freed':False,
                                    'caller_return_va':hex(self.read(sp))}
            self.unit_boundaries.append({'kind':'heap_allocation',**self.unit_allocation})
            self._stub_return(UNIT_POOL,0)
            return
        if address == 0x467020:
            if receiver != UNITCTRL or [self.read(sp+4),self.read(sp+8)] != [work,self.read(record+0xC,'H')]:
                raise RuntimeError('first unit original job selection')
            self.unit_calls.append({'va':hex(address),'receiver':receiver,'work':work,'job':self.read(sp+8),'caller_return_va':hex(self.read(sp))})
            self.visited.add(address)
            return
        if address == 0x466C80:
            args = [self.read(sp+4+i*4) for i in range(3)]
            if receiver != UNITCTRL or not self.unit_allocation or args[0] != UNITCTRL+CACHE_OFFSET:
                raise RuntimeError('first unit source cache allocation/selection')
            self.unit_calls.append({'va':hex(address),'receiver':receiver,'args':args,'caller_return_va':hex(self.read(sp))})
            self.visited.add(address)
            return
        if address == 0x464D70:
            args = [self.read(sp+4),self.read(sp+8)]
            if self.unit_allocation is None or receiver != UNIT_POOL or args != [TASK,self.read(record+0xC,'H')+8]:
                raise RuntimeError('first unit animation controller binding')
            self.unit_calls.append({'va':hex(address),'receiver':receiver,'args':args,'caller_return_va':hex(self.read(sp))})
            self.visited.add(address)
            return
        if address == 0x42B2D0:
            fmt = cstring(self,self.read(sp+4))
            args = [self.read(sp+8+i*4) for i in range(3)]
            if self.read(sp) != 0x467134 or fmt != 'char:%03d, job:%03d : palette:%03d\n' \
                or args[:2] != [self.read(record+2,'H'),self.read(record+0xC,'H')]:
                raise RuntimeError('first unit exact debug output')
            self.unit_boundaries.append({'kind':'debug_log','format':fmt,'args':args,'text':fmt % tuple(args)})
            self._stub_return(0,0)
            return
        if address == 0x4500B0:
            args = [self.read(sp+4+i*4) for i in range(4)]
            job = self.read(record+0xC,'H')
            if self.unit_allocation is None or receiver != TASK+0x80000 or self.read(sp) != 0x464F1F \
                or args[0] != self.read(0x610538+job*8) or self.unit_request is not None:
                raise RuntimeError('first unit natural art request')
            self.unit_request = {'receiver':receiver,'caller_return_va':hex(self.read(sp)),
                'args':args,'relative_path':cstring(self,args[0]),'loaded':False}
            self.stop_reason = 'before_first_unit_animation_resource_load'
            uc.emu_stop()
            return
        return ExitEmulator._hook(self,uc,address,size,context)

    def resources(self,name,commands=()):
        self.first_unit_loading = False
        self.reset_first_unit()
        result = super().resources(name,commands)
        result.update({'first_unit_work_prefix_initialized':False,'first_unit_work':None})
        if not result['ready']:
            return result
        self.active_index = result['current_constructor_input']['index']
        work = UNITCTRL+WORK_OFFSET+self.active_index*WORK_BYTES
        record = UNITCTRL+RECORD_OFFSET+self.active_index*176
        protected = [(CHAR_BASE,0x7F4488-CHAR_BASE),(0x7CF34C,45*0x124),(0x7A528E,4),
            (0x7F4488,UNITS-0x7F4488),(UNITS,len(self.combat_records)*176),(MAP_POOL,69368)]
        protected += [(a['pointer'],a['bytes']) for a in self.asset_allocations if not a['freed']]
        protected += [(self.texture_table+100*8,8)]
        protected += [(UNITCTRL+o,n*s) for o,n,s,p in WORK_GROUPS]
        before = [bytes(self.uc.mem_read(a,n)) for a,n in protected]
        prior_work = bytes(self.uc.mem_read(work,WORK_BYTES))
        prior_record = bytes(self.uc.mem_read(record,176))
        cache = bytes(self.uc.mem_read(UNITCTRL+CACHE_OFFSET,CACHE_COUNT*8))
        if prior_work != bytes(WORK_BYTES) or cache != bytes(CACHE_COUNT*8):
            raise RuntimeError('first unit original reset work/cache differs')
        self.unit_cache_input = {'previous_cache_sha256':hashlib.sha256(cache).hexdigest(),
            'previous_cache_hex':cache.hex(),'previous_counter':self.read(UNITCTRL+COUNTER_OFFSET),
            'classification_selector':self.read(UNITCTRL+0x2EF44,'B'),
            'graphics_context_hex':bytes(self.uc.mem_read(UNITCTRL+0x2A634,0xB4)).hex()}
        self.first_unit_loading = True
        self.clear_trace('tactical_startup')
        self.stop_reason = None
        self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30_000_000,count=12_000_000)
        if self.stop_reason != 'before_first_unit_animation_resource_load' or self.handles:
            raise RuntimeError(f'first unit missed art boundary at {self.uc.reg_read(UC_X86_REG_EIP):#x}')
        if before != [bytes(self.uc.mem_read(a,n)) for a,n in protected]:
            raise RuntimeError('first unit changed current/persistent/map/effect bytes')
        snapshot = {'index':self.active_index,'work_pointer':work,'record_pointer':record,
            'before_work_hex':prior_work.hex(),'work_hex':bytes(self.uc.mem_read(work,WORK_BYTES)).hex(),
            'before_record_hex':prior_record.hex(),'record_hex':bytes(self.uc.mem_read(record,176)).hex(),
            'cache_input':deepcopy(self.unit_cache_input),
            'cache_hex':bytes(self.uc.mem_read(UNITCTRL+CACHE_OFFSET,CACHE_COUNT*8)).hex(),
            'counter':self.read(UNITCTRL+COUNTER_OFFSET),'allocation':deepcopy(self.unit_allocation),
            'controller_hex':bytes(self.uc.mem_read(UNIT_POOL,84)).hex(),
            'calls':deepcopy(self.unit_calls),'boundaries':deepcopy(self.unit_boundaries),
            'resource_request':deepcopy(self.unit_request),'constructor_completed':False,
            'current_persistent_map_effect_bytes_unchanged':True}
        result.update({'first_unit_work_prefix_initialized':True,'first_unit_work':snapshot,'stop_reason':self.stop_reason})
        result['phases'].append({'phase':'natural_first_unit_work_cache_request','coverage':self.coverage()})
        self.first_unit_loading = False
        return result


def report():
    e = SchoolFirstUnitWorkEmulator()
    if not e.run_planning('first_unit_work_upstream')['school_data_prepared']:
        raise RuntimeError('actual fifth-school prefix missing')
    ranges = [(BASE,(SOURCE.stat().st_size+0xFFF)&~0xFFF),(TASK,0x120000),(GROUP_TASK,0x60000),
        (STACK,0x10000),(TACT,0x11A000),(SCRIPT_WORK,0x3000),(POOL,POOL_SIZE),
        (UHEAP,UHEAP_SIZE),(SCENE_POOL,SCENE_POOL_SIZE),(ASSET_POOL,ASSET_POOL_SIZE),
        (MAP_POOL,MAP_POOL_SIZE),(UNIT_POOL,UNIT_POOL_SIZE)]
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
        print('Native first unit work '+name+': '+str(cases[-1]['first_unit_work_prefix_initialized']),flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
        'boundary':'Original first4680B0 work/status/cache/controller prefix executed; unit art loading, constructor tail, remaining current/enemy work, VM/placement unexecuted; GPU declared.',**AUTHORITY}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',required=True)
    args = p.parse_args()
    path = ROOT/args.out
    if path.exists():
        p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
