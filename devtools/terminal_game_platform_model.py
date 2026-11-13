"""Bounded symbolic post-window WinMain continuation; no native or desktop calls."""
import argparse
import copy
import gzip
import json
import struct
import time
from devtools.terminal_window_lifetime_model import Model as ParentModel
from devtools.terminal_game_platform import GameEngine,GameOwner,begin_original_game,cleanup_before_graphics,base,ROOT,need,CLASSES,QUERIES,METHODS


class Model(ParentModel,GameOwner):
    consume_line=GameOwner.consume_line
    def __init__(self,*args):
        super().__init__(*args)
        self.com_refs={};self.com_groups={};self.group_of={};self.audio_live=set();self.notifications={};self.apartment=0;self.game_gate=0
    def send(self,lane,op,*args):
        extra={'GAME_GATE','ShowWindow','UpdateWindow','GetWindowRect','GetClientRect','CoInitialize','InitCommonControlsEx',
            'CoCreateInstance','COM_QUERY','COM_RELEASE','MultiByteToWideChar','CoUninitialize','DC_INFO','DeleteDC',*(x[0] for d in METHODS.values() for x in d.values())}
        if op not in extra:
            seq=super().send(lane,op,*args)
            if op=='STATUS':
                self.deliveries[seq][-1]+=f' game_gate={self.game_gate} com_balance={self.apartment} com_interfaces={len(self.com_refs)} com_refs={sum(self.com_refs.values())} com_groups={len(self.com_groups)} audio_initialized={len(self.audio_live)} audio_pending_close={len(self.audio_live)} graph_notifications={len(self.notifications)} game_call_active=0'
            return seq
        self.check();need(lane==0,'symbolic current MAIN')
        self.seq+=1;seq=self.seq;self.requests[seq]=(0,op)
        self.trace.append(dict(direction='request',id=seq,lane=0,op=op,args=list(args)))
        result=1;fields={}
        if op=='GAME_GATE':
            if not args[0]:need(not any((self.apartment,self.com_refs,self.audio_live,self.notifications)),'symbolic platform gate only closes when empty')
            self.game_gate=args[0]
        elif op in ('GetWindowRect','GetClientRect'):
            data,offset=self.primitive.region(args[1],16)
            data[offset:offset+16]=struct.pack('<4i',*( (16,16,1040,784) if op=='GetWindowRect' else (0,0,1024,768)))
        elif op=='CoInitialize':need(args==(0,) and not self.apartment,'symbolic original COM arg');result=0;self.apartment+=1
        elif op=='ShowWindow':result=0 # Explicit prior-invisible model; zero is not failure.
        elif op=='InitCommonControlsEx':
            data,offset=self.primitive.region(args[0],8)
            need(bytes(data[offset:offset+8])==struct.pack('<II',8,0x800),'original common-control request')
        elif op in ('CoCreateInstance','COM_QUERY','DM_GET_DEFAULT_AUDIO_PATH'):
            kind=CLASSES[(args[0],args[3])] if op=='CoCreateInstance' else QUERIES[args[1]] if op=='COM_QUERY' else 3
            ptr=0x30000000+seq*0x1000
            self.com_refs[ptr]=1
            group=ptr if op=='CoCreateInstance' else self.group_of[args[0]]
            self.group_of[ptr]=group;self.com_groups[group]=self.com_groups.get(group,0)+1
            data,offset=self.primitive.region(args[-1],4);data[offset:offset+4]=struct.pack('<I',ptr)
            fields=dict(object=ptr,kind=kind,kind_mask=1<<kind,vtable=ptr+256,method0=0x31000000,method2=0x31000020,owned_refs=1,group=group)
            for index in METHODS[kind]:fields['method'+str(index)]=0x31000000+index*16
            result=0
        elif op=='MultiByteToWideChar':
            data,offset=self.primitive.region(args[2],1)
            text=bytes(data[offset:]).split(b'\0',1)[0].decode('ascii')+'\0'
            wide=text.encode('utf-16le');out,offset=self.primitive.region(args[4],args[5]*2)
            need(len(wide)<=args[5]*2,'bounded symbolic conversion');out[offset:offset+len(wide)]=wide;result=len(text)
        elif op=='CoUninitialize':
            need(self.apartment==1 and not any((self.com_refs,self.audio_live,self.notifications)),'modeled apartment tears down after owned COM')
            self.apartment=0;fields=dict(void=1,com_balance=0);result=0
        elif op=='DC_INFO':fields=dict(dc_retired=1,now_flush=1,now_type=0,now_font=0,now_gdi_error=0,now_gdi_count=0,baseline_gdi_count=0)
        elif op=='DeleteDC':
            need(args[0] in self.primitive.dcs,'modeled current DC')
            self.primitive.dcs.remove(args[0])
            fields=dict(dc_retired=1,before_flush=1,before_type=3,before_font=5678,after_flush=1,after_type=0,after_font=0,
                baseline_gdi_error=0,before_gdi_error=0,after_gdi_error=0,before_gdi_count=1,after_gdi_count=0,baseline_gdi_count=0)
        elif op.startswith(('DM_','DS_')) or op=='COM_RELEASE':
            need(args[0] in self.com_refs,'live symbolic native interface')
            if op=='DM_INIT_AUDIO':self.audio_live.add(args[0])
            elif op=='DM_CLOSE_DOWN':need(args[0] in self.audio_live,'initialized symbolic audio');self.audio_live.remove(args[0])
            elif op=='DS_SET_NOTIFY':
                if args[1]:self.notifications[args[0]]=args[1:]
                else:self.notifications.pop(args[0],None)
            elif op=='COM_RELEASE':
                need(args[0] not in self.audio_live and args[0] not in self.notifications,'source audio/notification cleanup before release')
                self.com_refs[args[0]]-=1
                fields=dict(released_owned_ref=1,remaining_owned_refs=self.com_refs[args[0]])
                group=self.group_of[args[0]];self.com_groups[group]-=1
                if not self.com_groups[group]:del self.com_groups[group]
                if not self.com_refs[args[0]]:del self.com_refs[args[0]];del self.group_of[args[0]]
            result=0
        self.deliveries[seq]=[f'R {seq} 0 101 {self.primitive.errors[0]} 1 {result} teb=4096 '+
            ' '.join(k+'='+str(v) for k,v in fields.items())]
        return seq


