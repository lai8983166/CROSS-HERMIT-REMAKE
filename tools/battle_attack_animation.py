"""Original melee animation inputs and independent runtime (no drawing)."""
from functools import lru_cache
import struct
from tools.battle_attack_launch import case as attack_case
from tools.battle_pathfinding_emulation import ROOT,SOURCE,need,sha
from tools.dxanim_lib import parse_dxanim,parse_program_blocks
from tools.battle_attack_launch import Model as AttackModel

CTRL,UNIT,ANIM=0x11000000,0x11080AEC,0x11300000
DATA,EVENTS,POOL,EVENT_CTRL=0x12300000,0x12400000,0x765728,CTRL+0x2F164

ASSETS={1:('B0A','2d58f3bf4e5566b1cf021dbffd3531826c0b6ae5b2955905316a35b16bd4f785'),
        2:('B1A','cc746d7e3e33ce4ee6292e1422d90fbfe92146885ab91443e5b93cc3c188e4dd'),
        3:('A0A','9d3157608c29b1d3b9a118ba7a3c3d2ac85e3e4be6db7c9b0424be093b7fdc71'),
        4:('A1A','4cc024015e95e0d2c08f083c53770c4c925ff7fab9b0b188b6da622bf7803b85')}
DIRECTIONS={'E':(1,0),'W':(-1,0),'S':(0,1),'N':(0,-1),'NE':(1,-1),'SE':(1,1),'SW':(-1,1),'NW':(-1,-1)}


@lru_cache(maxsize=4)
def resource(job):
    name,digest=ASSETS[job];p=ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/DXANIM'/(name+'.BIN');raw=p.read_bytes()
    need(sha(raw)==digest,'fixed original melee animation '+name);offs=parse_dxanim(raw)
    return dict(raw=raw[:offs[6]],offsets=offs,programs=parse_program_blocks(raw),identity=dict(path=p.relative_to(ROOT).as_posix(),bytes=len(raw),sha256=digest,metadata_bytes=offs[6]))


def case(name,**kw):
    c=dict(name=name,job=1,direction='E',windup=3,consume='boundary');c.update(kw);return c


def corpus():
    rows=[case('job'+str(j)+'_'+d,job=j,direction=d) for j in range(1,5) for d in DIRECTIONS]
    rows += [case('zero_prepare',windup=0),case('target_command12_at_consume',consume='target_inactive'),case('actor_command12_at_consume',consume='actor_inactive'),
             case('animation_end_only',consume='none'),case('cancel_with_live_child',consume='cancel')]
    rows += [case('job'+str(j)+'_first_event',job=j,consume='early_boundary') for j in range(1,5)]
    return rows


def validate(c):
    need(set(c)==set(case('x')),'exact animation input fields')
    need(type(c['name']) is str and c['name'] and type(c['job']) is int and c['job'] in ASSETS,'melee animation identity')
    need(c['direction'] in DIRECTIONS and type(c['windup']) is int and c['windup'] in (0,3),'direction/preparation')
    need(c['consume'] in ('boundary','early_boundary','target_inactive','actor_inactive','none','cancel'),'animation consumption mode')


def attack_input(c):
    dx,dy=DIRECTIONS[c['direction']]
    return attack_case(c['name'],cell=[29+dx,5+dy],range=5,windup=c['windup'])


def basic(job):return struct.unpack_from('<h',SOURCE.read_bytes(),0x2B2D88+job*64+24)[0]


