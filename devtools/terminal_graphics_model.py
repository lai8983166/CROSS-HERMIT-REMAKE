"""Bounded original fullscreen/font continuation with explicit symbolic OS inputs."""
from __future__ import annotations
import argparse,copy,gzip,json,struct,time
from pathlib import Path
from devtools.terminal_game_platform_model import Model as ParentModel
from devtools.terminal_game_platform import begin_original_game
from devtools.terminal_graphics_platform import GraphicsEngine,GraphicsOwner,METHODS,base,need,cleanup_before_input

ROOT=base.ROOT
CAPS_SOURCE='analysis/school-device-init-native-v1-20261017.json'
CAPS_SHA='7f585fd99355cf5b6aa803db3577edf58f5283c262db35128ad8b23b7778825f'


class Model(ParentModel,GraphicsOwner):
    consume_line=GraphicsOwner.consume_line
    def __init__(self,*args):
        super().__init__(*args);self.deadline=time.monotonic()+90;self.primitive.deadline=self.deadline
        raw=(ROOT/CAPS_SOURCE).read_bytes();need(base.sha(raw)==CAPS_SHA,'fixed old capability input')
        old=json.loads(raw)['cases'][0]['actual']['live_results']
        self.caps=bytes.fromhex(next(x['result']['hex'] for x in old if x['op']=='caps'))
        self.objects={};self.gfx_gate=0;self.baseline=None;self.factory=0;self.device=0;self.next_object=0x33000000
        self.gdi={};self.dibs={};self.dc_selected={};self.tokens=set();self.recording=False;self.texture_bound=0;self.saved_gamma={};self.gamma={};self.debug_balance=0
        self.modes=[struct.pack('<4I',1024,768,60,f) for f in (22,23,24,25)]
    def check(self):need(time.monotonic()<self.deadline,'90 second bounded symbolic graphics route')
    def buffer_data(self,p,n):
        b,o=self.primitive.region(p,n);return bytes(b[o:o+n])
    def store(self,p,raw):
        b,o=self.primitive.region(p,len(raw));b[o:o+len(raw)]=raw
    def new(self,kind,**kw):
        ptr=self.next_object;self.next_object+=4096;self.objects[ptr]=dict(kind=kind,refs=1,**kw);return ptr
    def metadata(self,p):
        o=self.objects[p];r=dict(object=p,kind=o['kind'],vtable=p+256,owned_refs=o['refs'],group=o.get('parent',0),method0=0x35000000)
        for slot in METHODS[o['kind']]:r['method'+str(slot)]=0x35000000+o['kind']*4096+slot*16
        return r
    def send(self,lane,op,*a):
        if not op.startswith('GFX_'):
            seq=super().send(lane,op,*a)
            if op=='STATUS':self.deliveries[seq][-1]+=f' gfx_gate={self.gfx_gate} gfx_refs={sum(x["refs"] for x in self.objects.values())} gfx_interfaces={len(self.objects)} gfx_locks={sum("lock" in x for x in self.objects.values())} gfx_blocks={len(self.tokens)} gfx_recording={int(self.recording)} gfx_dcs={sum(x=="dc" for x in self.gdi.values())} gfx_bitmaps={sum(x=="bitmap" for x in self.gdi.values())} gfx_fonts={sum(x=="font" for x in self.gdi.values())} gfx_gamma_dirty={len(self.saved_gamma)} gfx_baseline={int(self.baseline is not None)} gfx_modules={int(self.factory!=0)} gfx_mute={self.debug_balance} gfx_unresolved_refs=0'
            return seq
        self.check();need(lane==0,'symbolic graphics MAIN')
        self.seq+=1;seq=self.seq;self.requests[seq]=(0,op);self.trace.append(dict(direction='request',id=seq,lane=0,op=op,args=list(a)))
        fields={};value=0
        if op=='GFX_GATE':self.gfx_gate=a[0];value=1
        elif op=='GFX_BASELINE':self.baseline=self.buffer_data(a[0],32);value=1
        elif op=='GFX_BASELINE_CLEAR':self.baseline=None;value=1
        else:
            need(self.gfx_gate and self.baseline,'declared graphics gate and baseline')
            if op=='GFX_FACTORY':need(a==(220,) and not self.factory,'one original factory');self.factory=self.new(10);value=self.factory;fields=self.metadata(value)
            elif op=='GFX_MODE_COUNT':value=len(self.modes)
            elif op=='GFX_ENUM_MODE':self.store(a[3],self.modes[a[2]])
            elif op in ('GFX_DISPLAY_MODE','GFX_DEVICE_MODE'):self.store(a[-1],self.modes[0])
            elif op=='GFX_CREATE_DEVICE':
                need(a[0]==self.factory and a[3]==self.hwnd and not self.device,'declared current device')
                pp=self.buffer_data(a[5],52);values=struct.unpack('<13I',pp);need(values[7]==0,'original fullscreen retained')
                self.pp=values;self.device=self.new(11,parent=self.factory);self.store(a[6],struct.pack('<I',self.device));fields=self.metadata(self.device)
            elif op=='GFX_CAPS':self.store(a[1],self.caps)
            elif op=='GFX_CREATION':self.store(a[1],struct.pack('<4I',0,1,self.hwnd,68))
            elif op=='GFX_GET_FACTORY':self.objects[self.factory]['refs']+=1;self.store(a[1],struct.pack('<I',self.factory));fields=self.metadata(self.factory)
            elif op=='GFX_BACKBUFFER':
                p=self.new(12,parent=a[0],desc=struct.pack('<8I',self.pp[2],1,1,0,0,0,self.pp[0],self.pp[1]));self.store(a[3],struct.pack('<I',p));fields=self.metadata(p)
            elif op=='GFX_SURFACE_DESC':self.store(a[1],self.objects[a[0]]['desc'])
            elif op=='GFX_TEXTURE':
                _,w,h,levels,usage,fmt,pool,out=a;need((w,h,levels,usage,fmt,pool) in ((64,16,1,512,21,0),(256,256,1,0,26,1)),'declared original font texture')
                pitch=w*(2 if fmt==26 else 4);p=self.new(13,parent=a[0],w=w,h=h,pitch=pitch,fmt=fmt,pool=pool,usage=usage,pixels=bytearray(pitch*h));self.store(out,struct.pack('<I',p));fields=self.metadata(p)
            elif op in ('GFX_TEXTURE_SURFACE','GFX_LEVEL_DESC'):
                o=self.objects[a[0]];desc=struct.pack('<8I',o['fmt'],1,o['usage'],o['pool'],len(o['pixels']),0,o['w'],o['h'])
                if op=='GFX_LEVEL_DESC':self.store(a[2],desc)
                else:p=self.new(12,parent=a[0],desc=desc);self.store(a[2],struct.pack('<I',p));fields=self.metadata(p)
            elif op=='GFX_LOCK':
                o=self.objects[a[0]];need('lock' not in o and a[1]==a[3]==0,'fresh declared lock');o['lock']=True;self.store(a[2],struct.pack('<II',o['pitch'],a[0]+0x1000000));fields['lock_bytes']=len(o['pixels'])
            elif op in ('GFX_LOCK_READ','GFX_LOCK_WRITE'):
                p,off,buf,n=a;o=self.objects[p];need(o.get('lock') and off+n<=len(o['pixels']),'owned symbolic lock range')
                if op.endswith('READ'):self.store(buf,bytes(o['pixels'][off:off+n]))
                else:o['pixels'][off:off+n]=self.buffer_data(buf,n)
                value=n
            elif op=='GFX_UNLOCK':del self.objects[a[0]]['lock']
            elif op=='GFX_VERTEX_BUFFER':p=self.new(14,parent=a[0]);self.store(a[5],struct.pack('<I',p));fields=self.metadata(p)
            elif op=='GFX_VERTEX_DESC':self.store(a[1],struct.pack('<6I',0,6,520,0,8400,0))
            elif op=='GFX_BEGIN':need(not self.recording,'no nested state block');self.recording=True
            elif op=='GFX_END':
                need(self.recording,'state block begun');self.recording=False;t=0x123000+len(self.tokens);self.tokens.add(t);self.store(a[1],struct.pack('<I',t))
            elif op=='GFX_DELETE_BLOCK':self.tokens.remove(a[1])
            elif op=='GFX_TEXTURE_BIND':self.texture_bound=a[2]
            elif op=='GFX_GET_RENDER_STATE':self.store(a[2],bytes(4))
            elif op in ('GFX_CHECK_FORMAT','GFX_VIEWPORT','GFX_RENDER_STATE','GFX_STAGE_STATE'):pass
            elif op in ('GFX_ADDREF','GFX_RELEASE'):
                o=self.objects[a[0]];o['refs']+=1 if op=='GFX_ADDREF' else -1;need(o['refs']>=0,'current graphics references')
                value=o['refs'];fields=dict(remaining_owned_refs=value,released_owned_ref=int(op=='GFX_RELEASE'))
                if not value:del self.objects[a[0]]
            elif op=='GFX_GAMMA_SAVE':
                need(a[0] not in self.saved_gamma,'one original device ramp save');raw=struct.pack('<768H',*[i*257 for _ in range(3) for i in range(256)]);self.saved_gamma[a[0]]=raw;self.gamma[a[0]]=raw;self.store(a[1],raw);value=1
            elif op=='GFX_GAMMA_SET':need(a[0] in self.saved_gamma,'device ramp saved');self.gamma[a[0]]=self.buffer_data(a[2],1536);value=0x12345678;fields['void']=1
            elif op=='GFX_GAMMA_READ':self.store(a[1],self.gamma[a[0]]);value=0x12345678;fields['void']=1
            elif op=='GFX_GAMMA_RESTORE':self.gamma[a[0]]=self.saved_gamma.pop(a[0]);self.store(a[1],self.gamma[a[0]]);value=0x12345678;fields=dict(gamma_restored=1)
            elif op=='GFX_RUNTIME_CLOSE':need(not self.objects and not self.gdi,'no graphics lifetime on runtime close');self.factory=0;value=1;fields=dict(remaining_load_refs=0)
            elif op in ('GFX_DEBUG_MUTE','GFX_DEBUG_MUTE_RESOLVED'):self.debug_balance+=1 if a[-1] else -1;value=0x13579bdf
            elif op in ('GFX_MODULE_GET','GFX_MODULE_LOAD'):
                buf,offset=self.primitive.region(a[0],1);text=bytes(buf[offset:]).split(b'\0')[0];value=0x39000000 if text==b'd3d8.dll' else 0
            elif op=='GFX_PROC':need(a[0]==0x39000000,'declared D3D module');value=0x39100000
            elif op=='GFX_GET_OBJECT':
                need(a[0] in self.primitive.fonts and a[1]==60,'declared source font');self.store(a[2],struct.pack('<5i8B32s',0,0,0,0,700,0,0,0,1,5,0,0,0,b'FixedSys'));value=60
            elif op=='GFX_DC_CREATE':value=0x36000000+seq*4096;self.gdi[value]='dc';self.dc_selected[value]={}
            elif op=='GFX_DIB':
                need(a[0] in self.gdi,'owned symbolic DIB DC');value=0x36000000+seq*4096;self.gdi[value]='bitmap';self.dibs[value]=bytearray(256*256*4);self.store(a[3],struct.pack('<I',value+0x1000000))
            elif op in ('GFX_DIB_READ','GFX_DIB_WRITE'):
                p,off,buf,n=a;need(off+n<=len(self.dibs[p]),'bounded symbolic DIB')
                if op.endswith('READ'):self.store(buf,bytes(self.dibs[p][off:off+n]))
                else:self.dibs[p][off:off+n]=self.buffer_data(buf,n)
                value=n
            elif op=='GFX_SELECT':
                kind='bitmap' if a[1] in self.dibs else 'font';value=self.dc_selected[a[0]].get(kind,0x7777 if kind=='font' else 0x8888);self.dc_selected[a[0]][kind]=a[1]
            elif op=='GFX_FONT_INDIRECT':value=0x36000000+seq*4096;self.gdi[value]='font'
            elif op=='GFX_TEXT_EXTENT':self.store(a[3],struct.pack('<2I',9,16));value=1
            elif op=='GFX_TEXT_OUT':value=1 # Explicit blank symbolic raster, never a live glyph claim.
            elif op=='GFX_MULDIV':value=round(struct.unpack('<i',struct.pack('<I',a[0]))[0]*a[1]/a[2])&0xffffffff
            elif op=='GFX_DELETE_OBJECT':
                bitmap=a[0] in self.dibs
                if a[0] in self.primitive.fonts:del self.primitive.fonts[a[0]]
                else:self.gdi.pop(a[0])
                value=1;fields=dict(retirement_observed=1,deferred_delete=0,retirement_flush=1,object_type_after=0,object_bytes_after=0,retired_bitmaps_hex=struct.pack('<I',a[0]).hex() if bitmap else '-',retired_fonts_hex='-' if bitmap else struct.pack('<I',a[0]).hex())
            elif op=='GFX_DC_DELETE':self.gdi.pop(a[0]);self.dc_selected.pop(a[0]);value=1;fields=dict(retirement_observed=1,retirement_flush=1,object_type_after=0,retired_bitmaps_hex='-',retired_fonts_hex='-')
            elif op in ('GFX_BK_MODE','GFX_MAP_MODE'):value=1
            elif op in ('GFX_BK_COLOR','GFX_TEXT_COLOR','GFX_TEXT_ALIGN'):value=0
            else:raise ValueError('undeclared symbolic graphics operation '+op)
        self.deliveries[seq]=[f'R {seq} 0 101 {self.primitive.errors[0]} 1 {value} teb=4096 '+' '.join(k+'='+str(v) for k,v in fields.items())];return seq


