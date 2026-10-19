"""Original65536-pixel conversion on guarded real-identity shadow buffers and upload."""
import argparse
import hashlib
import json
import struct
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_font_glyph_emulation import GlyphEmulator,prefix,OWNER,STACK,TOP,RETURN
from tools.school_font_glyph_device import owned_run
from tools.school_font_glyph_gdi import GlyphGDI
from tools.school_font_glyph import *
from tools.school_renderer_init_emulation import REGISTERS,buffer_evidence
from tools.school_device_init_verification import unpack


class PixelEmulator(GlyphEmulator):
    def __init__(self,bridge,platform,fill):
        self.pixel_running=False;self.shadows=[]
        super().__init__(bridge,platform,fill)

    def _map_page(self,address):
        if any(r['base']<=address<r['base']+r['bytes'] for r in self.shadows):raise RuntimeError('live interface mapping collides with audit ownership')
        return super()._map_page(address)

    def _shadow(self,name,pointer,data):
        start=(pointer&~4095)-4096;end=((pointer+len(data)+4095)&~4095)+4096
        if start<0 or end>0x100000000:raise RuntimeError('live interface mapping collides with audit ownership')
        for lo,hi,perm in self.uc.mem_regions():
            if start<=hi and lo<end:raise RuntimeError('live interface mapping collides with audit ownership')
        self.uc.mem_map(start,end-start);self.uc.mem_write(start,b'\xa5'*(end-start));self.uc.mem_write(pointer,data)
        self.shadows.append(dict(name=name,pointer=pointer,base=start,bytes=end-start,data_bytes=len(data)))

    def _write(self,uc,access,at,size,value,user):
        if not self.pixel_running:return super()._write(uc,access,at,size,value,user)
        if STACK<=at and at+size<=STACK+65536:return
        if hasattr(self,'locked_bits') and self.locked_bits<=at<self.locked_bits+self.pitch*256:
            n=self.pixel_writes;expected=self.locked_bits+(n//256)*self.pitch+(n%256)*2
            if n>=65536 or at!=expected or size!=2:raise RuntimeError('glyph exact native pixel write sequence')
            self.write_hash.update(struct.pack('<IIH',at,size,value&65535));self.pixel_writes+=1;return
        raise RuntimeError('glyph upload unowned native write '+hex(at))

    def _slot_read(self,uc,access,at,size,value,user):
        if not self.pixel_running:return super()._slot_read(uc,access,at,size,value,user)
        if self.atlas_bits<=at<self.atlas_bits+262144:
            if self.pixel_reads>=65536 or at!=self.atlas_bits+self.pixel_reads*4 or size!=4:raise RuntimeError('glyph exact native DIB read sequence')
            self.read_hash.update(struct.pack('<II',at,size));self.pixel_reads+=1;return
        if STACK<=at and at+size<=STACK+65536 or SLOT<=at and at+size<=SLOT+SIZE:return
        if any(a<=at and at+size<=a+4096 for a in self.foreign):return
        if BASE<=at and at+size<=BASE+len(self.image):return
        raise RuntimeError('glyph upload unowned native read '+hex(at))

    def _pixel_api(self,at,sp,ret):
        texture=self.objects['atlas_texture'];pointer=texture['pointer'];lock=ret==0x401681
        count=5 if lock else 2;args=[self.read(sp+4+i*4) for i in range(count)]
        if at!=texture['methods']['64' if lock else '68'] or args!=([pointer,0,TOP-548,0,0] if lock else [pointer,0]):
            raise RuntimeError('glyph original actual lock/unlock identity/ABI')
        if lock:
            request=dict(pointer=pointer,level=0,rect=0,flags=0);op='atlas_lock';result=self.bridge.request(op,**request)
            self.pitch,self.locked_bits=result['pitch'],result['bits'];self.locked_before=bytes.fromhex(result['before_hex'])
            if result['locked_hex']!=struct.pack('<2I',self.pitch,self.locked_bits).hex():raise RuntimeError('glyph actual full locked rectangle')
            self._shadow('texture',self.locked_bits,self.locked_before);self._put(TOP-548,bytes.fromhex(result['locked_hex']))
        else:
            actual=bytes(self.uc.mem_read(self.locked_bits,self.pitch*256))
            if actual!=pixels(self.dib_bytes,self.locked_before,self.pitch):raise RuntimeError('glyph full native conversion/padding mismatch')
            request=dict(pointer=pointer,level=0,bytes_hex=actual.hex());op='atlas_unlock';result=self.bridge.request(op,**request)
        self.pixel_calls.append(dict(op=op,va=hex(at),return_va=hex(ret),sp=sp,args=args,request=request,result=result,live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX,result['hr']);self.uc.reg_write(UC_X86_REG_ESP,sp+4+4*count);self.uc.reg_write(UC_X86_REG_EIP,ret)

    def _code(self,uc,at,size,user):
        if not self.pixel_running:return super()._code(uc,at,size,user)
        if at==0x4017B6:self.boundary=at;uc.emu_stop();return
        if at in (self.objects['atlas_texture']['methods']['64'],self.objects['atlas_texture']['methods']['68']):
            sp=uc.reg_read(UC_X86_REG_ESP);ret=self.read(sp)
            if ret not in (0x401681,0x4017AF):raise RuntimeError('glyph original texture API return')
            return self._pixel_api(at,sp,ret)
        if not any(a<=at and at+size<=b for a,b in RANGES.items()):raise RuntimeError('glyph upload undeclared native body '+hex(at))
        self.visited.add(at)
        if at==0x56CE82:
            sp=uc.reg_read(UC_X86_REG_ESP);self.returns.append(dict(va=hex(at),return_va=hex(self.read(sp)),sp=sp,eax=uc.reg_read(UC_X86_REG_EAX)))

    def resume_pixels(self,previous):
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x401660:raise RuntimeError('glyph upload same pending original CPU')
        before_cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        self.dib_bytes=bytes.fromhex(previous['inspections'][1]['result']['hex']);self._shadow('DIB',self.atlas_bits,self.dib_bytes)
        self.pixel_calls,self.returns,self.visited,self.boundary=[],[],set(),None
        self.pixel_reads=self.pixel_writes=0;self.read_hash,self.write_hash=hashlib.sha256(),hashlib.sha256();self.pixel_running=True
        try:self.uc.emu_start(0x401660,RETURN+1,timeout=90_000_000,count=10000000)
        finally:self.pixel_running=False
        if self.boundary!=0x4017B6 or self.pixel_reads!=65536 or self.pixel_writes!=65536:raise RuntimeError('glyph full original pixel loop not completed')
        state=self.check(unpack(previous['state']['owner']),bytes(self.uc.mem_read(BASE,len(self.image))),TOP-108)
        if state['image_sha256']!=previous['state']['image_sha256']:raise RuntimeError('glyph upload source image changed')
        for row in [*previous['heaps'],previous['slot_heap']]:
            if bytes(self.uc.mem_read(row['pointer'],12288))!=unpack(row):raise RuntimeError('glyph upload prior complete heap changed')
        regions=[]
        for r in self.shadows:
            data=self.dib_bytes if r['name']=='DIB' else pixels(self.dib_bytes,self.locked_before,self.pitch)
            expected=bytearray(b'\xa5'*r['bytes']);offset=r['pointer']-r['base'];expected[offset:offset+len(data)]=data
            actual=bytes(self.uc.mem_read(r['base'],r['bytes']))
            if actual!=expected:raise RuntimeError('glyph external buffer complete guards mismatch')
            regions.append(dict(**r,buffer=buffer_evidence(actual)))
        cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        return dict(before_cpu=before_cpu,api_calls=self.pixel_calls,returns=self.returns,visited=sorted(self.visited),state=state,
            heaps=previous['heaps'],slot_heap=previous['slot_heap'],cpu=cpu,pending=dict(va='0x4017b6',sp=cpu['ESP'],first_instruction_executed=False),
            external_regions=regions,native_pixel_reads=self.pixel_reads,native_pixel_writes=self.pixel_writes,
            read_sequence_sha256=self.read_hash.hexdigest(),write_sequence_sha256=self.write_hash.hexdigest(),
            locals=dict(x=self.read(TOP-520),y=self.read(TOP-524),pitch=self.read(TOP-548),bits=self.read(TOP-544),
                row=self.read(TOP-552),cursor=self.read(TOP-556),alpha=self.read(TOP-560)&255),
            original_lock_executed=True,original_conversion_executed=True,original_unlock_executed=True,
            actual_texture_upload_verified=True,readonly_readback_inspection_only=True,original_cleanup_executed=False,
            full4010D0_returned=False,full415F50_returned=False,state_blocks_created=False,retained_VM_advanced=False)


def generate():
    cases=[]
    for fill,width,height in ((0xA5,640,480),(0xCC,1024,768)):
        def run(bridge):
            with GlyphGDI() as platform:
                e=PixelEmulator(bridge,platform,fill);c=prefix(e,bridge,platform,fill);c['glyph_raster']=e.resume_glyphs(c['GDI_preparation']);c['pixel_upload']=e.resume_pixels(c['glyph_raster'])
            c.update(platform_trace=platform.trace,platform_cleanup=platform.cleanup);return c
        result=owned_run(run,width,height);c=result['value'];c.update(device_trace=result['trace'],device_cleanup=result['cleanup'],refused_address_collisions=result['refused_address_collisions']);cases.append(c)
        print(hex(fill)+': original65536 pixel conversion and real upload verified',flush=True)
    return dict(schema_version=1,phase='upload',source_contract=source_contract(),cases=cases,
        device_build=json.loads((ROOT/'analysis/school-font-glyph-device-v1-20261019.json').read_text())['build'],
        platform_build=json.loads((ROOT/'analysis/school-font-glyph-gdi-v1-20261019.json').read_text())['build'],
        explicit_empty_cache_experiment=True,CRT_adapter_executed=True,original_IAT_changed=False,game_helpers_stubbed=False,
        retained_VM_advanced=False,GPU_drawing_or_Present=False,full_outer_frame=False,live_handles_resumable_after_cleanup=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable pixel upload report required')
    path.write_text(json.dumps(generate(),indent=2)+'\n',encoding='utf-8',newline='\n')
