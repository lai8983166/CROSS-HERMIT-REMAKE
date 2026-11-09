"""Prepare immutable PE/export work before the original bounded input window.

The original begin function is split at its fresh live-owner snapshot. No input
deadline is increased. Live code/IAT/TLS bytes and current ownership are checked
again at the real trigger; the original event/duplicate/ETW start tail is intact.
"""
import ast
import copy
import inspect
import textwrap
import threading
from devtools import terminal_battle_wait_window as v1
from devtools.terminal_battle_wait_window import *

V1_SHA='efedb67200d4ae03a2437d88b55c3a0015913f227e8e74e6fa7f68d4aa46750b'


def split_original_begin():
    need(identity(v1.__file__)['sha256']==V1_SHA,'exact fixed original wait-window implementation')
    tree=ast.parse(textwrap.dedent(inspect.getsource(v1.WaitWindow.begin)))
    function=tree.body[0];scope=function.body[-1]
    need(isinstance(scope,ast.With) and len(scope.items)==1,'one original begin lock scope')
    expected=ast.parse("r['before']=self.snapshot()").body[0]
    positions=[i for i,node in enumerate(scope.body)if ast.dump(node)==ast.dump(expected)]
    need(len(positions)==1,'one exact fresh original owner-snapshot boundary')
    index=positions[0];prefix=scope.body[:3]
    need(ast.dump(ast.Module(body=prefix,type_ignores=[]))==ast.dump(ast.parse(
        "need(not self.active and not self.finished,'one original input-triggered trace only')\nc=self.c\nr=self.result")),
        'unchanged original start guard and bindings')
    result=[]
    for name,body in (('_prepare_original',scope.body[:index]),('_begin_original',prefix+scope.body[index:])):
        part=copy.deepcopy(tree);part.body[0].name=name;part.body[0].body[-1].body=copy.deepcopy(body)
        ast.fix_missing_locations(part);namespace=dict(v1.__dict__)
        exec(compile(part,v1.__file__,'exec'),namespace);result.append(namespace[name])
    return tuple(result)


_prepare_original,_begin_original=split_original_begin()


class WaitWindow(v1.WaitWindow):
    def prepare(self):
        with self.lock:
            need(not hasattr(self,'prepared'),'one immutable preparation before any input worker')
            begin=original.utc_now_ns(self.kernel)
            _prepare_original(self)
            need(not self.active and self.session is None and self.thread_handle is None,
                 'preparation creates no ETW session or retained thread handle')
            self.prepared=True
            self.result['preparation']=dict(begin_ns=begin,end_ns=original.utc_now_ns(self.kernel),
                outside_input_window=True,ETW_started=False,thread_duplicate_created=False,
                original_begin_implementation=identity(v1.__file__))

    def recheck_prepared_bytes(self):
        for item in self.result['original_code']:
            raw=bytes.fromhex(item['hex'])
            need(self.c.get(item['pointer'],len(raw))==raw,'prepared original code still live and exact')
        for item in self.result['API_exports']:
            raw=bytes.fromhex(item['entry_hex'])
            need(self.c.get(item['target'],len(raw))==raw,'prepared actual wait export still exact')
            if item['slot'] is not None:
                need(self.c.get(item['slot'],4)==bytes.fromhex(item['IAT_hex']),'actual wait IAT still exact')
        item=self.result['TLS_implementation'];raw=bytes.fromhex(item['code_hex'])
        need(self.c.get(item['target'],len(raw))==raw,'current TlsGetValue code still exact')

    def begin(self):
        with self.lock:
            need(getattr(self,'prepared',False),'prepare before the original input observation window')
            begin=original.utc_now_ns(self.kernel)
            self.recheck_prepared_bytes()
            _begin_original(self)
            self.result['prepared_trigger']=dict(begin_ns=begin,end_ns=original.utc_now_ns(self.kernel),
                live_bytes_rechecked=True,fresh_owner_snapshot=True,original_ETW_start_tail_unchanged=True)


class PreflightWindow(WaitWindow):
    """Rehearse real trigger/observer concurrency, without submitting input."""
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs);self.prepare()

    def begin(self):
        from devtools.terminal_input_window import observe
        outcome={};record=dict(input_samples=[],input_submitted=False,original_deadline_seconds=11)
        def start():
            try:WaitWindow.begin(self)
            except BaseException as exc:outcome['error']=repr(exc)
        worker=threading.Thread(target=start,name='preflight-window-trigger',daemon=False)
        def sample():
            # Same lock contention as the real input observer, after a current
            # read-only sample. There is no button packet or synthetic edge.
            value=dict(wall_time_ns=time.time_ns(),MAIN_event_hex=self.c.get(self.c.main+0x2C,8).hex())
            self.poll();return value
        self.result['trigger_concurrency_preflight']=record
        record['observation_begin_ns']=original.utc_now_ns(self.kernel)
        worker.start()
        try:observe(worker,sample,record)
        finally:
            worker.join(timeout=6)
            record['observation_end_ns']=original.utc_now_ns(self.kernel)
            record['trigger_error']=outcome.get('error')
        need(not worker.is_alive() and not outcome,'real prepared trigger finishes inside unchanged input window')
        need(record['input_window']['complete'],'complete actual no-input concurrency rehearsal')


startup_probe=clone(v1.startup_probe,WaitWindow=PreflightWindow)


def run(out,phase):
    from devtools.native_input_isolation import require_qualified_guest
    qualification=require_qualified_guest();out=Path(out).resolve()
    need(out.parent==ROOT/'analysis' and out.name.endswith('.json.gz') and not out.exists(),
         'fresh guest prepared-window output')
    need(phase=='startup_preflight','prepared short preflight only')
    paths=[Path(__file__),Path(v1.__file__),ROOT/'devtools/terminal_original_wait_etw.py',
           ROOT/'devtools/terminal_wait_etw_probe.py',ROOT/'devtools/terminal_input_window.py']
    before=[identity(p)for p in paths];result=startup_probe(out,qualification)
    need(before==[identity(p)for p in paths],'prepared window implementations unchanged')
    result['window_implementations']=before
    raw=json.dumps(result,separators=(',',':')).encode();need(len(raw)<=8*1024*1024,'bounded complete source')
    packed=gzip.compress(raw,mtime=0);need(len(packed)<=2*1024*1024,'bounded complete compressed source')
    with out.open('xb')as f:f.write(packed)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',type=Path,required=True)
    p.add_argument('--phase',choices=['startup_preflight'],default='startup_preflight');a=p.parse_args()
    r=run(a.out,a.phase)
    print(json.dumps(dict(error=r.get('error'),snapshots=len(r.get('window_snapshots',[])),ETL=r.get('ETL'),accepted=False)))
    raise SystemExit(1 if r.get('error')or r.get('lifecycle',{}).get('error')else 0)
