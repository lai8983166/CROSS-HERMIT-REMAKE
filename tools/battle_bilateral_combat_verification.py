"""Independent bilateral boundary contracts plus exact complete original replay."""
import argparse
from copy import deepcopy
from concurrent.futures import ProcessPoolExecutor
import gzip
import json
import struct
from types import SimpleNamespace
from tools.battle_bilateral_combat import corpus,validate,declarations,validate_pages,expand
from tools.battle_bilateral_combat_emulation import BilateralMachine,ROOT,CTRL,UNIT,TARGET,RECORD,ANIM,REGIONS,FINE,source_contract,need,sha
from tools import battle_bilateral_combat_model as model
from tools.battle_hit_damage_verification import root,full_cpu,platform
from tools.battle_world_update_emulation import WORLD_ENTRIES,STAGES

EXPECTED_ENTRIES=[0x46B470,0x4678C0,0x493630,0x467B60,0x46E9C0,0x49B180,0x46E520,0x46E730,0x48CD90,0x46EA10,0x46F440,0x490FC0,0x49CC60,0x49C400,0x466880,0x493A30,0x48CE60]
IMPLEMENTATIONS=tuple('tools/battle_bilateral_combat'+s+'.py' for s in ('','_model','_emulation','_verification'))


def ownership(row):
    fixture=BilateralMachine(row['input']);mutable=fixture.mutable
    for k in ('initial','final'):
        need([(r['pointer'],r['bytes']) for r in row[k]]==list(REGIONS),'all 37 exact owned regions')
        need(all(len(bytes.fromhex(r['hex']))==r['bytes'] for r in row[k]),'all owned raw bytes retained')
    for b,a in zip(row['initial'],row['final']):
        before,after=bytes.fromhex(b['hex']),bytes.fromhex(a['hex']);base=b['pointer'];cursor=0
        for lo,hi in sorted((max(0,lo-base),min(len(before),hi-base)) for lo,hi in mutable if lo<base+len(before) and base<hi):
            need(before[cursor:lo]==after[cursor:lo],'readonly bilateral original bytes '+hex(base+cursor));cursor=max(cursor,hi)
        need(before[cursor:]==after[cursor:],'readonly bilateral tail '+hex(base+cursor))
    for kind in ('fine','coarse'):
        pools=row['ownership'][kind];need(not pools[0]['links'] and not pools[1]['links'] and len(set(pools[2]['links']))==len(pools[2]['links'])==6144,'both 6144-node pools reclaimed')
    final=bytes.fromhex(expand(row['final_state'],row['blobs'])['unit'])
    need(len(final)==0x520,'complete actor state after cleanup')


