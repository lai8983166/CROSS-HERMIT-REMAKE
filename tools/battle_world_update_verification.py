"""Whole original world frames, independent state and fresh 57-register replay."""
import argparse
from copy import deepcopy
import gzip
import json
import struct
import types
from tools import battle_combat_aftermath_verification as prior
from tools.battle_world_update import corpus,validate
from tools.battle_world_update_model import Model
from tools.battle_world_update_emulation import (WorldMachine,ROOT,CTRL,UNIT,TARGET,RECORD,REGIONS,WORLD_FIELDS,
                                               VISIBLE_OTHER,parent,source_contract,need,sha)


def state(actual,m,label):
    expected=m.state()
    if actual!=expected:
        keys=[k for k in set(actual)|set(expected) if actual.get(k)!=expected.get(k)]
        raise ValueError('independent world state '+m.world['name']+' '+label+' '+str(keys))


def verify_updates(row,m):
    frames=row['consume']['world_frames'];need(len(frames)==m.world['frames'],'complete bounded continuous world frames')
    for i,f in enumerate(frames):
        need(f['index']==i,'continuous original world index');state(f['before'],m,'world before')
        prior.root(f['call'],0x46B470,CTRL,[])
        need(f['call']['result']==f['call']['cpu_after']['EAX']==(0 if m.world['world_enabled'] else CTRL),'natural whole world return')
        m.pre()
        expected_entries=[0x46B470]
        if m.world['world_enabled']:
            expected_entries += [0x4678C0,0x493630,0x467B60,0x46E9C0,0x49B180,0x46E520,0x46E730,0x48CD90,0x46EA10,0x46F440,
                                 0x490FC0,0x49CC60,0x49C400,0x466880,0x493A30,0x48CE60]
            need(f['scanned_slots']==[UNIT+j*0x520 for j in range(250)],'all 250 source used predicates in exact slot order')
            need([(s['unit'],s['index'],s['caller']) for s in f['unit_calls']]==[(UNIT,0,0x46B584),(TARGET,1,0x46B584)],'only naturally called used slots in order')
            need([s['name'] for s in f['stages']]==['before_units','after_units','world_return'],'original pre/unit/post frontier order')
            state(f['stages'][0]['state'],m,'before_units')
            for call in f['unit_calls']:
                prior.full_cpu(call);state(call['before'],m,'natural unit before')
                result=m.unit_update(call['unit']);need(call['result']==result,'natural nested unit return '+str((i,hex(call['unit']),call['result'],result)))
                need(call['cpu_after']['EAX']==result,'nested unit retained EAX')
                need(call['cpu_before']['EIP']==0x46B760 and call['cpu_after']['EIP']==0x46B584 and
                     call['cpu_after']['ESP']==call['cpu_before']['ESP']+12,'actual nested thiscall return stack')
                for reg in ('EBX','ESI','EDI','EBP'):need(call['cpu_before'][reg]==call['cpu_after'][reg],'nested unit callee saved '+reg)
                state(call['after'],m,'natural unit after')
            state(f['stages'][1]['state'],m,'after_units')
        else:
            need(not f['scanned_slots'] and not f['unit_calls'] and [s['name'] for s in f['stages']]==['world_return'],'total gate naturally skips world work')
        need(f['entries']==expected_entries,'original complete world helper order')
        m.post();state(f['stages'][-1]['state'],m,'world_return');state(f['after'],m,'world after')
        for s in f['stages']:
            prior.full_cpu(dict(cpu_before=s['CPU'],cpu_after=s['CPU']))
            need(s['CPU']['EIP']=={'before_units':0x46B529,'after_units':0x46B586,'world_return':0x46B652}[s['name']],'exact world CPU frontier')
    queued=bool(struct.unpack_from('<I',bytes.fromhex(row['consume']['hp']['before']['target']),0x510)[0])
    values=([struct.unpack_from('<H',bytes.fromhex(row['consume']['hp']['after']['target_record']),0x16)[0]] if queued else [])+m.target_regeneration_stores
    need([w['value'] for w in row['hp_writes']]==values,'all actual hit and world regeneration HP stores')
    for w in row['hp_writes']:need(0x472550<=w['pc']<0x472770 and (w['address'],w['bytes'])==(RECORD+0x116,2),'only original HP store')
    need([w for w in row['lifecycle_writes'] if w['address']==RECORD+0x116]==row['hp_writes'][int(queued):],'world lifecycle HP trace')


