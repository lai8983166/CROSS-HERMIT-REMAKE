"""Original first unit animation loading/binding, before unit animation work.

Read-only files, finite heap/CRT and GPU boundaries are explicit; no live GPU.
"""
import argparse
from copy import deepcopy
import hashlib
import struct
from unicorn.x86_const import UC_X86_REG_ECX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_first_unit_work_emulation import (
    SchoolFirstUnitWorkEmulator,UNIT_POOL,UNIT_POOL_SIZE,WORK_OFFSET,WORK_BYTES,
    RECORD_OFFSET,CACHE_OFFSET,CACHE_COUNT,COUNTER_OFFSET,MAP_POOL,MAP_POOL_SIZE,
    ASSET_POOL,ASSET_POOL_SIZE,SCENE_POOL,SCENE_POOL_SIZE,UHEAP,UHEAP_SIZE,
    UNITCTRL,POOL,POOL_SIZE,TACT,SCRIPT_WORK,GROUP_TASK,CHAR_BASE,UNITS,
    ROOT,SOURCE,SOURCE_SHA256,BASE,TASK,STACK,RETURN,report_text,ExitEmulator,
    AUTHORITY,cstring,WORK_GROUPS)
from tools.school_tactical_resources_emulation import FILE_API,FILE_IMPORTS,SchoolTacticalResourcesEmulator

ANIM_POOL,ANIM_POOL_SIZE = 0x15000000,0x200000
UNIT_PATH = 'data\\DxAnim\\d1a.bin'
UNIT_SHA = '6262a9fa80b112389ee5a9d2d61aee6526f87130e7ce2e828619e7c095979a5b'
NATIVE = ((0x464F1F,0x464F7B),(0x466D4E,0x466D9A))


def unit_resource():
    path = ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/DXANIM/D1A.BIN'
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=UNIT_SHA:
        raise ValueError('first unit animation source identity differs')
    return raw,{'relative_path':UNIT_PATH,'local_file':path.relative_to(ROOT).as_posix(),
                'bytes':len(raw),'sha256':UNIT_SHA}


