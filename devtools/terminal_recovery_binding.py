"""Authenticate current MAIN wire releases before any native recovery write.

No OS calls on import. Historical/model traces can be audited but cannot create a
native permit. A permit also requires the observer's retained process/Job handles.
"""
from __future__ import annotations
import copy
import struct
import types
from devtools import terminal_graphics_desktop as frozen

need=frozen.need

def paired(trace, owner):
    pending={}; result=[]; last=0
    for index,row in enumerate(trace):
        if row['direction']=='request':
            need(row['id']==last+1 and row['lane']==0,'ordered current MAIN requests')
            last=row['id'];pending[last]=(index,row)
        elif row['direction']=='response' and 'id' in row:
            need(row['id'] in pending,'one actual response per request')
            start,q=pending.pop(row['id'])
            need(row['lane']==0 and (row['tid'],row['teb'])==(owner['main_tid'],owner['main_teb']) and row['ok']==1,'same live MAIN response')
            result.append((start,index,q,row))
        elif row['direction']=='callback':
            need(row['parent_request'] in pending and (row['tid'],row['teb'])==(owner['main_tid'],owner['main_teb']),'callback belongs to pending actual MAIN request')
        else:
            need(row['direction']=='response' and 'event' in row,'known raw wire record')
    need(not pending,'all wire requests have real replies')
    return sorted(result)

