"""Independent complete world combat cycle and fresh original replay proof."""
import argparse
from copy import deepcopy
import gzip
import json
import struct
from concurrent.futures import ProcessPoolExecutor
from tools import battle_world_update_verification as prior
from tools.battle_world_combat import corpus,validate,pages,expand,validate_pages,settled
from tools.battle_world_combat_model import Model
from tools.battle_world_combat_emulation import CombatMachine,ROOT,CTRL,UNIT,TARGET,RECORD,ANIM,REGIONS,source_contract,need,sha


def state(actual,m,label):
    expected=pages(m.state())
    if actual!=expected:
        keys=[k for k in expected if actual.get(k)!=expected[k]]
        raise ValueError('independent world combat '+m.cycle['name']+' '+label+' '+str(keys))


def nested(f):
    calls=f['nested_calls']
    for entry,ret,n in ((0x475700,0x46B7E1,1),(0x482A30,0x46B86D,2),(0x4918D0,0x46B87D,2),(0x493450,0x46B889,1)):
        expected=[]
        for u in f['unit_calls']:
            if entry!=0x475700 and u['result']==1:continue
            expected.append(dict(entry=entry,receiver=CTRL,caller=ret,args=[u['unit']]+([u['index']] if n==2 else [])))
        need([c for c in calls if c['entry']==entry]==expected,'natural complete unit child caller '+hex(entry))
    direct=[c for c in calls if c['entry']==0x40A100 and c['caller'] in (0x46B80C,0x46B85B)]
    expected=[]
    for u in f['unit_calls']:
        if u['result']==1:continue
        base=u['unit'];expected.append(dict(entry=0x40A100,receiver=ANIM if base==UNIT else (ANIM if bytes.fromhex(u['before']['target'])[0x44:0x48]==struct.pack('<I',ANIM) else 0x12622000),caller=0x46B80C,args=[base+0x48]))
        expected.extend(dict(entry=0x40A100,receiver=0x12620000,caller=0x46B85B,args=[base+0xA0+i*88]) for i in range(5))
    need(direct==expected,'original main/five auxiliary animation calls inside unit roots')
    for c in calls:
        if c['entry']==0x48AAE0:need(c['caller']==0x482CF2 and c['receiver']==CTRL and c['args'][:2]==[UNIT,TARGET],'natural effect caller and actors')


