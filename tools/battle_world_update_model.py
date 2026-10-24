"""Independent finite world pre/unit/post model; no emulator output as input."""
import struct
from tools.battle_combat_aftermath_model import Model as UnitModel,CTRL,UNIT,TARGET
from tools.battle_world_update_emulation import WORLD_FIELDS,VISIBLE_OTHER,parent

VISIBLE=parent.VISIBLE


class Model(UnitModel):
    def __init__(self,c):
        super().__init__(c['aftermath']);self.world=c
        self.fields={a:bytearray(n) for a,n in WORLD_FIELDS};self.other=bytearray(0x2000)
        self.current,self.back=VISIBLE,VISIBLE_OTHER
        self.memput(parent.region.MAP+0xA4,self.current);self.memput(parent.region.MAP+0xA8,self.back)
        self.fields[0x7A2960][:]=self.source[0x3A2960:0x3A2980]
        # Frozen loaded-scene candidate declaration, before any game root.
        self.build_list(0xDC8EC,[UNIT,TARGET])

    def area(self,a,n):
        if hasattr(self,'fields'):
            for base,b in self.fields.items():
                if base<=a and a+n<=base+len(b):return b,a-base
        return super().area(a,n)

    def state(self):
        s=super().state();s.update(all_unit_slots=(self.unit+self.target+bytes(248*0x520)).hex(),
                                 world_fields={hex(a):b.hex() for a,b in self.fields.items()},visible_other=self.other.hex())
        return s

    def mark_view(self,u):
        if self.current==VISIBLE:return super().mark_view(u)
        physical=self.visible;self.visible=self.other
        try:super().mark_view(u)
        finally:self.other=self.visible;self.visible=physical

    def dispatch(self,u):
        if u==TARGET and self.memget(u+0x290,'B')==2 and self.memget(u+0x293,'B')==2:
            # Original 476250 recomputes an idle threshold on every enemy
            # phase-2 tick, even while its timer is far below that threshold.
            threshold=30+20*(self.rng.next()%10)
            if self.memget(u+0xA,'h')>threshold:
                self.memput(u+0x292,15,'B');self.memput(u+0x293,3,'B')
            return 0
        return super().dispatch(u)

    def build_list(self,a,units):
        self.memput(CTRL+a,len(units))
        for i,u in enumerate(units):self.memput(CTRL+a+4+i*4,u)

    def pre(self):
        self.last_updated=0
        if not self.world['world_enabled']:return
        self.current,self.back=self.back,self.current
        self.memput(parent.region.MAP+0xA4,self.current);self.memput(parent.region.MAP+0xA8,self.back)
        (self.visible if self.current==VISIBLE else self.other)[:6144]=bytes(6144)
        # Empty normalized mouse/keyboard, zero pan, no pending mode or event.
        for off,v,fmt in ((0x2A312,-1,'h'),(0x2A314,-1,'h'),(0x2A316,-1,'h'),(0x2A318,-1,'h'),
                          (0x2A31A,8,'h'),(0x2A31C,8,'h'),(0x2A340,0,'I'),(0x2A34C,-1,'h'),(0x2A34E,-1,'h'),
                          (0x2A350,0,'I'),(0x2F150,0,'I'),(0x2F157,0,'B')):self.memput(CTRL+off,v,fmt)
        self.fields[0x7A2960][:]=bytes(32)
        alive=[u for u,r in ((UNIT,self.records[0]),(TARGET,self.records[1])) if r[15]==1]
        visible=[u for u in alive if -64<=self.memget(u+0x2EC,'i')>>16<=1088 and -34<=((self.memget(u+0x2F0,'i')>>16)+30)<=664]
        visible.sort(key=lambda u:self.memget(u+0x2F0,'i'),reverse=True)
        self.build_list(0xDC30C,visible)
        for a,units in ((0xDC8EC,alive),(0xDCCD8,[]),(0xDD0C4,[u for u in alive if u==TARGET]),
                        (0xDD4B0,[u for u in alive if u==UNIT]),(0xDD89C,[u for u in alive if u==UNIT])):self.build_list(a,units)
        self.memput(CTRL+0x108B50,0);self.memput(CTRL+0x108B54,0)
        self.fields[CTRL+0x3098C][:]=bytes(16);self.memput(CTRL+0x30992,-1,'h')
        # Exactly 0x800 bytes reset; score/death totals immediately after it persist.
        self.stats[:0x800]=bytes(0x800)

    def post(self):
        self.last_updated=0
        if not self.world['world_enabled']:return
        self.memput(CTRL+0x115CB8,1,'B');self.memput(CTRL+0x109D4E,-1,'h');self.memput(CTRL+0x2F160,0,'I')
        for i in range(10):
            a=CTRL+0x10C680+i*0x520
            self.memput(a+4,1,'B');self.put_wrap(a+0xA,self.memget(a+0xA,'h')+1)
