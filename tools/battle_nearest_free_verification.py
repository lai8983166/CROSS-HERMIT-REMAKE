"""Independent nearest-free semantics, complete unit and fresh original replay."""
import argparse
import gzip
import json
import struct
from copy import deepcopy
from tools.battle_nearest_free import expected_table,select,selection_corpus,movement_corpus,RerouteModel
from tools.battle_nearest_free_emulation import (ROOT,CTRL,UNIT,MAP,FINDER,TABLE,DIST,REGIONS,NearestMachine,
    selection,flood,source_contract,need,sha,previous)


def ownership(row,mutable):
    for k in ('initial','final'):
        need([(r['pointer'],r['bytes']) for r in row[k]]==list(REGIONS),'complete exact ownership regions')
        need(all(len(bytes.fromhex(r['hex']))==r['bytes'] for r in row[k]),'complete region bytes')
    for before,after in zip(row['initial'],row['final']):
        a,b=bytes.fromhex(before['hex']),bytes.fromhex(after['hex']);start=before['pointer']
        spans=sorted((max(0,lo-start),min(len(a),hi-start)) for lo,hi in mutable if lo<start+len(a) and start<hi)
        cursor=0
        for lo,hi in spans:
            need(a[cursor:lo]==b[cursor:lo],'unrelated original inputs unchanged '+hex(start+cursor));cursor=max(cursor,hi)
        need(a[cursor:]==b[cursor:],'readonly trailing input '+hex(start+cursor))


def abi(call):
    need(call['ESP_after']==call['ESP_before']+4+4*len(call['args']),'original callee pop ESP')
    need(call['cpu_after']['EIP']==0x10B00000,'original root returned')
    for reg in ('EBX','ESI','EDI','EBP'):need(call['cpu_before'][reg]==call['cpu_after'][reg],'original preserved '+reg)


def verify_selection(row,replay=True,table=None):
    c=row['input'];counter=c['counter'];reservations=deepcopy(c['reservations']);work=bytearray(0xA4)
    struct.pack_into('<I',work,0,len(reservations))
    for i,p in enumerate(reservations):struct.pack_into('<hh',work,4+i*4,*p)
    successes=0;results=[]
    need(len(row['calls'])==c['calls']+int(c['reset']),'all selection roots')
    for index,record in enumerate(row['calls']):
        call=record['call'];abi(call)
        if c['reset'] and index==0:
            need(record['kind']=='reset' and (call['entry'],call['receiver'],call['args'])==(0x43D4E0,MAP,[]),'explicit source reset')
            reservations=[];work=bytearray(0xA4)
        else:
            need(record['kind']=='select' and (call['entry'],call['receiver'],call['args'])==(0x43D660,MAP,[*c['seed'],c['view'],c['mode'],0x109000F0,0x109000F2]),'original select root')
            counter,point=select(c,counter,reservations)
            need(call['result']==int(point is not None),'source select EAX')
            need(record['output']==(point if point is not None else [0xA55A,0x5AA5]),'independent output or unchanged failure sentinels')
            if point is not None:
                struct.pack_into('<I',work,0,len(reservations));struct.pack_into('<hh',work,4+(len(reservations)-1)*4,*point);successes+=1
            results.append(point)
        need(record['state']==dict(counter=counter,points=reservations,work_hex=work.hex()),'entire reservation work and rotation')
    need(row['OS_input_submitted'] is False and row['game_function_results_stubbed'] is False,'scope without OS input or game stubs')
    ownership(row,[(MAP+0x263C4,MAP+0x263C6),(MAP+0x263C8,MAP+0x2646C),(0x109000F0,0x109000F4),(0x10A00000,0x10A10000)])
    if replay:need(selection(c,table)==row,'fresh source selection full memory CPU instruction/write trace')
    return dict(name=c['name'],calls=c['calls'],successes=successes,outputs=results,final_counter=counter,
                instructions=row['instructions'],writes=row['writes'],full_original_replay=replay)


