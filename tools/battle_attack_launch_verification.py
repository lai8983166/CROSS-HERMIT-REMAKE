"""Independent whole-unit/record attack proof and fresh original trace replay."""
import argparse
import gzip
import json
import struct
from tools.battle_attack_launch import Model,corpus,charge_corpus,skill_cost
from tools.battle_attack_launch_emulation import AttackMachine,ROOT,CTRL,UNIT,RECORD,FINE,REGIONS,parent,source_contract,need,sha
from tools.battle_target_acquisition_verification import abi


def record(c,mp):
    r=bytearray(256)
    for off,val,fmt in ((2,c['actor_id'],'H'),(0xC,1,'H'),(0xF,1,'B'),(0x14,100,'h'),(0x16,100,'h'),
                        (0x1A,c['max_mp'],'h'),(0x1C,mp,'h'),(0x2C,5,'b'),(0x2E,999,'H'),(0x32,c['windup'],'h'),
                        (0x34,c['recovery'],'h'),(0x37,c['range'],'B')):struct.pack_into('<'+fmt,r,off,val)
    return r.hex()


def ownership(row,m):
    mutable=[(UNIT,UNIT+0x520),(RECORD+0x1C,RECORD+0x1E),(FINE,FINE+0x100),(parent.previous.STACK,parent.previous.STACK+0x20000)]
    mutable += [(a,a+n) for a,n in REGIONS if a in (parent.previous.F_LINK,parent.previous.F_NODE,parent.previous.F_INDEX)]
    for key in ('initial','final'):
        need([(r['pointer'],r['bytes']) for r in row[key]]==list(REGIONS),'exact nineteen owned regions')
        need(all(len(bytes.fromhex(r['hex']))==r['bytes'] for r in row[key]),'complete ownership bytes')
    for b,a in zip(row['initial'],row['final']):
        before,after=bytes.fromhex(b['hex']),bytes.fromhex(a['hex']);base=b['pointer'];cursor=0
        for lo,hi in sorted((max(0,lo-base),min(len(before),hi-base)) for lo,hi in mutable if lo<base+len(before) and base<hi):
            need(before[cursor:lo]==after[cursor:lo],'readonly attack memory '+hex(base+cursor));cursor=max(cursor,hi)
        need(before[cursor:]==after[cursor:],'readonly attack tail '+hex(base+cursor))
    ctrl=next(r for r in row['final'] if r['pointer']==CTRL)
    need(bytes.fromhex(ctrl['hex'])[UNIT-CTRL:UNIT-CTRL+0x520]==m.unit,'full independent final unit')
    rec=next(r for r in row['final'] if r['pointer']==RECORD)
    need(rec['hex'][:512]==record(row['input'],m.mp),'full independent final actor record')
    for kind,obj,off in [('fine',FINE,0x18),('coarse',parent.previous.COARSE,0x10)]:
        pools=row['ownership'][kind]
        need([r['head'] for r in pools]==[obj+off+d for d in (0x44,0x50,0x78)],'source pool heads')
        need(not pools[0]['links'] and not pools[1]['links'] and len(set(pools[2]['links']))==len(pools[2]['links'])==6144,'all source nodes reclaimed')


def verify_case(row,replay=True):
    c=row['input'];m=Model(c);moved=0;releases=[];phases=[];pending=0
    need([(r['entry'],r['receiver'],r['args']) for r in row['roots']]==[(0x437C90,FINE,[UNIT+off]) for off in (0x2F4,0x3E0)],'only source empty packet initializer roots')
    need(1<=len(row['steps'])<=c['calls'],'declared root budget')
    for i,s in enumerate(row['steps']):
        need(s['index']==i and s['before_hex']==m.unit.hex(),'continuous independent before unit '+c['name']+' '+str(i))
        need(s['record_before']==record(c,m.mp),'independent before record')
        before=bytes(m.unit);launches=m.launches;m.command()
        need(s['after_hex']==m.unit.hex(),'independent complete attack unit '+c['name']+' '+str(i))
        need(s['record_after']==record(c,m.mp),'independent complete attack MP record')
        call=s['call'];abi(call)
        need((call['entry'],call['receiver'],call['args'],call['result'])==(0x475700,CTRL,[UNIT],0),'complete original dispatcher root')
        moved+=before[0x2EC:0x2F4]!=m.unit[0x2EC:0x2F4];phases.append(m.get(0x293,'B'))
        if m.launches>launches:releases.append(i)
        pending=m.get(0x292,'B')
        if pending not in (0,6):need(i==len(row['steps'])-1,'stop on alternate request')
    expected_stop='pending_command' if pending not in (0,6) else ('release_then_three_waits' if releases else 'call_budget')
    need(row['stop']==expected_stop,'truthful bounded stop')
    if releases:
        need(len(releases)==1 and len(phases)==releases[0]+4,'one release and three complete waiting roots')
        wait=row['steps'][releases[0]]['after_hex']
        need(all(s['before_hex']==wait and s['after_hex']==wait for s in row['steps'][releases[0]+1:]),'source phase22 waits without host animation completion')
        need(m.get(4,'B')==0 and phases[-1]==22,'empty clip never manufactured completion')
    need(row['original_coordinate_writes']==moved*2,'source coordinate writes match model')
    need(row['popped']==dict(coarse=[],fine=m.search_popped),'independent actual chase search')
    need(row['entries'].get('0x46c990',0)==m.launches and row['entries'].get('0x472550',0)==m.launches,'only source release charges MP')
    need([dict(entry=e['entry'],args=e['args']) for e in row['action_events']]==m.events,'actual facing/action/MP argument sequence independently predicted')
    need([(r['entry'],r['receiver'],r['args']) for r in row['cleanup']]==[(0x439C60,FINE+0x18,[])],'explicit source pool cleanup')
    for call in row['roots']+row['cleanup']:abi(call)
    need(not row['OS_input_submitted'] and not row['game_function_results_stubbed'] and not row['host_unit_fields_changed_after_initialization'],'unmodified original execution scope')
    ownership(row,m)
    if replay:need(AttackMachine(c).run()==row,'fresh complete memory/CPU/source instruction and write replay')
    return dict(name=c['name'],roots=len(phases),phases=phases,release_roots=releases,mp=m.mp,pending=pending,
                moves=moved,instructions=row['instructions'],writes=row['writes'],all_unit_record_bytes_independent=True,
                whole_memory_CPU_trace_replay=replay,hit_or_damage_verified=False)


