"""Scoped verification of suspended worker retention; never full acceptance.

Only three exact frozen AST predicates change: pending graph nodes need not have
a retained thread, do not inherit a later thread's handle, and do not date it.
All original graph, context, TLS, input and source checks remain in force.
"""
import argparse
import ast
import hashlib
import inspect
import json
from pathlib import Path, PureWindowsPath
import types

from devtools import terminal_school_handoff_verification as frozen

ROOT=Path(__file__).resolve().parents[1]
PARENT_SHA='1d269d8496159b40d873db4b2e18459b4ee18159f22e4bab6b694cd7c5cf8288'
CALLBACK={0x421F8A,0x56E183}
need=frozen.need


def identity(path):
    path=Path(path);data=path.read_bytes()
    return dict(path=str(path),bytes=len(data),sha256=hashlib.sha256(data).hexdigest())


def retention_contract(row,p,workers):
    """Authenticate a receipt against unchanged graph/task/context evidence."""
    receipt=row['worker_retention'];frames=row['frames'];tasks=row['tasks']
    need(receipt['version']==1 and type(receipt['version'])is int and
         receipt['pid']==p['pid'] and receipt['main_tid']==p['startup']['window']['main_tid'],
         'same retention process and MAIN identity')
    begin=receipt['capture_begin_perf_ns'];end=receipt['capture_end_perf_ns']
    need(type(begin)is int and type(end)is int and 0<begin<=end and
         receipt['retained_while_suspended']is True,'bounded actual held retention interval')
    tids=[f['tid']for f in frames]
    need(0<len(tids)<=256 and len(set(tids))==len(tids) and
         receipt['cohort_tids']==tids and tids[0]==receipt['main_tid'],
         'exact MAIN-first complete suspended cohort')
    for frame in frames:
        frozen.owner.verify_frame(frame)
        need(frame['owner_verified_before_suspend']is True and
             type(frame['previous_suspend_count'])is int and 0<=frame['previous_suspend_count']<0xffffffff,
             'verified owner before same-handle suspend')
    proofs=receipt['tasks']
    need(len(proofs)==len(tasks)<=128 and len({t['pointer']for t in tasks})==len(tasks),
         'one retention result per original graph task')
    pending=set()
    for task,proof in zip(tasks,proofs):
        head=frozen.blob(task['header_hex'],64,'complete unchanged retention head')
        key=(task['pointer'],task['thread_id']);tid=key[1]
        remote=frozen.word(head,0x20);event=frozen.word(head,0x1C)
        need(tid==frozen.word(head,0x24) and
             (proof['pointer'],proof['thread_id'],proof['remote_handle'],proof['event'])==(*key,remote,event),
             'retention identity equals actual node header')
        frame=next((f for f in frames if f['tid']==tid),None)
        need(proof['observed_context_present']is (frame is not None),'actual context presence')
        ancestors={x['return_va']for x in frame['chain']}if frame else set()
        status=proof['status']
        need(status in ('pending_callback_ancestry','retained','already_retained'),'explicit retention outcome')
        if status=='pending_callback_ancestry':
            need(not CALLBACK&ancestors and 'TLS'not in task,
                 'pending has no partial callback ancestry or TLS')
            # A later retained worker may have the same node/TID; it must not
            # retroactively convert the earlier construction sample to a worker.
            if key in workers:
                need(row['elapsed']<workers[key]['first_elapsed'],'pending strictly precedes actual retention')
            pending.add(key)
        else:
            need(key in workers and remote and tid,'retained original worker identity exists')
            worker=workers[key]
            need((worker['original_handle'],worker['event']['remote_handle'],worker['vtable'])==
                 (remote,event,task['vtable']),'same retained native handle event and vtable')
            need(row['elapsed']>=worker['first_elapsed'],'retention follows first actual observation')
            if status=='retained':
                need(row['elapsed']==worker['first_elapsed'] and CALLBACK<=ancestors and 'TLS'in task,
                     'first retention requires complete callback ancestry and TLS')
            # An already retained worker may have returned from its callback
            # while still executing the original CRT wrapper. That partial
            # frame is neither a new worker nor proof of completed cleanup.
            if CALLBACK<=ancestors or 'TLS'in task:
                need(CALLBACK<=ancestors and 'TLS'in task,
                     'live callback cannot omit TLS or one original ancestor')
    return pending


def _rewrite(function,old_expression,new_expression,namespace):
    """One exact AST replacement under a complete immutable parent SHA."""
    tree=ast.parse(inspect.getsource(function));old=ast.parse(old_expression,mode='eval').body
    replacement=ast.parse(new_expression,mode='eval').body;count=0
    class Replace(ast.NodeTransformer):
        def visit_If(self,node):
            nonlocal count
            self.generic_visit(node)
            if ast.dump(node.test)==ast.dump(old):
                node.test=ast.copy_location(replacement,node.test);count+=1
            return node
    tree=Replace().visit(tree)
    need(count==1,'exact single frozen AST predicate replacement')
    ast.fix_missing_locations(tree);exec(compile(tree,str(Path(__file__)), 'exec'),namespace)
    return namespace[function.__name__]