class SchoolFirstUnitAnimationEmulator(SchoolFirstUnitWorkEmulator):
    def __init__(self):
        self.animation_loading = False
        super().__init__()
        self._function_ranges += NATIVE
        observed = {0x4500B0,0x41F340,0x41EC40,0x4142B0,0x467147,
                    0x56DDA0,0x424F80,0x41EFD0}
        self.animation_code = frozenset(a for start,end in self._function_ranges for a in range(start,end))-observed
        self.uc.mem_map(ANIM_POOL,ANIM_POOL_SIZE)
        self.reset_animation()

    def reset_animation(self):
        self.animation_cursor = ANIM_POOL
        self.animation_allocations = []
        self.animation_request = None
        self.animation_entries = []
        self.animation_boundaries = []
        self.animation_vector = None
        self.animation_binding = None
        self.animation_graphics_input = None
        self.animation_container_calls = []
        self.animation_call_results = []
        self.animation_file_release = None

    def _write_hook(self,uc,access,address,size,value,context):
        if not getattr(self,'animation_loading',False):
            return super()._write_hook(uc,access,address,size,value,context)
        allowed = [(STACK,STACK+0x10000),(0,4),(UNIT_POOL,UNIT_POOL+84),
            (TASK+0x808E8,TASK+0x809EC),(0x7A0EBC,0x7A0FC0),
            (self.texture_table+110*8,self.texture_table+111*8)]
        allowed += [(a['pointer'],a['pointer']+a['bytes']) for a in self.animation_allocations if not a['freed']]
        if not any(a<=address and address+size<=b for a,b in allowed):
            raise RuntimeError(f'first animation finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        if not STACK<=address<STACK+0x10000:
            self.writes.append((address,size,value & ((1<<(size*8))-1)))
            self.startup_writes.append((address,size))

    def animation_allocate(self,count,kind,caller):
        at,end = self.animation_cursor,self.animation_cursor+((count+15)&~15)
        if count<=0 or end>ANIM_POOL+ANIM_POOL_SIZE:
            raise RuntimeError('first animation finite allocation bounds')
        self.animation_cursor = end
        self.animation_allocations.append({'pointer':at,'bytes':count,'kind':kind,
                                          'caller_return_va':hex(caller),'freed':False})
        return at

    def _file_api(self,address,sp):
        if not getattr(self,'animation_loading',False):
            return super()._file_api(address,sp)
        _,(name,pop) = list(FILE_IMPORTS.items())[(address-FILE_API)//16]
        if name=='CreateFileA':
            args = [self.read(sp+4+i*4) for i in range(7)]
            if cstring(self,args[0])!=UNIT_PATH or args[1:]!=[0x80000000,1,0,3,1,0] or self.handles:
                raise RuntimeError('first animation exact read-only file arguments')
            raw,identity = unit_resource()
            self.handles[0xC00] = {'raw':raw,'identity':identity}
            self.file_events.append({'name':name,'args':args,'result':0xC00})
            self._stub_return(0xC00,pop)
            return
        if name=='ReadFile':
            handle,target,count,written,overlapped = [self.read(sp+4+i*4) for i in range(5)]
            if handle not in self.handles or overlapped!=0:
                raise RuntimeError('first animation read handle')
            raw = self.handles[handle]['raw']
            owned = [a for a in self.animation_allocations if a['kind']=='unit_file_buffer' and not a['freed']]
            if len(owned)!=1 or (target,count)!=(owned[0]['pointer'],len(raw)):
                raise RuntimeError('first animation read length/allocation')
            self.primitive_write(target,raw)
            self.primitive_write(written,struct.pack('<I',count))
            self.animation_request.update({'buffer_pointer':target,'loaded_bytes':count,
                'loaded_sha256':hashlib.sha256(bytes(self.uc.mem_read(target,count))).hexdigest(),'loaded':True})
            self.file_events.append({'name':name,'args':[handle,target,count,written,overlapped],'result':1})
            self._stub_return(1,pop)
            return
        return SchoolTacticalResourcesEmulator._file_api(self,address,sp)

    def _hook(self,uc,address,size,context):
        if not getattr(self,'animation_loading',False):
            return super()._hook(uc,address,size,context)
        if address in self.animation_code:
            self.visited.add(address)
            return
        sp,receiver = uc.reg_read(UC_X86_REG_ESP),uc.reg_read(UC_X86_REG_ECX)
        if address in (0x424F80,0x41EFD0):
            raise RuntimeError(f'unexpected first animation assertion/dynamic slot at {address:#x}')
        if address==0x467147:
            if self.handles or self.read(UNIT_POOL+0x40)!=1 or len(self.animation_entries)!=193:
                raise RuntimeError('first animation missed completed resource/cache binding')
            self.stop_reason = 'before_first_unit_animation_work_binding'
            uc.emu_stop()
            return
        if FILE_API<=address<FILE_API+len(FILE_IMPORTS)*16 and (address-FILE_API)%16==0:
            return self._file_api(address,sp)
        if address==0x4500B0:
            args = [self.read(sp+4+i*4) for i in range(4)]
            if self.animation_request or self.read(sp)!=0x464F1F or receiver!=TASK+0x80000 \
                or cstring(self,args[0])!=UNIT_PATH or args[1:]!=[3,1,0]:
                raise RuntimeError('first animation source file request')
            _,identity = unit_resource()
            self.animation_request = {'receiver':receiver,'args':args,'source':identity,
                                      'caller_return_va':hex(self.read(sp)),'loaded':False}
            self.visited.add(address)
            return
        if address==0x4142B0:
            if receiver!=TASK or self.read(sp)!=0x464F2F:
                raise RuntimeError('first animation renderer device query')
            self.visited.add(address)
            return
        if address==0x428A40:
            count,caller = self.read(sp+4),self.read(sp)
            if caller==0x42AD54 and self.handles and count==len(next(iter(self.handles.values()))['raw']):
                kind = 'unit_file_buffer'
            elif caller==0x409C53 and count==11476:
                kind = 'unit_metadata'
            elif caller==0x41F142 and count==193*84+4:
                kind = 'unit_texture_array'
            else:
                raise RuntimeError(f'first animation allocation caller/count {caller:#x}/{count}')
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
                raise RuntimeError('first animation exact source path formatting')
            if value!=UNIT_PATH:
                raise RuntimeError('first animation formatted source path')
            self.primitive_write(target,value.encode('ascii')+b'\0')
            self._stub_return(len(value),0)
            return
        if address==0x56D4D0:
            target,source,count = [self.read(sp+i) for i in (4,8,12)]
            owned = {a['kind']:a for a in self.animation_allocations}
            if (target,source,count,self.read(sp))!=(owned['unit_metadata']['pointer'],owned['unit_file_buffer']['pointer'],11476,0x409C84):
                raise RuntimeError('first animation metadata copy ownership')
            self.primitive_write(target,bytes(uc.mem_read(source,count)))
            self._stub_return(target,0)
            return
        if address==0x41EC40:
            args = [self.read(sp+4+i*4) for i in range(7)]
            file = next(a['pointer'] for a in self.animation_allocations if a['kind']=='unit_file_buffer')
            metadata = next(a['pointer'] for a in self.animation_allocations if a['kind']=='unit_metadata')
            if receiver!=UNIT_POOL+0x18 or args!=[0,self.texture_table,metadata+9932,file+11476,0,file+877872,file+916784]:
                raise RuntimeError(f'first animation palette/mask binding {args}')
            self.animation_binding = {'receiver':receiver,'args':args,'caller_return_va':hex(self.read(sp))}
            self.visited.add(address)
            return
        if address==0x56DDA0:
            args = tuple(self.read(sp+i) for i in (4,8,12,16,20))
            a = self.animation_allocations[-1]
            if a['kind']!='unit_texture_array' or args!=(a['pointer']+4,84,193,0x41F830,0x41F890):
                raise RuntimeError('first animation bounded texture vector')
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
                raise RuntimeError('first animation exact texture clear primitive')
            self.primitive_write(target,bytes(count))
            self._stub_return(target,0)
            return
        if address==0x41F340:
            device,buffer,index,records,left,right = [self.read(sp+i) for i in (4,8,12,16,20,24)]
            owned = {a['kind']:a for a in self.animation_allocations}
            base = owned['unit_file_buffer']['pointer']
            selected = base+877872 if self.read(base+916784+index,'B')==0 else 0
            if device!=0 or buffer!=base+11476 or index!=len(self.animation_entries) or index>=193 \
                or records!=owned['unit_texture_array']['pointer']+4 or (left,right)!=(0,selected):
                raise RuntimeError('first animation texture source/order/palette mask')
            offset = self.read(buffer+8+index*4)
            end = self.read(buffer+8+(index+1)*4) if index<192 else self.read(buffer)
            if not 780<=offset<end<=864180:
                raise RuntimeError('first animation texture entry bounds')
            self.active_texture = {'index':index,'offset':offset,'file_offset':11476+offset,
                'bytes':end-offset,'header_hex':bytes(uc.mem_read(buffer+offset,16)).hex(),
                'record_pointer':records+index*84,'palette_pointer':selected,
                'mask_value':self.read(base+916784+index,'B')}
            self.animation_entries.append(self.active_texture)
            self.visited.add(address)
            return
        if address==0x403BD0:
            if not self.animation_entries or receiver!=self.active_texture['record_pointer'] or [self.read(sp+4),self.read(sp+8)]!=[0,0]:
                raise RuntimeError('first animation exact GPU creation boundary')
            self.animation_boundaries.append({'kind':'texture_creation','index':self.active_texture['index'],
                'width':self.read(receiver+0x38,'H'),'height':self.read(receiver+0x3A,'H'),'format':self.read(receiver+0x34)})
            self._stub_return(0,8)
            return
        if address==0x404150:
            args = [self.read(sp+4+i*4) for i in range(4)]
            if not self.animation_entries or receiver!=self.active_texture['record_pointer'] \
                or args!=[self.animation_request['buffer_pointer']+self.active_texture['file_offset'],1,0,self.active_texture['palette_pointer']]:
                raise RuntimeError(f'first animation exact GPU pixel/palette upload boundary: {receiver:#x} {args} entry {self.active_texture}')
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
            if not owned or owned['kind']!='unit_file_buffer' or self.read(sp)!=0x409E5D or len(self.animation_entries)!=193:
                raise RuntimeError('first animation source release ownership/order')
            self.animation_file_release = {'pointer':pointer,'bytes':owned['bytes'],'caller_return_va':hex(self.read(sp)),
                'sha256_at_release':hashlib.sha256(bytes(uc.mem_read(pointer,owned['bytes']))).hexdigest()}
            owned['freed'] = True
            self.animation_boundaries.append({'kind':'source_file_release',**self.animation_file_release})
            self._stub_return(0,0)
            return
        return ExitEmulator._hook(self,uc,address,size,context)

    def run_animation_thread(self):
        batches,vectors = 0,0
        self.stop_reason = None
        while True:
            self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30_000_000,count=12_000_000)
            if self.stop_reason!='first_unit_texture_vector':
                if self.stop_reason is None and self.uc.reg_read(UC_X86_REG_EIP)!=RETURN:
                    batches += 1
                    if batches>4:
                        raise RuntimeError('first animation exceeded finite CPU batches')
                    continue
                break
            vectors += 1
            if vectors!=1:
                raise RuntimeError('first animation repeated texture vector')
            target,stride,count,ctor = self.vector_pending
            cpu,stack = self.uc.context_save(),bytes(self.uc.mem_read(STACK,0x10000))
            for i in range(count):
                self.call(ctor,receiver=target+i*stride)
                self.animation_vector['native_constructors_completed'] += 1
            self.uc.mem_write(STACK,stack)
            self.uc.context_restore(cpu)
            self._stub_return(0,20)
            self.stop_reason = None
        if self.stop_reason!='before_first_unit_animation_work_binding' or self.handles:
            raise RuntimeError(f'first animation missed binding boundary at {self.uc.reg_read(UC_X86_REG_EIP):#x}')

    def animation_snapshot(self):
        for e in self.animation_entries:
            p = e['record_pointer']
            e.update({'width':self.read(p+0x38,'H'),'height':self.read(p+0x3A,'H'),'format':self.read(p+0x34),
                      'raw_record_hex':bytes(self.uc.mem_read(p,84)).hex()})
        metadata = next(a for a in self.animation_allocations if a['kind']=='unit_metadata')
        return {'controller':UNIT_POOL,'controller_hex':bytes(self.uc.mem_read(UNIT_POOL,84)).hex(),
            'metadata_pointer':metadata['pointer'],'metadata_bytes':metadata['bytes'],
            'metadata_hex':bytes(self.uc.mem_read(metadata['pointer'],metadata['bytes'])).hex(),
            'metadata_sha256':hashlib.sha256(bytes(self.uc.mem_read(metadata['pointer'],metadata['bytes']))).hexdigest(),
            'section_pointers':[self.read(UNIT_POOL+4+i*4) for i in range(5)],
            'texture_slot':self.read(UNIT_POOL+0x28),'texture_table':self.read(UNIT_POOL+0x24),
            'texture_records':self.read(self.texture_table+110*8),'texture_count':self.read(self.texture_table+110*8+4),
            'mode_field':self.read(UNIT_POOL+0x40),'binding':deepcopy(self.animation_binding),
            'vector':deepcopy(self.animation_vector),'request':deepcopy(self.animation_request),
            'allocations':deepcopy(self.animation_allocations),'file_release':deepcopy(self.animation_file_release),
            'graphics_input':deepcopy(self.animation_graphics_input),'unit_constructor_completed':False,
            'unit_animation_work_bound':False}

    def resources(self,name,commands=()):
        self.animation_loading = False
        self.reset_animation()
        result = super().resources(name,commands)
        result.update({'first_unit_animation_loaded':False,'first_unit_animation':None,'unit_texture_entries':[]})
        if not result['ready']:
            return result
        work = UNITCTRL+WORK_OFFSET+self.active_index*WORK_BYTES
        record = UNITCTRL+RECORD_OFFSET+self.active_index*176
        protected = [(CHAR_BASE,0x7F4488-CHAR_BASE),(0x7CF34C,45*0x124),(0x7A528E,4),
            (0x7F4488,UNITS-0x7F4488),(UNITS,len(self.combat_records)*176),(MAP_POOL,69368),
            (work,WORK_BYTES),(record,176),(UNITCTRL+CACHE_OFFSET,CACHE_COUNT*8),(UNITCTRL+COUNTER_OFFSET,4)]
        protected += [(a['pointer'],a['bytes']) for a in self.asset_allocations if not a['freed']]
        protected += [(self.texture_table+100*8,8)]+[(UNITCTRL+o,n*s) for o,n,s,p in WORK_GROUPS]
        before = [bytes(self.uc.mem_read(a,n)) for a,n in protected]
        prior = bytes(self.uc.mem_read(self.texture_table+110*8,8))
        if prior!=bytes(8) or self.read(UNIT_POOL+0x28)!=110:
            raise RuntimeError('source unit texture slot110 differs or not empty')
        self.animation_graphics_input = {'slot':110,'previous_slot_hex':prior.hex(),
            'controller_before_hex':bytes(self.uc.mem_read(UNIT_POOL,84)).hex(),
            'scope':'Prior isolated renderer input; source counter110 selects slot, dynamic search and GPU are not executed.'}
        self.animation_loading = True
        self.clear_trace('tactical_startup')
        self.run_animation_thread()
        if before!=[bytes(self.uc.mem_read(a,n)) for a,n in protected]:
            raise RuntimeError('first animation changed previous work/current/persistent/map/effect bytes')
        result.update({'first_unit_animation_loaded':True,'first_unit_animation':self.animation_snapshot(),
            'unit_texture_entries':deepcopy(self.animation_entries),'unit_animation_boundaries':deepcopy(self.animation_boundaries),
            'file_events':deepcopy(self.file_events),'first_unit_animation_retained_ranges_unchanged':True,'stop_reason':self.stop_reason})
        result['phases'].append({'phase':'natural_first_unit_animation_loading_binding','coverage':self.coverage()})
        self.animation_loading = False
        return result


def report():
    e = SchoolFirstUnitAnimationEmulator()
    if not e.run_planning('first_unit_animation_upstream')['school_data_prepared']:
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
        print('Native first unit animation '+name+': '+str(cases[-1]['first_unit_animation_loaded']),flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
        'boundary':'First source-selected unit archive/metadata/palette/mask/texture binding completed; GPU declared. Unit work binding/constructor tail, other current/enemy units, VM/placement unexecuted.',**AUTHORITY}


if __name__=='__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',required=True)
    args = p.parse_args()
    path = ROOT/args.out
    if path.exists():
        p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
