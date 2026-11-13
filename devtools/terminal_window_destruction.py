"""Original WM_CLOSE destruction adapter and explicitly symbolic offline case.

The native helper is never launched by this module. Legacy startup evidence has
real close/exit observations, but no complete destruction callback API stream.
The offline model below declares only three messages and symbolic OS results.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import struct
import time
import base64
import zlib
from devtools.terminal_window_callbacks import WindowOwner, base, need, MAX_CALLBACKS, MAX_DEPTH
from devtools.terminal_window_preparation import PreparedWindowEngine

ROOT=base.ROOT
DESTROY_SLOT=0x592398
NEW_PARENTS={'WINDOW_CLOSE','CB_DESTROY_WINDOW'}
PINS={'devtools/terminal_window_callbacks.py':'0fe16272b777a4f2e6475a940f7603b1ca02a40e4cd50545cab235dfc30b83c8',
      'devtools/terminal_window_preparation.py':'1eb8fb9cbac45e4a1caf7981efd995674b06e61d6a0010c93aaa39552a6372f8'}
for path,digest in PINS.items():
    need(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,'frozen callback parent '+path)


class DestructionOwner(WindowOwner):
    """Locally admit C frames of exactly two additional synchronous requests."""
    def consume_line(self,line):
        if not isinstance(line,str) or not line.startswith('C ') or not self.waiting:
            return super().consume_line(line)
        parent=self.waiting[-1]
        if self.requests.get(parent,(None,None))[1] not in NEW_PARENTS:
            return super().consume_line(line)
        need(len(line)<=66000,'bounded destruction callback packet')
        row={}
        for token in line.split()[1:]:
            key,value=token.split('=',1);need(key not in row,'unique destruction callback field')
            if value=='-' and key.endswith('_hex'):value=''
            row[key]=int(value) if value.isdecimal() and not key.endswith('_hex') else value
        required={'callback_id','parent_request','parent_callback_id','depth','lane','tid','teb','guest_entry',
                  'hwnd','message','wParam','lParam','data_kind','data_bytes','data_hex','last_error',
                  'tls_slot','tls_value','tls_tracked_value','tls_error','ptd_bytes','ptd_hex'}
        need(required<=row.keys(),'complete destruction callback envelope')
        need(all(isinstance(row[k],int) and 0<=row[k]<=0xffffffff
                 for k in required-{'data_kind','data_hex','ptd_hex'}),'destruction callback uint32 fields')
        lane,op=self.requests[parent]
        need(row['parent_request']==parent and row['lane']==lane==0,'exact pending MAIN destruction request')
        ready=next(e for e in self.events if e['event']=='READY')
        need((row['tid'],row['teb'])==(ready['main_tid'],ready['main_teb']),'destruction callback real MAIN identity')
        need(row['callback_id']==len(self.callback_packets)+1<=MAX_CALLBACKS and
             row['depth']==len(self.callback_active)+1<=MAX_DEPTH and
             row['parent_callback_id']==(self.callback_active[-1] if self.callback_active else 0),'bounded destruction callback ancestry')
        if op=='WINDOW_CLOSE':
            need(row['message']==16 and row['wParam']==row['lParam']==0 and not self.callback_active,
                 'owned close request enters original WM_CLOSE only')
        else:
            need(self.callback_active,'original DestroyWindow nested inside WM_CLOSE')
        need(self.callback_handler is not None,'original destruction executor installed')
        self.trace.append(dict(direction='callback',**row));self.callback_packets.append(row);self.callback_active.append(row['callback_id'])
        try:
            value=self.callback_handler(row)
            reply=self.call('CB_RETURN',row['callback_id'],value)
            need(reply['result']==1 and reply['callback_result']==value,'exact original destruction callback return')
        finally:self.callback_active.pop()


class DestructionEngine(PreparedWindowEngine):
    def __init__(self):
        super().__init__();self.window_closed=False
        self.slots[DESTROY_SLOT]=('DestroyWindow',1)
        self.targets={self.word(slot):slot for slot in self.slots}
        need(len(self.targets)==len(self.slots),'unique original DestroyWindow import')
        target=self.word(DESTROY_SLOT)
        if not any(a<=target<=b for a,b,_ in self.u.mem_regions()):self.u.mem_map(target&-4096,4096)
        need(not 0x400000<=target<0x9b4000,'external DestroyWindow import landing')
        self.put(target,b'\xc3');self.md.topology()

    def api(self,slot):
        if slot!=DESTROY_SLOT:
            yield from super().api(slot);return
        need(self.frames and self.lane==0,'DestroyWindow is an original callback leaf')
        frame=self.frames[-1];packet=frame['packet'];sp=self.reg('ESP');ret=self.word(sp);hwnd=self.word(sp+4)
        need(packet['message']==16 and packet['wParam']==packet['lParam']==0 and
             hwnd==packet['hwnd']==self.window_handle and ret==0x450f74,'exact original450F6E DestroyWindow frame')
        row=dict(name='DestroyWindow',slot=slot,sp=sp,ret=ret,args=[hwnd],callback_id=packet['callback_id'],
                 before=self.state(),wire_start=len(self.owner.trace))
        self.records.append(row);frame['API_calls'].append(row)
        reply=yield('CB_DESTROY_WINDOW',packet['callback_id'],hwnd)
        need(reply['result']==1 and reply['is_window_after']==0 and reply['ncdestroy_observed']==1,
             'actual original DestroyWindow succeeds and native HWND is invalid')
        self.reg('EAX',reply['result']);self.reg('ESP',sp+8);self.reg('EIP',ret)
        row.update(native_leaf=reply,value=reply['result'],after=self.state(),wire_end=len(self.owner.trace))

    def assert_closed(self,reply):
        need(not self.frames and not self.owner.callback_active and not self.window_closed,'completed original close request')
        need(reply['is_window_after']==0 and reply['ncdestroy_observed']==reply['quit_posted']==reply['property_removed']==1,
             'native complete close lifetime observations')
        destroy=[r for r in self.records if r['name']=='DestroyWindow']
        quit_calls=[r for r in self.records if r['name']=='PostQuitMessage']
        removed=[r for r in self.records if r['name']=='RemovePropA']
        need(len(destroy)==len(quit_calls)==len(removed)==1,'one original destroy/quit/property removal sequence')
        need(quit_calls[0]['ret']==0x450f8a and removed[0]['ret']==0x42495e,'original close cleanup call sites')
        need(removed[0]['native_leaf']['result']==self.window_owner and removed[0]['native_leaf']['observed_property']==0,
             'actual original CPP_CLASS owner removed')
        need(any(c['packet']['message']==130 for c in self.callbacks),'original nonclient destruction callback received')
        # Original4248E0 does not clear MAIN+4 or7A0BB4. Keep those stale values
        # as original state; supplemental MAIN cleanup must not fake publication.
        self.window_closed=True


def source_contract():
    from capstone import Cs,CS_ARCH_X86,CS_MODE_32
    path=ROOT/'analysis/hermit_game.exe';raw=path.read_bytes()
    need(base.sha(raw)=='588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005','fixed original image')
    checks={0x450f6e:('call','dword ptr [0x592398]'),0x450f84:('call','dword ptr [0x59239c]'),
            0x424a30:('call','0x4248e0'),0x424958:('call','dword ptr [0x5923e4]'),
            0x424914:('je','0x42494a'),0x42493d:('call','dword ptr [0x5923f0]')}
    md=Cs(CS_ARCH_X86,CS_MODE_32);proof=[]
    for pc,wanted in checks.items():
        i=next(md.disasm(raw[pc-0x400000:pc-0x400000+16],pc));need((i.mnemonic,i.op_str)==wanted,'original destruction source '+hex(pc))
        proof.append(dict(va=hex(pc),hex=i.bytes.hex(),mnemonic=i.mnemonic,operands=i.op_str))
    return dict(image=base.identity(path),instructions=proof,
        subclassed_WNDPROC_branch='If MAIN+8 is nonzero,42493D requires original SetWindowLongA restoration. This narrow original-class route requires MAIN+8==0.',
        global_cleanup='4248E0 removes CPP_CLASS without clearing MAIN+4 or global7A0BB4.',
        legacy_observation=base.identity(ROOT/'analysis/school-startup-lifetime-native-v3-20261020.json'),
        legacy_scope='Two real original WM_CLOSE/exit observations; no complete destruction callback/API return stream available.')


class SymbolicCloseOwner(DestructionOwner):
    """Declared Win32 message/result model. Never a native owner or old replay."""
    def __init__(self,engine):
        self.engine=engine;self.waiting=[];self.callback_packets=[];self.callback_active=[]
        self.trace=[];self.responses={};self.requests={};self.seq=0;self.deliveries={}
        self.events=[dict(event='READY',main_tid=123,main_teb=456)];self.callback_handler=engine.callback
        self.property=engine.window_owner;self.destroyed=False;self.quit=False;self.next_callback=0
        self.deadline=time.monotonic()+15
    def check(self):need(time.monotonic()<self.deadline,'15second offline destruction model')
    def packet(self,message,parent,cid,parentcid,depth):
        return dict(callback_id=cid,parent_request=parent,parent_callback_id=parentcid,depth=depth,
            lane=0,tid=123,teb=456,guest_entry=0x424980,hwnd=self.engine.window_handle,message=message,
            wParam=0,lParam=0,last_error=0,data_kind='opaque',data_bytes=0,data_hex='',
            tls_slot=0xffffffff,tls_value=0,tls_tracked_value=0,tls_error=0,ptd_bytes=0,ptd_hex='')
    @staticmethod
    def callback_line(row):return 'C '+' '.join(k+'='+('-' if v=='' else str(v)) for k,v in row.items())
    def send(self,lane,op,*args):
        self.check();need(lane==0,'symbolic MAIN only');self.seq+=1;seq=self.seq
        self.requests[seq]=(lane,op);self.trace.append(dict(direction='request',id=seq,lane=lane,op=op,args=list(args)))
        cid=self.callback_active[-1] if self.callback_active else 0;children=[];reply=dict(result=0,last_error=0)
        if op=='WINDOW_CLOSE':
            need(not cid and args==(self.engine.window_handle,),'declared symbolic close input')
            children=[self.packet(16,seq,1,0,1)];reply.update(is_window_after=0,ncdestroy_observed=1,quit_posted=1,property_removed=1)
        else:
            need(cid and args[0]==cid,'symbolic active callback')
            if op=='CB_DESTROY_WINDOW':
                need(cid==1 and args==(1,self.engine.window_handle),'original symbolic DestroyWindow frame')
                children=[self.packet(2,seq,2,1,2),self.packet(130,seq,3,1,2)]
                self.destroyed=True;reply.update(result=1,is_window_after=0,ncdestroy_observed=1)
            elif op=='CB_GET_PROP':reply['result']=self.property
            elif op=='CB_GET_LONG':need(args[2]==4,'unsubclassed original model');reply['result']=0
            elif op=='CB_POST_QUIT':need(cid==2 and args[1]==0,'original symbolic quit');self.quit=True;reply['quit_posted']=1
            elif op=='CB_REMOVE_PROP':need(cid==2,'original symbolic remove');reply.update(result=self.property,observed_property=0);self.property=0
            elif op=='CB_DEFAULT':need(cid==3 and args==(3,self.engine.window_handle,130,0,0),'original symbolic nonclient default');reply.update(before_hex='',after_hex='')
            elif op=='CB_RETURN':reply.update(result=1,callback_result=args[1])
            else:raise ValueError('unadmitted symbolic destruction leaf '+op)
            reply['callback_id']=cid
        rows=[self.callback_line(c) for c in children]
        extra={k:v for k,v in reply.items() if k not in ('result','last_error')};extra['teb']=456
        rows.append('R '+' '.join(map(str,(seq,0,123,reply['last_error'],1,reply['result'])))+' '+
                    ' '.join(k+'='+('-' if v=='' else str(v)) for k,v in extra.items()))
        self.deliveries[seq]=rows;return seq
    def poll(self,block=False):
        self.check();seq=self.waiting[-1];need(self.deliveries[seq],'symbolic stream not exhausted')
        self.consume_line(self.deliveries[seq].pop(0))


def model_case(case):
    engine=DestructionEngine();block=case['hwnd_publication']['state']['guarded_owner']
    raw=zlib.decompress(base64.b64decode(block['zlib_base64']))
    need(len(raw)==block['bytes'] and base.sha(raw)==block['sha256'],'frozen created MAIN input bytes')
    engine.u.mem_map(0x1ffff000,0x4000);engine.md.topology();engine.put(0x1ffff000,raw)
    engine.allocations[0x20000000]=dict(native=0,bytes=0x1110)
    hwnd=case['creation_result']['result'];module=case['creation']['args'][10]
    engine.bind_window(0x20000000,module,hwnd)
    need(engine.word(0x20000004)==hwnd and engine.word(0x20000008)==0,'original unsubclassed created MAIN')
    for k,v in case['hwnd_publication']['cpu'].items():engine.reg(k,v)
    owner=SymbolicCloseOwner(engine);engine.owner=owner
    response=owner.call('WINDOW_CLOSE',hwnd);engine.assert_closed(response)
    need(owner.destroyed and owner.quit and not owner.property and not owner.requests and not owner.callback_active and not engine.frames,'symbolic close sequence complete')
    need(engine.word(0x20000004)==hwnd and engine.word(0x20000008)==0,'original destruction preserves MAIN window fields')
    need(all(r['restored_caller']['cpu']==r['suspended_caller']['cpu'] for r in engine.callbacks),'fullCPU57 destruction caller restoration')
    return dict(fill=case['fill'],native_executed=False,symbolic_only=True,old_native_results_replayed=False,
        declared_messages=[16,2,130],callbacks=len(engine.callbacks),max_depth=2,original_instructions=engine.count,
        original_API_sequence=[dict(name=x['name'],ret=hex(x['ret']),args=x['args'],value=x['value']) for x in engine.records],
        original_MAIN_HWND_retained=True,CPU57_restored=True,source_instruction_sha256=engine.ih.hexdigest(),
        callback_records=engine.callbacks,normal_native_window_cleanup_proven=False)


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--out',required=True);args=ap.parse_args()
    path=(ROOT/args.out).resolve();need(path.is_relative_to(ROOT) and not path.exists(),'fresh offline report')
    parent=ROOT/'analysis/school-window-startup-trajectory-v3-20261020.json';data=parent.read_bytes()
    need(base.sha(data)=='a5f30898f2add507e70277617838ad51e5328b56915c227460e3bc43f2afcd48','fixed creation source input')
    cases=[model_case(c) for c in json.loads(data)['cases']]
    report=dict(kind='original_window_destruction_symbolic_bounded_model',native_executed=False,desktop_used=False,
        formal_acceptance=False,actual_destruction_unverified=True,implementation=base.identity(Path(__file__)),
        source_contract=source_contract(),parent_creation_source=base.identity(parent),cases=cases,
        limits=['Declared minimal3-message model and symbolic platform results, not captured native destruction.',
                'Actual DestroyWindow can deliver additional messages; unsupported APIs must reject.',
                'Class/module unregistration and MAIN/PTD/CRT cleanup are separate supplemental roots, not original WinMain return.'])
    path.write_bytes(gzip.compress(json.dumps(report,separators=(',',':')).encode(),mtime=0))
    print(json.dumps(dict(out=base.identity(path),cases=[{k:v for k,v in c.items() if k!='callback_records'} for c in cases])))


if __name__=='__main__':main()
