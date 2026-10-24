"""Independent attack admission, chase, preparation and launch model."""
import struct
from tools import battle_target_acquisition as target
from tools.battle_pathfinding_emulation import SOURCE,need


def case(name,**kw):
    r=dict(name=name,cell=[30,0],alive=1,state=2,skill=101,mp=20,max_mp=50,windup=3,recovery=5,range=1,status=0,
           pending=False,selection=False,actor_id=10,calls=256)
    r.update(kw);return r


def corpus():
    return [case('ordinary'),case('natural_selection_to_release',selection=True),case('consume_attack_request',pending=True),case('zero_windup',windup=0),
            case('one_windup',windup=1),case('negative_windup',windup=-1),case('slow_status7',status=7),
            case('slow_zero',status=7,windup=0),case('windup_short_wrap',status=7,windup=32767,calls=12),
            case('recovery_short_wrap',status=7,recovery=32767),case('chase_east',cell=[34,0]),
            case('chase_south',cell=[29,5]),case('same_cell',cell=[29,0]),case('range_zero',range=0),
            case('wide_range',cell=[34,0],range=5),case('dead_target',alive=0),case('unselectable_target',state=12),
            case('mp_fallback',skill=2,mp=0),case('both_unaffordable',skill=2,mp=-1),
            case('mp_clamp_max',mp=100,max_mp=50),case('excluded_actor',actor_id=170),case('target_state1',state=1),
            case('face_west',cell=[28,0]),case('face_diagonal',cell=[30,1],range=5)]


def validate(c):
    need(set(c)==set(case('x')),'exact attack input fields')
    need(type(c['name']) is str and bool(c['name']),'attack name')
    for k,lo,hi in [('alive',0,1),('state',0,29),('skill',1,101),('mp',-32768,32767),('max_mp',0,32767),
                    ('windup',-32768,32767),('recovery',-32768,32767),('range',0,32),('status',0,7),('actor_id',10,170),('calls',1,512)]:
        need(type(c[k]) is int and lo<=c[k]<=hi,'attack '+k)
    need(c['skill'] in (2,101) and c['status'] in (0,7) and c['actor_id'] in (10,170),'supported declared attack families')
    need(type(c['pending']) is bool and type(c['selection']) is bool and not (c['pending'] and c['selection']) and type(c['cell']) is list and len(c['cell'])==2 and all(type(x) is int for x in c['cell']) and 0<=c['cell'][0]<64 and 0<=c['cell'][1]<96,'attack target cell/pending')


def charge_corpus():
    return [case(name,skill=2,mp=mp,max_mp=maximum) for name,mp,maximum in
            [('paid_sufficient',100,200),('paid_exact',45,200),('paid_short',44,200),
             ('paid_negative',-1,200),('paid_cap',32767,100),('paid_zero_capacity',100,0)]]


def target_input(c):
    return target.case(c['name'],kind='command',candidates=[target.candidate(1,cell=c['cell'],alive=c['alive'],state=c['state'])])


def skill_cost(s):return struct.unpack_from('<h',SOURCE.read_bytes(),0x2C2DC8+s*72+8)[0]


def short(v):return (v+32768)%65536-32768


