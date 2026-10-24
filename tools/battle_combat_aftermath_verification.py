"""Independent whole-state combat aftermath proof plus fresh actual TLS replay."""
import argparse
import gzip
import json
import struct
from copy import deepcopy
from tools.battle_combat_aftermath import corpus
from tools.battle_combat_aftermath_model import Model
from tools.battle_combat_aftermath_emulation import (AftermathMachine,ROOT,CTRL,UNIT,TARGET,RECORD,ANIM,REGIONS,
                                                        TASK,EVENT_ENV,VISIBLE,SEEN,region,parent,source_contract,need,sha)
from tools.battle_hit_damage_emulation import (FINE,EVENTS,EVENT_CTRL,FXDATA,FXOBJ,TLS,TANIM,DAMAGE,POPUP)
from tools import battle_attack_animation_emulation as animation_parent
from tools.battle_attack_animation_verification import full_cpu
from tools.battle_target_acquisition_verification import abi


def state(actual,m,label):need(actual==m.state(),'independent complete hit/FX/HP state '+m.combat['name']+' '+label)


def root(call,entry,receiver,args):
    abi(call);full_cpu(call);need((call['entry'],call['receiver'],call['args'])==(entry,receiver,args),'whole original declared root '+hex(entry))


def platform(p,m):
    create,cleanup=p['creation'],p['cleanup'];need(create['guest_index']==51 and create['guest_token']==TLS and create['actual_set_and_readback'] and create['pointer_is_guest_token_not_native_dereference'],'actual current TLS role creation')
    need(type(create['native_index']) is int and 0<=create['native_index']<0xFFFFFFFF and create['thread']>0,'actual native slot/thread')
    need(cleanup['thread']==create['thread'] and cleanup['native_index']==create['native_index'] and cleanup['actual_clear'] and cleanup['actual_free'] and cleanup['freed_readback']==0 and not cleanup['forced_cleanup'],'actual same-thread token clear/free/no stale token')
    expected=[]
    for _ in range(m.crt_draws):
        for name,args,value,before,after in [('GetLastError',[],0x1234,0x1234,0x1234),('TlsGetValue',[51],TLS,0x1234,0),('SetLastError',[0x1234],0,0,0x1234)]:
            expected.append(dict(name=name,guest_args=args,value=value,error_before=before,error_after=after,
                                 actual_native_index=create['native_index'] if name=='TlsGetValue' else None,actual_API_executed=True,void_EAX_normalized=name=='SetLastError'))
    need(p['trace']==expected,'every original CRT request has exact real TLS/LastError receipt')


def verify_updates(row,m):
    updates=row['consume']['aftermath'];cursor=0;actor_done=False;target_done=False
    target_needs_update=bool(m.memget(TARGET+0x292,'B')) or struct.unpack_from('<h',m.records[1],0x16)[0]==0
    all_writes=[]
    for i in range(256):
        for u,done in ((UNIT,actor_done),(TARGET,target_done)):
            if done:continue
            if u==TARGET and not target_needs_update and i>0:target_done=True;continue
            need(cursor<len(updates),'complete independent update schedule');step=updates[cursor];cursor+=1
            need((step['round'],step['unit'])==(i,u),'actual finite full-unit update order')
            state(step['before'],m,'unit update before');root(step['call'],0x46B760,CTRL,[u,0 if u==UNIT else 1])
            result=m.unit_update(u);need(step['call']['result']==result,'whole unit update natural result');state(step['after'],m,'unit update after')
            entries=step['entries'];need(entries and entries[0]==0x46B760,'actual whole unit root trace')
            need(0x48D720 in entries and 0x48E2A0 in entries,'original AI/effect gate bodies executed')
            if result!=1:
                need(entries.index(0x490350)<entries.index(0x472370)<entries.index(0x472770),'original status, regeneration and death gate order')
            all_writes.extend(step['writes'])
            if u==UNIT:actor_done=m.memget(UNIT+0x292,'B')!=0 or m.memget(UNIT+0x290,'B')!=6 or m.memget(UNIT+0x293,'B')==24
            else:target_done=(m.memget(TARGET+0x290,'B')==11 or m.memget(TARGET+0x292,'B') not in (0,8,9,13)) or (m.memget(TARGET+0x290,'B') in (8,9) and m.memget(TARGET+0x2A6,'B')==0)
        if actor_done and target_done:break
    need(actor_done and target_done and cursor==len(updates),'no missing or surplus original unit updates')
    need(all_writes==row['lifecycle_writes'],'all actual lifecycle stores retained in order')
    queued=bool(struct.unpack_from('<I',bytes.fromhex(row['consume']['hp']['before']['target']),0x510)[0])
    values=([struct.unpack_from('<H',bytes.fromhex(row['consume']['hp']['after']['target_record']),0x16)[0]] if queued else [])+m.target_regeneration_stores
    need([w['value'] for w in row['hp_writes']]==values,'every hit and natural regeneration HP store independently accounted')
    for w in row['hp_writes']:need(0x472550<=w['pc']<0x472770 and (w['address'],w['bytes'])==(RECORD+0x116,2),'only original HP store instruction')
    need([w for w in all_writes if w['address']==RECORD+0x116]==row['hp_writes'][int(queued):],'actual original regeneration stores inside whole unit roots')


