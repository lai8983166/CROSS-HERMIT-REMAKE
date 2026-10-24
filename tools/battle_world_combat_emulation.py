"""Original binding/request then whole world frames through one combat cycle."""
import argparse
import struct
import types
import json
from concurrent.futures import ProcessPoolExecutor
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_ESP,UC_X86_REG_ECX
from tools import battle_world_update_emulation as world
from tools.battle_hit_damage_platform import NativeTLS
from tools.battle_world_combat import corpus,validate,pages,settled

ROOT,SOURCE,need,sha=world.ROOT,world.SOURCE,world.need,world.sha
CTRL,UNIT,TARGET,RECORD,ANIM=world.CTRL,world.UNIT,world.TARGET,world.RECORD,world.ANIM
REGIONS=world.REGIONS
CODE=SOURCE.read_bytes()
EXTRA_RANGES=((0x479F40,0x47A240),(0x469AD0,0x469B90))
RANGES=world.RANGES+EXTRA_RANGES
ALLOWED=frozenset(at for a,b in RANGES for at in range(a,b))
REFERENCE=types.FunctionType(world.parent.region.RegionMachine.code.__code__,dict(world.parent.region.RegionMachine.code.__globals__,RANGES=RANGES))


def source_contract():
    return dict(parent=world.source_contract(),extra_code=[dict(start=a,end=b,sha256=sha(CODE[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],from_original_attack_request=True,independent_attack_animation_effect_or_HP_roots=False,
                declared_living_target_command=5,explicit_actor_stop_request_after_phase24=5,full_extra_settled_frame=True,
                lossless_page_bytes=4096,fast_guard_same_original_ranges=True,original_native_scheduler_rendering_or_victory_complete=False)


class CombatMachine(world.WorldMachine):
    def __init__(self,c,reference_guard=False):
        validate(c);self.blobs={};self.reference_guard=reference_guard
        super().__init__(dict(name=c['name'],aftermath=c['aftermath'],frames=3,world_enabled=True))
        self.cycle_input=c;self.put(TARGET+0x290,5,'B');self.frame_observation=None

    def state(self):return pages(super().state(),self.blobs)

    def code(self,uc,at,size,context):
        super().code(uc,at,size,context)
        if self.frame_observation is not None and at in (0x475700,0x40A100,0x482A30,0x4918D0,0x493450,0x48AAE0):
            sp=uc.reg_read(UC_X86_REG_ESP);n={0x475700:1,0x40A100:1,0x482A30:2,0x4918D0:2,0x493450:1,0x48AAE0:4}[at]
            self.frame_observation['nested_calls'].append(dict(entry=at,receiver=uc.reg_read(UC_X86_REG_ECX),caller=self.get(sp),args=[self.get(sp+4+j*4) for j in range(n)]))

    def source_code(self,uc,at,size,context):
        if self.reference_guard:return REFERENCE(self,uc,at,size,context)
        r=world.parent.region
        if at==r.RETURN:uc.emu_stop();return
        need(at in ALLOWED,'undeclared original instruction '+hex(at));need(CODE[at-0x400000]!=0xCC,'original assertion/padding '+hex(at))
        self.instructions+=1;self.code_hash.update(struct.pack('<I',at))
        if at in r.ROOTS or at in (0x44ED40,0x44F1E0,0x4380B0,0x47DA30,0x47DEC0):self.entries[hex(at)]+=1
        if at==0x439C4F:
            link=uc.reg_read(UC_X86_REG_EAX);node=self.get(link+8);kind='coarse' if r.C_LINK<=link<r.C_LINK+0x12000 else 'fine'
            self.popped[kind].append([self.get(node+2,'h'),self.get(node+4,'h')])
        if at==0x427C90:self.improved+=1
        if at==0x427D20:self.reopened+=1

    def run(self):
        self.native=NativeTLS(world.parent.parent.TLS)
        try:
            initial=self.snapshot();target_before=self.state();target_bind=self.call(0x467020,(TARGET,self.combat_input['job']));target_after=self.state()
            roots=[self.call(0x437C90,(UNIT+off,),world.parent.region.FINE) for off in (0x2F4,0x3E0)]
            before=self.state();bind=self.call(0x467020,(UNIT,self.combat_input['job']));after=self.state()
            request_before=self.state();request=self.call(0x475270,(UNIT,6));request_after=self.state()
            frames=[];stopped=False;terminal_index=None
            for i in range(self.cycle_input['budget']):
                f=dict(index=i,before=self.state(),entries=[],scanned_slots=[],unit_calls=[],stages=[],controls=[],nested_calls=[])
                self.frame_observation=f;self.running_update=True
                try:f['call']=self.call(0x46B470)
                finally:self.frame_observation=None;self.running_update=False
                f['after']=self.state()
                if not stopped and self.get(UNIT+0x290,'B')==6 and self.get(UNIT+0x293,'B')==24:
                    b=self.state();call=self.call(0x475270,(UNIT,5));f['controls'].append(dict(reason='stop completed first attack before re-admission',before=b,call=call,after=self.state()));stopped=True
                frames.append(f)
                done=settled(self.get,self.get(RECORD+0x10F,'B'),self.hit_observations,stopped)
                if done and terminal_index is None:terminal_index=i
                elif terminal_index is not None:
                    need(done and i==terminal_index+1,'one full additional settled world frame');break
            else:raise ValueError('complete world combat cycle budget')
            cleanup=[self.call(0x40AC90,(UNIT+0x48,),ANIM)]
            for off in (0x30,0x3C):
                while self.get(UNIT+0x48+off+4):cleanup.append(self.call(0x40BE20,(self.get(UNIT+0x48+off+4),),world.parent.parent.EVENT_CTRL))
            cleanup.append(self.call(0x439C60,receiver=world.parent.region.FINE+0x18))
            popup_cleanup=[]
            for j in range(512):
                if self.get(world.parent.parent.POPUP+j*16,'B')&128:popup_cleanup.append(self.call(0x494D70,(world.parent.parent.POPUP+j*16,)))
            row=dict(input=self.cycle_input,initial=initial,target_bind=dict(before=target_before,call=target_bind,after=target_after),roots=roots,
                     bind_before=before,bind=bind,bind_after=after,request=dict(before=request_before,call=request,after=request_after),
                     world_frames=frames,terminal_index=terminal_index,hit=self.hit_observations,cleanup=cleanup,popup_cleanup=popup_cleanup,
                     final_state=self.state(),hp_writes=self.hp_writes,lifecycle_writes=self.lifecycle_writes,**self.common())
            row['platform']=dict(creation=self.native.creation,trace=self.native.trace,cleanup=self.native.close());row['blobs']=self.blobs
            return row
        finally:
            if not self.native.closed:self.native.close()


def emit_case(task):
    c,out=task;r=CombatMachine(c).run()
    world.path.save(out,dict(schema_version=1,source_contract=source_contract(),cases=[r],R3_complete=False,R4_complete=False,R6_complete=False))
    raw=(ROOT/out).read_bytes();print(c['name'],len(r['world_frames']),r['instructions'],len(r['blobs']),flush=True)
    return dict(name=c['name'],path=out,bytes=len(raw),sha256=sha(raw))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case');p.add_argument('--jobs',type=int,default=3);a=p.parse_args();out=ROOT/a.out
    need(not out.exists() and 1<=a.jobs<=3,'fresh bounded world combat source')
    if a.case:
        selected=[c for c in corpus() if c['name']==a.case];need(len(selected)==1,'one declared source case');emit_case((selected[0],a.out))
    else:
        need(out.suffix=='.json','per-case source bundle manifest')
        tasks=[(c,out.with_name(out.stem+'-'+c['name']+'.json.gz').relative_to(ROOT).as_posix()) for c in corpus()]
        need(all(not (ROOT/s).exists() for c,s in tasks),'all case output paths fresh')
        with ProcessPoolExecutor(max_workers=a.jobs) as pool:refs=list(pool.map(emit_case,tasks))
        out.write_text(json.dumps(dict(schema_version=1,source_contract=source_contract(),case_reports=refs,R3_complete=False,R4_complete=False,R6_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
