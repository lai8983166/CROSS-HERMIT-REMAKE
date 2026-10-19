"""Continue the same live font CPU through original manager/queues/gamma admission."""
import argparse
import hashlib
import json
import struct
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_font_finish_emulation import FinishEmulator,OWNER,STACK,TOP,RETURN,unpack_large
from tools.school_font_finish_platform import FinishGDI,owned_run
from tools.school_font_finish import PHASES as FONT_PHASES,source_contract as font_source
from tools.school_font_glyph_upload import prefix
from tools.school_font_cache import COUNTER,HEAD,CACHE,dword,store
from tools.school_renderer_init_emulation import REGISTERS,buffer_evidence
from tools.school_device_init_verification import unpack
from tools.school_font_caller import *


class CallerEmulator(FinishEmulator):
    def __init__(self,bridge,platform,fill):
        self.caller_running=False
        super().__init__(bridge,platform,fill)
        self.caller_allocations=[]

    def _map_page(self,address):
        if any(p-4096<=address<p+n+4096 for p,n in ((HEADS,LAYER_BYTES),(ARENA,ARENA_BYTES))):
            raise RuntimeError('live interface mapping collides with audit ownership')
        return super()._map_page(address)

    def _write(self,uc,access,at,size,value,user):
        if not self.caller_running:return super()._write(uc,access,at,size,value,user)
        allowed=[('stack',STACK,STACK+65536)]
        if self.caller_phase=='bind':allowed.append(('manager',OWNER+0x1058,OWNER+0x1060))
        if self.caller_phase=='queues':
            allowed += [('manager',OWNER+0x1058,OWNER+0x10B8),('counter',COUNTER,COUNTER+4)]
            allowed += [(r['name'],r['pointer'],r['pointer']+r['bytes']) for r in self.caller_allocations]
        if self.caller_phase=='gamma':allowed.append(('gamma',OWNER+0xB408,OWNER+0xBA08))
        for name,a,b in allowed:
            if a<=at and at+size<=b:
                r=self.caller_writes.setdefault(name,dict(count=0,bytes=0));r['count']+=1;r['bytes']+=size
                return
        raise RuntimeError('font caller unowned original write '+hex(at))

    def _slot_read(self,uc,access,at,size,value,user):
        if not self.caller_running:return super()._slot_read(uc,access,at,size,value,user)
        allowed=[(BASE,BASE+len(self.image)),(OWNER,OWNER+0xC000),(STACK,STACK+65536)]
        allowed += [(p,p+4096) for p in self.foreign]
        allowed += [(r['pointer'],r['pointer']+r['bytes']) for r in self.caller_allocations]
        if not any(a<=at and at+size<=b for a,b in allowed):raise RuntimeError('font caller unowned original read '+hex(at))

    def _caller_allocate(self,sp):
        c=source_contract()['allocator'];ordinal=len(self.caller_allocations)
        args=[self.read(sp+4+i*4) for i in range(4)]
        if self.caller_phase!='queues' or ordinal>=2:raise RuntimeError('font caller undeclared CRT allocation')
        name,pointer,count=(('heads',HEADS,LAYER_BYTES),('arena',ARENA,ARENA_BYTES))[ordinal]
        if self.read(sp)!=int(c['return_va'],16) or args!=[count,c['block_type'],c['file'],c['line']]:
            raise RuntimeError('font caller exact original CRT allocation ABI')
        self.uc.mem_write(pointer,b'\xcd'*count)
        self.caller_allocations.append(dict(name=name,va='0x56e810',return_va='0x428a73',sp=sp,args=args,
            pointer=pointer,bytes=count,initial_byte=0xCD,initial_sha256=hashlib.sha256(b'\xcd'*count).hexdigest(),
            adapter='declared debug CRT allocation'))
        self.uc.reg_write(UC_X86_REG_EAX,pointer);self.uc.reg_write(UC_X86_REG_ESP,sp+4)
        self.uc.reg_write(UC_X86_REG_EIP,self.read(sp))

    def _code(self,uc,at,size,user):
        if not self.caller_running:return super()._code(uc,at,size,user)
        if at==self.caller_stop:self.boundary=at;uc.emu_stop();return
        sp=uc.reg_read(UC_X86_REG_ESP);ret=self.read(sp)
        if at==0x56E810:return self._caller_allocate(sp)
        if not any(a<=at and at+size<=b for a,b in RANGES.items()):raise RuntimeError('font caller undeclared original body '+hex(at))
        if self.caller_runs and self.caller_runs[-1]['va']==at:self.caller_runs[-1]['count']+=1
        else:self.caller_runs.append(dict(va=at,count=1))
        if at in ARGS:self.entries.append(dict(va=hex(at),return_va=hex(ret),sp=sp,
            receiver=uc.reg_read(REGISTERS['ECX']),args=[self.read(sp+4+i*4) for i in range(ARGS[at])]))
        if at in self.caller_rets:self.returns.append(dict(va=hex(at),return_va=hex(ret),sp=sp,eax=uc.reg_read(UC_X86_REG_EAX)))

    def resume_caller(self,phase,previous):
        start,stop=PHASES[phase]
        if self.uc.reg_read(UC_X86_REG_EIP)!=start:raise RuntimeError('font caller same pending CPU required')
        before_cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        if phase=='bind':
            for at,n in ((HEADS,LAYER_BYTES),(ARENA,ARENA_BYTES)):
                self.uc.mem_map(at-4096,n+8192);self.uc.mem_write(at-4096,b'\xa5'*(n+8192))
        self.entries,self.returns,self.caller_runs,self.caller_writes,self.boundary=[],[],[],{},None
        md=Cs(CS_ARCH_X86,CS_MODE_32)
        self.caller_rets={i.address for a,b in RANGES.items() for i in md.disasm(self.image[a-BASE:b-BASE],a) if i.mnemonic=='ret'}
        self.caller_phase,self.caller_stop,self.caller_running=phase,stop,True
        try:self.uc.emu_start(start,RETURN+1,timeout=30_000_000,count=1000000)
        finally:self.caller_running=False
        if self.boundary!=stop:raise RuntimeError('font caller original boundary not reached')
        owner=project_owner(unpack(previous['state']['owner']),phase,OWNER,self.objects['device']['pointer'])
        image=bytearray(self.constructed_image)
        store(image,COUNTER-BASE,dword(image,COUNTER-BASE)+3600+sum(r['bytes'] for r in self.caller_allocations));store(image,HEAD-BASE,CACHE)
        state=self.check(owner,bytes(image),0)
        for r in previous['retained_heaps']+[previous['second_heap']]:
            if bytes(self.uc.mem_read(r['pointer'],12288))!=unpack(r):raise RuntimeError('font caller complete prior heap retention')
        for r in previous['external_regions']:
            if bytes(self.uc.mem_read(r['base'],r['bytes']))!=unpack_large(r['buffer']):raise RuntimeError('font caller full pixel snapshot retention')
        queues=[]
        for name,p,n in (('heads',HEADS,LAYER_BYTES),('arena',ARENA,ARENA_BYTES)):
            raw=bytes(self.uc.mem_read(p-4096,n+8192));expected=b'\xa5'*4096+(bytes(n) if phase!='bind' else b'\xa5'*n)+b'\xa5'*4096
            if raw!=expected:raise RuntimeError('font caller full queue/guard mismatch '+name)
            queues.append(dict(name=name,pointer=p,guard_bytes=4096,payload_bytes=n,buffer=buffer_evidence(raw)))
        cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        pending=dict(va=hex(stop),sp=cpu['ESP'],first_instruction_executed=False)
        if phase=='gamma':pending.update(device=self.objects['device']['pointer'],vtable=self.objects['device']['vtable'],
            method_offset=72,args=[self.read(cpu['ESP']+i*4) for i in range(3)],target_read_executed=False)
        return dict(phase=phase,before_cpu=before_cpu,cpu=cpu,pending=pending,entries=self.entries,returns=self.returns,
            instruction_runs=self.caller_runs,native_writes=self.caller_writes,state=state,
            allocations=list(self.caller_allocations),queues=queues,
            retained_heaps=previous['retained_heaps'],second_heap=previous['second_heap'],heaps=previous['heaps'],slot_heap=previous['slot_heap'],
            external_regions=previous['external_regions'],retired_regions=previous['retired_regions'],
            manager_bound=True,queues_initialized=phase!='bind',gamma_table_generated=phase=='gamma',
            gamma_device_call_executed=False,full413450_returned=False,retained_VM_advanced=False,
            GPU_drawing_or_Present=False,saved_live_pointers_resumable=False)


