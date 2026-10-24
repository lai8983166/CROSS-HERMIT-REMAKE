"""Independent two-packet model and full original admission-state-machine replay."""
import argparse
import gzip
import json
from tools.battle_route_admission import Model,corpus
from tools.battle_route_admission_emulation import ROOT,UNIT,CTRL,FINDER,REGIONS,AdmissionMachine,source_contract,need,sha


def verify_case(row,replay=True):
    c=row['input'];model=Model(c,source_contract());events={};phases=set();moved=0;stop='frame_budget'
    need(not row['host_unit_fields_changed_after_initialization'] and not row['game_or_math_results_stubbed'] and not row['OS_input_submitted'],'isolated original execution scope')
    need([(r['entry'],r['receiver'],r['args']) for r in row['roots']]==[(0x437C90,FINDER,[UNIT+off]) for off in (0x2F4,0x3E0)],'empty packets only; no host search roots')
    need(1<=len(row['steps'])<=c['movement']['frames'],'bounded original AI steps')
    for i,step in enumerate(row['steps']):
        need(step['index']==i and step['before_hex']==model.unit.hex(),'continuous complete admission unit '+c['movement']['name']+' '+str(i))
        before=bytes(model.unit);phases.add(model.get(0x293,'B'));model.step();phase=model.get(0x293,'B');phases.add(phase)
        need(step['after_hex']==model.unit.hex() and step['phase']==phase,'independent full primary/local unit '+c['movement']['name']+' '+str(i))
        need(len(step['calls'])==1 and (step['calls'][0]['entry'],step['calls'][0]['receiver'],step['calls'][0]['args'])==(0x476680,CTRL,[UNIT,0]),'single original AI root')
        for e in model.last_events:events[e]=events.get(e,0)+1
        moved+=before[0x2EC:0x2F4]!=model.unit[0x2EC:0x2F4]
        selected=None
        if phase==8:selected='next_tile_blocked'
        elif phase==3 and model.get(0x314,'H')==0:selected='secondary_only_arrived'
        elif before==model.unit and phase in (0,3,4,5,6) and model.get(0x4E0,'h')==0:selected='stationary_phase_'+str(phase)
        if selected is not None:
            stop=selected;need(i==len(row['steps'])-1,'no extra roots after declared route boundary')
    need(row['stop']==stop,'honest route exhaustion/gating/budget stop')
    if stop=='frame_budget':need(len(row['steps'])==c['movement']['frames'],'full requested AI budget')
    need(row['search_popped']==model.search_popped,'independent persistent search queue order')
    need(row['original_coordinate_write_count']==moved*2,'actual coordinate writes distinguish gated/waiting roots')
    for key in ('initial','final'):
        need([(b['pointer'],b['bytes']) for b in row[key]]==list(REGIONS),'all exact source ownership regions')
        need(all(len(bytes.fromhex(b['hex']))==b['bytes'] for b in row[key]),'full source ownership bytes')
    for before,after in zip(row['initial'],row['final']):
        a,b=bytes.fromhex(before['hex']),bytes.fromhex(after['hex'])
        if before['pointer']==CTRL:
            for lo,hi in ((0,FINDER-CTRL),(FINDER-CTRL+0x100,UNIT-CTRL),(UNIT-CTRL+0x520,len(a))):
                need(a[lo:hi]==b[lo:hi],'unrelated controller/map/other units unchanged')
            need(b[UNIT-CTRL:UNIT-CTRL+0x520]==model.unit,'final whole unit in complete controller snapshot')
        elif before['pointer'] not in (0x10600000,0x10700000,0x10800000,0x10A00000):need(a==b,'read-only source input/unused parent descriptor')
    for call in row['roots']+[v for step in row['steps'] for v in step['calls']]+[row['cleanup']]:
        need(call['ESP_after']==call['ESP_before']+4+4*len(call['args']) and call['cpu_after']['EIP']==0x10B00000,'original ret and ESP')
        for reg in ('EBX','ESI','EDI','EBP'):need(call['cpu_before'][reg]==call['cpu_after'][reg],'original callee-saved '+reg)
    need(row['cleanup']['entry']==0x439C60 and row['cleanup']['receiver']==FINDER+0x18,'explicit source finder cleanup')
    need(not row['final_ownership'][0]['links'] and not row['final_ownership'][1]['links'],'current pool lists reclaimed')
    if replay:need(AdmissionMachine(c).run()==row,'fresh all-memory/CPU/instruction/write reproduction')
    return dict(name=c['movement']['name'],AI_calls=len(row['steps']),phases=sorted(phases),events=events,stop=stop,position_changing_calls=moved,
                search_popped=len(model.search_popped),partial_search_returns=model.partials,primary_cursor=model.get(0x312,'H'),primary_count=model.get(0x314,'H'),
                final_position_fixed=[model.get(0x2EC,'i'),model.get(0x2F0,'i')],instructions=row['instructions'],writes=row['writes'],
                whole_unit_independent_model=True,all_memory_and_trace_reproduced=replay,attack_or_scene_complete=False)


def verify(path):
    raw=path.read_bytes();report=json.loads(gzip.decompress(raw));need(report['source_contract']==source_contract(),'original admission source identity')
    need([r['input'] for r in report['cases']]==corpus(),'complete declared route corpus')
    need(all(report[k] is False for k in ('R3_complete','R4_complete','R6_complete')),'no global completion inflation')
    rows=[]
    for row in report['cases']:
        rows.append(verify_case(row));print('verified',row['input']['movement']['name'],flush=True)
    return dict(schema_version=1,source_report=dict(path=path.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=sha(raw)),case_count=len(rows),cases=rows,
                original_instructions=sum(r['instructions'] for r in rows),original_writes=sum(r['writes'] for r in rows),
                implementation_sha256={p:sha((ROOT/p).read_bytes()) for p in ('tools/battle_route_admission.py','tools/battle_route_admission_emulation.py','tools/battle_route_admission_verification.py')},
                independent_whole_unit_and_persistent_queue=True,full_memory_and_original_trace_replayed=True,R3_complete=False,R4_complete=False,R6_complete=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args()
    out=ROOT/a.out;need(not out.exists(),'fresh immutable proof output');out.write_text(json.dumps(verify(ROOT/a.report),indent=2)+'\n',encoding='utf8',newline='\n')
