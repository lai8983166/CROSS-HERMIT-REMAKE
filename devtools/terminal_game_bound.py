"""Bounded same-owner original GAME publication with display/recovery binding.

Default is plan-only. No screenshots or input injection. A fresh desktop window
and exact offline gate are required for the native path.
"""
from __future__ import annotations
import argparse,copy,gzip,json,os,struct,time
from datetime import datetime,timezone
from pathlib import Path
from devtools.terminal_display_platform import DisplayEngine,DisplayOwner,base,need
from devtools.terminal_display_model import DisplayModel,model_blob,DEVICE
from devtools.terminal_display_platform import decode_snapshot
from devtools.terminal_game_platform import begin_original_game
from devtools.terminal_input_platform import cleanup_after_publication
from devtools.terminal_input_model import CURSOR
from devtools.terminal_recovery_session import RecoverySession,binding_from_snapshot,WATCHED
from devtools.terminal_recovery_binding import authenticate
from devtools.terminal_scene_dc_probe import Owner as CloseObserved
from devtools.terminal_graphics_recovery import created
from devtools import terminal_graphics_desktop as desktop

ROOT=base.ROOT
NATIVE_SECONDS=90
EXTRA_ZERO=('texture_verify_pending','texture_verify_failed','display_bound','display_failed','display_dc')
RUNTIME=ROOT/'.venv-audit/scene-callback-runtime/CROSS HERMIT/CROSS HERMIT'

def cursor_bytes(state):
    c=state['cursor'];return struct.pack('<IIiiiiiiI',c['flags'],c['handle'],*c['position'],*c['clip'],state['last_input_tick'])

def route(engine,owner,baseline,input_snapshot):
    original_call=owner.call;registered=False
    def call(op,*args):
        nonlocal registered
        if op=='INPUT_INSTANCE_INFO' and not registered:
            # Parent baseline predates the visible original window. The input
            # owner baseline is a distinct actual snapshot after mode creation.
            state=input_snapshot();raw=cursor_bytes(state);ptd=engine.native(engine.thread_ptd[0]);saved=original_call('MEM_READ',ptd,116)['hex'];error=original_call('GetLastError')['result']
            token=original_call('MEM_ALLOC',32)['result'];cursor=original_call('MEM_ALLOC',36)['result']
            try:
                need(original_call('MEM_WRITE',token,baseline['baseline_token'])['result']==32,'register exact current recovery token')
                need(original_call('MEM_WRITE',cursor,raw.hex())['result']==36,'actual current owner cursor snapshot')
                need(original_call('INPUT_GATE',1)['result']==1 and original_call('INPUT_BASELINE',token,cursor)['result']==1,'actual input-owner baseline before original input call')
            finally:
                need(original_call('MEM_FREE',cursor)['result']==original_call('MEM_FREE',token)['result']==1,'registration temporaries freed')
                need(original_call('MEM_WRITE',ptd,saved)['result']==116,'registration restores full original native PTD')
                original_call('SetLastError',error)
                need(original_call('MEM_READ',ptd,116)['hex']==saved and original_call('GetLastError')['result']==error,'registration actual PTD/LastError readback')
            registered=True
        return original_call(op,*args)
    owner.call=call
    begin_original_game(engine,owner,0x413450);game=engine.reg('ECX')
    need(owner.call('GFX_GATE',1)['result']==1,'current graphics gate')
    token=owner.call('MEM_ALLOC',32)['result'];owner.call('MEM_WRITE',token,baseline['baseline_token'])
    need(owner.call('GFX_BASELINE',token)['result']==1,'actual parent graphics baseline registered');need(owner.call('MEM_FREE',token)['result']==1,'graphics registration temporary freed')
    engine.stop=0x4506eb;engine.done[0]=False;engine.drive();engine.checkpoint('original_GAME_published_with_bound_display')
    need(engine.reg('EIP')==0x4506eb and engine.word(0x7a49fc)==game and 0x4506e9 in engine.sites and registered,'original GAME store reached naturally')
    engine.run_generator(engine.capture_display(1))
    cleanup=cleanup_after_publication(engine,owner,game)
    for field in EXTRA_ZERO:need(cleanup['status'][field]==0,'new display/texture obligation empty '+field)
    cleanup['zero_fields']=list(cleanup['zero_fields'])+list(EXTRA_ZERO)
    return dict(published_GAME=game,cleanup=cleanup)

def model_baseline():
    from devtools.tests.test_terminal_graphics_desktop import state
    d=decode_snapshot(model_blob(0,0x33000000,0,0x4444));s=state();s['monitors'][0]['device']=DEVICE
    s['monitors'][0]['mode'].update(width=1920,height=1080,bits_per_pixel=32,frequency=60)
    s['display_identities']={DEVICE:d['display_identity']};s['mode_bytes']={DEVICE:d['mode_hex']};s['graphics']=dict(device=DEVICE,gamma_hex=d['gamma_hex'])
    s['cursor']=dict(flags=1,handle=0x7777,position=[200,100],clip=[0,0,1920,1080]);s['system_work_area']=[0,0,1920,1040]
    owner=dict(run_id='explicit-bound-display-model',pid=1,process_created=2,main_tid=101,main_teb=4096)
    b=dict(schema='terminal-graphics-baseline-v1',evidence_kind='model',owner=owner,target_device=DEVICE,state=s);b['baseline_token']=desktop.digest(b);return b

