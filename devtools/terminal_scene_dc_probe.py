"""One bounded original MAIN/GAME case with observed DC retirement and CRT cleanup.

Original instructions/platform returns are retained. Full GAME publication,
scene worker and battle acceptance remain separate requirements.
"""
from __future__ import annotations
import argparse
import gzip
import json
from pathlib import Path
import struct
import time
from devtools import terminal_scene_construction as frozen
from devtools import terminal_scene_dc_native as native

base=frozen.base
ROOT=base.ROOT
need=base.need


def delete_proof(q):
    return bool(q['result'] and q['dc_retired'] and q['before_flush'] and q['before_type']==1
        and q['before_font'] and q['after_flush'] and not q['after_type'] and not q['after_font']
        and not q['baseline_gdi_error'] and not q['before_gdi_error'] and not q['after_gdi_error']
        and q['after_gdi_count']==q['baseline_gdi_count'])


class Owner(base.Owner):
    """Also retain every actual parent-side CloseHandle BOOL, including initial pipes."""
    def __setattr__(self,name,value):
        if name=='w':
            object.__setattr__(self,'parent_closes',[])
            close=value.close
            def observed_close(handle):
                result=close(handle)
                self.parent_closes.append(dict(handle=int(getattr(handle,'value',handle)),result=int(result),before_resume=not getattr(self,'resumed',False)))
                return result
            value.close=observed_close
        super().__setattr__(name,value)


