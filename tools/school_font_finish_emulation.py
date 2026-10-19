"""One continuous two-font trajectory through original415F50 success return."""
import argparse
import json
import struct
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_font_second_glyph_emulation import SecondGlyphEmulator,OWNER,STACK,TOP,RETURN,unpack_large
from tools.school_font_finish_platform import FinishGDI,owned_run
from tools.school_font_glyph_upload import prefix
from tools.school_font_finish import *
from tools.school_font_cache import COUNTER,HEAD,CACHE,dword,store
from tools.school_renderer_init_emulation import REGISTERS,buffer_evidence
from tools.school_device_init_verification import unpack


class FinishEmulator(SecondGlyphEmulator):
    def __init__(self,bridge,platform,fill):
        self.finish_running=False
        super().__init__(bridge,platform,fill)

    def _write(self,uc,access,at,size,value,user):
        if not self.finish_running:return super()._write(uc,access,at,size,value,user)
        if STACK<=at and at+size<=STACK+65536:return
        if self.finish_phase=='return' and at==0 and size==4 and value==0:return
        raise RuntimeError('font finish unowned original write '+hex(at))

    def _slot_read(self,uc,access,at,size,value,user):
        if not self.finish_running:return super()._slot_read(uc,access,at,size,value,user)
        allowed=[(BASE,BASE+len(self.image)),(OWNER,OWNER+0xC000),(STACK,STACK+65536),(SECOND,SECOND+SIZE)]
        allowed += [(p,p+4096) for p in self.foreign]
        if not any(a<=at and at+size<=b for a,b in allowed):raise RuntimeError('font finish unowned original read '+hex(at))

    def _put(self,at,raw):
        if self.finish_running and self.finish_phase in ('vertex','states') and at in (SECOND+0x60,SECOND+0x670,SECOND+0x674) and len(raw)==4:
            self.uc.mem_write(at,raw);return
        return super()._put(at,raw)

    def _finish_delete(self,at,sp,ret):
        slot,name,old_op=IMPORTS[ret];arg=self.read(sp+4)
        expected={'font_delete_bitmap':self.second_bitmap,'font_delete_dc':self.second_dc,'font_delete_font':self.second_font}[old_op]
        if at!=self.read(slot) or arg!=expected:raise RuntimeError('font finish original second GDI delete identity/ABI')
        op='second_'+old_op;request=dict(pointer=arg);result=self.owner_bridge.request(op,**request)
        self.finish_calls.append(dict(op=op,name=name,slot=hex(slot),va=hex(at),return_va=hex(ret),sp=sp,args=[arg],request=request,result=result,live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX,result['result']);self.uc.reg_write(UC_X86_REG_ESP,sp+8);self.uc.reg_write(UC_X86_REG_EIP,ret)

    def _finish_device(self,at,sp,ret,spec):
        method=spec['method'];device=self.objects['device'];pointer=device['pointer']
        count=6 if method=='vb' else 1 if method=='begin' else 2 if method=='end' else 4 if method=='stage' else 3
        args=[self.read(sp+4+i*4) for i in range(count)]
        if at!=device['methods'][str(spec['offset'])] or args[0]!=pointer:raise RuntimeError('font finish actual second device identity')
        if method=='vb':
            expected=[pointer,8400,520,0,0,SECOND+0x60];request=dict(pointer=pointer,args=[8400,520,0,0]);op='second_font_vb'
        elif method=='end':
            output=SECOND+(0x670 if ret==0x401CE0 else 0x674);expected=[pointer,output];request=dict(pointer=pointer,method=method,args=[]);op='second_font_state'
        else:
            values=spec['immediate_args']+([self.objects['second_atlas_texture']['pointer']] if method=='texture' else [])
            expected=[pointer,*values];request=dict(pointer=pointer,method=method,args=values);op='second_font_state'
        if args!=expected:raise RuntimeError('font finish exact original state arguments '+method)
        result=self.bridge.request(op,**request)
        if method=='vb':self._identity('second_font_vertex',result['buffer']);self._put(SECOND+0x60,struct.pack('<I',result['buffer']['pointer']))
        if method=='end':self._put(expected[-1],struct.pack('<I',result['token']))
        self.finish_calls.append(dict(op=op,method=method,va=hex(at),return_va=hex(ret),sp=sp,args=args,request=request,result=result,live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX,result['hr']);self.uc.reg_write(UC_X86_REG_ESP,sp+4+count*4);self.uc.reg_write(UC_X86_REG_EIP,ret)

    def _code(self,uc,at,size,user):
        if not self.finish_running:return super()._code(uc,at,size,user)
        if at==self.finish_stop:self.boundary=at;uc.emu_stop();return
        sp=uc.reg_read(UC_X86_REG_ESP);ret=self.read(sp)
        if ret in IMPORTS and at==self.read(IMPORTS[ret][0]):return self._finish_delete(at,sp,ret)
        if ret in self.finish_specs and at==self.objects['device']['methods'].get(str(self.finish_specs[ret]['offset'])):
            return self._finish_device(at,sp,ret,self.finish_specs[ret])
        if not any(a<=at and at+size<=b for a,b in RANGES.items()):raise RuntimeError('font finish undeclared original body '+hex(at))
        self.visited.add(at);self.instruction_trace.append(at)
        if at==0x401810:self.entries.append(dict(va=hex(at),return_va=hex(ret),sp=sp,receiver=uc.reg_read(REGISTERS['ECX']),args=[]))
        if at in self.finish_rets:self.returns.append(dict(va=hex(at),return_va=hex(ret),sp=sp,eax=uc.reg_read(UC_X86_REG_EAX)))

    def finish(self,phase,previous):
        start,stop=PHASES[phase]
        if self.uc.reg_read(UC_X86_REG_EIP)!=start:raise RuntimeError('font finish same pending CPU required')
        before_cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        self.finish_calls,self.entries,self.returns,self.visited,self.instruction_trace,self.boundary=[],[],[],set(),[],None
        self.finish_specs={int(r['return_va'],16):r for r in source_contract()['shared_state_source']['calls']}
        md=Cs(CS_ARCH_X86,CS_MODE_32)
        self.finish_rets={i.address for a,b in RANGES.items() for i in md.disasm(self.image[a-BASE:b-BASE],a) if i.mnemonic=='ret'}
        self.finish_phase,self.finish_stop,self.finish_running=phase,stop,True
        try:self.uc.emu_start(start,RETURN+1,timeout=20_000_000,count=200000)
        finally:self.finish_running=False
        if self.boundary!=stop:raise RuntimeError('font finish original boundary not reached')
        image=bytearray(self.constructed_image);store(image,COUNTER-BASE,dword(image,COUNTER-BASE)+3600);store(image,HEAD-BASE,CACHE)
        state=self.check(unpack(previous['state']['owner']),bytes(image),0 if phase=='return' else TOP-108)
        for r in previous['retained_heaps']:
            if bytes(self.uc.mem_read(r['pointer'],12288))!=unpack(r):raise RuntimeError('font finish changed prior complete heap')
        for r in previous['external_regions']:
            if bytes(self.uc.mem_read(r['base'],r['bytes']))!=unpack_large(r['buffer']):raise RuntimeError('font finish changed full pixel snapshot')
        value=unpack(previous['second_heap'])[4096:4096+SIZE]
        if phase in ('vertex','states'):
            tokens=(self.read(SECOND+0x670),self.read(SECOND+0x674)) if phase=='states' else (0,0)
            value=project(value,self.objects['second_font_vertex']['pointer'],tokens)
        expected=bytearray(b'\xa5'*12288);expected[4096:4096+SIZE]=value;actual=bytes(self.uc.mem_read(SECOND-4096,12288))
        if actual!=expected:raise RuntimeError('font finish complete second object/guard mismatch')
        cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        return dict(phase=phase,before_cpu=before_cpu,api_calls=self.finish_calls,entries=self.entries,returns=self.returns,
            visited=sorted(self.visited),instruction_trace=self.instruction_trace,state=state,heaps=previous['heaps'],slot_heap=previous['slot_heap'],
            retained_heaps=previous['retained_heaps'],second_heap=dict(pointer=SECOND-4096,**buffer_evidence(actual)),
            external_regions=previous['external_regions'],external_regions_are_snapshots_after_native_GDI_release=True,
            retired_regions=previous['retired_regions'],cpu=cpu,pending=dict(va=hex(stop),sp=cpu['ESP'],first_instruction_executed=False),
            loop_locals=dict(index=self.read(TOP-120),status=self.read(TOP-116)),
            original_second_GDI_cleanup_executed=True,full_second4010D0_returned=True,second_vertex_buffer_created=phase!='cleanup',
            second_state_blocks_created=phase in ('states','return'),second_full401810_returned=phase in ('states','return'),
            both_additional_fonts_completed=phase in ('states','return'),full415F50_returned=phase=='return',
            first_font_resources_retained=True,parent_caller_instruction_executed=False,manager_bound=False,
            native_font_destructor_chain_executed=False,GPU_drawing_or_Present=False,retained_VM_advanced=False)


def generate():
    cases=[]
    for fill,width,height in ((0xA5,640,480),(0xCC,1024,768)):
        def run(bridge):
            with FinishGDI() as platform:
                e=FinishEmulator(bridge,platform,fill);c=prefix(e,bridge,platform,fill)
                c['glyph_raster']=e.resume_glyphs(c['GDI_preparation']);c['pixel_upload']=e.resume_pixels(c['glyph_raster'])
                c['font_cleanup']=e.resume_state('cleanup',c['pixel_upload']);c['font_vertex']=e.resume_state('vertex',c['font_cleanup']);c['font_states']=e.resume_state('states',c['font_vertex'])
                c['second_loop']=e.resume_second('loop',c['font_states']);c['second_constructor']=e.resume_second('constructor',c['second_loop']);c['second_atlas']=e.resume_second('atlas',c['second_constructor'])
                c['second_texture']=e.resume_resource('texture',c['second_atlas']);c['second_GDI']=e.resume_resource('gdi',c['second_texture'])
                c['DIB_retirement']=e.retire_first_DIB(c['second_GDI'],c['font_cleanup']);c['second_raster']=e.second_raster(c['DIB_retirement']);c['second_upload']=e.second_upload(c['second_raster'])
                previous=c['second_upload']
                for phase in PHASES:
                    c['finish_'+phase]=e.finish(phase,previous);previous=c['finish_'+phase]
            c.update(platform_trace=platform.trace,platform_cleanup=platform.cleanup);return c
        r=owned_run(run,width,height);c=r['value'];c.update(device_trace=r['trace'],device_cleanup=r['cleanup'],refused_address_collisions=r['refused_address_collisions']);cases.append(c)
        print(hex(fill)+': original second cleanup/VB/states/full415F50 return verified',flush=True)
    return dict(schema_version=1,phase='full_return',source_contract=source_contract(),cases=cases,
        device_build=json.loads((ROOT/'analysis/school-font-finish-device-v1-20261019.json').read_text())['build'],
        platform_build=json.loads((ROOT/'analysis/school-font-finish-gdi-v1-20261019.json').read_text())['build'],
        one_continuous_trajectory_per_case=True,explicit_empty_cache_experiment=True,CRT_adapter_executed=True,original_IAT_changed=False,game_helpers_stubbed=False,
        retained_VM_advanced=False,GPU_drawing_or_Present=False,full_outer_frame=False,live_handles_resumable_after_cleanup=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable font finish trajectory required')
    path.write_text(json.dumps(generate(),indent=2)+chr(10),encoding='utf8',newline=chr(10))
