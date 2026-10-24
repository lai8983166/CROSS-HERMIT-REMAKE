"""Independent actual-data graph and complete-AI verification plus fresh replay."""
import argparse
import gzip
import json
import struct
from tools.battle_region_routing import inputs,oracle,query_corpus,route_corpus,RegionModel
from tools.battle_region_routing_emulation import (ROOT,SOURCE,CTRL,UNIT,COARSE,FINE,MAP,VPT,PACKET,STACK,RETURN,SCRATCH,
    REGIONS,F_LINK,F_NODE,F_INDEX,C_LINK,C_NODE,C_INDEX,RegionMachine,run_route,source_contract,admission,need,sha)


def abi(call):
    need(call['ESP_after']==call['ESP_before']+4+len(call['args'])*4 and call['cpu_after']['EIP']==RETURN,'original callee pop and actual root return')
    for r in ('EBX','ESI','EDI','EBP'):need(call['cpu_before'][r]==call['cpu_after'][r],'original preserved '+r)


def ownership(row,route=False):
    for k in ('initial','final'):
        need([(r['pointer'],r['bytes']) for r in row[k]]==list(REGIONS),'all 17 exact source ownership regions')
        need(all(len(bytes.fromhex(r['hex']))==r['bytes'] for r in row[k]),'all full source region bytes')
    data=inputs();relocated=bytearray(data['vpt'])
    for off,records in zip(data['parsed']['offsets'][:4],data['parsed']['relative_records']):
        for i,p in enumerate(records):struct.pack_into('<I',relocated,off+24+i*4,VPT+off+p)
    initial=next(r for r in row['initial'] if r['pointer']==VPT);final=next(r for r in row['final'] if r['pointer']==VPT)
    need(bytes.fromhex(initial['hex'])==data['vpt']+bytes(initial['bytes']-len(data['vpt'])),'original VPT input bytes')
    need(bytes.fromhex(final['hex'])==relocated+bytes(final['bytes']-len(relocated)),'all 456 source relocation entries and unchanged graph/cell IDs')
    mutable=[(COARSE,COARSE+0xD8),(FINE,FINE+0x100),(SCRATCH,SCRATCH+200),(STACK,STACK+0x20000),(VPT,VPT+len(data['vpt']))]
    mutable += [(a,a+n) for a,n in REGIONS if a in (F_LINK,F_NODE,F_INDEX,C_LINK,C_NODE,C_INDEX)]
    mutable += [(UNIT,UNIT+0x520)] if route else [(PACKET,PACKET+236)]
    for before,after in zip(row['initial'],row['final']):
        a,b=bytes.fromhex(before['hex']),bytes.fromhex(after['hex']);start=before['pointer'];cursor=0
        spans=sorted((max(0,lo-start),min(len(a),hi-start)) for lo,hi in mutable if lo<start+len(a) and start<hi)
        for lo,hi in spans:
            need(a[cursor:lo]==b[cursor:lo],'unrelated map/controller/units remain unchanged '+hex(start+cursor));cursor=max(cursor,hi)
        need(a[cursor:]==b[cursor:],'readonly trailing owned bytes '+hex(start+cursor))
    for kind,base in [('coarse',COARSE+0x10),('fine',FINE+0x18)]:
        owned=row['ownership'][kind];need([p['head'] for p in owned]==[base+0x44,base+0x50,base+0x78],'exact original pool heads')
        need(not owned[0]['links'] and not owned[1]['links'] and len(owned[2]['links'])==len(set(owned[2]['links']))==6144,'all pool links freed exactly once')
    need(not row['game_function_results_stubbed'] and not row['OS_input_submitted'] and not row['host_unit_fields_changed_after_initialization'],'source execution without game/OS substitutes')


def roots(row,query=False):
    expected=[(0x44E5D0,COARSE,[i]) for i in range(4)]
    if query:expected.append((0x44E9A0,COARSE,[PACKET]))
    else:expected.extend((0x437C90,FINE,[UNIT+off]) for off in (0x2F4,0x3E0))
    need([(r['entry'],r['receiver'],r['args']) for r in row['roots']]==expected,'original relocation and empty-packet roots only')
    need([(r['entry'],r['receiver'],r['args']) for r in row['cleanup']]==[(0x439C60,COARSE+0x10,[]),(0x439C60,FINE+0x18,[])],'explicit original dual pool cleanup')
    for r in row['roots']+row['cleanup']:abi(r)


def scratch(row,chains):
    raw=bytearray(SOURCE.read_bytes()[SCRATCH-0x400000:SCRATCH-0x400000+200])
    for chain in chains:
        content=bytes(v for p in chain for v in p);need(len(content)<=200,'source compression scratch bound');raw[:len(content)]=content
    end=next(b for b in row['final'] if b['pointer']==0x7A3000)
    actual=bytes.fromhex(end['hex'])[SCRATCH-0x7A3000:SCRATCH-0x7A3000+200]
    need(actual==raw,'independent complete global compression buffer with retained tail')


