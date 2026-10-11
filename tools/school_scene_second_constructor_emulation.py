"""Finish actual second scene-unit51e mode0 binding and special-role387 tail."""
import argparse,hashlib,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_ECX,UC_X86_REG_EAX
from tools.school_scene_next_input_emulation import SchoolSceneNextInputEmulator
from tools.school_scene_unit_constructor_emulation import (
 ROOT,SOURCE,SOURCE_SHA256,BASE,UNITCTRL,TACT,TASK,STACK,RETURN,WORK_OFFSET,WORK_BYTES,
 RECORD_OFFSET,SCENE_CONTROLLER,ExitEmulator,AUTHORITY,report_text,cstring,
 FILE_API,FILE_IMPORTS,SchoolTacticalResourcesEmulator,SHARED_OFFSET,SHARED_BYTES)
from tools.dxanim_lib import parse_dxanim,parse_container

SECOND_ANIM,SECOND_ANIM_BYTES=0x1B000000,0x400000
SECOND_PATH='data\\DxAnim\\51e.bin'
SECOND_SHA='13251ba4450863865b66b9e7d0a5582fb5fd63b00af164c83013ff8aa343a43f'

def second_resource(job=387,variant=0,rules=None):
 if type(job) is not int or job!=387 or type(variant) is not int or variant!=0:
  raise ValueError('unsupported second scene-unit job/palette')
 p=ROOT/'CROSS HERMIT/CROSS HERMIT/data/DxAnim/51e.bin';raw=p.read_bytes()
 if hashlib.sha256(raw).hexdigest()!=SECOND_SHA:raise ValueError('second scene-unit source identity')
 o=parse_dxanim(raw)
 if len(o)!=9 or any(a>b for a,b in zip(o,o[1:])):raise ValueError('second scene-unit section shape')
 image_bytes,count,_=parse_container(raw,o[6]);_,palettes,_=parse_container(raw,o[7])
 if count!=126 or palettes!=4 or len(raw)-o[8]!=128 or raw[o[8]+126:]!=bytes(2):
  raise ValueError('second scene-unit image/palette/mask shape')
 return raw,{'relative_path':SECOND_PATH,'local_file':p.relative_to(ROOT).as_posix(),
  'bytes':len(raw),'sha256':SECOND_SHA},{'offsets':o,'metadata_bytes':o[6],
  'image_bytes':image_bytes,'count':count,'palette_offset':None,'variant':variant}

