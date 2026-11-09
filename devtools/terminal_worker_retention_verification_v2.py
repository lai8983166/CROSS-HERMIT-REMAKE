"""Strict classification of retained base-vtable retirement observations.

Unknown vtable transitions remain failures. A known exited thread and sampled
scheduler wait do not establish full destructor, resource, or PTD cleanup.
"""
import argparse
import ast
import functools
import inspect
import json
from pathlib import Path, PureWindowsPath
import types

from devtools import terminal_worker_retention_verification as v1

frozen=v1.frozen
need=v1.need
identity=v1.identity
ROOT=v1.ROOT
PARENT_SHA=v1.PARENT_SHA
V1_SHA='63891a42f0f6ecf73791bc5a13ccdce213ba2341fdafe678457af88c333d1fc8'
COLLECTOR_PARENT_SHA='8101263c5f356358ea365d37d58d36a779ad7a680c267dba86907770d4e0c088'
TRANSITION='retained_vtable_transition'
BASE_VTABLE=0x594A54


def rewrite(function,replacements,namespace):
    """Reject unknown AST shapes; never substitute text or mutate source."""
    tree=ast.parse(inspect.getsource(function))
    targets={ast.dump(ast.parse(a,mode='eval').body):b for a,b in replacements}
    counts={k:0 for k in targets}
    class Replace(ast.NodeTransformer):
        def generic_visit(self,node):
            key=ast.dump(node)
            if key in targets:
                counts[key]+=1
                return ast.copy_location(ast.parse(targets[key],mode='eval').body,node)
            return super().generic_visit(node)
    tree=Replace().visit(tree)
    need(set(counts.values())=={1},'exact single occurrence of every frozen AST expression')
    ast.fix_missing_locations(tree);exec(compile(tree,__file__,'exec'),namespace)
    return namespace[function.__name__]


def transition_contract(row,task,proof,worker,p):
    head=frozen.blob(task['header_hex'],64,'retiring original head')
    tid=task['thread_id'];node=task['pointer'];t=proof['transition'];q=t['thread_query']
    need(t['transition_verified']is False and t['full_resource_PTD_cleanup_proved']is False,
         'collector transition observation makes no verification or cleanup claim')
    need(proof['status']==TRANSITION and
         (t['previous_vtable'],t['observed_vtable'])==(worker['vtable'],task['vtable']) and
         worker['vtable']!=BASE_VTABLE and task['vtable']==frozen.word(head)==BASE_VTABLE,
         'only classified original derived-to-base vtable transition')
    need(frozen.word(head,4)==4 and frozen.word(head,8)==p['main']+0x64,
         'exact original completion flag and manager backpointer')
    need('TLS'not in task and not any(f['tid']==tid for f in row['frames']) and
         proof['observed_context_present']is False and t['worker_stack_regions']==[],
         'exited worker has no current context TLS or invented worker stack')
    need((q['owner_pid'],q['thread_id'])==(p['pid'],tid) and
         type(q['wait_status'])is int and type(q['exit_code'])is int and
         q['wait_status']==q['exit_code']==0 and q['zero_timeout']is True and
         q['observer_duplicate_only']is True and q['original_cleanup_proved']is False,
         'same owned retained duplicate really signaled with exit0')
    main=next((f for f in row['frames']if f['tid']==p['startup']['window']['main_tid']),None)
    need(main is not None,'actual suspended MAIN frame')
    frozen.owner.verify_frame(main)
    sched=[f for f in main['chain']if f['return_va']==0x42182F]
    sleep=[f for f in main['chain']if f['return_va']==0x421ACE]
    need(len(sched)==len(sleep)==1 and sleep[0]['saved_bp']==sched[0]['bp'],
         'exact original Sleep return linked to scheduler caller')
    frame=sched[0];s=t['scheduler_frame'];bp=frame['bp']
    need(s is not None and (s['bp'],s['return_va'],s['pointer'])==(bp,0x42182F,bp-0x5C),
         'retiring scheduler bytes belong to actual caller frame')
    raw=frozen.blob(s['hex'],0x6C,'complete original scheduler local frame')
    need((frozen.word(raw,0x5C),frozen.word(raw,0x60))==(frame['saved_bp'],frame['return_va']),
         'scheduler raw saved frame and return address')
    need(frozen.word(raw,0x64)==node and frozen.word(raw,0x58)==p['main']+0x64 and
         frozen.word(raw,0x54)==4,'scheduler actual node argument manager and completion flag')
    return True


