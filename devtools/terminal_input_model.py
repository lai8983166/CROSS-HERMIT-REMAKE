"""One bounded symbolic original GAME publication and supplemental cleanup."""
from __future__ import annotations
import argparse,gzip,json,struct,time
from pathlib import Path
from devtools.terminal_graphics_model import Model as GraphicsModel,checks as graphics_checks,CAPS_SOURCE
from devtools.terminal_input_platform import InputEngine,InputOwner,METHODS,base,need,cleanup_after_publication
from devtools.terminal_input_native import OPS
from devtools.terminal_game_platform import begin_original_game

ROOT=base.ROOT
CURSOR=struct.pack('<9I',1,0x7777,200,100,0,0,1920,1080,123)

class Model(GraphicsModel,InputOwner):
    consume_line=InputOwner.consume_line
    def __init__(self,*args):
        super().__init__(*args);self.input_gate=0;self.input_baseline=False;self.input_instance=False;self.input_live={};self.input_module=False;self.input_cursor_dirty=False;self.input_restored=False;self.input_unacquires=0;self.input_releases=0
    def send(self,lane,op,*a):
        if not op.startswith('INPUT_'):
            seq=super().send(lane,op,*a)
            if op=='STATUS':self.deliveries[seq][-1]+=f' input_gate={self.input_gate} input_baseline={int(self.input_baseline)} input_instance={int(self.input_instance)} input_interfaces={len(self.input_live)} input_modules={int(self.input_module)} input_show_delta_bits=0 input_position_dirty={int(self.input_cursor_dirty)} input_unacquires={self.input_unacquires} input_releases={self.input_releases}'
            return seq
        self.check();need(lane==0 and op in OPS and len(a)==OPS[op],'fixed input MAIN wire ABI')
        self.seq+=1;seq=self.seq;self.requests[seq]=(0,op);self.trace.append(dict(direction='request',id=seq,lane=0,op=op,args=list(a)));fields={};value=0
        if op=='INPUT_GATE':self.input_gate=a[0];value=1
        elif op=='INPUT_BASELINE':need(self.buffer_data(a[0],32)==self.baseline and self.buffer_data(a[1],36)==CURSOR,'declared symbolic pre-device cursor');self.input_baseline=True;value=1
        else:
            need(self.input_gate and self.input_baseline,'symbolic explicit input gate')
            if op=='INPUT_INSTANCE_INFO':need(a[0]==self.engine.window_module,'original creator instance');self.input_instance=True;value=1;fields=dict(original_instance=a[0],helper_instance_substituted=0)
            elif op in ('INPUT_CREATE','INPUT_DEVICE'):
                if op=='INPUT_CREATE':need(self.input_instance and a[1:3]==(0x800,0x5cc1bc) and a[4]==0,'original input create');kind=20;out=a[3];parent=0;self.input_module=True
                else:need(a[0] in self.input_live and self.input_live[a[0]]['kind']==20 and a[3]==0,'original input factory');kind=21 if a[1]==0x5cc04c else 22;out=a[2];parent=a[0]
                p=0x3b000000+len(self.input_live)*4096;self.input_live[p]=dict(kind=kind,parent=parent,format=False,cooperative=False,acquired=False,unacquired=False)
                fields=dict(object=p,kind=kind,vtable=p+256,owned_refs=1,group=parent)
                fields.update({'method'+str(s):0x3c000000+kind*4096+s*16 for s in METHODS[kind]});self.store(out,struct.pack('<I',p))
            elif op=='INPUT_FORMAT':
                o=self.input_live[a[0]];need(a[1]==(0x5cac3c if o['kind']==21 else 0x5cae44),'exact original data format');o['format']=True
            elif op=='INPUT_COOPERATIVE':need(a[1]==self.hwnd and a[2]==6,'original cooperative flags');self.input_live[a[0]]['cooperative']=True
            elif op=='INPUT_PROPERTY':need(a[1]==2 and self.buffer_data(a[2],20)==struct.pack('<5I',20,16,0,0,1),'original mouse property')
            elif op=='INPUT_DEVICE_INFO':need(struct.unpack('<I',self.buffer_data(a[1],4))[0]==580,'complete original instance');self.store(a[1],struct.pack('<I',580)+bytes(576))
            elif op in ('INPUT_ACQUIRE','INPUT_UNACQUIRE'):
                o=self.input_live[a[0]];need(o['format'] and o['cooperative'],'configured original input');o['acquired']=op=='INPUT_ACQUIRE';o['unacquired']=not o['acquired'];self.input_unacquires+=int(op=='INPUT_UNACQUIRE')
            elif op=='INPUT_RELEASE':
                o=self.input_live[a[0]];need(o['unacquired'] if o['kind']!=20 else len(self.input_live)==1,'original Unacquire then device/factory Release');del self.input_live[a[0]];self.input_releases+=1;fields=dict(remaining_owned_refs=0,native_remaining_refs=0)
            elif op=='INPUT_CLIENT_TO_SCREEN':need(a[0]==self.hwnd and self.buffer_data(a[1],8)==struct.pack('<2I',512,384),'original fullscreen center');value=1
            elif op=='INPUT_CURSOR_POS':need(a==(512,384),'original converted center');self.input_cursor_dirty=True;self.input_restored=False;value=1
            elif op=='INPUT_METRIC':need(a[0] in (36,37,68,69),'declared metrics');value=4
            elif op=='INPUT_DOUBLE_CLICK':value=500
            elif op=='INPUT_CURSOR_RESTORE':need(not self.input_live,'input released before restore');self.input_cursor_dirty=False;self.input_restored=True;value=1;fields=dict(actual_readback=1,cursor_hex=CURSOR.hex())
            elif op=='INPUT_CLOSE':need(self.input_restored and not self.input_live and not self.input_cursor_dirty,'explicit cursor restore required');self.input_baseline=False;self.input_module=False;self.input_instance=False;value=1
            else:raise ValueError('unmodelled input operation '+op)
        self.deliveries[seq]=[f'R {seq} 0 101 {self.primitive.errors[0]} 1 {value} teb=4096 '+' '.join(k+'='+str(v)for k,v in fields.items())];return seq

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',required=True);a=ap.parse_args();out=(ROOT/a.out).resolve();need(out.is_relative_to(ROOT/'.venv-audit') and not out.exists(),'fresh bounded F input model')
    template=ROOT/'analysis/school-window-startup-trajectory-v3-20261020.json';need(base.sha(template.read_bytes())=='a5f30898f2add507e70277617838ad51e5328b56915c227460e3bc43f2afcd48','fixed creation template')
    e=InputEngine();m=Model(e,json.loads(template.read_text())['cases'][0]);m.engine=e;start=time.monotonic()
    report=dict(kind='symbolic_original_GAME_publication',native_executed=False,desktop_used=False,ready_for_native=False,formal_acceptance=False,implementation=[base.identity(ROOT/p)for p in ('devtools/terminal_input_model.py','devtools/terminal_input_platform.py','devtools/terminal_graphics_model.py','devtools/terminal_graphics_platform.py','devtools/terminal_input_native.py','devtools/terminal_input_native.inc')],capability_input=base.identity(ROOT/CAPS_SOURCE),symbolic_inputs='Graphics parent symbolic successful modes/caps/glyphs/blank raster; successful DirectInput HRESULTs, devices, metrics, complete580 zero-padded instance, cursor36 and module qualification. No Windows observation.')
    try:
        begin_original_game(e,m,0x413450);game=e.reg('ECX');m.call('GFX_GATE',1)
        token=m.call('MEM_ALLOC',32)['result'];m.call('MEM_WRITE',token,'ab'*32);m.call('GFX_BASELINE',token)
        m.call('INPUT_GATE',1);cursor=m.call('MEM_ALLOC',36)['result'];m.call('MEM_WRITE',cursor,CURSOR.hex());m.call('INPUT_BASELINE',token,cursor);m.call('MEM_FREE',cursor);m.call('MEM_FREE',token)
        e.stop=0x4506eb;e.done[0]=False;e.drive();e.checkpoint('original_GAME_publication_after_input')
        report['reached']=e.reg('EIP')==0x4506eb and e.word(0x7a49fc)==game and 0x4506e9 in e.sites
        need(report['reached'],'original successful GAME publication');report['published_GAME']=game;report['cleanup']=cleanup_after_publication(e,m,game)
    except BaseException as exc:report.update(reached=False,failure=repr(exc))
    report.update(seconds=round(time.monotonic()-start,3),instructions=e.count,final=e.state(),API_calls=e.records,callbacks=e.callbacks,roots=e.roots,native_trace=m.trace,checkpoints=e.checkpoints,instruction_sites=[dict(pc=p,hex=e.image[p-0x400000:p-0x400000+n].hex(),count=c)for p,(n,c)in sorted(e.sites.items())],limits=dict(seconds=90,instructions=6000000,compressed_bytes=8*1024*1024),native_cleanup_qualified=False,worker_created=False,wait_return=False,result_consumed=False)
    if report['reached']:report['graphics_regressions']=graphics_checks(report)
    raw=gzip.compress(json.dumps(report,separators=(',',':')).encode(),mtime=0);need(len(raw)<8*1024*1024,'bounded compressed input evidence');out.write_bytes(raw)
    print(json.dumps(dict(output=base.identity(out),reached=report['reached'],failure=report.get('failure'),seconds=report['seconds'],instructions=e.count,pc=hex(e.reg('EIP')),last_API=e.records[-1]['name'] if e.records else None)));return 0 if report['reached'] else 1

if __name__=='__main__':raise SystemExit(main())
