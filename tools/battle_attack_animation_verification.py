"""Independent complete animation/event state and original frontier replay."""
import argparse
import gzip
import json
import struct
from tools.battle_attack_animation import Model,corpus,attack_input,basic
from tools.battle_attack_animation_emulation import (AnimationMachine,ROOT,CTRL,UNIT,RECORD,ANIM,FINE,REGIONS,POOL,PAGE,DATA,EVENTS,EVENT_CTRL,BOUNDARY,CPU_EXTRA_NAMES,parent,source_contract,need,sha)
from tools.battle_attack_launch_verification import record as parent_record
from tools.battle_target_acquisition_verification import abi
CPU_NAMES=set(CPU_EXTRA_NAMES)|{'EAX','EBX','ECX','EDX','ESI','EDI','EBP','ESP','EIP','EFLAGS','FPCW'}


def full_cpu(call):
    need(set(call['cpu_before'])==set(call['cpu_after'])==CPU_NAMES,'exact 57 recorded x86 CPU registers')
    for cpu in (call['cpu_before'],call['cpu_after']):
        for name in ('FP'+str(i) for i in range(8)):need(isinstance(cpu[name],list) and len(cpu[name])==2,'entire x87 80-bit register')


def record(c,mp):
    b=bytearray.fromhex(parent_record(attack_input(c),mp));struct.pack_into('<H',b,0xC,c['job']);return b.hex()


def state(actual,m,label):
    expected=m.state();expected['record']=record(m.animation,m.mp)
    need(actual==expected,'independent complete animation/target/event state '+m.animation['name']+' '+label)


def ownership(row,m):
    mutable=[(UNIT,UNIT+0xA40),(RECORD+0x1C,RECORD+0x1E),(FINE,FINE+0x100),(parent.parent.previous.STACK,parent.parent.previous.STACK+0x20000),
             (POOL,POOL+2048*88),(EVENT_CTRL,EVENT_CTRL+0x24),(EVENTS,EVENTS+16*12),(EVENTS+0x1000,EVENTS+0x1000+16*12)]
    mutable += [(a,a+n) for a,n in REGIONS if a in (parent.parent.previous.F_LINK,parent.parent.previous.F_NODE,parent.parent.previous.F_INDEX)]
    for key in ('initial','final'):
        need([(r['pointer'],r['bytes']) for r in row[key]]==list(REGIONS),'exact twenty-three ownership regions')
        need(all(len(bytes.fromhex(r['hex']))==r['bytes'] for r in row[key]),'complete owned bytes')
    for b,a in zip(row['initial'],row['final']):
        before,after=bytes.fromhex(b['hex']),bytes.fromhex(a['hex']);base=b['pointer'];cursor=0
        for lo,hi in sorted((max(0,lo-base),min(len(before),hi-base)) for lo,hi in mutable if lo<base+len(before) and base<hi):
            need(before[cursor:lo]==after[cursor:lo],'readonly original animation memory '+hex(base+cursor));cursor=max(cursor,hi)
        need(before[cursor:]==after[cursor:],'readonly original animation tail '+hex(base+cursor))
    def memory(p):return bytes.fromhex(next(x['hex'] for x in row['final'] if x['pointer']==p))
    ctrl=memory(CTRL)
    need(ctrl[UNIT-CTRL:UNIT-CTRL+0x520]==m.unit and ctrl[UNIT-CTRL+0x520:UNIT-CTRL+0xA40]==m.target,'independent both complete units in final memory')
    need(ctrl[EVENT_CTRL-CTRL:EVENT_CTRL-CTRL+0x24]==m.event_ctrl and memory(EVENTS)==m.event_data,'complete original event ownership')
    need(memory(PAGE)[POOL-PAGE:POOL-PAGE+2048*88]==m.children,'entire original 2048-slot animation pool independently checked')
    need(memory(RECORD)[:256].hex()==record(row['input'],m.mp),'independent entire actor record')
    need(memory(DATA)==m.data['raw']+bytes(0x10000-len(m.data['raw'])),'unaltered exact original metadata')
    need(not any(m.children[i*88] for i in range(2048)),'all actual animation children reclaimed')
    need(not m.memget(UNIT+0x48+0x34) and not m.memget(UNIT+0x48+0x40),'all declared event queues explicitly reclaimed')
    for kind in ('fine','coarse'):
        p=row['ownership'][kind];need(not p[0]['links'] and not p[1]['links'] and len(p[2]['links'])==len(set(p[2]['links']))==6144,'unchanged path pool complete ownership')


