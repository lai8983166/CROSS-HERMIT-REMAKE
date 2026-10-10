"""Load first scene NPC animation and finish its original constructor."""
import argparse
from copy import deepcopy
import hashlib
import struct
from unicorn.x86_const import UC_X86_REG_ECX,UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EAX,UC_X86_REG_EBP
from tools.school_scene_unit_work_emulation import (
    SchoolSceneUnitWorkEmulator,ROOT,SOURCE,SOURCE_SHA256,BASE,TACT,UNITCTRL,
    RECORD_OFFSET,WORK_OFFSET,WORK_BYTES,STACK,RETURN,ExitEmulator,AUTHORITY,report_text,
    SCENE_CONTROLLER,CACHE_OFFSET,CACHE_COUNT,COUNTER_OFFSET,TASK,cstring)
from tools.school_first_unit_constructor_emulation import SHARED_OFFSET,SHARED_BYTES
from tools.school_tactical_resources_emulation import FILE_API,FILE_IMPORTS,SchoolTacticalResourcesEmulator
from tools.dxanim_lib import parse_dxanim,parse_container

SCENE_ANIM,SCENE_ANIM_BYTES=0x19000000,0x400000
SCENE_PATH='data\\DxAnim\\a1a.bin'
SCENE_SHA='4cc024015e95e0d2c08f083c53770c4c925ff7fab9b0b188b6da622bf7803b85'


def scene_resource(job,variant,rules=None):
    if type(job) is not int or job!=4 or type(variant) is not int or not 1<=variant<=40:
        raise ValueError('unsupported first scene NPC job/palette')
    file=ROOT/'CROSS HERMIT/CROSS HERMIT/data/DxAnim/a1a.bin';raw=file.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SCENE_SHA:raise ValueError('scene animation source identity')
    offsets=parse_dxanim(raw)
    if len(offsets)!=9:raise ValueError('scene animation section count')
    image_bytes,count,_=parse_container(raw,offsets[6])
    _,palettes,entries=parse_container(raw,offsets[7])
    if len(offsets)!=9 or count!=244 or palettes!=40 or offsets[8]+244!=len(raw):raise ValueError('scene animation shape')
    return raw,{'relative_path':SCENE_PATH,'local_file':file.relative_to(ROOT).as_posix(),
        'bytes':len(raw),'sha256':SCENE_SHA},{'offsets':offsets,'metadata_bytes':offsets[6],
        'image_bytes':image_bytes,'count':count,'palette_offset':offsets[7]+entries[variant-1],'variant':variant}


