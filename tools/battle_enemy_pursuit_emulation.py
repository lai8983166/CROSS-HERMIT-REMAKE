"""Original idle/search/path admission/movement/attack in complete worlds."""
import argparse,json
from concurrent.futures import ProcessPoolExecutor
from unicorn.x86_const import UC_X86_REG_ESP,UC_X86_REG_ECX,UC_X86_REG_EIP
from tools import battle_enemy_engagement_emulation as parent
from tools.battle_enemy_pursuit import corpus,validate,base_input,target_fields

ROOT,SOURCE,need,sha=parent.ROOT,parent.SOURCE,parent.need,parent.sha
CTRL,UNIT,TARGET,RECORD,ANIM=parent.CTRL,parent.UNIT,parent.TARGET,parent.RECORD,parent.ANIM
REGIONS=parent.REGIONS
MOVEMENT_CALLS={0x476680:2,0x47D210:2,0x47D570:2,0x47D930:1,0x47DA30:1,0x47DBD0:1,0x47DEC0:1,0x470250:3,0x465040:3,0x437D90:2}


def source_contract():
    return dict(parent=parent.source_contract(),out_of_range_target_before_first_root=True,
                only_complete_worlds_after_binding=True,declared_initial_target_occupancy=True,
                source_code_admission_unchanged=True,explicit_attack_stop_move_or_coordinate_inputs=False,
                full_extra_replan_frame=True,original_native_scheduler_rendering_or_victory_complete=False)


class PursuitMachine(parent.EnemyMachine):
    def __init__(self,c,reference_guard=False):
        validate(c);super().__init__(base_input(c),reference_guard);self.cycle_input=c;self.coordinate_stores=[]
        occ=parent.world.parent.region.OCC;oldx=(self.get(TARGET+0x2EC,'i')>>16)//32;oldy=(self.get(TARGET+0x2F0,'i')>>16)//16
        at=occ+(oldy*64+oldx)*2+1;self.put(at,self.get(at,'B')-1,'B')
        for off,v,fmt in target_fields(c):self.put(TARGET+off,v,fmt)
        x,y=c['target_cell'];at=occ+(y*64+x)*2+1;self.put(at,self.get(at,'B')+1,'B')

    def code(self,uc,at,size,context):
        super().code(uc,at,size,context);f=self.frame_observation
        if f is None:return
        if at==0x46B470:f['pursuit_calls']=[]
        if at in MOVEMENT_CALLS:
            sp=uc.reg_read(UC_X86_REG_ESP);f['pursuit_calls'].append(dict(entry=at,receiver=uc.reg_read(UC_X86_REG_ECX),caller=self.get(sp),args=[self.get(sp+4+i*4) for i in range(MOVEMENT_CALLS[at])]))

    def write_hook(self,uc,access,at,size,value,context):
        super().write_hook(uc,access,at,size,value,context)
        if at in (UNIT+0x2EC,UNIT+0x2F0):self.coordinate_stores.append(dict(pc=uc.reg_read(UC_X86_REG_EIP),address=at,bytes=size,value=value&0xFFFFFFFF))

    def run(self):
        r=super().run();r['coordinate_stores']=self.coordinate_stores;return r


def emit_case(task):
    c,out=task;r=PursuitMachine(c).run();parent.world.path.save(out,dict(schema_version=1,source_contract=source_contract(),cases=[r],R3_complete=False,R4_complete=False,R6_complete=False))
    raw=(ROOT/out).read_bytes();print(c['name'],len(r['world_frames']),r['instructions'],len(r['coordinate_stores']),flush=True)
    return dict(name=c['name'],path=out,bytes=len(raw),sha256=sha(raw))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case');p.add_argument('--jobs',type=int,default=3);a=p.parse_args();out=ROOT/a.out
    need(not out.exists() and 1<=a.jobs<=3,'fresh bounded pursuit output')
    if a.case:
        selected=[c for c in corpus() if c['name']==a.case];need(len(selected)==1,'one declared pursuit case');emit_case((selected[0],a.out))
    else:
        need(out.suffix=='.json','pursuit source bundle')
        tasks=[(c,out.with_name(out.stem+'-'+c['name']+'.json.gz').relative_to(ROOT).as_posix()) for c in corpus()]
        need(all(not (ROOT/s).exists() for c,s in tasks),'all pursuit sources fresh')
        with ProcessPoolExecutor(max_workers=a.jobs) as pool:refs=list(pool.map(emit_case,tasks))
        out.write_text(json.dumps(dict(schema_version=1,source_contract=source_contract(),case_reports=refs,R3_complete=False,R4_complete=False,R6_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