class SchoolSceneSecondConstructorEmulator(SchoolSceneNextInputEmulator):
 def __init__(self):
  self.second_loading=False
  super().__init__();self.uc.mem_map(SECOND_ANIM,SECOND_ANIM_BYTES)
  extra=((0x46A950,0x46AA22),(0x46C290,0x46C33C))
  self.constructor_code=self.constructor_code|frozenset(a for s,t in extra for a in range(s,t))

 def _write_hook(self,uc,access,address,size,value,context):
  if not self.second_loading:return super()._write_hook(uc,access,address,size,value,context)
  if self.scene_phase=='tail':
   w=UNITCTRL+WORK_OFFSET+248*WORK_BYTES;r=UNITCTRL+RECORD_OFFSET+248*176
   allowed=[(STACK,STACK+0x10000),(0,4),(w,w+WORK_BYTES),
    (UNITCTRL+SHARED_OFFSET,UNITCTRL+SHARED_OFFSET+SHARED_BYTES),
    (self.constructor_cell,self.constructor_cell+1),(r+0x9F,r+0xA0)]
   if not any(a<=address and address+size<=b for a,b in allowed):
    raise RuntimeError(f'second scene tail finite guard{address:#x}/{size} at{uc.reg_read(UC_X86_REG_EIP):#x}')
   if not STACK<=address<STACK+0x10000:self.writes.append((address,size,value&((1<<(size*8))-1)))
   return
  return super()._write_hook(uc,access,address,size,value,context)

 def _hook(self,uc,address,size,context):
  if not self.second_loading:return super()._hook(uc,address,size,context)
  return self._second_animation_dispatch(uc,address,size,context)

 def resources(self,name,commands=()):
  self.second_loading=False;result=super().resources(name,commands)
  result.update({'second_scene_animation_loaded':False,'second_scene_animation':None,
   'second_scene_constructor_completed':False,'second_scene_constructor':None})
  if not result['ready']:return result
  self.second_loading=True
  try:
   animation=self.run_second_animation();tail=self.run_second_tail()
   result.update({'second_scene_animation_loaded':True,'second_scene_animation':animation,
    'second_scene_constructor_completed':True,'second_scene_constructor':tail,
    'stop_reason':self.stop_reason,'file_events':deepcopy(self.file_events)})
   return result
  finally:self.second_loading=False

 def animation_allocate(self, count, kind, caller):
     if not self.second_loading:
         return super().animation_allocate(count, kind, caller)
     at = self.scene_animation_cursor
     end = at + (count + 15 & ~15)
     if self.scene_phase != 'animation' or count <= 0 or end > SECOND_ANIM + SECOND_ANIM_BYTES:
         raise RuntimeError('scene animation finite allocation')
     self.scene_animation_cursor = end
     self.animation_allocations.append({'pointer': at, 'bytes': count, 'kind': kind, 'caller_return_va': hex(caller), 'freed': False})
     return at

 def _file_api(self, address, sp):
     if not self.second_loading:
         return super()._file_api(address, sp)
     if self.scene_phase != 'animation':
         raise RuntimeError('scene file API outside animation phase')
     (_, (name, pop)) = list(FILE_IMPORTS.items())[(address - FILE_API) // 16]
     if name == 'CreateFileA':
         args = [self.read(sp + 4 + i * 4) for i in range(7)]
         if cstring(self, args[0]) != SECOND_PATH or args[1:] != [2147483648, 1, 0, 3, 1, 0] or self.handles:
             raise RuntimeError('scene exact read-only file arguments')
         (raw, identity, _) = second_resource(387, self.current['variant'])
         handle = 3584
         self.handles[handle] = {'raw': raw, 'identity': identity}
         self.file_events.append({'name': name, 'args': args, 'result': handle})
         self._stub_return(handle, pop)
         return
     if name == 'ReadFile':
         (handle, target, count, written, overlapped) = [self.read(sp + 4 + i * 4) for i in range(5)]
         owned = [a for a in self.animation_allocations if a['kind'] == 'unit_file_buffer' and (not a['freed'])]
         if handle not in self.handles or overlapped or len(owned) != 1 or ((target, count) != (owned[0]['pointer'], self.unit_identity['bytes'])):
             raise RuntimeError('scene exact file read ownership')
         self.primitive_write(target, self.handles[handle]['raw'])
         self.primitive_write(written, struct.pack('<I', count))
         self.animation_request.update({'buffer_pointer': target, 'loaded_bytes': count, 'loaded_sha256': hashlib.sha256(bytes(self.uc.mem_read(target, count))).hexdigest(), 'loaded': True})
         self.file_events.append({'name': name, 'args': [handle, target, count, written, overlapped], 'result': 1})
         self._stub_return(1, pop)
         return
     return SchoolTacticalResourcesEmulator._file_api(self, address, sp)

 def _second_animation_dispatch(self, uc, address, size, context):
     if not self.scene_complete_loading:
         return super()._hook(uc, address, size, context)
     if self.scene_phase == 'animation':
         if address == 4616519:
             if self.handles or self.read(self.controller + 64) != 1 or len(self.animation_entries) != 126 or (self.animation_vector['native_constructors_completed'] != 126):
                 raise RuntimeError('scene incomplete archive binding')
             self.stop_reason = 'after_second_scene_unit_animation_binding'
             uc.emu_stop()
             return
         return self._second_animation_hook(uc, address, size, context)
     if self.scene_phase == 'tail':
         if address == 0x453630:
             if uc.reg_read(UC_X86_REG_EAX)!=0 or uc.reg_read(UC_X86_REG_ESP)!=self.constructor_return_sp:
                 raise RuntimeError('second constructor original return/stack differs')
             self.stop_reason='after_second_scene_unit_constructor_return';uc.emu_stop();return
         return self._scene_tail_hook(uc, address, size, context)
     raise RuntimeError('scene constructor invalid phase')

 def run_second_animation(self, variant=0):
     (raw, self.unit_identity, self.unit_inputs) = second_resource(387, variant)
     self.reset_animation()
     self.scene_animation_cursor = SECOND_ANIM
     self.controller = self.next_controller
     self.active_index = 248
     self.unit_path = SECOND_PATH
     self.scene_texture_slot = self.read(self.controller + 40)
     if self.scene_texture_slot not in (113, 114) or any(self.uc.mem_read(self.texture_table + self.scene_texture_slot * 8, 8)):
         raise RuntimeError('scene exact empty texture slot')
     before_controller = bytes(self.uc.mem_read(self.controller, 84)).hex()
     cursor = SECOND_ANIM
     excluded = []
     for count in (len(raw), self.unit_inputs['metadata_bytes'], 126 * 84 + 4):
         excluded.append((cursor, cursor + count))
         cursor += count + 15 & ~15
     excluded += [(self.controller, self.controller + 84), (TASK + 526568, TASK + 526828), (7999164, 7999424), (self.texture_table + self.scene_texture_slot * 8, self.texture_table + (self.scene_texture_slot + 1) * 8)]
     retained = self.capture_scene_memory(excluded)
     before_events = len(self.file_events)
     prefix_current = self.current
     self.current = {'job': 387, 'variant': variant}
     self.clear_trace('tactical_startup')
     self.stop_reason = None
     self.scene_phase = 'animation'
     self.scene_complete_loading = True
     try:
         for batch in range(8):
             self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP), RETURN, timeout=30000000, count=1000000)
             if self.stop_reason == 'first_unit_texture_vector':
                 (target, stride, count, ctor) = self.vector_pending
                 cpu = self.uc.context_save()
                 stack = bytes(self.uc.mem_read(STACK, 65536))
                 for i in range(count):
                     self.call(ctor, receiver=target + i * stride)
                     self.animation_vector['native_constructors_completed'] += 1
                 self.uc.mem_write(STACK, stack)
                 self.uc.context_restore(cpu)
                 self._stub_return(0, 20)
                 self.stop_reason = None
                 continue
             if self.stop_reason == 'after_second_scene_unit_animation_binding':
                 break
         else:
             raise RuntimeError('scene animation exceeded finite batches')
         preservation = self.verify_scene_memory(retained)
         for e in self.animation_entries:
             e['raw_record_hex'] = bytes(self.uc.mem_read(e['record_pointer'], 84)).hex()
         return {'index': 248, 'controller': self.controller, 'before_controller_hex': before_controller, 'controller_hex': bytes(self.uc.mem_read(self.controller, 84)).hex(), 'metadata_pointer': self.read(self.controller), 'metadata_hex': bytes(self.uc.mem_read(self.read(self.controller), self.unit_inputs['metadata_bytes'])).hex(), 'texture_slot': self.scene_texture_slot, 'texture_slot_hex': bytes(self.uc.mem_read(self.texture_table + self.scene_texture_slot * 8, 8)).hex(), 'texture_table': self.texture_table, 'variant': variant, 'request': deepcopy(self.animation_request), 'allocations': deepcopy(self.animation_allocations), 'entries': deepcopy(self.animation_entries), 'binding': deepcopy(self.animation_binding), 'vector': deepcopy(self.animation_vector), 'boundaries': deepcopy(self.animation_boundaries), 'file_release': deepcopy(self.animation_file_release), 'file_events': deepcopy(self.file_events[before_events:]), 'coverage': self.coverage(), 'constructor_completed': False, 'scene_placement_executed': False, **preservation}
     finally:
         self.current = prefix_current
         self.scene_complete_loading = False

 def run_second_tail(self):
     snap = self._prepare_scene_constructor()
     snap['relation_selector'] = self.read(UNITCTRL+0x2EF44, 'B')
     snap['relation_hex'] = bytes(self.uc.mem_read(UNITCTRL+0x115AAC,256)).hex()
     retained = self.capture_scene_memory([(snap['work_pointer'], snap['work_pointer'] + WORK_BYTES), (UNITCTRL + SHARED_OFFSET, UNITCTRL + SHARED_OFFSET + SHARED_BYTES), (self.constructor_cell, self.constructor_cell + 1), (snap['record_pointer']+0x9F, snap['record_pointer']+0xA0)])
     self.scene_phase = 'tail'
     self.clear_trace('tactical_startup')
     self.stop_reason = None
     self.scene_complete_loading = True
     try:
         self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP), RETURN, timeout=30000000, count=500000)
         if self.stop_reason != 'after_second_scene_unit_constructor_return' or self.handles:
             raise RuntimeError('scene constructor missed natural return')
         preservation = self.verify_scene_memory(retained)
         after = bytes(self.uc.mem_read(self.constructor_cm, 12288))
         prior = bytearray.fromhex(snap['before_cm_hex'])
         at = self.constructor_cell - self.constructor_cm
         prior[at] = prior[at] + 1 & 255
         if after != bytes(prior):
             raise RuntimeError('scene constructor exact cell accounting')
         snap.update({'before_record_hex': snap['record_hex'], 'record_hex': bytes(self.uc.mem_read(snap['record_pointer'],176)).hex(), 'work_hex': bytes(self.uc.mem_read(snap['work_pointer'], WORK_BYTES)).hex(), 'shared_hex': bytes(self.uc.mem_read(snap['shared_pointer'], SHARED_BYTES)).hex(), 'cm_hex': after.hex(), 'cm_sha256': hashlib.sha256(after).hexdigest(), 'calls': deepcopy(self.constructor_calls), 'clears': deepcopy(self.constructor_clears), 'return_va': '0x453630', 'return_eax': self.uc.reg_read(UC_X86_REG_EAX), 'constructor_completed': True, 'unit_animation_work_bound': True, 'scene_placement_executed': False, 'scene_vm_executed': False, 'coverage': self.coverage(), **preservation})
         return snap
     finally:
         self.scene_complete_loading = False

 def _second_animation_hook(self, uc, address, size, context):
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
         if self.animation_request or self.read(sp) != 4607775 or receiver != TASK + 524288 or (cstring(self, args[0]) != self.unit_path) or (args[1:] != [self.current['variant'], 0, 0]):
             raise RuntimeError('scene animation source file request')
         (_, identity, _) = second_resource(self.current['job'], self.current['variant'], self.current_rules)
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
         if receiver != self.controller + 24 or args != [0, self.texture_table, metadata + self.unit_inputs['offsets'][5], file + self.unit_inputs['metadata_bytes'], 0, 0, 0]:
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
         selected = 0
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

