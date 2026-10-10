"""Original current-unit loops on actual school CPU; stop before enemies."""
import argparse
from copy import deepcopy
import hashlib
import struct
from unicorn.x86_const import UC_X86_REG_ECX,UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_EAX,UC_X86_REG_EBP
from tools.school_first_unit_constructor_emulation import (
    SchoolFirstUnitConstructorEmulator,SHARED_OFFSET,SHARED_BYTES,UNIT_POOL,UNIT_POOL_SIZE,
    WORK_OFFSET,WORK_BYTES,RECORD_OFFSET,CACHE_OFFSET,CACHE_COUNT,COUNTER_OFFSET,
    MAP_POOL,MAP_POOL_SIZE,ASSET_POOL,ASSET_POOL_SIZE,SCENE_POOL,SCENE_POOL_SIZE,UHEAP,UHEAP_SIZE,
    UNITCTRL,POOL,POOL_SIZE,TACT,SCRIPT_WORK,GROUP_TASK,CHAR_BASE,UNITS,ROOT,SOURCE,SOURCE_SHA256,
    BASE,TASK,STACK,RETURN,report_text,ExitEmulator,AUTHORITY,WORK_GROUPS,ANIM_POOL,ANIM_POOL_SIZE)
from tools.school_first_unit_work_catalog import source_catalog as work_catalog
from tools.school_tactical_resources_emulation import FILE_API,FILE_IMPORTS,SchoolTacticalResourcesEmulator,cstring
from tools.dxanim_lib import parse_dxanim,parse_container

CONTROLLERS,CONTROLLER_BYTES = 0x16000000,0x10000
CURRENT_ANIM,CURRENT_ANIM_BYTES = 0x17000000,0x400000


def current_resource(job,variant,rules=None):
    rules = work_catalog() if rules is None else rules
    jobs = [j for j in rules['jobs'] if j['job']==job]
    if len(jobs)!=1 or type(variant) is not int or not 1<=variant<=40:
        raise ValueError('unsupported current unit job/palette')
    j = jobs[0];identity = j['resource_identity']
    raw = (ROOT/identity['path']).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=identity['sha256']:
        raise ValueError('current unit archive identity')
    offsets = parse_dxanim(raw)
    if len(offsets)!=9 or any(a>b for a,b in zip(offsets,offsets[1:])):
        raise ValueError('current unit archive section bounds')
    image_bytes,count,_ = parse_container(raw,offsets[6])
    _,palettes,entries = parse_container(raw,offsets[7])
    if count not in (147,193,219) or palettes!=40 or offsets[8]+((count+3)&~3)!=len(raw):
        raise ValueError('current unit image/palette/mask shape')
    return raw,{'relative_path':j['relative_path'],'local_file':identity['path'],'bytes':len(raw),'sha256':identity['sha256']}, \
        {'offsets':offsets,'metadata_bytes':offsets[6],'image_bytes':image_bytes,'count':count,
         'palette_offset':offsets[7]+entries[variant-1],'variant':variant}


