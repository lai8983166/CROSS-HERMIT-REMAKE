"""Failed-run desktop safety proof, separate from normal resource acceptance."""
from __future__ import annotations
import copy,struct
from devtools import terminal_graphics_desktop as d
from devtools.terminal_recovery_binding import authenticated_recover

need=d.need

def receipt_after_exit(report,baseline,binding,live,observations,current):
    need(report['native_executed'] and report['owner']==baseline['owner'],'actual current failed native lifetime')
    need(live['kind']=='retained-native-handles' and live['owner']==baseline['owner'] and live['process_wait']==0 and not live['job_members'] and live['same_job'],'actual process death and retained Job empty; not normal release proof')
    need(binding and binding['baseline_token']==baseline['baseline_token'] and binding['owner']==baseline['owner'],'actual current D3D target binding')
    need(current['input_observer']==baseline['state']['input_observer'] and current['display_identities']==baseline['state']['display_identities'],'same observer/input epoch/display topology')
    before=d._mutable(baseline['state'],baseline['target_device']);now=d._mutable(current,baseline['target_device'])
    known={key:[value] for key,value in before.items()};sources={}
    requests={x['id']:x for x in report['native_trace'] if x['direction']=='request'}
    responses={x['id']:x for x in report['native_trace'] if x['direction']=='response' and 'id' in x}
    begins={x['request_id']:x for x in report['native_trace'] if x.get('event')=='NATIVE_MUTATION_BEGIN'}
    allowed={
        'CreateWindowExA':{'foreground'},'ShowWindow':{'foreground'},
        'GFX_CREATE_DEVICE':{'mode','gamma','cursor_clip','taskbars','work_area','foreground'},
        'GFX_RELEASE':{'mode','gamma','cursor_clip','taskbars','work_area','foreground'},
        'GFX_GAMMA_SET':{'gamma'},'GFX_GAMMA_RESTORE':{'gamma'},
        'INPUT_CURSOR_POS':{'cursor_position'},'INPUT_SHOW_CURSOR':set(),
        'INPUT_CURSOR_RESTORE':{'cursor_position'},'WINDOW_CLOSE':{'foreground'}}
    for item in observations:
        ident=item['request_id'];op=item['op']
        if ident not in requests:
            need(item is observations[-1] and 'after' not in item and ident not in begins,'only untransmitted tail intent may be ignored')
            continue
        need(requests[ident]['op']==op,'safety bracket has actual transmitted current request')
        prior=item['before'];need(prior['input_observer']==baseline['state']['input_observer'] and prior['display_identities']==baseline['state']['display_identities'],'same context before failed run mutation')
        if 'after' in item:
            response=responses.get(ident);need(response and {k:v for k,v in response.items() if k!='direction'}==item['response'],'completed native mutation has exact raw reply')
            post=item['after'];need(post['input_observer']==baseline['state']['input_observer'] and post['display_identities']==baseline['state']['display_identities'],'same context after actual mutation')
            am,bm=d._mutable(prior,baseline['target_device']),d._mutable(post,baseline['target_device'])
            changed={k for k in am if am[k]!=bm[k]};need(changed<=allowed[op],'no unknown API side-effect attribution')
            for key in changed:known[key]=[before[key],copy.deepcopy(bm[key])];sources[key]=dict(request_id=ident,observation=item['sequence'],completed_native_response=True)
        else:
            event=begins.get(ident);need(event and event['op']==op and (event['tid'],event['teb'])==(baseline['owner']['main_tid'],baseline['owner']['main_teb']) and event['baseline_token_hex']==baseline['baseline_token'],'pending intent is insufficient: actual native MAIN BEGIN required')
            need(event['owned_hwnd']==binding['snapshot']['decoded']['hwnd'] and event['window_generation']==binding['snapshot']['decoded']['window_generation'],'BEGIN belongs to original bound window lifetime')
            need(event['pid']==baseline['owner']['pid'] and event['lane']==0 and event['argc']==len(requests[ident]['args']) and all(event['arg'+str(i)]==v for i,v in enumerate(requests[ident]['args'])),'actual native BEGIN carries exact current request arguments')
            # No inferred taskbar/clip/work-area values. Pending calls may only
            # contribute values derivable from their actual native input bytes.
            if op=='GFX_CREATE_DEVICE':
                need(event['data_kind']=='presentation52' and event['data_bytes']==52,'actual complete presentation input')
                pp=struct.unpack('<13I',bytes.fromhex(event['data_hex']));need(pp[0:2]==(1024,768) and pp[6]==event['owned_hwnd'] and pp[7]==0,'actual original fullscreen input')
                mode=copy.deepcopy(before['mode']);mode.update(width=1024,height=768)
                bits={22:32,23:16,24:16,25:16}.get(pp[2]);need(bits is not None,'known exact original display format')
                for key in ('bits_per_pixel','bits','bpp'):
                    if key in mode:mode[key]=bits
                if 'frequency' in mode and pp[11]:mode['frequency']=pp[11]
                known['mode']=[before['mode'],mode];sources['mode']=dict(request_id=ident,native_begin=event,completed_native_response=False)
            elif op in ('GFX_GAMMA_SET','GFX_GAMMA_RESTORE'):
                need(event['data_kind']=='gamma1536' and event['data_bytes']==1536,'actual complete native gamma input')
                d.ramp(event['data_hex']);known['gamma']=[before['gamma'],event['data_hex']];sources['gamma']=dict(request_id=ident,native_begin=event,completed_native_response=False)
            elif op=='INPUT_CURSOR_POS':
                known['cursor_position']=[before['cursor_position'],[struct.unpack('<i',struct.pack('<I',event['arg'+str(i)]))[0] for i in range(2)]];sources['cursor_position']=dict(request_id=ident,native_begin=event,completed_native_response=False)
    mutations={}
    for key,value in now.items():
        need(value in known[key],key+': current value has no independent owned mutation source; no write')
        if value!=before[key]:mutations[key]=value
    return dict(schema='terminal-containment-safety-v1',evidence_kind='native',owner=baseline['owner'],baseline_token=baseline['baseline_token'],events=[],mutations=mutations,
        mutation_sources={key:dict(source_ref=sources[key],owner=baseline['owner'],baseline_token=baseline['baseline_token']) for key in mutations},
        process_exit=live['process_exit'],normal_resource_cleanup_proven=False)

def restore_after_containment(baseline,receipt,backend,inspect):
    def empty():
        value=inspect(require_exit=False);need(value['process_wait']==0 and not value['job_members'],'retained actual process dead and Job empty before safety write');return value
    result=authenticated_recover(baseline,receipt,backend,empty)
    result.update(native_admission=False,normal_resource_cleanup_proven=False,containment_safety_only=True)
    return result
