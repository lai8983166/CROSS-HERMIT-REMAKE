"""Independent primary/local route admission and persistent 1001-node search model."""
from copy import deepcopy
import struct
from tools.battle_unit_movement import Model as MovementModel, corpus as movement_corpus
from tools.battle_pathfinding import source_contract as path_contract


class Search:
    def __init__(self,start,goal,clear,passable,occupied,avoid):
        self.start,self.goal=start,goal;self.clear=clear;self.passable=passable;self.occupied=occupied;self.avoid=avoid
        self.nodes={start:dict(g=0,h=self.h(start),parent=None,open=True,id=0)};self.queue=[start];self.closed=[];self.popped=[]
        self.neighbors=path_contract()['neighbors']

    def h(self,p):return sum((a-b)**2 for a,b in zip(p,self.goal))
    def insert(self,p):
        score=self.nodes[p]['g']+self.nodes[p]['h'];i=0
        while i<len(self.queue) and self.nodes[self.queue[i]]['g']+self.nodes[self.queue[i]]['h']<score:i+=1
        self.queue.insert(i,p)

    def advance(self,w,h):
        chunk=[]
        while self.queue:
            p=self.queue.pop(0);self.popped.append(p);chunk.append(p);n=self.nodes[p]
            if p==self.goal:
                chain=[p]
                while self.nodes[chain[-1]]['parent'] is not None:chain.append(self.nodes[chain[-1]]['parent'])
                chain.reverse();points=[];i=0
                while i<len(chain)-1 and len(points)<100:
                    best=i+1
                    if best<len(chain)-1:
                        for j in range(best,len(chain)):
                            if not self.clear(chain[i],chain[j],self.avoid):break
                            best=j
                    points.append(chain[best]);i=best
                return 1,points,chunk
            for dx,dy,normal in self.neighbors:
                q=p[0]+dx,p[1]+dy
                if q==n['parent'] or not (0<=q[0]<w and 0<=q[1]<h):continue
                cost=normal
                if q!=self.goal:
                    if not self.passable(q):cost=3600
                    if self.avoid and self.occupied(q):cost=100
                g=n['g']+cost
                if q not in self.nodes:
                    self.nodes[q]=dict(g=g,h=self.h(q),parent=p,open=True,id=len(self.nodes));self.insert(q)
                elif g<self.nodes[q]['g']:
                    if self.nodes[q]['open']:self.queue.remove(q)
                    else:self.closed.remove(q)
                    self.nodes[q].update(g=g,parent=p,open=True);self.insert(q)
            n['open']=False;self.closed.insert(0,p)
            if len(chunk)>=1001:return -1,[],chunk
        return 0,[],chunk


