"""Natural mapcom loading and first current-unit constructor input.

The original constructor is a stop boundary, never a fabricated return value.
Current record preparation is native CPU work; persistent game data is guarded.
"""
import argparse
from copy import deepcopy
import hashlib
import struct
from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_effect_initialization_emulation import (
    SchoolEffectInitializationEmulator, MAPCOM, WORK_GROUPS, ASSET_POOL,
    ASSET_POOL_SIZE, SCENE_POOL, SCENE_POOL_SIZE, UHEAP, UHEAP_SIZE,
    UNITCTRL, FILE_API, FILE_IMPORTS, POOL, POOL_SIZE, TACT, TACT_SIZE,
    SCRIPT_WORK, GROUP_TASK, CHAR_BASE, UNITS, ROOT, SOURCE, SOURCE_SHA256,
    BASE, TASK, STACK, RETURN, report_text, ExitEmulator, AUTHORITY, cstring)

MAP_POOL, MAP_POOL_SIZE = 0x13000000, 0x20000
MAP_OWNER = TACT+0x3EF8
MAP_SHA256 = 'ab98972c8a2d10cf70dd0bb795f2a0f17daaf874f168e7eb97b1c8cf4fe364ed'
NATIVE = ((0x43A510,0x43A63A),)


def map_common_resource():
    path = ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/MAPCOM.BIN'
    raw = path.read_bytes()
    if len(raw) != 69368 or hashlib.sha256(raw).hexdigest() != MAP_SHA256:
        raise ValueError('original mapcom resource differs')
    return raw, {'path':path.relative_to(ROOT).as_posix(),'relative_path':MAPCOM,
                 'bytes':len(raw),'sha256':MAP_SHA256}


