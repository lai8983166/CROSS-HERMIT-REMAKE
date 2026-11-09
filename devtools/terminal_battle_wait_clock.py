"""Short original-worker timing diagnosis; raw QPC and UTC stay distinct.

Only timestamps are added to the frozen snapshot. The TLS call is bracketed to
locate observer-induced scheduling, without altering input or original state.
This is not a new successful battle source or a resource-cleanup proof.
"""
import ast
import inspect
import textwrap
from types import SimpleNamespace
from devtools import terminal_battle_wait_window_v2 as prepared
from devtools.terminal_battle_wait_window_v2 import *


def snapshot_template():
    need(identity(v1.__file__)['sha256']==V1_SHA,'fixed complete original snapshot')
    tree=ast.parse(textwrap.dedent(inspect.getsource(v1.WaitWindow.snapshot)));count=0
    class TLSCall(ast.NodeTransformer):
        def visit_Call(self,node):
            nonlocal count
            if ast.dump(node.func)==ast.dump(ast.parse('base.capture_tls',mode='eval').body):
                count+=1;node.func=ast.Name(id='_capture_tls',ctx=ast.Load())
            return self.generic_visit(node)
    tree=TLSCall().visit(tree);need(count==1,'exactly one original TLS observation wrapped')
    ast.fix_missing_locations(tree);scope=dict(v1.__dict__)
    exec(compile(tree,__file__,'exec'),scope);return scope['snapshot']


TEMPLATE=snapshot_template()


def current_candidate(candidate,tids,main_tid):
    if candidate is None:return None
    tid=word(bytes.fromhex(candidate['head_hex']),0x24)
    return candidate if tid in tids and tid!=main_tid else None


def await_startup(c,main_tid,result,kernel,seconds=5):
    from devtools import terminal_scene_owner as base,terminal_startup_handoff as startup
    deadline=time.monotonic()+seconds;previous=None;result['startup_readiness']=[]
    while time.monotonic()<deadline:
        with original.owned_frames(c,[main_tid])as frames:
            manager,nodes=startup.graph(c);tids=base.original.threads(c.pid)
            need(main_tid in tids and len(tids)==len(set(tids))and len(tids)<=256,'bounded actual process thread inventory')
            candidate=original.startup_candidate(nodes,startup.STARTUP)
            signature=([(n['pointer'],n['head_hex'])for n in nodes],tids)
            if signature!=previous:
                need(len(result['startup_readiness'])<32,'bounded raw readiness transitions')
                result['startup_readiness'].append(dict(utc_ns=original.utc_now_ns(kernel),
                    manager_pointer=c.main+0x64,manager_hex=manager.hex(),registered_nodes=nodes,
                    actual_process_threads=tids,scheduler_frame=frames[0],candidate_present_in_inventory=current_candidate(candidate,tids,main_tid)is not None))
                previous=signature
            candidate=current_candidate(candidate,tids,main_tid)
            if candidate:
                node=candidate['pointer'];tid=word(bytes.fromhex(candidate['head_hex']),0x24)
                # Keep MAIN held through the same-handle ownership check. Any
                # actual OpenThread/context/restore error remains a hard failure.
                with original.owned_frames(c,[tid])as worker_frames:
                    frame=worker_frames[0]
                    if {0x421F8A,0x56E183}<={r['return_va']for r in frame['chain']}:
                        result['startup_readiness_ancestor']=frame;return node,tid
        time.sleep(.010)
    raise ValueError('original registered worker did not become a current owned thread within 5 seconds')


