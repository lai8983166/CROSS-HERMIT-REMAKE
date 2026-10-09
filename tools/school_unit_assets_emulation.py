"""Natural current-school unit reset and effect animation metadata preparation.

Text rasterization is an explicit platform success boundary, with no fabricated
pixels or GPU objects. Stops before original effect texture binding41EBF0.
"""
import argparse
from copy import deepcopy
import hashlib
import struct
from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_scene_resources_emulation import SchoolSceneResourcesEmulator, SCENE_POOL, SCENE_POOL_SIZE
from tools.school_unitctrl_map_emulation import UHEAP, UHEAP_SIZE, UNITCTRL
from tools.school_tactical_resources_emulation import FILE_API, FILE_IMPORTS, POOL, POOL_SIZE
from tools.school_tactical_startup_emulation import TACT, TACT_SIZE, SCRIPT_WORK, cstring
from tools.school_adventure_handoff_emulation import GROUP_TASK
from tools.school_combat_records_emulation import CHAR_BASE, UNITS
from tools.school_course_unlock_emulation import AUTHORITY
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, BASE, TASK, STACK, RETURN, report_text, ExitEmulator

ASSET_POOL, ASSET_POOL_SIZE = 0x11000000, 0x1100000
EFFECT_PATH = 'data\\DxAnim\\Efct.bin'
EFFECT_SHA = '9c0a8896610e8168f324bc0ca91bc7e860024a8e54cf713db8ad33c2f8906106'
TEXT_GROUPS = ((0x617F40,64,0xDE930),(0x6162AC,512,0xE0930),
               (0x616AAC,512,0xF0930),(0x617AAC,256,0x100930))
RESET_RANGES = ((0x2A6E8,8),(0x2A6F0,0x1000),(0x80AEC,0x50140),
                (0xD0C2C,44000),(0xDB86C,0xAA0),(0x115CBA,0x5A),
                (0x2E714,0x800),(0x2C6F0,0x2000))
NATIVE = ((0x467EB0,0x4680AB),(0x468BC0,0x468BFB),(0x468CD0,0x468D12),
          (0x4671F0,0x46731F),(0x467380,0x4674B5),(0x467520,0x467655),
          (0x4676C0,0x4677E5),(0x4677F0,0x467850),(0x4674C0,0x467520),
          (0x467660,0x4676C0),(0x408E30,0x408E94),(0x466000,0x4662B0),
          (0x464C60,0x464CC0),(0x409900,0x4099E8),(0x41EAD0,0x41EB25),
          (0x464D70,0x464DD7),(0x464DE0,0x464EA7),(0x409B70,0x409E7C),
          (0x409A70,0x409AD0))


def effect_resource():
    path = ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/DXANIM/EFCT.BIN'
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EFFECT_SHA:
        raise ValueError('effect original source identity differs')
    return raw, {'relative_path':EFFECT_PATH,'local_file':path.relative_to(ROOT).as_posix(),
                 'bytes':len(raw),'sha256':EFFECT_SHA}


def text_bytes(e, pointer):
    raw = bytes(e.uc.mem_read(pointer,1024))
    if b'\0' not in raw:
        raise RuntimeError('unterminated original text')
    return raw.split(b'\0',1)[0]


