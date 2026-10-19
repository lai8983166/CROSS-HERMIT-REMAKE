"""Retire deleted first DIB shadow, execute second glyphs and native pixel upload."""
import argparse
import hashlib
import json
import struct
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools.school_font_second_resource_emulation import SecondResourceEmulator,OWNER,STACK,TOP,RETURN,unpack_large
from tools.school_font_second_glyph_platform import SecondGlyphGDI,owned_run
from tools.school_font_glyph_upload import prefix
from tools.school_font_second_glyph import *
from tools.school_font_cache import COUNTER,HEAD,CACHE,dword,store
from tools.school_renderer_init_emulation import REGISTERS,buffer_evidence
from tools.school_device_init_verification import unpack


class SecondGlyphEmulator(SecondResourceEmulator):
    def __init__(self,bridge,platform,fill):
        self.second_glyph_running=False;self.second_pixel_running=False
        super().__init__(bridge,platform,fill)

    def _write(self,uc,access,at,size,value,user):
        if not (self.second_glyph_running or self.second_pixel_running):return super()._write(uc,access,at,size,value,user)
        if STACK<=at and at+size<=STACK+65536:return
        if self.second_glyph_running and SECOND+112<=at and at+size<=SECOND+1632:
            if size!=4:raise RuntimeError('second glyph exact UV store size')
            self.second_uv_stores+=1;return
        if self.second_pixel_running and hasattr(self,'second_locked_bits') and self.second_locked_bits<=at<self.second_locked_bits+self.second_pitch*256:
            n=self.second_pixel_writes;expected=self.second_locked_bits+(n//256)*self.second_pitch+(n%256)*2
            if n>=65536 or at!=expected or size!=2:raise RuntimeError('second pixel exact native write order')
            self.second_write_hash.update(struct.pack('<IIH',at,size,value&65535));self.second_pixel_writes+=1;return
        raise RuntimeError('second glyph/upload unowned native write '+hex(at))

    def _slot_read(self,uc,access,at,size,value,user):
        if not (self.second_glyph_running or self.second_pixel_running):return super()._slot_read(uc,access,at,size,value,user)
        if self.second_pixel_running and self.second_bits<=at<self.second_bits+262144:
            if self.second_pixel_reads>=65536 or at!=self.second_bits+self.second_pixel_reads*4 or size!=4:raise RuntimeError('second pixel exact native DIB read order')
            self.second_read_hash.update(struct.pack('<II',at,size));self.second_pixel_reads+=1;return
        allowed=[(BASE,BASE+len(self.image)),(STACK,STACK+65536),(SECOND,SECOND+SIZE)]
        allowed += [(p,p+4096) for p in self.foreign]
        if not any(a<=at and at+size<=b for a,b in allowed):raise RuntimeError('second glyph/upload unowned native read '+hex(at))

    def _glyph_second_api(self,at,sp,ret):
        slot,name,count,old_op=IMPORTS[ret];dc=self.second_dc;ch=bytes(self.uc.mem_read(TOP-528,1))[0]
        args=[self.read(sp+4+i*4) for i in range(count)]
        if at!=self.read(slot):raise RuntimeError('second glyph original import identity')
        if old_op=='glyph_measure':
            if args!=[dc,TOP-528,1,TOP-536]:raise RuntimeError('second original measurement ABI')
            request=dict(pointer=dc,character=ch,before_hex=bytes(self.uc.mem_read(TOP-536,8)).hex())
        else:
            if args[0]!=dc or args[3:]!=[2,0,TOP-528,1,0]:raise RuntimeError('second original drawing ABI')
            request=dict(pointer=dc,character=ch,x=args[1],y=args[2])
        op='second_'+old_op;result=self.owner_bridge.request(op,**request)
        if old_op=='glyph_measure':self._put(TOP-536,bytes.fromhex(result['hex']))
        self.second_calls.append(dict(op=op,name=name,slot=hex(slot),va=hex(at),return_va=hex(ret),sp=sp,args=args,request=request,result=result,live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX,result['result']);self.uc.reg_write(UC_X86_REG_ESP,sp+4+count*4);self.uc.reg_write(UC_X86_REG_EIP,ret)

    def _pixel_second_api(self,at,sp,ret):
        texture=self.objects['second_atlas_texture'];pointer=texture['pointer'];lock=ret==0x401681
        args=[self.read(sp+4+i*4) for i in range(5 if lock else 2)]
        if at!=texture['methods']['64' if lock else '68'] or args!=([pointer,0,TOP-548,0,0] if lock else [pointer,0]):
            raise RuntimeError('second original lock/unlock identity/ABI')
        if lock:
            op='second_atlas_lock';request=dict(pointer=pointer,level=0,rect=0,flags=0);result=self.bridge.request(op,**request)
            self.second_pitch,self.second_locked_bits=result['pitch'],result['bits'];self.second_locked_before=bytes.fromhex(result['before_hex'])
            if result['locked_hex']!=struct.pack('<2I',self.second_pitch,self.second_locked_bits).hex():raise RuntimeError('second actual locked rectangle')
            self._shadow('second_texture',self.second_locked_bits,self.second_locked_before);self._put(TOP-548,bytes.fromhex(result['locked_hex']))
        else:
            actual=bytes(self.uc.mem_read(self.second_locked_bits,self.second_pitch*256))
            if actual!=pixels(self.second_dib,self.second_locked_before,self.second_pitch):raise RuntimeError('second complete native pixel projection')
            op='second_atlas_unlock';request=dict(pointer=pointer,level=0,bytes_hex=actual.hex());result=self.bridge.request(op,**request)
            first=result['retained_first_texture_inspection']
            if (first['pointer']!=self.objects['atlas_texture']['pointer'] or first['pitch']!=self.pitch
                    or bytes.fromhex(first['hex'])!=pixels(self.dib_bytes,self.locked_before,self.pitch)):
                raise RuntimeError('second upload changed retained actual first texture bytes')
        self.second_calls.append(dict(op=op,va=hex(at),return_va=hex(ret),sp=sp,args=args,request=request,result=result,live_host_observed=True))
        self.uc.reg_write(UC_X86_REG_EAX,result['hr']);self.uc.reg_write(UC_X86_REG_ESP,sp+4+len(args)*4);self.uc.reg_write(UC_X86_REG_EIP,ret)

    def _code(self,uc,at,size,user):
        if not (self.second_glyph_running or self.second_pixel_running):return super()._code(uc,at,size,user)
        if at==self.second_stop:self.boundary=at;uc.emu_stop();return
        sp=uc.reg_read(UC_X86_REG_ESP);ret=self.read(sp)
        if self.second_glyph_running and ret in IMPORTS and at==self.read(IMPORTS[ret][0]):return self._glyph_second_api(at,sp,ret)
        if self.second_pixel_running and ret in (0x401681,0x4017AF):return self._pixel_second_api(at,sp,ret)
        if not any(a<=at and at+size<=b for a,b in RANGES.items()):raise RuntimeError('second glyph/upload undeclared native body '+hex(at))
        self.visited.add(at)
        if at==0x56CE82:self.returns.append(dict(va=hex(at),return_va=hex(ret),sp=sp,eax=uc.reg_read(UC_X86_REG_EAX)))

    def _retention(self,previous):
        image=bytearray(self.constructed_image);store(image,COUNTER-BASE,dword(image,COUNTER-BASE)+3600);store(image,HEAD-BASE,CACHE)
        state=self.check(unpack(previous['state']['owner']),bytes(image),TOP-108)
        for r in previous['retained_heaps']:
            if bytes(self.uc.mem_read(r['pointer'],12288))!=unpack(r):raise RuntimeError('second glyph/upload changed retained heap')
        for r in previous['external_regions']:
            if bytes(self.uc.mem_read(r['base'],r['bytes']))!=unpack_large(r['buffer']):raise RuntimeError('second glyph/upload changed retained pixel region')
        return state

    def _row(self,previous,state):
        return dict(state=state,heaps=previous['heaps'],slot_heap=previous['slot_heap'],retained_heaps=previous['retained_heaps'],
            external_regions=previous['external_regions'],retired_regions=self.retired_regions,
            second_heap=previous['second_heap'],first_font_resources_retained=True,
            full4010D0_returned=False,full415F50_returned=False,second_state_blocks_created=False,
            GPU_drawing_or_Present=False,retained_VM_advanced=False)

    def retire_first_DIB(self,previous,cleanup):
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x401491:raise RuntimeError('second retirement same pending CPU required')
        if (cleanup['original_GDI_cleanup_executed'] is not True or cleanup['full4010D0_returned'] is not True
                or [r['result']['result'] for r in cleanup['api_calls']]!=[1,1,1]
                or cleanup['api_calls'][1]['result']['inspection']['result']!=0):raise RuntimeError('second retirement requires verified first native GDI deletion')
        self._retention(previous)
        active,retired=retire_regions(previous['external_regions']);old=retired[0]['region']
        if self.shadows!=[{k:v for k,v in r.items() if k!='buffer'} for r in previous['external_regions']]:raise RuntimeError('second retirement exact shadow ownership')
        before_cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()};before=[list(r) for r in self.uc.mem_regions()]
        self.uc.mem_unmap(old['base'],old['bytes'])
        self.shadows=[{k:v for k,v in r.items() if k!='buffer'} for r in active];self.retired_regions=retired
        state=self.check(unpack(previous['state']['owner']),bytes(self.uc.mem_read(BASE,len(self.image))),TOP-108)
        row=self._row(previous,state);row.update(phase='retirement',before_cpu=before_cpu,cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()},
            pending=previous['pending'],external_regions=active,mappings_before=before,mappings_after=[list(r) for r in self.uc.mem_regions()],
            api_calls=[],original_instructions_executed=0,second_glyphs_completed=0)
        return row

    def second_raster(self,previous):
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x401491:raise RuntimeError('second raster same pending CPU required')
        before_cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()};inspections=[]
        def snapshot(stage):
            request=dict(pointer=self.second_bits,stage=stage);result=self.owner_bridge.request('second_glyph_pixels',**request)
            inspections.append(dict(op='second_glyph_pixels',request=request,result=result))
        snapshot('before');self.second_calls,self.returns,self.visited,self.boundary=[],[],set(),None
        self.second_uv_stores=0;self.second_glyph_running,self.second_stop=True,0x401660
        try:self.uc.emu_start(0x401491,RETURN+1,timeout=20_000_000,count=1000000)
        finally:self.second_glyph_running=False
        if self.boundary!=0x401660:raise RuntimeError('second native glyph loop boundary')
        snapshot('after');measures=[struct.unpack('<2I',bytes.fromhex(r['result']['hex'])) for r in self.second_calls if r['op']=='second_glyph_measure']
        expected=bytearray(b'\xa5'*12288);expected[4096:4096+SIZE]=glyph_object(unpack(previous['second_heap'])[4096:4096+SIZE],measures)
        actual=bytes(self.uc.mem_read(SECOND-4096,12288))
        if actual!=expected or self.second_uv_stores!=380:raise RuntimeError('second complete native UV object/guards/stores')
        state=self._retention(previous);cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()};rows,end=layout(measures)
        row=self._row(previous,state);row.update(phase='raster',before_cpu=before_cpu,api_calls=self.second_calls,returns=self.returns,visited=sorted(self.visited),
            second_heap=dict(pointer=SECOND-4096,**buffer_evidence(actual)),cpu=cpu,pending=dict(va='0x401660',sp=cpu['ESP'],first_instruction_executed=False),
            inspections=inspections,layout=rows,cursor=list(end),character=self.read(TOP-540)&255,second_glyphs_completed=95,UV_stores_completed=self.second_uv_stores,
            native_second_DIB_pixels_read=False,second_texture_upload_executed=False)
        return row

    def second_upload(self,previous):
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x401660:raise RuntimeError('second upload same pending CPU required')
        before_cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()}
        self.second_dib=bytes.fromhex(previous['inspections'][1]['result']['hex']);self._shadow('second_DIB',self.second_bits,self.second_dib)
        self.second_calls,self.returns,self.visited,self.boundary=[],[],set(),None
        self.second_pixel_reads=self.second_pixel_writes=0;self.second_read_hash,self.second_write_hash=hashlib.sha256(),hashlib.sha256()
        self.second_pixel_running,self.second_stop=True,0x4017B6
        try:self.uc.emu_start(0x401660,RETURN+1,timeout=90_000_000,count=10000000)
        finally:self.second_pixel_running=False
        if self.boundary!=0x4017B6 or self.second_pixel_reads!=65536 or self.second_pixel_writes!=65536:raise RuntimeError('second complete original pixel loop')
        state=self._retention(previous);regions=list(previous['external_regions'])
        for r in self.shadows[1:]:
            data=self.second_dib if r['name']=='second_DIB' else pixels(self.second_dib,self.second_locked_before,self.second_pitch)
            expected=bytearray(b'\xa5'*r['bytes']);offset=r['pointer']-r['base'];expected[offset:offset+len(data)]=data
            actual=bytes(self.uc.mem_read(r['base'],r['bytes']))
            if actual!=expected:raise RuntimeError('second new pixel complete guards')
            regions.append(dict(**r,buffer=buffer_evidence(actual)))
        cpu={k:self.uc.reg_read(r) for k,r in REGISTERS.items()};row=self._row(previous,state)
        row.update(phase='upload',before_cpu=before_cpu,api_calls=self.second_calls,returns=self.returns,visited=sorted(self.visited),cpu=cpu,
            pending=dict(va='0x4017b6',sp=cpu['ESP'],first_instruction_executed=False),external_regions=regions,
            native_pixel_reads=self.second_pixel_reads,native_pixel_writes=self.second_pixel_writes,
            read_sequence_sha256=self.second_read_hash.hexdigest(),write_sequence_sha256=self.second_write_hash.hexdigest(),
            locals=dict(x=self.read(TOP-520),y=self.read(TOP-524),pitch=self.read(TOP-548),bits=self.read(TOP-544),row=self.read(TOP-552),cursor=self.read(TOP-556),alpha=self.read(TOP-560)&255),
            second_glyphs_completed=95,original_lock_executed=True,original_conversion_executed=True,original_unlock_executed=True,
            second_texture_upload_executed=True,actual_second_readback_verified=True,actual_first_texture_unchanged_verified=True)
        return row


