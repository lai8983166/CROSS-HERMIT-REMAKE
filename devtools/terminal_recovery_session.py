"""Versioned bound-recovery protocol, reusing the frozen external supervisor."""
from __future__ import annotations
import argparse
import copy
import gzip
import hashlib
import json
import os
from pathlib import Path
import time
from devtools import terminal_graphics_recovery as parent
from devtools import terminal_graphics_desktop as frozen
from devtools.terminal_recovery_binding import authenticate,authenticated_recover

ROOT,need=parent.ROOT,parent.need
PARENT_SHA='4b8dab2856786b972d617aa54e7f745b594c6200123b06decfd05a8db27ad35c'

def adapted():
    data=Path(parent.__file__).read_bytes();need(hashlib.sha256(data).hexdigest()==PARENT_SHA,'frozen external supervisor source')
    source=data.decode()
    def replace(old,new,count):
        nonlocal source
        need(source.count(old)==count,'exact supervisor extension '+old[:50]);source=source.replace(old,new)
    replace("'devtools.terminal_graphics_recovery'","'devtools.terminal_recovery_session'",2)
    replace("('model','native-readonly')","('model','native-readonly','native-bound')",3)
    replace("MAX_COMMANDS=8","MAX_COMMANDS=64",1)
    replace("backend='model'):","backend='model',absolute_deadline_ns=None):",1)
    replace("controller_created=creation,implementation_sha256=", "controller_created=creation,absolute_deadline_ns=absolute_deadline_ns,implementation_sha256=",1)
    replace("deadline=start+int(cfg['lifetime_seconds']*1e9);", "deadline=min(start+int(cfg['lifetime_seconds']*1e9),cfg.get('absolute_deadline_ns') or (2**63-1));",1)
    replace("else ('baseline','readback','close')","else ('baseline','bind','begin','end','recover','containment','readback','close') if cfg['backend']=='native-bound' else ('baseline','readback','close')",1)
    replace("maximum=20000 if q['op']=='recover' else 5000","maximum=20000 if q['op'] in ('recover','containment') else 5000",1)
    replace("result['native_observation_commands_completed']+=", "result['desktop_writes']+=r.get('desktop_writes',0)\n            if command['op']=='recover':result['desktop_restored']=bool(r.get('ok') and r.get('value',{}).get('restored'))\n            result['native_observation_commands_completed']+=",1)
    namespace=dict(__name__='devtools._bound_recovery_core',__file__=__file__)
    exec(compile(source,str(Path(__file__).resolve())+'[frozen-supervisor-adapter]','exec'),namespace)
    oldpins=namespace['implementation_pins']
    def pins():
        extra=['devtools/terminal_recovery_session.py','devtools/terminal_recovery_binding.py','devtools/terminal_recovery_native.py','devtools/terminal_recovery_admission.py','devtools/terminal_recovery_containment.py','devtools/terminal_game_bound.py','devtools/terminal_game_bound_native.py','devtools/terminal_display_platform.py','devtools/terminal_display_native.py','devtools/terminal_display_native.inc','devtools/terminal_display_native_v2.py','devtools/terminal_display_mutation.inc']
        return oldpins()+[dict(path=n,bytes=(ROOT/n).stat().st_size,sha256=hashlib.sha256((ROOT/n).read_bytes()).hexdigest()) for n in extra]
    namespace['implementation_pins']=pins
    return namespace

def binding_from_snapshot(snapshot,baseline):
    from devtools.terminal_display_platform import decode_snapshot
    d,r=snapshot['decoded'],snapshot['receipt'];target=d['target_device']
    need(decode_snapshot(bytes.fromhex(snapshot['blob_hex']))==d,'decoded binding matches complete original observation bytes')
    need(snapshot['phase']==0 and r['baseline_token_hex']==baseline['baseline_token'],'actual initial D3D snapshot for registered token')
    need(target==baseline['target_device'],'D3D adapter0 exactly matches pre-device recovery target')
    need(d['display_identity']==baseline['state']['display_identities'][target],'exact D3D monitor and Win32 hardware identities')
    need(d['mode_hex']==baseline['state']['mode_bytes'][target] and d['gamma_hex']==baseline['state']['graphics']['gamma_hex'],'pre-device actual mode/gamma equal original observer baseline')
    need((r['tid'],r['teb'])==(baseline['owner']['main_tid'],baseline['owner']['main_teb']),'binding belongs to current MAIN')
    return dict(validated=True,baseline_token=baseline['baseline_token'],owner=baseline['owner'],target_device=target,snapshot=copy.deepcopy(snapshot))