def ownership(row,m):
    region=parent.region
    for key in ('initial','final'):
        need([(r['pointer'],r['bytes']) for r in row[key]]==list(REGIONS),'all 37 owned regions retained')
        need(all(len(bytes.fromhex(r['hex']))==r['bytes'] for r in row[key]),'every owned byte retained')
    mutable=[(UNIT,UNIT+0xA40),(RECORD,RECORD+512),(prior.FINE,prior.FINE+0x100),(region.STACK,region.STACK+0x20000),
             (prior.animation_parent.POOL,prior.animation_parent.POOL+2048*88),(prior.EVENT_CTRL,prior.EVENT_CTRL+0x24),
             (prior.EVENTS,prior.EVENTS+16*12),(prior.EVENTS+0x1000,prior.EVENTS+0x1000+16*12),
             (prior.DAMAGE,prior.DAMAGE+512*8),(prior.POPUP,prior.POPUP+512*16),(CTRL+0x2E70C,CTRL+0x2EF44),
             (prior.TLS+0x14,prior.TLS+0x18),(region.OCC,region.OCC+0x3000),(0x7A49E0,0x7A49E4),
             (0x618CF0,0x618CF8),(parent.VISIBLE,parent.VISIBLE+0x2000),(parent.SEEN,parent.SEEN+0x2000),
             (VISIBLE_OTHER,VISIBLE_OTHER+0x2000)]+[(a,a+n) for a,n in WORLD_FIELDS]
    mutable += [(a,a+n) for a,n in REGIONS if a in (region.F_LINK,region.F_NODE,region.F_INDEX)]
    for before,after in zip(row['initial'],row['final']):
        b,a=bytes.fromhex(before['hex']),bytes.fromhex(after['hex']);base=before['pointer'];cursor=0
        for lo,hi in sorted((max(0,lo-base),min(len(b),hi-base)) for lo,hi in mutable if lo<base+len(b) and base<hi):
            need(b[cursor:lo]==a[cursor:lo],'readonly world memory '+hex(base+cursor));cursor=max(cursor,hi)
        need(b[cursor:]==a[cursor:],'readonly world tail '+hex(base+cursor))
    def memory(p,n):
        r=next(x for x in row['final'] if x['pointer']<=p and p+n<=x['pointer']+x['bytes']);b=bytes.fromhex(r['hex']);return b[p-r['pointer']:p-r['pointer']+n]
    for p,b in [(UNIT,m.unit+m.target+bytes(248*0x520)),(RECORD,m.records[0]+m.records[1]),
                (prior.DAMAGE,m.damage_pool),(prior.POPUP,m.popups),(prior.EVENT_CTRL,m.event_ctrl),(CTRL+0x2E714,m.stats),
                (prior.animation_parent.POOL,m.children),(prior.EVENTS,m.event_data),(region.OCC,m.occupancy),
                (parent.VISIBLE,m.visible),(parent.SEEN,m.seen),(VISIBLE_OTHER,m.other),(0x618CF0,m.motion_scratch)]+list(m.fields.items()):
        need(memory(p,len(b))==b,'independent complete owned world memory '+hex(p))
    for kind in ('fine','coarse'):
        pools=row['ownership'][kind];need(not pools[0]['links'] and not pools[1]['links'] and len(pools[2]['links'])==len(set(pools[2]['links']))==6144,'all owned path nodes reclaimed')


def verify_case(row,replay=True):
    cfg=row['input'];validate(cfg)
    # Execute the unchanged, frozen prefix/cleanup proof in a private namespace.
    # Its old input envelope is a view only; the actual world evidence is intact.
    view=dict(row,input=cfg['aftermath'],consume=dict(row['consume'],aftermath=row['consume']['world_frames']))
    verifier=types.FunctionType(prior.verify_case.__code__,dict(prior.verify_case.__globals__,
        Model=lambda _:Model(cfg),REGIONS=REGIONS,state=state,verify_updates=verify_updates,ownership=ownership))
    result=verifier(view,False)
    if replay:
        other=WorldMachine(cfg).run();p,q=row['platform'],other['platform']
        # The frozen prefix verifier already validates each real TLS receipt;
        # compare only per-run native allocation IDs separately.
        prior.platform(q,types.SimpleNamespace(crt_draws=len(p['trace'])//3))
        a,b=deepcopy(row),other;a.pop('platform');b.pop('platform');need(a==b,'fresh all-memory/57-register/world CPU and instruction/write trace reproduction')
        for x in (p,q):
            trace=[{k:v for k,v in leaf.items() if k!='actual_native_index'} for leaf in x['trace']]
            if x is p:expected=trace
            else:need(trace==expected,'fresh actual API role/argument/result reproduction')
    result.update(name=cfg['name'],world_frames=cfg['frames'],scanned_slots=sum(len(f['scanned_slots']) for f in row['consume']['world_frames']),
                  unit_updates=sum(len(f['unit_calls']) for f in row['consume']['world_frames']),all_memory_CPU_trace_replayed=replay)
    return result


def verify(p):
    raw=p.read_bytes();data=json.loads(gzip.decompress(raw));need(data['source_contract']==source_contract(),'original world source contract')
    need([r['input'] for r in data['cases']]==corpus(),'whole declared world corpus')
    need(all(data[k] is False for k in ('R3_complete','R4_complete','R6_complete')),'global milestones incomplete')
    rows=[]
    for r in data['cases']:rows.append(verify_case(r));print('verified',r['input']['name'],flush=True)
    return dict(schema_version=1,source_report=dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=sha(raw)),cases=rows,case_count=len(rows),
                world_frames=sum(r['world_frames'] for r in rows),scanned_slots=sum(r['scanned_slots'] for r in rows),
                unit_updates=sum(r['unit_updates'] for r in rows),original_instructions=sum(r['instructions'] for r in rows),original_writes=sum(r['writes'] for r in rows),
                implementation_sha256={s:sha((ROOT/s).read_bytes()) for s in ('tools/battle_world_update.py','tools/battle_world_update_model.py','tools/battle_world_update_emulation.py','tools/battle_world_update_verification.py')},
                original_native_outer_scheduler_rendering_or_victory_complete=False,R3_complete=False,R4_complete=False,R6_complete=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report',required=True);p.add_argument('--out',required=True);a=p.parse_args();out=ROOT/a.out
    need(not out.exists(),'fresh world proof');out.write_text(json.dumps(verify(ROOT/a.report),indent=2)+'\n',encoding='utf8',newline='\n')