def same_retained_identity(row,task,proof,worker,p):
    head=bytes.fromhex(task['header_hex'])
    same=(worker['original_handle'],worker['event']['remote_handle'])==(
        frozen.word(head,0x20),frozen.word(head,0x1C))
    need(same,'retiring handle and event cannot change')
    if proof['status']==TRANSITION:return transition_contract(row,task,proof,worker,p)
    need('transition'not in proof,'no unclassified transition on ordinary retention')
    return worker['vtable']==task['vtable']


@functools.lru_cache(maxsize=1)
def retention_function():
    need(identity(v1.__file__)['sha256']==V1_SHA,'fixed first retention verifier SHA')
    ns=dict(v1.__dict__,_same_retained_identity=same_retained_identity)
    return rewrite(v1.retention_contract,(
        ("receipt['version']==1","receipt['version']==2"),
        ("status in ('pending_callback_ancestry','retained','already_retained')",
         "status in ('pending_callback_ancestry','retained','already_retained','retained_vtable_transition')"),
        ("(worker['original_handle'],worker['event']['remote_handle'],worker['vtable'])==(remote,event,task['vtable'])",
         "_same_retained_identity(row,task,proof,worker,p)")),ns)


def retry_contract(row,p,source_version=2):
    need(source_version in (2,3) and type(source_version)is int,'explicit supported retention source layer')
    if source_version==2:
        need('cohort_observation_retries'not in row and 'cohort_retry_budget'not in row,
             'source2 cannot hide cohort retry evidence')
        return
    need('cohort_observation_retries'in row and 'cohort_retry_budget'in row,
         'source3 atomic row requires explicit retry ledger and budget')
    retries=row['cohort_observation_retries'];budget=row['cohort_retry_budget']
    need(isinstance(retries,list) and len(retries)<=4,'at most four failed attempts before a successful fifth')
    need(isinstance(budget,dict) and set(budget)=={'maximum_attempts','retry_budget_ns','started_perf_ns',
         'successful_attempt_begin_perf_ns','deadline_applies_to_next_attempt_start'},'exact retry budget fields')
    need(type(budget['maximum_attempts'])is int and budget['maximum_attempts']==5 and
         type(budget['retry_budget_ns'])is int and budget['retry_budget_ns']==500_000_000 and
         budget['deadline_applies_to_next_attempt_start']is True,'exact next-attempt-start retry budget')
    started=budget['started_perf_ns'];success=budget['successful_attempt_begin_perf_ns']
    final=row['worker_retention']['capture_begin_perf_ns']
    need(type(started)is int and type(success)is int and 0<started<=success<=final,
         'actual successful attempt begins before its held snapshot')
    previous=started
    for i,retry in enumerate(retries,1):
        need(isinstance(retry,dict) and set(retry)=={'pid','main_tid','attempt','before_tids','after_tids',
             'capture_begin_perf_ns','capture_end_perf_ns','owned_suspend_restored','source_snapshot_emitted'},
             'failed inventory attempt contains no emitted snapshot or hidden fields')
        need(retry['pid']==p['pid'] and retry['main_tid']==p['startup']['window']['main_tid'] and
             type(retry['attempt'])is int and retry['attempt']==i,'exact retry owner and consecutive attempt index')
        before=retry['before_tids'];after=retry['after_tids']
        for tids in (before,after):
            need(isinstance(tids,list) and 0<len(tids)<=256 and
                 all(type(t)is int and 0<t<0x100000000 for t in tids) and
                 len(set(tids))==len(tids) and retry['main_tid']in tids,
                 'bounded unique actual inventory includes MAIN')
        need(set(before)!=set(after),'actual membership change, not enumeration reordering')
        begin=retry['capture_begin_perf_ns'];end=retry['capture_end_perf_ns']
        need(type(begin)is int and type(end)is int and previous<=begin<=end<=success,
             'ordered nonoverlapping completed failed attempts precede successful attempt')
        if i>1:need(begin-started<500_000_000,'later failed attempt starts within retry budget')
        need(retry['owned_suspend_restored']is True and retry['source_snapshot_emitted']is False,
             'only fully restored inventory differences can retry without a snapshot')
        previous=end
    if retries:need(success-started<500_000_000,'successful retry starts within budget')


def retention_contract(row,p,workers,source_version=2):
    retry_contract(row,p,source_version)
    return retention_function()(row,p,workers)


def task_vtable_matches(row,task,worker,p):
    proofs=row['worker_retention']['tasks']
    proof=next(x for x in proofs if x['pointer']==task['pointer'])
    if proof['status']==TRANSITION:return transition_contract(row,task,proof,worker,p)
    return worker['vtable']==task['vtable']


