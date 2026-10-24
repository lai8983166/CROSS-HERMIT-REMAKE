"""Independent whole-state hit/EFCT/HP proof plus fresh actual TLS replay."""
import argparse
import gzip
import json
import struct
from copy import deepcopy
from tools.battle_hit_damage import corpus
from tools.battle_hit_damage_model import Model
from tools.battle_hit_damage_emulation import (DamageMachine,ROOT,CTRL,UNIT,TARGET,RECORD,ANIM,FINE,REGIONS,EVENTS,EVENT_CTRL,
                                             FXDATA,FXOBJ,TLS,TANIM,DAMAGE,POPUP,parent,source_contract,need,sha)
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


def ownership(row,m):
    for key in ('initial','final'):
        need([(r['pointer'],r['bytes']) for r in row[key]]==list(REGIONS),'all exact twenty-nine ownership regions')
        need(all(len(bytes.fromhex(r['hex']))==r['bytes'] for r in row[key]),'every original owned byte retained')
    mutable=[(UNIT,UNIT+0xA40),(RECORD+0x1C,RECORD+0x1E),(RECORD+0x116,RECORD+0x118),(RECORD+0x1A6,RECORD+0x1A8),
             (FINE,FINE+0x100),(parent.parent.parent.previous.STACK,parent.parent.parent.previous.STACK+0x20000),
             (parent.POOL,parent.POOL+2048*88),(EVENT_CTRL,EVENT_CTRL+0x24),(EVENTS,EVENTS+16*12),(EVENTS+0x1000,EVENTS+0x1000+16*12),
             (DAMAGE,DAMAGE+512*8),(POPUP,POPUP+512*16),(CTRL+0x2E70C,CTRL+0x2E714),(TLS+0x14,TLS+0x18)]
    mutable += [(a,a+n) for a,n in REGIONS if a in (parent.parent.parent.previous.F_LINK,parent.parent.parent.previous.F_NODE,parent.parent.parent.previous.F_INDEX)]
    for b,a in zip(row['initial'],row['final']):
        before,after=bytes.fromhex(b['hex']),bytes.fromhex(a['hex']);base=b['pointer'];cursor=0
        for lo,hi in sorted((max(0,lo-base),min(len(before),hi-base)) for lo,hi in mutable if lo<base+len(before) and base<hi):
            need(before[cursor:lo]==after[cursor:lo],'readonly original damage memory '+hex(base+cursor));cursor=max(cursor,hi)
        need(before[cursor:]==after[cursor:],'readonly original damage tail '+hex(base+cursor))
    def memory(p):return bytes.fromhex(next(x['hex'] for x in row['final'] if x['pointer']==p))
    ctrl=memory(CTRL)
    for p,b in ((UNIT,m.unit),(TARGET,m.target),(DAMAGE,m.damage_pool),(POPUP,m.popups),(EVENT_CTRL,m.event_ctrl)):
        need(ctrl[p-CTRL:p-CTRL+len(b)]==b,'independent entire original unit/pool '+hex(p))
    need(memory(RECORD)[:512]==m.records[0]+m.records[1],'independent both full original records')
    need(memory(parent.PAGE)[parent.POOL-parent.PAGE:parent.POOL-parent.PAGE+2048*88]==m.children and not any(m.children[i*88] for i in range(2048)),'entire 2048 child slots independent and reclaimed')
    need(memory(EVENTS)==m.event_data,'whole independent event data and links')
    need(memory(FXDATA)==m.fx['raw']+bytes(0x20000-len(m.fx['raw'])),'unaltered real EFCT metadata')
    need(struct.unpack_from('<II',ctrl,0x2E70C)==(m.rng.seed,m.rng.count) and struct.unpack_from('<I',memory(TLS),0x14)[0]==m.crt_seed,'entire independent battle/CRT RNG state')
    for kind in ('fine','coarse'):
        pools=row['ownership'][kind];need(not pools[0]['links'] and not pools[1]['links'] and len(pools[2]['links'])==len(set(pools[2]['links']))==6144,'unchanged owned path pools')