WATCHED={'CreateWindowExA','ShowWindow','GFX_CREATE_DEVICE','GFX_GAMMA_SET','GFX_GAMMA_RESTORE','GFX_RELEASE','INPUT_CURSOR_POS','INPUT_SHOW_CURSOR','INPUT_CURSOR_RESTORE','WINDOW_CLOSE'}

def attribute_mutations(receipt,baseline,observations,report):
    from devtools.terminal_recovery_binding import paired
    pairs={x[2]['id']:x for x in paired(report['native_trace'],baseline['owner'])}
    original=frozen._mutable(baseline['state'],baseline['target_device']);mutations={};sources={}
    for item in observations:
        need(item['op'] in WATCHED and item['request_id'] in pairs and 'after' in item,'completed actual mutation bracket')
        row=pairs[item['request_id']];need(row[2]['op']==item['op'] and {k:v for k,v in row[3].items() if k!='direction'}==item['response'],'bracket bound to exact raw API response')
        a,b=item['before'],item['after'];device=baseline['target_device']
        need(a['input_observer']==b['input_observer']==baseline['state']['input_observer'],'no new user input during original API mutation')
        need(a['display_identities']==b['display_identities']==baseline['state']['display_identities'],'unchanged physical target identity')
        am,bm=frozen._mutable(a,device),frozen._mutable(b,device)
        changed={k for k in am if am[k]!=bm[k]}
        allowed={
            'CreateWindowExA':{'foreground'},'ShowWindow':{'foreground'},
            'GFX_CREATE_DEVICE':{'mode','gamma','cursor_clip','taskbars','work_area','foreground'},
            'GFX_RELEASE':{'mode','gamma','cursor_clip','taskbars','work_area','foreground'},
            'GFX_GAMMA_SET':{'gamma'},'GFX_GAMMA_RESTORE':{'gamma'},
            'INPUT_CURSOR_POS':{'cursor_position'},'INPUT_SHOW_CURSOR':set(),
            'INPUT_CURSOR_RESTORE':{'cursor_position'},'WINDOW_CLOSE':{'foreground'}}[item['op']]
        need(changed<=allowed,'unexplained side effects outside actual API scope')
        if 'mode' in changed and item['op']=='GFX_CREATE_DEVICE':need(bm['mode']['width']==1024 and bm['mode']['height']==768,'actual original fullscreen mode only')
        for key in changed:
            mutations[key]=copy.deepcopy(bm[key]);sources[key]=dict(source_ref=dict(bracket=item['sequence'],request_id=item['request_id'],response_sha256=frozen.digest(item['response']),before_sha256=frozen.digest(a),after_sha256=frozen.digest(b)),owner=baseline['owner'],baseline_token=baseline['baseline_token'])
    receipt['mutations']=mutations;receipt['mutation_sources']=sources
    return receipt