def require_input_owner(row,task,p,workers,source_version=2):
    key=(task['pointer'],task['thread_id']);pending=retention_contract(row,p,workers,source_version)
    proof=next(x for x in row['worker_retention']['tasks']if x['pointer']==key[0])
    need(proof['status']in ('retained','already_retained') and key not in pending and
         key in workers and 'TLS'in task,'input target requires live retained current TLS without transition')


def verify_transition_history(report,source_version=2):
    p=report['probe'];workers={(w['pointer'],w['thread_id']):w for w in p['workers']}
    rows=list(p['samples']);qualified={};count=0
    # Include all ordinary rows referenced by input/dependency receipts as well;
    # none may hide an unclassified transition merely by not being a main sample.
    stack=[p];seen=set();row_ids={id(r)for r in rows}
    while stack:
        value=stack.pop()
        if isinstance(value,dict):
            if id(value)in seen:continue
            seen.add(id(value))
            if source_version==2:
                need('cohort_observation_retries'not in value and 'cohort_retry_budget'not in value,
                     'source2 cannot hide cohort retry evidence')
            if 'worker_retention'in value and id(value)not in row_ids:
                rows.append(value);row_ids.add(id(value))
            stack.extend(value.values())
        elif isinstance(value,list):stack.extend(value)
    rows.sort(key=lambda r:r['elapsed'])
    for row in rows:
        pending=retention_contract(row,p,workers,source_version)
        for task,proof in zip(row['tasks'],row['worker_retention']['tasks']):
            key=(task['pointer'],task['thread_id'])
            if proof['status']==TRANSITION:
                need(key in qualified and qualified[key]<row['elapsed'],
                     'transition requires earlier real derived worker with TLS')
                count+=1
            elif key not in pending and 'TLS'in task:
                need(task['vtable']==workers[key]['vtable'],'historical derived identity unchanged')
                frame=next(f for f in row['frames']if f['tid']==key[1])
                callbacks=[f for f in frame['chain']if f['return_va']==0x421F8A]
                need(len(callbacks)==1,'historical real callback frame')
                frozen.startup.verify_tls(task['TLS'],frame,bytes.fromhex(task['header_hex']),key[0],key[1],
                    p['pid'],{'pointer':callbacks[0]['bp']-0x80},2)
                qualified.setdefault(key,row['elapsed'])
    return count


def verify_layers(report,source_version):
    need(type(source_version)is int and source_version in (2,3),'explicit supported retention source layer')
    need(type(report['worker_retention_version'])is int and report['worker_retention_version']==source_version,
         'explicit transition-aware retention source version')
    layers=(('worker_retention_implementation','terminal_worker_retention_v2.py'),
            ('worker_retention_parent_implementation','terminal_worker_retention.py'))if source_version==2 else (
            ('worker_retention_implementation','terminal_worker_retention_v3.py'),
            ('worker_retention_parent_implementation','terminal_worker_retention_v2.py'),
            ('worker_retention_grandparent_implementation','terminal_worker_retention.py'))
    if source_version==2:
        need('worker_retention_grandparent_implementation'not in report,'source2 has exactly two retention layers')
    for field,name in layers:
        declared=report[field];expected=identity(ROOT/'devtools'/name);path=PureWindowsPath(declared['path'])
        need(path.name==name and path.parent.name=='devtools' and
             all(declared[k]==expected[k]for k in ('bytes','sha256')),'exact executed retention layer')
    need(report[layers[-1][0]]['sha256']==COLLECTOR_PARENT_SHA,
         'unchanged first native-tested retention collector')