def prefix(p,m):
    full_cpu(p)
    need(p['entry']==0x482A30 and p['receiver']==CTRL and p['args']==[UNIT,0] and p['returned'] is False and p['boundary']==BOUNDARY,'whole consumer prefix, no manufactured return')
    cpu=p['cpu_after'];need(cpu['EIP']==BOUNDARY and cpu['ECX']==CTRL and cpu['ESP']==p['stack_pointer'],'natural effect entry CPU')
    need(struct.unpack_from('<5I',bytes.fromhex(p['stack_hex']))==(0x482CF2,UNIT,UNIT+0x520,EVENTS+0x1000,0x6C2DC8+basic(m.animation['job'])*72),'natural source effect caller and exact original payload/skill arguments')
    need([(x['pointer'],x['bytes']) for x in p['memory']]==list(REGIONS),'complete retained frontier ownership')
    stack=next(x for x in p['memory'] if x['pointer']==parent.parent.previous.STACK);b=bytes.fromhex(stack['hex']);e=cpu['EBP']
    for ret in (0x482B15,0x482A64,parent.parent.previous.RETURN):
        old,actual=struct.unpack_from('<II',b,e-stack['pointer']);need(actual==ret,'natural full effect caller chain');e=old
    need(e==p['cpu_before']['EBP'],'original declared caller EBP retained')
    state(p['state'],m,'effect boundary')