def ownership(row,m):
    for key in ('initial','final'):
        need([(r['pointer'],r['bytes']) for r in row[key]]==list(REGIONS),'all thirty-five owned regions retained')
        need(all(len(bytes.fromhex(r['hex']))==r['bytes'] for r in row[key]),'all owned bytes retained')
    mutable=[(UNIT,UNIT+0xA40),(RECORD,RECORD+512),(FINE,FINE+0x100),(region.STACK,region.STACK+0x20000),
             (animation_parent.POOL,animation_parent.POOL+2048*88),(EVENT_CTRL,EVENT_CTRL+0x24),
             (EVENTS,EVENTS+16*12),(EVENTS+0x1000,EVENTS+0x1000+16*12),(DAMAGE,DAMAGE+512*8),(POPUP,POPUP+512*16),
             (CTRL+0x2E70C,CTRL+0x2EF44),(TLS+0x14,TLS+0x18),(region.OCC,region.OCC+0x3000),
             (0x7A49E0,0x7A49E4),(0x618CF0,0x618CF8),(VISIBLE,VISIBLE+0x2000),(SEEN,SEEN+0x2000)]
    mutable += [(a,a+n) for a,n in REGIONS if a in (region.F_LINK,region.F_NODE,region.F_INDEX)]
    for before,after in zip(row['initial'],row['final']):
        b,a=bytes.fromhex(before['hex']),bytes.fromhex(after['hex']);base=before['pointer'];cursor=0
        for lo,hi in sorted((max(0,lo-base),min(len(b),hi-base)) for lo,hi in mutable if lo<base+len(b) and base<hi):
            need(b[cursor:lo]==a[cursor:lo],'readonly aftermath memory '+hex(base+cursor));cursor=max(cursor,hi)
        need(b[cursor:]==a[cursor:],'readonly aftermath tail '+hex(base+cursor))
    def memory(p):return bytes.fromhex(next(x['hex'] for x in row['final'] if x['pointer']==p))
    ctrl=memory(CTRL)
    for p,b in ((UNIT,m.unit),(TARGET,m.target),(DAMAGE,m.damage_pool),(POPUP,m.popups),(EVENT_CTRL,m.event_ctrl),(CTRL+0x2E714,m.stats)):
        need(ctrl[p-CTRL:p-CTRL+len(b)]==b,'entire independent original owned unit/pool/statistics '+hex(p))
    need(memory(RECORD)[:512]==m.records[0]+m.records[1],'whole independent original two records')
    need(memory(animation_parent.PAGE)[animation_parent.POOL-animation_parent.PAGE:animation_parent.POOL-animation_parent.PAGE+2048*88]==m.children,'entire independent 2048-slot child pool')
    need(memory(EVENTS)==m.event_data,'entire original event arena');need(memory(region.OCC)==m.occupancy,'whole independent occupancy')
    need(memory(VISIBLE)==m.visible and memory(SEEN)==m.seen,'entire original max visibility fields')
    need(memory(0x618000)[0xCF0:0xCF8]==m.motion_scratch,'original CRT/fixed-point motion scratch')
    for kind in ('fine','coarse'):
        pools=row['ownership'][kind];need(not pools[0]['links'] and not pools[1]['links'] and len(pools[2]['links'])==len(set(pools[2]['links']))==6144,'all owned path nodes reclaimed')


