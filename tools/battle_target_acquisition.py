"""Independent ordinary target filters, priorities, scan cadence and command model."""
from functools import lru_cache
from copy import deepcopy
import struct
from tools.school_map_common_emulation import map_common_resource
from tools.school_map_common_catalog import map_common_inputs
from tools.battle_region_routing import RegionModel
from tools import battle_route_admission_emulation as admission
from tools.battle_pathfinding_emulation import SOURCE,need,sha


@lru_cache(maxsize=1)
def inputs():
    raw,identity=map_common_resource();entries=map_common_inputs(raw)['first_section_entries'];source=SOURCE.read_bytes()
    sizes=[list(struct.unpack_from('<bb',source,0x19558C+i*2)) for i in range(33)];masks=[]
    for e,(w,h) in zip(entries,sizes):
        at=e['file_offset'];data=raw[at:at+e['bytes']];need(w*h<=len(data)<w*h+4 and not any(data[w*h:]),'actual source view mask shape/padding')
        masks.append(dict(offset=at,bytes=len(data),width=w,height=h,hex=data.hex()))
    jobs=[struct.unpack_from('<h',source,0x2B2DA0+i*64)[0] for i in range(8)]
    return dict(raw=raw,identity=identity,masks=masks,basic_skills=jobs,source_reference=dict(job_table=0x6B2D88,skill_table=0x6C2DC8))


def candidate(i,**kw):
    r=dict(id=i,cell=[29+i,0],fraction=[0,0],faction=4,state=2,record_id=10+i,alive=1,hp=100,max_hp=100,metric=100,lifetime=100)
    r.update(kw);return r


def case(name,**kw):
    r=dict(name=name,kind='scan',policy=9,scope=0,view=5,interval=1,counter=0,calls=1,allow_base=False,method=0,initial_skill=-1,
           candidates=[candidate(1,metric=10,hp=70,lifetime=80),candidate(2,metric=200,hp=20,lifetime=-10),candidate(3,metric=50,hp=90,lifetime=400)],
           relations=[1]*16,include_self=True,actor_faction=0)
    r.update(kw);return r


def corpus():
    rows=[case('policy_'+str(p),policy=p) for p in range(1,11)]
    for p in (0,11):rows.append(case('unrecognized_policy_'+str(p),policy=p))
    rows.append(case('stable_tie',policy=1,candidates=[candidate(2),candidate(1)]))
    rows.append(case('fixed_distance_tie',candidates=[candidate(2,cell=[31,0]),candidate(1,cell=[31,0])]))
    rows.append(case('fixed_pixel_distance',policy=9,candidates=[candidate(1,cell=[30,0],fraction=[32768,0]),candidate(2,cell=[30,0])]))
    rows.append(case('unsigned_metric',policy=1,candidates=[candidate(1,metric=32768),candidate(2,metric=65535)]))
    rows.append(case('signed_hp',policy=4,candidates=[candidate(1,hp=-1),candidate(2,hp=32767)]))
    rows.append(case('cadence',interval=3,calls=7))
    rows.append(case('counter_overflow',interval=0,counter=2147483647,calls=2))
    for name,scope,view in [('sight0',1,0),('sight1',1,1),('sight5',1,5),('sight32',1,32),('scope_disabled',2,5)]:rows.append(case(name,scope=scope,view=view))
    for relation in (0,1,2,3):
        r=case('relation_'+str(relation));r['relations'][4]=relation;rows.append(r)
    rows.append(case('same_faction',candidates=[candidate(1,faction=0)]))
    rows.append(case('filters',candidates=[candidate(1,state=12),candidate(2,state=13),candidate(3,alive=0),candidate(4,record_id=405),candidate(5,record_id=406),candidate(6,record_id=387),candidate(7)]))
    rows.append(case('base_allowed',allow_base=True,candidates=[candidate(1,record_id=387),candidate(2)]))
    rows.append(case('no_candidates',candidates=[]))
    for name,values in [('attack_request',{}),('alternate_target_action',dict(method=2)),('forced_attack_method',dict(method=4,initial_skill=101)),('delayed_scan',dict(interval=3)),('move_without_enemy',dict(candidates=[],calls=8)),('move_scan_not_ready',dict(interval=100,calls=8)),('disabled_search_move',dict(scope=2,calls=8))]:
        values.setdefault('calls',8);rows.append(case(name,kind='command',**values))
    return rows


