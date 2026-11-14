"""One explicitly authorized 120-second host component run; default plan only."""
from __future__ import annotations
import argparse,gzip,json,time,queue
from datetime import datetime,timezone
from pathlib import Path
from devtools import terminal_game_bound as route
from devtools.terminal_recovery_admission import current_build
from devtools.terminal_recovery_session import RecoverySession,CORE
from devtools.terminal_graphics_recovery import created

ROOT,need,base=route.ROOT,route.need,route.base
NATIVE_WINDOW_ADMISSION=False
BLOCKER='Visible-window failure before DISPLAY_BIND has no qualified attributed foreground restoration; no GPU/GAME launch admitted.'

def check_gate(path):
    need(NATIVE_WINDOW_ADMISSION,BLOCKER)
    gate=json.loads(path.read_text('utf-8'));need(gate['ready_for_one_bounded_native_window'] is True,'current complete offline admission')
    build=current_build();need(gate['helper']==build['helper'],'exact qualified executable')
    for pin in gate['pins']:need(base.identity(ROOT/pin['path'])==pin,'exact admitted source '+pin['path'])
    return gate,build

def equal_desktop(b,state):
    previous=b['state'];issues=route.desktop.frozen.differences(previous,state)
    for key in ('graphics','cursor','display_identities','shell_identity','taskbar_identities','appbar_state'):
        if state[key]!=previous[key]:issues.append(key)
    return sorted(set(issues))