def verify_route(row,replay=True,table=None):
    c=row['input'];model=RerouteModel(c,previous.source_contract());moved=0;stop='frame_budget';phases=set();cooldowns=[]
    need(not row['host_unit_fields_changed_after_initialization'] and not row['game_or_math_results_stubbed'] and not row['OS_input_submitted'],'original isolated route scope')
    need([(r['entry'],r['receiver'],r['args']) for r in row['roots']]==[(0x437C90,FINDER,[UNIT+off]) for off in (0x2F4,0x3E0)],'no host-supplied route roots')
    for i,step in enumerate(row['steps']):
        need(step['index']==i and step['before_hex']==model.unit.hex(),'continuous complete before unit')
        before=bytes(model.unit);model.step();phase=model.get(0x293,'B');phases.add(phase);cooldowns.append(model.get(0x4E0,'h'))
        need(step['after_hex']==model.unit.hex() and step['phase']==phase,'independent complete rerouting unit '+c['movement']['name']+' '+str(i))
        need(len(step['calls'])==1 and (step['calls'][0]['entry'],step['calls'][0]['receiver'],step['calls'][0]['args'])==(0x476680,CTRL,[UNIT,0]),'one complete original AI call')
        moved+=before[0x2EC:0x2F4]!=model.unit[0x2EC:0x2F4]
        selected=None
        if phase==8:selected='next_tile_blocked'
        elif phase==3 and model.get(0x314,'H')==0:selected='secondary_only_arrived'
        elif before==model.unit and phase in (0,3,4,5,6) and not model.get(0x4E0,'h'):selected='stationary_phase_'+str(phase)
        if selected is not None:
            stop=selected;need(i==len(row['steps'])-1,'stop at first source boundary')
    need(row['stop']==stop=='secondary_only_arrived','actual local destination arrival')
    need(row['original_coordinate_write_count']==moved*2,'original coordinate write count')
    need(row['search_popped']==model.search_popped,'independent search queue')
    need(len(model.adjustments)==row['entries'].get('0x470840',0)==1,'natural one occupied-target adjustment')
    need(model.grid(0x4CC)==tuple(c['movement']['path']['goal']),'requested primary location retained')
    need(model.grid(0x4D0)==tuple(model.adjustments[-1]) and model.cell()==tuple(model.adjustments[-1]),'source moved to adjusted cell')
    for call in row['roots']+[v for s in row['steps'] for v in s['calls']]+[row['cleanup']]:abi(call)
    need(row['cleanup']['entry']==0x439C60 and row['cleanup']['receiver']==FINDER+0x18,'explicit original pool cleanup')
    need(not row['final_ownership'][0]['links'] and not row['final_ownership'][1]['links'],'open/closed pool recycled')
    n=len(c['movement']['path']['grid'])*len(c['movement']['path']['grid'][0])
    ownership(row,[(FINDER,FINDER+0x100),(UNIT,UNIT+0x520),(MAP+0x263C4,MAP+0x263C6),(MAP+0x263C8,MAP+0x2646C),
                   (0x10600000,0x10600000+n*12),(0x10700000,0x10700000+n*28),(0x10800000,0x10800000+n*4),(0x10A00000,0x10A10000)])
    if replay:need(NearestMachine(c,table).run()==row,'fresh original route full memory CPU instruction/write trace')
    return dict(name=c['movement']['name'],AI_calls=len(row['steps']),adjustments=model.adjustments,phases=sorted(phases),
                maximum_cooldown=max(cooldowns),positive_cooldown_boundaries=sum(v>0 for v in cooldowns),position_changing_calls=moved,
                original_coordinate_writes=row['original_coordinate_write_count'],stop=stop,instructions=row['instructions'],writes=row['writes'],full_original_replay=replay)


def verify_flood(row,replay=True,table=None):
    expected=b''.join(struct.pack('<h',max(0,64-abs(x-32)-abs(y-32))) for y in range(65) for x in range(65))
    need(row['distances_hex']==expected.hex(),'all 4225 original flood cells vs closed-form Manhattan distance')
    need((row['call']['entry'],row['call']['receiver'],row['call']['args'])==(0x43B110,MAP,[DIST,65,65,32,32,64]),'original recursive distance fill root');abi(row['call'])
    ownership(row,[(DIST,DIST+65*65*2),(0x10A00000,0x10A10000)])
    if replay:need(flood(table)==row,'fresh original full flood memory/CPU/trace')
    return dict(cells=4225,instructions=row['instructions'],writes=row['writes'],full_original_replay=replay)


def verify(report_path):
    raw=report_path.read_bytes();data=json.loads(gzip.decompress(raw));need(data['source_contract']==source_contract(),'current source identity')
    table=expected_table();need(data['declared_table_hex']==table.hex(),'all 4225 source-derived table records independently sorted')
    need([r['input'] for r in data['selection']]==selection_corpus(),'complete selection corpus')
    need([r['input'] for r in data['routes']]==movement_corpus(),'complete route corpus')
    need(all(data[k] is False for k in ('R3_complete','R4_complete','R6_complete')),'no global completion')
    rows=[]
    for r in data['selection']:
        rows.append(verify_selection(r,table=table));print('verified select',r['input']['name'],flush=True)
    routes=[]
    for r in data['routes']:
        routes.append(verify_route(r,table=table));print('verified route',r['input']['movement']['name'],flush=True)
    distance=verify_flood(data['flood'],table=table);print('verified original flood',flush=True)
    return dict(schema_version=1,source_report=dict(path=report_path.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=sha(raw)),
                selection=rows,routes=routes,flood=distance,table_sha256=sha(table),
                original_instructions=sum(r['instructions'] for r in rows+routes)+distance['instructions'],
                original_writes=sum(r['writes'] for r in rows+routes)+distance['writes'],
                implementation_sha256={p:sha((ROOT/p).read_bytes()) for p in ('tools/battle_nearest_free.py','tools/battle_nearest_free_emulation.py','tools/battle_nearest_free_verification.py')},
                full_original_constructor_executed=False,all_memory_CPU_and_original_traces_replayed=True,R3_complete=False,R4_complete=False,R6_complete=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    out=ROOT/a.out;need(not out.exists(),'fresh immutable verification output')
    out.write_text(json.dumps(verify(ROOT/a.report),indent=2)+'\n',encoding='utf8',newline='\n')
