"""Original ordinary enemy selection, movement dispatcher and explicit handoff."""
import argparse
import struct
import types
from tools import battle_region_routing_emulation as previous
from tools import battle_pathfinding_emulation as path
from tools.battle_target_acquisition import inputs,corpus

ROOT,SOURCE,need,sha=previous.ROOT,previous.SOURCE,previous.need,previous.sha
CTRL,UNIT,RECORD,MAP,FINE=previous.CTRL,previous.UNIT,previous.RECORD,previous.MAP,previous.FINE
TAIL,COMMON=CTRL+0x10A000,0x12200000
REGIONS=previous.REGIONS+((TAIL,0x20000),(COMMON,0x11000))
EXTRA_RANGES=((0x40AC90,0x40ADA0),(0x43C1D0,0x43C320),(0x468D80,0x468E10),(0x4690A0,0x469170),(0x4697F0,0x469B90),
 (0x469C60,0x469D30),(0x46A050,0x46A0A0),(0x46ABC0,0x46B0A4),(0x46BEB0,0x46BF70),(0x46C9F0,0x46CA60),
 (0x4751F0,0x475370),(0x4756A0,0x475C80),(0x476DD0,0x4771A0),(0x47A920,0x47B340),(0x47B790,0x47B800),
 (0x47C580,0x47C8A0),(0x47CC90,0x47CE70),(0x480480,0x480540),(0x4DDBB0,0x4DDC60))
RANGES=previous.RANGES+EXTRA_RANGES
ROOTS=previous.ROOTS|{0x47A920,0x475700,0x4751F0}
ENTRIES={0x47A920,0x47A9D0,0x47AC80,0x47AED0,0x47B2C0,0x47C580,0x47C690,0x475700,0x4751F0,0x476DD0,0x475270,0x4756A0,0x43C1D0,0x4DDBB0}