def verify_case(row,replay=True):
    c=row['input'];m=Model(c);state(row['bind_before'],m,'before binding')
    need([(x['entry'],x['receiver'],x['args']) for x in row['roots']]==[(0x437C90,FINE,[UNIT+o]) for o in (0x2F4,0x3E0)],'only source packet initializer roots')
    need((row['bind']['entry'],row['bind']['receiver'],row['bind']['args'])==(0x467020,CTRL,[UNIT,c['job']]),'whole original binding root')
    m.bind();state(row['bind_after'],m,'after binding');m.put(0x292,6,'B')
    need((row['request']['entry'],row['request']['receiver'],row['request']['args'])==(0x475270,CTRL,[UNIT,6]),'explicit original attack request root')
    for i,s in enumerate(row['steps']):
        need(s['index']==i,'continuous command index');state(s['before'],m,'command before');m.command();state(s['after'],m,'command after')
        abi(s['call']);full_cpu(s['call']);need((s['call']['entry'],s['call']['receiver'],s['call']['args'],s['call']['result'])==(0x475700,CTRL,[UNIT],0),'complete original attack dispatcher')
    need(m.get(0x293,'B')==22 and m.launches==1 and len(row['steps'])==(3 if c['windup']==0 else 6),'single source release')
    first_event=None
    for i,t in enumerate(row['ticks']):
        need(t['index']==i,'continuous source animation index');state(t['before'],m,'tick before');result=m.tick();state(t['after'],m,'tick after');call=t['call'];abi(call)
        full_cpu(call);need((call['entry'],call['receiver'],call['args'],call['result'])==(0x40A100,ANIM,[UNIT+0x48],result),'complete original frame root result')
        if first_event is None and m.memget(UNIT+0x48+0x34):first_event=i
    need(first_event==(15 if c['job']<3 else 11),'actual attack event before animation finish')
    early=c['consume'] in ('early_boundary','cancel')
    need(len(row['ticks'])==((16 if c['job']<3 else 12) if early else (48 if c['job']<3 else 36)),'independent full/early animation duration')
    need(bool(m.memget(UNIT+0x48+4))==early,'truthful animation completion boundary')
    need(m.get(4,'B')==0,'host never propagates standalone completion to world field')
    if c['consume'] in ('boundary','early_boundary'):
        need(not row['invalidation'],'no target changes on valid effect frontier');prefix(row['consume'],m)
    elif c['consume'] in ('target_inactive','actor_inactive'):
        actor=UNIT+0x520 if c['consume']=='target_inactive' else UNIT
        need([(x['entry'],x['receiver'],x['args']) for x in row['invalidation']]==[(0x475270,CTRL,[actor,12]),(0x4751F0,CTRL,[actor])],'explicit original command12 transition, not a death assertion')
        m.invalidate();state(row['consume']['before'],m,'before inactive consumption');m.consume_events();state(row['consume']['after'],m,'after inactive consumption')
        call=row['consume']['call'];abi(call);full_cpu(call);need(row['consume']['returned'] and (call['entry'],call['receiver'],call['args'])==(0x482A30,CTRL,[UNIT,0]),'whole original inactive-target consumer')
    else:need(row['consume'] is None and not row['invalidation'],'no invented event consumer')
    need([dict(entry=e['entry'],args=e['args']) for e in row['action_events']]==m.events,'independent idle/prepare/release action arguments')
    for call in row['roots']+[row['bind'],row['request']]+row['invalidation']+row['cleanup']:abi(call);full_cpu(call)
    cleanup=[(0x40AC90,ANIM,[UNIT+0x48])]
    for off in (0x30,0x3C):
        while m.memget(UNIT+0x48+off+4):
            node=m.memget(UNIT+0x48+off+4);cleanup.append((0x40BE20,EVENT_CTRL,[node]));m.return_event(node)
    m.free_work(UNIT+0x48);cleanup.append((0x439C60,FINE+0x18,[]))
    need([(x['entry'],x['receiver'],x['args']) for x in row['cleanup']]==cleanup,'only explicit original child/event/fine cleanup')
    state(row['final_state'],m,'final cleanup');ownership(row,m)
    need(not row['original_coordinate_writes'] and not row['OS_input_submitted'] and not row['game_function_results_stubbed'] and not row['host_unit_fields_changed_after_initialization'],'isolated original animation scope')
    if replay:need(AnimationMachine(c).run()==row,'fresh complete memory CPU and original instruction/write trace replay')
    return dict(name=c['name'],job=c['job'],command_roots=len(row['steps']),animation_roots=len(row['ticks']),first_event_tick=first_event+1,
                animation_ended=not early,effect_frontier=c['consume'] in ('boundary','early_boundary'),inactive_consumer_returned=c['consume'] in ('target_inactive','actor_inactive'),
                instructions=row['instructions'],writes=row['writes'],full_state_independent=True,all_memory_CPU_trace_replayed=replay,hit_damage_death_complete=False)


def verify(p):
    raw=p.read_bytes();data=json.loads(gzip.decompress(raw));need(data['source_contract']==source_contract(),'fixed original code and animation assets')
    need([r['input'] for r in data['cases']]==corpus(),'complete exact animation corpus')
    need(all(data[k] is False for k in ('R3_complete','R4_complete','R6_complete')),'no global completion inflation')
    rows=[]
    for r in data['cases']:rows.append(verify_case(r));print('verified',r['input']['name'],flush=True)
    return dict(schema_version=1,source_report=dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=sha(raw)),cases=rows,case_count=len(rows),
                original_instructions=sum(r['instructions'] for r in rows),original_writes=sum(r['writes'] for r in rows),
                implementation_sha256={s:sha((ROOT/s).read_bytes()) for s in ('tools/battle_attack_animation.py','tools/battle_attack_animation_emulation.py','tools/battle_attack_animation_verification.py')},
                full_world_or_hit_damage_death_verified=False,R3_complete=False,R4_complete=False,R6_complete=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh animation proof');out.write_text(json.dumps(verify(ROOT/a.report),indent=2)+'\n',encoding='utf8',newline='\n')
