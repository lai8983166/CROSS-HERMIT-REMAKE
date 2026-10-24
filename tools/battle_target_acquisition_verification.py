"""Independent full-unit target/command model and fresh source memory/CPU replay."""
import argparse
import gzip
import json
from tools.battle_target_acquisition import Model,corpus,inputs
from tools.battle_target_acquisition_emulation import (ROOT,CTRL,UNIT,FINE,COMMON,REGIONS,TargetMachine,source_contract,previous,need,sha)


def abi(call):
    need(call['ESP_after']==call['ESP_before']+4+len(call['args'])*4 and call['cpu_after']['EIP']==previous.RETURN,'original ret/ESP')
    for reg in ('EBX','ESI','EDI','EBP'):need(call['cpu_before'][reg]==call['cpu_after'][reg],'source preserved '+reg)


def ownership(row,m):
    for key in ('initial','final'):
        need([(r['pointer'],r['bytes']) for r in row[key]]==list(REGIONS),'all exact 19 ownership regions')
        need(all(len(bytes.fromhex(r['hex']))==r['bytes'] for r in row[key]),'all complete owned bytes')
    mutable=[(UNIT,UNIT+0x520),(FINE,FINE+0x100),(previous.STACK,previous.STACK+0x20000)]
    mutable += [(a,a+n) for a,n in REGIONS if a in (previous.F_LINK,previous.F_NODE,previous.F_INDEX)]
    for before,after in zip(row['initial'],row['final']):
        a,b=bytes.fromhex(before['hex']),bytes.fromhex(after['hex']);base=before['pointer'];cursor=0
        spans=sorted((max(0,lo-base),min(len(a),hi-base)) for lo,hi in mutable if lo<base+len(a) and base<hi)
        for lo,hi in spans:
            need(a[cursor:lo]==b[cursor:lo],'readonly map/candidates/records/view/relation bytes '+hex(base+cursor));cursor=max(cursor,hi)
        need(a[cursor:]==b[cursor:],'readonly remaining owned bytes '+hex(base+cursor))
    controller=next(r for r in row['final'] if r['pointer']==CTRL)
    need(bytes.fromhex(controller['hex'])[UNIT-CTRL:UNIT-CTRL+0x520]==m.unit,'independent final full unit in actual controller')
    raw=inputs()['raw'];common=next(r for r in row['final'] if r['pointer']==COMMON)
    need(bytes.fromhex(common['hex'])==raw+bytes(common['bytes']-len(raw)),'actual original view input unchanged')
    for kind,obj,offset in [('fine',FINE,0x18),('coarse',previous.COARSE,0x10)]:
        pools=row['ownership'][kind];need([r['head'] for r in pools]==[obj+offset+d for d in (0x44,0x50,0x78)],'exact independent pool heads')
        need(not pools[0]['links'] and not pools[1]['links'] and len(pools[2]['links'])==len(set(pools[2]['links']))==6144,'all actual nodes reclaimed')