class SchoolUnitAssetsEmulator(SchoolSceneResourcesEmulator):
    def __init__(self):
        self.unit_loading = False
        super().__init__()
        self._function_ranges += NATIVE
        self.uc.mem_map(ASSET_POOL,ASSET_POOL_SIZE)
        self.reset_assets()

    def reset_assets(self):
        self.asset_cursor = ASSET_POOL
        self.asset_allocations = []
        self.asset_requests = []
        self.text_requests = []
        self.asset_boundaries = []
        self.effect_controller = None
        self.texture_binding = None
        self.reset_snapshot = None

    def _write_hook(self,uc,access,address,size,value,context):
        if not getattr(self,'unit_loading',False):
            return super()._write_hook(uc,access,address,size,value,context)
        if STACK <= address and address+size <= STACK+0x10000:
            return
        allowed = [(0,4),(TACT,TACT+TACT_SIZE),(TASK+0x808E8,TASK+0x809EC),(0x7A0EBC,0x7A0FC0)]
        allowed += [(a['pointer'],a['pointer']+a['bytes']) for a in self.asset_allocations if not a['freed']]
        if not any(a <= address and address+size <= b for a,b in allowed):
            raise RuntimeError(f'unit assets finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        self.writes.append((address,size,value & ((1<<(size*8))-1)))
        self.startup_writes.append((address,size))

    def asset_allocate(self,count,kind,caller):
        pointer = self.asset_cursor
        end = pointer+((count+15)&~15)
        if count <= 0 or end > ASSET_POOL+ASSET_POOL_SIZE:
            raise RuntimeError('unit assets allocation bounds')
        self.asset_cursor = end
        self.asset_allocations.append({'pointer':pointer,'bytes':count,'kind':kind,
                                       'caller_return_va':hex(caller),'freed':False})
        return pointer

    def _file_api(self,address,sp):
        if not self.unit_loading:
            return super()._file_api(address,sp)
        _,(name,pop) = list(FILE_IMPORTS.items())[(address-FILE_API)//16]
        if name == 'CreateFileA':
            args = [self.read(sp+4+i*4) for i in range(7)]
            if cstring(self,args[0]) != EFFECT_PATH or args[1:] != [0x80000000,1,0,3,1,0] or self.handles:
                raise RuntimeError('effect read-only file arguments')
            raw,identity = effect_resource()
            handle = 0xA00
            self.handles[handle] = {'raw':raw,'identity':identity}
            self.file_events.append({'name':name,'args':args,'result':handle})
            self._stub_return(handle,pop)
            return
        if name == 'ReadFile':
            handle,target,count,written,overlapped = [self.read(sp+4+i*4) for i in range(5)]
            if handle not in self.handles or overlapped != 0:
                raise RuntimeError('effect read handle')
            raw = self.handles[handle]['raw']
            if count != len(raw) or self.asset_allocations[-1]['pointer'] != target:
                raise RuntimeError('effect read length/allocation')
            self.primitive_write(target,raw)
            self.primitive_write(written,struct.pack('<I',len(raw)))
            self.asset_requests[-1].update({'buffer_pointer':target,'loaded_bytes':len(raw),
                                            'loaded_sha256':hashlib.sha256(raw).hexdigest()})
            self.file_events.append({'name':name,'args':[handle,target,count,written,overlapped],'result':1})
            self._stub_return(1,pop)
            return
        return super()._file_api(address,sp)

    def _hook(self,uc,address,size,context):
        if not getattr(self,'unit_loading',False):
            return super()._hook(uc,address,size,context)
        sp = uc.reg_read(UC_X86_REG_ESP)
        receiver = uc.reg_read(UC_X86_REG_ECX)
        if address == 0x466000:
            self.reset_snapshot = {'regions':[{'offset':hex(o),'bytes':n,'sha256':hashlib.sha256(bytes(uc.mem_read(UNITCTRL+o,n))).hexdigest()} for o,n in RESET_RANGES],
                                   'relation_hex':bytes(uc.mem_read(UNITCTRL+0x115AAC,256)).hex(),
                                   'text_request_count':len(self.text_requests)}
        if FILE_API <= address < FILE_API+len(FILE_IMPORTS)*16 and (address-FILE_API)%16 == 0:
            return self._file_api(address,sp)
        if address == 0x405160:
            index = len(self.text_requests)
            local = index
            for table,count,offset in TEXT_GROUPS:
                if local < count:
                    break
                local -= count
            else:
                raise RuntimeError('extra unit text request')
            args = [self.read(sp+4+i*4) for i in range(4)]
            pointer = self.read(table+local*4)
            if receiver != UNITCTRL+offset+local*128 or args != [self.read(self.read(0x7A49FC)+0xB210),self.read(UNITCTRL+0xDB80C),pointer,1]:
                raise RuntimeError('unit text request table/destination/arguments')
            if bytes(uc.mem_read(receiver+0x64,4)) != bytes([255])*4:
                raise RuntimeError('original unit text color initialization missing')
            self.text_requests.append({'table_va':hex(table),'index':local,'destination':receiver,
                                       'args':args,'text_hex':text_bytes(self,pointer).hex(),
                                       'source_color_hex':'ffffffff','platform_rendered':False})
            self._stub_return(0,16)
            return
        if address == 0x407780:
            if not UNITCTRL+0xDE930 <= receiver <= UNITCTRL+0x108930-128 or (receiver-UNITCTRL-0xDE930)%128:
                raise RuntimeError('unit graphics cleanup receiver')
            self.asset_boundaries.append({'kind':'prior_graphics_cleanup_boundary','receiver':receiver})
            self._stub_return(0,0)
            return
        if address == 0x56CEC0:
            target,byte,count = [self.read(sp+i) for i in (4,8,12)]
            offset = target-UNITCTRL
            slot_reset = count == 8 and 0x2B6F0 <= offset < 0x2C6F0 and (offset-0x2B6F0)%8 == 0
            if byte != 0 or ((offset,count) not in RESET_RANGES and not slot_reset):
                raise RuntimeError(f'unit exact reset primitive bounds {target-UNITCTRL:#x}/{byte}/{count} caller {self.read(sp):#x}')
            self.primitive_write(target,bytes(count))
            self._stub_return(target,0)
            return
        if address == 0x428A40:
            count,caller = self.read(sp+4),self.read(sp)
            if caller == 0x466069 and count == 0x54:
                kind = 'effect_controller'
            elif caller == 0x42AD54 and self.handles and count == len(next(iter(self.handles.values()))['raw']):
                kind = 'effect_file_buffer'
            elif caller == 0x409C53 and count == struct.unpack_from('<I',effect_resource()[0],0x20)[0]:
                kind = 'effect_metadata'
            else:
                raise RuntimeError(f'unit assets allocation caller/count {caller:#x}/{count}')
            pointer = self.asset_allocate(count,kind,caller)
            if kind == 'effect_controller':
                self.effect_controller = pointer
            self._stub_return(pointer,0)
            return
        if address == 0x4500B0:
            if self.asset_requests or receiver != TASK+0x80000 or cstring(self,self.read(sp+4)) != EFFECT_PATH:
                raise RuntimeError('natural effect resource request')
            _,identity = effect_resource()
            self.asset_requests.append({'source':identity,'caller_return_va':hex(self.read(sp))})
            self.visited.add(address)
            return
        if address == 0x56D810:
            target,fmt,left,right = [self.read(sp+i) for i in (4,8,12,16)]
            format_string = cstring(self,fmt)
            if format_string == '%s%s' and self.read(sp) == 0x4500EF and target == TASK+0x808E8:
                value = (cstring(self,left)+cstring(self,right)).encode('ascii')
            elif format_string == '%s' and self.read(sp) == 0x42ACB9 and target == 0x7A0EBC:
                value = cstring(self,left).encode('ascii')
            else:
                raise RuntimeError(f'effect source format/target/caller {format_string!r}/{target:#x}/{self.read(sp):#x}')
            if value.decode() != EFFECT_PATH:
                raise RuntimeError('effect source formatted identity')
            self.primitive_write(target,value+b'\0')
            self._stub_return(len(value),0)
            return
        if address == 0x56D4D0:
            target,source,count = [self.read(sp+i) for i in (4,8,12)]
            owned = {a['kind']:a for a in self.asset_allocations}
            if target != owned['effect_metadata']['pointer'] or source != owned['effect_file_buffer']['pointer'] or count != owned['effect_metadata']['bytes']:
                raise RuntimeError('effect metadata copy ownership')
            self.primitive_write(target,bytes(uc.mem_read(source,count)))
            self._stub_return(target,0)
            return
        if address == 0x41EBF0:
            self.texture_binding = {'receiver':receiver,'args':[self.read(sp+4+i*4) for i in range(5)]}
            self.stop_reason = 'before_effect_texture_binding'
            uc.emu_stop()
            return
        if address == 0x42B2D0:
            if cstring(self,self.read(sp+4)) not in ('UNIT_DATA : SIZE = %d\n','UNIT_WORK : SIZE = %d\n'):
                raise RuntimeError('unexpected unit debug log')
            self._stub_return(0,0)
            return
        return ExitEmulator._hook(self,uc,address,size,context)

    def assets_snapshot(self):
        at = self.effect_controller
        pointer = self.read(at)
        count = next(a['bytes'] for a in self.asset_allocations if a['kind']=='effect_metadata')
        return {'controller':at,'renderer':self.read(at+0x44),'animation_id':self.read(at+0x48,'h'),
                'animation_table':self.read(at+0x4C),'position_table':self.read(at+0x50),
                'kind_field':self.read(at+0x28),'metadata_pointer':pointer,'metadata_bytes':count,
                'metadata_sha256':hashlib.sha256(bytes(self.uc.mem_read(pointer,count))).hexdigest(),
                'section_pointers':[self.read(at+4+i*4) for i in range(5)],
                'texture_binding':deepcopy(self.texture_binding),
                'work_regions':[{'offset':hex(o),'bytes':n,'sha256':hashlib.sha256(bytes(self.uc.mem_read(UNITCTRL+o,n))).hexdigest()} for o,n in RESET_RANGES],
                'relation_hex':bytes(self.uc.mem_read(UNITCTRL+0x115AAC,256)).hex()}

    def resources(self,name,commands=()):
        self.unit_loading = False
        self.reset_assets()
        result = super().resources(name,commands)
        result.update({'unit_assets_prepared':False,'unit_assets':None,'text_requests':[],'asset_requests':[]})
        if result['ready']:
            protected = [(CHAR_BASE,0x7F4488-CHAR_BASE),(0x7CF34C,45*0x124),(0x7A528E,4),(UNITS,len(self.combat_records)*176)]
            before = [bytes(self.uc.mem_read(a,n)) for a,n in protected]
            self.unit_loading = True
            self.clear_trace('tactical_startup')
            self.stop_reason = None
            self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30_000_000,count=12_000_000)
            if self.stop_reason != 'before_effect_texture_binding' or self.handles:
                raise RuntimeError('unit assets missed effect texture boundary')
            if before != [bytes(self.uc.mem_read(a,n)) for a,n in protected]:
                raise RuntimeError('unit assets changed current/persistent records')
            result.update({'unit_assets_prepared':True,'unit_assets':self.assets_snapshot(),
                           'text_requests':deepcopy(self.text_requests),'asset_requests':deepcopy(self.asset_requests),
                           'asset_allocations':deepcopy(self.asset_allocations),'asset_boundaries':deepcopy(self.asset_boundaries),
                           'unit_reset_snapshot':deepcopy(self.reset_snapshot),
                           'file_events':deepcopy(self.file_events),'stop_reason':self.stop_reason})
            result['phases'].append({'phase':'natural_unit_reset_effect_metadata','coverage':self.coverage()})
            self.unit_loading = False
        return result


def report():
    e = SchoolUnitAssetsEmulator()
    up = e.run_planning('unit_assets_upstream')
    if not up['school_data_prepared']:
        raise RuntimeError('actual fifth-school prefix missing')
    ranges = [(BASE,(SOURCE.stat().st_size+0xFFF)&~0xFFF),(TASK,0x120000),(GROUP_TASK,0x60000),
              (STACK,0x10000),(TACT,0x11A000),(SCRIPT_WORK,0x3000),(POOL,POOL_SIZE),
              (UHEAP,UHEAP_SIZE),(SCENE_POOL,SCENE_POOL_SIZE),(ASSET_POOL,ASSET_POOL_SIZE)]
    checkpoint = [(a,bytes(e.uc.mem_read(a,n))) for a,n in ranges]
    cpu = e.uc.context_save()
    cases = []
    for name,commands in [('initial',()),('student9_waiting',[('student',9,-1)]),
        ('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1),('student',9,-1)]),
        ('teacher_only',[('student',3,-1),('student',4,-1),('student',9,-1)]),('teacher_waiting',[('teacher',101,-1)])]:
        for a,data in checkpoint:
            e.uc.mem_write(a,data)
        e.uc.context_restore(cpu)
        e.stop_reason = None
        cases.append(e.resources(name,commands))
        print('Native unit assets '+name+': '+str(cases[-1]['unit_assets_prepared']),flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
            'boundary':'Unit reset/effect metadata prepared; text/GPU boundaries declared; effect texture binding/current units/enemies/VM/placement unexecuted.',**AUTHORITY}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',required=True)
    args = p.parse_args()
    path = ROOT/args.out
    if path.exists():
        p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
