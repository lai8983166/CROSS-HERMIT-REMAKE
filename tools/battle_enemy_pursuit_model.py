"""Independent original route admission, movement animation and world combat."""
from tools.battle_enemy_engagement_model import Model as EnemyModel
from tools.battle_enemy_pursuit import base_input,target_fields
from tools.battle_enemy_engagement_emulation import UNIT,TARGET


class Model(EnemyModel):
    def __init__(self,c):
        super().__init__(base_input(c));self.cycle=c;self.attack['cell']=c['target_cell'][:]
        x,y=self.cell(TARGET);self.occupancy[(y*64+x)*2+1]-=1
        for off,v,fmt in target_fields(c):self.memput(TARGET+off,v,fmt)
        x,y=c['target_cell'];self.occupancy[(y*64+x)*2+1]+=1
        self.coordinate_stores=[];self.expected_pursuit=None;self.direct_movement_action=False

    def path_call(self,entry,caller,args,receiver=0x11000000):
        if self.expected_pursuit is not None:self.expected_pursuit.append(dict(entry=entry,receiver=receiver,caller=caller,args=args))

    def action_for(self,u,action):
        if getattr(self,'expected_pursuit',None) is not None:
            self.path_call(0x465040,0x47E1E6 if self.direct_movement_action else 0x46BCFE,[u+0x48,action,self.memget(u+0x28A,'B')],self.memget(u+0x44))
        return super().action_for(u,action)

    def consume_pending(self,u):
        if self.memget(u+0x292,'B'):self.path_call(0x437D90,0x4756E7,[u,0],0x1102A634)
        return super().consume_pending(u)

    def command(self):
        if self.get(0x293,'B')==12 and not self.range_ok():self.path_call(0x476680,0x4780F3,[UNIT,1])
        return super().command()

    def cancel(self):self.path_call(0x437D90,0x477B10,[UNIT,0],0x1102A634)

    def evaluate(self,avoid=False,force_search=False,resume=False):
        entry=0x47D730 if resume else 0x47D570 if force_search else 0x47D210
        caller=(0x476A57 if avoid else 0x476894) if resume else (0x4769E5 if avoid else 0x476827) if force_search else (0x47696B if avoid else 0x4767AA)
        self.path_call(entry,caller,[UNIT,int(avoid)])
        if not force_search and not resume and self.cell()!=self.grid(0x4D0) and not self.clear(self.cell(),self.grid(0x4D0),avoid):self.path_call(0x437D90,0x47D4D6,[UNIT,int(avoid)],0x1102A634)
        return super().evaluate(avoid,force_search,resume)

    def segment(self):self.path_call(0x47D930,0x476AF5,[UNIT]);return super().segment()
    def next_tile(self):self.path_call(0x47DA30,0x476B0D,[UNIT]);return super().next_tile()
    def arrival(self):self.path_call(0x47DBD0,0x476B7E,[UNIT]);return super().arrival()

    def occupied(self,p):
        x,y=p
        return 0<=x<64 and 0<=y<96 and bool(self.occupancy[(y*64+x)*2+1])

    def move(self):
        self.path_call(0x47DEC0,0x476BA1,[UNIT]);self.path_call(0x470250,0x47DEF1,[UNIT])
        before_action=self.get(0x54,'h');before_direction=self.get(0x28A,'B');old_done=self.get(4,'B');old_timer=self.get(0xA,'h')
        super().move()
        if before_action!=3 or before_direction!=self.get(0x28A,'B'):
            self.direct_movement_action=True
            try:self.action_for(UNIT,3)
            finally:self.direct_movement_action=False
            self.put(4,old_done,'B');self.put(0xA,old_timer,'h')
        self.coordinate_stores.extend([self.get(0x2EC),self.get(0x2F0)])
