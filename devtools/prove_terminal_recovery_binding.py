"""Reuse the completed model; qualify current owner handles without any UI."""
from __future__ import annotations
import argparse,copy,gzip,json,os,time
from pathlib import Path
from devtools.terminal_display_platform import DisplayOwner,base,need
from devtools.terminal_scene_dc_probe import Owner as CloseObserved
from devtools.terminal_recovery_admission import current_build,ROOT
from devtools.terminal_recovery_native import RetainedOwner
from devtools.terminal_recovery_binding import authenticate
from devtools.terminal_recovery_session import RecoverySession,binding_from_snapshot
from devtools.terminal_graphics_recovery import created,publish,read
from devtools.terminal_oplock import Win

SOURCE=ROOT/'.venv-audit/terminal-game-bound-model-v1-20261114.json.gz'
SOURCE_SHA='8750713d1b730e275ba802c6c4fc326952ac4387adc466a78a66a7bc52871a08'

def model_source():
    need(base.identity(SOURCE)['sha256']==SOURCE_SHA,'reuse exact completed current model')
    r=json.loads(gzip.decompress(SOURCE.read_bytes()));need(r['failure']=="KeyError('token')" and r['published_GAME'] and len(r['display_snapshots'])==3 and not r['native_executed'],'only known post-execution auditor field mismatch')
    for p in r['implementation_pins']:
        if p['path'] not in ('devtools/terminal_recovery_binding.py','devtools/terminal_recovery_session.py'):
            need(base.identity(ROOT/p['path'])==p,'unchanged original model execution input '+p['path'])
    b=r['baseline'];binding=binding_from_snapshot(r['display_snapshots'][0],b)
    live=dict(kind='explicit-symbolic-handles',owner=b['owner'],process_wait=0,process_exit=0,job_members=[],same_job=True)
    return r,b,binding,live

class ProbeOwner(DisplayOwner,CloseObserved):
    def __setattr__(self,name,value):
        if name=='deadline' and hasattr(self,'start'):value=min(value,self.start+5)
        super().__setattr__(name,value)

def owner_probe(folder):
    need(not folder.exists() and folder.is_relative_to(ROOT/'.venv-audit'),'fresh F no-UI evidence');folder.mkdir()
    start=time.monotonic();build=current_build();owner=None;binding=None
    r=dict(kind='current_admitted_owner_handle_probe',native_helper_executed=False,accepted=False,game_windows=0,D3D_calls=0,desktop_calls=0,screenshots=0,input_sent=False,helper=build['helper'])
    try:
        owner=ProbeOwner.__new__(ProbeOwner);ProbeOwner.__init__(owner,ROOT/build['helper']['path'],folder);r['native_helper_executed']=owner.resumed
        w=Win();parent=w.openp(0x1000,False,os.getpid())
        try:controller_created=created(w,parent)
        finally:w.close(parent)
        reg=dict(owner=dict(run_id=folder.name,pid=owner.pi.pid,process_created=created(owner.w,owner.pi.process),main_tid=owner.hello['main_tid'],main_teb=owner.hello['main_teb']),job_handle=owner.job,helper=build['helper'])
        wrong=copy.deepcopy(reg);wrong['owner']['process_created']+=1
        try:RetainedOwner(wrong,os.getpid(),controller_created)
        except ValueError as exc:r['wrong_lifetime_rejected']=str(exc)
        else:raise AssertionError('wrong lifetime accepted')
        binding=RetainedOwner(reg,os.getpid(),controller_created);r['live']=binding.inspect(require_exit=False)
        try:binding.inspect()
        except ValueError as exc:r['live_process_refused_restore']=str(exc)
        else:raise AssertionError('live process admitted for restoration')
        status=owner.call('STATUS');need(all(status[k]==0 for k in ('ui_gate','game_gate','gfx_gate','input_gate','windows','gfx_interfaces','display_bound','display_dc','texture_verify_pending','tls_slots','allocations')),'no window/device/TLS gate entered')
        need(owner.call('Shutdown')['result']==1 and owner.wait(1000)==0,'actual normal empty-resource helper exit')
        r['after_exit']=binding.inspect();r['status']=status
    except BaseException as exc:r['failure']=repr(exc)
    finally:
        if owner is not None and hasattr(owner,'receipt'):
            owner.finish();r.update(cleanup=owner.receipt,trace=owner.trace,parent_closes=owner.parent_closes)
        if binding:r['retained_handle_closes']=binding.close()
        r['seconds']=round(time.monotonic()-start,3)
    c=r.get('cleanup',{});r['accepted']=bool(not r.get('failure') and c.get('job_empty') and c.get('handles_closed') and not c.get('forced') and not c.get('errors') and c['exits'].get(str(c['parent_pid']))==dict(wait=0,code=0) and len(r['parent_closes'])==7 and all(x['result']==1 for x in r['parent_closes']) and len(r['retained_handle_closes'])==2 and all(x['result']==1 for x in r['retained_handle_closes']))
    r['implementation']=base.implementation_pins();publish(folder/'report.json',r);return r