def verify_case(row,replay=True):
    c=row['input'];m=Model(c);tb=row['target_bind'];state(tb['before'],m,'before target binding');root(tb['call'],0x467020,CTRL,[TARGET,c['job']]);m.bind_target();state(tb['after'],m,'after target binding')
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
    need(resume['cpu_after']['EIP']==parent.parent.parent.previous.RETURN and resume['cpu_after']['ESP']==p['cpu_before']['ESP']+12,'whole original consumer natural ret8')
    for reg in ('EBX','ESI','EDI','EBP'):need(resume['cpu_after'][reg]==p['cpu_before'][reg],'original consumer callee-saved '+reg)
    m.resolve();need(row['consume']['hit']==[m.hit],'independent full combat snapshots, raw hit kind and RNG');state(resume['after'],m,'resolved original effect')
    damage=row['consume']['damage'];state(damage['before'],m,'damage event before');root(damage['call'],0x4918D0,CTRL,[TARGET,1]);m.damage_event();state(damage['after'],m,'damage event after')
    queued=bool(m.memget(TARGET+0x510));hp=row['consume']['hp'];state(hp['before'],m,'HP before');root(hp['call'],0x493450,CTRL,[TARGET]);m.apply_hp();state(hp['after'],m,'HP after')
    if queued:
        need(len(row['hp_writes'])==1,'one actual HP record store');w=row['hp_writes'][0]
        need(0x472550<=w['pc']<0x472770 and (w['address'],w['bytes'],w['value'])==(RECORD+0x116,2,struct.unpack_from('<H',m.records[1],0x16)[0]),'original 472550 HP store and exact output')
    else:need(row['hp_writes']==[],'no fabricated HP write on miss/block')
    for t in row['consume']['effect_ticks']:
        need(m.memget(TARGET+0xA0+0x20)!=0,'no extra empty effect frames');state(t['before'],m,'FX tick before');result=m.effect_tick();state(t['after'],m,'FX tick after');root(t['call'],0x40A100,ANIM,[TARGET+0xA0]);need(t['call']['result']==result,'whole original FX update')
    need(not m.memget(TARGET+0xA0+0x20),'original effect naturally ended')
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
        other=DamageMachine(c).run();platform(other['platform'],m)
        a,b=deepcopy(row),other;a.pop('platform');b.pop('platform');need(a==b,'fresh whole-memory/57-register/source instruction and write reproduction')
    return dict(name=c['name'],raw_hit=m.hit['kind'],event_hit=m.result,damage32=struct.unpack_from('<i',bytes.fromhex(m.hit['attack']),0x28)[0],delta16=m.delta,
                hp_before=c['hp'],hp_after=struct.unpack_from('<h',m.records[1],0x16)[0],effect=m.effect_id,effect_frames=len(row['consume']['effect_ticks']),
                reaction_request=m.memget(TARGET+0x292,'B'),battle_draws=m.rng.count,CRT_draws=m.crt_draws,actual_API_leaves=len(row['platform']['trace']),HP_written=queued,
                instructions=row['instructions'],writes=row['writes'],full_units_records_pools_independent=True,all_memory_CPU_trace_replayed=replay,death_complete=False)


def verify(p):
    raw=p.read_bytes();data=json.loads(gzip.decompress(raw));need(data['source_contract']==source_contract(),'original code, EFCT, IAT and actual platform implementation')
    need([r['input'] for r in data['cases']]==corpus(),'entire declared physical combat corpus')
    need(all(data[k] is False for k in ('R3_complete','R4_complete','R6_complete')),'no global completion claim')
    rows=[]
    for r in data['cases']:rows.append(verify_case(r));print('verified',r['input']['name'],flush=True)
    return dict(schema_version=1,source_report=dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=sha(raw)),cases=rows,case_count=len(rows),
                original_instructions=sum(r['instructions'] for r in rows),original_writes=sum(r['writes'] for r in rows),
                implementation_sha256={s:sha((ROOT/s).read_bytes()) for s in ('tools/battle_hit_damage.py','tools/battle_hit_damage_model.py','tools/battle_hit_damage_platform.py','tools/battle_hit_damage_emulation.py','tools/battle_hit_damage_verification.py')},
                death_world_or_GPU_complete=False,R3_complete=False,R4_complete=False,R6_complete=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh original hit/HP proof');out.write_text(json.dumps(verify(ROOT/a.report),indent=2)+'\n',encoding='utf8',newline='\n')
