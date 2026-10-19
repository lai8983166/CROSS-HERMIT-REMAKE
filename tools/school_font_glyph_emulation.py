"""Continue original glyph loop on its existing CPU with owned live GDI responses."""
import argparse
import json
import struct
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_font_atlas_emulation import AtlasEmulator, OWNER, STACK, TOP, RETURN
from tools.school_font_atlas_device import owned_run
from tools.school_font_glyph_gdi import GlyphGDI
from tools.school_font_cache import FONT,CACHE,SPRITE,COUNTER,HEAD
from tools.school_font_glyph import *
from tools.school_renderer_init_emulation import REGISTERS,buffer_evidence
from tools.school_device_init_verification import unpack


class GlyphEmulator(AtlasEmulator):
    def __init__(self,bridge,platform,fill):
        self.glyph_running=False
        super().__init__(bridge,platform,fill)

    def _write(self,uc,access,at,size,value,user):
        if not self.glyph_running:return super()._write(uc,access,at,size,value,user)
        if not (STACK<=at and at+size<=STACK+65536 or SLOT+112<=at and at+size<=SLOT+1632):
            raise RuntimeError('glyph unowned native write '+hex(at))

    def _slot_read(self,uc,access,at,size,value,user):
        if not self.glyph_running:return super()._slot_read(uc,access,at,size,value,user)
        allowed=[(BASE,BASE+len(self.image)),(OWNER,OWNER+0xC000),(STACK,STACK+65536),(SLOT,SLOT+SIZE)]
        allowed += [(p,p+4096) for p in self.foreign]
        if not any(a<=at and at+size<=b for a,b in allowed):raise RuntimeError('glyph unowned native read '+hex(at))

    def _glyph_api(self,at,sp,ret):
        slot,name,count,op=IMPORTS[ret]
        args=[self.read(sp+4+i*4) for i in range(count)]
        dc=self.atlas_dc;ch=bytes(self.uc.mem_read(TOP-528,1))[0]
        if at!=self.read(slot):raise RuntimeError('glyph original imported target')
        if op=='glyph_measure':
            if args!=[dc,TOP-528,1,TOP-536]:raise RuntimeError('glyph original measure ABI')
            request=dict(pointer=dc,character=ch,before_hex=bytes(self.uc.mem_read(TOP-536,8)).hex())
        else:
            if args[0]!=dc or args[3:]!=[2,0,TOP-528,1,0]:raise RuntimeError('glyph original draw ABI')
            request=dict(pointer=dc,character=ch,x=args[1],y=args[2])
        result=self.owner_bridge.request(op,**request)
        if op=='glyph_measure':self._put(TOP-536,bytes.fromhex(result['hex']))
        self.glyph_calls.append(dict(op=op,name=name,slot=hex(slot),va=hex(at),return_va=hex(ret),sp=sp,
            args=args,request=request,result=result,live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX,result['result']);self.uc.reg_write(UC_X86_REG_ESP,sp+4+4*count);self.uc.reg_write(UC_X86_REG_EIP,ret)

    def _code(self,uc,at,size,user):
        if not self.glyph_running:return super()._code(uc,at,size,user)
        if at==self.glyph_stop:self.boundary=at;uc.emu_stop();return
        sp=uc.reg_read(UC_X86_REG_ESP);ret=self.read(sp)
        if ret in IMPORTS and at==self.read(IMPORTS[ret][0]):return self._glyph_api(at,sp,ret)
        if not any(a<=at and at+size<=b for a,b in RANGES.items()):raise RuntimeError('glyph undeclared native body '+hex(at))
        self.visited.add(at)
        if at==0x56CE82:self.returns.append(dict(va=hex(at),return_va=hex(ret),sp=sp,eax=uc.reg_read(UC_X86_REG_EAX)))

    def resume_glyphs(self,previous):
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x401491:raise RuntimeError('glyph same pending CPU required')
        before_cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        for slot,*_ in IMPORTS.values():self._foreign_write(self.read(slot),b'\xc3')
        inspections=[]
        def snapshot(stage):
            request=dict(pointer=self.atlas_bits,stage=stage);result=self.owner_bridge.request('glyph_pixels',**request)
            inspections.append(dict(op='glyph_pixels',request=request,result=result));return result
        before=snapshot('before')
        self.glyph_calls,self.returns,self.visited,self.boundary=[],[],set(),None
        self.glyph_running,self.glyph_stop=True,0x401660
        try:self.uc.emu_start(0x401491,RETURN+1,timeout=20_000_000,count=1000000)
        finally:self.glyph_running=False
        if self.boundary!=self.glyph_stop:raise RuntimeError('glyph natural loop boundary not reached')
        after=snapshot('after')
        measures=[struct.unpack('<2I',bytes.fromhex(r['result']['hex'])) for r in self.glyph_calls if r['op']=='glyph_measure']
        expected=bytearray(b'\xa5'*12288);expected[4096:4096+SIZE]=glyph_object(unpack(previous['slot_heap'])[4096:4096+SIZE],measures)
        actual=bytes(self.uc.mem_read(SLOT-4096,12288))
        if actual!=expected:raise RuntimeError('glyph full native UV object/guard mismatch')
        image=bytearray(self.constructed_image);struct.pack_into('<I',image,COUNTER-BASE,dword(image,COUNTER-BASE)+288+SIZE);struct.pack_into('<I',image,HEAD-BASE,CACHE)
        state=self.check(unpack(previous['state']['owner']),bytes(image),TOP-108)
        for row in previous['heaps']:
            if bytes(self.uc.mem_read(row['pointer'],12288))!=unpack(row):raise RuntimeError('glyph modified prior heap')
        cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()};rows,end=layout(measures)
        return dict(before_cpu=before_cpu,api_calls=self.glyph_calls,returns=self.returns,visited=sorted(self.visited),
            state=state,heaps=previous['heaps'],slot_heap=dict(pointer=SLOT-4096,**buffer_evidence(actual)),
            cpu=cpu,pending=dict(va='0x401660',sp=cpu['ESP'],first_instruction_executed=False),
            inspections=inspections,layout=rows,cursor=list(end),character=self.read(TOP-540)&255,
            glyphs_completed=95,UV_stores_completed=380,DIB_snapshot_read=True,
            native_DIB_pixels_read=False,texture_lock_executed=False,texture_upload_executed=False,
            original_cleanup_executed=False,full415F50_returned=False,state_blocks_created=False,retained_VM_advanced=False)