def adapted_namespace(source_version=2):
    need(type(source_version)is int and source_version in (2,3),'explicit supported retention source layer')
    need(identity(frozen.__file__)['sha256']==PARENT_SHA,'fixed frozen school verifier SHA')
    need(identity(v1.__file__)['sha256']==V1_SHA,'fixed first retention verifier SHA')
    def contract(row,p,workers):return retention_contract(row,p,workers,source_version)
    ns=dict(frozen.__dict__)
    for name,fn in frozen.__dict__.items():
        if isinstance(fn,types.FunctionType) and fn.__globals__ is frozen.__dict__:
            ns[name]=types.FunctionType(fn.__code__,ns,fn.__name__,fn.__defaults__,fn.__closure__)
    ns['_pending_keys']=contract
    task_ns=dict(ns,_task_vtable_matches=task_vtable_matches)
    replacements=(
        ('require_retained','require_retained and (ptr,tid) not in _pending_keys(row,p,workers)'),
        ('(ptr,tid) in workers','(ptr,tid) in workers and (ptr,tid) not in _pending_keys(row,p,workers)'),
        ("w['vtable']==vt","_task_vtable_matches(row,task,w,p)"))
    targets=[ast.dump(ast.parse(a,mode='eval').body)for a,b in replacements];counts=[0,0,0]
    class TaskPredicates(ast.NodeTransformer):
        def visit_If(self,node):
            self.generic_visit(node)
            for i in (0,1):
                if ast.dump(node.test)==targets[i]:
                    counts[i]+=1;node.test=ast.copy_location(ast.parse(replacements[i][1],mode='eval').body,node.test)
            return node
        def visit_Compare(self,node):
            if ast.dump(node)==targets[2]:
                counts[2]+=1
                return ast.copy_location(ast.parse(replacements[2][1],mode='eval').body,node)
            return self.generic_visit(node)
    tree=TaskPredicates().visit(ast.parse(inspect.getsource(frozen.verify_task_row)))
    need(counts==[1,1,1],'exact three frozen task predicates')
    ast.fix_missing_locations(tree);exec(compile(tree,__file__,'exec'),task_ns)
    task_impl=task_ns['verify_task_row']
    def task_row(row,p,raw,game,workers,require_retained=True):
        if 'worker_retention'in row:
            contract(row,p,workers)
            return task_impl(row,p,raw,game,workers,require_retained)
        need(require_retained is False,'ordinary task row requires atomic retention receipt')
        return frozen.verify_task_row(row,p,raw,game,workers,False)
    ns['verify_task_row']=task_row;ready_impl=ns['verify_ready']
    def ready(row,p,raw,game,workers,stage):
        task=ready_impl(row,p,raw,game,workers,stage)
        require_input_owner(row,task,p,workers,source_version)
        return task
    ns['verify_ready']=ready
    report_impl=rewrite(frozen.verify_report,((
        "not supplemental and word(head,0x20) and t['thread_id']",
        "not supplemental and word(head,0x20) and t['thread_id'] and key not in _pending_keys(row,p,workers)"),),ns)
    def report(report,raw,inventory,check_disk=True,startup_root=None):
        verify_layers(report,source_version)
        p=report['probe'];need('worker_retention_failure'not in p,'no failed atomic retention')
        cleanup=p['observer_retention_cleanup']
        need(cleanup['closed_observer_handles']==len(p['workers']) and
             cleanup['original_resource_cleanup_proved']is False,'own duplicate closure only')
        transitions=verify_transition_history(report,source_version)
        result=report_impl(report,raw,inventory,check_disk,startup_root)
        result.update(worker_retention_verified=True,worker_retention_version=source_version,
            worker_retention_verifier=identity(__file__),parent_retention_verifier=identity(v1.__file__),
            classified_retiring_observations=transitions,unclassified_transitions_accepted=False,
            full_destructor_trace_proved=False,normal_PTD_cleanup_proved=False,
            full_resource_lifetime_proved=False)
        return result
    ns['verify_report']=report
    return ns


def verify_file(path,digest,guest_modules=None):
    report=frozen.read_report(path,digest)
    return adapted_namespace(report['worker_retention_version'])['verify_file'](path,digest,guest_modules)


def execution_identities():
    return [identity(path)for path in (__file__,v1.__file__,frozen.__file__)]


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source',required=True);parser.add_argument('--source-sha',required=True)
    parser.add_argument('--guest-modules');parser.add_argument('--out',required=True)
    a=parser.parse_args();out=Path(a.out);need(not out.exists(),'new independent report path only')
    before=execution_identities()
    try:result=verify_file(a.source,a.source_sha,a.guest_modules)
    except Exception as exc:
        result=dict(status='blocked',error=repr(exc),accepted=False,
                    source=dict(path=a.source,sha256=a.source_sha),verifier=before[0])
    result['execution_implementations']=before
    result['execution_implementation_errors']=[]
    try:
        after=execution_identities()
        result['execution_implementations_after']=after
        if before!=after:
            result['execution_implementation_errors'].append('v2, v1 or frozen school verifier changed during verification')
    except Exception as exc:
        result['execution_implementation_errors'].append('final implementation identity check failed: '+repr(exc))
    if result['execution_implementation_errors']:
        result.update(status='blocked',accepted=False,worker_retention_verified=False)
    with out.open('x',encoding='utf8')as stream:json.dump(result,stream,ensure_ascii=False,indent=2)
    return 0 if result.get('worker_retention_verified')is True else 2


if __name__=='__main__':raise SystemExit(main())