class ClockWindow(prepared.WaitWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.kernel.QueryPerformanceCounter.argtypes=[C.POINTER(C.c_int64)]
        self.kernel.QueryPerformanceCounter.restype=W.BOOL
        self.kernel.QueryPerformanceFrequency.argtypes=[C.POINTER(C.c_int64)]
        self.kernel.QueryPerformanceFrequency.restype=W.BOOL
        frequency=C.c_int64();need(self.kernel.QueryPerformanceFrequency(C.byref(frequency))and frequency.value>0,'actual QPC frequency')
        self.result['snapshot_clock']=dict(frequency=frequency.value,clock='QueryPerformanceCounter raw ticks',
            UTC_retained_separately=True,clock_conversion_or_tolerance_applied=False)

    def qpc(self):
        value=C.c_int64();need(self.kernel.QueryPerformanceCounter(C.byref(value))and value.value>0,'actual QPC timestamp')
        return value.value

    def snapshot(self):
        from devtools import terminal_scene_owner as base
        clocks=[];tls_calls=[]
        def utc(kernel):
            before=self.qpc();value=original.utc_now_ns(kernel);after=self.qpc()
            clocks.append(dict(qpc_before=before,UTC_ns=value,qpc_after=after));return value
        def tls(*args):
            row=dict(qpc_begin=self.qpc(),completed=False);tls_calls.append(row)
            def selector(*arguments):
                interval=dict(qpc_begin=self.qpc());row['selector_query']=interval
                try:
                    answer=base.selector_entry(*arguments);interval['result']=int(answer);return answer
                finally:interval['qpc_end']=self.qpc()
            try:
                value=clone(base.capture_tls,selector_entry=selector)(*args)
                c=args[0];pointer=value['PTD']
                row['allocator_observation']=dict(PTD=pointer,header_pointer=pointer-0x20,header_hex=c.get(pointer-0x20,0x20).hex(),
                    globals=[dict(pointer=p,hex=c.get(p,4).hex())for p in (0x7619c0,0x762130,0x761980,0x80ab28,0x80ab2c,0x761bc0)])
                row['completed']=True;return value
            finally:row['qpc_end']=self.qpc()
        proxy=SimpleNamespace(**dict(original.__dict__,utc_now_ns=utc))
        with self.lock:
            row=clone(TEMPLATE,original=proxy,_capture_tls=tls)(self)
            if row is None and len(clocks)==1:
                self.result['unretained_non_wait_timing_samples']=self.result.get('unretained_non_wait_timing_samples',0)+1
                return None
            need(len(clocks)==2,'original saved snapshot has two actual timestamp calls')
            timing=dict(clock_reads=clocks,TLS_calls=tls_calls,
                data_interval_qpc=[clocks[0]['qpc_before'],clocks[1]['qpc_after']],
                includes_original_context_acquisition=False,
                context_acquired_while_same_handles_suspended=True)
            if row is not None:row['timing_diagnostic']=timing
            elif self.result['non_wait_samples'] and self.result['non_wait_samples'][-1]['snapshot_begin_ns']==clocks[0]['UTC_ns']:
                self.result['non_wait_samples'][-1]['timing_diagnostic']=timing
            return row


class PreflightWindow(ClockWindow,prepared.PreflightWindow):
    pass


def run(out):
    from devtools.native_input_isolation import require_qualified_guest
    qualification=require_qualified_guest();out=Path(out).resolve()
    need(out.parent==ROOT/'analysis' and out.name.endswith('.json.gz')and not out.exists(),'new bounded guest clock source')
    paths=[Path(__file__),Path(prepared.__file__),Path(v1.__file__),Path(original.__file__),
           ROOT/'devtools/terminal_wait_etw_probe.py',ROOT/'devtools/terminal_input_window.py']
    before=[identity(p)for p in paths]
    readiness=[]
    def await_recorded(*args,**kwargs):
        readiness.append(args[2]);return await_startup(*args,**kwargs)
    proxy=SimpleNamespace(**dict(original.__dict__,await_startup=await_recorded))
    result=clone(v1.startup_probe,WaitWindow=PreflightWindow,original=proxy)(out,qualification)
    result['readiness_attempts']=readiness
    need(before==[identity(p)for p in paths],'actual timing observer remains unchanged')
    result.update(window_implementations=before,clock_diagnostic_only=True,long_capture_preflight_passed=False)
    raw=json.dumps(result,separators=(',',':')).encode();need(len(raw)<=8*1024*1024,'bounded complete clock source')
    packed=gzip.compress(raw,mtime=0);need(len(packed)<=2*1024*1024,'bounded packed clock source')
    with out.open('xb')as f:f.write(packed)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=run(a.out)
    print(json.dumps(dict(error=r.get('error'),snapshots=len(r.get('window_snapshots',[])),accepted=False)))
    raise SystemExit(1 if r.get('error')or r.get('lifecycle',{}).get('error')else 0)
