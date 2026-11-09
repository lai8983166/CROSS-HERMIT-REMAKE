"""Observe both complete WOW64 contexts on the same held original handles.

No kernel scheduling is inferred from suspension or equal endpoint registers.
The whole acquisition and data interval is separately checked against raw ETW.
This finite startup observer does not claim continuous instructions or cleanup.
"""
from devtools import terminal_battle_wait_clock_settled as settled
from devtools.terminal_battle_wait_clock_settled import *

OWNED_SHA='9d7aff0b2f19796902a3b4973a0a48bea0162c89501029e45b45f5cfdb0926b0'
SETTLED_SHA='a2ea64f5e85da0f99160ff085d4f234606f3ffb81357e3e23b4d44fa0d8276cf'


@contextmanager
def observed_owned_frames(c,thread_ids,record,qpc,backend=None):
    need(identity(original.__file__)['sha256']==OWNED_SHA,'fixed same-handle context owner')
    if backend is None:
        from devtools import terminal_scene_owner as backend
    api=backend.original;handles={};phase='before'
    record.update(qpc_begin=qpc(),threads=[],operations=[],complete=False)
    def key(h):return int(getattr(h,'value',h)or 0)
    def opened(access,inherit,tid):
        h=api.opent(access,inherit,tid)
        if h:
            row=dict(tid=tid,handle=key(h),contexts=[]);handles[key(h)]=row;record['threads'].append(row)
        return h
    def operation(name,function,h):
        item=dict(action=name,handle=key(h),qpc_begin=qpc());record['operations'].append(item)
        try:item['result']=int(function(h));return item['result']
        finally:item['qpc_end']=qpc()
    def ctx(h,address):
        item=dict(phase=phase,qpc_begin=qpc());handles[key(h)]['contexts'].append(item)
        try:
            item['result']=int(api.ctx(h,address))
            if item['result']:item['raw_hex']=C.string_at(address,716).hex()
            return item['result']
        finally:item['qpc_end']=qpc()
    proxy_api=SimpleNamespace(**dict(api.__dict__,opent=opened,ctx=ctx,
        suspend=lambda h:operation('suspend',api.suspend,h),
        resume=lambda h:operation('resume',api.resume,h),close=lambda h:operation('close',api.close,h)))
    proxy=SimpleNamespace(**dict(backend.__dict__,original=proxy_api))
    try:
        with original.owned_frames(c,thread_ids,proxy)as frames:
            for frame,row in zip(frames,record['threads']):
                need(frame['tid']==row['tid']and frame['context_hex']==row['contexts'][0]['raw_hex'],
                     'original raw context returned by the same intercepted call')
                row['owner_verified_before_suspend']=frame['owner_verified_before_suspend']
                row['previous_suspend_count']=frame['previous_suspend_count']
            record['data_scope_begin_qpc']=qpc()
            yield frames
            record['data_scope_end_qpc']=qpc();phase='after'
            for row in record['threads']:
                storage=C.create_string_buffer(736);at=(C.addressof(storage)+15)&~15
                C.memset(at,0,716);C.c_uint32.from_address(at).value=0x1003f
                api.check(ctx(row['handle'],at),'read complete ending context on same held handle')
                row['all_716_bytes_equal']=row['contexts'][0]['raw_hex']==row['contexts'][1]['raw_hex']
        record['complete']=True
    except BaseException as exc:
        record['error']=repr(exc);raise
    finally:record['qpc_end']=qpc()


class ContextWindow(settled.SettledWindow):
    def snapshot(self):
        need(identity(settled.__file__)['sha256']==SETTLED_SHA,'fixed held settling observer')
        with self.lock:
            attempts=self.result.setdefault('context_attempts',[])
            need(len(attempts)<MAX_SNAPSHOTS+18,'bounded all context attempts; no truncation')
            record=dict(index=len(attempts));attempts.append(record)
            def held(c,tids,backend=None):return observed_owned_frames(c,tids,record,self.qpc,backend)
            proxy=SimpleNamespace(**dict(original.__dict__,owned_frames=held))
            count=len(self.result['non_wait_samples'])
            row=clone(clock.ClockWindow.snapshot,TEMPLATE=settled.SETTLED_TEMPLATE,original=proxy)(self)
            # Include the actual settling record even for non-wait attempts.
            record['settling']=self._settling
            if row is not None:
                row['context_attempt_index']=record['index']
                row['timing_diagnostic']['suspension_settling']=self._settling
            elif len(self.result['non_wait_samples'])>count:
                self.result['non_wait_samples'][-1]['context_attempt_index']=record['index']
            return row


class PreflightWindow(ContextWindow,armed.PreflightWindow):
    pass


def run(out):
    from devtools.native_input_isolation import require_qualified_guest
    qualification=require_qualified_guest();out=Path(out).resolve()
    need(out.parent==ROOT/'analysis'and out.name.endswith('.json.gz')and not out.exists(),'new bounded context source')
    paths=[Path(__file__),Path(settled.__file__),Path(armed.__file__),Path(clock.__file__),Path(prepared.__file__),
        Path(v1.__file__),Path(original.__file__),ROOT/'devtools/terminal_wait_etw_probe.py',ROOT/'devtools/terminal_input_window.py']
    before=[identity(p)for p in paths];readiness=[]
    def ready(*args,**kwargs):readiness.append(args[2]);return clock.await_startup(*args,**kwargs)
    proxy=SimpleNamespace(**dict(original.__dict__,await_startup=ready))
    result=clone(v1.startup_probe,WaitWindow=PreflightWindow,original=proxy)(out,qualification)
    need(before==[identity(p)for p in paths],'all context observer implementations unchanged')
    result.update(window_implementations=before,readiness_attempts=readiness,clock_diagnostic_only=True,
                  long_capture_preflight_passed=False,full_context_observation_diagnostic_only=True)
    raw=json.dumps(result,separators=(',',':')).encode();need(len(raw)<=8*1024*1024,'bounded complete context source')
    packed=gzip.compress(raw,mtime=0);need(len(packed)<=2*1024*1024,'bounded packed context source')
    with out.open('xb')as f:f.write(packed)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=run(a.out)
    print(json.dumps(dict(error=r.get('error'),snapshots=len(r.get('window_snapshots',[])),accepted=False)))
    raise SystemExit(1 if r.get('error')or r.get('lifecycle',{}).get('error')else 0)