class Model(target.Model):
    def __init__(self,c):
        validate(c);super().__init__(target_input(c));self.attack=c
        for off,v,fmt in ((0x290,4 if c['pending'] else 6,'B'),(0x292,6 if c['pending'] else 0,'B'),
                          (0x4EE,1,'h'),(0x4F2,c['skill'],'h'),(0x4F0,c['cell'][0],'B'),(0x4F1,c['cell'][1],'B'),(0x14,c['status'],'B')):self.put(off,v,fmt)
        self.mp=c['mp'];self.launches=0;self.events=[]
        if c['selection']:
            self.put(0x290,4,'B');self.put(0x4EE,-1,'h');self.put(0x4F2,-1,'h')

    def cancel(self):
        # In this corpus no unfinished search owns FINE+60 at cancellation;
        # original 437D90's ownership gate leaves both route packets intact.
        pass

    def range_ok(self):
        mask=target.inputs()['masks'][self.attack['range']];x,y=self.cell();tx,ty=self.attack['cell'];dx,dy=abs(tx-x),abs(ty-y)
        rx,ry=(mask['width']-1)//2,(mask['height']-1)//2
        return dx<=rx and dy<=ry and bytes.fromhex(mask['hex'])[(dy+ry)*mask['width']+dx+rx]!=0

    def release(self):
        self.put(6,1,'B');self.put(0xC,0,'h');self.put(0x293,22,'B')
        self.put(0x90,1<<24);self.put(0x94,self.get(0x4F2,'h'));self.put(0x98,0)
        self.events += [dict(entry=0x46BCC0,args=[0x11080AEC,5]),dict(entry=0x46C990,args=[0x11080AEC,self.get(0x4F2,'h')])]
        self.put(4,0,'B');self.put(0xA,0,'h');self.mp=max(0,min(self.attack['max_mp'],min(32767,self.mp-skill_cost(self.get(0x4F2,'h')))))
        self.put(0x10,self.get(0x12,'h'),'h');self.launches+=1

    def command(self):
        c=self.attack
        if self.get(0x292,'B'):self.consume()
        if self.get(0x290,'B')==4:
            target.Model.command(self);return
        phase=self.get(0x293,'B');s=self.get(0x4F2,'h')
        if c['actor_id']==170:
            self.put(0x4EE,-1,'h');self.put(0x4F2,-1,'h');self.put(0x292,15,'B');return
        if phase and phase<20 and (not c['alive'] or c['state'] in (1,12,13,25)):
            self.cancel();self.put(0x292,2,'B');return
        if 9<phase<20 and self.range_ok():
            self.cancel();self.put(0x293,20,'B');return
        if phase==0:
            if self.mp<skill_cost(s):
                if self.mp>=skill_cost(101):self.put(0x4F2,101,'h');return
                self.put(0x4EE,-1,'h');self.put(0x4F2,-1,'h');self.put(0x292,15,'B');return
            if not c['alive'] or c['state'] in (12,13):
                self.put(0x4EE,-1,'h');self.put(0x4F2,-1,'h');self.put(0x292,15,'B');return
            tx,ty=c['cell']
            for off,val in ((0x4CC,tx*32+16),(0x4CE,ty*16+8),(0x4D0,tx*32+16),(0x4D2,ty*16+8)):self.put(off,val,'h')
            self.put(0x293,10,'B')
        elif phase==10:
            self.put(0x294,0,'B');self.put(0x4E0,0,'h');self.put(0x293,11,'B')
        elif phase==11:self.put(0x293,12,'B')
        elif phase==12:
            # RegionModel implements the accepted original movement rules on
            # the same map; attack's nested phase is +294, not +293.
            self.put(0x293,self.get(0x294,'B'),'B');super(target.Model,self).step()
            self.put(0x294,self.get(0x293,'B'),'B');self.put(0x293,12,'B')
        elif phase==20:
            self.put(7,1,'B');wind=c['windup'];rec=c['recovery']
            if c['status']==7:wind=short(int(wind*150/100));rec=short(int(rec*150/100))
            self.put(0xE,wind,'h');self.put(0x12,rec,'h');self.put(0x293,21,'B')
            self.events.append(dict(entry=0x46C120,args=[0x11080AEC,self.get(0x4D0,'h'),self.get(0x4D2,'h')]))
            # atan2 direction uses the original 16-entry lookup; angles are
            # independently computed from integer pixel positions.
            import math
            dx=self.get(0x4D0,'h')-(self.get(0x2EC,'i')>>16);dy=self.get(0x4D2,'h')-(self.get(0x2F0,'i')>>16)
            radians=math.atan2(dy,dx);degrees=radians/struct.unpack_from('<f',SOURCE.read_bytes(),0x192778)[0]
            degrees=struct.unpack('<f',struct.pack('<f',degrees))[0]
            if degrees<0:degrees+=360
            self.put(0x28A,SOURCE.read_bytes()[0x218768+(int(degrees)%360)//23],'B')
            if wind==0:self.release()
            else:
                self.events.append(dict(entry=0x46BCC0,args=[0x11080AEC,11]))
                self.put(4,0,'B');self.put(0xA,0,'h');self.put(0xC,wind,'h')
        elif phase==21:
            self.put(0xC,short(self.get(0xC,'h')-1),'h')
            if self.get(0xC,'h')<1:self.release()
        else:need(phase==22,'independent supported phase')
