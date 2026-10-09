"""Current-school natural tactical resource buffers and native container traversal.

File/heap/CRT primitives are isolated; DirectX upload, audio and UnitCtrl remain
declared boundaries. Stop before the first tactical phase update, not a battle.
"""
import argparse
from copy import deepcopy
import hashlib
import struct
from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_tactical_startup_emulation import (
    SchoolTacticalStartupEmulator, TACT, TACT_SIZE, SCRIPT_WORK, FONT_API, cstring)
from tools.school_combat_records_emulation import UNITS, CHAR_BASE
from tools.school_adventure_handoff_emulation import GROUP_TASK
from tools.adv_return_state_emulation import CONTROLLER
from tools.tactics_exit_emulation import BASE, ROOT, SOURCE, SOURCE_SHA256, TASK, STACK, ExitEmulator, report_text
from tools.school_course_unlock_emulation import AUTHORITY

POOL, POOL_SIZE, FILE_API = 0xE400000, 0x800000, 0xE320000
RESOURCE_NAMES = ('data\\Tactics\\common.bin', 'data\\Tactics\\TactStart\\TactStart05.bin',
                  'data\\adv\\bin\\Gybc_00.bin', 'data\\Tactics\\Script\\t0005.bin')
RESOURCE_HASHES = ('110e230ffa1f3457ab7f5d7d4a31334e933c5edc90962855e921d86b84700d85',
 '96f4141566471c26e9e38c90b22e731f6e80e5da265f79bb371ffd30e916a2b4',
 '558b9530e36bb9970af3f0ea92df8031893132a4c85a94d9d879ecb192b256af',
 '44ca546b5ea90ec23a4bc7d8dffeac6547a44bfd035383c91983f7c13ae72a52')
FILE_IMPORTS = {0x592214: ('GetCurrentDirectoryA', 8), 0x5921EC: ('CreateFileA', 28),
                0x5921F0: ('GetFileSize', 8), 0x5921E8: ('ReadFile', 20),
                0x592270: ('CloseHandle', 4), 0x5922C4: ('lstrlenA', 4)}
NATIVE = ((0x4500B0,0x45010D),(0x42AE20,0x42AE6B),(0x42AC50,0x42ADCE),
 (0x416790,0x4167D2),(0x4167E0,0x416864),(0x41F090,0x41F0DC),
 (0x41F0E0,0x41F292),(0x41F4E0,0x41F59F),(0x41F830,0x41F887),
 (0x403620,0x4036C0),(0x41F930,0x41F9D5),(0x41F340,0x41F47F),
 (0x4214F0,0x421538),(0x4209F0,0x420A38),(0x420B50,0x420B98),
 (0x4048D0,0x404B0D),(0x420A40,0x420AB5),(0x404FB0,0x405129),
 (0x4548E0,0x454977),(0x454FA0,0x45505B))
NATIVE_CODE=frozenset(address for start,end in NATIVE for address in range(start,end))


