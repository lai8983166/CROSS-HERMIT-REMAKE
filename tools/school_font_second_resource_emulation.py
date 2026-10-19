"""Continue second40120C through real owned texture and GDI preparation."""
import argparse
import json
import struct
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_font_second_emulation import SecondEmulator,OWNER,STACK,TOP,RETURN,unpack_large
from tools.school_font_second_resource_platform import SecondGDI,owned_run
from tools.school_font_glyph_upload import prefix
from tools.school_font_second_resource import *
from tools.school_font_cache import COUNTER,HEAD,CACHE,dword,store
from tools.school_renderer_init_emulation import REGISTERS,buffer_evidence
from tools.school_device_init_verification import unpack


class SecondResourceEmulator(SecondEmulator):
    def __init__(self,bridge,platform,fill):
        self.resource_running=False
        super().__init__(bridge,platform,fill)

    def _write(self,uc,access,at,size,value,user):
        if not self.resource_running:return super()._write(uc,access,at,size,value,user)
        if STACK<=at and at+size<=STACK+65536:return
        raise RuntimeError('second resource unowned native write '+hex(at))

    def _slot_read(self,uc,access,at,size,value,user):
        if not self.resource_running:return super()._slot_read(uc,access,at,size,value,user)
        allowed=[(BASE,BASE+len(self.image)),(STACK,STACK+65536),(OWNER,OWNER+0xC000),(SECOND,SECOND+SIZE)]
        allowed += [(p,p+4096) for p in self.foreign]
        if not any(a<=at and at+size<=b for a,b in allowed):
            raise RuntimeError('second resource unowned native read '+hex(at))

    def _put(self,at,raw):
        if self.resource_running and self.resource_phase=='texture' and at==SECOND+0x5C and len(raw)==4:
            self.uc.mem_write(at,raw);return
        return super()._put(at,raw)

    def _create_second(self,at,sp,ret):
        device=self.objects['device']
        args=[self.read(sp+4+i*4) for i in range(8)]
        if at!=device['methods']['80'] or ret!=0x40120F or args!=[device['pointer'],256,256,1,0,26,1,SECOND+0x5C]:
            raise RuntimeError('second original texture target/ABI')
        request=dict(pointer=device['pointer'],width=256,height=256,levels=1,usage=0,format=26,pool=1)
        result=self.bridge.request('second_atlas_create',**request)
        if result['hr']!=0:raise RuntimeError('second actual texture prerequisite')
        self._identity('second_atlas_texture',result['texture'])
        self._put(SECOND+0x5C,struct.pack('<I',result['texture']['pointer']))
        self.resource_calls.append(dict(op='second_atlas_create',va=hex(at),return_va=hex(ret),sp=sp,
            args=args,request=request,result=result,live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX,result['hr']);self.uc.reg_write(UC_X86_REG_ESP,sp+36);self.uc.reg_write(UC_X86_REG_EIP,ret)

    def _second_gdi(self,at,sp,ret):
        slot,name,_,count,original_op=next(r for r in IMPORTS if r[2]==ret)
        if at!=self.read(slot):raise RuntimeError('second original GDI import identity')
        args=[self.read(sp+4+i*4) for i in range(count)]
        if original_op=='atlas_dc':expected,request=[0],{}
        elif original_op=='atlas_dib':
            expected=[self.second_dc,TOP-488,0,TOP-444,0,0]
            request=dict(pointer=self.second_dc,header_hex=bytes(self.uc.mem_read(TOP-488,40)).hex())
        elif original_op=='atlas_muldiv':expected,request=[8,96,72],dict(args=[8,96,72])
        elif original_op=='atlas_font':
            expected=[v&0xFFFFFFFF for v in FONT_ARGS]+[SECOND]
            request=dict(args=FONT_ARGS,face_hex=bytes(self.uc.mem_read(SECOND,len(FACE))).hex())
        elif original_op in ('atlas_bitmap_select','atlas_font_select'):
            obj=self.second_bitmap if original_op=='atlas_bitmap_select' else self.second_font
            expected,request=[self.second_dc,obj],dict(pointer=self.second_dc,object=obj)
        else:
            value=dict(atlas_map=1,atlas_text=0xFFFFFF,atlas_background=0,atlas_align=0)[original_op]
            expected,request=[self.second_dc,value],dict(pointer=self.second_dc,value=value)
        if args!=expected:raise RuntimeError('second exact original GDI arguments '+original_op)
        op='second_'+original_op;result=self.owner_bridge.request(op,**request)
        if original_op=='atlas_dc':self.second_dc=result['result']
        elif original_op=='atlas_dib':
            self.second_bitmap,self.second_bits=result['result'],result['bits']
            self._put(TOP-444,struct.pack('<I',self.second_bits))
        elif original_op=='atlas_font':self.second_font=result['result']
        self.resource_calls.append(dict(op=op,name=name,slot=hex(slot),va=hex(at),return_va=hex(ret),sp=sp,
            args=args,request=request,result=result,live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX,result['result']&0xFFFFFFFF)
        self.uc.reg_write(UC_X86_REG_ESP,sp+4+count*4);self.uc.reg_write(UC_X86_REG_EIP,ret)

    def _code(self,uc,at,size,user):
        if not self.resource_running:return super()._code(uc,at,size,user)
        if at==self.resource_stop:self.boundary=at;uc.emu_stop();return
        sp=uc.reg_read(UC_X86_REG_ESP);ret=self.read(sp)
        if ret==0x40120F and at==self.objects['device']['methods']['80']:
            return self._create_second(at,sp,ret)
        if ret in {r[2] for r in IMPORTS} and at==self.read(next(r[0] for r in IMPORTS if r[2]==ret)):
            return self._second_gdi(at,sp,ret)
        if not any(a<=at and at+size<=b for a,b in RANGES.items()):
            raise RuntimeError('second resource undeclared original body '+hex(at))
        self.visited.add(at)
        if at in (0x56CEC0,0x56CFCC):
            self.entries.append(dict(va=hex(at),return_va=hex(ret),sp=sp,receiver=uc.reg_read(REGISTERS['ECX']),
                args=[self.read(sp+4+i*4) for i in range(3 if at==0x56CEC0 else 0)]))
        if at in self.resource_rets:
            self.returns.append(dict(va=hex(at),return_va=hex(ret),sp=sp,eax=uc.reg_read(UC_X86_REG_EAX)))

    def resume_resource(self,phase,previous):
        if phase not in ('texture','gdi'):raise ValueError('second resource phase')
        start,stop=(0x40120C,self.read(0x592094)) if phase=='texture' else (self.read(0x592094),0x401491)
        if self.uc.reg_read(UC_X86_REG_EIP)!=start:raise RuntimeError('second resource same pending CPU required')
        before_cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        self.entries,self.returns,self.resource_calls,self.visited,self.boundary=[],[],[],set(),None
        md=Cs(CS_ARCH_X86,CS_MODE_32)
        self.resource_rets={i.address for a,b in RANGES.items() for i in md.disasm(self.image[a-BASE:b-BASE],a) if i.mnemonic=='ret'}
        self.resource_phase,self.resource_stop,self.resource_running=phase,stop,True
        try:self.uc.emu_start(start,RETURN+1,timeout=15_000_000,count=100000)
        finally:self.resource_running=False
        if self.boundary!=stop:raise RuntimeError('second resource native boundary not reached')
        image=bytearray(self.constructed_image)
        store(image,COUNTER-BASE,dword(image,COUNTER-BASE)+3600);store(image,HEAD-BASE,CACHE)
        state=self.check(unpack(previous['state']['owner']),bytes(image),TOP-108)
        for row in previous['retained_heaps']:
            if bytes(self.uc.mem_read(row['pointer'],12288))!=unpack(row):raise RuntimeError('second resource changed prior complete heap')
        for row in previous['external_regions']:
            if bytes(self.uc.mem_read(row['base'],row['bytes']))!=unpack_large(row['buffer']):raise RuntimeError('second resource changed pixel snapshot')
        value=texture_object(unpack(previous['second_heap'])[4096:4096+SIZE],self.objects['second_atlas_texture']['pointer'])
        expected=bytearray(b'\xa5'*12288);expected[4096:4096+SIZE]=value
        actual=bytes(self.uc.mem_read(SECOND-4096,12288))
        if actual!=expected:raise RuntimeError('second resource complete second object/guard mismatch')
        cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        pending=dict(va=hex(stop),sp=cpu['ESP'],first_instruction_executed=False,platform_call_executed=False)
        if phase=='texture':pending.update(return_va=hex(self.read(cpu['ESP'])),args=[self.read(cpu['ESP']+4)])
        else:pending.update(method_target=self.read(0x5920BC),args=[self.read(cpu['ESP']+i*4) for i in range(4)])
        return dict(phase=phase,before_cpu=before_cpu,entries=self.entries,returns=self.returns,api_calls=self.resource_calls,
            visited=sorted(self.visited),state=state,heaps=previous['heaps'],slot_heap=previous['slot_heap'],
            retained_heaps=previous['retained_heaps'],second_heap=dict(pointer=SECOND-4096,**buffer_evidence(actual)),
            external_regions=previous['external_regions'],external_regions_are_retained_snapshots=True,cpu=cpu,pending=pending,
            bitmap_header=dict(pointer=TOP-488,hex=bytes(self.uc.mem_read(TOP-488,40)).hex()),
            GDI_locals=None if phase=='texture' else dict(dc=self.read(TOP-492),bitmap=self.read(TOP-496),bits=self.read(TOP-444),
                font=self.read(TOP-516),height=self.read(TOP-504),weight=self.read(TOP-508),italic=self.read(TOP-512),
                x=self.read(TOP-520),y=self.read(TOP-524),text_hex=bytes(self.uc.mem_read(TOP-528,2)).hex(),character=bytes(self.uc.mem_read(TOP-540,1)).hex()),
            first_additional_font_resources_retained=True,second_texture_created=True,second_GDI_prepared=phase=='gdi',
            second_glyph_measurement_executed=False,second_DIB_pixels_mapped=False,second_DIB_pixels_read=False,
            second_glyph_upload_executed=False,second_state_blocks_created=False,full415F50_returned=False,
            GPU_drawing_or_Present=False,retained_VM_advanced=False)


def generate(phase):
    cases=[]
    for fill,width,height in ((0xA5,640,480),(0xCC,1024,768)):
        def run(bridge):
            with SecondGDI() as platform:
                e=SecondResourceEmulator(bridge,platform,fill);c=prefix(e,bridge,platform,fill)
                c['glyph_raster']=e.resume_glyphs(c['GDI_preparation']);c['pixel_upload']=e.resume_pixels(c['glyph_raster'])
                c['font_cleanup']=e.resume_state('cleanup',c['pixel_upload']);c['font_vertex']=e.resume_state('vertex',c['font_cleanup']);c['font_states']=e.resume_state('states',c['font_vertex'])
                c['second_loop']=e.resume_second('loop',c['font_states']);c['second_constructor']=e.resume_second('constructor',c['second_loop']);c['second_atlas']=e.resume_second('atlas',c['second_constructor'])
                c['second_texture']=e.resume_resource('texture',c['second_atlas'])
                if phase=='gdi':c['second_GDI']=e.resume_resource('gdi',c['second_texture'])
            c.update(platform_trace=platform.trace,platform_cleanup=platform.cleanup);return c
        r=owned_run(run,width,height);c=r['value'];c.update(device_trace=r['trace'],device_cleanup=r['cleanup'],refused_address_collisions=r['refused_address_collisions']);cases.append(c)
        print(hex(fill)+': original second atlas '+phase+' verified',flush=True)
    return dict(schema_version=1,phase=phase,source_contract=source_contract(),cases=cases,
        device_build=json.loads((ROOT/'analysis/school-font-second-resource-device-v2-20261019.json').read_text())['build'],
        platform_build=json.loads((ROOT/'analysis/school-font-second-resource-gdi-v1-20261019.json').read_text())['build'],
        explicit_empty_cache_experiment=True,CRT_adapter_executed=True,original_IAT_changed=False,game_helpers_stubbed=False,
        retained_VM_advanced=False,GPU_drawing_or_Present=False,full_outer_frame=False,live_handles_resumable_after_cleanup=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--phase',choices=('texture','gdi'),required=True);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable second resource execution required')
    path.write_text(json.dumps(generate(a.phase),indent=2)+'\n',encoding='utf8',newline='\n')