def verify_case(row,replay=True):
    cfg=row['input'];c=cfg['combat'];m=Model(cfg);tb=row['target_bind'];state(tb['before'],m,'before target binding');root(tb['call'],0x467020,CTRL,[TARGET,c['job']]);m.bind_target();state(tb['after'],m,'after target binding')
    need(len(row['roots'])==2,'two empty packet initializer roots')
    for call,off in zip(row['roots'],(0x2F4,0x3E0)):root(call,0x437C90,FINE,[UNIT+off]);m.clear_packet(off)
    state(row['bind_before'],m,'before actor binding');root(row['bind'],0x467020,CTRL,[UNIT,c['job']]);m.bind();state(row['bind_after'],m,'after actor binding')
    root(row['request'],0x475270,CTRL,[UNIT,6]);m.put(0x292,6,'B')
    need(len(row['steps'])==6,'complete source preparation budget')
    for i,s in enumerate(row['steps']):
        need(s['index']==i,'continuous source command index');state(s['before'],m,'command before');m.command();state(s['after'],m,'command after');root(s['call'],0x475700,CTRL,[UNIT]);need(s['call']['result']==0,'source command result')
    expected_ticks=16 if c['job']<3 else 12;need(len(row['ticks'])==expected_ticks,'stop at actual first attack event')
    for i,t in enumerate(row['ticks']):
        need(t['index']==i,'continuous attack animation index');state(t['before'],m,'attack tick before');result=m.tick();state(t['after'],m,'attack tick after');root(t['call'],0x40A100,ANIM,[UNIT+0x48]);need(t['call']['result']==result,'original animation result')
    p=row['consume']['frontier'];need(p['boundary']==0x48AAE0 and p['returned'] is False and p['entry']==0x482A30 and p['receiver']==CTRL and p['args']==[UNIT,0],'natural original effect frontier')
    full_cpu(p);state(p['state'],m,'natural effect frontier');need(p['cpu_after']['EIP']==0x48AAE0,'unexecuted effect entry')
    need(struct.unpack_from('<5I',bytes.fromhex(p['stack_hex']))==(0x482CF2,UNIT,TARGET,EVENTS+0x1000,0x6C2DC8+(100+c['job'])*72),'actual original caller and effect packet')
    need([(x['pointer'],x['bytes']) for x in p['memory']]==list(REGIONS),'whole pre-effect memory frontier')
    resume=row['consume']['continuation'];full_cpu(resume);state(resume['before'],m,'resume before')
    need(resume['cpu_before']==p['cpu_after'] and resume['returned'] and resume['instructions']>0,'same exact original CPU/stack, no independent effect root')
    need(resume['cpu_after']['EIP']==region.RETURN and resume['cpu_after']['ESP']==p['cpu_before']['ESP']+12,'whole original consumer natural ret8')
    for reg in ('EBX','ESI','EDI','EBP'):need(resume['cpu_after'][reg]==p['cpu_before'][reg],'original consumer callee-saved '+reg)
    m.resolve();need(row['consume']['hit']==[m.hit],'independent full combat snapshots, raw hit kind and RNG');state(resume['after'],m,'resolved original effect')
    damage=row['consume']['damage'];state(damage['before'],m,'damage event before');root(damage['call'],0x4918D0,CTRL,[TARGET,1]);m.damage_event();state(damage['after'],m,'damage event after')
    queued=bool(m.memget(TARGET+0x510));hp=row['consume']['hp'];state(hp['before'],m,'HP before');root(hp['call'],0x493450,CTRL,[TARGET]);m.apply_hp();state(hp['after'],m,'HP after')
    if queued:
        need(len(row['hp_writes'])>=1,'one actual HP record store');w=row['hp_writes'][0]
        need(0x472550<=w['pc']<0x472770 and (w['address'],w['bytes'],w['value'])==(RECORD+0x116,2,struct.unpack_from('<H',m.records[1],0x16)[0]),'original 472550 HP store and exact output')
    for t in row['consume']['effect_ticks']:
        need(m.memget(TARGET+0xA0+0x20)!=0,'no extra empty effect frames');state(t['before'],m,'FX tick before');result=m.effect_tick();state(t['after'],m,'FX tick after');root(t['call'],0x40A100,ANIM,[TARGET+0xA0]);need(t['call']['result']==result,'whole original FX update')
    need(not m.memget(TARGET+0xA0+0x20),'original effect naturally ended')
    verify_updates(row,m)
    need(not row['invalidation'],'no host/test invalidation after source initialization')
    need([dict(entry=e['entry'],args=e['args']) for e in row['action_events']]==m.events,'exact independent original actor/target action arguments')
    need([(x['entry'],x['receiver'],x['args']) for x in row['cleanup']]==[(0x40AC90,ANIM,[UNIT+0x48]),(0x439C60,FINE+0x18,[])],'explicit source actor child and path cleanup')
    for call in row['cleanup']:abi(call);full_cpu(call)
    m.cleanup();popups=[i for i in range(512) if m.popups[i*16]&128]
    need(len(row['popup_cleanup'])==len(popups),'explicit popup cleanup budget')
    for call,i in zip(row['popup_cleanup'],popups):root(call,0x494D70,CTRL,[POPUP+i*16]);m.popups[i*16:i*16+16]=bytes(16)
    state(row['final_state'],m,'final after explicit cleanup');ownership(row,m);platform(row['platform'],m)
    need(row['entries'].get('0x570fe0',0)==m.crt_draws and row['entries'].get('0x5753b0',0)==m.crt_draws and row['entries'].get('0x467e00',0)==m.rng.count,'all original game/CRT random bodies executed, no draws supplied')
    need(not row['OS_input_submitted'] and not row['game_function_results_stubbed'] and not row['host_unit_fields_changed_after_initialization'] and row['original_coordinate_writes']==0,'original code only derived combat writes')
    if replay:
        other=AftermathMachine(cfg).run();platform(other['platform'],m)
        a,b=deepcopy(row),other;a.pop('platform');b.pop('platform');need(a==b,'fresh whole-memory/57-register/source instruction and write reproduction')
    return dict(name=cfg['name'],updates=len(row['consume']['aftermath']),actor_phase=m.memget(UNIT+0x293,'B'),
                target_command=m.memget(TARGET+0x290,'B'),target_pending=m.memget(TARGET+0x292,'B'),target_alive=m.records[1][0xF],
                target_HP=struct.unpack_from('<h',m.records[1],0x16)[0],death_removed=m.records[1][0xF]==3,
                kills=struct.unpack_from('<h',m.records[0],0xAA)[0],points=struct.unpack_from('<h',m.records[0],0xAC)[0],
                deaths=m.records[1][0xAE],score=struct.unpack_from('<h',m.stats,0x800)[0],
                target_position=[m.memget(TARGET+off,'i') for off in (0x2EC,0x2F0)],
                instructions=row['instructions'],writes=row['writes'],actual_API_leaves=len(row['platform']['trace']),
                full_state_independent=True,all_memory_CPU_trace_replayed=replay)


