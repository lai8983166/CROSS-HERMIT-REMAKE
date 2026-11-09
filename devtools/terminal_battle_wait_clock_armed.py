"""Short QPC observer with an explicit no-input trace warm-up.

Keep all ETL records. Wait 50 ms before taking the first data snapshot so the
already-pending pre-trace syscall need not supply a snapshot. This is a sampling
start boundary, never a discarded-record rule or a successful wait assumption.
"""
from devtools import terminal_battle_wait_clock as clock
from devtools.terminal_battle_wait_clock import *


class ArmedWindow(clock.ClockWindow):
    def __init__(self,*args,**kwargs):
        self.arming=True
        super().__init__(*args,**kwargs)

    def begin(self):
        need(self.arming,'single explicit trace arming phase')
        super().begin()
        row=dict(qpc_begin=self.qpc(),minimum_seconds=.050,target_suspended_during_warmup=False,
                 input_submitted=False,ETL_records_discarded=False)
        self.result['trace_arming']=row
        time.sleep(.050)
        with self.lock:
            need(not self.thread_exit(),'actual worker remains live after no-input trace arming')
            row['qpc_end']=self.qpc();self.arming=False

    def poll(self):
        if self.arming:return
        return super().poll()


class PreflightWindow(ArmedWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs);self.prepare()

    def begin(self):
        from devtools.terminal_input_window import observe
        outcome={};record=dict(input_samples=[],input_submitted=False,original_deadline_seconds=11)
        def start():
            try:ArmedWindow.begin(self)
            except BaseException as exc:outcome['error']=repr(exc)
        worker=threading.Thread(target=start,name='armed-clock-trigger',daemon=False)
        def sample():
            value=dict(wall_time_ns=time.time_ns(),MAIN_event_hex=self.c.get(self.c.main+0x2C,8).hex())
            self.poll();return value
        self.result['trigger_concurrency_preflight']=record
        record['observation_begin_ns']=original.utc_now_ns(self.kernel);worker.start()
        try:observe(worker,sample,record)
        finally:
            worker.join(timeout=6);record['observation_end_ns']=original.utc_now_ns(self.kernel)
            record['trigger_error']=outcome.get('error')
        need(not worker.is_alive()and not outcome and record['input_window']['complete'],
             'actual armed trigger completes inside original 11 second observation')

    def drain(self,seconds=.150):
        need(seconds==.150,'one original short drain request')
        self.result['extended_short_sampling']=dict(original_drain_seconds=seconds,actual_drain_seconds=.900,
            maximum_window_seconds=3.0,maximum_snapshots=768,no_input=True)
        return super().drain(.900)


def run(out):
    from devtools.native_input_isolation import require_qualified_guest
    qualification=require_qualified_guest();out=Path(out).resolve()
    need(out.parent==ROOT/'analysis'and out.name.endswith('.json.gz')and not out.exists(),'new armed short source')
    paths=[Path(__file__),Path(clock.__file__),Path(prepared.__file__),Path(v1.__file__),Path(original.__file__),
           ROOT/'devtools/terminal_wait_etw_probe.py',ROOT/'devtools/terminal_input_window.py']
    before=[identity(p)for p in paths];readiness=[]
    def ready(*args,**kwargs):readiness.append(args[2]);return clock.await_startup(*args,**kwargs)
    proxy=SimpleNamespace(**dict(original.__dict__,await_startup=ready))
    result=clone(v1.startup_probe,WaitWindow=PreflightWindow,original=proxy)(out,qualification)
    need(before==[identity(p)for p in paths],'all armed observer implementations unchanged')
    result.update(window_implementations=before,readiness_attempts=readiness,clock_diagnostic_only=True,long_capture_preflight_passed=False)
    raw=json.dumps(result,separators=(',',':')).encode();need(len(raw)<=8*1024*1024,'bounded complete armed source')
    packed=gzip.compress(raw,mtime=0);need(len(packed)<=2*1024*1024,'bounded packed armed source')
    with out.open('xb')as f:f.write(packed)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=run(a.out)
    print(json.dumps(dict(error=r.get('error'),snapshots=len(r.get('window_snapshots',[])),accepted=False)))
    raise SystemExit(1 if r.get('error')or r.get('lifecycle',{}).get('error')else 0)