def original_resource(name):
    if name not in RESOURCE_NAMES:
        raise ValueError('resource outside actual scene5 startup subset')
    path = ROOT/'CROSS HERMIT/CROSS HERMIT'/name.upper().replace('\\','/')
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=RESOURCE_HASHES[RESOURCE_NAMES.index(name)]:
        raise ValueError('original tactical resource identity differs')
    return raw, {'relative_path': name, 'local_file': path.relative_to(ROOT).as_posix(),
                 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


class SchoolTacticalResourcesEmulator(SchoolTacticalStartupEmulator):
    def __init__(self):
        super().__init__()
        self._function_ranges += NATIVE
        self.uc.mem_map(POOL, POOL_SIZE)
        self.uc.mem_map(FILE_API, 0x1000)
        self.loading = False
        self.reset_resources()

    def reset_resources(self):
        self.pool_cursor = POOL
        self.resource_allocations = []
        self.handles = {}
        self.file_events = []
        self.requests = []
        self.texture_entries = []
        self.gpu_events = []
        self.audio_boundaries = []
        self.active_texture = None

    def _write_hook(self, uc, access, address, size, value, context):
        if not getattr(self,'loading',False):
            return super()._write_hook(uc, access, address, size, value, context)
        if STACK<=address and address+size<=STACK+0x10000:return
        ranges = [(0,4),(STACK,STACK+0x10000),(TACT,TACT+TACT_SIZE),
                  (UNITS,UNITS+len(self.combat_records)*176),(0x7A4394,0x7A4398),
                  (0x7A0EBC,0x7A0FC0),(TASK+0x808E8,TASK+0x809EC),
                  (self.texture_table+0x5A*8,self.texture_table+0x5C*8),
                  (self.texture_table+0x14*8,self.texture_table+0x15*8)]
        ranges += [(a['pointer'],a['pointer']+a['bytes']) for a in self.resource_allocations
                   if not a.get('freed')]
        if not any(a<=address and address+size<=b for a,b in ranges):
            raise RuntimeError(f'resource finite guard: {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        if not STACK<=address<STACK+0x10000:
            self.writes.append((address,size,value & ((1<<(size*8))-1)))
            self.startup_writes.append((address,size))

    def primitive_write(self, address, data):
        self._write_hook(self.uc,0,address,len(data),0,None)
        self.uc.mem_write(address,data)

    def allocate(self, count, caller):
        # Only source file buffers or source texture entry arrays can allocate.
        if caller == 0x42AD54:
            if not self.handles or count != len(self.handles[max(self.handles)]['raw']):
                raise RuntimeError('file allocation differs from native GetFileSize')
            kind = 'file_buffer'
        elif caller == 0x41F142:
            if not self.requests or count != self.requests[-1]['entry_count']*0x54+4:
                raise RuntimeError('texture allocation differs from source container count')
            kind = 'texture_array'
        else:
            raise RuntimeError(f'undeclared resource allocation caller {caller:#x}')
        pointer = self.pool_cursor
        self.pool_cursor += (count+0xF)&~0xF
        if count<=0 or self.pool_cursor>POOL+POOL_SIZE:
            raise RuntimeError('resource heap bounds')
        self.resource_allocations.append({'pointer':pointer,'bytes':count,'kind':kind,
                                         'caller_return_va':hex(caller),'freed':False})
        return pointer

    def bind_resources(self):
        renderer = self.read(0x7A49FC)
        self.texture_table=renderer+0x844
        self.graphics_input = {'renderer':hex(renderer), 'device_pointer':hex(self.read(renderer+0xB210)),
            'embedded_texture_table':hex(self.texture_table),
            'previous_slots':{str(slot):bytes(self.uc.mem_read(self.texture_table+slot*8,8)).hex()
                              for slot in (0x14,0x5A,0x5B)},
            'declared_empty_slots':[0x14,0x5A,0x5B],
            'reason':'prior graphics constructors are boundaries; no old texture ownership is imported',
            'resource_prefix':cstring(self,TASK+0x80BF4)}
        for slot in (0x14,0x5A,0x5B):
            self.uc.mem_write(self.texture_table+slot*8,bytes(8))
        for i,(slot,_) in enumerate(FILE_IMPORTS.items()):
            self.write(slot,FILE_API+i*16)

    def _file_api(self, address, sp):
        index = (address-FILE_API)//16
        slot,(name,pop) = list(FILE_IMPORTS.items())[index]
        args = [self.read(sp+4+i*4) for i in range(pop//4)]
        result = 0
        if name=='GetCurrentDirectoryA':
            if args != [260,0x7A0EBC]: raise RuntimeError('current directory arguments')
            value = str(ROOT/'CROSS HERMIT/CROSS HERMIT').replace('/','\\').encode('ascii')
            self.primitive_write(args[1],value+b'\0'); result=len(value)
        elif name=='CreateFileA':
            relative = cstring(self,args[0])
            if args[1:] != [0x80000000,1,0,3,1,0]: raise RuntimeError('non-read-only file access')
            if relative != RESOURCE_NAMES[len(self.requests)-1]: raise RuntimeError('native file path differs')
            raw,identity = original_resource(relative)
            result = 0x700+len(self.requests)
            self.handles[result]={'raw':raw,'identity':identity}
        elif name=='GetFileSize':
            if args[0] not in self.handles or args[1]!=0: raise RuntimeError('file size handle')
            result=len(self.handles[args[0]]['raw'])
        elif name=='ReadFile':
            handle,target,count,written,overlapped=args
            if handle not in self.handles or overlapped!=0: raise RuntimeError('file read handle')
            raw=self.handles[handle]['raw']
            if count!=len(raw) or self.resource_allocations[-1]['pointer']!=target:
                raise RuntimeError('file read length/allocation')
            self.primitive_write(target,raw);self.primitive_write(written,struct.pack('<I',len(raw)))
            self.requests[-1].update({'buffer_pointer':target,'loaded_bytes':len(raw),
                'loaded_sha256':hashlib.sha256(bytes(self.uc.mem_read(target,count))).hexdigest()})
            result=1
        elif name=='CloseHandle':
            if args[0] not in self.handles: raise RuntimeError('unknown/double file close')
            del self.handles[args[0]];result=1
        elif name=='lstrlenA':
            if cstring(self,args[0])!='Dm-No-MakeTex':raise RuntimeError('undeclared string length')
            result=13
        self.file_events.append({'name':name,'import_va':hex(slot),'args':args,'result':result})
        self._stub_return(result,pop)

    def _hook(self, uc, address, size, context):
        if not getattr(self,'loading',False):
            return super()._hook(uc,address,size,context)
        if address in NATIVE_CODE and address not in (0x4500B0,0x41F340):
            self.visited.add(address);return
        sp=uc.reg_read(UC_X86_REG_ESP);receiver=uc.reg_read(UC_X86_REG_ECX)
        if address==0x4519C0:
            self.stop_reason='before_first_tactical_phase_update';uc.emu_stop();return
        if FILE_API<=address<FILE_API+len(FILE_IMPORTS)*16 and (address-FILE_API)%16==0:
            self._file_api(address,sp);return
        if address==0x4500B0:
            name=cstring(self,self.read(sp+4))
            if len(self.requests)>=4 or name!=RESOURCE_NAMES[len(self.requests)] or receiver!=TASK+0x80000:
                raise RuntimeError('natural resource order/receiver differs')
            raw,identity=original_resource(name)
            self.requests.append({'source':identity,'entry_count':self.read_container_count(raw),
                'caller_return_va':hex(self.read(sp))})
        if address==0x56D810:
            target,fmt=[self.read(sp+i) for i in (4,8)]
            format_text=cstring(self,fmt)
            arguments=[cstring(self,self.read(sp+12))]
            if format_text=='%s%s':
                if target!=TASK+0x808E8 or self.read(sp+12)!=TASK+0x80BF4:
                    raise RuntimeError('resource manager formatter receiver')
                arguments.append(cstring(self,self.read(sp+16)))
            elif format_text=='%s':
                if target!=0x7A0EBC:raise RuntimeError('file diagnostic formatter target')
            elif format_text in ('data\\Tactics\\TactStart\\%s','data\\Tactics\\Script\\%s'):
                if not STACK<=target<STACK+0xFF00:raise RuntimeError('scene formatter target')
            else:raise RuntimeError('undeclared resource format')
            value=(format_text % tuple(arguments)).encode('ascii')
            if len(value)>=260:raise RuntimeError('resource format overflow')
            self.primitive_write(target,value+b'\0');self._stub_return(len(value),0);return
        if address==0x428A40:
            self._stub_return(self.allocate(self.read(sp+4),self.read(sp)),0);return
        if address==0x428AD0:
            pointer=self.read(sp+4)
            match=[a for a in self.resource_allocations if a['pointer']==pointer and not a['freed']]
            if len(match)!=1 or match[0]['kind']!='file_buffer':raise RuntimeError('resource free ownership')
            match[0]['freed']=True;self._stub_return(0,0);return
        if address==0x56DDA0:
            target,stride,count,ctor,dtor=[self.read(sp+i) for i in (4,8,12,16,20)]
            allocation=self.resource_allocations[-1]
            if (target,stride,count,ctor,dtor)!=(allocation['pointer']+4,84,
                    self.requests[-1]['entry_count'],0x41F830,0x41F890):
                raise RuntimeError('undeclared texture vector constructor')
            # Suspend before iterating. Unicorn must not run nested emu_start
            # from its instruction hook. The driver executes original ctors.
            self.vector_pending=(target,stride,count,ctor)
            self.stop_reason='texture_vector_primitive';uc.emu_stop();return
        if address==0x56CEC0:
            target,byte,count=[self.read(sp+i) for i in (4,8,12)]
            if byte!=0 or count!=4 or not any(a['kind']=='texture_array' and
                    a['pointer']+4<=target<a['pointer']+a['bytes'] for a in self.resource_allocations):
                raise RuntimeError('texture memset bounds')
            self.primitive_write(target,bytes(count));self._stub_return(target,0);return
        if address==0x41F340:
            _,buffer,index,record,_,_=[self.read(sp+i) for i in (4,8,12,16,20,24)]
            request=self.requests[-1]
            if buffer!=request['buffer_pointer'] or index!=sum(e['resource']==len(self.requests)-1 for e in self.texture_entries):
                raise RuntimeError('native texture entry order')
            offset=self.read(buffer+8+index*4)
            end=self.read(buffer+8+(index+1)*4) if index+1<request['entry_count'] else request['loaded_bytes']
            self.active_texture={'resource':len(self.requests)-1,'index':index,'offset':offset,'bytes':end-offset,
                'header_hex':bytes(uc.mem_read(buffer+offset,min(16,end-offset))).hex(),
                'record_pointer':record+index*84}
            self.texture_entries.append(self.active_texture)
        if address==0x403BD0:
            entry=self.active_texture
            if entry is None or receiver!=entry['record_pointer']:raise RuntimeError('GPU entry receiver')
            width,height=[self.read(receiver+i,'H') for i in (0x38,0x3A)]
            self.gpu_events.append({'boundary':'texture_creation','entry':deepcopy(entry),
                'width':width,'height':height,'format':self.read(receiver+0x34)})
            self._stub_return(0,8);return
        if address in (0x404150,0x404690,0x4046F0):
            if self.active_texture is None or receiver!=self.active_texture['record_pointer']:
                raise RuntimeError('GPU upload receiver')
            self.gpu_events.append({'boundary':'pixel_upload','va':hex(address),
                                   'resource':self.active_texture['resource'],'index':self.active_texture['index']})
            self._stub_return(0,16 if address==0x404150 else 12);return
        if address==0x56E260:
            left,right,count=[self.read(sp+i) for i in (4,8,12)]
            if count!=13 or cstring(self,right)!='Dm-No-MakeTex':raise RuntimeError('marker comparison')
            a,b=bytes(uc.mem_read(left,count)),bytes(uc.mem_read(right,count))
            self._stub_return((a>b)-(a<b),0);return
        if address in (0x458FF0,0x459080):
            self.audio_boundaries.append({'va':hex(address),'caller_return_va':hex(self.read(sp))})
            self._stub_return(0,0);return
        if any(a<=address<b for a,b in NATIVE):return ExitEmulator._hook(self,uc,address,size,context)
        return super()._hook(uc,address,size,context)

    @staticmethod
    def read_container_count(raw):
        if len(raw)<12 or struct.unpack_from('<I',raw)[0]!=len(raw):
            raise ValueError('source container total length differs')
        count=struct.unpack_from('<I',raw,4)[0]
        if not 1<=count<=580 or 8+count*4>len(raw):raise ValueError('source container count')
        offsets=list(struct.unpack_from('<'+str(count)+'I',raw,8))
        if offsets[0]!=8+count*4 or any(a>=b for a,b in zip(offsets,offsets[1:]+[len(raw)])):
            raise ValueError('source container offsets')
        return count

    def run_resource_thread(self):
        self._thread(0x451670,TACT,timeout=40_000_000,count=6_000_000)
        iterations=0
        while self.stop_reason=='texture_vector_primitive':
            iterations+=1
            if iterations>3:raise RuntimeError('unexpected texture vector count')
            target,stride,count,ctor=self.vector_pending
            cpu=self.uc.context_save()
            saved_stack=bytes(self.uc.mem_read(STACK,0x10000))
            for i in range(count):
                self.call(ctor,receiver=target+i*stride)
            self.uc.mem_write(STACK,saved_stack)
            self.uc.context_restore(cpu)
            self._stub_return(0,20);self.stop_reason=None
            self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),0x3000000,
                             timeout=40_000_000,count=6_000_000)

    def resources(self,name,commands=()):
        self.loading=False;self.stage='departure_checkpoint'
        handoff=self.handoff(name,commands)
        self.startup_events=[];self.tactical_allocations=[];self.startup_writes=[]
        self.reset_resources();self.graphics_input=None;phases=[];task=None;script=None
        protected=[(CHAR_BASE,0x7F4488-CHAR_BASE),(0x7CF34C,45*0x124),(0x7A528E,4)]
        before=[bytes(self.uc.mem_read(a,n)) for a,n in protected]
        if handoff['ready']:
            self.write(0x5920A0,FONT_API)
            self.clear_trace('tactical_dispatch');self.call(0x49E2B0)
            phases.append({'phase':'dispatch16','coverage':self.coverage()})
            self.bind_resources();self.loading=True
            self.clear_trace('tactical_startup');self.stop_reason=None
            self.run_resource_thread()
            if self.stop_reason!='before_first_tactical_phase_update':raise RuntimeError('resource startup did not reach phase boundary')
            if self.handles or len(self.requests)!=4:raise RuntimeError('incomplete natural resource loading')
            task=self.task_snapshot()
            for entry in self.texture_entries:
                at=entry['record_pointer'];entry.update({'width':self.read(at+0x38,'H'),
                    'height':self.read(at+0x3A,'H'),'format':self.read(at+0x34),
                    'raw_record_hex':bytes(self.uc.mem_read(at,84)).hex()})
            request=self.requests[-1];pointer=self.read(TACT+100)
            if pointer!=request['buffer_pointer']:raise RuntimeError('script ownership pointer')
            script={'pointer':pointer,'source':request['source'],
                'sha256':hashlib.sha256(bytes(self.uc.mem_read(pointer,request['loaded_bytes']))).hexdigest()}
            phases.append({'phase':'natural_resource_startup','coverage':self.coverage()})
        if before!=[bytes(self.uc.mem_read(a,n)) for a,n in protected]:raise RuntimeError('resources changed persistent roles/MVP/calendar')
        self.loading=False
        return {'name':name,'ready':handoff['ready'],'commands':handoff['commands'],'handoff':handoff,
            'requests':deepcopy(self.requests),'file_events':deepcopy(self.file_events),
            'resource_allocations':deepcopy(self.resource_allocations),'texture_entries':deepcopy(self.texture_entries),
            'gpu_boundaries':deepcopy(self.gpu_events),'audio_boundaries':deepcopy(self.audio_boundaries),
            'graphics_input':self.graphics_input,'task_after':task,'scene_script':script,'phases':phases,
            'persistent_ranges_unchanged':True,'buffers_loaded':handoff['ready'],
            'gpu_textures_uploaded':False,'unitctrl_constructed':False,'battle_world_constructed':False,
            'stop_reason':self.stop_reason if handoff['ready'] else None,**AUTHORITY}


def report():
    e=SchoolTacticalResourcesEmulator();up=e.run_planning('tactical_resources_upstream')
    if not up['school_data_prepared']:raise RuntimeError('missing actual fifth-school prefix')
    ranges=[(BASE,(SOURCE.stat().st_size+0xFFF)&~0xFFF),(TASK,0x120000),(GROUP_TASK,0x60000),
        (STACK,0x10000),(TACT,0x11A000),(SCRIPT_WORK,0x3000),(POOL,POOL_SIZE)]
    checkpoint=[(a,bytes(e.uc.mem_read(a,n))) for a,n in ranges];cpu=e.uc.context_save();cases=[]
    for name,commands in [('initial',()),('student9_waiting',[('student',9,-1)]),
        ('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1),('student',9,-1)]),
        ('teacher_only',[('student',3,-1),('student',4,-1),('student',9,-1)]),('teacher_waiting',[('teacher',101,-1)])]:
        for a,data in checkpoint:e.uc.mem_write(a,data)
        e.uc.context_restore(cpu);e.stop_reason=None;cases.append(e.resources(name,commands))
        print('Native tactical resource loading '+name+': '+str(cases[-1]['buffers_loaded']),flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'cases':cases,
        'limitations':['Same actual school -> pending10 -> pending16 -> natural resource startup.',
            'Original path/file loader and texture container/header bodies execute with bounded external primitives.',
            'Declared empty graphics texture table, GPU creation/upload and audio are boundaries.',
            'UnitCtrl, map/enemy/event initial state and first tactical phase update remain unexecuted.'],**AUTHORITY}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);args=p.parse_args()
    path=ROOT/args.out
    if path.exists():p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
