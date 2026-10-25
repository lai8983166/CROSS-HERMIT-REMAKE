"""Natural lethal worlds followed by one explicitly supplemental result-input root."""
import argparse,json,types
from unicorn import UC_PROT_READ,UC_PROT_WRITE
from concurrent.futures import ProcessPoolExecutor
from tools import battle_bilateral_combat_emulation as parent
from tools.battle_hit_damage_platform import NativeTLS
from tools.battle_lethal_combat import corpus,validate,base_input,declarations,done,pages

ROOT,SOURCE,need,sha=parent.ROOT,parent.SOURCE,parent.need,parent.sha
CTRL,UNIT,TARGET,RECORD,ANIM,FINE=parent.CTRL,parent.UNIT,parent.TARGET,parent.RECORD,parent.ANIM,parent.FINE
REGIONS=parent.REGIONS+((0x7F5000,0x1000),)
EXTRA_RANGES=((0x46CB10,0x46CBD0),(0x473860,0x473DC0),(0x4307B0,0x430980),(0x469C60,0x469D30))
RANGES=parent.RANGES+EXTRA_RANGES
ALLOWED=frozenset(at for a,b in RANGES for at in range(a,b))
REFERENCE=types.FunctionType(parent.REFERENCE.__code__,dict(parent.REFERENCE.__globals__,RANGES=RANGES))
OBSERVED=dict(parent.OBSERVED,**{})
OBSERVED.update({0x4799C0:1,0x479F40:1,0x46BA10:1,0x472770:1,0x475370:3})