def authenticate(report, baseline, binding, live, *, native):
    """Reconstruct releases from raw request/response pairs, not summary flags."""
    owner=baseline['owner']; token=baseline['baseline_token']
    need(frozen.digest({k:v for k,v in baseline.items() if k!='baseline_token'})==token,'unchanged registered baseline')
    need(report['native_executed'] is native and report['owner']==owner,'explicit evidence class and exact process lifetime')
    need(binding['baseline_token']==token and binding['owner']==owner and binding['target_device']==baseline['target_device'],'same bound D3D target and baseline')
    need(binding['validated'] is True,'decoded D3D monitor identity required')
    need(live['owner']==owner and live['process_wait']==0 and live['process_exit']==0 and live['job_members']==[] and live['same_job'] is True,'retained current process exit0 and actual empty Job')
    if native:need(live['kind']=='retained-native-handles' and baseline['evidence_kind']=='native','no model permit for native writes')
    rows=paired(report['native_trace'],owner)
    def allop(name):return [r for r in rows if r[2]['op']==name]
    def one(name):
        out=allop(name);need(len(out)==1,'exactly one '+name);return out[0]
    def source(row):return dict(request=row[2]['id'],request_sha256=frozen.digest(row[2]),response_sha256=frozen.digest(row[3]))
    displays=report['display_snapshots']
    need(len(displays)==3 and [x['phase'] for x in displays]==[0,1,2],'three actual display lifetime observations')
    from devtools.terminal_display_platform import decode_snapshot
    for snapshot in displays:
        need(snapshot['accepted'] and snapshot['temporary_freed'] and snapshot['CPU57_before']==snapshot['CPU57_after'] and len(snapshot['CPU57_before'])==57,'display observation complete state/temporary cleanup')
        need(decode_snapshot(bytes.fromhex(snapshot['blob_hex']))==snapshot['decoded'],'actual display blob decoded without substitution')
        found=[x for x in rows if x[2]['id']==snapshot['receipt']['id']];need(len(found)==1,'display source has one actual wire response');observed=found[0]
        need({k:v for k,v in observed[3].items() if k!='direction'}==snapshot['receipt'],'display receipt equals original wire')
        need(observed[2]['op']==('DISPLAY_BIND' if snapshot['phase']==0 else 'DISPLAY_STATE'),'actual phase command')
        output=observed[2]['args'][-1]
        reads=[x for x in rows if x[0]>observed[1] and x[0]<snapshot['wire_end'] and x[2]['op']=='MEM_READ' and x[2]['args']==[output,16204]]
        need(len(reads)==1 and reads[0][3]['result']==16204 and reads[0][3]['hex']==snapshot['blob_hex'],'complete actual readback from current owned display output')
        need(snapshot['receipt']['baseline_token_hex']==token and snapshot['decoded']['target_device']==binding['target_device'] and snapshot['decoded']['display_identity']==binding['snapshot']['decoded']['display_identity'],'same registered display across release')
    need(displays[0]['blob_hex']==binding['snapshot']['blob_hex'],'current raw D3D binding is the observer registered binding')
    registered=one('GFX_BASELINE');reg=registered[3];hwnd=reg['hwnd']
    need(reg['result']==1 and reg['pid']==owner['pid'] and reg['baseline_token_hex']==token and reg['registration_only']==1,'actual baseline registration')
    creates=allop('CreateWindowExA');need(len(creates)==1 and creates[0][3]['result']==hwnd,'one current HWND creation source')
    window=dict(hwnd=hwnd,generation=creates[0][3]['window_generation'])
    need(window['generation']>0 and binding['snapshot']['decoded']['hwnd']==hwnd and binding['snapshot']['decoded']['window_generation']==window['generation'],'real current window generation')
    inp={};gfx={};locks=set();blocks=set();input_releases=[];unacquires=[];gamma=None
    for row in rows:
        q,r=row[2:];op=q['op'];args=q['args']
        if op in ('INPUT_CREATE','INPUT_DEVICE') and r['result']<0x80000000:
            obj=r['object'];need(obj and obj not in inp,'fresh input object');inp[obj]=dict(kind=r['kind'],unacquired=False)
        elif op=='INPUT_UNACQUIRE':
            obj=args[0];need(obj in inp and inp[obj]['kind']!=20 and r['result'] in (0,1) and r['unacquired']==1 and r['acquired']==0,'actual device Unacquire')
            inp[obj]['unacquired']=True;unacquires.append(row)
        elif op=='INPUT_RELEASE':
            obj=args[0];need(obj in inp and (inp[obj]['kind']==20 or inp[obj]['unacquired']),'release actual current unacquired object')
            need(r['result']==r['native_remaining_refs']==r['remaining_owned_refs']==0 and r['window_alive']==1 and r['hwnd']==hwnd,'actual zero input Release with live original HWND')
            del inp[obj];input_releases.append(row)
        elif op=='GFX_FACTORY' and r['result'] or op in ('GFX_CREATE_DEVICE','GFX_GET_FACTORY','GFX_BACKBUFFER','GFX_TEXTURE','GFX_TEXTURE_SURFACE','GFX_VERTEX_BUFFER') and r['result']<0x80000000:
            obj=r['object'];need(obj,'nonzero created graphics object');gfx[obj]=gfx.get(obj,0)+1
        elif op in ('GFX_ADDREF','GFX_RELEASE'):
            obj=args[0];need(obj in gfx,'release/AddRef known graphics identity')
            gfx[obj]+=1 if op=='GFX_ADDREF' else -1
            need(gfx[obj]>=0 and r['remaining_owned_refs']==gfx[obj],'independently reconstructed graphics references')
            if not gfx[obj]:
                need(obj not in locks,'no released locked texture')
                if r['kind'] in (10,11):need(r['result']==0,'actual final device/factory Release0')
                del gfx[obj]
        elif op=='GFX_LOCK' and r['result']<0x80000000:need(args[0] not in locks,'one original lock');locks.add(args[0])
        elif op=='GFX_UNLOCK' and r['result']<0x80000000:need(args[0] in locks,'original lock exists');locks.remove(args[0])
        elif op=='GFX_END' and r['result']<0x80000000:
            reads=[x for x in rows if x[0]>row[1] and x[2]['op']=='MEM_READ' and x[2]['args']==[args[1],4]]
            need(reads and reads[0][3]['result']==4,'actual state-block output readback')
            block=struct.unpack('<I',bytes.fromhex(reads[0][3]['hex']))[0]
            need(block and block not in blocks and ('token' not in r or r['token']==block),'actual new state block token');blocks.add(block)
        elif op=='GFX_DELETE_BLOCK' and r['result']<0x80000000:need(args[1] in blocks,'owned state block');blocks.remove(args[1])
        elif op=='GFX_GAMMA_RESTORE':
            need(gamma is None and r['gamma_restored']==1 and r['gamma_dirty']==0 and r['baseline_token_hex']==token,'one actual original gamma restoration')
            frozen.ramp(r['gamma_after_hex']);gamma=row
        if op in ('INPUT_UNACQUIRE','INPUT_RELEASE','INPUT_CURSOR_RESTORE','GFX_GAMMA_RESTORE','GFX_RELEASE'):
            need(r['baseline_token_hex']==token and r['display_window_generation']==window['generation'],'release bound to current registered window generation')
    need(len(unacquires)==2 and len(input_releases)==3 and not inp and not gfx and not locks and not blocks,'complete independent input/graphics/lock/block ledger zero')
    need(gamma is not None,'actual device gamma restoration present')
    cursor=one('INPUT_CURSOR_RESTORE');c=cursor[3]
    need(c['result']==c['actual_readback']==1 and c['show_delta_bits']==0 and c['show_count_bits']==c['initial_show_count_bits'],'owner cursor count balanced with actual readback')
    values=struct.unpack('<IIiiiiiiI',bytes.fromhex(c['cursor_hex']));b=baseline['state'];input_baseline=one('INPUT_BASELINE')[3]
    need(input_baseline['result']==1 and input_baseline['observed']==1 and input_baseline['baseline_token_hex']==token and input_baseline['cursor_hex']==c['cursor_hex'],'all 36 actual owner cursor baseline bytes restored')
    need(values[-1]==b['last_input_tick'],'same user-input epoch across parent and input-owner baselines')
    runtime=one('GFX_RUNTIME_CLOSE');need(runtime[3]['result']==1 and runtime[3]['remaining_load_refs']==0,'actual graphics DLL releases')
    destroy=one('CB_DESTROY_WINDOW');need(destroy[2]['args'][1]==hwnd and destroy[3]['result']==1 and destroy[3]['is_window_after']==0 and destroy[3]['ncdestroy_observed']==1,'actual original DestroyWindow success')
    close=one('WINDOW_CLOSE');need(close[3]['window_generation']==window['generation'] and close[3]['is_window_after']==0 and close[3]['ncdestroy_observed']==close[3]['quit_posted']==close[3]['property_removed']==1,'complete original window close observations')
    status=one('STATUS');shutdown=one('Shutdown')
    zero=report['cleanup']['zero_fields']
    required={'allocations','memory_bytes','heaps','handles','criticals','tls_slots','fonts','dcs','windows','gfx_refs','gfx_locks','gfx_blocks','gfx_interfaces','gfx_dcs','gfx_bitmaps','gfx_fonts','gfx_gamma_dirty','input_interfaces','input_modules','texture_verify_pending','texture_verify_failed','display_bound','display_failed','display_dc'}
    need(required<=set(zero),'complete required zero-field contract')
    need(all(status[3][k]==0 for k in zero) and shutdown[3]['result']==1,'raw final status and normal Shutdown')
    order=[max(x[1] for x in unacquires),max(x[1] for x in input_releases),cursor[1],gamma[1],runtime[1],destroy[1],close[1],status[1],shutdown[1]]
    # The original cleanup interleaves device Unacquire/Release; require each
    # pair locally and final input completion before all graphics retirement.
    need(order[0]<order[1]<order[2]<order[3]<order[4]<order[5]<order[6]<order[7]<order[8],'actual input/gamma/graphics/window/CRT/Shutdown ordering')
    v=report['texture_verifications'];need(len(v)==2 and all(x['accepted'] and x['temporary_freed'] and x['CPU57_restored'] and x['CPU57_before']==x['CPU57_after'] and len(x['CPU57_before'])==57 for x in v),'both complete supplemental texture verifications')
    from devtools.terminal_texture_platform import validate_receipt,logical_pixels
    import hashlib
    by_id={x[2]['id']:x for x in rows}
    for proof in v:
        original=by_id[proof['original_unlock_request']];verify=by_id[proof['receipt']['id']]
        need(original[2]['op']=='GFX_UNLOCK' and original[3]['result']<0x80000000 and verify[2]['op']=='TEX_VERIFY' and verify[0]>original[1],'independent texture lock follows actual successful original unlock')
        obj,generation,output=verify[2]['args'];need(original[2]['args'][0]==obj and generation==proof['source_generation']==original[3]['unlocked_generation'],'exact current texture object/generation')
        need({k:val for k,val in verify[3].items() if k!='direction'}==proof['receipt'],'texture proof equals actual raw reply')
        validate_receipt(verify[3],generation,bytes.fromhex(verify[3]['ptd_before_hex']),original[3]['last_error'])
        pieces=[]
        for offset in range(0,131072,32768):
            reads=[x for x in rows if verify[1]<x[0]<proof['wire_end'] and x[2]['op']=='MEM_READ' and x[2]['args']==[output+offset,32768]]
            need(len(reads)==1 and reads[0][3]['result']==32768,'four actual fresh texture-readback chunks');pieces.append(bytes.fromhex(reads[0][3]['hex']))
        actual=b''.join(pieces);need(len(actual)==131072,'complete actual logical texture pixels')
        lock=max(x[0] for x in rows if x[0]<original[0] and x[2]['op']=='GFX_LOCK' and x[2]['args'][0]==obj)
        uploads=[x for x in rows if lock<x[0]<original[0] and x[2]['op']=='GFX_LOCK_WRITE' and x[2]['args'][0]==obj]
        uploaded=bytearray();position=0
        for item in uploads:
            _,offset,buffer,size=item[2]['args'];need(offset==position and item[3]['result']==size,'contiguous actual writable-lock uploads')
            writes=[x for x in rows if lock<x[0]<item[0] and x[2]['op']=='MEM_WRITE' and x[2]['args'][0]==buffer]
            need(writes and writes[-1][3]['result']==size,'actual upload source memory write');chunk=bytes.fromhex(writes[-1][2]['args'][1]);need(len(chunk)==size,'complete actual upload source');uploaded.extend(chunk);position+=size
        expected=logical_pixels(bytes(uploaded),proof['source_pitch']);need(actual==expected,'actual pixels persisted across original Unlock and independent readonly Lock')
        digest=hashlib.sha256(actual).hexdigest();need(digest==proof['observed_logical_sha256']==proof['expected_logical_sha256'],'reported pixel hashes match reconstructed raw bytes')
    events=[]
    for kind,row in [('input_unacquire',unacquires[-1]),('input_release',input_releases[-1]),('graphics_gamma_restore',gamma),('graphics_release',runtime),('window_destroy',destroy)]:
        events.append(dict(kind=kind,seq=row[1],observed=True,source_ref=source(row),baseline_token=token,window_alive=True,main_tid=owner['main_tid'],main_teb=owner['main_teb'],window_identity=window))
    events[0]['hresults']=[x[3]['result'] for x in unacquires];events[1].update(remaining_refs=0,objects=3)
    saved=one('GFX_GAMMA_SAVE')[3]['gamma_after_hex'];need(saved==gamma[3]['gamma_after_hex'],'actual device saved gamma restored exactly')
    events[2].update(device_alive=True,saved_hex=saved,readback_hex=gamma[3]['gamma_after_hex']);events[3].update(remaining_refs=0,live_resources=0,locked_resources=0)
    events[4].update(is_window=False,destroy_result=1);events.append(dict(kind='job_empty',seq=len(report['native_trace'])+1,observed=True,source_ref=copy.deepcopy(live),baseline_token=token,active_processes=0))
    return dict(schema=frozen.SCHEMA,evidence_kind='native' if native else 'model',owner=owner,window_identity=window,baseline_token=token,events=events,owner_cursor_receipt=dict(source_ref=source(cursor),main_tid=owner['main_tid'],main_teb=owner['main_teb'],net_showcursor_delta=0,flags=values[0],handle=values[1]),mutations={},mutation_sources={})