def execute(g,owner):
    g.owner=owner
    g.root('original_heap_init',0x57b9d0,(1,))
    need(g.root('original_TLS_and_lock_init',0x5752d0)==1,'real main TLS ready')
    g.root('WinMain_entry_to_published_MAIN_and_empty_buckets',0x49dd70,(0,0,0,0),stop=0x49de23)
    main=g.word(0x7a4a00);need(main and g.word(main)==0x5986a0,'original MAIN publication and vtable')
    need(g.read(main+0x64,256)==bytes(256),'original scheduler bucket initialization')
    g.checkpoint('original_MAIN_published_before_window_setup')
    retained_stack=g.read(base.cold.old.STACK,65536)
    # Independent factory root; neither a guessed ancestor nor a published GAME.
    g.stack=base.WORK_STACK;output=g.stack+0x100
    g.put(output,struct.pack('<I',0xa5a5a5a5))
    g.root('original_412C70_factory_through_complete_412E30',0x412c70,(0,output,0,0),stop=0x413450)
    game=g.reg('ECX');game_raw,allocation=g.owned(game)
    need(game+0xba20<=game_raw+allocation['bytes'],'current original GAME allocation')
    need(g.word(0x7a49fc)==0 and g.word(output)==0xa5a5a5a5,'GAME not prematurely published')
    need(g.word(g.reg('ESP'))==0x412d06 and 0x412cc2 in g.sites,'constructor returned into original factory')
    need(0x413450 not in g.sites and 0x451080 not in g.sites and g.worker_handle is None,'no device initialization, scene or worker')
    dc=g.word(game+0xb208);need(dc in g.dcs,'original GAME stores actual current DC')
    need(g.read(base.cold.old.STACK,65536)==retained_stack,'pending WinMain stack retained')
    point=g.checkpoint('complete_GAME_constructor_before_platform_initialization')
    point.update(GAME_object=game,GAME_bytes=0xba20,GAME_sha256=base.sha(g.read(game,0xba20)),
                 GAME_DC=dc,GAME_drawing_gate=g.read(game+0xb28e,2).hex(),factory_output=g.word(output),
                 pending_factory_stack_sha256=base.sha(g.read(base.WORK_STACK,65536)))
    pending_factory=g.read(base.WORK_STACK,65536)
    g.stack=0x65600000;g.u.mem_map(g.stack,65536);g.md.topology()
    g.root('supplemental_original_GAME_destructor_and_free',0x412dd0,(1,),game,True)
    need(game_raw not in g.allocations,'original scalar deleting GAME destructor frees allocation')
    deletions=[r for r in g.records if r['name']=='DeleteDC']
    need(len(deletions)==1 and deletions[0]['args']==[dc],'original GAME DeleteDC attempted exactly once')
    point['original_DeleteDC_result']=deletions[0]['value']
    deletion=deletions[0]['native_leaf']
    if deletion['dc_retired']:
        need(delete_proof(deletion),'DeleteDC success AND real invalid object AND baseline GDI count')
        point['DC_retirement']='original_DeleteDC_with_object_evidence'
    else:
        # Only a still-live DC can take the documented supplementary release.
        q=owner.call('DC_INFO',dc)
        need(q['now_type']==1 and q['now_font'] and not q['dc_retired'],'unresolved DC must still be observed live')
        q=owner.call('ReleaseDC',0,dc)
        need(q['result']==1 and q['dc_retired']==1 and q['after_gdi_count']==q['baseline_gdi_count'],'actual supplemental release and count restoration')
        point['DC_retirement']='supplemental_ReleaseDC_with_resource_evidence';point['supplemental_ReleaseDC']=q
    point['DeleteDC_observations']=deletion
    observed=owner.call('DC_INFO',dc);point['DC_after_original_GAME_free']=observed
    need(observed['dc_retired']==1 and observed['now_flush'] and not observed['now_gdi_error'] and observed['now_gdi_count']==observed['baseline_gdi_count'],'independent follow-up current-process DC observation')
    if point['DC_retirement'].startswith('original_'):
        need(not observed['now_type'] and not observed['now_font'],'deleted DC remains invalid after original GAME free')
    g.dcs.remove(dc)
    need(g.read(base.WORK_STACK,65536)==pending_factory,'pending GAME factory stack retained')
    need(g.read(base.cold.old.STACK,65536)==retained_stack,'pending WinMain stack still retained')
    g.root('original_MAIN_destructor',0x44fe60,receiver=main,callee=True)
    g.root('original_MAIN_allocation_free',0x428ad0,(main,))
    g.root('original_MAIN_PTD_free_and_TLS_clear',0x575450,(0,))
    g.root('original_TLS_and_lock_teardown',0x575360)
    g.root('original_heap_teardown',0x57ba60)
    need(not any((g.allocations,g.events,g.locks,g.fonts,g.dcs,g.heap)),'current owner resources explicitly empty')
    g.checkpoint('supplemental_cleanup_complete_globals_not_rewritten')
    status=owner.call('STATUS');need(owner.call('Shutdown')['result']==1,'normal native owner shutdown')
    need(owner.wait(min(1000,max(0,int((owner.deadline-time.monotonic())*1000))))==0,'native owner exited within budget')
    return status


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--execute',action='store_true')
    ap.add_argument('--helper',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    helper=(ROOT/a.helper).resolve();out=(ROOT/a.out).resolve()
    need(helper.is_relative_to(ROOT/'.venv-audit') and out.is_relative_to(ROOT) and not out.exists(),'fresh F output and helper')
    build=json.loads((helper.parent/'static-report.json').read_text())
    for key in ('base_source','parent_generator','generator','generated_source','helper'):
        need(base.identity(ROOT/build[key]['path'])==build[key],'unchanged build input '+key)
    need(base.identity(helper)==build['helper'],'exact requested helper')
    need((ROOT/build['generated_source']['path']).read_bytes()==native.generated_source().encode(),'exact generated observer')
    gate=json.loads((helper.parent/'offline-route.json').read_text())
    need(gate['route_closed'] and not gate['native_executed'],'bounded offline path closed')
    need(gate['collector']==base.identity(Path(__file__)),'offline gate matches this collector')
    g=frozen.SceneEngine()
    r=dict(schema_version=2,kind='original_MAIN_GAME_with_observed_DC_retirement',accepted=False,formal_acceptance=False,
        GAME_published=False,scene_constructed=False,worker_started=False,cooperative_wait_executed=False,first_result_consumption=False,
        independent_full_replay=False,full_WinMain_executed=False,full_GAME_factory_executed=False,
        screen_DC_handle_acquired=False,window_created=False,pixels_read=False,host_input_sent=False,native_executed=False,
        parent_source=base.identity(ROOT/'analysis/terminal-scene-owner-preflight-v1-20261113.json.gz'),
        original=base.identity(base.cold.base.SOURCE),implementation=base.identity(Path(__file__)),build=build,
        helper=base.identity(helper),implementation_pins=base.implementation_pins(),offline_gate=base.identity(helper.parent/'offline-route.json'),
        declaration=g.declaration,initial=g.state(),roots=g.roots,API_calls=g.records,checkpoints=g.checkpoints)
    if a.execute:
        with (helper.parent/'native-attempt.once').open('x') as f:json.dump(dict(helper=base.identity(helper),utc=time.time()),f)
        owner=None
        try:
            owner=Owner.__new__(Owner);Owner.__init__(owner,helper,helper.parent)
            r['status']=execute(g,owner);r['accepted']=True
        except BaseException as exc:r['failure']=repr(exc);r['failure_guest']=dict(state=g.state(),pending=g.pending)
        finally:
            if owner:
                owner.finish();r.update(native_executed=owner.resumed,native_process_created=owner.started,native_trace=owner.trace,
                    events=owner.events,cleanup=owner.receipt,parent_CloseHandle_receipts=owner.parent_closes)
                r['screen_DC_handle_acquired']=any(x.get('op')=='GetDC' for x in owner.trace)
                end=owner.receipt['exits'].get(str(owner.receipt['parent_pid']),{})
                if owner.receipt['forced'] or owner.expired or owner.receipt['errors'] or not owner.receipt['job_empty'] or not owner.receipt['handles_closed'] or end!={'wait':0,'code':0} or not all(x['result']==1 for x in owner.parent_closes) or len(owner.parent_closes)!=7:r['accepted']=False
            r.update(final=g.state(),instruction_sites=[dict(pc=p,hex=g.image[p-0x400000:p-0x400000+n].hex(),count=c) for p,(n,c) in sorted(g.sites.items())],adapter_writes=g.host_writes)
    payload=gzip.compress(json.dumps(r,separators=(',',':')).encode(),mtime=0)
    need(len(payload)<16*1024*1024,'16MiB evidence limit');out.write_bytes(payload)
    print(json.dumps(dict(out=str(out),bytes=len(payload),accepted=r['accepted'],native_executed=r['native_executed'],failure=r.get('failure'))))
    return 0 if not a.execute or r['accepted'] else 1


if __name__=='__main__':raise SystemExit(main())