def source_contract():
    return dict(frozen_driver=parent.source_contract(),extra_code=[dict(start=a,end=b,sha256=sha(parent.parent.CODE[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],
                initial_HP=[70,1000],victim_role_explicit=True,HP_recovery_interval=32767,world_only_until_removal=True,
                supplemental_finalization_root=0x473860,result_selector_declared_unresolved_zero=True,automatic_victory_or_rewards=False,
                independent_whole_world_byte_model=False,owned_regions=38)


class LethalMachine(parent.BilateralMachine):
    source_code=types.FunctionType(parent.BilateralMachine.source_code.__code__,dict(parent.BilateralMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))
    code=types.FunctionType(parent.BilateralMachine.code.__code__,dict(parent.BilateralMachine.code.__globals__,OBSERVED=OBSERVED),closure=parent.BilateralMachine.code.__closure__)
    snapshot=types.FunctionType(parent.BilateralMachine.snapshot.__code__,dict(parent.BilateralMachine.snapshot.__globals__,REGIONS=REGIONS))
    base_call=types.FunctionType(parent.BilateralMachine.base_call.__code__,dict(parent.BilateralMachine.base_call.__globals__,ROOTS=parent.BilateralMachine.base_call.__globals__['ROOTS']|{0x473860}))

    def __init__(self,c,reference_guard=False):
        validate(c);super().__init__(base_input(c),reference_guard);self.cycle_input=c;self.uc.mem_protect(0x7F5000,0x1000,UC_PROT_READ|UC_PROT_WRITE)
        for at,v,f in declarations(c):self.put(at,v,f)
        self.mutable.extend([(0x7F450C,0x7F4514)]+[(0x7F4518+j*0xB0+0xAA,0x7F4518+j*0xB0+0xAF) for j in range(20)])

    def boundary_state(self):
        s=super().boundary_state();s['death_stats']=bytes(self.uc.mem_read(CTRL+0x2EF14,0x30)).hex()
        s['occupied']=[self.get(0x11600000+((((self.get(u+0x2F0,'i')>>16)//16)*64+(self.get(u+0x2EC,'i')>>16)//32)*2)+1,'B') for u in (UNIT,TARGET)]
        return s

    def state(self):
        s=super().state();s['result_data']=bytes(self.uc.mem_read(0x7F4000,0x2000)).hex();return pages(s,self.blobs)

    def run(self):
        self.native=NativeTLS(parent.parent.world.parent.parent.TLS)
        try:
            initial=self.snapshot();target_before=self.state();target_bind=self.call(0x467020,(TARGET,self.combat_input['job']));target_after=self.state()
            roots=[self.call(0x437C90,(u+off,),FINE) for u in (UNIT,TARGET) for off in (0x2F4,0x3E0)]
            before=self.state();bind=self.call(0x467020,(UNIT,self.combat_input['job']));after=self.state()
            frames=[];terminal=None
            for i in range(self.cycle_input['budget']):
                f=dict(index=i,before=self.state(),entries=[],scanned_slots=[],unit_calls=[],stages=[],controls=[],nested_calls=[],ai_calls=[])
                self.frame_observation=f;self.running_update=True
                try:f['call']=self.call(0x46B470)
                except Exception as error:
                    self.failure=dict(error=str(error),frame=i,CPU=self.cpu(),boundary=self.boundary_state(),pending=self.pending_contracts,last_contracts=self.contracts[-20:],hit=self.hit_observations,hit_sides=self.hit_sides);raise
                finally:self.frame_observation=None;self.running_update=False
                need(not self.pending_contracts,'all original nested contracts returned');f['after']=self.state();frames.append(f)
                if i%64==0:print(self.cycle_input['name'],'world',i,flush=True)
                if terminal is None and done(self.get,self.cycle_input,i):terminal=i
                elif terminal is not None:need(i==terminal+1,'one extra world after removal');break
            else:raise ValueError('lethal world budget')
            result_before=self.state();result_call=self.call(0x473860);result_after=self.state()
            finalization=dict(before=result_before,call=result_call,after=result_after)
            cleanup=[]
            for u in (UNIT,TARGET):
                cleanup.append(self.call(0x40AC90,(u+0x48,),self.get(u+0x44)))
                for off in (0x30,0x3C):
                    while self.get(u+0x48+off+4):cleanup.append(self.call(0x40BE20,(self.get(u+0x48+off+4),),parent.parent.world.parent.parent.EVENT_CTRL))
                for j in range(5):cleanup.append(self.call(0x40AC90,(u+0xA0+j*88,),0x12620000))
            cleanup.append(self.call(0x439C60,receiver=FINE+0x18))
            popup_cleanup=[self.call(0x494D70,(parent.parent.world.parent.parent.POPUP+j*16,)) for j in range(512) if self.get(parent.parent.world.parent.parent.POPUP+j*16,'B')&128]
            row=dict(input=self.cycle_input,initial=initial,target_bind=dict(before=target_before,call=target_bind,after=target_after),roots=roots,bind_before=before,bind=bind,bind_after=after,
                world_frames=frames,terminal_index=terminal,hit=self.hit_observations,hit_sides=self.hit_sides,contracts=self.contracts,both_hp_writes=self.both_hp_writes,
                finalization=finalization,cleanup=cleanup,popup_cleanup=popup_cleanup,final_state=self.state(),hp_writes=self.hp_writes,lifecycle_writes=self.lifecycle_writes,**self.common())
            row['platform']=dict(creation=self.native.creation,trace=self.native.trace,cleanup=self.native.close());row['blobs']=self.blobs;return row
        finally:
            if not self.native.closed:self.native.close()


def emit_case(task):
    c,out=task;m=LethalMachine(c)
    try:r=m.run()
    except Exception:
        if hasattr(m,'failure'):parent.parent.world.path.save(out+'.failure.json.gz',dict(input=c,source_contract=source_contract(),failure=m.failure,accepted=False))
        raise RuntimeError(c['name']+' original execution failed') from None
    parent.parent.world.path.save(out,dict(schema_version=1,source_contract=source_contract(),cases=[r],R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False))
    raw=(ROOT/out).read_bytes();print(c['name'],len(r['world_frames']),r['instructions'],flush=True);return dict(name=c['name'],path=out,bytes=len(raw),sha256=sha(raw))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case');p.add_argument('--jobs',type=int,default=3);a=p.parse_args();out=ROOT/a.out
    need(not out.exists() and 1<=a.jobs<=3,'fresh bounded lethal output')
    if a.case:
        cs=[c for c in corpus() if c['name']==a.case];need(len(cs)==1,'one lethal case');emit_case((cs[0],a.out))
    else:
        tasks=[(c,out.with_name(out.stem+'-'+c['name']+'.json.gz').relative_to(ROOT).as_posix()) for c in corpus()];need(out.suffix=='.json' and all(not (ROOT/s).exists() for c,s in tasks),'fresh case files')
        with ProcessPoolExecutor(max_workers=a.jobs) as pool:refs=list(pool.map(emit_case,tasks))
        out.write_text(json.dumps(dict(schema_version=1,source_contract=source_contract(),case_reports=refs,R3_complete=False,R4_complete=False,R5_complete=False,R6_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