def checks(report):
    from devtools.terminal_graphics_native import OPS,METHODS as NATIVE_METHODS
    need({k:{slot:name for slot,(name,_) in d.items()} for k,d in METHODS.items()}==NATIVE_METHODS,'fixed native/guest method ABI table')
    for q in report['native_trace']:
        if q['direction']=='request' and q['op'].startswith('GFX_'):
            need(q['op'] in OPS and len(q['args'])==OPS[q['op']],'exact graphics wire argument count '+q['op'])
    bad=[]
    original=dict(object=0x33000000,kind=11,vtable=0x33000100,owned_refs=2,group=0x33001000,method2=0x35000020)
    for name,patch in [('changed_vtable',dict(vtable=9)),('changed_parent',dict(group=9)),('wrong_kind',dict(kind=13)),('wrong_reference_count',dict(owned_refs=9))]:
        e=GraphicsEngine.__new__(GraphicsEngine);e.graphics={0x69000000:dict(native=original['object'],kind=11,refs=1,identity=original.copy())}
        try:e.graphics_interface(dict(original,**patch),11)
        except ValueError as exc:bad.append(dict(case=name,rejected=True,reason=str(exc)))
        else:raise ValueError('changed graphics identity admitted '+name)
    # A deferred DeleteObject success must retain its obligation until a later
    # source-linked census names that exact current generation.
    e=GraphicsEngine.__new__(GraphicsEngine);e.fonts={123:{}};e.graphics_fonts=set();e.bitmap_regions={456:dict(live=False)};e.pending_gdi={123,456}
    e.gdi_retirements(dict(retirement_flush=1,retired_fonts_hex='',retired_bitmaps_hex=''))
    need(e.pending_gdi=={123,456},'deferred GDI not falsely retired')
    e.gdi_retirements(dict(retirement_flush=1,retired_fonts_hex=struct.pack('<I',123).hex(),retired_bitmaps_hex=struct.pack('<I',456).hex()))
    need(not e.pending_gdi and not e.fonts and e.bitmap_regions[456]['retired'],'later actual census closes original obligation')
    for name,q in [('flush_failed',dict(retirement_flush=0,retired_fonts_hex='',retired_bitmaps_hex='')),('foreign_retirement',dict(retirement_flush=1,retired_fonts_hex=struct.pack('<I',999).hex(),retired_bitmaps_hex=''))]:
        try:e.gdi_retirements(q)
        except ValueError as exc:bad.append(dict(case=name,rejected=True,reason=str(exc)))
        else:raise ValueError('invalid retirement admitted')
    template=copy.deepcopy(report['callbacks'][0]['packet'])
    for name,change in [('callback_wrong_thread',dict(tid=999)),('callback_wrong_TEB',dict(teb=999)),('callback_wrong_parent',dict(parent_request=2)),('callback_wrong_depth',dict(depth=2))]:
        o=GraphicsOwner.__new__(GraphicsOwner);o.waiting=[1];o.requests={1:(0,'GFX_GAMMA_RESTORE')};o.events=[dict(event='READY',main_tid=101,main_teb=4096)]
        o.callback_packets=[];o.callback_active=[];o.trace=[];o.callback_handler=lambda p:(_ for _ in ()).throw(AssertionError('invalid callback executed'))
        row=dict(template,parent_request=1,parent_callback_id=0,callback_id=1,depth=1);row.update(change)
        try:o.consume_line('C '+' '.join(k+'='+('-' if v=='' else str(v))for k,v in row.items()))
        except ValueError as exc:bad.append(dict(case=name,rejected=True,reason=str(exc)))
        else:raise ValueError('invalid graphics callback admitted')
    return dict(native_wire_ABI_matches=True,deferred_GDI_receipts_required=True,rejections=bad,limitations='Synthetic identity/callback/retirement checks; no native OS result or device qualification.')


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',required=True);ap.add_argument('--stop',type=lambda s:int(s,0),default=0x413560);args=ap.parse_args()
    out=(ROOT/args.out).resolve();need(out.is_relative_to(ROOT/'.venv-audit') and not out.exists(),'fresh F graphics evidence')
    template=ROOT/'analysis/school-window-startup-trajectory-v3-20261020.json';need(base.sha(template.read_bytes())=='a5f30898f2add507e70277617838ad51e5328b56915c227460e3bc43f2afcd48','fixed creation template')
    e=GraphicsEngine();m=Model(e,json.loads(template.read_text())['cases'][0]);start=time.monotonic()
    report=dict(kind='symbolic_fullscreen_font_route',native_executed=False,desktop_used=False,ready_for_native=False,formal_acceptance=False,implementation=[base.identity(Path(__file__)),base.identity(ROOT/'devtools/terminal_graphics_platform.py')],capability_input=base.identity(ROOT/CAPS_SOURCE),symbolic_inputs='Old capability bytes explicitly reused as model input; fullscreen modes1024x768 formats22-25, successful methods,9x16 glyph metrics, blank raster, interface IDs and return bits are declared symbolic. No Windows observation.')
    try:
        begin_original_game(e,m,0x413450);game=e.reg('ECX');m.call('GFX_GATE',1)
        pointer=m.call('MEM_ALLOC',32)['result'];m.call('MEM_WRITE',pointer,'ab'*32);m.call('GFX_BASELINE',pointer);m.call('MEM_FREE',pointer)
        e.stop=args.stop;e.done[0]=False;e.drive();e.checkpoint('continuous_original_graphics_boundary')
        report['reached']=e.reg('EIP')==args.stop;report['GAME_published']=bool(e.word(0x7a49fc))
        report['forward_reached_before_input']=report['reached'] and args.stop==0x413560
        if report['reached'] and args.stop==0x413560:report['cleanup']=cleanup_before_input(e,m,game)
    except BaseException as exc:report.update(reached=False,failure=repr(exc))
    report.update(seconds=round(time.monotonic()-start,3),final=e.state(),API_calls=e.records,callbacks=e.callbacks,roots=e.roots,native_trace=m.trace,checkpoints=e.checkpoints,instruction_sites=[dict(pc=p,hex=e.image[p-0x400000:p-0x400000+n].hex(),count=c) for p,(n,c) in sorted(e.sites.items())],resource_summary=dict(graphics_references=sum(x['refs'] for x in m.objects.values()),graphics_objects=len(m.objects),GDI=len(m.gdi),gamma_pending=len(m.saved_gamma),state_blocks=len(m.tokens)),limits=dict(seconds=90,instructions=6000000,compressed_bytes=8*1024*1024),cleanup_qualified=False)
    if report['reached']:report['regressions']=checks(report)
    raw=gzip.compress(json.dumps(report,separators=(',',':')).encode(),mtime=0);need(len(raw)<8*1024*1024,'bounded compressed graphics evidence');out.write_bytes(raw)
    print(json.dumps(dict(output=base.identity(out),reached=report['reached'],failure=report.get('failure'),seconds=report['seconds'],instructions=e.count,pc=hex(e.reg('EIP')),last_API=e.records[-1]['name'] if e.records else None)))
    return 0 if report['reached'] else 1


if __name__=='__main__':raise SystemExit(main())