def verify_case(row,replay=True):
    cfg=row['input'];validate(cfg);m=Model(cfg)
    for key,h in row['blobs'].items():
        b=bytes.fromhex(h);need(0<len(b)<=4096 and sha(b)==key,'every retained original page identity')
    validate_pages(row,row['blobs'])
    tb=row['target_bind'];state(tb['before'],m,'target bind before');prior.prior.root(tb['call'],0x467020,CTRL,[TARGET,m.combat['job']]);m.bind_target();state(tb['after'],m,'target bind after')
    need(len(row['roots'])==2,'two packet initializers')
    for call,off in zip(row['roots'],(0x2F4,0x3E0)):prior.prior.root(call,0x437C90,prior.prior.FINE,[UNIT+off]);m.clear_packet(off)
    state(row['bind_before'],m,'actor bind before');prior.prior.root(row['bind'],0x467020,CTRL,[UNIT,m.combat['job']]);m.bind();state(row['bind_after'],m,'actor bind after')
    request=row['request'];state(request['before'],m,'request before');prior.prior.root(request['call'],0x475270,CTRL,[UNIT,6]);m.put(0x292,6,'B');state(request['after'],m,'request after')
    frames=row['world_frames'];need(1<len(frames)<=cfg['budget'],'bounded complete world cycle')
    stopped=False;terminal=None
    for i,f in enumerate(frames):
        need(f['index']==i,'continuous world combat frames');state(f['before'],m,'frame '+str(i)+' before');prior.prior.root(f['call'],0x46B470,CTRL,[])
        need(f['call']['result']==f['call']['cpu_after']['EAX']==0,'natural whole world return')
        need(f['scanned_slots']==[UNIT+j*0x520 for j in range(250)],'all 250 original slots in order')
        need([(s['unit'],s['index'],s['caller']) for s in f['unit_calls']]==[(UNIT,0,0x46B584),(TARGET,1,0x46B584)],'two naturally dispatched used slots')
        need([s['name'] for s in f['stages']]==['before_units','after_units','world_return'],'three exact world frontiers')
        need(f['entries']==[0x46B470,0x4678C0,0x493630,0x467B60,0x46E9C0,0x49B180,0x46E520,0x46E730,0x48CD90,0x46EA10,0x46F440,0x490FC0,0x49CC60,0x49C400,0x466880,0x493A30,0x48CE60],'whole original world pre/post helper order')
        m.pre();state(f['stages'][0]['state'],m,'frame '+str(i)+' pre')
        for call in f['unit_calls']:
            prior.prior.full_cpu(call);state(call['before'],m,'frame '+str(i)+' unit '+hex(call['unit'])+' before')
            result=m.unit_update(call['unit']);need(call['result']==call['cpu_after']['EAX']==result,'nested source unit result '+str((i,hex(call['unit']),call['result'],result)))
            need(call['cpu_before']['EIP']==0x46B760 and call['cpu_after']['EIP']==0x46B584 and call['cpu_after']['ESP']==call['cpu_before']['ESP']+12,'natural nested ret8')
            for reg in ('EBX','ESI','EDI','EBP'):need(call['cpu_before'][reg]==call['cpu_after'][reg],'nested callee saved '+reg)
            state(call['after'],m,'frame '+str(i)+' unit '+hex(call['unit'])+' after')
        state(f['stages'][1]['state'],m,'frame '+str(i)+' after units');m.post();state(f['stages'][2]['state'],m,'frame '+str(i)+' post');state(f['after'],m,'frame '+str(i)+' return')
        for s in f['stages']:
            prior.prior.full_cpu(dict(cpu_before=s['CPU'],cpu_after=s['CPU']));need(s['CPU']['EIP']=={'before_units':0x46B529,'after_units':0x46B586,'world_return':0x46B652}[s['name']],'exact frontier CPU')
        nested(f)
        should_stop=not stopped and m.memget(UNIT+0x290,'B')==6 and m.memget(UNIT+0x293,'B')==24
        need(len(f['controls'])==int(should_stop),'only one declared post-attack stop request')
        if should_stop:
            control=f['controls'][0];need(control['reason']=='stop completed first attack before re-admission','explicit control reason')
            state(control['before'],m,'control before');prior.prior.root(control['call'],0x475270,CTRL,[UNIT,5]);m.memput(UNIT+0x292,5,'B');state(control['after'],m,'control after');stopped=True
        done=settled(m.memget,m.records[1][15],m.hit_history,stopped)
        if done and terminal is None:terminal=i
        elif terminal is not None:need(done and i==terminal+1 and i==len(frames)-1,'exactly one extra complete settled frame')
    need(terminal is not None and row['terminal_index']==terminal==len(frames)-2,'independent terminal and final extra frame')
    need(row['hit']==m.hit_history and len(m.hit_history)==1,'one independently resolved original melee event')
    need([w['value'] for w in row['hp_writes']]==m.hp_stores,'all hit and natural regeneration HP writes in order')
    for w in row['hp_writes']:need(0x472550<=w['pc']<0x472770 and (w['address'],w['bytes'])==(RECORD+0x116,2),'original HP store PC/record')
    need([w for w in row['lifecycle_writes'] if w['address']==RECORD+0x116]==row['hp_writes'],'all HP stores inside whole world roots')
    need([dict(entry=e['entry'],args=e['args']) for e in row['action_events']]==m.events,'independent exact actor/target action events')
    need([(x['entry'],x['receiver'],x['args']) for x in row['cleanup']]==[(0x40AC90,ANIM,[UNIT+0x48]),(0x439C60,prior.prior.FINE+0x18,[])],'explicit original actor/path cleanup')
    for call in row['cleanup']:prior.prior.abi(call);prior.prior.full_cpu(call)
    m.cleanup();popups=[i for i in range(512) if m.popups[i*16]&128];need(len(row['popup_cleanup'])==len(popups),'exact explicit popup cleanup')
    for call,j in zip(row['popup_cleanup'],popups):prior.prior.root(call,0x494D70,CTRL,[prior.prior.POPUP+j*16]);m.popups[j*16:j*16+16]=bytes(16)
    state(row['final_state'],m,'final cleanup');prior.ownership(row,m);prior.prior.platform(row['platform'],m)
    need(row['entries'].get('0x570fe0',0)==row['entries'].get('0x5753b0',0)==m.crt_draws and row['entries'].get('0x467e00',0)==m.rng.count,'all actual original random draws')
    need(not row['OS_input_submitted'] and not row['game_function_results_stubbed'] and not row['host_unit_fields_changed_after_initialization'] and row['original_coordinate_writes']==0,'no host gameplay results or OS input')
    if replay:
        other=CombatMachine(cfg).run();prior.prior.platform(other['platform'],m);a,b=deepcopy(row),other;a.pop('platform');b.pop('platform');need(a==b,'fresh complete owned bytes/57-register/world instruction/write trace replay')
    return dict(name=cfg['name'],frames=len(frames),slot_predicates=250*len(frames),unit_updates=2*len(frames),terminal_index=terminal,
                hit_kind=m.hit_history[0]['kind'],HP=struct.unpack_from('<h',m.records[1],0x16)[0],target_alive=m.records[1][15],
                target_command=m.memget(TARGET+0x290,'B'),target_position=[m.memget(TARGET+o,'i') for o in (0x2EC,0x2F0)],
                instructions=row['instructions'],writes=row['writes'],actual_API_leaves=len(row['platform']['trace']),
                full_state_independent=True,all_memory_CPU_trace_replayed=replay)