def verify_case(row,replay=True):
    c=row['input'];validate(c);need('request' not in row,'no independent attack request')
    for key,h in row['blobs'].items():need(0<len(bytes.fromhex(h))<=4096 and sha(bytes.fromhex(h))==key,'lossless page identity')
    validate_pages(row,row['blobs'])
    for at,value,fmt in declarations(c):
        region=next(r for r in row['initial'] if r['pointer']<=at and at+struct.calcsize('<'+fmt)<=r['pointer']+r['bytes'])
        need(struct.unpack_from('<'+fmt,bytes.fromhex(region['hex']),at-region['pointer'])[0]==value,'exact fresh bilateral declaration '+hex(at))
    root(row['target_bind']['call'],0x467020,CTRL,[TARGET,c['aftermath']['combat']['job']]);root(row['bind'],0x467020,CTRL,[UNIT,c['aftermath']['combat']['job']])
    need(len(row['roots'])==4,'both units get both original packet initializers')
    for call,(u,off) in zip(row['roots'],[(u,o) for u in (UNIT,TARGET) for o in (0x2F4,0x3E0)]):root(call,0x437C90,FINE,[u+off])
    contracts=row['contracts'];frames=row['world_frames'];hp=[1000,1000];expected_stores=[];hits=[];received=[];counts=[0,0];terminal=None;scan_counts=[0,0];selections=[0,0]
    rng=model.Random(c['aftermath']['combat']['seed']);crt=c['aftermath']['combat']['crt_seed'];crt_draws=0
    need(1<len(frames)<=c['budget'],'bounded full worlds')
    by_frame=[[] for _ in frames]
    for e in contracts:
        need(type(e['frame']) is int and 0<=e['frame']<len(frames) and 'after' in e and type(e['result']) is int,'complete observed contract return')
        by_frame[e['frame']].append(e)
    need([e['frame'] for e in contracts]==sorted(e['frame'] for e in contracts),'contract frame order')
    for index,f in enumerate(frames):
        need(f['index']==index,'continuous whole worlds');root(f['call'],0x46B470,CTRL,[])
        need(f['call']['result']==0 and not f['controls'],'natural return without host combat requests')
        need(f['scanned_slots']==[UNIT+j*0x520 for j in range(250)],'all 250 ordered predicates')
        need(f['entries']==EXPECTED_ENTRIES,'complete original helper order')
        need([(u['unit'],u['index'],u['caller']) for u in f['unit_calls']]==[(UNIT,0,0x46B584),(TARGET,1,0x46B584)],'both units naturally dispatched')
        need([s['name'] for s in f['stages']]==list(STAGES.values()),'all world frontiers')
        for s in f['stages']:full_cpu(dict(cpu_before=s['CPU'],cpu_after=s['CPU']));need(s['CPU']['EIP'] in STAGES,'original frontier CPU')
        for u in f['unit_calls']:
            full_cpu(u);need(u['cpu_before']['EIP']==0x46B760 and u['cpu_after']['EIP']==0x46B584 and u['cpu_after']['ESP']==u['cpu_before']['ESP']+12,'natural full unit ret8')
            need(u['result']==u['cpu_after']['EAX'],'actual nested result')
            for reg in ('EBX','ESI','EDI','EBP'):need(u['cpu_before'][reg]==u['cpu_after'][reg],'unit callee saved '+reg)
        es=by_frame[index]
        for entry,ret,n in ((0x475700,0x46B7E1,1),(0x482A30,0x46B86D,2),(0x4918D0,0x46B87D,2),(0x493450,0x46B889,1)):
            expected=[dict(entry=entry,receiver=CTRL,caller=ret,args=[u]+([j] if n==2 else [])) for j,u in enumerate((UNIT,TARGET))]
            need([e for e in f['nested_calls'] if e['entry']==entry]==expected,'whole unit natural child caller '+hex(entry))
        for entry,ret in [(0x4751F0,0x475734),(0x493450,0x46B889)]:
            need([(e['args'],e['caller'],e['receiver']) for e in es if e['entry']==entry]==[([UNIT],ret,CTRL),([TARGET],ret,CTRL)],'two mandatory natural boundary contracts '+hex(entry))
        for entry in (0x475270,0x476250,0x476470,0x4776A0,0x47A920,0x47C580,0x477980):
            projection=lambda e:{k:e[k] for k in ('entry','receiver','caller','args')}
            need([projection(e) for e in es if e['entry']==entry]==[e for e in f['ai_calls'] if e['entry']==entry],'cross-observed natural AI caller '+hex(entry))
        need([{k:e[k] for k in ('entry','receiver','caller','args')} for e in es if e['entry']==0x48AAE0]==[e for e in f['nested_calls'] if e['entry']==0x48AAE0],'both effect identities cross-observed at actual call site')
        for e in es:
            entry=e['entry']
            if entry==0x467E00:
                need((e['before']['battle_seed'],e['before']['battle_draws'])==(rng.seed,rng.count),'continuous battle RNG boundary input');value=rng.next()
                need((e['result'],e['after']['battle_seed'],e['after']['battle_draws'])==(value,rng.seed,rng.count),'independent actual game RNG body')
            elif entry==0x570FE0:
                need(e['before']['CRT_seed']==crt,'continuous CRT seed input');crt=(crt*0x343FD+0x269EC3)&0xFFFFFFFF;crt_draws+=1
                need(e['result']==((crt>>16)&32767) and e['after']['CRT_seed']==crt,'independent CRT random body')
            elif entry==0x48AAE0:
                need(e['receiver']==CTRL and e['caller']==0x482CF2,'natural attack effect call')
                hit=model.hit_contract(e);hits.append(hit);counts[(hit['attacker']-UNIT)//0x520]+=1
            elif entry==0x47A920:
                side=model.UNITS.index(e['args'][0]);scan_counts[side]+=1;selections[side]+=int(model.scan_contract(e,c))
            elif entry in (0x493450,0x472370):
                side=model.UNITS.index(e['args'][0]);need(model.number(model.bytes_at(e['before'],'records',side),0x16)==hp[side],'HP chain from declared initial input')
                stores=(model.hp_contract if entry==0x493450 else model.regen_contract)(e)
                expected_stores.extend(dict(frame=index,pc=0x472658,address=RECORD+side*256+0x16,bytes=2,value=v) for v in stores)
                if stores:hp[side]=model.signed(stores[-1],16)
            elif entry==0x4918D0:
                event=model.damage_contract(e)
                if event:received.append(event)
            else:model.ai_contract(e)
        s=expand(f['after'],row['blobs'])
        need([model.number(bytes.fromhex(s[k]),0x16) for k in ('record','target_record')]==hp,'complete frame HP derives from damage and regeneration contracts')
        need((s['battle_seed'],s['battle_draws'],s['CRT_seed'])==(rng.seed,rng.count,crt),'full frame random state derives from every original RNG call')
        if index:need(f['before']==frames[index-1]['after'],'uninterrupted whole world state')
        done=(counts[0]>=2 and counts[1]>=2*int(c['player_active'])) if c['rounds'] else index==c['budget']-2
        if terminal is None and done:terminal=index
    need(terminal==row['terminal_index']==len(frames)-2,'one full extra original world after acceptance frontier')
    need(row['both_hp_writes']==expected_stores,'every actual HP store independently derived, in order and at original PC')
    raw_stores=[{k:v for k,v in w.items() if k!='frame'} for w in expected_stores]
    need([w for w in row['lifecycle_writes'] if w['address'] in (RECORD+0x16,RECORD+0x116)]==raw_stores,'all HP lifecycle writes cross-observed')
    need(row['hp_writes']==[w for w in raw_stores if w['address']==RECORD+0x116],'legacy target HP observer remains exact')
    need([dict(frame=h['frame'],attacker=h['attacker'],victim=h['victim'],hit_index=i) for i,h in enumerate(hits)]==row['hit_sides'],'all actual hit identities')
    need([e['resolved'] for e in contracts if e['entry']==0x48AAE0]==row['hit'],'all original raw physical observations')
    if c['rounds']:
        need(counts[0]>=2 and counts[1]>=2*int(c['player_active']),'two hits by each active side')
        need(len(received)==len(hits),'every hit produces exactly one received event before stop')
        for victim in (UNIT,TARGET):
            hs=[h for h in hits if h['victim']==victim];rs=[r for r in received if r['victim']==victim]
            need(len(hs)==len(rs),'each victim consumes every actual hit')
            for h,r in zip(hs,rs):
                need(r['attacker_index']==model.UNITS.index(h['attacker']) and r['delta']==h['delta16'] and h['frame']<=r['frame']<=h['frame']+1,'each effect reaches the other unit HP queue on its natural update')
    else:need(not hits and hp==[1000,1000] and len(frames)==96,'full no-attack control')
    if not c['player_active']:need(counts[1]==0,'passive control never attacks')
    need(not row['OS_input_submitted'] and not row['game_function_results_stubbed'] and not row['host_unit_fields_changed_after_initialization'],'original only derived gameplay')
    need(row['original_coordinate_writes']==0,'declared in-range combat has no actor coordinate stores')
    need(not any(w['address'] in (UNIT+0x2EC,UNIT+0x2F0,TARGET+0x2EC,TARGET+0x2F0) for w in row['lifecycle_writes']),'neither side has hidden coordinate movement')
    platform(row['platform'],SimpleNamespace(crt_draws=crt_draws));need(row['entries'].get('0x570fe0',0)==crt_draws and row['entries'].get('0x467e00',0)==rng.count,'all random bodies observed')
    for call in row['cleanup']+row['popup_cleanup']:full_cpu(call)
    ownership(row)
    if replay:
        other=BilateralMachine(c).run();platform(other['platform'],SimpleNamespace(crt_draws=crt_draws));a,b=deepcopy(row),other;a.pop('platform');b.pop('platform');need(a==b,'fresh all memory/CPU/original trace and observer replay')
    return dict(name=c['name'],frames=len(frames),slot_predicates=250*len(frames),unit_updates=2*len(frames),hits_by_side=counts,hit_results=hits,
                received_events=received,HP=hp,HP_stores=len(expected_stores),scans=scan_counts,selections=selections,battle_draws=rng.count,CRT_draws=crt_draws,
                instructions=row['instructions'],writes=row['writes'],actual_API_leaves=len(row['platform']['trace']),
                independent_function_contracts=True,full_state_independent=False,all_memory_CPU_trace_replayed=replay)


def load_case(ref):
    raw=(ROOT/ref['path']).read_bytes();need(len(raw)==ref['bytes'] and sha(raw)==ref['sha256'],'immutable bilateral source identity')
    d=json.loads(gzip.decompress(raw));need(d['source_contract']==source_contract() and len(d['cases'])==1 and d['cases'][0]['input']['name']==ref['name'],'one exact source contract and case')
    need(all(d[k] is False for k in ('R3_complete','R4_complete','R6_complete')),'global milestones remain incomplete');return d['cases'][0]


def verify_reference(task):
    ref,c=task;r=load_case(ref);need(r['input']==c,'exact bilateral corpus input');result=verify_case(r);print('verified',c['name'],result['frames'],flush=True);return result


def verify(p,jobs=3):
    raw=p.read_bytes();d=json.loads(raw);need(d['source_contract']==source_contract(),'bilateral bundle source contract');cs=corpus()
    need([r['name'] for r in d['case_reports']]==[c['name'] for c in cs] and all(d[k] is False for k in ('R3_complete','R4_complete','R6_complete')),'all seven exact cases and no global completion')
    need(1<=jobs<=3,'bounded verifier jobs')
    with ProcessPoolExecutor(max_workers=jobs) as pool:rows=list(pool.map(verify_reference,zip(d['case_reports'],cs)))
    return dict(schema_version=1,source_report=dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=sha(raw)),cases=rows,case_count=len(rows),
                world_frames=sum(r['frames'] for r in rows),slot_predicates=sum(r['slot_predicates'] for r in rows),unit_updates=sum(r['unit_updates'] for r in rows),
                original_instructions=sum(r['instructions'] for r in rows),original_writes=sum(r['writes'] for r in rows),
                implementation_sha256={s:sha((ROOT/s).read_bytes()) for s in IMPLEMENTATIONS},full_state_independent=False,R3_complete=False,R4_complete=False,R6_complete=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);p.add_argument('--jobs',type=int,default=3);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh bilateral proof');out.write_text(json.dumps(verify(ROOT/a.report,a.jobs),indent=2)+'\n',encoding='utf8',newline='\n')
