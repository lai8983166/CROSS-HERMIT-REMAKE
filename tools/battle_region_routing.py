"""Original MAP05 inputs and independent region search / smoothing rules."""
from functools import lru_cache
from copy import deepcopy
import struct
from tools.school_unitctrl_map_emulation import map_resource
from tools.school_formation_placement_catalog import source_catalog as formation_source
from tools.battle_pathfinding_emulation import need,sha
from tools.battle_route_admission import Model as AdmissionModel


def parse_vpt(raw,w=64,h=96):
    need(len(raw)>=40 and struct.unpack_from('<II',raw)==(len(raw),8),'VPT container size/count')
    offsets=list(struct.unpack_from('<8I',raw,8));need(offsets[0]==40 and offsets==sorted(set(offsets)) and offsets[-1]<len(raw),'VPT ordered chunks')
    graphs=[];indices=[];relocations=[]
    for mode in range(4):
        begin,end=offsets[mode],offsets[mode+1];chunk=raw[begin:end]
        need(chunk[:16]==b'MapEditFlIDCode\x00' and struct.unpack_from('<I',chunk,16)[0]==28,'VPT region marker/version')
        n=struct.unpack_from('<I',chunk,20)[0];need(0<n<=w*h and 24+n*4<=len(chunk),'VPT count bound')
        rel=list(struct.unpack_from('<'+str(n)+'I',chunk,24));need(rel[0]==24+n*4 and rel==sorted(set(rel)),'VPT record offsets')
        rows=[]
        for i,start in enumerate(rel):
            stop=rel[i+1] if i+1<n else len(chunk)
            need(start%4==0 and start+4<=stop<=len(chunk),'VPT record bound')
            x,y,count=struct.unpack_from('<BBh',chunk,start);need(x<w and y<h and count>=0 and start+4+count*12==stop,'VPT record extent')
            edges=[]
            for k in range(count):
                at=start+4+k*12;target=struct.unpack_from('<h',chunk,at)[0];weight=struct.unpack_from('<i',chunk,at+8)[0]
                need(0<=target<n and weight>=0,'VPT edge target/cost');edges.append(dict(target=target,weight=weight,opaque_hex=chunk[at+2:at+8].hex()))
            rows.append(dict(center=[x,y],edges=edges))
        index_at=offsets[mode+4];index_end=offsets[mode+5] if mode<3 else len(raw)
        need(index_end-index_at==w*h*2,'VPT exact cell-index bytes')
        ids=list(struct.unpack_from('<'+str(w*h)+'h',raw,index_at));need(all(0<=v<n for v in ids),'VPT signed cell region IDs')
        need(all(ids[p['center'][1]*w+p['center'][0]]==i for i,p in enumerate(rows)),'VPT center belongs to own region')
        graphs.append(rows);indices.append(ids);relocations.append(rel)
    return dict(width=w,height=h,offsets=offsets,graphs=graphs,cell_regions=indices,relative_records=relocations)


@lru_cache(maxsize=1)
def inputs():
    vpt,vpt_id=map_resource('map05.vpt');logical,logical_id=map_resource('map05.bin');formation=formation_source()
    need(logical.hex()==formation['map_hex'],'same original logical input')
    terrain=bytes.fromhex(formation['terrain_hex']);w,h=struct.unpack_from('<HH',logical,4)
    parsed=parse_vpt(vpt,w,h);rates=[]
    for mode in range(4):rates.append([struct.unpack_from('<i',terrain,logical[16+i*6]*76+12+mode*16)[0] for i in range(w*h)])
    return dict(vpt=vpt,logical=logical,terrain=terrain,parsed=parsed,rates=rates,
                identity=dict(vpt=vpt_id,logical=logical_id,terrain=formation['terrain_source'],terrain_offset=formation['terrain_offset'],terrain_bytes=len(terrain),terrain_sha256=sha(terrain)))


def line(a,b):
    x,y=a;dx,dy=abs(b[0]-x),abs(b[1]-y);sx=1 if b[0]>=x else -1;sy=1 if b[1]>=y else -1;error=0
    for _ in range(max(dx,dy)):
        if dx<dy:
            y+=sy;error+=dx
            if error>=dy:x+=sx;error-=dy
        else:
            x+=sx;error+=dy
            if error>=dx:y+=sy;error-=dx
        yield x,y


def passable(point,mode=0):
    x,y=point;data=inputs();w,h=data['parsed']['width'],data['parsed']['height']
    return 0<=x<w and 0<=y<h and data['rates'][mode][y*w+x]!=0


def clear(a,b,mode=0,occupied=(),avoid=False):
    return all(passable(p,mode) and (not avoid or list(p) not in occupied) for p in line(a,b))


def compress(reverse_chain,mode,occupied=(),avoid=False):
    # Literal state transitions of 44F1E0; intentionally different from fine A*.
    end=len(reverse_chain)-1;limit=end;current=reverse_chain[end];scan=0;points=[]
    for _ in range(10000):
        target=reverse_chain[scan]
        if clear(current,target,mode,occupied,False): # source always passes avoid=0
            points.append(list(target));current=target
            if scan==0:return points
            limit=scan;scan=0;continue
        scan+=1
        if scan!=limit:continue
        if limit!=end:points.append(list(current))
        if scan==0:return points
        limit-=1;current=reverse_chain[limit];scan=0
    raise ValueError('source compression convergence bound')