class SchoolMapCommonEmulator(SchoolEffectInitializationEmulator):
    def __init__(self):
        self.map_loading = False
        super().__init__()
        self._function_ranges += NATIVE
        observed = {0x4500B0,0x4214F0,0x56D4D0,0x56DDA0,0x4680B0}
        self.map_code = frozenset(a for start,end in self._function_ranges
                                 for a in range(start,end)) - observed
        self.uc.mem_map(MAP_POOL,MAP_POOL_SIZE)
        self.reset_map_common()

    def reset_map_common(self):
        self.map_allocation = None
        self.map_request = None
        self.map_pointer_calls = []
        self.map_file_events = []
        self.map_boundaries = []
        self.current_copies = []
        self.current_constructor_input = None

    def _write_hook(self,uc,access,address,size,value,context):
        if not getattr(self,'map_loading',False):
            return super()._write_hook(uc,access,address,size,value,context)
        allowed = [(STACK,STACK+0x10000),(0,4),(TACT,TACT+TACT_SIZE),
                   (TASK+0x808E8,TASK+0x809EC),(0x7A0EBC,0x7A0FC0)]
        if self.map_allocation and not self.map_allocation['freed']:
            a = self.map_allocation
            allowed.append((a['pointer'],a['pointer']+a['bytes']))
        for index in range(len(self.combat_records)):
            p = UNITS+index*176
            allowed.extend(((p+0xF,p+0x10),(p+0x24,p+0x28)))
        if not any(a <= address and address+size <= b for a,b in allowed):
            raise RuntimeError(f'map common finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        if not STACK <= address < STACK+0x10000:
            self.writes.append((address,size,value & ((1<<(size*8))-1)))
            self.startup_writes.append((address,size))

    def map_file_api(self,address,sp):
        slot,(name,pop) = list(FILE_IMPORTS.items())[(address-FILE_API)//16]
        args = [self.read(sp+4+i*4) for i in range(pop//4)]
        if name == 'CreateFileA':
            if self.map_request is None or self.handles or cstring(self,args[0]) != MAPCOM \
                or args[1:] != [0x80000000,1,0,3,1,0]:
                raise RuntimeError('mapcom read-only file request/order')
            raw,identity = map_common_resource()
            result = 0x7A0
            self.handles[result] = {'raw':raw,'identity':identity}
        elif name == 'ReadFile':
            handle,target,count,written,overlapped = args
            a = self.map_allocation
            if handle not in self.handles or a is None or (target,count,overlapped) != (a['pointer'],a['bytes'],0):
                raise RuntimeError('mapcom file buffer ownership')
            raw = self.handles[handle]['raw']
            self.primitive_write(target,raw)
            self.primitive_write(written,struct.pack('<I',len(raw)))
            self.map_request.update({'loaded':True,'buffer_pointer':target,'loaded_bytes':len(raw),
                'loaded_sha256':hashlib.sha256(bytes(self.uc.mem_read(target,count))).hexdigest()})
            result = 1
        elif name in ('GetCurrentDirectoryA','GetFileSize','CloseHandle'):
            prior = len(self.file_events)
            self._file_api(address,sp)
            self.map_file_events.extend(deepcopy(self.file_events[prior:]))
            return
        else:
            raise RuntimeError('undeclared mapcom file API')
        self.map_file_events.append({'name':name,'import_va':hex(slot),'args':args,'result':result})
        self._stub_return(result,pop)

    def _hook(self,uc,address,size,context):
        if not getattr(self,'map_loading',False):
            return super()._hook(uc,address,size,context)
        if address in self.map_code:
            self.visited.add(address)
            return
        sp,receiver = uc.reg_read(UC_X86_REG_ESP),uc.reg_read(UC_X86_REG_ECX)
        if address == 0x56DDA0:
            raise RuntimeError('unexpected vector construction during mapcom continuation')
        if address == 0x424F80:
            raise RuntimeError(f'unexpected mapcom assertion at {self.read(sp):#x}')
        if FILE_API <= address < FILE_API+len(FILE_IMPORTS)*16 and (address-FILE_API)%16 == 0:
            self.map_file_api(address,sp)
            return
        if address == 0x4500B0:
            if self.map_request or receiver != TASK+0x80000 or self.read(sp) != 0x43A53D \
                or cstring(self,self.read(sp+4)) != MAPCOM:
                raise RuntimeError('natural mapcom resource manager request')
            _,identity = map_common_resource()
            self.map_request = {'source':identity,'receiver':receiver,'caller_return_va':hex(self.read(sp)),'loaded':False}
            self.visited.add(address)
            return
        if address == 0x56D810:
            target,fmt = self.read(sp+4),cstring(self,self.read(sp+8))
            caller = self.read(sp)
            if (target,fmt,caller) == (TASK+0x808E8,'%s%s',0x4500EF) and self.read(sp+12) == TASK+0x80BF4:
                values = (cstring(self,self.read(sp+12)),cstring(self,self.read(sp+16)))
                if values[1] != MAPCOM:
                    raise RuntimeError('mapcom formatted resource path')
            elif (target,fmt,caller) == (0x7A0EBC,'%s',0x42ACB9):
                values = (cstring(self,self.read(sp+12)),)
            else:
                raise RuntimeError('mapcom formatter caller/target')
            raw = (fmt % values).encode('ascii')
            if len(raw) >= 260:
                raise RuntimeError('mapcom format overflow')
            self.primitive_write(target,raw+b'\0')
            self.map_boundaries.append({'kind':'formatter','caller_return_va':hex(caller),'target':target,'value':raw.decode('ascii')})
            self._stub_return(len(raw),0)
            return
        if address == 0x428A40:
            count,caller = self.read(sp+4),self.read(sp)
            if self.map_allocation or caller != 0x42AD54 or not self.handles or count != 69368 or count > MAP_POOL_SIZE:
                raise RuntimeError('mapcom finite file allocation')
            self.map_allocation = {'pointer':MAP_POOL,'bytes':count,'kind':'mapcom_file_buffer',
                                   'caller_return_va':hex(caller),'freed':False}
            self.map_boundaries.append({'kind':'heap_allocation',**self.map_allocation})
            self._stub_return(MAP_POOL,0)
            return
        if address == 0x4214F0:
            buffer,index = self.read(sp+4),self.read(sp+8)
            roots = {0x43A59F:0,0x43A5B3:1,0x43A5CA:2,0x43A5E1:3}
            caller = self.read(sp)
            if self.map_allocation is None or receiver != MAP_OWNER:
                raise RuntimeError('mapcom pointer receiver/ownership')
            if caller in roots:
                valid = buffer == MAP_POOL and index == roots[caller]
            else:
                valid = caller == 0x43A61B and buffer == self.read(MAP_OWNER+4) \
                    and index == len(self.map_pointer_calls)-4 and 0 <= index < 33
            if not valid:
                raise RuntimeError('mapcom source pointer selection/order')
            offset = self.read(buffer+8+index*4)
            self.map_pointer_calls.append({'buffer':buffer,'index':index,'offset':offset,
                'pointer':buffer+offset,'caller_return_va':hex(caller)})
            self.visited.add(address)
            return
        if address == 0x56D4D0:
            target,source,count = [self.read(sp+i) for i in (4,8,12)]
            index = (source-UNITS)//176
            if self.current_copies or self.read(sp) not in (0x4533E5,0x45346C) or count != 176 \
                or not 0 <= index < len(self.combat_records) or source != UNITS+index*176 \
                or target != UNITCTRL+0xD0C2C+index*176:
                raise RuntimeError('first native current record copy')
            raw = bytes(uc.mem_read(source,count))
            self.primitive_write(target,raw)
            self.current_copies.append({'index':index,'source':source,'target':target,'bytes':count,
                'caller_return_va':hex(self.read(sp)),'record_hex':raw.hex(),'sha256':hashlib.sha256(raw).hexdigest()})
            self._stub_return(target,0)
            return
        if address == 0x4680B0:
            index = self.read(sp+4)
            if len(self.current_copies) != 1 or receiver != UNITCTRL or index != self.current_copies[0]['index'] \
                or self.read(sp) not in (0x4533FA,0x453481):
                raise RuntimeError('first current constructor source input')
            self.current_constructor_input = {'va':hex(address),'receiver':receiver,'index':index,
                'caller_return_va':hex(self.read(sp)),'body_executed':False}
            self.stop_reason = 'before_first_current_unit_work_constructor'
            uc.emu_stop()
            return
        if address in (0x451E20,0x415420,0x422360):
            self.map_boundaries.append({'kind':{0x451E20:'loading_screen_render',0x415420:'render_flush',0x422360:'scheduler_yield'}[address],
                'receiver':receiver,'caller_return_va':hex(self.read(sp))})
            self._stub_return(0,4 if address==0x422360 else 0)
            return
        return ExitEmulator._hook(self,uc,address,size,context)

    def resources(self,name,commands=()):
        self.map_loading = False
        self.reset_map_common()
        result = super().resources(name,commands)
        result.update({'map_common_loaded':False,'map_common':None,'current_constructor_input':None,
                       'current_record_preparation':None,'current_copies':[]})
        if not result['ready']:
            return result
        protected = [(CHAR_BASE,0x7F4488-CHAR_BASE),(0x7CF34C,45*0x124),(0x7A528E,4),(0x7F4488,UNITS-0x7F4488)]
        protected += [(a['pointer'],a['bytes']) for a in self.asset_allocations if not a['freed']]
        protected += [(self.texture_table+100*8,8)]
        protected += [(UNITCTRL+o,n*s) for o,n,s,p in WORK_GROUPS]
        before = [bytes(self.uc.mem_read(a,n)) for a,n in protected]
        records_before = [bytes(self.uc.mem_read(UNITS+i*176,176)).hex() for i in range(len(self.combat_records))]
        header = {hex(a):self.read(a,'B') for a in (0x7F448C,0x7F448D,0x7F448F,0x7F4490,0x7F44B8)}
        self.map_loading = True
        self.clear_trace('tactical_startup')
        self.stop_reason = None
        self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30_000_000,count=12_000_000)
        if self.stop_reason != 'before_first_current_unit_work_constructor' or self.handles:
            raise RuntimeError(f'mapcom continuation missed first constructor at {self.uc.reg_read(UC_X86_REG_EIP):#x}')
        if before != [bytes(self.uc.mem_read(a,n)) for a,n in protected]:
            raise RuntimeError('mapcom changed persistent/header/retained effect bytes')
        records_after = [bytes(self.uc.mem_read(UNITS+i*176,176)).hex() for i in range(len(self.combat_records))]
        result.update({'map_common_loaded':True,'map_common':{'request':deepcopy(self.map_request),
            'allocation':deepcopy(self.map_allocation),'owner':MAP_OWNER,
            'top_level_pointers':[self.read(MAP_OWNER+o) for o in (4,0x8C,0x90,0x94)],
            'nested_pointers':[self.read(MAP_OWNER+8+i*4) for i in range(33)],
            'retained_buffer_sha256':hashlib.sha256(bytes(self.uc.mem_read(MAP_POOL,69368))).hexdigest(),
            'pointer_calls':deepcopy(self.map_pointer_calls),'file_events':deepcopy(self.map_file_events),
            'boundaries':deepcopy(self.map_boundaries),'open_handles':len(self.handles)},
            'current_record_preparation':{'header':header,'before_records':records_before,'after_records':records_after,
                'allowed_changed_offsets':[0xF,0x24,0x25,0x26,0x27]},
            'current_copies':deepcopy(self.current_copies),'current_constructor_input':deepcopy(self.current_constructor_input),
            'current_combat_records_unchanged':records_before==records_after,
            'map_common_persistent_and_effect_bytes_unchanged':True,'stop_reason':self.stop_reason})
        result['phases'].append({'phase':'natural_map_common_and_first_current_input','coverage':self.coverage()})
        self.map_loading = False
        return result


def report():
    e = SchoolMapCommonEmulator()
    if not e.run_planning('map_common_upstream')['school_data_prepared']:
        raise RuntimeError('actual fifth-school prefix missing')
    ranges = [(BASE,(SOURCE.stat().st_size+0xFFF)&~0xFFF),(TASK,0x120000),(GROUP_TASK,0x60000),
              (STACK,0x10000),(TACT,0x11A000),(SCRIPT_WORK,0x3000),(POOL,POOL_SIZE),
              (UHEAP,UHEAP_SIZE),(SCENE_POOL,SCENE_POOL_SIZE),(ASSET_POOL,ASSET_POOL_SIZE),(MAP_POOL,MAP_POOL_SIZE)]
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
        print('Native map common '+name+': '+str(cases[-1]['map_common_loaded']),flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
        'boundary':'Original mapcom/current preparation/first record copy executed; first4680B0 body, enemy work, VM and placement unexecuted; GPU declared.',**AUTHORITY}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',required=True)
    args = p.parse_args()
    path = ROOT/args.out
    if path.exists():
        p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