def checks(report):
    from devtools.terminal_game_native import OPS,original_contract
    original_contract()
    for q in report['native_trace']:
        if q['direction']=='request' and q['op'] in OPS:
            need(len(q['args'])==OPS[q['op']],'same typed native wire ABI '+q['op'])
    probe=GameEngine()
    row=dict(object=0x30001000,kind=4,kind_mask=1<<4,vtable=0x31001000,
        method0=0x32000000,method2=0x32000020,owned_refs=1,group=1)
    first=probe.interface(row,4)
    second=probe.interface(dict(row,kind=6,kind_mask=(1<<4)|(1<<6),owned_refs=2),6)
    need(first==second and probe.interfaces[first]['refs']==2 and probe.interfaces[first]['kinds']==[4,6],
         'one native identity can carry two original interface references')
    rejections=[]
    for label,patch in [('changed_vtable',dict(vtable=1)),('wrong_reference_count',dict(owned_refs=99))]:
        candidate=copy.copy(probe);candidate.interfaces=copy.deepcopy(probe.interfaces)
        try:candidate.interface(dict(row,kind=6,owned_refs=3,**patch) if 'owned_refs' not in patch else dict(row,kind=6,**patch),6)
        except ValueError as exc:rejections.append(dict(case=label,rejected=True,reason=str(exc)))
        else:raise ValueError('bad COM identity accepted: '+label)
    template=copy.deepcopy(report['callbacks'][0]['packet'])
    for label,change in [('wrong_callback_TID',dict(tid=999)),('wrong_callback_TEB',dict(teb=999)),
                         ('wrong_callback_parent',dict(parent_request=9)),('wrong_callback_depth',dict(depth=2))]:
        owner=GameOwner.__new__(GameOwner)
        owner.waiting=[1];owner.requests={1:(0,'InitCommonControlsEx')};owner.events=[dict(event='READY',main_tid=101,main_teb=4096)]
        owner.callback_packets=[];owner.callback_active=[];owner.trace=[]
        owner.callback_handler=lambda p:(_ for _ in ()).throw(AssertionError('invalid callback reached executor'))
        packet=dict(template,parent_request=1,parent_callback_id=0,callback_id=1,depth=1)
        packet.update(change)
        line='C '+' '.join(k+'='+('-' if v=='' else str(v)) for k,v in packet.items())
        try:owner.consume_line(line)
        except ValueError as exc:rejections.append(dict(case=label,rejected=True,reason=str(exc)))
        else:raise ValueError('invalid callback admitted: '+label)
    owner=GameOwner.__new__(GameOwner)
    owner.waiting=[1];owner.requests={1:(0,'InitCommonControlsEx')};owner.events=[dict(event='READY',main_tid=101,main_teb=4096)]
    owner.callback_packets=[];owner.callback_active=[];owner.trace=[];owner.callback_handler=lambda p:17
    owner.call=lambda op,*args:dict(result=1,callback_result=17)
    packet=dict(template,parent_request=1,parent_callback_id=0,callback_id=1,depth=1)
    owner.consume_line('C '+' '.join(k+'='+('-' if v=='' else str(v)) for k,v in packet.items()))
    need(len(owner.callback_packets)==1 and not owner.callback_active,'new common-controls callback parent retains envelope transport')
    return dict(wire_argument_counts_match_native=True,COM_alias_identity_preserved=True,
        common_controls_callback_transport=True,rejections=rejections,
        limits='Synthetic interface/envelope regression only. No native COM aliases, reentrancy or UI exercised.')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args()
    out=(ROOT/a.out).resolve();need(out.is_relative_to(ROOT/'.venv-audit') and not out.exists(),'fresh F bounded model output')
    source=ROOT/'analysis/school-window-startup-trajectory-v3-20261020.json'
    need(base.sha(source.read_bytes())=='a5f30898f2add507e70277617838ad51e5328b56915c227460e3bc43f2afcd48','fixed old creation template')
    e=GameEngine();m=Model(e,json.loads(source.read_text())['cases'][0]);start=time.monotonic()
    report=dict(native_executed=False,desktop_used=False,symbolic_only=True,formal_acceptance=False,
        original_source=base.identity(base.cold.SOURCE) if hasattr(base.cold,'SOURCE') else base.identity(ROOT/'analysis/hermit_game.exe'),
        engine=base.identity(ROOT/'devtools/terminal_game_platform.py'),model=base.identity(__file__),
        parent_creation_template=base.identity(source),original_roots=e.roots,callbacks=e.callbacks,API_calls=e.records,
        ready_for_native=False,complete_GAME_platform=False)
    try:
        report['outcome']=begin_original_game(e,m,0x413450)
        report['cleanup']=cleanup_before_graphics(e,m)
        report['bounded_route_reached']=True
    except BaseException as exc:
        report.update(bounded_route_reached=False,failure=repr(exc))
    report.update(seconds=round(time.monotonic()-start,3),final=e.state(),native_trace=m.trace,
        instruction_sites=[dict(pc=pc,hex=e.image[pc-0x400000:pc-0x400000+n].hex(),count=c) for pc,(n,c) in sorted(e.sites.items())],
        checkpoints=e.checkpoints,
        limits='Declared geometry/COM/creation model. No native lifetime, ShowWindow messages, audio/graphics/input or recovery is proven. No synthesized GAME pointer or result fields.')
    if report['bounded_route_reached']:report['regressions']=checks(report)
    raw=gzip.compress(json.dumps(report,separators=(',',':')).encode(),mtime=0)
    need(len(raw)<4*1024*1024,'4MiB model evidence budget');out.write_bytes(raw)
    print(json.dumps(dict(output=base.identity(out),reached=report['bounded_route_reached'],failure=report.get('failure'),seconds=report['seconds'],instructions=e.count)))
    return 0 if report['bounded_route_reached'] else 1


if __name__=='__main__':raise SystemExit(main())
