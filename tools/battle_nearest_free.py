"""Independent candidate-order, reservation and full-unit rerouting model."""
from collections import defaultdict
from copy import deepcopy
import struct
from tools.battle_pathfinding import TERRAIN
from tools.battle_route_admission import Model as RouteModel


def expected_table():
    shells = defaultdict(list)
    for y in range(-32, 33):
        for x in range(-32, 33): shells[abs(x)+abs(y)].append((x,y))
    ranked=[]
    for distance, points in shells.items():
        for rank, (x,y) in enumerate(reversed(points)):
            priority = abs(x)<7 and abs(y)<7 and (x-y)%2 != 0
            ranked.append((((distance<<8)+rank-(32768 if priority else 0)) & 65535,x,y,distance))
    return b''.join(struct.pack('<bbHH',x,y,d,i) for i,(_,x,y,d) in enumerate(sorted(ranked)))


def select(c, counter, reservations):
    """Logical oracle: no source process memory or recorded outputs are read."""
    counter=(counter+1)%5
    order=list(range(5))
    for i in range(counter*3): order[0],order[i%5]=order[i%5],order[0]
    table=expected_table(); grid=c['grid']; occupied=c['occupied']; mode=c['mode']
    selected=None
    for group in range(0,4225,5):
        for k in order:
            dx,dy,radius,_=struct.unpack_from('<bbHH',table,(group+k)*6)
            if radius>c['view']: continue
            x,y=c['seed'][0]+dx,c['seed'][1]+dy
            if not (0<=y<len(grid) and 0<=x<len(grid[0])): continue
            allowed=mode==4 or (TERRAIN[int(grid[y][x])][mode]!=0 and [x,y] not in occupied)
            if allowed and [x,y] not in reservations:
                selected=[x,y];break
        if selected is not None:break
    if selected is not None:
        if len(reservations)>=40:raise ValueError('original reservation capacity assertion')
        reservations.append(selected)
    return counter,selected


def selection_corpus():
    rows=[]
    def add(name,**kw):
        c=dict(name=name,grid=['0000000']*7,occupied=[],mode=0,seed=[3,3],view=31,counter=0,reservations=[],calls=1,reset=False)
        c.update(kw);rows.append(c);return c
    for n in range(5):add('rotation_'+str(n),counter=n)
    for v in (0,1,2,32):add('view_'+str(v),view=v)
    add('corner',seed=[0,0]);add('outside_seed',seed=[-1,0])
    add('all_blocked',grid=['1111111']*7)
    add('all_occupied',occupied=[[x,y] for y in range(7) for x in range(7)])
    add('mode4_bypasses_both',mode=4,grid=['1111111']*7,occupied=[[x,y] for y in range(7) for x in range(7)])
    for mode in (1,2,3):add('terrain_mode_'+str(mode),mode=mode,grid=['1212121']*7)
    add('reserve_40',calls=40)
    add('reservation_reset',reservations=[[2,3],[3,2],[4,3],[3,4]],reset=True,calls=3)
    add('view0_reserved',view=0,reservations=[[3,3]])
    add('partial_occupied',occupied=[[2,3],[3,2],[4,3]])
    return rows


def movement_corpus():
    rows=[]
    for name,start,goal,occupied in (
        ('east',[1,3],[5,3],[[2,3],[5,3]]),
        ('diagonal',[1,1],[5,5],[[2,2],[5,5]]),
        ('west',[5,3],[1,3],[[4,3],[1,3]]),
        ('north',[3,5],[3,1],[[3,4],[3,1]])):
        movement=dict(name=name,path=dict(name=name,kind='search',direction=0,grid=['0000000']*7,start=start,goal=goal,mode=0,avoid=False,occupied=occupied),
                      speed=999,terrain_rate=100,status=0,frames=160,blocker_speed=0)
        rows.append(dict(movement=movement,initial_phase=4,retry=0,cooldown=0,movement_type=0,unit_kind=0,ai_mode=0,faction=0))
    delayed=deepcopy(rows[0]);delayed['faction']=4;delayed['movement']['name']='east_faction4_cooldown';rows.append(delayed)
    return rows


class RerouteModel(RouteModel):
    def __init__(self,c,contract):
        super().__init__(c,contract);self.counter=0;self.reservations=[];self.adjustments=[]
        x,y=c['movement']['path']['goal'];self.put(0x4CC,x*32+16,'h');self.put(0x4CE,y*16+8,'h')

    def step(self):
        super().step()
        if 'nearest_free' in self.last_events and self.route.get('faction',0)>=4:self.put(0x4E0,30,'h')

    def next_tile(self):
        # Reuse the independently modeled raster step, with a local view of the
        # occupancy list so its previous scope guard does not supply a result.
        occupied=self.c['path']['occupied'];self.c=deepcopy(self.c);self.c['path']['occupied']=[]
        try: result=super().next_tile()
        finally:self.c['path']['occupied']=occupied
        if result==0 and self.occupied(self.grid(0x4DC)) and self.occupied(self.grid(0x4D0)):
            self.last_events.append('nearest_free')
            p=self.c['path'];query=dict(grid=p['grid'],occupied=p['occupied'],mode=0,seed=list(self.grid(0x4CC)),view=31)
            self.reservations=[]
            self.counter,point=select(query,self.counter,self.reservations)
            self.adjustments.append(point)
            if point is not None:
                self.put(0x4D0,point[0]*32+16,'h');self.put(0x4D2,point[1]*16+8,'h')
            return 2
        return result
