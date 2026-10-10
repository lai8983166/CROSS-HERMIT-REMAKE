"""Actual next scene template input, plus separately declared original cache queries."""
import argparse,hashlib,json,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_ECX,UC_X86_REG_EAX
from tools.school_scene_unit_constructor_emulation import (
 SchoolSceneUnitConstructorEmulator,ROOT,SOURCE,SOURCE_SHA256,BASE,UNITCTRL,TACT,TASK,
 RECORD_OFFSET,WORK_OFFSET,WORK_BYTES,STACK,RETURN,SCENE_CONTROLLER,CACHE_OFFSET,CACHE_COUNT,COUNTER_OFFSET,ExitEmulator,AUTHORITY,report_text,cstring)
from tools.school_enemy_records_emulation import SchoolEnemyRecordsEmulator,SCRATCH
from tools.school_scene_unit_work_catalog import EVIDENCE as PREFIX_EVIDENCE,EVIDENCE_SHA256 as PREFIX_SHA
from tools.school_scene_unit_constructor_catalog import EVIDENCE as FIRST_EVIDENCE,EVIDENCE_SHA256 as FIRST_SHA

class SchoolSceneNextInputEmulator(SchoolSceneUnitConstructorEmulator):
    def __init__(self):
        self.next_loading=False;self.next_phase=None
        super().__init__();self.next_controller=SCENE_CONTROLLER+96
        self._function_ranges+=((0x466DA0,0x466E1C),)

    def capture_scene_retained(self):
        return self._next_capture_retained() if self.next_loading else super().capture_scene_retained()

    def finish_scene_work(self):
        return self._next_finish_work() if self.next_loading else super().finish_scene_work()

    def run_scene_thread(self):
        # Preserve the frozen upstream driver. Resume time/instruction yields
        # at their actual EIP; neither a return nor a successful phase is faked.
        vectors=0;self.stop_reason=None
        for _ in range(8):
            self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30_000_000,count=12_000_000)
            if self.stop_reason=='before_unit_art_reset':break
            if self.stop_reason=='scene_texture_vector':
                vectors+=1
                if vectors>1:raise RuntimeError('unexpected upstream scene vectors')
                target,stride,count,ctor=self.vector_pending
                cpu=self.uc.context_save();stack=bytes(self.uc.mem_read(STACK,0x10000))
                for i in range(count):self.call(ctor,receiver=target+i*stride)
                self.uc.mem_write(STACK,stack);self.uc.context_restore(cpu)
                self._stub_return(0,20);self.stop_reason=None
            elif self.stop_reason is not None:raise RuntimeError('unexpected upstream scene stop')
        else:raise RuntimeError('upstream scene resource traversal exceeded finite batches')
        if self.handles:raise RuntimeError('upstream scene handles remain open')

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.next_loading:return super()._write_hook(uc,access,address,size,value,context)
        if self.next_phase=='prefix':return self._next_prefix_write(uc,access,address,size,value,context)
        allowed=[(STACK,STACK+0x10000),(0,4)]
        if self.next_phase in ('loop','record'):allowed.append((TACT+0x40,TACT+0x42))
        if self.next_phase=='record' and self.enemy_record:
            p=self.enemy_record['record_pointer'];allowed.append((p,p+176))
            if self.enemy_record['identity']<200:allowed.append((SCRATCH,SCRATCH+48))
        if not any(a<=address and address+size<=b for a,b in allowed):
            raise RuntimeError(f'next scene finite guard {address:#x}/{size} phase{self.next_phase}')
        if not STACK<=address<STACK+0x10000:self.writes.append((address,size,value&((1<<(8*size))-1)))

    def _hook(self,uc,address,size,context):
        if not self.next_loading:return super()._hook(uc,address,size,context)
        if self.next_phase=='prefix':return self._next_prefix_hook(uc,address,size,context)
        if self.next_phase=='cache_query':
            if 0x466DA0<=address<0x466E1C:self.visited.add(address);return
            if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
            raise RuntimeError(f'undeclared cache query code {address:#x}')
        sp=uc.reg_read(UC_X86_REG_ESP);receiver=uc.reg_read(UC_X86_REG_ECX)
        if address==0x4680B0:
            if self.next_phase!='record' or (receiver,self.read(sp),self.read(sp+4))!=(UNITCTRL,0x453630,248):
                raise RuntimeError('second scene natural constructor input')
            self.next_record=self.finish_record();self.stop_reason='before_second_scene_unit_work';uc.emu_stop();return
        if address==0x451D80:
            if self.next_phase!='loop' or (receiver,self.read(sp))!=(TACT,0x453638):raise RuntimeError('second scene progress input')
            self.next_progress={'caller_return_va':hex(self.read(sp)),
                'before_hex':bytes(uc.mem_read(TACT+0x40,2)).hex(),'primitives':[]}
            self.visited.add(address);return
        if address in (0x451E20,0x415420,0x422360):
            recv,caller,pop={0x451E20:(TACT,0x451DF1,0),0x415420:(TASK,0x451DFC,0),0x422360:(TACT,0x451E06,4)}[address]
            if (receiver,self.read(sp))!=(recv,caller) or (pop and self.read(sp+4)!=0):raise RuntimeError('second scene graphics/scheduler args')
            if address==0x451E20:self.next_progress['after_hex']=bytes(uc.mem_read(TACT+0x40,2)).hex()
            self.next_progress['primitives'].append({'va':hex(address),'receiver':receiver,'caller_return_va':hex(caller)})
            self._stub_return(0,pop);return
        if 0x451D80<=address<0x451E19:self.visited.add(address);return
        if address==0x4DA450:self.next_phase='record'
        if self.next_phase=='record':return SchoolEnemyRecordsEmulator._hook(self,uc,address,size,context)
        if address in self.enemy_code:self.visited.add(address);return
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        raise RuntimeError(f'undeclared next scene loop code {address:#x}')

    def resources(self,name,commands=()):
        self.next_loading=False;result=super().resources(name,commands)
        result.update({'second_scene_input_prepared':False,'second_scene_record':None,'second_scene_work':None,'scene_progress':None})
        if not result['ready']:return result
        retained=self.capture_scene_memory([(TACT+0x40,TACT+0x42),
            (UNITCTRL+RECORD_OFFSET+248*176,UNITCTRL+RECORD_OFFSET+249*176)])
        self.enemy_ordinal=1;self.enemy_mode='actual_school';self.enemy_record=None;self.enemy_loading=True
        self.next_phase='loop';self.next_loading=True;self.next_progress=None
        try:
            self.clear_trace('tactical_startup');self.stop_reason=None
            self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=3_000_000,count=200_000)
            if self.stop_reason!='before_second_scene_unit_work' or self.handles:raise RuntimeError('second record boundary missing')
            preservation=self.verify_scene_memory(retained)
            self.next_progress.update(preservation);self.next_progress['coverage']=self.coverage()
            self.enemy_loading=False;self.next_phase='prefix'
            self.begin_scene_work(1,'actual_school_second_scene_unit')
            self.clear_trace('tactical_startup');self.stop_reason=None
            self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=3_000_000,count=200_000)
            if self.stop_reason!='before_second_scene_unit_animation_load':raise RuntimeError('second animation request missing')
            prefix=self.finish_scene_work()
            result.update({'second_scene_input_prepared':True,'second_scene_record':self.next_record,
                'second_scene_work':prefix,'scene_progress':self.next_progress,'stop_reason':self.stop_reason})
            return result
        finally:self.next_loading=False;self.enemy_loading=False

    def query(self,cache,group,palette):
        if not isinstance(cache,(bytes,bytearray)) or len(cache)!=CACHE_COUNT*8:
            raise ValueError('declared cache query requires exact4096-byte input')
        if any(type(v) is not int or not -2**31<=v<2**31 for v in (group,palette)):
            raise ValueError('declared cache query requires signed32 arguments')
        cache=bytes(cache)
        self.uc.mem_write(UNITCTRL+CACHE_OFFSET,cache)
        self.next_loading=True;self.next_phase='cache_query';self.clear_trace('tactical_startup')
        sp=STACK+0xFF00;self.write(sp,RETURN);self.write(sp+4,group&0xFFFFFFFF);self.write(sp+8,palette&0xFFFFFFFF)
        self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,UNITCTRL)
        self.uc.emu_start(0x466DA0,RETURN,timeout=1_000_000,count=50_000)
        if self.uc.reg_read(UC_X86_REG_EIP)!=RETURN or self.uc.reg_read(UC_X86_REG_ESP)!=sp+12:
            raise RuntimeError('cache query native return/stack')
        after=bytes(self.uc.mem_read(UNITCTRL+CACHE_OFFSET,CACHE_COUNT*8))
        if after!=cache:raise RuntimeError('read-only cache query changed cache')
        return {'group':group,'palette':palette,'cache_hex':cache.hex(),'cache_after_hex':after.hex(),
            'return_pointer':self.uc.reg_read(UC_X86_REG_EAX),'return_sp':sp+12,'cache_unchanged':True,'coverage':self.coverage()}


    def _next_prefix_write(self, uc, access, address, size, value, context):
        if not self.next_loading:
            return super()._write_hook(uc, access, address, size, value, context)
        s = self.scene_work
        allowed = [(STACK, STACK + 65536), (0, 4)]
        if s:
            allowed += [(s['work_pointer'], s['work_pointer'] + WORK_BYTES), (s['record_pointer'], s['record_pointer'] + 176), (s['cache_pointer'], s['cache_pointer'] + 8), (UNITCTRL + COUNTER_OFFSET, UNITCTRL + COUNTER_OFFSET + 4)]
            if s.get('allocation'):
                allowed.append((self.next_controller, self.next_controller + 84))
        if not any((a <= address and address + size <= b for (a, b) in allowed)):
            raise RuntimeError(f'scene work finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        if not STACK <= address < STACK + 65536:
            self.writes.append((address, size, value & (1 << size * 8) - 1))

    def _next_capture_retained(self):
        s = self.scene_work
        excluded = [(STACK, STACK + 65536), (0, 4), (s['work_pointer'], s['work_pointer'] + WORK_BYTES), (s['record_pointer'], s['record_pointer'] + 176), (s['cache_pointer'], s['cache_pointer'] + 8), (UNITCTRL + COUNTER_OFFSET, UNITCTRL + COUNTER_OFFSET + 4), (self.next_controller, self.next_controller + 84)]
        spans = []
        for (start, end, _) in self.uc.mem_regions():
            pieces = [(start, end + 1)]
            for (left, right) in excluded:
                pieces = [p for (a, b) in pieces for p in ((a, min(b, left)), (max(a, right), b)) if p[0] < p[1]]
            spans.extend(((a, bytes(self.uc.mem_read(a, b - a))) for (a, b) in pieces))
        return spans

    def _next_finish_work(self):
        s = self.scene_work
        retained = s.pop('retained_before')
        if any((bytes(self.uc.mem_read(a, len(raw))) != raw for (a, raw) in retained)):
            raise RuntimeError('scene prefix changed retained memory')
        if not s['resource_request'] or not s['allocation'] or self.handles:
            raise RuntimeError('scene prefix missed natural empty-handle request')
        s.update({'work_hex': bytes(self.uc.mem_read(s['work_pointer'], WORK_BYTES)).hex(), 'record_hex': bytes(self.uc.mem_read(s['record_pointer'], 176)).hex(), 'cache_hex': bytes(self.uc.mem_read(UNITCTRL + CACHE_OFFSET, CACHE_COUNT * 8)).hex(), 'counter': self.read(UNITCTRL + COUNTER_OFFSET), 'controller_hex': bytes(self.uc.mem_read(self.next_controller, 84)).hex(), 'retained_ranges_unchanged': True, 'retained_bytes': sum((len(raw) for (_, raw) in retained)), 'retained_ranges': [{'pointer': a, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()} for (a, raw) in retained], 'constructor_completed': False, 'animation_loaded': False, 'scene_placement_executed': False, 'scene_vm_executed': False, 'coverage': self.coverage()})
        return deepcopy(s)

    def _next_prefix_hook(self, uc, address, size, context):
        if not self.next_loading:
            return super()._hook(uc, address, size, context)
        s = self.scene_work
        sp = uc.reg_read(UC_X86_REG_ESP)
        recv = uc.reg_read(UC_X86_REG_ECX)
        if address == 4620464:
            caller = 4535856 if s['evidence_kind'] == 'actual_school_second_scene_unit' else RETURN
            if (recv, self.read(sp), self.read(sp + 4)) != (UNITCTRL, caller, s['index']):
                raise RuntimeError('scene prefix natural constructor input')
            s['constructor_entry'] = {'receiver': recv, 'caller_return_va': hex(self.read(sp)), 'index': self.read(sp + 4)}
        if address == 5089040:
            args = [self.read(sp + 4), self.read(sp + 8)]
            if args != [s['template_pointer'], s['work_pointer']] or self.read(sp) != 4673825:
                raise RuntimeError('scene prefix exact status overlay')
            s['calls'].append({'va': hex(address), 'args': args, 'caller_return_va': hex(self.read(sp))})
        if address == 5689024:
            (target, byte, count) = [self.read(sp + i) for i in (4, 8, 12)]
            allowed = [(s['work_pointer'], WORK_BYTES, 4620634), (s['work_pointer'] + 656, 92, 4673509)]
            if byte or (target, count, self.read(sp)) not in allowed:
                raise RuntimeError('scene prefix exact clear')
            self.primitive_write(target, bytes(count))
            s['clears'].append({'pointer': target, 'bytes': count, 'caller_return_va': hex(self.read(sp))})
            self._stub_return(target, 0)
            return
        if address == 4360768:
            if s['allocation'] or (self.read(sp + 4), self.read(sp)) != (84, 4615096) or any(uc.mem_read(self.next_controller, 84)):
                raise RuntimeError('scene prefix exact controller allocation')
            s['allocation'] = {'pointer': self.next_controller, 'bytes': 84, 'freed': False, 'caller_return_va': hex(self.read(sp))}
            s['primitives'].append({'kind': 'heap_allocation', **s['allocation']})
            self._stub_return(self.next_controller, 0)
            return
        if address == 4371152:
            args = [self.read(sp + i) for i in (8, 12, 16)]
            if self.read(sp) != 4616500 or cstring(self, self.read(sp + 4)) != 'char:%03d, job:%03d : palette:%03d\n' or args != [s['role'], s['job'], s['variant'] - 1]:
                raise RuntimeError('scene prefix exact debug output')
            s['primitives'].append({'kind': 'debug_log', 'args': args})
            self._stub_return(0, 0)
            return
        if address == 4615296:
            args = [self.read(sp + i) for i in (4, 8, 12)]
            if recv != UNITCTRL or args != [s['cache_pointer'], s['group'], s['variant']]:
                raise RuntimeError('scene prefix exact cache binding')
            s['calls'].append({'va': hex(address), 'receiver': recv, 'args': args})
        if address == 4607344:
            if recv != self.next_controller or [self.read(sp + 4), self.read(sp + 8)] != [s['renderer'], s['group'] + 8]:
                raise RuntimeError('scene prefix source animation binding')
        if address == 4522160:
            args = [self.read(sp + 4 + i * 4) for i in range(4)]
            expected = [self.read(6358328 + s['group'] * 8), s['variant'], int(s['variant'] != 0), 0]
            if recv != s['renderer'] + 524288 or self.read(sp) != 4607775 or args != expected or s['resource_request']:
                raise RuntimeError('scene prefix exact source animation request')
            s['resource_request'] = {'receiver': recv, 'caller_return_va': hex(self.read(sp)), 'args': args, 'relative_path': cstring(self, args[0]), 'loaded': False}
            self.stop_reason = 'before_second_scene_unit_animation_load'
            uc.emu_stop()
            return
        if address in self.scene_work_code:
            self.visited.add(address)
            return
        if address == 5688960:
            return ExitEmulator._hook(self, uc, address, size, context)
        raise RuntimeError(f'undeclared scene prefix code {address:#x}')

def cache_report():
    raw=PREFIX_EVIDENCE.read_bytes();first=FIRST_EVIDENCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=PREFIX_SHA or hashlib.sha256(first).hexdigest()!=FIRST_SHA:raise ValueError('declared cache seed identity')
    prefixes=json.loads(raw)['declared_scene_prefix_diagnostic']['units']
    seed=bytes.fromhex(json.loads(first)['cases'][0]['scene_unit_work']['cache_hex'])
    e=SchoolSceneNextInputEmulator();cache=bytearray(seed);queries=[]
    retained=e.capture_scene_memory([(UNITCTRL+CACHE_OFFSET,UNITCTRL+CACHE_OFFSET+CACHE_COUNT*8)])
    for p in prefixes:
        q=e.query(bytes(cache),p['group'],p['variant']);q['ordinal']=p['ordinal'];q['declared_insertion']=None
        if not q['return_pointer']:
            slot=next(i for i in range(CACHE_COUNT) if cache[i*8]==0)
            entry=struct.pack('<BBHI',1,p['variant'],p['group'],0x1A000000+p['ordinal']*96)
            cache[slot*8:slot*8+8]=entry
            q['declared_insertion']={'slot':slot,'entry_hex':entry.hex(),'opaque_controller_token_not_allocation':True}
        q['driver_cache_after_hex']=cache.hex();queries.append(q)
    boundary=[]
    def probe(name,rows,group,palette):
        c=bytearray(CACHE_COUNT*8)
        for slot,used,g,p in rows:struct.pack_into('<BBHI',c,slot*8,used,p&255,g&65535,0x1B000000+slot*96)
        q=e.query(bytes(c),group,palette);q['name']=name;boundary.append(q)
    probe('last_slot',[(511,1,4,5)],4,5)
    probe('first_duplicate',[(1,1,4,5),(511,1,4,5)],4,5)
    probe('inactive_match_skipped',[(0,0,4,5),(511,1,4,5)],4,5)
    probe('signed_nonzero_match',[(511,255,-1,-1)],-1,-1)
    probe('unsigned_query_does_not_match_signed_row',[(511,255,-1,-1)],65535,255)
    probe('full_cache_miss',[(i,1,301,1) for i in range(512)],383,1)
    preservation=e.verify_scene_memory(retained)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,
        'evidence_kind':'declared_scene5_ordered_read_only_cache_query_driver',
        'seed_report_sha256':FIRST_SHA,'keys_report_sha256':PREFIX_SHA,'seed_cache_hex':seed.hex(),
        'queries':queries,'boundary_probes':boundary,'final_declared_cache_hex':cache.hex(),
        'hits':sum(bool(q['return_pointer']) for q in queries),'misses':sum(not q['return_pointer'] for q in queries),
        'declared_insertions':True,'controller_allocation_executed':False,'cache_binding_executed':False,
        'school_scene_loop_executed':False,'constructors_executed':False,'archives_loaded':False,
        **preservation,**AUTHORITY}

def report():
    e=SchoolSceneNextInputEmulator()
    if not e.run_planning('scene_next_upstream')['school_data_prepared']:raise RuntimeError('school prefix missing')
    checkpoint=[(a,bytes(e.uc.mem_read(a,b-a+1))) for a,b,_ in e.uc.mem_regions()];cpu=e.uc.context_save();cases=[]
    for name,commands in [('initial',()),('student9_waiting',[('student',9,-1)]),
        ('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1),('student',9,-1)]),
        ('teacher_only',[('student',3,-1),('student',4,-1),('student',9,-1)]),('teacher_waiting',[('teacher',101,-1)])]:
        for at,raw in checkpoint:e.uc.mem_write(at,raw)
        e.uc.context_restore(cpu);e.next_loading=False;e.stop_reason=None
        cases.append(e.resources(name,commands));print('Actual next scene input '+name+': '+str(cases[-1]['second_scene_input_prepared']),flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
        'boundary':'Actual second template progress/record/work input only. Stop before51e animation loading; no completed second constructor or remaining loop/deployment/VM.',**AUTHORITY}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--cache-only',action='store_true');a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('use a new immutable evidence path')
    path.write_text(report_text(cache_report() if a.cache_only else report()),encoding='utf-8',newline='\n')