def generate():
    cases=[]
    for fill,width,height in ((0xA5,640,480),(0xCC,1024,768)):
        def run(bridge):
            with FinishGDI() as platform:
                e=CallerEmulator(bridge,platform,fill);c=prefix(e,bridge,platform,fill)
                c['glyph_raster']=e.resume_glyphs(c['GDI_preparation']);c['pixel_upload']=e.resume_pixels(c['glyph_raster'])
                c['font_cleanup']=e.resume_state('cleanup',c['pixel_upload']);c['font_vertex']=e.resume_state('vertex',c['font_cleanup']);c['font_states']=e.resume_state('states',c['font_vertex'])
                c['second_loop']=e.resume_second('loop',c['font_states']);c['second_constructor']=e.resume_second('constructor',c['second_loop']);c['second_atlas']=e.resume_second('atlas',c['second_constructor'])
                c['second_texture']=e.resume_resource('texture',c['second_atlas']);c['second_GDI']=e.resume_resource('gdi',c['second_texture'])
                c['DIB_retirement']=e.retire_first_DIB(c['second_GDI'],c['font_cleanup']);c['second_raster']=e.second_raster(c['DIB_retirement']);c['second_upload']=e.second_upload(c['second_raster'])
                previous=c['second_upload']
                for phase in FONT_PHASES:c['finish_'+phase]=e.finish(phase,previous);previous=c['finish_'+phase]
                for phase in PHASES:c['caller_'+phase]=e.resume_caller(phase,previous);previous=c['caller_'+phase]
            c.update(platform_trace=platform.trace,platform_cleanup=platform.cleanup);return c
        r=owned_run(run,width,height);c=r['value'];c.update(device_trace=r['trace'],device_cleanup=r['cleanup'],refused_address_collisions=r['refused_address_collisions']);cases.append(c)
        print(hex(fill)+': original caller bind/queues/gamma admission verified',flush=True)
    font=dict(schema_version=1,phase='full_return',source_contract=font_source(),cases=cases,
        device_build=json.loads((ROOT/'analysis/school-font-finish-device-v1-20261019.json').read_text())['build'],
        platform_build=json.loads((ROOT/'analysis/school-font-finish-gdi-v1-20261019.json').read_text())['build'],
        one_continuous_trajectory_per_case=True,explicit_empty_cache_experiment=True,CRT_adapter_executed=True,
        original_IAT_changed=False,game_helpers_stubbed=False,retained_VM_advanced=False,GPU_drawing_or_Present=False,
        full_outer_frame=False,live_handles_resumable_after_cleanup=False)
    return dict(schema_version=1,source_contract=source_contract(),font_report=font,
        one_continuous_trajectory_per_case=True,owned_helpers_unchanged=True,retained_VM_advanced=False,
        gamma_device_call_executed=False,full413450_returned=False,GPU_drawing_or_Present=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable caller trajectory required')
    path.write_text(json.dumps(generate(),indent=2)+chr(10),encoding='utf8',newline=chr(10))
