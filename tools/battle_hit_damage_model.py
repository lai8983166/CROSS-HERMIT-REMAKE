"""Byte-level independent oracle for source hit, EFCT and HP queue lifecycle."""
import struct
from tools import battle_attack_animation as animation
from tools.battle_hit_damage import animation_input,effect_resource,physical,Random,signed,div
from tools.battle_region_routing import inputs as map_inputs

CTRL,UNIT,ANIM=animation.CTRL,animation.UNIT,animation.ANIM
TARGET,RECORD=UNIT+0x520,0x11200000
FXDATA,FXOBJ,TLS,TANIM=0x12600000,0x12620000,0x12621000,0x12622000
DAMAGE,POPUP=CTRL+0x2B6F0,CTRL+0x2C6F0


class Model(animation.Model):
    def __init__(self,c):
        super().__init__(animation_input(c));self.combat=c;self.melee=self.data;self.fx=effect_resource();self.rng=Random(c['seed']);self.crt_seed=c['crt_seed'];self.crt_draws=0
        self.target_resource=ANIM if self.source[0x218090+10+c['job']*40]==self.source[0x218090+11+c['job']*40] else TANIM
        self.damage_pool=bytearray(512*8);self.popups=bytearray(512*16);self.records=[bytearray(256),bytearray(256)]
        fields=[[(2,10,'H'),(0xC,c['job'],'H'),(0xF,1,'B'),(0x14,100,'h'),(0x16,100,'h'),(0x1A,50,'h'),(0x1C,20,'h'),
                 (0x2C,5,'b'),(0x2E,999,'H'),(0x32,3,'h'),(0x34,5,'h'),(0x37,5,'B'),(0x38,c['accuracy'],'H'),(0x3A,c['power'],'H'),(0x3C,c['spread'],'H')],
                [(2,11,'H'),(0xC,c['job'],'H'),(0xF,1,'B'),(0x14,c['max_hp'],'h'),(0x16,c['hp'],'h'),(0x24,100,'i'),(0x3A,100,'H'),
                 (0x4C,c['evasion'],'B'),(0x4D,c['armor'],'B'),(0x52,c['mental'],'H'),(0x54,c['threshold'],'H'),(0xA4,4,'B')]]
        for r,items in zip(self.records,fields):
            for o,v,f in items:struct.pack_into('<'+f,r,o,v)
        self.memput(TARGET+6,int(c['target_attacking']),'B');self.memput(TARGET+0x28A,6,'B');self.hit=None;self.effect_id=None
        self.unit[0x2F4:0x4CC]=bytes(472)

    def area(self,a,n):
        if not hasattr(self,'melee'):return super().area(a,n)
        for base,b in ((UNIT,self.unit),(TARGET,self.target),(animation.POOL,self.children),(animation.EVENTS,self.event_data),(animation.EVENT_CTRL,self.event_ctrl),
                       (animation.DATA,self.melee['raw']),(FXDATA,self.fx['raw']),(RECORD,self.records[0]),(RECORD+0x100,self.records[1]),(DAMAGE,self.damage_pool),(POPUP,self.popups)):
            if base<=a and a+n<=base+len(b):return b,a-base
        raise ValueError('independent damage address '+hex(a))

    def init_work(self,a):
        super().init_work(a)
        if TARGET<=a<TARGET+0x520:self.memput(a+0x1C,self.target_resource)

    def for_resource(self,a):return self.fx if self.memget(a+0x1C)==FXOBJ else self.melee

    def start(self,a,block,index):
        r=self.for_resource(a);base=FXDATA if r is self.fx else animation.DATA;o=r['offsets'][block];rel=struct.unpack_from('<I',r['raw'],o+8+index*4)[0]
        self.memput(a+4,base+o+rel);self.enter(a)

    def enter(self,a):
        old=self.data;self.data=self.for_resource(a)
        try:super().enter(a)
        finally:self.data=old

    def action_for(self,unit,action):
        a=unit+0x48;typ=self.combat['job']+8;direction=self.memget(unit+0x28A,'B')
        table=struct.unpack_from('<I',self.source,0x20E850+typ*4)[0]-0x400000;programs=struct.unpack_from('<I',self.source,0x20F070+typ*4)[0]-0x400000
        off=self.source[0x210510+direction];index,flags=self.source[table+(action*8+off)*2:table+(action*8+off)*2+2];encoded=struct.unpack_from('<H',self.source,programs+index*2)[0]
        self.memput(a+0xC,action,'h')
        for k,v,f in ((3,flags&3,'B'),(8,0,'B'),(0x18,7,'I'),(0x12,0,'h'),(0x14,0,'h'),(0x24,a,'I'),(0xB,0,'B'),(0x10,0,'h')):self.memput(a+k,v,f)
        self.start(a,encoded>>8,encoded&255);self.memput(unit+4,0,'B');self.memput(unit+0xA,0,'h')

    def action(self,action):self.action_for(UNIT,action)

    def bind_target(self):
        self.memput(TARGET+0x44,self.target_resource);self.init_work(TARGET+0x48);self.memput(TARGET+0x74,animation.EVENT_CTRL);self.action_for(TARGET,1)
        for i in range(5):self.init_work(TARGET+0xA0+i*88)
        self.memput(TARGET+0xCC,animation.EVENT_CTRL);self.events.append(dict(entry=0x46BCC0,args=[TARGET,1]))

    def snapshot_combat(self,which):
        r=self.records[which];b=bytearray(44)
        for dst,src,n in ((0,0x3A,2),(2,0x3C,2),(4,0x38,2),(8,0x4C,1),(9,0x4D,1),(10,0x50,1),(11,0x4F,1),(12,0x4E,1),(0x24,0x52,2)):b[dst:dst+n]=r[src:src+n]
        unit=UNIT if which==0 else TARGET;x=(self.memget(unit+0x2EC,'i')>>16)//32;y=(self.memget(unit+0x2F0,'i')>>16)//16
        data=map_inputs();t=data['logical'][16+(y*64+x)*6];coefs=struct.unpack_from('<3i',data['terrain'],t*76+16)
        struct.pack_into('<3i',b,0x10,*coefs);return b

    def crt(self):
        self.crt_seed=(self.crt_seed*0x343FD+0x269EC3)&0xFFFFFFFF;self.crt_draws+=1;return (self.crt_seed>>16)&32767

    def popup(self,unit,kind,number=0):
        i=next(i for i in range(512) if not (self.popups[i*16]&128));a=POPUP+i*16
        self.popups[i*16:i*16+16]=bytes(16);self.memput(a,128,'B');self.memput(a+1,kind,'B');self.memput(a+4,0 if unit==UNIT else 1,'H')
        self.memput(a+8,abs(number)&65535,'H');desc=struct.unpack_from('<I',self.source,0x219668+kind*4)[0];self.memput(a+0xC,desc)
        self.memput(a+6,struct.unpack_from('<h',self.source,desc-0x400000+6)[0],'h');self.memput(a+0xA,0,'B')
        if kind in (0,1,2,3,4,5,9,10,11,12,13,14):x=self.crt()%24-12;y=-44-(self.crt()&7)
        else:x=(self.crt()&15)-8;y=(self.crt()&7)-44
        self.memput(a+2,x,'b');self.memput(a+3,y,'b')

    def effect(self,global_id,packet):
        a=TARGET+0xA0;root=self.memget(a+0x24);b,o=self.area(a+0x48,12);b[o:o+12]=packet
        at=next(animation.POOL+i*88 for i in range(2048) if not self.children[i*88]);self.init_work(at)
        p=0x20F890+(global_id//1000-1)*800+(global_id%1000)*4;flags,block,index=self.source[p:p+3]
        mirror=(flags&128) if flags&128 else self.memget(a+3,'B')
        for off,v,f in ((3,mirror|64,'B'),(0x24,root,'I'),(0x1C,FXOBJ,'I'),(2,1,'B'),(0x20,self.memget(root+0x20),'I'),
                        (0x12,self.memget(a+0x12,'h'),'h'),(0x14,self.memget(a+0x14,'h'),'h'),(8,self.memget(a+8,'B')+1,'B'),(0x18,7,'I')):self.memput(at+off,v,f)
        self.memput(root+0x20,at)
        if self.memget(a+0x2C):self.memput(at+0x2C,self.memget(a+0x2C));self.copy(at+0x48,a+0x48,12)
        self.start(at,block,index);self.update(at)

    def resolve(self):
        attack,defense=self.snapshot_combat(0),self.snapshot_combat(1);ev,armor=struct.unpack_from('<2i',defense,0x10)
        hit=physical(self.combat,ev,armor,self.rng);struct.pack_into('<i',attack,0x28,hit['damage'])
        self.hit=dict(kind=hit['kind'],attack=attack.hex(),defense=defense.hex(),seed=self.rng.seed,draws=self.rng.count)
        self.result=1 if hit['kind'] and self.combat['target_attacking'] else hit['kind'];self.delta=signed(-hit['damage'],16)
        if self.result==0:self.popup(UNIT,19)
        else:
            packet=bytearray(12);struct.pack_into('<IhB',packet,0,1<<24,animation.basic(self.combat['job']),self.result);struct.pack_into('<h',packet,10,self.delta)
            offset={1:2,2:2,3:4,4:0}[self.result];g=struct.unpack_from('<h',self.source,0x213B78+animation.basic(self.combat['job'])*6+offset)[0]
            if g in (2001,2007,2012,2018,2023,2029,2052,2057):g+=self.rng.next()%5
            self.effect_id=g;self.effect(g,packet)
        # Actual outer attack consumer now reclaims its original flag4 node.
        node=self.memget(UNIT+0x48+0x34);self.return_event(node)

    def damage_event(self):
        node=self.memget(TARGET+0xA0+0x40)
        if not node:return
        struct.pack_into('<H',self.records[1],0xA6,0)
        if self.result!=4 or self.delta>0:
            self.damage_pool[:8]=bytes(8);self.memput(DAMAGE,128,'B');self.memput(DAMAGE+2,self.delta,'h');self.memput(TARGET+0x510,DAMAGE)
            self.popup(TARGET,11 if self.delta>0 else 9,self.delta)
        if self.result in (2,3) and not self.combat['target_attacking']:
            self.target[0x29B:0x2A6]=self.target[0x290:0x29B];self.memput(TARGET+0x2A6,1,'B')
            self.memput(TARGET+0x292,8 if self.result==2 else 9,'B');self.memput(TARGET+0x4F8,0,'h')
            if self.result==3:self.memput(TARGET+0x4F6,1,'B')
        if self.result==4:self.popup(TARGET,18)
        self.memput(TARGET+0x4FA,0,'h');self.return_event(node)

    def apply_hp(self):
        if not self.memget(TARGET+0x510):return
        c=self.combat;hp=min(32767,c['hp']+self.delta)
        if c['threshold'] and hp<1 and self.delta<0 and c['hp']>=c['threshold'] and -self.delta>=c['threshold']:hp=1
        hp=0 if hp<0 else min(c['max_hp'],hp);struct.pack_into('<h',self.records[1],0x16,hp)
        self.damage_pool[:8]=bytes(8);self.memput(TARGET+0x510,0)

    def effect_tick(self):
        a=TARGET+0xA0;p=self.memget(a+0x20)
        while p:self.memput(p+1,0,'B');p=self.memget(p+0x20)
        result=1 if not self.memget(a+4) else int(bool(self.update(a)))
        while True:
            p=self.memget(a+0x20);restart=False
            while p:
                if not self.memget(p+1,'B') and self.update(p):restart=True;break
                p=self.memget(p+0x20)
            if not restart:break
        return result

    def state(self):
        s=super().state();struct.pack_into('<h',self.records[0],0x1C,self.mp)
        s.update(record=self.records[0].hex(),target_record=self.records[1].hex(),damage_pool=self.damage_pool.hex(),popup_pool=self.popups.hex(),
                 battle_seed=self.rng.seed,battle_draws=self.rng.count,CRT_seed=self.crt_seed,platform_error=0x1234)
        return s