def choose(c,actor_cell=(29,0)):
    if c['scope'] not in (0,1):return None
    best=None
    for p in c['candidates']:
        if p['faction']==c['actor_faction']:continue
        if c['relations'][p['faction']] not in (1,2):continue
        if p['state'] in (1,12,13,25) or not p['alive'] or p['record_id'] in (405,406):continue
        if 387<=p['record_id']<=404 and not c['allow_base']:continue
        if c['scope']==1:
            m=inputs()['masks'][c['view']];dx,dy=abs(p['cell'][0]-actor_cell[0]),abs(p['cell'][1]-actor_cell[1]);rx,ry=(m['width']-1)//2,(m['height']-1)//2
            if dx>rx or dy>ry or not bytes.fromhex(m['hex'])[(dy+ry)*m['width']+dx+rx]:continue
        if best is None:best=p;continue
        field={1:'metric',2:'metric',3:'hp',4:'hp',5:'hp',6:'hp',7:'lifetime',8:'lifetime'}.get(c['policy'])
        if field is not None:a,b=best[field],p[field]
        elif c['policy'] in (9,10):
            def distance(q):
                return abs((q['cell'][0]-actor_cell[0])*32*65536+q['fraction'][0])+abs((q['cell'][1]-actor_cell[1])*16*65536+q['fraction'][1])
            a,b=distance(best),distance(p)
        else:continue
        if (b>a if c['policy'] in (1,3,5,7,10) else b<a):best=p
    return best


class Model(RegionModel):
    def __init__(self,c):
        super().__init__(dict(name=c['name'],start=[29,0],goal=[34,0],frames=1024),admission.source_contract());self.config=c
        if c['kind']=='scan':self.unit[0x2F4:0x4CC]=bytes(472)
        self.put(0x290,4,'B');self.put(0x2A7,1,'B');self.route['unit_kind']=1
        for off in (0x4EE,0x4F2,0x4FA,0x4FC):self.put(off,-1,'h')
        self.put(0x4F2,c['initial_skill'],'h')
        for off,value,fmt in ((0x2B8,c['interval'],'i'),(0x2D4,c['counter'],'i'),(0x2BC,c['scope'],'b'),(0x2BD,c['policy'],'b'),(0x2BE,c['method'],'b'),(0x2C8,int(c['allow_base']),'b')):self.put(off,value,fmt)

    def scan(self):
        counter=(self.get(0x2D4,'i')+1+2147483648)%4294967296-2147483648;self.put(0x2D4,counter,'i')
        if counter<self.config['interval']:return None
        self.put(0x2D4,0,'i');return choose(self.config,self.cell())

    def command(self):
        phase=self.get(0x293,'B')
        if phase==0:
            self.put(0x294,0,'B');self.put(0x4E0,0,'h');self.put(0x293,1,'B');return None
        p=self.scan()
        if p is not None:
            if self.config['method']==0:
                self.put(0x4EE,p['id'],'h');self.put(0x4F2,inputs()['basic_skills'][1],'h');self.put(0x4F0,p['cell'][0],'B');self.put(0x4F1,p['cell'][1],'B');self.put(0x292,6,'B')
                return p
            elif self.config['method']==4:self.put(0x292,6,'B');return p
            elif self.config['method']==2:self.put(0x4EE,p['id'],'h');self.put(0x292,29,'B')
        # Logical adapter for the already verified movement rules; the actual
        # source 476680(unit,1) uses +294 rather than the command's +293.
        command_phase=self.get(0x293,'B');self.put(0x293,self.get(0x294,'B'),'B')
        super().step();self.put(0x294,self.get(0x293,'B'),'B');self.put(0x293,command_phase,'B')
        return p

    def consume(self):
        pending=self.get(0x292,'B')
        if pending:
            self.put(0x291,self.get(0x290,'B'),'B');self.put(0x290,pending,'B');self.put(0x292,0,'B');self.put(0x293,0,'B')
            # The empty layer cleanup executes but its zero fields stay zero.
