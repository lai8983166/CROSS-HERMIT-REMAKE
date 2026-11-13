"""One five-second, no-window, read-only real desktop observer qualification."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
from devtools.terminal_graphics_recovery import RecoverySession,read,publish,ROOT,need,verify_implementations,digest
from devtools.prove_terminal_graphics_recovery import identity
from devtools import terminal_graphics_desktop as frozen

def validate(folder):
    cfg=read(folder/'config.json');verify_implementations(cfg);need(cfg['backend']=='native-readonly' and cfg['scenario']=='normal' and cfg['lifetime_seconds']==5,'fixed genuine read-only observer scope')
    r=read(folder/'observer-report.json');s=r['supervisor'];c=s['cleanup']
    need(s==read(folder/'supervisor-result.json'),'observer report agrees with independent supervisor receipt')
    need(r['game_runs']==r['screenshots']==r['desktop_writes']==0 and s['desktop_writes']==0,'no game, pixels or desktop mutations')
    need(s['normal_close'] and s['close_acknowledged'] and s['natural_job_drain']['accepted'] and not s['natural_job_drain']['final_members'] and c['exits'][str(s['launch_pid'])]==dict(wait=0,code=0) and c['job_empty'] and c['handles_closed'] and not c['forced'] and not c['errors'],'normal observation process cleanup')
    for seq,name in ((1,'baseline'),(2,'readback'),(3,'close')):
        q=read(folder/f'request-{seq}.json');a=read(folder/f'armed-{seq}.json');v=read(folder/f'response-{seq}.json')
        need(q['op']==name and v['ok'] and v['backend']=='native-readonly' and v['desktop_writes']==0,'actual expected observation response')
        need(v==r[name] if name!='close' else v['value']==dict(closed=True),'actual observation or close acknowledgement')
        need(q['token']==a['token']==v['token']==cfg['token'] and digest(q)==a['request_sha256']==v['request_sha256'] and v['completed_ns']<=a['deadline_ns'],'same fresh arm/request/response within external deadline')
    a,b=r['baseline']['value']['state'],r['readback']['value']['state'];pid=r['baseline']['worker_pid']
    need(pid==r['readback']['worker_pid']==a['input_observer']['pid']==b['input_observer']['pid'],'same actual observer process across reads')
    need(a['input_observer']==b['input_observer'],'same observer creation/session/input tick')
    need(not frozen.frozen.previous.health(a) and not frozen.frozen.previous.health(b),'actual healthy desktop snapshots')
    differences=frozen.frozen.differences(a,b)
    for key in ('graphics','cursor','display_identities','shell_identity','taskbar_identities','appbar_state'):
        if a[key]!=b[key]:differences.append(key)
    need(not differences,'actual unchanged resolution/taskbar/work-area/foreground/gamma/cursor observations')
    need(len(bytes.fromhex(a['graphics']['gamma_hex']))==1536 and s['native_observation_commands_completed']==2,'two full original gamma metadata observations')
    return dict(accepted_within_readonly_scope=True,native_game_runs=0,desktop_writes=0,screenshots=0,actual_readonly_observations=2,same_observer_pid=pid,normal_close=True,job_empty=True,elapsed_seconds=s['elapsed_seconds'],differences=differences,gamma_bytes=1536,gamma_sha256=hashlib.sha256(bytes.fromhex(a['graphics']['gamma_hex'])).hexdigest(),modes=[x['mode']for x in b['monitors']],taskbars_visible=[x['visible']for x in b['taskbars']],target=a['graphics']['device'],D3D_adapter_mapping_proven=False,write_recovery_qualified=False)

def observe(folder):
    s=RecoverySession(folder,backend='native-readonly',lifetime_seconds=5);r=dict(kind='bounded_real_readonly_observer',game_runs=0,screenshots=0,desktop_writes=0)
    try:
        r['baseline']=s.call('baseline',2000)
        if r['baseline']['ok']:r['readback']=s.call('readback',2000)
    finally:r['supervisor']=s.finish();publish(s.folder/'observer-report.json',r)
    return s.folder

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--folder',required=True);p.add_argument('--out',required=True);p.add_argument('--validate-only',action='store_true');a=p.parse_args()
    folder=(ROOT/a.folder).resolve();out=(ROOT/a.out).resolve();need(out.is_relative_to(ROOT/'analysis') and not out.exists(),'fresh F small read-only report')
    if not a.validate_only:folder=observe(folder)
    r=dict(kind='native_readonly_observer_preflight',formal_acceptance=False,formal_progress='2/8',native_write_admission=False,implementation=[identity(ROOT/x)for x in ('devtools/prove_terminal_graphics_observer.py','devtools/terminal_graphics_recovery.py','devtools/terminal_graphics_recovery_observer.py','devtools/terminal_graphics_recovery_observer_v2.py')])
    try:r['checks']=validate(folder);r['accepted']=True
    except BaseException as exc:r.update(accepted=False,failure=repr(exc))
    r['evidence']=[identity(x)for x in sorted(folder.iterdir())if x.is_file()]
    r['limits']=dict(session_seconds=5,observation_command_ms=2000,external_containment_seconds=3)
    r['limitations']=['No display/desktop change was made, so this proves actual observation and unchanged state, not successful restoration after a display change.','First attached Win32 display is explicitly the observation target; no D3D adapter association is inferred.','Read-only observer write, inherited repair and gamma-write paths are blocked; native restoration gate remains false.','Actual GAME publication, original platform lifetimes, wait and result consumption still require a separately admitted original-game test.']
    publish(out,r);print(json.dumps(dict(report=identity(out),accepted=r['accepted'],checks=r.get('checks'),failure=r.get('failure'))));raise SystemExit(0 if r['accepted'] else 1)