def verify_case(row,replay=True):
    c=row['input'];m=Model(c);results=[];moved=0;scans=0;counter_ready=0
    expected_roots=[] if c['kind']=='scan' else [(0x437C90,FINE,[UNIT+off]) for off in (0x2F4,0x3E0)]
    need([(r['entry'],r['receiver'],r['args']) for r in row['roots']]==expected_roots,'only declared empty packet initializers')
    need(1<=len(row['steps'])<=c['calls'],'declared target call budget')
    for i,step in enumerate(row['steps']):
        need(step['index']==i and step['before_hex']==m.unit.hex(),'continuous whole before unit '+c['name']+' '+str(i))
        before=bytes(m.unit);before_counter=m.get(0x2D4,'i');p=m.scan() if c['kind']=='scan' else m.command()
        need(step['after_hex']==m.unit.hex(),'independent complete scan/command unit '+c['name']+' '+str(i))
        call=step['call'];abi(call);entry=0x47A920 if c['kind']=='scan' else 0x475700
        need((call['entry'],call['receiver'],call['args'])==(entry,CTRL,[UNIT]),'whole source root, no child scheduling')
        expected=UNIT+p['id']*0x520 if c['kind']=='scan' and p else 0
        need(call['result']==expected,'independent target pointer / dispatcher return')
        results.append(p['id'] if p else None);moved+=before[0x2EC:0x2F4]!=m.unit[0x2EC:0x2F4]
        scanned=c['kind']=='scan' or before[0x293]==1
        scans+=scanned
        incremented=(before_counter+1+2147483648)%4294967296-2147483648
        if scanned and incremented>=c['interval']:counter_ready+=1
        if m.get(0x292,'B'):need(i==len(row['steps'])-1,'stop at first actual pending request')
    pending=m.get(0x292,'B');consumer=row['consumer']
    if pending:
        need(c['kind']=='command' and consumer is not None and consumer['before_hex']==m.unit.hex(),'current request consumer boundary')
        need((consumer['call']['entry'],consumer['call']['receiver'],consumer['call']['args'])==(0x4751F0,CTRL,[UNIT]),'explicit supplemental source consumer root');abi(consumer['call'])
        m.consume();need(consumer['after_hex']==m.unit.hex(),'entire original consumed-command state')
    else:need(consumer is None and len(row['steps'])==c['calls'],'no invented request or early budget stop')
    need(row['popped']==dict(coarse=[],fine=m.search_popped),'unused graph and independent local search')
    need(not m.region_calls and m.partials==0,'no unmodeled graph/partial frontier')
    need(row['original_coordinate_writes']==moved*2,'only actual original coordinate writes')
    need(row['entries'].get('0x47a920',0)==scans,'source scan cadence root count')
    need(row['entries'].get('0x47a9d0',0)==counter_ready,'source scan-not-ready gate')
    need([(r['entry'],r['receiver'],r['args']) for r in row['cleanup']]==[(0x439C60,FINE+0x18,[])],'explicit fine pool cleanup')
    for call in row['roots']+row['cleanup']:abi(call)
    need(not row['OS_input_submitted'] and not row['game_function_results_stubbed'] and not row['host_unit_fields_changed_after_initialization'],'isolated original execution scope')
    ownership(row,m)
    if replay:need(TargetMachine(c).run()==row,'fresh all-memory CPU and original instruction/write reproduction')
    return dict(name=c['name'],kind=c['kind'],root_calls=len(row['steps']),selected_ids=results,scan_calls=scans,scans_ready=counter_ready,
                requested_command=pending,command_consumed=consumer is not None,final_command=m.get(0x290,'B'),target=m.get(0x4EE,'h'),skill=m.get(0x4F2,'h'),
                position_changing_calls=moved,original_coordinate_writes=row['original_coordinate_writes'],instructions=row['instructions'],writes=row['writes'],
                whole_unit_independent=True,full_memory_CPU_and_original_trace_replayed=replay,attack_or_damage_complete=False)


def verify(report_path):
    raw=report_path.read_bytes();data=json.loads(gzip.decompress(raw));need(data['source_contract']==source_contract(),'source and actual masks identity')
    need([r['input'] for r in data['cases']]==corpus(),'complete normal target corpus')
    need(all(data[k] is False for k in ('R3_complete','R4_complete','R6_complete')),'no global completion inflation')
    rows=[]
    for r in data['cases']:rows.append(verify_case(r));print('verified',r['input']['name'],flush=True)
    return dict(schema_version=1,source_report=dict(path=report_path.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=sha(raw)),case_count=len(rows),cases=rows,
                original_instructions=sum(r['instructions'] for r in rows),original_writes=sum(r['writes'] for r in rows),
                implementation_sha256={p:sha((ROOT/p).read_bytes()) for p in ('tools/battle_target_acquisition.py','tools/battle_target_acquisition_emulation.py','tools/battle_target_acquisition_verification.py')},
                independent_full_unit_and_filters=True,full_memory_CPU_and_original_trace_replayed=True,healing_random_skill_and_full_attack_supported=False,
                original_file_API_or_allocator_executed=False,R3_complete=False,R4_complete=False,R6_complete=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh proof path');out.write_text(json.dumps(verify(ROOT/a.report),indent=2)+'\n',encoding='utf8',newline='\n')