def verify_query(row,replay=True):
    c=row['input'];pred=oracle(c);call=row['call'];abi(call);roots(row,True);ownership(row)
    need((call['entry'],call['receiver'],call['args'])==(0x44EA80,COARSE,[*c['start'],*c['goal'],PACKET,c['mode'],int(c['avoid'])]),'actual coarse query root')
    need(call['result']==pred['result'],'independent graph return')
    packet=bytearray(236);struct.pack_into('<hh',packet,24,-1,-1);packet[28:30]=b'\xff\xff'
    if pred['result']!=2:
        struct.pack_into('<hhHH',packet,24,*c['goal'],65535,0) # start bytes remain FF; cursor zero
        struct.pack_into('<H',packet,32,len(pred['points']));packet[34:36]=bytes(c['start'])
        for i,p in enumerate(pred['points']):packet[34+i*2:36+i*2]=bytes(p)
    need(row['packet_hex']==packet.hex(),'entire independent original query packet')
    need(row['popped']==dict(coarse=pred['popped'],fine=[]),'independent region queue and unused fine search')
    need((row['reopened'],row['improved'])==(pred['reopened'],pred['improved']),'independent open improvement and closed reopen')
    need(row['original_coordinate_writes']==0,'query never moves original unit')
    scratch(row,[pred['reverse_chain']] if pred['result']==1 else [])
    if replay:need(RegionMachine(c).query()==row,'fresh source query all memory CPU instruction and write trace')
    return dict(name=c['name'],result=pred['result'],waypoints=pred['points'],popped=len(pred['popped']),reopened=pred['reopened'],improved=pred['improved'],
                instructions=row['instructions'],writes=row['writes'],all_memory_and_original_trace_replayed=replay)


def verify_route(row,replay=True):
    c=row['input'];m=RegionModel(c,admission.source_contract());stop='frame_budget';moved=0;phases=set();roots(row);ownership(row,True)
    need(1<=len(row['steps'])<=c['frames'],'declared route budget')
    for i,step in enumerate(row['steps']):
        need(step['index']==i and step['before_hex']==m.unit.hex(),'continuous complete original before unit '+c['name']+' '+str(i))
        before=bytes(m.unit);m.step();phase=m.get(0x293,'B');phases.add(phase)
        need(step['after_hex']==m.unit.hex() and step['phase']==phase,'independent full region/fine unit '+c['name']+' '+str(i))
        call=step['call'];need((call['entry'],call['receiver'],call['args'])==(0x476680,CTRL,[UNIT,0]),'one complete original AI root');abi(call)
        moved+=before[0x2EC:0x2F4]!=m.unit[0x2EC:0x2F4];selected=None
        if phase==8:selected='next_tile_blocked'
        elif before==m.unit and phase in (0,3,4,5,6) and not m.get(0x4E0,'h'):selected='stationary_phase_'+str(phase)
        if selected:
            stop=selected;need(i==len(row['steps'])-1,'first natural stationary source boundary')
    need(row['stop']==stop=='stationary_phase_3' and m.cell()==tuple(c['goal']),'actual requested-cell arrival; no attack claim')
    need(row['original_coordinate_writes']==moved*2,'source coordinate writes')
    need(row['popped']==dict(coarse=m.region_popped,fine=m.search_popped),'independent both search queue histories')
    need(len(m.region_calls)==row['entries'].get('0x44ea80',0)>=1,'natural full-AI coarse entry')
    need(m.partials==0,'this actual-map corpus has no partial fine frontier projection')
    scratch(row,[r['reverse_chain'] for r in m.region_calls if r['result']==1])
    if replay:need(run_route(c)==row,'fresh source AI all memory CPU instruction and write trace')
    return dict(name=c['name'],AI_calls=len(row['steps']),phases=sorted(phases),region_calls=len(m.region_calls),
                region_results=[r['result'] for r in m.region_calls],region_expansions=len(m.region_popped),fine_expansions=len(m.search_popped),
                position_changing_calls=moved,original_coordinate_writes=row['original_coordinate_writes'],stop=stop,
                final_cell=list(m.cell()),instructions=row['instructions'],writes=row['writes'],whole_unit_model=True,all_memory_and_original_trace_replayed=replay)


def verify(report_path):
    raw=report_path.read_bytes();data=json.loads(gzip.decompress(raw));need(data['source_contract']==source_contract(),'source/data identity')
    need([r['input'] for r in data['queries']]==query_corpus() and [r['input'] for r in data['routes']]==route_corpus(),'all declared original-map cases')
    need(all(data[k] is False for k in ('R3_complete','R4_complete','R6_complete')),'no global completion inflation')
    queries=[];routes=[]
    for r in data['queries']:queries.append(verify_query(r));print('verified query',r['input']['name'],flush=True)
    for r in data['routes']:routes.append(verify_route(r));print('verified route',r['input']['name'],flush=True)
    return dict(schema_version=1,source_report=dict(path=report_path.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=sha(raw)),queries=queries,routes=routes,
                original_instructions=sum(r['instructions'] for r in queries+routes),original_writes=sum(r['writes'] for r in queries+routes),
                implementation_sha256={p:sha((ROOT/p).read_bytes()) for p in ('tools/battle_region_routing.py','tools/battle_region_routing_emulation.py','tools/battle_region_routing_verification.py')},
                independent_original_data_graph_full_unit_and_global_scratch=True,full_memory_CPU_and_original_trace_replayed=True,
                original_file_API_or_allocator_executed=False,R3_complete=False,R4_complete=False,R6_complete=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh immutable proof output');out.write_text(json.dumps(verify(ROOT/a.report),indent=2)+'\n',encoding='utf8',newline='\n')