def authenticated_recover(baseline,receipt,backend,check_live,*,sleep=None):
    """Local function bindings; never open the frozen module's global gate."""
    need(backend.evidence_kind=='native' and receipt['evidence_kind']=='native','native recovery permit only')
    expected=frozen.digest(receipt);namespace=dict(vars(frozen),NATIVE_ADMISSION=True)
    def validate(value,old,*,evidence_kind):
        need(frozen.digest(value)==expected and old is baseline,'immutable authenticated receipt')
        need(evidence_kind=='native' and value['owner']==old['owner'] and value['baseline_token']==old['baseline_token'],'exact authenticated native owner')
        check_live();return {x['kind']:x for x in value['events']}
    namespace['validate_release_receipt']=validate
    def context(before,state,device):
        # Parent cursor shape is determined by the window under its restored
        # position. Do not write an opaque foreign HCURSOR. Require both final
        # observations to match; the input owner's own count is authenticated.
        temporary=copy.deepcopy(before);temporary['cursor']['flags']=state['cursor']['flags'];temporary['cursor']['handle']=state['cursor']['handle']
        frozen._context(temporary,state,device)
    namespace['_context']=context
    run=types.FunctionType(frozen.recover.__code__,namespace,argdefs=frozen.recover.__defaults__)
    run.__kwdefaults__=frozen.recover.__kwdefaults__.copy()
    backend.authorize(baseline,receipt,check_live)
    try:
        result=run(baseline,receipt,backend,**({'sleep':sleep} if sleep else {}));result['native_admission']=True
        final=result['observations'][-2:]
        cursor_ok=len(final)==2 and all(x['cursor']==baseline['state']['cursor'] for x in final)
        result['final_parent_cursor_equal_twice']=cursor_ok
        if not cursor_ok:result.update(restored=False,error=result['error'] or 'original parent cursor not restored in both final readbacks')
        return result
    finally:backend.disarm()