def generate(phase):
    cases=[]
    for fill,width,height in ((0xA5,640,480),(0xCC,1024,768)):
        def run(bridge):
            with SecondGlyphGDI() as platform:
                e=SecondGlyphEmulator(bridge,platform,fill);c=prefix(e,bridge,platform,fill)
                c['glyph_raster']=e.resume_glyphs(c['GDI_preparation']);c['pixel_upload']=e.resume_pixels(c['glyph_raster'])
                c['font_cleanup']=e.resume_state('cleanup',c['pixel_upload']);c['font_vertex']=e.resume_state('vertex',c['font_cleanup']);c['font_states']=e.resume_state('states',c['font_vertex'])
                c['second_loop']=e.resume_second('loop',c['font_states']);c['second_constructor']=e.resume_second('constructor',c['second_loop']);c['second_atlas']=e.resume_second('atlas',c['second_constructor'])
                c['second_texture']=e.resume_resource('texture',c['second_atlas']);c['second_GDI']=e.resume_resource('gdi',c['second_texture'])
                c['DIB_retirement']=e.retire_first_DIB(c['second_GDI'],c['font_cleanup'])
                if phase!='retirement':c['second_raster']=e.second_raster(c['DIB_retirement'])
                if phase=='upload':c['second_upload']=e.second_upload(c['second_raster'])
            c.update(platform_trace=platform.trace,platform_cleanup=platform.cleanup);return c
        r=owned_run(run,width,height);c=r['value'];c.update(device_trace=r['trace'],device_cleanup=r['cleanup'],refused_address_collisions=r['refused_address_collisions']);cases.append(c)
        print(hex(fill)+': second glyph '+phase+' verified',flush=True)
    return dict(schema_version=1,phase=phase,source_contract=source_contract(),cases=cases,
        device_build=json.loads((ROOT/'analysis/school-font-second-glyph-device-v1-20261019.json').read_text())['build'],
        platform_build=json.loads((ROOT/'analysis/school-font-second-glyph-gdi-v2-20261019.json').read_text())['build'],
        explicit_empty_cache_experiment=True,CRT_adapter_executed=True,original_IAT_changed=False,game_helpers_stubbed=False,
        retained_VM_advanced=False,GPU_drawing_or_Present=False,full_outer_frame=False,live_handles_resumable_after_cleanup=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--phase',choices=('retirement','raster','upload'),required=True);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable second glyph execution required')
    path.write_text(json.dumps(generate(a.phase),indent=2)+chr(10),encoding='utf8',newline=chr(10))