def require_input_owner(row,task,p,workers):
    key=(task['pointer'],task['thread_id'])
    need(key not in retention_contract(row,p,workers) and key in workers and 'TLS'in task,
         'input target requires retained authenticated current TLS')


def adapted_namespace():
    need(identity(frozen.__file__)['sha256']==PARENT_SHA,'fixed frozen school verifier SHA')
    ns=dict(frozen.__dict__)
    # Shared globals are essential: verify_report -> verify_mouse_action ->
    # verify_ready must resolve the scoped functions, never old globals.
    for name,fn in frozen.__dict__.items():
        if isinstance(fn,types.FunctionType) and fn.__globals__ is frozen.__dict__:
            ns[name]=types.FunctionType(fn.__code__,ns,fn.__name__,fn.__defaults__,fn.__closure__)
    ns['_pending_keys']=lambda row,p,workers:retention_contract(row,p,workers)
    task_ns=dict(ns)
    # Replace only membership predicates; keep every raw graph/TLS statement.
    tree=ast.parse(inspect.getsource(frozen.verify_task_row))
    targets={ast.dump(ast.parse(a,mode='eval').body):b for a,b in (
        ('require_retained','require_retained and (ptr,tid) not in _pending_keys(row,p,workers)'),
        ('(ptr,tid) in workers','(ptr,tid) in workers and (ptr,tid) not in _pending_keys(row,p,workers)'))}
    counts={key:0 for key in targets}
    class TaskPredicates(ast.NodeTransformer):
        def visit_If(self,node):
            self.generic_visit(node);key=ast.dump(node.test)
            if key in targets:
                counts[key]+=1;node.test=ast.copy_location(ast.parse(targets[key],mode='eval').body,node.test)
            return node
    tree=TaskPredicates().visit(tree);need(set(counts.values())=={1},'two exact frozen task AST predicates')
    ast.fix_missing_locations(tree);exec(compile(tree,str(Path(__file__)),'exec'),task_ns)
    task_impl=task_ns['verify_task_row']
    def task_row(row,p,raw,game,workers,require_retained=True):
        if 'worker_retention'in row:
            retention_contract(row,p,workers)
            return task_impl(row,p,raw,game,workers,require_retained)
        # Frozen post-release snapshots legitimately have their separate
        # no-retention contract. Ordinary observations cannot take this route.
        need(require_retained is False,'ordinary task row requires atomic retention receipt')
        return frozen.verify_task_row(row,p,raw,game,workers,False)
    ns['verify_task_row']=task_row
    ready_impl=ns['verify_ready']
    def ready(row,p,raw,game,workers,stage):
        task=ready_impl(row,p,raw,game,workers,stage)
        require_input_owner(row,task,p,workers)
        return task
    ns['verify_ready']=ready
    report_impl=_rewrite(frozen.verify_report,
        "not supplemental and word(head,0x20) and t['thread_id']",
        "not supplemental and word(head,0x20) and t['thread_id'] and key not in _pending_keys(row,p,workers)",ns)
    def report(report,raw,inventory,check_disk=True,startup_root=None):
        declared=report['worker_retention_implementation']
        expected=identity(ROOT/'devtools/terminal_worker_retention.py')
        path=PureWindowsPath(declared['path'])
        need(path.name=='terminal_worker_retention.py' and path.parent.name=='devtools' and
             all(declared[k]==expected[k]for k in ('bytes','sha256')),
             'exact executed retention collector implementation')
        p=report['probe'];need('worker_retention_failure'not in p,'no failed atomic retention')
        cleanup=p['observer_retention_cleanup']
        need(cleanup['closed_observer_handles']==len(p['workers']) and
             cleanup['original_resource_cleanup_proved']is False,'own duplicates closed without original cleanup claim')
        result=report_impl(report,raw,inventory,check_disk,startup_root)
        result.update(worker_retention_verified=True,worker_retention_implementation=declared,
            worker_retention_verifier=identity(__file__),frozen_school_verifier_sha256=PARENT_SHA,
            pending_graph_observations=sum(len(retention_contract(r,p,
                {(w['pointer'],w['thread_id']):w for w in p['workers']}))for r in p['samples']),
            complete_worker_construction_trace_proved=False)
        return result
    ns['verify_report']=report
    return ns


def verify_file(path,digest,guest_modules=None):
    return adapted_namespace()['verify_file'](path,digest,guest_modules)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True);parser.add_argument('--source-sha',required=True)
    parser.add_argument('--guest-modules');parser.add_argument('--out',required=True)
    a=parser.parse_args();out=Path(a.out);need(not out.exists(),'new independent report path only')
    try:
        result=verify_file(a.source,a.source_sha,a.guest_modules)
    except Exception as exc:
        result=dict(status='blocked',error=repr(exc),accepted=False,
                    source=dict(path=a.source,sha256=a.source_sha),verifier=identity(__file__))
    with out.open('x',encoding='utf8')as stream:json.dump(result,stream,ensure_ascii=False,indent=2)
    return 0 if result.get('worker_retention_verified')is True else 2


if __name__=='__main__':raise SystemExit(main())
