"""Continuous original startup through real void gamma and natural ret20."""
import argparse
import hashlib
import json
import struct
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_font_caller_emulation import CallerEmulator,OWNER,STACK,TOP,RETURN,unpack_large
from tools.school_font_caller import PHASES as CALLER_PHASES,HEADS,ARENA,LAYER_BYTES,ARENA_BYTES
from tools.school_font_finish import PHASES as FONT_PHASES
from tools.school_startup_return_platform import FinishGDI,owned_run
from tools.school_font_glyph_upload import prefix
from tools.school_font_cache import COUNTER,HEAD,CACHE,dword,store
from tools.school_renderer_init_emulation import REGISTERS,buffer_evidence
from tools.school_device_init_verification import unpack
from tools.school_startup_return import *


class ReturnEmulator(CallerEmulator):
    def __init__(self,bridge,platform,fill):
        self.return_running=False
        super().__init__(bridge,platform,fill)

    def _write(self,uc,access,at,size,value,user):
        if not self.return_running:return super()._write(uc,access,at,size,value,user)
        if not STACK<=at or at+size>STACK+65536:raise RuntimeError('startup return unowned original write '+hex(at))

    def _slot_read(self,uc,access,at,size,value,user):
        if not self.return_running:return super()._slot_read(uc,access,at,size,value,user)
        allowed=[(BASE,BASE+len(self.image)),(OWNER,OWNER+0xC000),(STACK,STACK+65536)]
        allowed += [(p,p+4096) for p in self.foreign]
        if not any(a<=at and at+size<=b for a,b in allowed):raise RuntimeError('startup return unowned original read '+hex(at))

    def retention(self,previous):
        image=bytearray(self.constructed_image)
        store(image,COUNTER-BASE,dword(image,COUNTER-BASE)+3600+LAYER_BYTES+ARENA_BYTES);store(image,HEAD-BASE,CACHE)
        state=self.check(unpack(previous['state']['owner']),bytes(image),0)
        for r in previous['retained_heaps']+[previous['second_heap']]:
            if bytes(self.uc.mem_read(r['pointer'],12288))!=unpack(r):raise RuntimeError('startup return full prior heap retention')
        for r in previous['external_regions']:
            if bytes(self.uc.mem_read(r['base'],r['bytes']))!=unpack_large(r['buffer']):raise RuntimeError('startup return full pixel retention')
        for r in previous['queues']:
            p,n=r['pointer'],r['payload_bytes'];raw=bytes(self.uc.mem_read(p-4096,n+8192))
            if raw!=b'\xa5'*4096+bytes(n)+b'\xa5'*4096:raise RuntimeError('startup return full queue/guard retention')
        return state

    def prepare_gamma(self,previous):
        cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        if cpu!=previous['cpu'] or cpu['EIP']!=0x416CFA:raise RuntimeError('startup return natural gamma CPU required')
        stack=hashlib.sha256(bytes(self.uc.mem_read(STACK,65536))).hexdigest()
        old=self.objects['device'];request=dict(pointer=old['pointer']);result=self.bridge.request('gamma_prepare',**request)
        identity=result['device']
        if identity['pointer']!=old['pointer'] or identity['vtable']!=old['vtable'] or set(identity['methods'])!={'72'}:
            raise RuntimeError('startup return late actual gamma method identity')
        # Keep the original create_device result immutable; expose only this late mapping.
        self.objects['device']=dict(pointer=old['pointer'],vtable=old['vtable'],methods=dict(old['methods'],**identity['methods']))
        for slot,target in identity['methods'].items():
            self._foreign_write(identity['vtable']+int(slot),struct.pack('<I',target));self._foreign_write(target,b'\xc3')
        after={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        after_stack=hashlib.sha256(bytes(self.uc.mem_read(STACK,65536))).hexdigest()
        if after!=cpu or stack!=after_stack:raise RuntimeError('startup return method inspection changed CPU/stack')
        row={k:previous[k] for k in ('heaps','slot_heap','retained_heaps','second_heap','external_regions','retired_regions','queues','allocations')}
        row.update(before_cpu=cpu,cpu=after,pending=previous['pending'],state=self.retention(previous),
            inspection=dict(op='gamma_prepare',request=request,result=result),stack_before_sha256=stack,stack_after_sha256=after_stack,
            original_instructions_executed=0,original_gamma_call_executed=False)
        return row

    def _gamma_api(self,at,sp,ret):
        args=[self.read(sp+4+i*4) for i in range(3)];pointer=self.objects['device']['pointer']
        if ret!=0x416CFD or args!=[pointer,1,OWNER+0xB408] or self.return_calls:raise RuntimeError('startup return original void gamma ABI')
        request=dict(pointer=pointer,flags=1,hex=bytes(self.uc.mem_read(args[2],1536)).hex())
        result=self.bridge.request('gamma_set',**request)
        if result['native_return_type']!='void' or result['eax_is_status'] is not False:raise RuntimeError('startup return void API cannot supply HRESULT')
        self.return_calls.append(dict(op='gamma_set',va=hex(at),return_va=hex(ret),sp=sp,args=args,
            request=request,result=result,live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX,result['eax_bits_observed']);self.uc.reg_write(UC_X86_REG_ESP,sp+16);self.uc.reg_write(UC_X86_REG_EIP,ret)

    def _code(self,uc,at,size,user):
        if not self.return_running:return super()._code(uc,at,size,user)
        if at==self.return_stop:self.boundary=at;uc.emu_stop();return
        sp=uc.reg_read(UC_X86_REG_ESP);ret=self.read(sp)
        if self.return_phase=='gamma' and at==self.objects['device']['methods']['72']:return self._gamma_api(at,sp,ret)
        if not any(a<=at and at+size<=b for a,b in RANGES.items()):raise RuntimeError('startup return undeclared original body '+hex(at))
        self.return_trace.append(at)
        if at in (0x56CE82,0x416D14,0x413558):self.returns.append(dict(va=hex(at),return_va=hex(ret),sp=sp,eax=uc.reg_read(UC_X86_REG_EAX)))

    def resume_return(self,phase,previous):
        start,stop=PHASES[phase]
        before={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        if before!=previous['cpu'] or before['EIP']!=start:raise RuntimeError('startup return same original CPU required')
        self.return_calls,self.return_trace,self.returns,self.boundary=[],[],[],None
        self.return_phase,self.return_stop,self.return_running=phase,stop,True
        try:self.uc.emu_start(start,RETURN+1,timeout=10_000_000,count=1000)
        finally:self.return_running=False
        if self.boundary!=stop:raise RuntimeError('startup return natural boundary not reached')
        cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        row={k:previous[k] for k in ('heaps','slot_heap','retained_heaps','second_heap','external_regions','retired_regions','queues','allocations')}
        row.update(phase=phase,before_cpu=before,cpu=cpu,pending=dict(va=hex(stop),sp=cpu['ESP'],first_instruction_executed=False),
            api_calls=self.return_calls,instruction_trace=self.return_trace,returns=self.returns,state=self.retention(previous),
            original_gamma_call_executed=True,full416CC0_returned=True,full413450_returned=phase=='return',
            original_font_destructor_chain_executed=False,upstream_caller_executed=False,retained_VM_advanced=False,
            GPU_drawing_or_Present=False,saved_live_pointers_resumable=False)
        return row


def generate():
    cases=[]
    for fill,width,height in ((0xA5,640,480),(0xCC,1024,768)):
        def run(bridge):
            with FinishGDI() as platform:
                e=ReturnEmulator(bridge,platform,fill);c=prefix(e,bridge,platform,fill)
                c['glyph_raster']=e.resume_glyphs(c['GDI_preparation']);c['pixel_upload']=e.resume_pixels(c['glyph_raster'])
                c['font_cleanup']=e.resume_state('cleanup',c['pixel_upload']);c['font_vertex']=e.resume_state('vertex',c['font_cleanup']);c['font_states']=e.resume_state('states',c['font_vertex'])
                c['second_loop']=e.resume_second('loop',c['font_states']);c['second_constructor']=e.resume_second('constructor',c['second_loop']);c['second_atlas']=e.resume_second('atlas',c['second_constructor'])
                c['second_texture']=e.resume_resource('texture',c['second_atlas']);c['second_GDI']=e.resume_resource('gdi',c['second_texture'])
                c['DIB_retirement']=e.retire_first_DIB(c['second_GDI'],c['font_cleanup']);c['second_raster']=e.second_raster(c['DIB_retirement']);c['second_upload']=e.second_upload(c['second_raster'])
                previous=c['second_upload']
                for p in FONT_PHASES:c['finish_'+p]=e.finish(p,previous);previous=c['finish_'+p]
                for p in CALLER_PHASES:c['caller_'+p]=e.resume_caller(p,previous);previous=c['caller_'+p]
                c['gamma_admission']=e.prepare_gamma(previous);previous=c['gamma_admission']
                for p in PHASES:c['startup_'+p]=e.resume_return(p,previous);previous=c['startup_'+p]
            c.update(platform_trace=platform.trace,platform_cleanup=platform.cleanup);return c
        r=owned_run(run,width,height);c=r['value'];c.update(device_trace=r['trace'],device_cleanup=r['cleanup'],refused_address_collisions=r['refused_address_collisions']);cases.append(c)
        print(hex(fill)+': actual void gamma and original413450 success return verified',flush=True)
    return dict(schema_version=1,source_contract=source_contract(),cases=cases,
        device_build=json.loads((ROOT/'analysis/school-startup-return-device-v1-20261019.json').read_text())['build'],
        platform_build=json.loads((ROOT/'analysis/school-font-finish-gdi-v1-20261019.json').read_text())['build'],
        one_continuous_trajectory_per_case=True,explicit_empty_cache_experiment=True,CRT_adapter_executed=True,
        original_IAT_changed=False,game_helpers_stubbed=False,full413450_returned=True,
        retained_VM_advanced=False,GPU_drawing_or_Present=False,full_outer_frame=False,live_handles_resumable_after_cleanup=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable complete startup return trajectory required')
    path.write_text(json.dumps(generate(),indent=2)+chr(10),encoding='utf8',newline=chr(10))
