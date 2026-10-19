"""Original atlas cleanup, vertex buffer and complete first-font state-block return."""
import argparse
import json
import struct
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_font_glyph_upload import PixelEmulator,prefix,OWNER,STACK,TOP,RETURN
from tools.school_font_glyph_device import owned_run as pixel_owned_run
from tools.school_font_state_gdi import StateGDI
from tools.school_font_state import *
from tools.school_renderer_init_emulation import REGISTERS,buffer_evidence
from tools.school_device_init_verification import unpack


class StateEmulator(PixelEmulator):
    def __init__(self,bridge,platform,fill):
        self.state_running=False
        super().__init__(bridge,platform,fill)

    def _write(self,uc,access,at,size,value,user):
        if not self.state_running:return super()._write(uc,access,at,size,value,user)
        if STACK<=at and at+size<=STACK+65536:return
        if self.state_phase!='cleanup' and at in (SLOT+0x60,SLOT+0x670,SLOT+0x674) and size==4:return
        raise RuntimeError('font state unowned native write '+hex(at))

    def _slot_read(self,uc,access,at,size,value,user):
        if not self.state_running:return super()._slot_read(uc,access,at,size,value,user)
        allowed=[(STACK,STACK+65536),(SLOT,SLOT+SIZE),(OWNER,OWNER+0xC000),(BASE,BASE+len(self.image))]
        allowed += [(p,p+4096) for p in self.foreign]
        if not any(a<=at and at+size<=b for a,b in allowed):raise RuntimeError('font state unowned native read '+hex(at))

    def _put(self,at,raw):
        if self.state_running and at in (SLOT+0x60,SLOT+0x670,SLOT+0x674) and len(raw)==4:self.uc.mem_write(at,raw);return
        return super()._put(at,raw)

    def _native_delete(self,at,sp,ret):
        slot,name,op=IMPORTS[ret];arg=self.read(sp+4)
        expected={'font_delete_bitmap':self.atlas_bitmap,'font_delete_dc':self.atlas_dc,'font_delete_font':self.atlas_font}[op]
        if at!=self.read(slot) or arg!=expected:raise RuntimeError('font original GDI deletion target/ABI')
        request=dict(pointer=arg);result=self.owner_bridge.request(op,**request)
        self.state_calls.append(dict(op=op,name=name,slot=hex(slot),va=hex(at),return_va=hex(ret),sp=sp,args=[arg],request=request,result=result,live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX,result['result']);self.uc.reg_write(UC_X86_REG_ESP,sp+8);self.uc.reg_write(UC_X86_REG_EIP,ret)

    def _device_state(self,at,sp,ret,spec):
        method=spec['method'];device=self.objects['device'];pointer=device['pointer']
        count=6 if method=='vb' else 1 if method=='begin' else 2 if method=='end' else 4 if method=='stage' else 3
        args=[self.read(sp+4+i*4) for i in range(count)]
        if at!=device['methods'][str(spec['offset'])] or args[0]!=pointer:raise RuntimeError('font actual state device identity')
        if method=='vb':
            expected=[pointer,8400,520,0,0,SLOT+0x60];request=dict(pointer=pointer,args=[8400,520,0,0]);op='font_vb'
        elif method=='end':
            output=SLOT+(0x670 if ret==0x401CE0 else 0x674);expected=[pointer,output];request=dict(pointer=pointer,method=method,args=[]);op='font_state'
        else:
            values=spec['immediate_args']+([self.objects['atlas_texture']['pointer']] if method=='texture' else [])
            expected=[pointer,*values];request=dict(pointer=pointer,method=method,args=values);op='font_state'
        if args!=expected:raise RuntimeError('font source state arguments '+method)
        result=self.bridge.request(op,**request)
        if method=='vb':self._identity('font_vertex',result['buffer']);self._put(SLOT+0x60,struct.pack('<I',result['buffer']['pointer']))
        if method=='end':self._put(expected[-1],struct.pack('<I',result['token']))
        self.state_calls.append(dict(op=op,method=method,va=hex(at),return_va=hex(ret),sp=sp,args=args,request=request,result=result,live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX,result['hr']);self.uc.reg_write(UC_X86_REG_ESP,sp+4+4*count);self.uc.reg_write(UC_X86_REG_EIP,ret)

    def _code(self,uc,at,size,user):
        if not self.state_running:return super()._code(uc,at,size,user)
        if at==self.state_stop:self.boundary=at;uc.emu_stop();return
        sp=uc.reg_read(UC_X86_REG_ESP);ret=self.read(sp)
        if ret in IMPORTS and at==self.read(IMPORTS[ret][0]):return self._native_delete(at,sp,ret)
        if ret in self.device_specs and at==self.objects['device']['methods'].get(str(self.device_specs[ret]['offset'])):
            return self._device_state(at,sp,ret,self.device_specs[ret])
        if not any(a<=at and at+size<=b for a,b in RANGES.items()):raise RuntimeError('font state undeclared original body '+hex(at))
        self.visited.add(at)
        if at==0x401810:self.entries.append(dict(va=hex(at),return_va=hex(ret),sp=sp,receiver=uc.reg_read(REGISTERS['ECX']),args=[]))
        if at in self.state_rets:self.returns.append(dict(va=hex(at),return_va=hex(ret),sp=sp,eax=uc.reg_read(UC_X86_REG_EAX)))

    def resume_state(self,phase,previous):
        start,stop={'cleanup':(0x4017B6,0x401810),'vertex':(0x401810,0x40186E),'states':(0x40186E,0x416101)}[phase]
        if self.uc.reg_read(UC_X86_REG_EIP)!=start:raise RuntimeError('font state same pending CPU required')
        before_cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        if phase=='cleanup':
            for slot,*_ in IMPORTS.values():self._foreign_write(self.read(slot),b'\xc3')
        self.state_calls,self.entries,self.returns,self.visited,self.boundary=[],[],[],set(),None
        self.state_phase,self.state_stop=phase,stop;self.device_specs={int(r['return_va'],16):r for r in source_contract()['calls']}
        md=Cs(CS_ARCH_X86,CS_MODE_32);self.state_rets={i.address for a,b in RANGES.items() for i in md.disasm(self.image[a-BASE:b-BASE],a) if i.mnemonic=='ret'}
        self.state_running=True
        try:self.uc.emu_start(start,RETURN+1,timeout=20_000_000,count=200000)
        finally:self.state_running=False
        if self.boundary!=stop:raise RuntimeError('font state native boundary not reached')
        state=self.check(unpack(previous['state']['owner']),bytes(self.uc.mem_read(BASE,len(self.image))),TOP-108)
        if state['image_sha256']!=previous['state']['image_sha256']:raise RuntimeError('font state original image changed')
        before=unpack(previous['slot_heap'])[4096:4096+SIZE]
        value=before if phase=='cleanup' else project(before,self.objects['font_vertex']['pointer'],
            (self.read(SLOT+0x670),self.read(SLOT+0x674)) if phase=='states' else (0,0))
        expected=bytearray(b'\xa5'*12288);expected[4096:4096+SIZE]=value;actual=bytes(self.uc.mem_read(SLOT-4096,12288))
        if actual!=expected:raise RuntimeError('font state complete source object/guard mismatch')
        for row in previous['heaps']:
            if bytes(self.uc.mem_read(row['pointer'],12288))!=unpack(row):raise RuntimeError('font state prior heap changed')
        for r in previous['external_regions']:
            if bytes(self.uc.mem_read(r['base'],r['bytes']))!=unpack_large(r['buffer']):raise RuntimeError('font state prior pixel snapshot changed')
        cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        return dict(phase=phase,before_cpu=before_cpu,entries=self.entries,returns=self.returns,api_calls=self.state_calls,
            visited=sorted(self.visited),state=state,heaps=previous['heaps'],slot_heap=dict(pointer=SLOT-4096,**buffer_evidence(actual)),
            external_regions=previous['external_regions'],external_regions_are_retained_snapshots=True,cpu=cpu,
            pending=dict(va=hex(stop),sp=cpu['ESP'],first_instruction_executed=False),
            original_GDI_cleanup_executed=True,full4010D0_returned=True,vertex_buffer_created=phase!='cleanup',
            state_blocks_created=phase=='states',full401810_returned=phase=='states',first_additional_font_completed=phase=='states',
            second_additional_font_constructed=False,full415F50_returned=False,GPU_drawing_or_Present=False,retained_VM_advanced=False)


def unpack_large(row):
    import base64,zlib
    from tools.school_renderer_init_verification import verify_buffer
    if not 0<row['bytes']<=274432:raise ValueError('font bounded pixel snapshot')
    dec=zlib.decompressobj();raw=dec.decompress(base64.b64decode(row['zlib_base64'],validate=True),row['bytes']+1)
    verify_buffer(row,raw);return raw


def generate(phase):
    if phase=='cleanup':owned_run=pixel_owned_run
    else:
        from tools.school_font_state_device import owned_run
    cases=[]
    for fill,width,height in ((0xA5,640,480),(0xCC,1024,768)):
        def run(bridge):
            with StateGDI() as platform:
                e=StateEmulator(bridge,platform,fill);c=prefix(e,bridge,platform,fill);c['glyph_raster']=e.resume_glyphs(c['GDI_preparation']);c['pixel_upload']=e.resume_pixels(c['glyph_raster'])
                c['font_cleanup']=e.resume_state('cleanup',c['pixel_upload'])
                if phase!='cleanup':c['font_vertex']=e.resume_state('vertex',c['font_cleanup'])
                if phase=='states':c['font_states']=e.resume_state('states',c['font_vertex'])
            c.update(platform_trace=platform.trace,platform_cleanup=platform.cleanup);return c
        result=owned_run(run,width,height);c=result['value'];c.update(device_trace=result['trace'],device_cleanup=result['cleanup'],refused_address_collisions=result['refused_address_collisions']);cases.append(c)
        print(hex(fill)+': original first-font '+phase+' verified',flush=True)
    device_path='analysis/school-font-glyph-device-v1-20261019.json' if phase=='cleanup' else 'analysis/school-font-state-device-v1-20261019.json'
    return dict(schema_version=1,phase=phase,source_contract=source_contract(),cases=cases,
        device_build=json.loads((ROOT/device_path).read_text())['build'],platform_build=json.loads((ROOT/'analysis/school-font-state-gdi-v5-20261019.json').read_text())['build'],
        explicit_empty_cache_experiment=True,CRT_adapter_executed=True,original_IAT_changed=False,game_helpers_stubbed=False,
        retained_VM_advanced=False,GPU_drawing_or_Present=False,full_outer_frame=False,live_handles_resumable_after_cleanup=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--phase',choices=('cleanup','vertex','states'),required=True);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable font state execution required')
    path.write_text(json.dumps(generate(a.phase),indent=2)+'\n',encoding='utf-8',newline='\n')