def bound_worker(folder,core):
    from devtools.terminal_recovery_native import BoundWindowsBackend,RetainedOwner
    folder=parent.folder_path(folder);cfg=parent.read(folder/'config.json');core['verify_implementations'](cfg)
    baseline=None;binding=None;retained=None;observations=[];active=None;sequence=0;operation=0;writes=0
    def journal(phase,kind):
        nonlocal operation,writes
        operation+=1;need(operation<=256,'bounded native recovery journal')
        if phase=='begin' and kind.startswith('write:'):writes+=1
        row=dict(seq=operation,phase=phase,operation=kind,pid=os.getpid(),at_ns=time.monotonic_ns())
        with (folder/'operations.jsonl').open('ab') as f:f.write((json.dumps(row)+'\n').encode());f.flush();os.fsync(f.fileno())
    backend=BoundWindowsBackend(journal)
    try:
        while sequence<64:
            arm=folder/f'armed-{sequence+1}.json'
            if not arm.exists():time.sleep(.005);continue
            q=parent.read(folder/f'request-{sequence+1}.json');a=parent.read(arm);sequence+=1
            need(a['token']==q['token']==cfg['token'] and a['seq']==q['seq']==sequence and a['request_sha256']==parent.digest(q) and time.monotonic_ns()<a['deadline_ns'],'current externally armed command')
            reply=dict(seq=sequence,token=cfg['token'],request_sha256=parent.digest(q),worker_pid=os.getpid(),backend='native-bound',desktop_writes=0)
            previous_writes=writes
            try:
                op=q['op'];payload=q.get('payload',{})
                if op=='baseline':
                    need(baseline is None and retained is None,'one current native owner')
                    retained=RetainedOwner(payload,cfg['controller_pid'],cfg['controller_created'])
                    journal('begin','baseline');first=backend.first();baseline=frozen.capture_baseline(backend,first['graphics']['device'],retained.owner);journal('end','baseline');value=baseline
                elif op=='bind':
                    need(baseline is not None and binding is None,'one D3D binding')
                    binding=binding_from_snapshot(payload,baseline);value=binding
                elif op in ('begin','end','readback'):
                    need(baseline is not None,'original baseline required');journal('begin','read:'+op)
                    state=backend.read(baseline['target_device'],foreground_identity=baseline['state']['foreground_identity']);journal('end','read:'+op)
                    if op=='begin':
                        need(active is None and payload['op'] in WATCHED and len(observations)<20,'bounded original mutation begin')
                        active=dict(sequence=len(observations)+1,op=payload['op'],request_id=payload['request_id'],before=state);observations.append(active)
                    elif op=='end':
                        need(active is not None and payload['id']==active['request_id'],'current matching mutation end');active.update(after=state,response=payload);active=None
                    value=dict(state=state)
                elif op in ('recover','containment'):
                    need(baseline is not None and binding is not None and (op=='containment' or active is None),'complete binding and mutation brackets')
                    source=payload['report'];path=(ROOT/source['path']).resolve();need(path.is_relative_to(folder.parent) and path.suffix=='.gz' and source['bytes']<=16*1024*1024,'bounded current F report')
                    raw=path.read_bytes();need(len(raw)==source['bytes'] and hashlib.sha256(raw).hexdigest()==source['sha256'],'exact native release report')
                    with gzip.open(path,'rb') as f:decoded=f.read(64*1024*1024+1)
                    need(len(decoded)<=64*1024*1024,'bounded decompressed current report');report=json.loads(decoded)
                    if op=='recover':
                        live=retained.inspect();receipt=authenticate(report,baseline,binding,live,native=True)
                        attribute_mutations(receipt,baseline,observations,report)
                        value=authenticated_recover(baseline,receipt,backend,retained.inspect)
                    else:
                        from devtools.terminal_recovery_containment import receipt_after_exit,restore_after_containment
                        live=retained.inspect(require_exit=False)
                        state=backend.read(baseline['target_device'],foreground_identity=baseline['state']['foreground_identity'])
                        receipt=receipt_after_exit(report,baseline,binding,live,observations,state)
                        value=restore_after_containment(baseline,receipt,backend,retained.inspect)
                    audit=json.dumps(dict(receipt=receipt,report=source,live=live,observations=observations),separators=(',',':')).encode();need(len(audit)<4*1024*1024,'bounded authenticated desktop journal')
                    with (folder/('authenticated-release.json.gz' if op=='recover' else 'containment-safety.json.gz')).open('xb') as f:f.write(gzip.compress(audit,mtime=0))
                else:
                    need(op=='close','only declared bound operations')
                    closed=retained.close() if retained else [];parent.publish(folder/'retained-handles-close.json',dict(handles=closed));retained=None;value=dict(closed=True)
                reply.update(ok=True,value=value)
            except BaseException as exc:reply.update(ok=False,failure=repr(exc))
            reply.update(completed_ns=time.monotonic_ns(),desktop_writes=writes-previous_writes);parent.publish(folder/f'response-{sequence}.json',reply)
            if q['op']=='close':return 0
        return 38
    finally:
        if retained:retained.close()

CORE=adapted()
original_worker=CORE['worker']
def worker(folder):
    cfg=parent.read(parent.folder_path(folder)/'config.json')
    return bound_worker(folder,CORE) if cfg['backend']=='native-bound' else original_worker(folder)
CORE['worker']=worker

class RecoverySession(CORE['RecoverySession']):
    def request(self,op,timeout_ms=5000,payload=None):
        need(not self.finished and self.process.poll() is None and self.pending is None,'live serial bound supervisor');self.seq+=1
        q=dict(seq=self.seq,token=self.token,op=op,timeout_ms=timeout_ms,created_ns=time.monotonic_ns(),payload=payload or {})
        parent.publish(self.folder/f'request-{self.seq}.json',q);self.pending=q;return q
    def call(self,op,timeout_ms=5000,payload=None):return self.collect(self.request(op,timeout_ms,payload))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);g=parser.add_mutually_exclusive_group(required=True);g.add_argument('--supervisor');g.add_argument('--worker');args=parser.parse_args()
    raise SystemExit(CORE['supervisor'](args.supervisor) if args.supervisor else worker(args.worker))