class SchoolSceneUnitConstructorEmulator(SchoolSceneUnitWorkEmulator):
    def __init__(self):
        self.scene_complete_loading=False
        super().__init__();self.uc.mem_map(SCENE_ANIM,SCENE_ANIM_BYTES)
        self.scene_phase=None

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.scene_complete_loading:return super()._write_hook(uc,access,address,size,value,context)
        allowed=[(STACK,STACK+0x10000),(0,4)]
        if self.scene_phase=='animation':
            allowed += [(self.controller,self.controller+84),(TASK+0x808E8,TASK+0x809EC),(0x7A0EBC,0x7A0FC0),
                (self.texture_table+self.scene_texture_slot*8,self.texture_table+(self.scene_texture_slot+1)*8)]
            allowed += [(a['pointer'],a['pointer']+a['bytes']) for a in self.animation_allocations if not a['freed']]
        elif self.scene_phase=='tail':
            w=UNITCTRL+WORK_OFFSET+self.active_index*WORK_BYTES
            allowed += [(w,w+WORK_BYTES),(UNITCTRL+SHARED_OFFSET,UNITCTRL+SHARED_OFFSET+SHARED_BYTES),
                (self.constructor_cell,self.constructor_cell+1)]
        if not any(a<=address and address+size<=b for a,b in allowed):
            raise RuntimeError(f'scene constructor finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x} phase {self.scene_phase}')
        if not STACK<=address<STACK+0x10000:self.writes.append((address,size,value&((1<<(size*8))-1)))

    def capture_scene_memory(self,excluded):
        spans=[];excluded=[(STACK,STACK+0x10000),(0,4),*excluded]
        for start,end,_ in self.uc.mem_regions():
            pieces=[(start,end+1)]
            for left,right in excluded:
                pieces=[p for a,b in pieces for p in ((a,min(b,left)),(max(a,right),b)) if p[0]<p[1]]
            spans.extend((a,bytes(self.uc.mem_read(a,b-a))) for a,b in pieces)
        return spans

    def verify_scene_memory(self,spans):
        if any(bytes(self.uc.mem_read(a,len(raw)))!=raw for a,raw in spans):raise RuntimeError('scene constructor changed retained memory')
        return {'retained_ranges_unchanged':True,'retained_bytes':sum(len(raw) for _,raw in spans),
            'retained_ranges':[{'pointer':a,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()} for a,raw in spans]}

    def animation_allocate(self,count,kind,caller):
        if not self.scene_complete_loading:return super().animation_allocate(count,kind,caller)
        at=self.scene_animation_cursor;end=at+((count+15)&~15)
        if self.scene_phase!='animation' or count<=0 or end>SCENE_ANIM+SCENE_ANIM_BYTES:raise RuntimeError('scene animation finite allocation')
        self.scene_animation_cursor=end
        self.animation_allocations.append({'pointer':at,'bytes':count,'kind':kind,'caller_return_va':hex(caller),'freed':False})
        return at

    def _file_api(self,address,sp):
        if not self.scene_complete_loading:return super()._file_api(address,sp)
        if self.scene_phase!='animation':raise RuntimeError('scene file API outside animation phase')
        _,(name,pop)=list(FILE_IMPORTS.items())[(address-FILE_API)//16]
        if name=='CreateFileA':
            args=[self.read(sp+4+i*4) for i in range(7)]
            if cstring(self,args[0])!=SCENE_PATH or args[1:]!=[0x80000000,1,0,3,1,0] or self.handles:raise RuntimeError('scene exact read-only file arguments')
            raw,identity,_=scene_resource(4,self.current['variant']);handle=0xE00
            self.handles[handle]={'raw':raw,'identity':identity};self.file_events.append({'name':name,'args':args,'result':handle})
            self._stub_return(handle,pop);return
        if name=='ReadFile':
            handle,target,count,written,overlapped=[self.read(sp+4+i*4) for i in range(5)]
            owned=[a for a in self.animation_allocations if a['kind']=='unit_file_buffer' and not a['freed']]
            if handle not in self.handles or overlapped or len(owned)!=1 or (target,count)!=(owned[0]['pointer'],self.unit_identity['bytes']):
                raise RuntimeError('scene exact file read ownership')
            self.primitive_write(target,self.handles[handle]['raw']);self.primitive_write(written,struct.pack('<I',count))
            self.animation_request.update({'buffer_pointer':target,'loaded_bytes':count,'loaded_sha256':hashlib.sha256(bytes(self.uc.mem_read(target,count))).hexdigest(),'loaded':True})
            self.file_events.append({'name':name,'args':[handle,target,count,written,overlapped],'result':1});self._stub_return(1,pop);return
        return SchoolTacticalResourcesEmulator._file_api(self,address,sp)

    def _hook(self,uc,address,size,context):
        if not self.scene_complete_loading:return super()._hook(uc,address,size,context)
        if self.scene_phase=='animation':
            if address==0x467147:
                if self.handles or self.read(self.controller+0x40)!=1 or len(self.animation_entries)!=244 or self.animation_vector['native_constructors_completed']!=244:
                    raise RuntimeError('scene incomplete archive binding')
                self.stop_reason='after_first_scene_unit_animation_binding';uc.emu_stop();return
            return self._scene_animation_hook(uc,address,size,context)
        if self.scene_phase=='tail':return self._scene_tail_hook(uc,address,size,context)
        raise RuntimeError('scene constructor invalid phase')

    def run_scene_animation(self,variant=5):
        raw,self.unit_identity,self.unit_inputs=scene_resource(4,variant)
        self.reset_animation();self.scene_animation_cursor=SCENE_ANIM;self.controller=SCENE_CONTROLLER
        self.active_index=249;self.unit_path=SCENE_PATH
        self.scene_texture_slot=self.read(self.controller+0x28)
        if self.scene_texture_slot not in (110,112,113) or any(self.uc.mem_read(self.texture_table+self.scene_texture_slot*8,8)):
            raise RuntimeError('scene exact empty texture slot')
        before_controller=bytes(self.uc.mem_read(self.controller,84)).hex();cursor=SCENE_ANIM;excluded=[]
        for count in (len(raw),self.unit_inputs['metadata_bytes'],244*84+4):
            excluded.append((cursor,cursor+count));cursor+=(count+15)&~15
        excluded += [(self.controller,self.controller+84),(TASK+0x808E8,TASK+0x809EC),(0x7A0EBC,0x7A0FC0),
            (self.texture_table+self.scene_texture_slot*8,self.texture_table+(self.scene_texture_slot+1)*8)]
        retained=self.capture_scene_memory(excluded);before_events=len(self.file_events)
        prefix_current=self.current
        self.current={'job':4,'variant':variant}
        self.clear_trace('tactical_startup');self.stop_reason=None;self.scene_phase='animation';self.scene_complete_loading=True
        try:
            for batch in range(8):
                self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30_000_000,count=1_000_000)
                if self.stop_reason=='first_unit_texture_vector':
                    target,stride,count,ctor=self.vector_pending;cpu=self.uc.context_save();stack=bytes(self.uc.mem_read(STACK,0x10000))
                    for i in range(count):
                        self.call(ctor,receiver=target+i*stride);self.animation_vector['native_constructors_completed']+=1
                    self.uc.mem_write(STACK,stack);self.uc.context_restore(cpu);self._stub_return(0,20);self.stop_reason=None
                    continue
                if self.stop_reason=='after_first_scene_unit_animation_binding':break
            else:raise RuntimeError('scene animation exceeded finite batches')
            preservation=self.verify_scene_memory(retained)
            for e in self.animation_entries:e['raw_record_hex']=bytes(self.uc.mem_read(e['record_pointer'],84)).hex()
            return {'index':249,'controller':self.controller,'before_controller_hex':before_controller,
                'controller_hex':bytes(self.uc.mem_read(self.controller,84)).hex(),'metadata_pointer':self.read(self.controller),
                'metadata_hex':bytes(self.uc.mem_read(self.read(self.controller),self.unit_inputs['metadata_bytes'])).hex(),
                'texture_slot':self.scene_texture_slot,'texture_slot_hex':bytes(self.uc.mem_read(self.texture_table+self.scene_texture_slot*8,8)).hex(),
                'texture_table':self.texture_table,'variant':variant,'request':deepcopy(self.animation_request),
                'allocations':deepcopy(self.animation_allocations),'entries':deepcopy(self.animation_entries),
                'binding':deepcopy(self.animation_binding),'vector':deepcopy(self.animation_vector),
                'boundaries':deepcopy(self.animation_boundaries),'file_release':deepcopy(self.animation_file_release),
                'file_events':deepcopy(self.file_events[before_events:]),'coverage':self.coverage(),
                'constructor_completed':False,'scene_placement_executed':False,**preservation}
        finally:
            self.current=prefix_current
            self.scene_complete_loading=False

    def run_scene_constructor_tail(self):
        snap=self._prepare_scene_constructor()
        retained=self.capture_scene_memory([(snap['work_pointer'],snap['work_pointer']+WORK_BYTES),
            (UNITCTRL+SHARED_OFFSET,UNITCTRL+SHARED_OFFSET+SHARED_BYTES),(self.constructor_cell,self.constructor_cell+1)])
        self.scene_phase='tail';self.clear_trace('tactical_startup');self.stop_reason=None;self.scene_complete_loading=True
        try:
            self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30_000_000,count=500_000)
            if self.stop_reason!='after_first_scene_unit_constructor_return' or self.handles:raise RuntimeError('scene constructor missed natural return')
            preservation=self.verify_scene_memory(retained)
            after=bytes(self.uc.mem_read(self.constructor_cm,12288));prior=bytearray.fromhex(snap['before_cm_hex'])
            at=self.constructor_cell-self.constructor_cm;prior[at]=(prior[at]+1)&255
            if after!=bytes(prior):raise RuntimeError('scene constructor exact cell accounting')
            snap.update({'work_hex':bytes(self.uc.mem_read(snap['work_pointer'],WORK_BYTES)).hex(),
                'shared_hex':bytes(self.uc.mem_read(snap['shared_pointer'],SHARED_BYTES)).hex(),'cm_hex':after.hex(),
                'cm_sha256':hashlib.sha256(after).hexdigest(),'calls':deepcopy(self.constructor_calls),
                'clears':deepcopy(self.constructor_clears),'return_va':'0x453630','return_eax':self.uc.reg_read(UC_X86_REG_EAX),
                'constructor_completed':True,'unit_animation_work_bound':True,'scene_placement_executed':False,
                'scene_vm_executed':False,'coverage':self.coverage(),**preservation})
            return snap
        finally:self.scene_complete_loading=False

    def resources(self,name,commands=()):
        self.scene_complete_loading=False;result=super().resources(name,commands)
        result.update({'scene_unit_animation_loaded':False,'scene_unit_animation':None,'scene_unit_constructor_completed':False,'scene_unit_constructor':None})
        if not result['ready']:return result
        animation=self.run_scene_animation()
        tail=self.run_scene_constructor_tail()
        result.update({'scene_unit_animation_loaded':True,'scene_unit_animation':animation,
            'scene_unit_constructor_completed':True,'scene_unit_constructor':tail,'stop_reason':self.stop_reason,
            'file_events':deepcopy(self.file_events)})
        result['phases'].append({'phase':'native_first_scene_unit_constructor_return','coverage':self.coverage()})
        return result


    def _scene_animation_hook(self, uc, address, size, context):
        if address in self.animation_code:
            self.visited.add(address)
            return
        (sp, receiver) = (uc.reg_read(UC_X86_REG_ESP), uc.reg_read(UC_X86_REG_ECX))
        if address in (4345728, 4321232):
            raise RuntimeError(f'unexpected scene animation assertion/dynamic slot at {address:#x}')
        if FILE_API <= address < FILE_API + len(FILE_IMPORTS) * 16 and (address - FILE_API) % 16 == 0:
            return self._file_api(address, sp)
        if address == 4522160:
            args = [self.read(sp + 4 + i * 4) for i in range(4)]
            if self.animation_request or self.read(sp) != 4607775 or receiver != TASK + 524288 or (cstring(self, args[0]) != self.unit_path) or (args[1:] != [self.current['variant'], 1, 0]):
                raise RuntimeError('scene animation source file request')
            (_, identity, _) = scene_resource(self.current['job'], self.current['variant'], self.current_rules)
            self.animation_request = {'receiver': receiver, 'args': args, 'source': identity, 'caller_return_va': hex(self.read(sp)), 'loaded': False}
            self.visited.add(address)
            return
        if address == 4276912:
            if receiver != TASK or self.read(sp) != 4607791:
                raise RuntimeError('scene animation renderer device query')
            self.visited.add(address)
            return
        if address == 4360768:
            (count, caller) = (self.read(sp + 4), self.read(sp))
            if caller == 4369748 and self.handles and (count == len(next(iter(self.handles.values()))['raw'])):
                kind = 'unit_file_buffer'
            elif caller == 4234323 and count == self.unit_inputs['metadata_bytes']:
                kind = 'unit_metadata'
            elif caller == 4321602 and count == self.unit_inputs['count'] * 84 + 4:
                kind = 'unit_texture_array'
            else:
                raise RuntimeError(f'scene animation allocation caller/count {caller:#x}/{count}')
            self._stub_return(self.animation_allocate(count, kind, caller), 0)
            return
        if address == 5691408:
            (target, fmt, left) = [self.read(sp + i) for i in (4, 8, 12)]
            format_text = cstring(self, fmt)
            if format_text == '%s%s' and target == TASK + 526568 and (self.read(sp) == 4522223):
                value = cstring(self, left) + cstring(self, self.read(sp + 16))
            elif format_text == '%s' and target == 7999164 and (self.read(sp) == 4369593):
                value = cstring(self, left)
            else:
                raise RuntimeError('scene animation exact source path formatting')
            if value != self.unit_path:
                raise RuntimeError('scene animation formatted source path')
            self.primitive_write(target, value.encode('ascii') + b'\x00')
            self._stub_return(len(value), 0)
            return
        if address == 5690576:
            (target, source, count) = [self.read(sp + i) for i in (4, 8, 12)]
            owned = {a['kind']: a for a in self.animation_allocations}
            if (target, source, count, self.read(sp)) != (owned['unit_metadata']['pointer'], owned['unit_file_buffer']['pointer'], self.unit_inputs['metadata_bytes'], 4234372):
                raise RuntimeError('scene animation metadata copy ownership')
            self.primitive_write(target, bytes(uc.mem_read(source, count)))
            self._stub_return(target, 0)
            return
        if address == 4320320:
            args = [self.read(sp + 4 + i * 4) for i in range(7)]
            file = next((a['pointer'] for a in self.animation_allocations if a['kind'] == 'unit_file_buffer'))
            metadata = next((a['pointer'] for a in self.animation_allocations if a['kind'] == 'unit_metadata'))
            if receiver != self.controller + 24 or args != [0, self.texture_table, metadata + self.unit_inputs['offsets'][5], file + self.unit_inputs['metadata_bytes'], 0, file + self.unit_inputs['palette_offset'], file + self.unit_inputs['offsets'][8]]:
                raise RuntimeError(f'scene animation palette/mask binding {args}')
            self.animation_binding = {'receiver': receiver, 'args': args, 'caller_return_va': hex(self.read(sp))}
            self.visited.add(address)
            return
        if address == 5692832:
            args = tuple((self.read(sp + i) for i in (4, 8, 12, 16, 20)))
            a = self.animation_allocations[-1]
            if a['kind'] != 'unit_texture_array' or args != (a['pointer'] + 4, 84, self.unit_inputs['count'], 4323376, 4323472):
                raise RuntimeError('scene animation bounded texture vector')
            self.vector_pending = args[:4]
            self.animation_vector = {'target': args[0], 'stride': args[1], 'count': args[2], 'constructor_va': hex(args[3]), 'destructor_va': hex(args[4]), 'native_constructors_completed': 0, 'iteration_outside_instruction_hook': True}
            self.stop_reason = 'first_unit_texture_vector'
            uc.emu_stop()
            return
        if address == 5689024:
            (target, byte, count) = [self.read(sp + i) for i in (4, 8, 12)]
            a = next((a for a in self.animation_allocations if a['kind'] == 'unit_texture_array'), None)
            if not a or byte != 0 or count != 4 or (self.read(sp) != 4323774) or (not a['pointer'] + 4 + 36 <= target <= a['pointer'] + a['bytes'] - 4) or (target - a['pointer'] - 4 - 36) % 84:
                raise RuntimeError('scene animation exact texture clear primitive')
            self.primitive_write(target, bytes(count))
            self._stub_return(target, 0)
            return
        if address == 4322112:
            (device, buffer, index, records, left, right) = [self.read(sp + i) for i in (4, 8, 12, 16, 20, 24)]
            owned = {a['kind']: a for a in self.animation_allocations}
            base = owned['unit_file_buffer']['pointer']
            selected = base + self.unit_inputs['palette_offset'] if self.read(base + self.unit_inputs['offsets'][8] + index, 'B') == 0 else 0
            if device != 0 or buffer != base + self.unit_inputs['metadata_bytes'] or index != len(self.animation_entries) or (index >= self.unit_inputs['count']) or (records != owned['unit_texture_array']['pointer'] + 4) or ((left, right) != (0, selected)):
                raise RuntimeError('scene animation texture source/order/palette mask')
            offset = self.read(buffer + 8 + index * 4)
            end = self.read(buffer + 8 + (index + 1) * 4) if index < self.unit_inputs['count'] - 1 else self.read(buffer)
            if not 8 + 4 * self.unit_inputs['count'] <= offset < end <= self.unit_inputs['image_bytes']:
                raise RuntimeError('scene animation texture entry bounds')
            self.active_texture = {'index': index, 'offset': offset, 'file_offset': self.unit_inputs['metadata_bytes'] + offset, 'bytes': end - offset, 'header_hex': bytes(uc.mem_read(buffer + offset, 16)).hex(), 'record_pointer': records + index * 84, 'palette_pointer': selected, 'mask_value': self.read(base + self.unit_inputs['offsets'][8] + index, 'B')}
            self.animation_entries.append(self.active_texture)
            self.visited.add(address)
            return
        if address == 4209616:
            if not self.animation_entries or receiver != self.active_texture['record_pointer'] or [self.read(sp + 4), self.read(sp + 8)] != [0, 0]:
                raise RuntimeError('scene animation exact GPU creation boundary')
            self.animation_boundaries.append({'kind': 'texture_creation', 'index': self.active_texture['index'], 'width': self.read(receiver + 56, 'H'), 'height': self.read(receiver + 58, 'H'), 'format': self.read(receiver + 52)})
            self._stub_return(0, 8)
            return
        if address == 4211024:
            args = [self.read(sp + 4 + i * 4) for i in range(4)]
            if not self.animation_entries or receiver != self.active_texture['record_pointer'] or args != [self.animation_request['buffer_pointer'] + self.active_texture['file_offset'], 1, 0, self.active_texture['palette_pointer']]:
                raise RuntimeError(f'scene animation exact GPU pixel/palette upload boundary: {receiver:#x} {args} entry {self.active_texture}')
            bmp = args[0]
            body = self.read(bmp + 10)
            (w, h) = (self.read(bmp + 18), self.read(bmp + 22))
            palette = args[3] or bmp + 54
            self.active_texture.update({'pixel_sha256': hashlib.sha256(bytes(uc.mem_read(bmp + body, (w + 3 & ~3) * h))).hexdigest(), 'upload_palette_pointer': palette, 'upload_palette_hex': bytes(uc.mem_read(palette, 1024)).hex(), 'upload_palette_sha256': hashlib.sha256(bytes(uc.mem_read(palette, 1024))).hexdigest()})
            self.animation_boundaries.append({'kind': 'pixel_upload', 'index': self.active_texture['index'], 'args': args, 'palette_sha256': self.active_texture['upload_palette_sha256'], 'pixel_sha256': self.active_texture['pixel_sha256']})
            self._stub_return(0, 16)
            return
        if address == 4360912:
            pointer = self.read(sp + 4)
            owned = next((a for a in self.animation_allocations if a['pointer'] == pointer and (not a['freed'])), None)
            if not owned or owned['kind'] != 'unit_file_buffer' or self.read(sp) != 4234845 or (len(self.animation_entries) != self.unit_inputs['count']):
                raise RuntimeError('scene animation source release ownership/order')
            self.animation_file_release = {'pointer': pointer, 'bytes': owned['bytes'], 'caller_return_va': hex(self.read(sp)), 'sha256_at_release': hashlib.sha256(bytes(uc.mem_read(pointer, owned['bytes']))).hexdigest()}
            owned['freed'] = True
            self.animation_boundaries.append({'kind': 'source_file_release', **self.animation_file_release})
            self._stub_return(0, 0)
            return
        return ExitEmulator._hook(self, uc, address, size, context)

    def _scene_tail_hook(self, uc, address, size, context):
        if not self.scene_complete_loading:
            return super()._hook(uc, address, size, context)
        if address == 4535856:
            if uc.reg_read(UC_X86_REG_EAX) != 0 or uc.reg_read(UC_X86_REG_ESP) != self.constructor_return_sp:
                raise RuntimeError('first constructor original return/stack differs')
            self.stop_reason = 'after_first_scene_unit_constructor_return'
            uc.emu_stop()
            return
        if address in (4345728, 4360768, 4360912, 5692832, 4522160):
            raise RuntimeError(f'unexpected first constructor assertion/allocation/resource at {address:#x}')
        if address in self.constructor_code:
            self.visited.add(address)
            return
        (sp, receiver) = (uc.reg_read(UC_X86_REG_ESP), uc.reg_read(UC_X86_REG_ECX))
        work = UNITCTRL + WORK_OFFSET + self.active_index * WORK_BYTES
        if address == 5689024:
            (target, byte, count) = [self.read(sp + i) for i in (4, 8, 12)]
            allowed = [(work + o, 88, 4235034) for o in [72, *[160 + i * 88 for i in range(5)]]]
            allowed += [(work + o, 236, 4422845) for o in (756, 992)]
            allowed += [(UNITCTRL + SHARED_OFFSET, SHARED_BYTES, 4722565)]
            if byte != 0 or (target, count, self.read(sp)) not in allowed:
                raise RuntimeError('first constructor exact owned clear')
            self.primitive_write(target, bytes(count))
            self.constructor_clears.append({'target': target, 'bytes': count, 'caller_return_va': hex(self.read(sp))})
            self._stub_return(target, 0)
            return
        if address in self.constructor_entries:
            argc = {4608064: 3, 4235248: 4, 4621968: 3, 4441200: 3, 4635840: 2}.get(address, 1)
            self.constructor_calls.append({'va': hex(address), 'receiver': receiver, 'args': [self.read(sp + 4 + i * 4) for i in range(argc)], 'caller_return_va': hex(self.read(sp))})
            self.visited.add(address)
            return
        return ExitEmulator._hook(self, uc, address, size, context)

    def _prepare_scene_constructor(self):
        work = UNITCTRL + WORK_OFFSET + self.active_index * WORK_BYTES
        record = UNITCTRL + RECORD_OFFSET + self.active_index * 176
        (header, cm) = (self.read(UNITCTRL + 172804), self.read(UNITCTRL + 172808))
        (width, height) = (self.read(header + 4, 'H'), self.read(header + 6, 'H'))
        (x, y) = (self.read(record + 155, 'B'), self.read(record + 156, 'B'))
        if not (0 <= x < width and 0 <= y < height) or (width, height) != (64, 96):
            raise RuntimeError('first constructor source logical coordinates/bounds')
        self.constructor_cm = self.read(cm)
        self.constructor_cell = self.constructor_cm + 2 * (y * width + x) + 1
        (self.constructor_calls, self.constructor_clears) = ([], [])
        outer_frame = self.read(self.uc.reg_read(UC_X86_REG_EBP))
        if self.read(outer_frame + 4) != 4535856:
            raise RuntimeError('first constructor actual outer frame/caller')
        self.constructor_return_sp = outer_frame + 12
        return {'work_pointer': work, 'record_pointer': record, 'index': self.active_index, 'before_work_hex': bytes(self.uc.mem_read(work, WORK_BYTES)).hex(), 'record_hex': bytes(self.uc.mem_read(record, 176)).hex(), 'shared_pointer': UNITCTRL + SHARED_OFFSET, 'before_shared_hex': bytes(self.uc.mem_read(UNITCTRL + SHARED_OFFSET, SHARED_BYTES)).hex(), 'cm_pointer': cm, 'cm_data_pointer': self.constructor_cm, 'cm_bytes': width * height * 2, 'before_cm_hex': bytes(self.uc.mem_read(self.constructor_cm, width * height * 2)).hex(), 'cell_counter_pointer': self.constructor_cell, 'constructor_coordinates': [x, y], 'logical_dimensions': [width, height], 'return_sp': self.constructor_return_sp}

def report():
    e=SchoolSceneUnitConstructorEmulator()
    if not e.run_planning('scene_constructor_upstream')['school_data_prepared']:raise RuntimeError('scene constructor school prefix missing')
    checkpoint=[(a,bytes(e.uc.mem_read(a,b-a+1))) for a,b,_ in e.uc.mem_regions()];cpu=e.uc.context_save();cases=[]
    for name,commands in [('initial',()),('student9_waiting',[('student',9,-1)]),
        ('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1),('student',9,-1)]),
        ('teacher_only',[('student',3,-1),('student',4,-1),('student',9,-1)]),('teacher_waiting',[('teacher',101,-1)])]:
        for at,raw in checkpoint:e.uc.mem_write(at,raw)
        e.uc.context_restore(cpu);e.scene_complete_loading=False;e.stop_reason=None
        cases.append(e.resources(name,commands));print('Native scene constructor '+name+': '+str(cases[-1]['scene_unit_constructor_completed']),flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
        'boundary':'Exactly first scene-unit animation and4680B0 naturally complete at453630. Other34 templates, deployment and VM remain unexecuted; GPU declared.',**AUTHORITY}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
