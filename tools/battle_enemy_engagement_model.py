"""Independent enemy decisions and repeated attacks with actual faction roles."""
import struct
from tools.battle_world_combat_model import Model as CombatModel
from tools.battle_world_combat_emulation import CTRL,UNIT,TARGET,RECORD
from tools.battle_enemy_engagement import declarations
from tools.battle_target_acquisition import choose,candidate,case,inputs
from tools.battle_attack_animation import basic
from tools.battle_hit_damage import signed,div


class Model(CombatModel):
    def __init__(self,c):
        super().__init__(dict(name=c['name'],aftermath=c['aftermath'],budget=192));self.cycle=c;self.attack['state']=5
        self.expected_ai=[]
        for at,v,fmt in declarations(c):
            # The relation matrix is immutable declared world input, checked
            # in initial/final owned memory; it is never a runtime model write.
            if at!=CTRL+0x115AAC+4*16:self.memput(at,v,fmt)

    def build_list(self,a,units):
        if a in (0xDD0C4,0xDD4B0,0xDD89C):
            units=[UNIT] if a==0xDD0C4 and self.records[0][15]==1 else [TARGET] if a!=0xDD0C4 and self.records[1][15]==1 else []
        return super().build_list(a,units)

    def mark_view(self,u):
        if u!=TARGET:return
        physical=self.visible
        if self.current!=0x12740000:self.visible=self.other
        try:
            x,y=self.cell(u);data=inputs();mask=data['masks'][self.records[1][0x2C]];raw=data['raw'];w,h=mask['width'],mask['height']
            for yy in range(h):
                for xx in range(w):
                    tx=x-div(w-1,2)+xx;ty=y-div(h-1,2)+yy
                    if 0<=tx<64 and 0<=ty<96:
                        v=raw[mask['offset']+yy*w+xx];at=ty*64+tx
                        self.visible[at]=max(self.visible[at],v);self.seen[at]=max(self.seen[at],self.visible[at])
        finally:
            if self.current!=0x12740000:self.other=self.visible;self.visible=physical

    def popup(self,unit,kind,number=0):
        # Original 493090 uses player-relative popup kind 0 rather than 9.
        return super().popup(unit,0 if unit==TARGET and kind==9 else kind,number)

    def damage_event(self):
        node=self.memget(TARGET+0xA0+0x40);super().damage_event()
        # Normal damage on player character 11 reaches voice event149 after
        # creating the popup. Chance precedes the declared empty audio gate.
        if node and self.delta<=0 and self.crt()%100>=70:self.crt()

    def observe(self,entry,caller,args):
        self.expected_ai.append(dict(entry=entry,receiver=CTRL,caller=caller,args=args))

    def request(self,command,caller):
        self.observe(0x475270,caller,[UNIT,command]);self.memput(UNIT+0x292,command,'B')

    def consume_pending(self,u):
        # 475700 unconditionally invokes the request consumer, even with no
        # pending request. Its early exit is original game code.
        self.observe(0x4751F0,0x475734,[u]);super().consume_pending(u)

    def dispatch(self,u):
        command,phase=self.memget(u+0x290,'B'),self.memget(u+0x293,'B')
        if u==TARGET:return 0
        if command==2:
            self.observe(0x476250,0x475A42,[u])
            if phase==0:self.act(u,1);self.memput(u+0x293,2,'B');self.memput(u+0xA,0,'h')
            elif phase==2:
                threshold=30+20*(self.rng.next()%10)
                if self.memget(u+0xA,'h')>threshold:self.request(15,0x4763AA);self.memput(u+0x293,3,'B')
        elif command==15:
            self.observe(0x476470,0x475A7E,[u]);self.memput(u+0x2A7,1,'B');self.request(19,0x47654C)
        elif command==19:
            self.observe(0x4776A0,0x475B82,[u])
            if phase==0:self.act(u,1);self.memput(u+0x293,1,'B')
            elif phase==1 and self.memget(u+0xA,'h')>=180:self.act(u,24);self.memput(u+0x293,2,'B')
            if self.memget(u+0x293,'B'):
                self.observe(0x47A920,0x477886,[u]);counter=signed(self.get(0x2D4,'i')+1);self.put(0x2D4,counter,'i')
                if counter>=self.get(0x2B8,'i'):
                    self.put(0x2D4,0,'i');relations=[0]*16;relations[0]=self.cycle['relation']
                    rec=self.records[1];p=candidate(1,cell=list(self.cell(TARGET)),faction=0,state=self.memget(TARGET+0x290,'B'),record_id=11,alive=rec[15],hp=struct.unpack_from('<h',rec,0x16)[0],max_hp=1000)
                    selected=choose(case('world',scope=self.cycle['scope'],policy=9,candidates=[p],actor_faction=4,relations=relations),self.cell())
                    if selected:
                        self.observe(0x47C580,0x4778D0,[u,TARGET])
                        self.put(0x4EE,1,'h');self.put(0x4F2,basic(self.combat['job']),'h');x,y=self.cell(TARGET);self.put(0x4F0,x,'B');self.put(0x4F1,y,'B');self.request(6,0x4778E2)
        elif command==6:
            self.observe(0x477980,0x475ABA,[u])
            if phase==24:
                self.put(0x4EE,-1,'h');self.put(0x4F2,-1,'h');self.request(15,0x4786C5)
            elif phase==22 and self.memget(u+4,'B'):
                self.memput(u+0x293,23,'B');self.memput(u+0x10,self.memget(u+0x12,'h'),'h');self.act(u,14);self.memput(u+6,0,'B')
                # Enemy faction fails the original player voice predicate.
            else:return super().dispatch(u)
        else:raise ValueError('undeclared ordinary enemy command '+str(command))
        return 0