def verify(p):
    raw=p.read_bytes();data=json.loads(gzip.decompress(raw));need(data['source_contract']==source_contract(),'original whole-unit source contract')
    need([r['input'] for r in data['cases']]==corpus(),'entire declared aftermath corpus')
    need(all(data[k] is False for k in ('R3_complete','R4_complete','R6_complete')),'global milestones remain incomplete')
    rows=[]
    for r in data['cases']:rows.append(verify_case(r));print('verified',r['input']['name'],flush=True)
    return dict(schema_version=1,source_report=dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=sha(raw)),cases=rows,case_count=len(rows),
                unit_updates=sum(r['updates'] for r in rows),death_removed_cases=sum(r['death_removed'] for r in rows),
                original_instructions=sum(r['instructions'] for r in rows),original_writes=sum(r['writes'] for r in rows),
                implementation_sha256={s:sha((ROOT/s).read_bytes()) for s in ('tools/battle_combat_aftermath.py','tools/battle_combat_aftermath_model.py',
                                         'tools/battle_combat_aftermath_emulation.py','tools/battle_combat_aftermath_verification.py')},
                full_world_outer_frame_or_GPU_complete=False,R3_complete=False,R4_complete=False,R6_complete=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh combat aftermath proof');out.write_text(json.dumps(verify(ROOT/a.report),indent=2)+'\n',encoding='utf8',newline='\n')
