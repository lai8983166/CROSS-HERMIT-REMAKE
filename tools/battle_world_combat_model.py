"""Independent whole-unit preparation, animation, hit, HP and aftermath order."""
import struct
from tools.battle_world_update_model import Model as WorldModel
from tools.battle_combat_aftermath_model import STATS
from tools.battle_world_update_emulation import CTRL,UNIT,TARGET,RECORD


class Model(WorldModel):
    def __init__(self,c):
        super().__init__(dict(name=c['name'],aftermath=c['aftermath'],frames=3,world_enabled=True))
        self.cycle=c;self.memput(TARGET+0x290,5,'B');self.hp_stores=[];self.hit_history=[]

    def bind_target(self):
        self.memput(TARGET+0x44,self.target_resource);self.init_work(TARGET+0x48);self.memput(TARGET+0x74,CTRL+0x2F164);self.action_for(TARGET,2)
        for i in range(5):self.init_work(TARGET+0xA0+i*88)
        self.memput(TARGET+0xCC,CTRL+0x2F164);self.events.append(dict(entry=0x46BCC0,args=[TARGET,2]))

    def pre(self):
        super().pre()
        self.build_list(0xDCCD8,[u for u,r in ((UNIT,self.records[0]),(TARGET,self.records[1])) if r[15] in (0,2,3,4,5)])

    def dispatch(self,u):
        command,phase=self.memget(u+0x290,'B'),self.memget(u+0x293,'B')
        if command==11:
            if phase==0:
                self.memput(u+6,0,'B');self.memput(u+7,0,'B');self.memput(u+0xA,0,'h');self.memput(u+0x293,1,'B')
            rec=self.records[0 if u==UNIT else 1]
            if rec[15]==3:rec[15]=4
            return 1
        if u==UNIT and command==6 and phase<22:self.command();return 0
        return super().dispatch(u)

    def resolve(self):
        super().resolve();self.hit_history.append(self.hit)

    def apply_current_hp(self):
        if not self.memget(TARGET+0x510):return
        c=self.combat;current=struct.unpack_from('<h',self.records[1],0x16)[0];hp=min(32767,current+self.delta)
        if c['threshold'] and hp<1 and self.delta<0 and current>=c['threshold'] and -self.delta>=c['threshold']:hp=1
        hp=max(0,min(c['max_hp'],hp));struct.pack_into('<h',self.records[1],0x16,hp);self.hp_stores.append(hp)
        self.damage_pool[:8]=bytes(8);self.memput(TARGET+0x510,0)

    def regenerate(self,u):
        n=len(self.target_regeneration_stores);super().regenerate(u);self.hp_stores.extend(self.target_regeneration_stores[n:])

    def unit_update(self,u):
        self.last_updated=u;self.memput(u+8,self.memget(u+8,'B')&127,'B');self.consume_pending(u)
        if self.dispatch(u):return 1
        self.memput(u+4,self.update_animation(u+0x48),'B');self.put_wrap(u+0xA,self.memget(u+0xA,'h')+1)
        for i in range(5):self.update_animation(u+0xA0+i*88)
        if u==UNIT and self.memget(UNIT+0x48+0x34):self.resolve()
        if u==TARGET:self.damage_event();self.apply_current_hp()
        self.regenerate(u);rec=self.records[0 if u==UNIT else 1]
        if struct.unpack_from('<h',rec,0x16)[0]<=0 and self.memget(u+0x290,'B')!=13:self.memput(u+0x292,13,'B')
        if rec[15]!=1:return 0
        faction=rec[0xA4];self.put_wrap(STATS+faction*4,self.memget(STATS+faction*4,'h')+1)
        kind=self.source[0x2B2D88+self.combat['job']*64+2];self.stats[faction*4+2]|=(1<<(kind-1)) if 1<=kind<=5 else 0
        self.mark_view(u);x,y=self.cell(u);oldx,oldy=self.memget(u+0x4E7,'B'),self.memget(u+0x4E8,'B')
        self.memput(u+0x4E9,oldx,'B');self.memput(u+0x4EA,oldy,'B');self.memput(u+0x4E7,x,'B');self.memput(u+0x4E8,y,'B')
        if (x,y)!=(oldx,oldy):
            for xx,yy,delta in ((oldx,oldy,-1),(x,y,1)):
                at=(yy*64+xx)*2+1;self.occupancy[at]=(self.occupancy[at]+delta)&255
            return 0x11700000|self.occupancy[(y*64+x)*2+1]
        return y