def evidence(engine,owner,baseline,outcome,native):
    return dict(kind='same_owner_bound_GAME_publication',native_executed=native,formal_acceptance=False,formal_progress='2/8',owner=baseline['owner'],baseline=baseline,**outcome,
        native_trace=owner.trace,API_calls=[x for x in engine.records if 'callback_id' not in x],callbacks=engine.callbacks,roots=engine.roots,checkpoints=engine.checkpoints,
        display_snapshots=engine.display_snapshots,texture_verifications=engine.texture_verifications,final=engine.state(),instructions=engine.count,
        instruction_sites=[dict(pc=p,hex=engine.image[p-0x400000:p-0x400000+n].hex(),count=c) for p,(n,c) in sorted(engine.sites.items())],
        worker_created=False,wait_return=False,result_consumed=False,screenshots=False,global_input=False,WinMain_completed=False,independent_full_replay=False)

def save(path,value):
    need(not path.exists() and path.is_relative_to(ROOT/'.venv-audit'),'fresh F evidence')
    raw=gzip.compress(json.dumps(value,separators=(',',':')).encode(),mtime=0);need(len(raw)<16*1024*1024,'bounded16MiB compressed evidence');path.write_bytes(raw);return base.identity(path)

def model(path):
    start=time.monotonic();e=DisplayEngine();template=ROOT/'analysis/school-window-startup-trajectory-v3-20261020.json';need(base.sha(template.read_bytes())=='a5f30898f2add507e70277617838ad51e5328b56915c227460e3bc43f2afcd48','fixed original window template')
    m=DisplayModel(e,json.loads(template.read_text())['cases'][0]);m.engine=e;b=model_baseline();binding=None;outcome={}
    def check(snapshot):
        nonlocal binding
        if snapshot['phase']==0:binding=binding_from_snapshot(snapshot,b)
    e.binding_validator=check
    try:
        outcome=route(e,m,b,lambda:b['state']);r=evidence(e,m,b,outcome,False)
        live=dict(kind='explicit-symbolic-handles',owner=b['owner'],process_wait=0,process_exit=0,job_members=[],same_job=True)
        r['authenticated_release_model']=authenticate(r,b,binding,live,native=False);r['reached']=True
    except BaseException as exc:
        r=evidence(e,m,b,outcome,False);r.update(reached=False,failure=repr(exc))
    r['seconds']=round(time.monotonic()-start,3);r['implementation_pins']=base.implementation_pins();r['limits']=dict(seconds=90,instructions=6000000,compressed_bytes=16*1024*1024)
    return dict(output=save(path,r),reached=r['reached'],failure=r.get('failure'),seconds=r['seconds'],pc=hex(e.reg('EIP')))

class NativeOwner(DisplayOwner,CloseObserved):
    def __setattr__(self,name,value):
        if name=='deadline' and hasattr(self,'start'):value=self.start+NATIVE_SECONDS
        if name=='create':
            actual=value
            def create(*args):
                args=list(args);args[7]=str(RUNTIME);return actual(*args)
            value=create
        super().__setattr__(name,value)
    def call(self,op,*args):
        observer=getattr(self,'observer',None);device=getattr(self,'device_pointer',0);refs=getattr(self,'device_refs',0)
        watched=observer and op in WATCHED and (op!='GFX_RELEASE' or args[0]==device and refs==1)
        if watched:
            q=observer.call('begin',2000,dict(op=op,request_id=self.seq+1));need(q['ok'],'bounded mutation start: '+str(q.get('failure')))
        reply=super().call(op,*args)
        if op=='GFX_CREATE_DEVICE' and reply['result']<0x80000000:self.device_pointer=reply['object'];self.device_refs=1
        elif op=='GFX_ADDREF' and args[0]==device:self.device_refs=reply['remaining_owned_refs']
        elif op=='GFX_RELEASE' and args[0]==device:self.device_refs=reply['remaining_owned_refs']
        if watched:
            q=observer.call('end',2000,reply);need(q['ok'],'bounded mutation end: '+str(q.get('failure')))
        return reply

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--model-out');args=p.parse_args()
    if args.model_out:
        r=model((ROOT/args.model_out).resolve());print(json.dumps(r));return 0 if r['reached'] else 1
    print(json.dumps(dict(mode='plan_only',native_executed=False,native_seconds=90,desktop_seconds=120,normal_recovery_connected=True,interactive_admission=False,reason='Current-owner handle and fault-containment qualification must pass before adding execute entry.')));return 0

if __name__=='__main__':raise SystemExit(main())
