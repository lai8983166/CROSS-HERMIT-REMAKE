"""Natural effect texture binding and work initialization, before mapcom load.

Original CPU functions execute. GPU operations remain declared external
boundaries, never live proof. The source explicitly selects texture slot100.
"""
import argparse
from copy import deepcopy
import hashlib
import struct
from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_unit_assets_emulation import (
    SchoolUnitAssetsEmulator, effect_resource, ASSET_POOL, ASSET_POOL_SIZE,
    SCENE_POOL, SCENE_POOL_SIZE, UHEAP, UHEAP_SIZE, UNITCTRL, FILE_API,
    FILE_IMPORTS, POOL, POOL_SIZE, TACT, TACT_SIZE, SCRIPT_WORK, GROUP_TASK,
    CHAR_BASE, UNITS, ROOT, SOURCE, SOURCE_SHA256, BASE, TASK, STACK,
    RETURN, report_text, ExitEmulator, AUTHORITY, cstring)

NATIVE = ((0x41EB70,0x41EBE9),(0x41EBF0,0x41EC40),(0x41EC40,0x41ECFE),
          (0x41EFD0,0x41F089),(0x40B960,0x40B98F),(0x409EF0,0x409F6F),
          (0x409F70,0x409FA3),(0x409FB0,0x409FE7),(0x409FF0,0x40A0FD),
          (0x40A400,0x40A520),(0x40A520,0x40A7E6),(0x415070,0x415099),
          (0x466500,0x4665BD),(0x4937A0,0x493857),(0x451D80,0x451E19),
          (0x43A510,0x43A53D))
WORK_GROUPS = ((0x109340,10,0x520,0),(0x10C680,10,0x520,0),(0x116254,5,0x524,4))
MAPCOM = 'data\\Tactics\\mapcom.bin'