def load_case(ref):
    p=ROOT/ref['path'];raw=p.read_bytes();need(len(raw)==ref['bytes'] and sha(raw)==ref['sha256'],'immutable world combat case source')
    data=json.loads(gzip.decompress(raw));need(data['source_contract']==source_contract(),'complete world combat case source contract')
    need(len(data['cases'])==1 and data['cases'][0]['input']['name']==ref['name'],'one exact original case')
    need(all(data[k] is False for k in ('R3_complete','R4_complete','R6_complete')),'case milestones incomplete');return data['cases'][0]


def verify_reference(task):
    ref,c=task;r=load_case(ref);need(r['input']==c,'exact independent combat input');result=verify_case(r);print('verified',r['input']['name'],len(r['world_frames']),flush=True);return result


def verify(p,jobs=3):
    raw=p.read_bytes();data=json.loads(raw);need(data['source_contract']==source_contract(),'complete world combat source contract')
    need([r['name'] for r in data['case_reports']]==[c['name'] for c in corpus()],'full declared world combat corpus')
    need(all(data[k] is False for k in ('R3_complete','R4_complete','R6_complete')),'whole milestones incomplete')
    need(1<=jobs<=3,'bounded fresh verification processes')
    with ProcessPoolExecutor(max_workers=jobs) as pool:rows=list(pool.map(verify_reference,zip(data['case_reports'],corpus())))
    return dict(schema_version=1,source_report=dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=sha(raw)),cases=rows,case_count=len(rows),
                world_frames=sum(r['frames'] for r in rows),slot_predicates=sum(r['slot_predicates'] for r in rows),unit_updates=sum(r['unit_updates'] for r in rows),
                original_instructions=sum(r['instructions'] for r in rows),original_writes=sum(r['writes'] for r in rows),
                implementation_sha256={s:sha((ROOT/s).read_bytes()) for s in ('tools/battle_world_combat.py','tools/battle_world_combat_model.py','tools/battle_world_combat_emulation.py','tools/battle_world_combat_verification.py')},
                original_native_outer_scheduler_rendering_or_victory_complete=False,R3_complete=False,R4_complete=False,R6_complete=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);p.add_argument('--jobs',type=int,default=3);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh world combat proof');out.write_text(json.dumps(verify(ROOT/a.report,a.jobs),indent=2)+'\n',encoding='utf8',newline='\n')