class Model(MovementModel):
    def __init__(self,c,contract):
        self.route=c;self.c=c['movement'];self.contract=contract['parent'];self.unit=bytearray(0x520)
        self.put(0,1,'H');self.put(0x44,0x11300000);self.put(0x258,0x11200000);self.put(0x14,self.c['status'],'B')
        self.put(0x293,c['initial_phase'],'B');self.put(0x2A7,c['unit_kind'],'B');self.put(0x4E4,c['retry'],'b');self.put(0x4E0,c['cooldown'],'h')
        x,y=self.c['path']['start'];gx,gy=self.c['path']['goal']
        self.put(0x2EC,(x*32+16)*65536);self.put(0x2F0,(y*16+8)*65536);self.put(0x4D0,gx*32+16,'h');self.put(0x4D2,gy*16+8,'h')
        for off in (0x2F4,0x3E0):self.clear_packet(off)
        self.search=None;self.search_off=None;self.search_popped=[];self.last_events=[];self.partials=0

    def clear_packet(self,off):
        self.unit[off:off+236]=bytes(236);self.put(off+24,-1,'h');self.put(off+26,-1,'h');self.unit[off+28:off+30]=b'\xff\xff'

    def line(self,a,b):
        x,y=a;dx,dy=abs(b[0]-x),abs(b[1]-y);sx=1 if b[0]>=x else -1;sy=1 if b[1]>=y else -1;error=0
        for _ in range(max(dx,dy)):
            if dx<dy:
                y+=sy;error+=dx
                if error>=dy:x+=sx;error-=dy
            else:
                x+=sx;error+=dy
                if error>=dx:y+=sy;error-=dx
            yield x,y

    def clear(self,a,b,avoid):return all(self.passable(p) and (not avoid or not self.occupied(p)) for p in self.line(a,b))
    def packet(self,off,goal,points,start=None,clear=False):
        if clear:self.clear_packet(off)
        self.put(off+24,goal[0],'h');self.put(off+26,goal[1],'h');self.put(off+30,0,'H');self.put(off+32,len(points),'H')
        if start is not None:self.unit[off+28:off+30]=bytes(start)
        for i,p in enumerate(points):self.unit[off+34+i*2:off+36+i*2]=bytes(p)

    def finish_search(self,off):
        rows=self.c['path']['grid'];result,points,chunk=self.search.advance(len(rows[0]),len(rows));self.search_popped.extend([list(p) for p in chunk])
        goal=self.search.goal
        self.put(off+24,goal[0],'h');self.put(off+26,goal[1],'h')
        if result==-1:
            self.partials+=1
            head=lambda seq:0x10600000+self.search.nodes[seq[0]]['id']*12 if seq else 0
            self.unit[off:off+24]=struct.pack('<6I',0,head(self.search.queue),0,0,head(self.search.closed),0)
            return 3
        self.unit[off:off+24]=bytes(24)
        self.packet(off,goal,points,start=self.cell() if result==1 else None)
        self.search=None
        return 1 if result==1 else 0

    def evaluate(self,avoid=False,force_search=False,resume=False):
        self.last_events.append('resume' if resume else 'search_eval' if force_search else 'route_eval')
        off=0x3E0 if avoid else 0x2F4
        if resume:
            if self.search is None:raise ValueError('resume requires original persistent frontier')
            return self.finish_search(off)
        if avoid and not force_search and self.get(0x4E4,'b')>10:return 5
        start,goal=self.cell(),self.grid(0x4D0)
        if start==goal:return 4
        if not force_search and self.clear(start,goal,avoid):
            self.packet(off,goal,[goal],start,True);return 1
        if not force_search and not avoid and (not self.passable(goal) or sum((a-b)**2 for a,b in zip(start,goal))>=100):
            raise ValueError('abstract region graph dependency')
        if not force_search and not self.passable(goal):
            last=start
            for p in self.line(start,goal):
                if not self.passable(p):break
                last=p
            if last!=start:
                self.packet(off,last,[last],start);return 1
        if not self.passable(goal):
            self.packet(off,goal,[goal],start);return 1
        self.search=Search(start,goal,self.clear,self.passable,self.occupied,avoid);self.search_off=off
        return self.finish_search(off)

    def locate(self):
        self.last_events.append('locate');off=0x2F4;self.put(0x4E4,0,'B')
        cur,total=self.get(off+30,'H'),self.get(off+32,'H')
        if cur==total:
            goal=self.pair(off+24);last=tuple(self.unit[off+32+cur*2:off+34+cur*2])
            if goal==last:return 1
            point=goal;result=2
        else:
            point=tuple(self.unit[off+34+cur*2:off+36+cur*2]);self.put(off+30,cur+1,'H');result=0
        for offset,val in ((0x4CC,point[0]*32+16),(0x4CE,point[1]*16+8),(0x4D0,point[0]*32+16),(0x4D2,point[1]*16+8)):
            self.put(offset,val,'h')
        return result

    def arrival(self):
        if self.get(0x3FE,'H')==self.get(0x400,'H') and self.get(0x312,'H')!=self.get(0x314,'H'):
            if sum((a-b)**2 for a,b in zip(self.cell(),self.grid(0x4D0)))<9:
                self.last_events.append('arrival');return 1
        return super().arrival()

    def step(self):
        self.last_events=[];phase=self.get(0x293,'B')
        if self.get(0x4E0,'h'):
            self.put(0x4E0,self.get(0x4E0,'h')-1,'h');return
        if phase==0:
            self.unit[0x2D8:0x2E0]=bytes(8)
            if self.route['movement_type']==4 or (self.route['unit_kind'] and self.route['ai_mode'] in (2,3)):return
            result=self.evaluate()
            phase={1:3,2:1,3:2}.get(result,0)
        elif phase==1:
            result=self.evaluate(force_search=True);phase={1:3,3:2}.get(result,1)
        elif phase==2:
            result=self.evaluate(resume=True);phase=3 if result==1 else 2
        if phase==3:
            result=self.locate()
            if result==0:phase=4
            elif result==2:phase=0
            self.put(0x293,phase,'B');return
        if phase in (4,5,6):
            result=self.evaluate(avoid=True,force_search=phase==5,resume=phase==6)
            if result==0:raise ValueError('screen visibility cooldown branch not covered')
            phase={1:7,2:5,3:6,4:3}.get(result,phase)
        self.put(0x293,phase,'B')
        # The already-verified original phase7/8/9 numeric rules are reused.
        if phase in (7,8,9):
            events=self.last_events[:];super().step();self.last_events=events+self.last_events


def corpus():
    rows=[];base=movement_corpus()
    def add(m,**kw):
        c=dict(movement=deepcopy(m),initial_phase=0,retry=0,cooldown=0,movement_type=0,unit_kind=0,ai_mode=0);c.update(kw);rows.append(c);return c
    for m in base[:8]:add(m)
    add(base[15]) # wall_detour
    add(base[14]) # half_scale
    c=add(base[2],initial_phase=1);c['movement']['name']='force_primary_search'
    for retry in (10,11,-128):
        c=add(base[2],initial_phase=4,retry=retry);c['movement']['name']='retry_'+str(retry)
    c=add(base[2],initial_phase=5);c['movement']['name']='retry_search'
    c=add(base[2],cooldown=3);c['movement']['name']='initial_cooldown'
    c=add(base[2],movement_type=4);c['movement']['name']='movement_type4_gate'
    for mode in (2,3):
        c=add(base[2],unit_kind=1,ai_mode=mode);c['movement']['name']='AI_mode_gate_'+str(mode)
    c=add(base[2]);c['movement']['name']='same_cell';c['movement']['path']['goal']=c['movement']['path']['start'][:]
    c=add(base[2]);c['movement']['name']='primary_partial_1001';c['movement']['frames']=8
    grid=['0'*40 for _ in range(40)]
    for y in range(4,7):
        for x in range(4,7):
            if (x,y)!=(5,5):grid[y]=grid[y][:x]+'1'+grid[y][x+1:]
    c['movement']['path'].update(grid=grid,start=[0,0],goal=[5,5])
    d=deepcopy(c);d['initial_phase']=4;d['movement']['name']='secondary_partial_1001';rows.append(d)
    return rows
