"""Independent byte model for full basic combat unit follow-up updates."""
import math
import struct
from tools.battle_hit_damage_model import Model as HitModel,CTRL,UNIT,TARGET,RECORD,FXOBJ
from tools.battle_hit_damage import signed,div
from tools.battle_region_routing import inputs as map_inputs
from tools.battle_target_acquisition import inputs as target_inputs
from tools.battle_attack_animation import POOL

STATS=CTRL+0x2E714


def f32(v):return struct.unpack('<f',struct.pack('<f',v))[0]


class Model(HitModel):
    def __init__(self,c):
        super().__init__(c['combat']);self.aftermath=c;self.occupancy=bytearray(0x3000);self.stats=bytearray(0x830)
        self.visible=bytearray(0x2000);self.seen=bytearray(0x2000);self.last_updated=0;self.motion_scratch=self.source[0x218CF0:0x218CF8]
        self.target_regeneration_stores=[]
        for at,v,fmt in ((RECORD+0xAA,c['actor_kills'],'h'),(RECORD+0xAC,c['actor_points'],'h'),
                         (RECORD+0x1AE,c['target_deaths'],'b'),(RECORD+0x1A8,c['kill_points'],'h')):self.memput(at,v,fmt)
        struct.pack_into('<h',self.stats,0,c['region_count']);struct.pack_into('<h',self.stats,0x800,c['score'])
        for u in (UNIT,TARGET):
            x,y=self.cell(u)
            for off,v in ((0x4E7,x),(0x4E8,y),(0x4E9,x),(0x4EA,y)):self.memput(u+off,v,'B')
            self.occupancy[(y*64+x)*2+1]+=1

    def area(self,a,n):
        if hasattr(self,'stats') and STATS<=a and a+n<=STATS+len(self.stats):return self.stats,a-STATS
        return super().area(a,n)

    def cell(self,u=UNIT):return (div(self.memget(u+0x2EC,'i')>>16,32),div(self.memget(u+0x2F0,'i')>>16,16))

    def state(self):
        s=super().state();s.update(occupancy=self.occupancy.hex(),world_stats=self.stats.hex(),last_updated=self.last_updated,
                                 motion_scratch=self.motion_scratch.hex(),visible=self.visible.hex(),seen=self.seen.hex());return s

    def put_wrap(self,a,v,fmt='h'):
        bits=struct.calcsize('<'+fmt)*8;self.memput(a,signed(v,bits) if fmt in ('b','h','i') else v&((1<<bits)-1),fmt)

    def act(self,u,action):
        self.action_for(u,action);self.events.append(dict(entry=0x46BCC0,args=[u,action]))

    def face(self,u,other):
        x,y=(self.memget(other+o,'i')>>16 for o in (0x2EC,0x2F0));ox,oy=(self.memget(u+o,'i')>>16 for o in (0x2EC,0x2F0))
        degrees=f32(math.atan2(y-oy,x-ox)/struct.unpack_from('<f',self.source,0x192778)[0])
        if degrees<0:degrees+=360
        self.memput(u+0x28A,self.source[0x218768+(int(degrees)%360)//23],'B');self.events.append(dict(entry=0x46C120,args=[u,x,y]))

    def consume_pending(self,u):
        command=self.memget(u+0x292,'B')
        if command:
            self.memput(u+0x291,self.memget(u+0x290,'B'),'B');self.memput(u+0x290,command,'B')
            self.memput(u+0x292,0,'B');self.memput(u+0x293,0,'B')
            self.free_work(u+0xA0)

    def update_animation(self,a):
        p=self.memget(a+0x20)
        while p:self.memput(p+1,0,'B');p=self.memget(p+0x20)
        result=1 if not self.memget(a+4) else int(bool(self.update(a)))
        while True:
            p=self.memget(a+0x20);restart=False
            while p:
                if not self.memget(p+1,'B') and self.update(p):restart=True;break
                p=self.memget(p+0x20)
            if not restart:break
        return result

    def counter_max_add(self,a,amount,fmt):
        before=self.memget(a,fmt);after=signed(before+amount,8*struct.calcsize('<'+fmt))
        if after>before:self.memput(a,after,fmt)

    def death_effect(self,u):
        a=u+0x48;global_id=struct.unpack_from('<h',self.source,0x2149D0+self.combat['job']*10+4)[0]
        p=0x20F890+(global_id//1000-1)*800+(global_id%1000)*4;flags,block,index=self.source[p:p+3]
        at=next(POOL+i*88 for i in range(2048) if not self.children[i*88]);self.init_work(at);top=self.memget(a+0x24)
        mirror=(flags&128) if flags&128 else self.memget(a+3,'B')
        for off,v,fmt in ((3,mirror|64,'B'),(0x24,top,'I'),(0x1C,FXOBJ,'I'),(2,1,'B'),(0x20,self.memget(top+0x20),'I'),
                          (0x12,self.memget(a+0x12,'h'),'h'),(0x14,self.memget(a+0x14,'h'),'h'),(8,self.memget(a+8,'B')+1,'B'),(0x18,7,'I')):self.memput(at+off,v,fmt)
        self.memput(top+0x20,at)
        if self.memget(a+0x2C):self.memput(at+0x2C,self.memget(a+0x2C));self.copy(at+0x48,a+0x48,12)
        self.start(at,block,index);self.update(at)

    def remove(self,u):
        self.memput(u+0x291,0,'B');self.memput(u+0x290,11,'B');self.memput(u+0x292,0,'B');self.memput(u+0x293,0,'B')
        x,y=self.cell(u);self.occupancy[(y*64+x)*2+1]=(self.occupancy[(y*64+x)*2+1]-1)&255
        for off in (0x4E9,0x4EA,0x4E5,0x4E6):self.memput(u+off,255,'B')
        self.free_work(u+0x48)
        for i in range(5):self.free_work(u+0xA0+i*88)
        self.memput(u+0x4FE,600,'h')
        for off in (0x4F8,0x4FA,0x4FC):self.memput(u+off,-1,'h')
        for off in (0x14,0x24,0x34):
            b,o=self.area(u+off,16);b[o:o+16]=bytes(16)
        for off in (0x10,0x12,0xC,0xE,0x4E0):self.memput(u+off,0,'h')
        self.memput(u+0x4E4,0,'B');self.memput(u+0x4EE,-1,'h');self.memput(u+0x4F0,0,'B');self.memput(u+0x4F1,0,'B')
        self.memput(u+0x4F2,-1,'h');self.memput(u+0x4FC,0,'h');self.records[1][0xF]=3

    def reaction(self,u,command,phase):
        if phase==0:
            self.memput(u+7,1,'B');self.memput(u+6,1,'B');self.face(u,UNIT)
            action=8 if command==9 or self.rng.next()%2 else 9;self.act(u,action)
            for off,v in ((0xE,0),(0xA,0),(0x12,60 if command==8 else 90),(0xC,0),(0x10,60 if command==8 else 90)):self.memput(u+off,v,'h')
            self.memput(u+0x293,1,'B')
        elif phase==1:
            if command==9:self.knockback(u)
            self.put_wrap(u+0x10,self.memget(u+0x10,'h')-1)
            if self.memget(u+0xA,'h')>(45 if command==8 else 60):
                self.memput(u+6,0,'B');self.act(u,14);self.memput(u+0x293,2,'B')
        elif phase==2:
            self.put_wrap(u+0x10,self.memget(u+0x10,'h')-1)
            if self.memget(u+0x10,'h')<=0:self.act(u,2);self.memput(u+0x10,0,'h');self.memput(u+0x293,3,'B')
        elif phase==3:
            b,o=self.area(u,0x520);b[o+0x290:o+0x29B]=b[o+0x29B:o+0x2A6]
            self.memput(u+0x292,self.memget(u+0x290,'B'),'B');self.memput(u+0x2A6,0,'B');self.memput(u+7,0,'B')

    def knockback(self,u):
        tick=self.memget(u+0xA,'h')
        if tick>=32 or self.memget(u+0x4F6,'b')==-1:return
        dx=(self.memget(u+0x2EC,'i')-self.memget(UNIT+0x2EC,'i'))>>16;dy=(self.memget(u+0x2F0,'i')-self.memget(UNIT+0x2F0,'i'))>>16
        length=f32(math.sqrt(signed(dx*dx+dy*dy,32)));nx=f32(dx/length);ny=f32(dy/length)
        step=struct.unpack_from('<h',self.source,0x218CF8+tick*2)[0];sx=signed(step<<16,32);sy=signed(div(step,2)<<16,32)
        self.motion_scratch=struct.pack('<ii',sx,sy);mx=int(sx*nx);my=int(sy*ny)
        px=signed(self.memget(u+0x2EC,'i')+mx,32);py=signed(self.memget(u+0x2F0,'i')+my,32)
        x,y=div(px>>16,32),div(py>>16,16)
        if x<1 or y<1:return
        data=map_inputs();kind=data['logical'][16+(y*64+x)*6];passable=struct.unpack_from('<i',data['terrain'],kind*76+12)[0]
        if not passable:return
        old=self.cell(u);occupant=self.occupancy[(y*64+x)*2+1]
        if occupant==(1 if (x,y)==old else 0):self.memput(u+0x2EC,px,'i');self.memput(u+0x2F0,py,'i')

    def dispatch(self,u):
        command,phase=self.memget(u+0x290,'B'),self.memget(u+0x293,'B')
        if u==UNIT:
            if phase==22 and self.memget(u+4,'B'):
                self.memput(u+0x293,23,'B');self.memput(u+0x10,self.memget(u+0x12,'h'),'h');self.act(u,14);self.memput(u+6,0,'B')
                # Original voice event 106 tests its chance before the empty
                # device gate; that CRT draw is observable even without audio.
                if self.crt()%100>=80:self.crt()
            elif phase==23:
                self.put_wrap(u+0x10,self.memget(u+0x10,'h')-1)
                if self.memget(u+0x10,'h')<=0:
                    self.act(u,2);self.memput(u+0x10,0,'h');self.memput(u+7,0,'B');self.memput(u+0x293,24,'B')
        elif command in (8,9):self.reaction(u,command,phase)
        elif command==2:
            if phase==0:self.act(u,1);self.memput(u+0x293,2,'B')
        elif command==13:
            if phase==0:
                self.memput(u+6,1,'B');self.memput(u+7,1,'B');self.counter_max_add(RECORD+0x1AE,1,'b')
                self.counter_max_add(RECORD+0xAA,1,'h');self.counter_max_add(RECORD+0xAC,self.aftermath['kill_points'],'h')
                self.counter_max_add(STATS+0x800,self.aftermath['kill_points'],'h');self.stats[0x824]=(self.stats[0x824]+1)&255
                self.memput(u+0x293,1,'B');self.act(u,20);self.death_effect(u)
            elif phase==1 and self.memget(u+4,'B'):self.memput(u+0x293,2,'B');self.memput(u+0xA,0,'h')
            elif phase==2 and self.memget(u+0xA,'h')>70:
                self.memput(u+6,0,'B');self.memput(u+7,0,'B');self.remove(u);return 1
        return 0

    def regenerate(self,u):
        rec=self.records[0 if u==UNIT else 1]
        for off,cap,interval,counter in ((0x16,0x14,0x18,0x504),(0x1C,0x1A,0x1E,0x506)):
            hp=struct.unpack_from('<h',rec,off)[0];maximum=struct.unpack_from('<h',rec,cap)[0]
            if (hp==0 if off==0x16 else False) or hp>=maximum:self.memput(u+counter,0,'h');continue
            value=signed(self.memget(u+counter,'h')+1,16);self.memput(u+counter,value,'h');rate=struct.unpack_from('<h',rec,interval)[0]
            if value>=max(1 if rate<0 else 0,rate):
                self.memput(u+counter,0,'h');struct.pack_into('<h',rec,off,max(0,min(maximum,min(32767,hp+1))))
                if u==TARGET and off==0x16:self.target_regeneration_stores.append(struct.unpack_from('<H',rec,off)[0])
        if u==UNIT:self.mp=struct.unpack_from('<h',rec,0x1C)[0]

    def mark_view(self,u):
        if u!=UNIT:return
        x,y=self.cell(u);data=target_inputs();mask=data['masks'][5];raw=data['raw'];w,h=mask['width'],mask['height']
        # Original mask is unsigned and keeps the maximum existing visibility.
        for yy in range(h):
            for xx in range(w):
                tx=x-div(w-1,2)+xx;ty=y-div(h-1,2)+yy
                if 0<=tx<64 and 0<=ty<96:
                    v=raw[mask['offset']+yy*w+xx];at=ty*64+tx
                    self.visible[at]=max(self.visible[at],v);self.seen[at]=max(self.seen[at],self.visible[at])

    def unit_update(self,u):
        self.last_updated=u;self.memput(u+8,self.memget(u+8,'B')&127,'B');self.consume_pending(u)
        if self.dispatch(u):return 1
        self.memput(u+4,self.update_animation(u+0x48),'B');self.put_wrap(u+0xA,self.memget(u+0xA,'h')+1)
        for i in range(5):self.update_animation(u+0xA0+i*88)
        self.regenerate(u)
        rec=self.records[0 if u==UNIT else 1]
        if struct.unpack_from('<h',rec,0x16)[0]<=0 and self.memget(u+0x290,'B')!=13:self.memput(u+0x292,13,'B')
        faction=rec[0xA4];self.put_wrap(STATS+faction*4,self.memget(STATS+faction*4,'h')+1)
        kind=self.source[0x2B2D88+self.combat['job']*64+2];self.stats[faction*4+2]|=(1<<(kind-1)) if 1<=kind<=5 else 0
        self.mark_view(u)
        x,y=self.cell(u);oldx,oldy=self.memget(u+0x4E7,'B'),self.memget(u+0x4E8,'B')
        self.memput(u+0x4E9,oldx,'B');self.memput(u+0x4EA,oldy,'B');self.memput(u+0x4E7,x,'B');self.memput(u+0x4E8,y,'B')
        if (x,y)!=(oldx,oldy):
            for xx,yy,delta in ((oldx,oldy,-1),(x,y,1)):
                at=(yy*64+xx)*2+1;self.occupancy[at]=(self.occupancy[at]+delta)&255
            return 0x11700000|self.occupancy[(y*64+x)*2+1]
        return y