def source_contract():
    raw=SOURCE.read_bytes();data=inputs()
    return dict(parent=previous.source_contract(),extra_code=[dict(start=a,end=b,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],
                mapcom=data['identity'],view_masks=data['masks'],basic_skill_table=data['basic_skills'],
                declared_candidate_records_and_faction_matrix=True,source_job=1,healing_random_skill_and_full_attack_supported=False,
                command_dispatch_root=0x475700,explicit_supplemental_request_consumer_root=0x4751F0,native_world_or_damage_complete=False)


def validate(c):
    need(set(c)=={'name','kind','policy','scope','view','interval','counter','calls','allow_base','method','initial_skill','candidates','relations','include_self','actor_faction'},'exact target input fields')
    need(c['kind'] in ('scan','command') and isinstance(c['name'],str) and c['name'],'declared kind/name')
    for key,lo,hi in [('policy',0,11),('scope',0,2),('view',0,32),('interval',0,100),('counter',-2147483648,2147483647),('calls',1,16),('actor_faction',0,3)]:
        need(type(c[key]) is int and lo<=c[key]<=hi,'declared '+key)
    need(type(c['allow_base']) is bool and type(c['include_self']) is bool and type(c['method']) is int and c['method'] in (0,2,4),'declared target flags')
    need(type(c['initial_skill']) is int and c['initial_skill'] in (-1,101),'declared existing basic skill')
    need(len(c['relations'])==16 and all(type(v) is int and 0<=v<=3 for v in c['relations']),'source relation entries')
    need(len(c['candidates'])<=8 and len({p['id'] for p in c['candidates']})==len(c['candidates']),'bounded distinct unit slots')
    for p in c['candidates']:
        need(set(p)=={'id','cell','fraction','faction','state','record_id','alive','hp','max_hp','metric','lifetime'},'candidate fields')
        for key,lo,hi in [('id',1,8),('faction',0,15),('state',0,29),('record_id',0,500),('alive',0,1),('hp',-32768,32767),('max_hp',1,32767),('metric',0,65535),('lifetime',-2147483648,2147483647)]:
            need(type(p[key]) is int and lo<=p[key]<=hi,'candidate '+key)
        need(len(p['cell'])==2 and all(type(v) is int for v in p['cell']) and 0<=p['cell'][0]<64 and 0<=p['cell'][1]<96,'candidate cell')
        need(len(p['fraction'])==2 and all(type(v) is int and 0<=v<=65535 for v in p['fraction']),'candidate fixed fractions')


class TargetMachine(previous.RegionMachine):
    def __init__(self,c):
        validate(c);super().__init__(dict(name=c['name'],start=[29,0],goal=[34,0],mode=0,avoid=False,occupied=[]));self.input=c
        for at,n in REGIONS[len(previous.REGIONS):]:self.uc.mem_map(at,n)
        data=inputs();self.uc.mem_write(COMMON,data['raw'])
        for i,m in enumerate(data['masks']):self.put(MAP+8+i*4,COMMON+m['offset'])
        self.put(RECORD+0xC,1,'H');self.put(RECORD+2,10,'H');self.put(RECORD+0xF,1,'B');self.put(RECORD+0x2C,c['view'],'b');self.put(RECORD+0xA4,c['actor_faction'],'B')
        self.put(UNIT+0x290,4,'B');self.put(UNIT+0x2A7,1,'B')
        for off in (0x4EE,0x4F2,0x4FA,0x4FC):self.put(UNIT+off,-1,'h')
        self.put(UNIT+0x4F2,c['initial_skill'],'h')
        for off,v,fmt in ((0x2B8,c['interval'],'i'),(0x2D4,c['counter'],'i'),(0x2BC,c['scope'],'b'),(0x2BD,c['policy'],'b'),(0x2BE,c['method'],'b'),(0x2C8,int(c['allow_base']),'b')):self.put(UNIT+off,v,fmt)
        for i,v in enumerate(c['relations']):self.put(CTRL+0x115AAC+c['actor_faction']*16+i,v,'B')
        pointers=[UNIT] if c['include_self'] else []
        for p in c['candidates']:
            at=UNIT+p['id']*0x520;rec=RECORD+p['id']*0x100;pointers.append(at)
            self.put(at,1,'H');self.put(at+2,p['id'],'H');self.put(at+0x258,rec);self.put(at+0x290,p['state'],'B')
            self.put(at+0x2EC,(p['cell'][0]*32+16)*65536+p['fraction'][0]);self.put(at+0x2F0,(p['cell'][1]*16+8)*65536+p['fraction'][1])
            for off,v,fmt in ((2,p['record_id'],'H'),(0xF,p['alive'],'B'),(0x14,p['max_hp'],'h'),(0x16,p['hp'],'h'),(0x3A,p['metric'],'H'),(0x24,p['lifetime'],'i'),(0xA4,p['faction'],'B')):self.put(rec+off,v,fmt)
        self.put(CTRL+0xDC8EC,len(pointers))
        for i,p in enumerate(pointers):self.put(CTRL+0xDC8F0+i*4,p)
        self.mutable=[(UNIT,UNIT+0x520),(FINE,FINE+0x100),(previous.STACK,previous.STACK+0x20000)]
        self.mutable += [(a,a+n) for a,n in previous.REGIONS if a in (previous.F_LINK,previous.F_NODE,previous.F_INDEX)]

    base_call=types.FunctionType(path.PathMachine.call.__code__,dict(path.PathMachine.call.__globals__,ROOTS=ROOTS,STACK=previous.STACK,RETURN=previous.RETURN))
    snapshot=types.FunctionType(path.PathMachine.snapshot.__code__,dict(path.PathMachine.snapshot.__globals__,REGIONS=REGIONS))
    # Private source-hook copy widens only code admission; previous modules stay frozen.
    source_code=types.FunctionType(previous.RegionMachine.code.__code__,dict(previous.RegionMachine.code.__globals__,RANGES=RANGES))

    def code(self,uc,at,size,context):
        self.source_code(uc,at,size,context)
        if at in ENTRIES:self.entries[hex(at)]+=1

    def run(self):
        c=self.input;initial=self.snapshot();roots=[];steps=[];consumer=None
        if c['kind']=='command':roots=[self.call(0x437C90,(UNIT+off,),FINE) for off in (0x2F4,0x3E0)]
        entry=0x47A920 if c['kind']=='scan' else 0x475700
        for i in range(c['calls']):
            before=self.unit();call=self.call(entry,(UNIT,));steps.append(dict(index=i,before_hex=before,after_hex=self.unit(),call=call))
            if c['kind']=='command' and self.get(UNIT+0x292,'B'):
                before=self.unit();consumer=dict(before_hex=before,call=self.call(0x4751F0,(UNIT,)),after_hex=self.unit());break
        cleanup=[self.call(0x439C60,receiver=FINE+0x18)]
        return dict(input=c,initial=initial,roots=roots,steps=steps,consumer=consumer,cleanup=cleanup,**self.common())


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();need(not (ROOT/a.out).exists(),'fresh original target output')
    rows=[]
    for c in corpus():
        r=TargetMachine(c).run();rows.append(r);print(c['name'],len(r['steps']),'handoff',r['consumer'] is not None,flush=True)
    path.save(a.out,dict(schema_version=1,source_contract=source_contract(),cases=rows,R3_complete=False,R4_complete=False,R6_complete=False))