def report():
 e=SchoolSceneSecondConstructorEmulator()
 if not e.run_planning('scene_second_upstream')['school_data_prepared']:raise RuntimeError('school prefix missing')
 checkpoint=[(a,bytes(e.uc.mem_read(a,b-a+1))) for a,b,_ in e.uc.mem_regions()];cpu=e.uc.context_save();cases=[]
 for name,commands in [('initial',()),('student9_waiting',[('student',9,-1)]),
  ('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1),('student',9,-1)]),
  ('teacher_only',[('student',3,-1),('student',4,-1),('student',9,-1)]),('teacher_waiting',[('teacher',101,-1)])]:
  for at,raw in checkpoint:e.uc.mem_write(at,raw)
  e.uc.context_restore(cpu);e.second_loading=False;e.stop_reason=None
  cases.append(e.resources(name,commands))
  print('Actual second scene constructor '+name+': '+str(cases[-1]['second_scene_constructor_completed']),flush=True)
 return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
  'boundary':'Actual second scene-unit51e mode0 binding and complete4680B0 at natural453630. Remaining33/placement/VM unexecuted; GPU declared.',**AUTHORITY}

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
 if path.exists():p.error('use a new immutable evidence path')
 path.write_text(report_text(report()),encoding='utf-8',newline='\n')