def verify(report):
    raw=report.read_bytes();data=json.loads(gzip.decompress(raw))
    need(data['source_contract']==source_contract(),'original code/table/map identity')
    need([r['input'] for r in data['cases']]==corpus(),'complete exact attack corpus')
    need(all(data[k] is False for k in ('R3_complete','R4_complete','R6_complete')),'no global completion claims')
    need([r['input'] for r in data['charge_cases']]==charge_corpus(),'complete paid MP corpus')
    rows=[]
    for r in data['cases']:
        rows.append(verify_case(r));print('verified',r['input']['name'],flush=True)
    charges=[verify_charge(r) for r in data['charge_cases']]
    return dict(schema_version=1,source_report=dict(path=report.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=sha(raw)),
                cases=rows,case_count=len(rows),original_instructions=sum(r['instructions'] for r in rows),original_writes=sum(r['writes'] for r in rows),
                charge_cases=charges,charge_case_count=len(charges),charge_instructions=sum(r['instructions'] for r in charges),charge_writes=sum(r['writes'] for r in charges),
                implementation_sha256={p:sha((ROOT/p).read_bytes()) for p in ('tools/battle_attack_launch.py','tools/battle_attack_launch_emulation.py','tools/battle_attack_launch_verification.py')},
                native_world_or_hit_damage_complete=False,R3_complete=False,R4_complete=False,R6_complete=False)


def verify_charge(row,replay=True):
    c=row['input'];m=Model(c);affordable=c['mp']>=skill_cost(c['skill'])
    need(row['before_hex']==m.unit.hex() and row['after_hex']==m.unit.hex(),'MP helper preserves whole independent unit')
    need(row['record_before']==record(c,m.mp),'whole independent MP input record')
    if affordable:m.mp=max(0,min(c['max_mp'],min(32767,m.mp-skill_cost(c['skill']))))
    need(row['record_after']==record(c,m.mp),'whole independent paid MP output record')
    gate=row['gate'];abi(gate)
    need((gate['entry'],gate['receiver'],gate['args'],gate['result'])==(0x46C930,CTRL,[UNIT,c['skill']],int(affordable)),'actual MP admission root')
    if affordable:
        call=row['charge'];need(call is not None,'actual source MP consumption required');abi(call)
        need((call['entry'],call['receiver'],call['args'])==(0x46C990,CTRL,[UNIT,c['skill']]),'explicit paid MP helper root')
    else:need(row['charge'] is None,'no unaffordable helper consumption')
    need([(r['entry'],r['receiver'],r['args']) for r in row['roots']]==[(0x437C90,FINE,[UNIT+off]) for off in (0x2F4,0x3E0)],'declared MP fixture initializer roots')
    need([(r['entry'],r['receiver'],r['args']) for r in row['cleanup']]==[(0x439C60,FINE+0x18,[])],'MP explicit cleanup')
    for call in row['roots']+row['cleanup']:abi(call)
    need(row['entries'].get('0x472550',0)==int(affordable) and row['original_coordinate_writes']==0,'only actual MP helper modifies record')
    need([dict(entry=e['entry'],args=e['args']) for e in row['action_events']]==([dict(entry=0x46C990,args=[UNIT,c['skill']])] if affordable else []),'actual paid charge arguments')
    need(not row['OS_input_submitted'] and not row['game_function_results_stubbed'] and not row['host_unit_fields_changed_after_initialization'],'isolated original MP helpers')
    ownership(row,m)
    if replay:need(AttackMachine(c).charge()==row,'fresh complete MP helper memory CPU trace')
    return dict(name=c['name'],affordable=affordable,mp_after=m.mp,instructions=row['instructions'],writes=row['writes'],whole_memory_CPU_trace_replay=replay,
                paid_skill_attack_dispatcher_executed=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh attack proof');out.write_text(json.dumps(verify(ROOT/a.report),indent=2)+'\n',encoding='utf8',newline='\n')