class SchoolCurrentUnitsEmulator(SchoolFirstUnitConstructorEmulator):
    def __init__(self):
        self.current_loading = False
        super().__init__()
        self._function_ranges += ((0x451D80,0x451E19),)
        self.current_observed = {0x4680B0,0x467147,0x4533FA,0x453481,0x453540,
            0x451D80,0x451E20,0x415420,0x422360,0x56D4D0,0x56CEC0,0x428A40,0x428AD0,
            0x56D810,0x42B2D0,0x56DDA0,0x4500B0,0x4142B0,0x41EC40,0x41F340,
            0x403BD0,0x404150,0x424F80,0x41EFD0,0x465040,0x409FF0,0x468690,0x43C470}
        self.current_code = frozenset(a for s,t in self._function_ranges for a in range(s,t))-self.current_observed
        self.uc.mem_map(CONTROLLERS,CONTROLLER_BYTES)
        self.uc.mem_map(CURRENT_ANIM,CURRENT_ANIM_BYTES)
        self.current_rules = work_catalog()
        self.reset_current()

    def reset_current(self):
        self.current_phase = 'loop'
        self.controller_cursor,self.current_animation_cursor = CONTROLLERS,CURRENT_ANIM
        self.current_controller_allocations,self.current_animation_allocations = [],[]
        self.current_units,self.current_copies,self.current_progress,self.current_primitives = [],[],[],[]
        self.current_pending = None
        self.current = None

    def _write_hook(self,uc,access,address,size,value,context):
        if not getattr(self,'current_loading',False):
            return super()._write_hook(uc,access,address,size,value,context)
        allowed = [(STACK,STACK+0x10000),(0,4),(TACT+0x40,TACT+0x42)]
        if self.current_pending is not None and self.current_phase=='loop':
            p = UNITCTRL+RECORD_OFFSET+self.current_pending*176
            allowed.append((p,p+176))
        if self.current:
            w = self.current['work_pointer']
            allowed.append((w,w+WORK_BYTES))
            if self.current_phase=='prefix':
                p = self.current['record_pointer'];allowed.append((p,p+176))
                if not self.current['cache_hit']:
                    p = UNITCTRL+CACHE_OFFSET+self.current['cache_slot']*8
                    allowed += [(p,p+8),(UNITCTRL+COUNTER_OFFSET,UNITCTRL+COUNTER_OFFSET+4)]
            if self.current_phase=='animation':
                allowed += [(self.controller,self.controller+84),(TASK+0x808E8,TASK+0x809EC),(0x7A0EBC,0x7A0FC0),
                    (self.texture_table+self.current['texture_slot']*8,self.texture_table+(self.current['texture_slot']+1)*8)]
                allowed += [(a['pointer'],a['pointer']+a['bytes']) for a in self.animation_allocations if not a['freed']]
            if self.current_phase=='prefix' and self.current.get('allocation'):
                p = self.current['allocation']['pointer'];allowed.append((p,p+84))
            if self.current_phase=='tail':
                allowed += [(UNITCTRL+SHARED_OFFSET,UNITCTRL+SHARED_OFFSET+SHARED_BYTES),
                    (self.constructor_cell,self.constructor_cell+1)]
        if not any(a<=address and address+size<=b for a,b in allowed):
            raise RuntimeError(f'current units finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x} phase {self.current_phase}')
        if not STACK<=address<STACK+0x10000:
            self.writes.append((address,size,value & ((1<<(size*8))-1)));self.startup_writes.append((address,size))

    def retained(self):
        spans = [(CHAR_BASE,0x7F4488-CHAR_BASE),(0x7CF34C,45*0x124),(0x7A528E,4),
            (0x7F4488,UNITS-0x7F4488),(UNITS,len(self.combat_records)*176),(MAP_POOL,69368),(UNIT_POOL,84)]
        spans += [(a['pointer'],a['bytes']) for a in self.asset_allocations+self.original_animation_allocations+self.current_animation_allocations if not a['freed']]
        spans += [(UNITCTRL+o,n*s) for o,n,s,p in WORK_GROUPS]
        spans += [(a['pointer'],84) for a in self.current_controller_allocations]
        spans += [(u['work_pointer'],WORK_BYTES) for u in self.current_units]
        spans += [(u['record_pointer'],176) for u in self.current_units]
        spans += [(self.texture_table+u['texture_slot']*8,8) for u in self.current_units]
        spans += [(self.texture_table+100*8,8)]
        return [(a,bytes(self.uc.mem_read(a,n))) for a,n in spans]

    def begin_current(self,sp):
        index = self.read(sp+4)
        if index!=self.current_pending or index in [u['index'] for u in self.current_units] or not 0<=index<len(self.combat_records):
            raise RuntimeError('current constructor natural index/copy/order')
        work,record = UNITCTRL+WORK_OFFSET+index*WORK_BYTES,UNITCTRL+RECORD_OFFSET+index*176
        raw = bytes(self.uc.mem_read(record,176));role,job = self.read(record+2,'H'),self.read(record+12,'H')
        j = next((j for j in self.current_rules['jobs'] if j['job']==job),None)
        if not j or not 1<=role<=34 or raw[0xF]!=1 or raw[0xA4]>=4 or any(self.uc.mem_read(work,WORK_BYTES)):
            raise RuntimeError('unsupported initialized current record/work')
        variant = j['palettes_by_character'][role]+1
        _,identity,inputs = current_resource(job,variant,self.current_rules)
        cache = bytes(self.uc.mem_read(UNITCTRL+CACHE_OFFSET,CACHE_COUNT*8))
        matching = [i for i in range(CACHE_COUNT) if cache[i*8]==1 and cache[i*8+1]==variant and struct.unpack_from('<H',cache,i*8+2)[0]==j['group']]
        empty = [i for i in range(CACHE_COUNT) if cache[i*8]==0]
        if len(matching)>1 or (not matching and not empty):raise RuntimeError('current finite cache ownership')
        slot = matching[0] if matching else empty[0]
        self.current = {'index':index,'role':role,'job':job,'variant':variant,'work_pointer':work,'record_pointer':record,
            'before_record_hex':raw.hex(),'before_work_hex':bytes(WORK_BYTES).hex(),'cache_before_hex':cache.hex(),
            'counter_before':self.read(UNITCTRL+COUNTER_OFFSET),'cache_slot':slot,'cache_hit':bool(matching),
            'source':identity,'inputs':inputs,'calls':[],'clears':[],'boundaries':[],
            'constructor_entry_sp':sp,'return_va':hex(self.read(sp)),'retained_before':self.retained()}
        self.controller = self.read(UNITCTRL+CACHE_OFFSET+slot*8+4) if matching else None
        self.current_phase = 'prefix';self.active_index = index;self.current_pending = None
        self.reset_animation();self.animation_cursor = self.current_animation_cursor
        self.unit_inputs,self.unit_identity,self.unit_path = inputs,identity,identity['relative_path']

    def animation_allocate(self,count,kind,caller):
        if not getattr(self,'current_loading',False):return super().animation_allocate(count,kind,caller)
        at,end = self.current_animation_cursor,self.current_animation_cursor+((count+15)&~15)
        if count<=0 or end>CURRENT_ANIM+CURRENT_ANIM_BYTES:raise RuntimeError('current finite animation allocation')
        self.current_animation_cursor = end
        a = {'pointer':at,'bytes':count,'kind':kind,'caller_return_va':hex(caller),'freed':False,'index':self.active_index}
        self.animation_allocations.append(a);self.current_animation_allocations.append(a)
        return at

    def _file_api(self,address,sp):
        if not getattr(self,'current_loading',False):return super()._file_api(address,sp)
        if self.current_phase!='animation':raise RuntimeError('current file API outside resource phase')
        _,(name,pop) = list(FILE_IMPORTS.items())[(address-FILE_API)//16]
        if name=='CreateFileA':
            args = [self.read(sp+4+i*4) for i in range(7)]
            if cstring(self,args[0])!=self.unit_path or args[1:]!=[0x80000000,1,0,3,1,0] or self.handles:
                raise RuntimeError('current exact read-only file arguments')
            raw,identity,_ = current_resource(self.current['job'],self.current['variant'],self.current_rules)
            handle = 0xD00+self.active_index
            self.handles[handle] = {'raw':raw,'identity':identity};self.file_events.append({'name':name,'args':args,'result':handle})
            self._stub_return(handle,pop);return
        if name=='ReadFile':
            handle,target,count,written,overlapped = [self.read(sp+4+i*4) for i in range(5)]
            owned = [a for a in self.animation_allocations if a['kind']=='unit_file_buffer' and not a['freed']]
            if handle not in self.handles or overlapped or len(owned)!=1 or (target,count)!=(owned[0]['pointer'],self.unit_identity['bytes']):
                raise RuntimeError('current exact file read ownership')
            self.primitive_write(target,self.handles[handle]['raw']);self.primitive_write(written,struct.pack('<I',count))
            self.animation_request.update({'buffer_pointer':target,'loaded_bytes':count,'loaded_sha256':hashlib.sha256(bytes(self.uc.mem_read(target,count))).hexdigest(),'loaded':True})
            self.file_events.append({'name':name,'args':[handle,target,count,written,overlapped],'result':1});self._stub_return(1,pop);return
        return SchoolTacticalResourcesEmulator._file_api(self,address,sp)

    def enter_tail(self):
        c = self.current;work = c['work_pointer']
        if self.current_phase=='animation' and (self.read(self.controller+0x40)!=1 or len(self.animation_entries)!=self.unit_inputs['count'] \
            or self.animation_vector['native_constructors_completed']!=self.unit_inputs['count']):
            raise RuntimeError('current incomplete archive binding')
        cache_pointer = self.uc.reg_read(UC_X86_REG_EAX)
        if cache_pointer!=UNITCTRL+CACHE_OFFSET+c['cache_slot']*8 or self.read(cache_pointer+4)!=self.controller:
            raise RuntimeError('current source cache/controller result')
        c.update({'prefix_work_hex':bytes(self.uc.mem_read(work,WORK_BYTES)).hex(),
            'prefix_record_hex':bytes(self.uc.mem_read(c['record_pointer'],176)).hex(),
            'cache_after_hex':bytes(self.uc.mem_read(UNITCTRL+CACHE_OFFSET,CACHE_COUNT*8)).hex(),
            'counter_after':self.read(UNITCTRL+COUNTER_OFFSET),'controller':self.controller,
            'controller_hex':bytes(self.uc.mem_read(self.controller,84)).hex(),'metadata_pointer':self.read(self.controller),
            'texture_slot':self.read(self.controller+0x28),
            'metadata_hex':bytes(self.uc.mem_read(self.read(self.controller),self.unit_inputs['metadata_bytes'])).hex(),
            'entries':deepcopy(self.animation_entries),'animation_allocations':deepcopy(self.animation_allocations),
            'animation_boundaries':deepcopy(self.animation_boundaries),'vector':deepcopy(self.animation_vector),
            'request':deepcopy(self.animation_request),'file_release':deepcopy(self.animation_file_release)})
        for e in c['entries']:e['raw_record_hex'] = bytes(self.uc.mem_read(e['record_pointer'],84)).hex()
        cm = self.read(UNITCTRL+0x2A308);self.constructor_cm = self.read(cm)
        x,y = self.read(c['record_pointer']+0x9B,'B'),self.read(c['record_pointer']+0x9C,'B')
        if x>=64 or y>=96:raise RuntimeError('current source coordinates')
        self.constructor_cell = self.constructor_cm+2*(y*64+x)+1
        c['before_cm_hex'] = bytes(self.uc.mem_read(self.constructor_cm,12288)).hex()
        c['tail_retained'] = [(self.controller,bytes(self.uc.mem_read(self.controller,84)))]
        c['tail_retained'] += [(a['pointer'],bytes(self.uc.mem_read(a['pointer'],a['bytes']))) for a in self.animation_allocations if not a['freed']]
        self.current_phase = 'tail'

    def finish_current(self,address):
        c = self.current
        if hex(address)!=c['return_va'] or self.uc.reg_read(UC_X86_REG_ESP)!=c['constructor_entry_sp']+8 or self.uc.reg_read(UC_X86_REG_EAX)!=0:
            raise RuntimeError('current natural constructor return/stack')
        for a,raw in c.pop('retained_before')+c.pop('tail_retained'):
            if bytes(self.uc.mem_read(a,len(raw)))!=raw:raise RuntimeError(f'current constructor changed retained bytes {a:#x}')
        after = bytes(self.uc.mem_read(self.constructor_cm,12288));before = bytearray.fromhex(c['before_cm_hex'])
        at = self.constructor_cell-self.constructor_cm;before[at] = (before[at]+1)&255
        if after!=bytes(before):raise RuntimeError('current logical cell accounting')
        c.update({'work_hex':bytes(self.uc.mem_read(c['work_pointer'],WORK_BYTES)).hex(),
            'record_hex':bytes(self.uc.mem_read(c['record_pointer'],176)).hex(),
            'shared_hex':bytes(self.uc.mem_read(UNITCTRL+SHARED_OFFSET,SHARED_BYTES)).hex(),
            'cm_hex':after.hex(),'cm_pointer':self.constructor_cm,'constructor_completed':True,
            'retained_ranges_unchanged':True,'scene_placement_executed':False,'return_eax':0})
        self.current_units.append(c);self.current = None;self.current_phase = 'loop'

    def _hook(self,uc,address,size,context):
        if not getattr(self,'current_loading',False):return super()._hook(uc,address,size,context)
        if address in (0x424F80,0x41EFD0):raise RuntimeError('unexpected current assertion/dynamic slot')
        sp,receiver = uc.reg_read(UC_X86_REG_ESP),uc.reg_read(UC_X86_REG_ECX)
        if address==0x453540:
            if self.current or self.current_pending is not None or len(self.current_units)!=len(self.combat_records):
                raise RuntimeError('current loops missed a selected unit')
            self.stop_reason = 'before_enemy_unit_construction';uc.emu_stop();return
        if address in (0x4533FA,0x453481) and self.current_phase=='tail':self.finish_current(address)
        if address==0x4680B0:
            if receiver!=UNITCTRL:raise RuntimeError('current constructor receiver')
            self.begin_current(sp);self.visited.add(address);return
        if address==0x467147:
            if self.current_phase not in ('prefix','animation') or self.handles:raise RuntimeError('current cache binding phase')
            self.enter_tail();self.visited.add(address);return
        if self.current_phase=='animation':return self._animation_hook(uc,address,size,context)
        if address in (0x56DDA0,0x428AD0,0x56D810,0x4142B0,0x41EC40,0x41F340,0x403BD0,0x404150):
            raise RuntimeError('current archive boundary outside loading phase')
        if address==0x4500B0:
            if self.current_phase!='prefix' or not self.current.get('allocation'):raise RuntimeError('unexpected current resource request')
            self.current['controller_before_hex'] = bytes(uc.mem_read(self.controller,84)).hex()
            self.current['texture_slot'] = self.read(self.controller+0x28)
            slot = self.current['texture_slot']
            if not 111<=slot<114 or any(uc.mem_read(self.texture_table+slot*8,8)):raise RuntimeError('current exact empty texture slot')
            self.current_phase = 'animation'
            return self._animation_hook(uc,address,size,context)
        if address==0x56D4D0:
            target,source,count = [self.read(sp+i) for i in (4,8,12)]
            index = (source-UNITS)//176
            if self.current_phase!='loop' or count!=176 or source!=UNITS+index*176 or target!=UNITCTRL+RECORD_OFFSET+index*176 \
                or not 0<=index<len(self.combat_records) or self.read(sp) not in (0x4533E5,0x45346C):
                raise RuntimeError('current exact source copy')
            self.current_pending = index
            raw = bytes(uc.mem_read(source,count));self.primitive_write(target,raw)
            self.current_copies.append({'index':index,'source':source,'target':target,'record_hex':raw.hex(),'caller_return_va':hex(self.read(sp))})
            self._stub_return(target,0);return
        if address==0x428A40:
            if self.current_phase!='prefix' or self.current['cache_hit'] or self.current.get('allocation') or (self.read(sp+4),self.read(sp))!=(84,0x466BB8):
                raise RuntimeError('current controller allocation ownership')
            at = self.controller_cursor;self.controller_cursor += 96
            if self.controller_cursor>CONTROLLERS+CONTROLLER_BYTES:raise RuntimeError('current controller pool exhausted')
            a = {'pointer':at,'bytes':84,'kind':'unit_animation_controller','freed':False,'index':self.active_index}
            self.current['allocation'] = a;self.current_controller_allocations.append(a);self.controller = at
            self._stub_return(at,0);return
        if address==0x56CEC0:
            target,byte,count = [self.read(sp+i) for i in (4,8,12)]
            if not self.current or byte:raise RuntimeError('current owned clear phase')
            work = self.current['work_pointer'];caller = self.read(sp)
            allowed = [(work,WORK_BYTES,0x46815A),(work+0x290,92,0x474FE5)] if self.current_phase=='prefix' else \
                [(work+o,88,0x409F1A) for o in [0x48,*[0xA0+i*88 for i in range(5)]]]+ \
                [(work+o,236,0x437CBD) for o in (0x2F4,0x3E0)]+[(UNITCTRL+SHARED_OFFSET,42,0x480F85)]
            if (target,count,caller) not in allowed:raise RuntimeError('current exact clear target/count/caller')
            self.primitive_write(target,bytes(count));self.current['clears'].append({'target':target,'bytes':count,'caller_return_va':hex(caller)})
            self._stub_return(target,0);return
        if address==0x42B2D0:
            if not self.current or self.read(sp)!=0x467134 or cstring(self,self.read(sp+4))!='char:%03d, job:%03d : palette:%03d\n':
                raise RuntimeError('current exact debug output')
            args = [self.read(sp+i) for i in (8,12,16)]
            if args!=[self.current['role'],self.current['job'],self.current['variant']-1]:raise RuntimeError('current debug source args')
            self.current['boundaries'].append({'kind':'debug_log','args':args});self._stub_return(0,0);return
        if address==0x451D80:
            if receiver!=TACT or self.current_phase!='loop':raise RuntimeError('current progress receiver/phase')
            self.current_progress.append({'caller_return_va':hex(self.read(sp)),'before_hex':bytes(uc.mem_read(TACT+0x40,2)).hex()})
            self.visited.add(address);return
        if address in (0x451E20,0x415420,0x422360):
            expected = {0x451E20:(TACT,0x451DF1,0),0x415420:(TASK,0x451DFC,0),0x422360:(TACT,0x451E06,4)}
            recv,caller,pop = expected[address]
            if (receiver,self.read(sp))!=(recv,caller) or (pop and self.read(sp+4)!=0):raise RuntimeError('current exact graphics/scheduler primitive')
            if address==0x451E20:self.current_progress[-1]['after_hex'] = bytes(uc.mem_read(TACT+0x40,2)).hex()
            self.current_primitives.append({'va':hex(address),'receiver':receiver,'caller_return_va':hex(caller)});self._stub_return(0,pop);return
        if address in (0x465040,0x409FF0,0x468690,0x43C470):
            argc = {0x465040:3,0x409FF0:4,0x468690:3,0x43C470:3}[address]
            if not self.current:raise RuntimeError('current work helper phase')
            self.current['calls'].append({'va':hex(address),'receiver':receiver,'args':[self.read(sp+4+i*4) for i in range(argc)]})
            self.visited.add(address);return
        if address in self.current_code or address in (0x4533FA,0x453481):self.visited.add(address);return
        return ExitEmulator._hook(self,uc,address,size,context)

    def run_current(self):
        self.stop_reason = None;batches = 0
        while True:
            self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30_000_000,count=12_000_000)
            if self.stop_reason=='first_unit_texture_vector':
                target,stride,count,ctor = self.vector_pending
                cpu,stack = self.uc.context_save(),bytes(self.uc.mem_read(STACK,0x10000))
                for i in range(count):
                    self.call(ctor,receiver=target+i*stride);self.animation_vector['native_constructors_completed'] += 1
                self.uc.mem_write(STACK,stack);self.uc.context_restore(cpu);self._stub_return(0,20);self.stop_reason = None
                continue
            if self.stop_reason=='before_enemy_unit_construction':break
            batches += 1
            if batches>8:raise RuntimeError('current loop exceeded finite instruction batches')
        if self.handles:raise RuntimeError('current loop left open resource handles')

    def resources(self,name,commands=()):
        self.current_loading = False;self.reset_current()
        result = super().resources(name,commands)
        result.update({'current_units_constructed':False,'current_units':[],'current_loop':None})
        if not result['ready']:return result
        first = result['first_unit_constructor'];animation = result['first_unit_animation']
        self.original_animation_allocations = deepcopy(self.animation_allocations)
        self.current_units = [{'index':first['index'],'role':self.read(first['record_pointer']+2,'H'),
            'job':self.read(first['record_pointer']+12,'H'),'work_pointer':first['work_pointer'],
            'record_pointer':first['record_pointer'],'work_hex':first['work_hex'],'record_hex':first['record_hex'],
            'texture_slot':animation['texture_slot'],'controller':animation['controller'],'metadata_pointer':animation['metadata_pointer'],
            'constructor_completed':True,'first_constructor_checkpoint':True}]
        header = bytes(self.uc.mem_read(0x7F4488,UNITS-0x7F4488))
        before_records = [bytes(self.uc.mem_read(UNITS+i*176,176)).hex() for i in range(len(self.combat_records))]
        before_progress = bytes(self.uc.mem_read(TACT+0x40,2)).hex()
        self.current_loading = True;self.clear_trace('tactical_startup');self.run_current();self.current_loading = False
        if header!=bytes(self.uc.mem_read(0x7F4488,len(header))) or before_records!=[bytes(self.uc.mem_read(UNITS+i*176,176)).hex() for i in range(len(self.combat_records))]:
            raise RuntimeError('current loops changed source global records/header')
        result.update({'current_units_constructed':True,'current_units':deepcopy(self.current_units),
            'current_loop':{'source_header_hex':header.hex(),'source_records':before_records,
                'before_progress_hex':before_progress,'after_progress_hex':bytes(self.uc.mem_read(TACT+0x40,2)).hex(),
                'progress':deepcopy(self.current_progress),'primitives':deepcopy(self.current_primitives),
                'copies':deepcopy(self.current_copies),'controller_allocations':deepcopy(self.current_controller_allocations),
                'animation_allocations':deepcopy(self.current_animation_allocations),
                'cache_hex':bytes(self.uc.mem_read(UNITCTRL+CACHE_OFFSET,CACHE_COUNT*8)).hex(),
                'counter':self.read(UNITCTRL+COUNTER_OFFSET),'cm_hex':bytes(self.uc.mem_read(self.read(self.read(UNITCTRL+0x2A308)),12288)).hex(),
                'retained_ranges_unchanged':True,'enemy_constructor_executed':False,'scene_placement_executed':False},
            'file_events':deepcopy(self.file_events),'stop_reason':self.stop_reason})
        result['phases'].append({'phase':'natural_all_current_unit_constructors','coverage':self.coverage()})
        return result

    def _animation_hook(self,uc,address,size,context):
        if address in self.animation_code:
            self.visited.add(address)
            return
        sp,receiver = uc.reg_read(UC_X86_REG_ESP),uc.reg_read(UC_X86_REG_ECX)
        if address in (0x424F80,0x41EFD0):
            raise RuntimeError(f'unexpected current animation assertion/dynamic slot at {address:#x}')
        if FILE_API<=address<FILE_API+len(FILE_IMPORTS)*16 and (address-FILE_API)%16==0:
            return self._file_api(address,sp)
        if address==0x4500B0:
            args = [self.read(sp+4+i*4) for i in range(4)]
            if self.animation_request or self.read(sp)!=0x464F1F or receiver!=TASK+0x80000 \
                or cstring(self,args[0])!=self.unit_path or args[1:]!=[self.current['variant'],1,0]:
                raise RuntimeError('current animation source file request')
            _,identity,_ = current_resource(self.current['job'],self.current['variant'],self.current_rules)
            self.animation_request = {'receiver':receiver,'args':args,'source':identity,
                                      'caller_return_va':hex(self.read(sp)),'loaded':False}
            self.visited.add(address)
            return
        if address==0x4142B0:
            if receiver!=TASK or self.read(sp)!=0x464F2F:
                raise RuntimeError('current animation renderer device query')
            self.visited.add(address)
            return
        if address==0x428A40:
            count,caller = self.read(sp+4),self.read(sp)
            if caller==0x42AD54 and self.handles and count==len(next(iter(self.handles.values()))['raw']):
                kind = 'unit_file_buffer'
            elif caller==0x409C53 and count==self.unit_inputs['metadata_bytes']:
                kind = 'unit_metadata'
            elif caller==0x41F142 and count==self.unit_inputs['count']*84+4:
                kind = 'unit_texture_array'
            else:
                raise RuntimeError(f'current animation allocation caller/count {caller:#x}/{count}')
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
                raise RuntimeError('current animation exact source path formatting')
            if value!=self.unit_path:
                raise RuntimeError('current animation formatted source path')
            self.primitive_write(target,value.encode('ascii')+b'\0')
            self._stub_return(len(value),0)
            return
        if address==0x56D4D0:
            target,source,count = [self.read(sp+i) for i in (4,8,12)]
            owned = {a['kind']:a for a in self.animation_allocations}
            if (target,source,count,self.read(sp))!=(owned['unit_metadata']['pointer'],owned['unit_file_buffer']['pointer'],self.unit_inputs['metadata_bytes'],0x409C84):
                raise RuntimeError('current animation metadata copy ownership')
            self.primitive_write(target,bytes(uc.mem_read(source,count)))
            self._stub_return(target,0)
            return
        if address==0x41EC40:
            args = [self.read(sp+4+i*4) for i in range(7)]
            file = next(a['pointer'] for a in self.animation_allocations if a['kind']=='unit_file_buffer')
            metadata = next(a['pointer'] for a in self.animation_allocations if a['kind']=='unit_metadata')
            if receiver!=self.controller+0x18 or args!=[0,self.texture_table,metadata+self.unit_inputs['offsets'][5],file+self.unit_inputs['metadata_bytes'],0,file+self.unit_inputs['palette_offset'],file+self.unit_inputs['offsets'][8]]:
                raise RuntimeError(f'current animation palette/mask binding {args}')
            self.animation_binding = {'receiver':receiver,'args':args,'caller_return_va':hex(self.read(sp))}
            self.visited.add(address)
            return
        if address==0x56DDA0:
            args = tuple(self.read(sp+i) for i in (4,8,12,16,20))
            a = self.animation_allocations[-1]
            if a['kind']!='unit_texture_array' or args!=(a['pointer']+4,84,self.unit_inputs['count'],0x41F830,0x41F890):
                raise RuntimeError('current animation bounded texture vector')
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
                raise RuntimeError('current animation exact texture clear primitive')
            self.primitive_write(target,bytes(count))
            self._stub_return(target,0)
            return
        if address==0x41F340:
            device,buffer,index,records,left,right = [self.read(sp+i) for i in (4,8,12,16,20,24)]
            owned = {a['kind']:a for a in self.animation_allocations}
            base = owned['unit_file_buffer']['pointer']
            selected = base+self.unit_inputs['palette_offset'] if self.read(base+self.unit_inputs['offsets'][8]+index,'B')==0 else 0
            if device!=0 or buffer!=base+self.unit_inputs['metadata_bytes'] or index!=len(self.animation_entries) or index>=self.unit_inputs['count'] \
                or records!=owned['unit_texture_array']['pointer']+4 or (left,right)!=(0,selected):
                raise RuntimeError('current animation texture source/order/palette mask')
            offset = self.read(buffer+8+index*4)
            end = self.read(buffer+8+(index+1)*4) if index<self.unit_inputs['count']-1 else self.read(buffer)
            if not (8+4*self.unit_inputs['count'])<=offset<end<=self.unit_inputs['image_bytes']:
                raise RuntimeError('current animation texture entry bounds')
            self.active_texture = {'index':index,'offset':offset,'file_offset':self.unit_inputs['metadata_bytes']+offset,
                'bytes':end-offset,'header_hex':bytes(uc.mem_read(buffer+offset,16)).hex(),
                'record_pointer':records+index*84,'palette_pointer':selected,
                'mask_value':self.read(base+self.unit_inputs['offsets'][8]+index,'B')}
            self.animation_entries.append(self.active_texture)
            self.visited.add(address)
            return
        if address==0x403BD0:
            if not self.animation_entries or receiver!=self.active_texture['record_pointer'] or [self.read(sp+4),self.read(sp+8)]!=[0,0]:
                raise RuntimeError('current animation exact GPU creation boundary')
            self.animation_boundaries.append({'kind':'texture_creation','index':self.active_texture['index'],
                'width':self.read(receiver+0x38,'H'),'height':self.read(receiver+0x3A,'H'),'format':self.read(receiver+0x34)})
            self._stub_return(0,8)
            return
        if address==0x404150:
            args = [self.read(sp+4+i*4) for i in range(4)]
            if not self.animation_entries or receiver!=self.active_texture['record_pointer'] \
                or args!=[self.animation_request['buffer_pointer']+self.active_texture['file_offset'],1,0,self.active_texture['palette_pointer']]:
                raise RuntimeError(f'current animation exact GPU pixel/palette upload boundary: {receiver:#x} {args} entry {self.active_texture}')
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
            if not owned or owned['kind']!='unit_file_buffer' or self.read(sp)!=0x409E5D or len(self.animation_entries)!=self.unit_inputs['count']:
                raise RuntimeError('current animation source release ownership/order')
            self.animation_file_release = {'pointer':pointer,'bytes':owned['bytes'],'caller_return_va':hex(self.read(sp)),
                'sha256_at_release':hashlib.sha256(bytes(uc.mem_read(pointer,owned['bytes']))).hexdigest()}
            owned['freed'] = True
            self.animation_boundaries.append({'kind':'source_file_release',**self.animation_file_release})
            self._stub_return(0,0)
            return
        return ExitEmulator._hook(self,uc,address,size,context)