def supervisor_probe(folder):
    need(not folder.exists(),'fresh versioned supervisor preflight');folder.mkdir();cases=[]
    for name in ('normal','block_gamma_write'):
        s=RecoverySession(folder/name,scenario=name);value=None
        try:
            need(s.call('baseline')['ok'],'same persistent model baseline')
            if name=='normal':value=s.call('recover');need(value['ok'] and value['value']['restored'],'versioned supervisor runs original model restoration')
            else:
                q=s.request('recover',1000);time.sleep(2)
                failure=read(s.folder/'supervisor-result.json');need(failure['reason']=='command_deadline','external process observes actual blocked-kernel deadline without controller')
                try:s.collect(q)
                except TimeoutError:pass
                else:raise AssertionError('hung worker returned success')
        finally:result=s.finish()
        need(result['cleanup']['job_empty'] and result['cleanup']['handles_closed'] and not result['cleanup']['errors'],'actual versioned Job and handles empty')
        need(result['normal_close']==(name=='normal'),'timeout never treated as normal restoration')
        cases.append(dict(case=name,supervisor=result))
    session=RecoverySession(folder/'absolute_deadline',lifetime_seconds=30,absolute_deadline_ns=time.monotonic_ns()+1_000_000_000)
    try:
        need(session.call('baseline',500)['ok'],'absolute-deadline model baseline');time.sleep(1.4)
    finally:result=session.finish()
    need(result['reason']=='session_deadline' and not result['normal_close'] and result['cleanup']['job_empty'] and result['cleanup']['handles_closed'] and result['elapsed_seconds']<2,'absolute deadline overrides longer relative lifetime')
    cases.append(dict(case='absolute_deadline',supervisor=result))
    return cases

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--folder',required=True);p.add_argument('--out',required=True);p.add_argument('--native-owner-probe',action='store_true');a=p.parse_args()
    folder=(ROOT/a.folder).resolve();need(not folder.exists() and folder.is_relative_to(ROOT/'.venv-audit'),'fresh F preflight root');folder.mkdir()
    report,b,binding,live=model_source();start=time.monotonic();receipt=authenticate(report,b,binding,live,native=False)
    result=dict(kind='bound_release_and_display_preflight',formal_acceptance=False,formal_progress='2/8',model_source=base.identity(SOURCE),source_original_collection_result='GAME publication and cleanup completed; post-audit token-field mismatch preserved unchanged',resumed_post_audit=True,original_instructions_rerun=False,authenticated_symbolic_release=receipt,model_seconds=report['seconds'],post_audit_seconds=round(time.monotonic()-start,3),native_GAME=False,native_GPU=False,native_desktop_write=False,interactive_admission=False)
    if a.native_owner_probe:
        result['native_owner_handles']=owner_probe(folder/'owner');need(result['native_owner_handles']['accepted'],'current admitted no-UI owner proof')
        result['supervisor_cases']=supervisor_probe(folder/'supervisor')
    result['implementation_pins']=base.implementation_pins();result['evidence']=[base.identity(x) for x in sorted(folder.rglob('*')) if x.is_file()];result['accepted_for_component_scope']=True
    out=(ROOT/a.out).resolve();need(out.is_relative_to(ROOT/'analysis') and not out.exists(),'fresh small component report');publish(out,result)
    print(json.dumps(dict(report=base.identity(out),accepted=True,owner_seconds=result.get('native_owner_handles',{}).get('seconds'),supervisor_cases=len(result.get('supervisor_cases',[])))));return 0

if __name__=='__main__':raise SystemExit(main())