class Model(AttackModel):
    def __init__(self,c):
        super().__init__(attack_input(c));self.animation=c;self.data=resource(c['job']);self.source=SOURCE.read_bytes()
        self.children=bytearray(2048*88);self.event_data=bytearray(0x2000);self.event_ctrl=bytearray(0x24)
        self.put(0x290,2,'B');self.put(0x28A,6,'B');self.put(0x2F0,88*65536);self.put(0x4F2,basic(c['job']),'h')
        self.memput(EVENT_CTRL+0x1C,EVENTS)
        for i in range(16):
            a=EVENTS+i*12;self.memput(a,EVENT_CTRL+0x18 if i==0 else a-12);self.memput(a+4,a+12 if i<15 else 0);self.memput(a+8,EVENTS+0x1000+i*12)
        self.target=bytearray(0x520);tx,ty=self.attack['cell']
        for off,v,fmt in ((0,1,'H'),(2,1,'H'),(0x258,0x11200100,'I'),(0x290,2,'B'),(0x2EC,(tx*32+16)*65536,'I'),(0x2F0,(ty*16+8)*65536,'I')):struct.pack_into('<'+fmt,self.target,off,v)

    def area(self,a,n):
        for base,b in ((UNIT,self.unit),(POOL,self.children),(EVENTS,self.event_data),(EVENT_CTRL,self.event_ctrl),(DATA,self.data['raw'])):
            if base<=a and a+n<=base+len(b):return b,a-base
        raise ValueError('independent animation address '+hex(a))

    def memget(self,a,fmt='I'):
        b,o=self.area(a,struct.calcsize('<'+fmt));return struct.unpack_from('<'+fmt,b,o)[0]

    def memput(self,a,v,fmt='I'):
        b,o=self.area(a,struct.calcsize('<'+fmt));struct.pack_into('<'+fmt,b,o,v&0xFFFFFFFF if fmt=='I' else v)

    def copy(self,a,b,n):
        dst,o=self.area(a,n);src,p=self.area(b,n);dst[o:o+n]=src[p:p+n]

    def init_work(self,a):
        b,o=self.area(a,88);b[o:o+88]=bytes(88)
        for off,v,fmt in ((0,1,'B'),(0xC,-1,'h'),(0x1C,ANIM,'I'),(0x24,a,'I'),(0x54,128,'B'),(0x55,128,'B'),(0x56,128,'B')):self.memput(a+off,v,fmt)

    def bind(self):
        self.put(0x44,ANIM)
        self.init_work(UNIT+0x48);self.memput(UNIT+0x74,EVENT_CTRL);self.action(1)
        self.events.append(dict(entry=0x46BCC0,args=[UNIT,1]))
        for i in range(5):self.init_work(UNIT+0xA0+i*88)
        self.memput(UNIT+0xCC,EVENT_CTRL);self.put(4,0,'B');self.put(0xA,0,'h')

    def action(self,action):
        a=UNIT+0x48;typ=self.animation['job']+8
        table=struct.unpack_from('<I',self.source,0x20E850+typ*4)[0]-0x400000
        programs=struct.unpack_from('<I',self.source,0x20F070+typ*4)[0]-0x400000
        off=self.source[0x210510+self.get(0x28A,'B')];index,flags=self.source[table+(action*8+off)*2:table+(action*8+off)*2+2]
        encoded=struct.unpack_from('<H',self.source,programs+index*2)[0]
        self.memput(a+0xC,action,'h')
        for k,v,f in ((3,flags&3,'B'),(8,0,'B'),(0x18,7,'I'),(0x12,0,'h'),(0x14,0,'h'),(0x24,a,'I'),(0xB,0,'B'),(0x10,0,'h')):self.memput(a+k,v,f)
        self.start(a,encoded>>8,encoded&255)
        self.put(4,0,'B');self.put(0xA,0,'h')

    def start(self,a,block,index):
        o=self.data['offsets'][block];rel=struct.unpack_from('<I',self.data['raw'],o+8+index*4)[0]
        self.memput(a+4,DATA+o+rel);self.enter(a)

    def link(self,head,node):
        old=self.memget(head+4)
        if old:self.memput(old,node)
        self.memput(node,head);self.memput(node+4,old);self.memput(head+4,node)

    def unlink(self,node):
        prev,nxt=self.memget(node),self.memget(node+4)
        if prev:self.memput(prev+4,nxt)
        if nxt:self.memput(nxt,prev)

    def queue(self,a,head):
        node=self.memget(EVENT_CTRL+0x1C);need(node!=0,'independent event capacity')
        self.memput(EVENT_CTRL+0x1C,self.memget(node+4));self.copy(self.memget(node+8),a+0x48,12);self.link(head,node)

    def enter(self,a):
        p=self.memget(a+4)
        if not p:return
        flags=self.memget(p,'B');op=flags&3
        if op==0:
            self.memput(a+0x28,p);self.memput(a+0xE,self.memget(p+8,'h'),'h');top=self.memget(a+0x24)
            for bit,flag,off in ((4,9,0x30),(8,10,0x3C)):
                if flags&bit:
                    self.memput(top+flag,1,'B')
                    if self.memget(a+0x2C):self.queue(a,top+off)
            if self.memget(a+3,'B')&0x40 or self.memget(a+8,'B')==0:
                desc=self.memget(p+2,'B')|((self.memget(p+6,'H')&15)<<8)
                if desc<4095:self.memput(a+0x18,self.data['raw'][self.data['offsets'][4]+desc*10+8])
        elif op==3 and self.memget(a+0x10,'h')==0:
            times=self.memget(p+1,'B');self.memput(a+0x10,times if times==127 else times+1,'h')

    def free_work(self,a):
        if self.memget(a+8,'B')==0:
            child=self.memget(a+0x20)
            while child:
                nxt=self.memget(child+0x20)
                if self.memget(child+2,'B')==0:self.free_work(child)
                child=nxt
        else:
            prev=self.memget(a+0x24)
            while self.memget(prev+0x20)!=a:prev=self.memget(prev+0x20)
            self.memput(prev+0x20,self.memget(a+0x20));self.memput(a,0,'B')

    def child(self,a,p):
        at=next((POOL+i*88 for i in range(2048) if self.children[i*88]==0),None)
        if at is None:return
        self.init_work(at);self.memput(at+3,self.memget(a+3,'B')&~0x40,'B')
        top=self.memget(a+0x24)
        for off in (0x1C,0x24):self.memput(at+off,self.memget(a+off))
        self.memput(at+2,self.memget(a+2,'B'),'B');self.memput(at+0x20,self.memget(top+0x20));self.memput(top+0x20,at)
        for off,arg,bit in ((0x12,4,1),(0x14,6,2)):
            v=self.memget(a+off,'h')+self.memget(p+arg,'h')*(-1 if self.memget(at+3,'B')&bit else 1)
            self.memput(at+off,(v+32768)%65536-32768,'h')
        self.memput(at+8,self.memget(a+8,'B')+1,'B');self.memput(at+0x18,self.memget(p+1,'b')&0xFFFFFFFF)
        if self.memget(a+0x2C):self.memput(at+0x2C,self.memget(a+0x2C));self.copy(at+0x48,a+0x48,12)
        self.start(at,3,self.memget(p+2,'h'));self.update(at)

    def update(self,a):
        self.memput(a+1,1,'B')
        if self.memget(a+0xB,'B'):
            self.memput(a+4,0);self.free_work(a);return 1
        for _ in range(1000):
            p=self.memget(a+4)
            if not p:return 0
            flags=self.memget(p,'B');op=flags&3
            if op==0:
                self.memput(a+0x28,p);n=self.memget(a+0xE,'h')-1;self.memput(a+0xE,n,'h')
                if n>0:return 0
            elif op==1:
                if self.memget(a+8,'B')<8 and self.memget(p+2,'h')!=-1:self.child(a,p)
            elif op==2:pass # Actual source closed sound-device gate is executed.
            elif op==3:
                n=self.memget(a+0x10,'h')
                if n not in (0,1):
                    if n!=127:self.memput(a+0x10,n-1,'h')
                    jump=self.memget(p+2,'h')*10*(1 if flags&64 else -1);self.memput(a+4,p+jump);self.enter(a);continue
                self.memput(a+0x10,0,'h')
            if flags&128:self.memput(a+0xB,1,'B');return 1
            self.memput(a+4,p+10);self.enter(a)
            if op==0 and (self.memget(p+10,'B')&3)==0:return 0
        raise ValueError('independent finite animation budget')

    def tick(self):
        a=UNIT+0x48;p=self.memget(a+0x20)
        while p:self.memput(p+1,0,'B');p=self.memget(p+0x20)
        result=1 if not self.memget(a+4) else int(bool(self.update(a)))
        while True:
            p=self.memget(a+0x20);restart=False
            while p:
                if not self.memget(p+1,'B') and self.update(p):restart=True;break
                p=self.memget(p+0x20)
            if not restart:break
        return result

    def release(self):
        super().release();self.action(5)

    def command(self):
        phase=self.get(0x293,'B');super().command()
        if phase==20 and self.get(0xE,'h')!=0:self.action(11)

    def return_event(self,node):
        self.unlink(node);self.link(EVENT_CTRL+0x18,node)

    def invalidate(self):
        if self.animation['consume']=='target_inactive':
            self.target[0x291]=self.target[0x290];self.target[0x290]=12;self.target[0x292:0x294]=bytes(2)
        else:
            self.put(0x292,12,'B');self.consume()

    def consume_events(self):
        p=self.memget(UNIT+0x48+0x34)
        while p:nxt=self.memget(p+4);self.return_event(p);p=nxt

    def cleanup(self):
        self.free_work(UNIT+0x48)
        for off in (0x30,0x3C):
            while self.memget(UNIT+0x48+off+4):self.return_event(self.memget(UNIT+0x48+off+4))

    def state(self):
        return dict(unit=self.unit.hex(),children=self.children[:8*88].hex(),children_sha256=sha(self.children),events=self.event_data.hex(),event_controller=self.event_ctrl.hex(),target=self.target.hex())