def report():
    e = SchoolCurrentUnitsEmulator()
    if not e.run_planning('current_units_upstream')['school_data_prepared']:raise RuntimeError('actual school prefix missing')
    ranges = [(BASE,(SOURCE.stat().st_size+4095)&~4095),(TASK,0x120000),(GROUP_TASK,0x60000),(STACK,0x10000),
        (TACT,0x11A000),(SCRIPT_WORK,0x3000),(POOL,POOL_SIZE),(UHEAP,UHEAP_SIZE),(SCENE_POOL,SCENE_POOL_SIZE),
        (ASSET_POOL,ASSET_POOL_SIZE),(MAP_POOL,MAP_POOL_SIZE),(UNIT_POOL,UNIT_POOL_SIZE),(ANIM_POOL,ANIM_POOL_SIZE),
        (CONTROLLERS,CONTROLLER_BYTES),(CURRENT_ANIM,CURRENT_ANIM_BYTES)]
    checkpoint,cpu = [(a,bytes(e.uc.mem_read(a,n))) for a,n in ranges],e.uc.context_save();cases = []
    for name,commands in [('initial',()),('student9_waiting',[('student',9,-1)]),
        ('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1),('student',9,-1)]),
        ('teacher_only',[('student',3,-1),('student',4,-1),('student',9,-1)]),('teacher_waiting',[('teacher',101,-1)])]:
        for a,raw in checkpoint:e.uc.mem_write(a,raw)
        e.uc.context_restore(cpu);e.stop_reason = None;cases.append(e.resources(name,commands))
        print('Native current units '+name+': '+str(len(cases[-1]['current_units'])),flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
        'boundary':'All actual current-unit loops completed; stop before453540 enemies. GPU/scheduler declared; scene placement/VM unexecuted.',**AUTHORITY}


if __name__=='__main__':
    p = argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);args = p.parse_args()
    path = ROOT/args.out
    if path.exists():p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