def prefix(e,bridge,platform,fill):
    c=dict(fill=fill,hello=bridge.hello,platform_hello=platform.hello,constructor=e.construct(),device=e.device(),font=e.font(),factory=e.factory('empty'))
    e.source_logfont=c['font']['LOGFONT'];c['requirements'],c['texture']=e.resume('requirements'),e.resume('texture')
    c['sprite'],c['font_return']=e.resume_cache('sprite'),e.resume_cache('font')
    c['slot_constructor'],c['atlas_admission']=e.resume_slot('constructor'),e.resume_slot('atlas')
    c['atlas_texture']=e.resume_atlas('texture',c['atlas_admission']);c['GDI_preparation']=e.resume_atlas('gdi',c['atlas_texture'])
    return c


def generate(phase='raster'):
    cases=[]
    for fill,width,height in ((0xA5,640,480),(0xCC,1024,768)):
        def run(bridge):
            with GlyphGDI() as platform:
                e=GlyphEmulator(bridge,platform,fill);c=prefix(e,bridge,platform,fill);c['glyph_raster']=e.resume_glyphs(c['GDI_preparation'])
            c.update(platform_trace=platform.trace,platform_cleanup=platform.cleanup);return c
        result=owned_run(run,width,height);c=result['value'];c.update(device_trace=result['trace'],device_cleanup=result['cleanup'],refused_address_collisions=result['refused_address_collisions']);cases.append(c)
        print(hex(fill)+': original95 glyph raster verified',flush=True)
    return dict(schema_version=1,phase=phase,source_contract=source_contract(),cases=cases,
        device_build=json.loads((ROOT/'analysis/school-font-atlas-device-v1-20261018.json').read_text())['build'],
        platform_build=json.loads((ROOT/'analysis/school-font-glyph-gdi-v1-20261019.json').read_text())['build'],
        explicit_empty_cache_experiment=True,CRT_adapter_executed=True,original_IAT_changed=False,game_helpers_stubbed=False,
        retained_VM_advanced=False,GPU_drawing_or_Present=False,full_outer_frame=False,live_handles_resumable_after_cleanup=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable glyph report required')
    path.write_text(json.dumps(generate(),indent=2)+'\n',encoding='utf-8',newline='\n')
