"""Bounded original MAIN publication and GAME construction, without a window.

The WinMain prefix stops before window setup. An independent 412C70 factory
root completes 412E30, stopping before 413450. GAME is not published.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import struct
import time

from devtools import terminal_native_owner_probe as base

ROOT=base.ROOT
EXTRA={0x592310:('PathAddBackslashA',1),0x592294:('lstrcpyA',2),
       0x592218:('lstrcatA',2),0x5920a0:('CreateFontA',14),
       0x5920c4:('DeleteObject',1),0x5921cc:('GetLocalTime',1),
       0x5922ec:('GetSystemTime',1),0x592188:('GetTimeZoneInformation',1),
       0x592290:('WideCharToMultiByte',8),0x59234c:('GetDC',1),
       0x592060:('DeleteDC',1),0x592284:('QueryPerformanceCounter',1),
       0x592288:('QueryPerformanceFrequency',1)}
CHUNK=32768
SCENE_BYTES=0x1194f0
need=base.need


class SceneEngine(base.Engine):
    def __init__(self):
        super().__init__()
        self.slots.update(EXTRA);self.targets={self.word(s):s for s in self.slots}
        need(len(self.targets)==len(self.slots),'distinct immutable source API targets')
        for target in self.targets:
            if not any(a<=target<=b for a,b,_ in self.u.mem_regions()):self.u.mem_map(target&-4096,4096)
        self.md.topology();self.stop=None;self.stack=base.cold.old.STACK
        self.fonts={};self.checkpoints=[];self.host_writes=[];self.freed=[];self.dcs=set()

    def code(self,u,pc,n,_):
        if pc in (base.RETURN,self.stop) or pc in self.targets:u.emu_stop();return
        need(0x400000<=pc<0x592000 and self.read(pc,n)==self.image[pc-0x400000:pc-0x400000+n],'original source instruction '+hex(pc))
        self.count+=1;need(self.count<=2000000,'two million original instructions per case')
        if self.count%2048==0:self.owner.check()
        raw=self.read(pc,n);self.ih.update(struct.pack('<BI',self.lane,pc)+raw)
        self.sites[pc]=[n,self.sites.get(pc,[n,0])[1]+1]

    def put(self,p,b):
        super().put(p,b)
        self.host_writes.append(dict(pointer=p,bytes=len(b),sha256=base.sha(b)))

    def string(self,p,limit=260):
        data=bytearray()
        for i in range(limit):
            v=self.read(p+i,1);data+=v
            if v==b'\0':return bytes(data)
        raise ValueError('bounded original NUL string')

    def sync(self,p):
        g,r=self.owned(p)
        for offset in range(0,r['bytes'],CHUNK):
            data=self.read(g+offset,min(CHUNK,r['bytes']-offset))
            q=yield('MEM_WRITE',r['native']+offset,data.hex())
            need(q['result']==len(data),'complete chunked current allocation mirror')

    def api(self,slot):
        name,argc=self.slots[slot]
        need(name not in ('CreateThread','ResumeThread','WaitForSingleObject','ExitThread'),
             'construction preflight must not start a worker or wait')
        if name!='HeapAlloc' and slot not in EXTRA:
            before=set(self.allocations)
            yield from super().api(slot)
            if name=='HeapFree':self.freed.extend(sorted(before-set(self.allocations)))
            return
        sp=self.reg('ESP');ret=self.word(sp);a=[self.word(sp+4+4*i) for i in range(argc)]
        row=dict(lane=self.lane,name=name,slot=slot,target=self.word(slot),sp=sp,ret=ret,args=a,
                 before=self.state(),wire_start=len(self.owner.trace),outputs=[])
        self.records.append(row)
        ptd=self.thread_ptd[self.lane]
        if ptd and any(g<=ptd<g+r['bytes'] for g,r in self.allocations.items()):
            yield from self.sync(ptd)
            observed=yield('MEM_READ',self.native(ptd),116)
            need(observed['hex']==self.read(ptd,116).hex(),'current thread complete PTD mirror at added leaf')
            row['current_native_PTD']=dict(guest=ptd,native=self.native(ptd),hex=observed['hex'])
        def put(p,data):
            self.put(p,data);row['outputs'].append(dict(pointer=p,bytes=len(data),sha256=base.sha(data),hex=data.hex() if len(data)<=525 else None))
        if name=='HeapAlloc':
            need(a[0]==base.cold.HEAP_TOKEN and 0<a[2]<=2*1024*1024,'bounded original heap request')
            q=yield(name,self.heap,*a[1:]);native=q['result'];need(native,'real owned allocation')
            value=self.next;self.next+=0x200000
            self.u.mem_map(value,(a[2]+4095)&-4096);self.md.topology()
            for offset in range(0,a[2],CHUNK):
                n=min(CHUNK,a[2]-offset);q=yield('MEM_READ',native+offset,n)
                need(q['result']==n and len(bytes.fromhex(q['hex']))==n,'complete allocated native chunk')
                put(value+offset,bytes.fromhex(q['hex']))
            self.allocations[value]=dict(native=native,bytes=a[2])
            row['allocation']=dict(guest=value,native=native,bytes=a[2])
        elif name in ('GetDC','DeleteDC'):
            need(a==[0] if name=='GetDC' else a[0] in self.dcs,'owned screen DC only')
            q=yield(name,*a);value=q['result'];row['native_leaf']=q
            if name=='GetDC':need(value,'actual screen DC');self.dcs.add(value)
            # Original DeleteDC is not substituted for ReleaseDC, even on failure.
        elif name=='WideCharToMultiByte':
            need(a[6]==0 and 0<=a[5]<=4096,'bounded original conversion ABI')
            units=a[3]
            if units==0xffffffff:
                units=next((i+1 for i in range(512) if self.read(a[2]+i*2,2)==b'\0\0'),0)
            need(0<units<=512,'bounded original wide input')
            raw=self.read(a[2],units*2);q=yield('MEM_ALLOC',len(raw));src=q['result'];need(src,'wide input allocation')
            yield('MEM_WRITE',src,raw.hex());dst=0
            if a[5]:
                need(a[4],'original conversion output');q=yield('MEM_ALLOC',a[5]);dst=q['result'];need(dst,'multibyte output allocation')
                yield('MEM_WRITE',dst,self.read(a[4],a[5]).hex())
            used=0
            if a[7]:
                q=yield('MEM_ALLOC',4);used=q['result'];need(used,'used-default BOOL allocation')
                yield('MEM_WRITE',used,self.read(a[7],4).hex())
            q=yield(name,a[0],a[1],src,a[3],dst,a[5],0,used);value=q['result'];row['native_leaf']=q
            if used:
                q=yield('MEM_READ',used,4);put(a[7],bytes.fromhex(q['hex']))
                q=yield('MEM_FREE',used);need(q['result']==1,'used-default BOOL release')
            if dst:
                q=yield('MEM_READ',dst,a[5]);put(a[4],bytes.fromhex(q['hex']))
                q=yield('MEM_FREE',dst);need(q['result']==1,'conversion output release')
            q=yield('MEM_FREE',src);need(q['result']==1,'conversion input release')
        elif name in ('GetLocalTime','GetSystemTime','GetTimeZoneInformation','QueryPerformanceCounter','QueryPerformanceFrequency'):
            n=172 if name=='GetTimeZoneInformation' else (8 if name.startswith('QueryPerformance') else 16)
            q=yield('MEM_ALLOC',n);tmp=q['result'];need(tmp,'time output storage')
            yield('MEM_WRITE',tmp,self.read(a[0],n).hex())
            q=yield(name,tmp);value=q['result']
            need(value!=0xffffffff,'actual time API success')
            if name.startswith('QueryPerformance'):need(value==1,'actual performance clock success')
            q=yield('MEM_READ',tmp,n);put(a[0],bytes.fromhex(q['hex']))
            q=yield('MEM_FREE',tmp);need(q['result']==1,'time output storage release')
        elif name=='CreateFontA':
            face=self.string(a[13],64);q=yield('MEM_ALLOC',len(face));tmp=q['result'];need(tmp,'font face storage')
            yield('MEM_WRITE',tmp,face.hex());q=yield(name,*a[:13],tmp);value=q['result'];need(value,'actual original HFONT')
            self.fonts[value]=dict(args=a,face_hex=face.hex(),create_ret=ret)
            row['font']=dict(self.fonts[value]);q=yield('MEM_FREE',tmp);need(q['result']==1,'font face buffer released')
        elif name=='DeleteObject':
            need(a[0] in self.fonts,'only current source-created font')
            q=yield(name,*a);value=q['result'];need(value==1,'actual source font deleted')
            del self.fonts[a[0]]
        else:
            n=525 if name=='PathAddBackslashA' else 260
            q=yield('MEM_ALLOC',n);dst=q['result'];need(dst,'owned string target')
            yield('MEM_WRITE',dst,self.read(a[0],n).hex())
            src=None
            if len(a)==2:
                data=self.string(a[1]);q=yield('MEM_ALLOC',max(260,len(data)));src=q['result'];need(src,'owned string input')
                yield('MEM_WRITE',src,data.hex())
            q=yield((name,dst) if src is None else (name,dst,src))
            need(dst<=q['result']<dst+n,'native string result in current target')
            value=a[0]+q['result']-dst
            q=yield('MEM_READ',dst,n);put(a[0],bytes.fromhex(q['hex']))
            if src is not None:
                q=yield('MEM_FREE',src);need(q['result']==1,'string source release')
            q=yield('MEM_FREE',dst);need(q['result']==1,'string target release')
        self.reg('EAX',value);self.reg('ESP',sp+4+4*argc);self.reg('EIP',ret)
        row.update(value=value,after=self.state(),wire_end=len(self.owner.trace))

    def drive(self):
        # Single MAIN lane only in this constructor case; no cooperative worker.
        while not self.done[0] or self.pending:
            self.owner.check();self.lane=0;self.u.context_restore(self.ctx[0])
            if 0 in self.pending:
                i=self.pending[0]
                while i not in self.owner.responses:self.owner.poll(True)
                q=self.owner.responses.pop(i);del self.pending[0]
                try:req=self.generators[0].send(q)
                except StopIteration:del self.generators[0]
                else:self.pending[0]=self.owner.send(0,*req)
            else:
                self.u.emu_start(self.reg('EIP'),0,count=50000,timeout=250000)
                pc=self.reg('EIP')
                if pc in (base.RETURN,self.stop):self.done[0]=True
                elif pc in self.targets:
                    gen=self.api(self.targets[pc]);self.generators[0]=gen
                    self.pending[0]=self.owner.send(0,*next(gen))
                # A bounded instruction slice may end inside original code.
            self.ctx[0]=self.u.context_save()
        self.u.context_restore(self.ctx[0])

    def root(self,label,pc,args=(),receiver=0,callee=False,stop=None):
        need(self.done[0] and not self.pending,'quiescent declared root')
        self.u.context_restore(self.ctx[0]);sp=self.stack+0xf000
        raw=struct.pack('<'+'I'*(len(args)+1),base.RETURN,*args)
        declaration=dict(stack_pointer=sp,stack_before_hex=self.read(sp,len(raw)).hex(),stack_after_hex=raw.hex())
        self.put(sp,raw)
        for k,v in dict(EIP=pc,ESP=sp,ECX=receiver,EFLAGS=0x202).items():self.reg(k,v)
        row=dict(label=label,lane=0,entry=pc,args=list(args),receiver=receiver,callee=callee,stop_before=stop,
                 declared_independent_function_root=True,stack=declaration,before=self.state())
        self.roots.append(row);self.stop=stop;self.ctx[0]=self.u.context_save();self.done[0]=False
        self.drive();row['after']=self.state();self.stop=None
        if stop is None:need(self.reg('EIP')==base.RETURN and self.reg('ESP')==sp+4+(4*len(args) if callee else 0),'original natural return ABI')
        else:need(self.reg('EIP')==stop,'original boundary reached without executing it')
        return self.reg('EAX')

    def checkpoint(self,label):
        row=dict(label=label,state=self.state(),MAIN=self.word(0x7a4a00),GAME=self.word(0x7a49fc),scene=self.word(0x7a4174),
                 fonts={str(k):v for k,v in self.fonts.items()},allocations={str(k):v for k,v in self.allocations.items()})
        if row['scene'] and any(p<=row['scene']<p+a['bytes'] for p,a in self.allocations.items()):
            row['scene_header_hex']=self.read(row['scene'],0x68).hex()
            row['scene_complete_sha256']=base.sha(self.read(row['scene'],SCENE_BYTES))
        self.checkpoints.append(row);return row


def execute(g,owner):
    g.owner=owner
    g.root('original_heap_init',0x57b9d0,(1,))
    need(g.root('original_TLS_and_lock_init',0x5752d0)==1,'real main TLS ready')
    g.root('WinMain_entry_to_published_MAIN_and_empty_buckets',0x49dd70,(0,0,0,0),stop=0x49de23)
    main=g.word(0x7a4a00);need(main and g.word(main)==0x5986a0,'original MAIN publication and vtable')
    need(g.read(main+0x64,256)==bytes(256),'original scheduler bucket initialization')
    g.checkpoint('original_MAIN_published_before_window_setup')
    retained_stack=g.read(base.cold.old.STACK,65536)
    # Independent factory root; neither a guessed ancestor nor a published GAME.
    g.stack=base.WORK_STACK;output=g.stack+0x100
    g.put(output,struct.pack('<I',0xa5a5a5a5))
    g.root('original_412C70_factory_through_complete_412E30',0x412c70,(0,output,0,0),stop=0x413450)
    game=g.reg('ECX');game_raw,allocation=g.owned(game)
    need(game+0xba20<=game_raw+allocation['bytes'],'current original GAME allocation')
    need(g.word(0x7a49fc)==0 and g.word(output)==0xa5a5a5a5,'GAME not prematurely published')
    need(g.word(g.reg('ESP'))==0x412d06 and 0x412cc2 in g.sites,'constructor returned into original factory')
    need(0x413450 not in g.sites and 0x451080 not in g.sites and g.worker_handle is None,'no device initialization, scene or worker')
    dc=g.word(game+0xb208);need(dc in g.dcs,'original GAME stores actual current DC')
    need(g.read(base.cold.old.STACK,65536)==retained_stack,'pending WinMain stack retained')
    point=g.checkpoint('complete_GAME_constructor_before_platform_initialization')
    point.update(GAME_object=game,GAME_bytes=0xba20,GAME_sha256=base.sha(g.read(game,0xba20)),
                 GAME_DC=dc,GAME_drawing_gate=g.read(game+0xb28e,2).hex(),factory_output=g.word(output),
                 pending_factory_stack_sha256=base.sha(g.read(base.WORK_STACK,65536)))
    pending_factory=g.read(base.WORK_STACK,65536)
    g.stack=0x65600000;g.u.mem_map(g.stack,65536);g.md.topology()
    g.root('supplemental_original_GAME_destructor_and_free',0x412dd0,(1,),game,True)
    need(game_raw not in g.allocations,'original scalar deleting GAME destructor frees allocation')
    deletions=[r for r in g.records if r['name']=='DeleteDC']
    need(len(deletions)==1 and deletions[0]['args']==[dc],'original GAME DeleteDC attempted exactly once')
    point['original_DeleteDC_result']=deletions[0]['value']
    q=owner.call('ReleaseDC',0,dc);need(q['result']==1,'supplemental actual matching screen DC release')
    point['supplemental_ReleaseDC']=q;g.dcs.remove(dc)
    need(g.read(base.WORK_STACK,65536)==pending_factory,'pending GAME factory stack retained')
    need(g.read(base.cold.old.STACK,65536)==retained_stack,'pending WinMain stack still retained')
    g.root('original_MAIN_destructor',0x44fe60,receiver=main,callee=True)
    g.root('original_MAIN_allocation_free',0x428ad0,(main,))
    g.root('original_MAIN_PTD_free_and_TLS_clear',0x575450,(0,))
    g.root('original_TLS_and_lock_teardown',0x575360)
    g.root('original_heap_teardown',0x57ba60)
    need(not any((g.allocations,g.events,g.locks,g.fonts,g.dcs,g.heap)),'current owner resources explicitly empty')
    g.checkpoint('supplemental_cleanup_complete_globals_not_rewritten')
    status=owner.call('STATUS');need(owner.call('Shutdown')['result']==1,'normal native owner shutdown')
    need(owner.wait(min(1000,max(0,int((owner.deadline-time.monotonic())*1000))))==0,'native owner exited within budget')
    return status


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--execute',action='store_true')
    ap.add_argument('--helper',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    helper=(ROOT/a.helper).resolve();out=(ROOT/a.out).resolve()
    need(out.is_relative_to(ROOT) and helper.is_relative_to(ROOT) and not out.exists(),'fresh F workspace output')
    build=json.loads((helper.parent/'static-report.json').read_text(encoding='utf-8'))
    # The extension builder's pinned identities are verified before any launch.
    from devtools.terminal_scene_native_extension import generated_source
    for key in ('base_source','generator','generated_source','helper'):
        need(base.identity(ROOT/build[key]['path'])==build[key],'exact scene build '+key)
    need(base.identity(helper)==build['helper'],'requested executable is exact reviewed helper')
    need((ROOT/build['generated_source']['path']).read_bytes()==generated_source().encode(),'exact reviewed generated source')
    import pefile
    pe=pefile.PE(str(helper))
    need(pe.FILE_HEADER.Machine==0x14c and pe.OPTIONAL_HEADER.Subsystem==2,'x86 no-console helper')
    need({x.dll.lower() for x in pe.DIRECTORY_ENTRY_IMPORT}=={b'kernel32.dll',b'gdi32.dll',b'user32.dll',b'shlwapi.dll'},'exact non-window resource DLLs')
    gate_path=ROOT/'.venv-audit/terminal-scene-owner-build-v1-20261113/offline-route-v4.json'
    gate=json.loads(gate_path.read_text(encoding='utf-8'))
    need(gate['symbolic_only'] and not gate['native_executed'] and gate['route_closed'],'offline route must close before native launch')
    g=SceneEngine();report=dict(schema_version=1,kind='same_owner_original_MAIN_and_GAME_constructor_prefix',accepted=False,
        formal_acceptance=False,GAME_published=False,scene_constructed=False,full_GAME_factory_executed=False,worker_started=False,scene_callback_executed=False,cooperative_wait_executed=False,
        first_result_consumption=False,independent_full_replay=False,full_WinMain_executed=False,
        WinMain_to_scene_factory_continuous=False,desktop_used=False,screenshot=False,native_executed=False,
        original=base.identity(base.cold.base.SOURCE),implementation=base.identity(Path(__file__)),
        helper=base.identity(helper),build=build,offline_route=base.identity(gate_path),implementation_pins=base.implementation_pins(),
        declaration=g.declaration,initial=g.state(),roots=g.roots,API_calls=g.records,checkpoints=g.checkpoints)
    if a.execute:
        marker=helper.parent/'native-attempt.once'
        with marker.open('x',encoding='ascii') as f:f.write(json.dumps(dict(helper=base.identity(helper),utc=time.time())))
        owner=None
        try:
            owner=base.Owner.__new__(base.Owner);base.Owner.__init__(owner,helper,helper.parent)
            report['status']=execute(g,owner);report['accepted']=True
        except BaseException as e:
            report['failure']=repr(e);report['failure_guest']=dict(state=g.state(),pending=g.pending)
        finally:
            if owner:
                owner.finish();report.update(native_executed=owner.resumed,native_process_created=owner.started,
                    native_trace=owner.trace,events=owner.events,cleanup=owner.receipt)
                end=owner.receipt['exits'].get(str(owner.receipt['parent_pid']),{})
                if owner.receipt['forced'] or owner.expired or owner.receipt['errors'] or not owner.receipt['job_empty'] or not owner.receipt['handles_closed'] or end!={'wait':0,'code':0}:report['accepted']=False
            report.update(final=g.state(),instruction_sites=[dict(pc=p,hex=g.image[p-0x400000:p-0x400000+n].hex(),count=c) for p,(n,c) in sorted(g.sites.items())],adapter_writes=g.host_writes)
    else:report['offline_preparation_only']=True
    payload=gzip.compress(json.dumps(report,separators=(',',':')).encode(),mtime=0)
    need(len(payload)<16*1024*1024,'bounded 16MiB persistent evidence');out.write_bytes(payload)
    print(json.dumps(dict(out=str(out),bytes=len(payload),accepted=report['accepted'],native_executed=report['native_executed'],failure=report.get('failure'))))
    return 0 if not a.execute or report['accepted'] else 1


if __name__=='__main__':raise SystemExit(main())