def oracle(c):
    data=inputs()['parsed'];mode=c['mode'];w,h=data['width'],data['height'];nodes=data['graphs'][mode]
    start,goal=c['start'],c['goal'];first=data['cell_regions'][mode][start[1]*w+start[0]];last=data['cell_regions'][mode][goal[1]*w+goal[0]]
    if first==last:return dict(result=2,points=[],popped=[],reopened=0,improved=0,reverse_chain=[],same_region=True)
    target=nodes[last]['center'];queue=[first];closed=[];records={first:dict(g=0,parent=None)};popped=[];improved=0;reopened=0
    def score(i):return records[i]['g']+sum((a-b)**2 for a,b in zip(nodes[i]['center'],target))
    def insert(i):
        k=0
        while k<len(queue) and score(queue[k])<score(i):k+=1
        queue.insert(k,i)
    while queue:
        i=queue.pop(0);popped.append(list(nodes[i]['center']));r=records[i]
        if i==last:
            chain=[list(goal)];cur=i
            while cur is not None and len(chain)<100:chain.append(nodes[cur]['center']);cur=records[cur]['parent']
            if cur is None:chain.append(list(start))
            return dict(result=1,points=compress(chain,mode,c['occupied'],c['avoid']),popped=popped,reopened=reopened,improved=improved,reverse_chain=chain,same_region=False)
        for edge in nodes[i]['edges']:
            j=edge['target'];p=nodes[j]['center']
            if p==nodes[i]['center'] or (r['parent'] is not None and p==nodes[r['parent']]['center']):continue
            g=r['g']+edge['weight']
            if j not in records:records[j]=dict(g=g,parent=i);insert(j)
            elif g<records[j]['g']:
                if j in queue:queue.remove(j);improved+=1
                else:closed.remove(j);reopened+=1
                records[j].update(g=g,parent=i);insert(j)
        closed.insert(0,i)
    return dict(result=0,points=[],popped=popped,reopened=reopened,improved=improved,reverse_chain=[],same_region=False)


def query_corpus():
    rows=[]
    for mode in range(4):
        nodes=inputs()['parsed']['graphs'][mode]
        for name,a,b in [('long',0,len(nodes)-1),('middle',len(nodes)//4,len(nodes)*3//4),('same',0,0)]:
            rows.append(dict(name='mode'+str(mode)+'_'+name,mode=mode,start=nodes[a]['center'][:],goal=nodes[b]['center'][:],avoid=False,occupied=[]))
        extra=deepcopy(rows[-3]);extra['name']='mode'+str(mode)+'_avoid_occupied';extra['avoid']=True;extra['occupied']=[extra['goal'][:]];rows.append(extra)
    rows.append(dict(name='same_region_blocked_line',mode=0,start=[23,66],goal=[15,73],avoid=False,occupied=[]))
    return rows


def route_corpus():
    nodes=inputs()['parsed']['graphs'][0];rows=[]
    for name,a,b in [('north_south',0,119),('south_north',119,0),('cross_middle',30,90),('reverse_middle',90,30)]:
        rows.append(dict(name=name,start=nodes[a]['center'][:],goal=nodes[b]['center'][:],frames=1024))
    rows.append(dict(name='same_region_fallback',start=[23,66],goal=[15,73],frames=1024))
    return rows


def admission_input(c):
    w,h=inputs()['parsed']['width'],inputs()['parsed']['height']
    grid=[''.join('0' if passable((x,y)) else '1' for x in range(w)) for y in range(h)]
    path=dict(name=c['name'],kind='search',direction=0,grid=grid,start=c['start'],goal=c['goal'],occupied=[],mode=0,avoid=False)
    return dict(movement=dict(name=c['name'],path=path,speed=999,terrain_rate=100,status=0,frames=c['frames'],blocker_speed=0),
                initial_phase=0,retry=0,cooldown=0,movement_type=0,unit_kind=0,ai_mode=0)


class RegionModel(AdmissionModel):
    def __init__(self,c,contract,record_pointer=0x11200000,animation_pointer=0x11300000):
        super().__init__(admission_input(c),contract);self.region_popped=[];self.region_calls=[]
        self.put(0x44,animation_pointer);self.put(0x258,record_pointer)

    def evaluate(self,avoid=False,force_search=False,resume=False):
        start,goal=self.cell(),self.grid(0x4D0)
        needs_region=not (avoid or force_search or resume or start==goal or self.clear(start,goal,False)) and (not self.passable(goal) or sum((a-b)**2 for a,b in zip(start,goal))>=100)
        if needs_region:
            result=oracle(dict(start=list(start),goal=list(goal),mode=0,avoid=False,occupied=[]));self.region_calls.append(result);self.region_popped.extend(result['popped'])
            if result['result']!=2:
                self.last_events.append('region_eval');off=0x2F4
                # The original writes the request start into waypoint[0] before
                # compression and leaves bytes beyond the resulting count intact.
                self.unit[off+34:off+36]=bytes(start)
                self.packet(off,goal,result['points'],start if result['result']==1 else None)
                return result['result']
            return super().evaluate(avoid,True,resume)
        return super().evaluate(avoid,force_search,resume)

    def move(self):
        old=self.c['terrain_rate'];x,y=self.cell();rate=inputs()['rates'][0][y*64+x]
        self.c['terrain_rate']=rate or 50
        try:return super().move()
        finally:self.c['terrain_rate']=old
