"""Bounded timing experiment: allow a held thread's kernel tail to settle.

The 1 ms delay is an observed sampling phase, not a proof of descheduling. All
ETL records remain retained and every data interval still needs the strict raw
QPC single-off-CPU check. Context acquisition remains outside that interval.
"""
from devtools import terminal_battle_wait_clock_armed as armed
from devtools.terminal_battle_wait_clock_armed import *

CLOCK_SHA='5e5b524cffba7aba76d7854a6bd187c6c932ff4174e070cc28294345d7b3a26e'
ARMED_SHA='3570690add8e4ca7a1ef530c9924f2be7fc2f7261235691e1b41ba6037ba8cf6'


def settled_template():
    need(identity(clock.__file__)['sha256']==CLOCK_SHA and identity(armed.__file__)['sha256']==ARMED_SHA,
         'fixed diagnostic parents')
    need(identity(v1.__file__)['sha256']==V1_SHA,'fixed original complete snapshot')
    tree=ast.parse(textwrap.dedent(inspect.getsource(v1.WaitWindow.snapshot)));counts=[0,0]
    class Settle(ast.NodeTransformer):
        def visit_Assign(self,node):
            if len(node.targets)==1 and isinstance(node.targets[0],ast.Name)and node.targets[0].id=='begin':
                need(ast.dump(node.value)==ast.dump(ast.parse('original.utc_now_ns(self.kernel)',mode='eval').body),'exact first data timestamp')
                counts[0]+=1
                return [*ast.parse('self.settle_held()').body,node]
            return self.generic_visit(node)
        def visit_Call(self,node):
            if ast.dump(node.func)==ast.dump(ast.parse('base.capture_tls',mode='eval').body):
                counts[1]+=1;node.func=ast.Name(id='_capture_tls',ctx=ast.Load())
            return self.generic_visit(node)
    tree=Settle().visit(tree);need(counts==[1,1],'one held settling phase and original TLS wrapper')
    ast.fix_missing_locations(tree);scope=dict(v1.__dict__)
    exec(compile(tree,__file__,'exec'),scope);return scope['snapshot']


SETTLED_TEMPLATE=settled_template()


class SettledWindow(armed.ArmedWindow):
    def settle_held(self):
        row=dict(qpc_begin=self.qpc(),requested_seconds=.001,original_contexts_already_acquired=True,
                 original_threads_still_suspended=True,input_submitted=False,ETL_records_discarded=False,
                 descheduling_assumed=False)
        self._settling=row
        time.sleep(.001)
        row['qpc_end']=self.qpc()

    def snapshot(self):
        with self.lock:
            row=clone(clock.ClockWindow.snapshot,TEMPLATE=SETTLED_TEMPLATE)(self)
            if row is not None:row['timing_diagnostic']['suspension_settling']=self._settling
            return row


class PreflightWindow(SettledWindow,armed.PreflightWindow):
    pass


def run(out):
    from devtools.native_input_isolation import require_qualified_guest
    qualification=require_qualified_guest();out=Path(out).resolve()
    need(out.parent==ROOT/'analysis'and out.name.endswith('.json.gz')and not out.exists(),'new settled short source')
    paths=[Path(__file__),Path(armed.__file__),Path(clock.__file__),Path(prepared.__file__),Path(v1.__file__),Path(original.__file__),
           ROOT/'devtools/terminal_wait_etw_probe.py',ROOT/'devtools/terminal_input_window.py']
    before=[identity(p)for p in paths];readiness=[]
    def ready(*args,**kwargs):readiness.append(args[2]);return clock.await_startup(*args,**kwargs)
    proxy=SimpleNamespace(**dict(original.__dict__,await_startup=ready))
    result=clone(v1.startup_probe,WaitWindow=PreflightWindow,original=proxy)(out,qualification)
    need(before==[identity(p)for p in paths],'all settled observer implementations unchanged')
    result.update(window_implementations=before,readiness_attempts=readiness,clock_diagnostic_only=True,long_capture_preflight_passed=False)
    raw=json.dumps(result,separators=(',',':')).encode();need(len(raw)<=8*1024*1024,'bounded complete settled source')
    packed=gzip.compress(raw,mtime=0);need(len(packed)<=2*1024*1024,'bounded packed settled source')
    with out.open('xb')as f:f.write(packed)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True);a=p.parse_args();r=run(a.out)
    print(json.dumps(dict(error=r.get('error'),snapshots=len(r.get('window_snapshots',[])),accepted=False)))
    raise SystemExit(1 if r.get('error')or r.get('lifecycle',{}).get('error')else 0)