def run(folder,gate,build,deadline):
    need(NATIVE_WINDOW_ADMISSION,BLOCKER)
    need(not folder.exists() and folder.is_relative_to(ROOT/'.venv-audit'),'one fresh F native case');folder.mkdir()
    helper=ROOT/build['helper']['path'];need(not (helper.parent/'native-GAME-attempt.once').exists(),'single current original GRAPHICS attempt')
    (helper.parent/'native-GAME-attempt.once').write_text(json.dumps(dict(started_utc=datetime.now(timezone.utc).isoformat(),scope='original GAME publication then supplemental cleanup',gate=gate['kind'])),'utf-8')
    e=route.DisplayEngine();owner=None;observer=None;baseline=None;report={};outcome={};bound=False
    try:
        need(deadline-time.monotonic()>=115,'90s native plus bounded restoration reserve')
        owner=route.NativeOwner.__new__(route.NativeOwner);route.NativeOwner.__init__(owner,helper,folder)
        observer=RecoverySession(folder/'recovery',backend='native-bound',lifetime_seconds=115,absolute_deadline_ns=int((deadline-3)*1e9))
        identity=dict(run_id=folder.name,pid=owner.pi.pid,process_created=created(owner.w,owner.pi.process),main_tid=owner.hello['main_tid'],main_teb=owner.hello['main_teb'])
        answer=observer.call('baseline',3000,dict(owner=identity,job_handle=owner.job,helper=build['helper']));need(answer['ok'],'actual pre-window baseline: '+str(answer.get('failure')));baseline=answer['value'];owner.observer=observer
        def binding(snapshot):
            nonlocal bound
            if snapshot['phase']==0:
                response=observer.call('bind',3000,snapshot);need(response['ok'],'actual D3D target binding: '+str(response.get('failure')));bound=True
        e.binding_validator=binding
        def input_snapshot():
            response=observer.call('readback',2000);need(response['ok'],'actual input owner pre-input state');return response['value']['state']
        outcome=route.route(e,owner,baseline,input_snapshot)
        need(owner.wait(max(0,min(1000,int((owner.deadline-time.monotonic())*1000))))==0,'normal native exit within original component budget')
        report=route.evidence(e,owner,baseline,outcome,True);report['component_completed']=True
    except BaseException as exc:
        report=route.evidence(e,owner,baseline,outcome,bool(owner and owner.resumed)) if owner and baseline else dict(native_executed=bool(owner and owner.resumed))
        report.update(component_completed=False,failure=repr(exc))
    finally:
        if owner and hasattr(owner,'receipt'):
            # Keep any already-delivered native BEGIN before terminating the
            # owned Job. Never execute abandoned callbacks after a failure.
            for _ in range(256):
                try:line=owner.q.get_nowait()
                except queue.Empty:break
                if isinstance(line,str) and line.startswith('E NATIVE_MUTATION_BEGIN '):
                    row=dict(direction='response',event='NATIVE_MUTATION_BEGIN')
                    for field in line.split()[2:]:
                        key,value=field.split('=',1);row[key]=int(value) if value.isdecimal() and not key.endswith('_hex') else value
                    owner.trace.append(row)
            owner.finish();report.update(native_trace=owner.trace,owner_cleanup=owner.receipt,parent_closes=owner.parent_closes)
            clean=owner.receipt;normal=not clean['forced'] and not clean['errors'] and clean['job_empty'] and clean['handles_closed'] and clean['exits'].get(str(clean['parent_pid']))==dict(wait=0,code=0)
            report['component_completed']=bool(report.get('component_completed') and normal and len(owner.parent_closes)==7 and all(x['result']==1 for x in owner.parent_closes))
    report.update(collector=base.identity(__file__),helper=build['helper'],formal_acceptance=False,formal_progress='2/8',wait_return=False,result_consumed=False,screenshots=False,global_input=False,desktop_restored=False)
    source=route.save(folder/'native-release-source.json.gz',report)
    try:
        if observer and baseline:
            if bound:
                op='recover' if report.get('component_completed') else 'containment'
                remaining_ms=int((deadline-time.monotonic()-3)*1000);need(remaining_ms>=100,'authorized restoration window ended')
                answer=observer.call(op,min(20000,remaining_ms),dict(report=source));report['restoration']=answer
                report['desktop_restored']=bool(answer['ok'] and answer['value']['restored'])
                if op=='recover' and not report['desktop_restored'] and observer.process.poll() is None:
                    # Preserve the rejected normal audit. Safety restoration is
                    # independently classified and cannot turn it into success.
                    report['component_completed']=False
                    remaining_ms=int((deadline-time.monotonic()-3)*1000);need(remaining_ms>=100,'authorized fallback restoration window ended')
                    answer=observer.call('containment',min(20000,remaining_ms),dict(report=source));report['containment_restoration']=answer
                    report['desktop_restored']=bool(answer['ok'] and answer['value']['restored'])
            else:
                checks=[]
                for index in range(2):
                    if index:time.sleep(.5)
                    answer=observer.call('readback',2000);need(answer['ok'],'actual post-containment readback');checks.append(equal_desktop(baseline,answer['value']['state']))
                report['unchanged_desktop_checks']=checks;report['desktop_restored']=not any(checks)
    except BaseException as exc:report['restoration_error']=repr(exc)
    finally:
        if observer:report['observer_cleanup']=observer.finish()
    report['accepted_component']=bool(report.get('component_completed') and report['desktop_restored'] and report.get('observer_cleanup',{}).get('normal_close'))
    return dict(output=route.save(folder/'result.json.gz',report),accepted=report['accepted_component'],GAME_published=bool(report.get('published_GAME')),desktop_restored=report['desktop_restored'],failure=report.get('failure'),restoration_error=report.get('restoration_error'))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--execute',action='store_true');p.add_argument('--gate');p.add_argument('--folder');p.add_argument('--desktop-until');a=p.parse_args()
    if not a.execute:print(json.dumps(dict(plan_only=True,native_seconds=90,desktop_total_seconds=120,requires_fresh_desktop_window=True,screenshots=False,input_injection=False,native_admission=NATIVE_WINDOW_ADMISSION,blocker=BLOCKER,scope='GAME publication, two real texture readbacks, original supplemental cleanup and desktop restoration; no scene or battle')));return 0
    need(a.gate and a.folder and a.desktop_until,'exact gate, fresh F case and new desktop deadline required')
    end=datetime.fromisoformat(a.desktop_until);need(end.tzinfo is not None,'explicit UTC desktop deadline');seconds=(end-datetime.now(timezone.utc)).total_seconds();need(118<=seconds<=120,'fresh at-most120-second authorized host window')
    gate,build=check_gate((ROOT/a.gate).resolve());result=run((ROOT/a.folder).resolve(),gate,build,time.monotonic()+seconds);print(json.dumps(result));return 0 if result['accepted'] else 1

if __name__=='__main__':raise SystemExit(main())