class SchoolEffectInitializationEmulator(SchoolUnitAssetsEmulator):
    def __init__(self):
        self.effect_loading = False
        super().__init__()
        self._function_ranges += NATIVE
        observed_entries = {0x41F340,0x409EF0,0x409FF0,0x4500B0,0x56DDA0}
        self.effect_code = frozenset(a for start,end in self._function_ranges for a in range(start,end)) - observed_entries
        self.reset_effect()

    def reset_effect(self):
        self.effect_entries = []
        self.effect_boundaries = []
        self.effect_resets = []
        self.effect_work_calls = []
        self.mapcom_request = None
        self.effect_graphics_input = None
        self.effect_vector = None
        self.effect_animation_request = None

    def _write_hook(self,uc,access,address,size,value,context):
        if not getattr(self,'effect_loading',False):
            return super()._write_hook(uc,access,address,size,value,context)
        allowed = [(STACK,STACK+0x10000),(0,4),(TACT,TACT+TACT_SIZE),
                   (self.texture_table+100*8,self.texture_table+101*8)]
        allowed += [(a['pointer'],a['pointer']+a['bytes']) for a in self.asset_allocations if not a['freed']]
        if not any(a <= address and address+size <= b for a,b in allowed):
            raise RuntimeError(f'effect finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        if not STACK <= address < STACK+0x10000:
            self.writes.append((address,size,value & ((1<<(size*8))-1)))
            self.startup_writes.append((address,size))

    def _hook(self,uc,address,size,context):
        if not getattr(self,'effect_loading',False):
            return super()._hook(uc,address,size,context)
        if address in self.effect_code:
            self.visited.add(address)
            return
        sp,receiver = uc.reg_read(UC_X86_REG_ESP),uc.reg_read(UC_X86_REG_ECX)
        if address == 0x424F80:
            raise RuntimeError(f'unexpected effect assertion at caller {self.read(sp):#x}')
        if address == 0x428A40:
            count,caller = self.read(sp+4),self.read(sp)
            if caller != 0x41F142 or count != 1959*84+4:
                raise RuntimeError('effect texture allocation caller/count')
            self._stub_return(self.asset_allocate(count,'effect_texture_array',caller),0)
            return
        if address == 0x428AD0:
            pointer = self.read(sp+4)
            match = [a for a in self.asset_allocations if a['pointer']==pointer and not a['freed']]
            if len(match) != 1 or match[0]['kind'] != 'effect_file_buffer' or len(self.effect_entries) != 1959:
                raise RuntimeError('effect source free ownership/order')
            match[0]['freed'] = True
            self.effect_boundaries.append({'kind':'source_file_release','pointer':pointer,'caller_return_va':hex(self.read(sp))})
            self._stub_return(0,0)
            return
        if address == 0x56DDA0:
            args = tuple(self.read(sp+i) for i in (4,8,12,16,20))
            a = self.asset_allocations[-1]
            if a['kind'] != 'effect_texture_array' or args != (a['pointer']+4,84,1959,0x41F830,0x41F890):
                raise RuntimeError('effect bounded texture vector')
            self.vector_pending = args[:4]
            self.effect_vector = {'target':args[0],'stride':args[1],'count':args[2],
                'constructor_va':hex(args[3]),'destructor_va':hex(args[4]),
                'native_constructors_completed':0,'iteration_outside_instruction_hook':True}
            self.stop_reason = 'effect_texture_vector'
            uc.emu_stop()
            return
        if address == 0x56CEC0:
            target,byte,count = [self.read(sp+i) for i in (4,8,12)]
            caller = self.read(sp)
            textures = [a for a in self.asset_allocations if a['kind']=='effect_texture_array']
            is_texture = count == 4 and any(a['pointer']+4 <= target and target+count <= a['pointer']+a['bytes'] for a in textures)
            offset = target-UNITCTRL
            is_group = (offset,count,caller) in ((0x109340,0x3340,0x46616D),(0x10C680,0x3340,0x46653E))
            is_tail = count==0x524 and caller==0x4937F5 and offset in [0x116254+i*0x524 for i in range(5)]
            anims = [UNITCTRL+o+i*s+p+0x48 for o,n,s,p in WORK_GROUPS for i in range(n)]
            is_anim = count==0x58 and caller==0x409F1A and target in anims
            if byte != 0 or not (is_texture or is_group or is_tail or is_anim):
                raise RuntimeError(f'effect clear primitive {target:#x}/{count} caller {caller:#x}')
            self.primitive_write(target,bytes(count))
            if not is_texture:
                self.effect_resets.append({'target':target,'bytes':count,'caller_return_va':hex(caller)})
            self._stub_return(target,0)
            return
        if address == 0x41F340:
            device,buffer,index,records,left,right = [self.read(sp+i) for i in (4,8,12,16,20,24)]
            owned = {a['kind']:a for a in self.asset_allocations}
            if device != 0 or buffer != owned['effect_file_buffer']['pointer']+77212 or index != len(self.effect_entries) or index >= 1959 \
                or records != owned['effect_texture_array']['pointer']+4 or (left,right) != (0,0):
                raise RuntimeError('effect texture source/order/record')
            offset = self.read(buffer+8+index*4)
            end = self.read(buffer+8+(index+1)*4) if index<1958 else self.read(buffer)
            if not 8+1959*4 <= offset < end <= owned['effect_file_buffer']['bytes']-77212:
                raise RuntimeError('effect texture offset bounds')
            self.active_texture = {'index':index,'offset':offset,'file_offset':77212+offset,
                'bytes':end-offset,'header_hex':bytes(uc.mem_read(buffer+offset,min(16,end-offset))).hex(),
                'record_pointer':records+index*84}
            self.effect_entries.append(self.active_texture)
        if address == 0x403BD0:
            if receiver != self.active_texture['record_pointer']:
                raise RuntimeError('effect GPU creation receiver')
            self.effect_boundaries.append({'kind':'texture_creation','index':self.active_texture['index'],
                'width':self.read(receiver+0x38,'H'),'height':self.read(receiver+0x3A,'H'),'format':self.read(receiver+0x34)})
            self._stub_return(0,8)
            return
        if address in (0x404150,0x404690,0x4046F0):
            if receiver != self.active_texture['record_pointer']:
                raise RuntimeError('effect GPU upload receiver')
            self.effect_boundaries.append({'kind':'pixel_upload','va':hex(address),'index':self.active_texture['index']})
            self._stub_return(0,16 if address==0x404150 else 12)
            return
        if address == 0x56E260:
            left,right,count = [self.read(sp+i) for i in (4,8,12)]
            if count != 13 or cstring(self,right) != 'Dm-No-MakeTex':
                raise RuntimeError('effect marker comparison')
            a,b = bytes(uc.mem_read(left,count)),bytes(uc.mem_read(right,count))
            self._stub_return((a>b)-(a<b),0)
            return
        if FILE_API <= address < FILE_API+len(FILE_IMPORTS)*16 and (address-FILE_API)%16 == 0:
            name = list(FILE_IMPORTS.values())[(address-FILE_API)//16][0]
            if name != 'lstrlenA' or cstring(self,self.read(sp+4)) != 'Dm-No-MakeTex':
                raise RuntimeError('unexpected effect file API')
            self._stub_return(13,4)
            return
        if address == 0x409EF0:
            self.effect_work_calls.append({'receiver':receiver,'animation_work':self.read(sp+4),'caller_return_va':hex(self.read(sp))})
        if address == 0x409FF0:
            args = [self.read(sp+4+i*4) for i in range(4)]
            if receiver != self.effect_controller or args != [UNITCTRL+0x109388,1,65,0]:
                raise RuntimeError('initial source effect animation selection')
            self.effect_animation_request = {'receiver':receiver,'args':args,'caller_return_va':hex(self.read(sp))}
        if address in (0x451E20,0x415420,0x422360):
            self.effect_boundaries.append({'kind':{0x451E20:'loading_screen_render',0x415420:'render_flush',0x422360:'scheduler_yield'}[address],
                'receiver':receiver,'caller_return_va':hex(self.read(sp))})
            self._stub_return(0,4 if address==0x422360 else 0)
            return
        if address == 0x4500B0:
            if receiver != TASK+0x80000 or cstring(self,self.read(sp+4)) != MAPCOM or self.read(sp) != 0x43A53D:
                raise RuntimeError('following source mapcom request')
            self.mapcom_request = {'relative_path':MAPCOM,'caller_return_va':'0x43a53d','receiver':receiver,'loaded':False}
            self.stop_reason = 'before_mapcom_resource_load'
            uc.emu_stop()
            return
        return ExitEmulator._hook(self,uc,address,size,context)

    def run_effect_thread(self):
        vectors = 0
        batches = 0
        self.stop_reason = None
        while True:
            self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30_000_000,count=12_000_000)
            if self.stop_reason != 'effect_texture_vector':
                if self.stop_reason is None and self.uc.reg_read(UC_X86_REG_EIP) != RETURN:
                    batches += 1
                    if batches > 12:
                        raise RuntimeError('effect CPU exceeded bounded continuation batches')
                    continue
                break
            vectors += 1
            if vectors != 1:
                raise RuntimeError('unexpected extra effect texture vector')
            target,stride,count,ctor = self.vector_pending
            cpu,stack = self.uc.context_save(),bytes(self.uc.mem_read(STACK,0x10000))
            for i in range(count):
                self.call(ctor,receiver=target+i*stride)
                self.effect_vector['native_constructors_completed'] += 1
            self.uc.mem_write(STACK,stack)
            self.uc.context_restore(cpu)
            self._stub_return(0,20)
            self.stop_reason = None
        if self.stop_reason != 'before_mapcom_resource_load' or self.handles:
            raise RuntimeError(f'effect missed mapcom boundary at {self.uc.reg_read(UC_X86_REG_EIP):#x}')

    def effect_snapshot(self):
        for entry in self.effect_entries:
            p = entry['record_pointer']
            entry.update({'width':self.read(p+0x38,'H'),'height':self.read(p+0x3A,'H'),
                          'format':self.read(p+0x34),'raw_record_hex':bytes(self.uc.mem_read(p,84)).hex()})
        groups = []
        for offset,count,stride,prefix in WORK_GROUPS:
            entries = []
            for i in range(count):
                p = UNITCTRL+offset+i*stride+prefix
                entries.append({'index':i,'pointer':p,'used':self.read(p,'H'),'controller':self.read(p+0x44),
                                'animation_work_pointer':p+0x48,'animation_work_hex':bytes(self.uc.mem_read(p+0x48,0x58)).hex()})
            groups.append({'offset':hex(offset),'count':count,'stride':stride,'prefix':prefix,'entries':entries})
        aw = UNITCTRL+0x109388
        instruction = self.read(aw+4)
        metadata = self.read(self.effect_controller)
        return {'controller':self.effect_controller,'texture_slot':self.read(self.effect_controller+0x28),
                'texture_table':self.read(self.effect_controller+0x24),'texture_records':self.read(self.texture_table+100*8),
                'texture_count':self.read(self.texture_table+100*8+4),'mode_field':self.read(self.effect_controller+0x40),
                'metadata_pointer':metadata,'metadata_sha256':hashlib.sha256(bytes(self.uc.mem_read(metadata,77212))).hexdigest(),
                'source_file_buffer_freed':next(a['freed'] for a in self.asset_allocations if a['kind']=='effect_file_buffer'),
                'groups':groups,'animation_request':deepcopy(self.effect_animation_request),
                'initial_animation':{'instruction_pointer':instruction,'metadata_offset':instruction-metadata,
                    'instruction_hex':bytes(self.uc.mem_read(instruction,10)).hex(),'duration':self.read(aw+0xE,'H'),
                    'descriptor_value':self.read(aw+0x18),'self_pointer':self.read(aw+0x24),'current_instruction':self.read(aw+0x28)},
                'tail_work_index':self.read(UNITCTRL+0x116250),'mapcom_request':deepcopy(self.mapcom_request)}

    def resources(self,name,commands=()):
        self.effect_loading = False
        self.reset_effect()
        result = super().resources(name,commands)
        result.update({'effect_initialized':False,'effect_initialization':None,'effect_entries':[],'effect_boundaries':[]})
        if result['ready']:
            protected = [(CHAR_BASE,0x7F4488-CHAR_BASE),(0x7CF34C,45*0x124),(0x7A528E,4),(UNITS,len(self.combat_records)*176)]
            before = [bytes(self.uc.mem_read(a,n)) for a,n in protected]
            prior = bytes(self.uc.mem_read(self.texture_table+100*8,8))
            if prior != bytes(8) or self.read(self.effect_controller+0x28) != 100:
                raise RuntimeError('source effect slot100 differs or is not declared empty')
            self.effect_graphics_input = {'slot':100,'previous_slot_hex':prior.hex(),
                'scope':'Prior isolated renderer input; original4660FC selects slot100, bypassing41EFD0. Full renderer constructor/GPU remain boundaries.'}
            self.effect_loading = True
            self.clear_trace('tactical_startup')
            self.run_effect_thread()
            if before != [bytes(self.uc.mem_read(a,n)) for a,n in protected]:
                raise RuntimeError('effect initialization changed current/persistent records')
            result.update({'effect_initialized':True,'effect_initialization':self.effect_snapshot(),
                'effect_entries':deepcopy(self.effect_entries),'effect_boundaries':deepcopy(self.effect_boundaries),
                'effect_resets':deepcopy(self.effect_resets),'effect_work_calls':deepcopy(self.effect_work_calls),
                'effect_vector':deepcopy(self.effect_vector),
                'effect_graphics_input':deepcopy(self.effect_graphics_input),'asset_allocations':deepcopy(self.asset_allocations),
                'stop_reason':self.stop_reason})
            result['phases'].append({'phase':'natural_effect_texture_work_initialization','coverage':self.coverage()})
            self.effect_loading = False
        return result


def report():
    e = SchoolEffectInitializationEmulator()
    if not e.run_planning('effect_initialization_upstream')['school_data_prepared']:
        raise RuntimeError('actual fifth-school prefix missing')
    ranges = [(BASE,(SOURCE.stat().st_size+0xFFF)&~0xFFF),(TASK,0x120000),(GROUP_TASK,0x60000),
              (STACK,0x10000),(TACT,0x11A000),(SCRIPT_WORK,0x3000),(POOL,POOL_SIZE),
              (UHEAP,UHEAP_SIZE),(SCENE_POOL,SCENE_POOL_SIZE),(ASSET_POOL,ASSET_POOL_SIZE)]
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
        print('Native effect initialization '+name+': '+str(cases[-1]['effect_initialized']),flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
        'boundary':'Original effect texture/work initialization executed; GPU declared; mapcom/current units/enemies/VM/placement unexecuted.',**AUTHORITY}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',required=True)
    args = p.parse_args()
    path = ROOT/args.out
    if path.exists():
        p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
