"""Unmodified original whole worlds with both units autonomous and read-only contracts."""
import argparse
import json
import struct
import types
from concurrent.futures import ProcessPoolExecutor
from unicorn.x86_const import UC_X86_REG_ESP,UC_X86_REG_EAX,UC_X86_REG_ECX,UC_X86_REG_EIP
from tools import battle_enemy_engagement_emulation as parent
from tools.battle_hit_damage_platform import NativeTLS
from tools.battle_bilateral_combat import corpus,validate,base_input,declarations

ROOT,SOURCE,need,sha=parent.ROOT,parent.SOURCE,parent.need,parent.sha
CTRL,UNIT,TARGET,RECORD,ANIM,REGIONS=parent.CTRL,parent.UNIT,parent.TARGET,parent.RECORD,parent.ANIM,parent.REGIONS
FINE=parent.world.parent.region.FINE
EXTRA_RANGES=((0x47B800,0x47BA20),(0x492E20,0x492F00),(0x47CE70,0x47D010),(0x43C1D0,0x43C320),(0x47C210,0x47C580),(0x47E460,0x47E680))
RANGES=parent.RANGES+EXTRA_RANGES
ALLOWED=frozenset(at for a,b in RANGES for at in range(a,b))
REFERENCE=types.FunctionType(parent.REFERENCE.__code__,dict(parent.REFERENCE.__globals__,RANGES=RANGES))
OBSERVED={0x4751F0:1,0x475270:2,0x476250:1,0x476470:1,0x4776A0:1,0x47A920:1,0x47C580:2,0x477980:1,
          0x48AAE0:4,0x4918D0:2,0x493450:1,0x472370:1,0x467E00:2,0x570FE0:0}


def source_contract():
    return dict(frozen_driver=parent.source_contract(),both_initial_commands_are_idle=True,passive_control=True,
                both_initial_reaction_target_and_skill=-1,
                declarations_before_first_root=True,world_only_after_binding=True,external_attack_or_stop_requests=False,
                boundary_observations_are_read_only=True,full_state_independent_model=False,
                independent_scope=['target scan boundary','physical hit boundary','HP queue boundary'],
                frozen_guard_algorithm_and_call_and_API_implementation=True,
                extra_code=[dict(start=a,end=b,sha256=sha(parent.CODE[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],complete_native_gameplay=False)


class BilateralMachine(parent.EnemyMachine):
    source_code=types.FunctionType(parent.EnemyMachine.source_code.__code__,dict(parent.EnemyMachine.source_code.__globals__,ALLOWED=ALLOWED,REFERENCE=REFERENCE))
    def __init__(self,c,reference_guard=False):
        validate(c);super().__init__(base_input(c),reference_guard);self.cycle_input=c
        for at,v,f in declarations(c):self.put(at,v,f)
        self.pending_contracts=[];self.contracts=[];self.both_hp_writes=[];self.hit_sides=[];self.return_sites=set()

    def boundary_state(self):
        records=[bytes(self.uc.mem_read(RECORD+i*256,256)).hex() for i in range(2)]
        units=[bytes(self.uc.mem_read(u,0x520)).hex() for u in (UNIT,TARGET)]
        queues=[]
        for u in (UNIT,TARGET):
            nodes=[];p=self.get(u+0x510)
            while p:
                need(len(nodes)<512 and p not in [r['pointer'] for r in nodes] and CTRL+0x2B6F0<=p<CTRL+0x2B6F0+4096 and (p-CTRL-0x2B6F0)%8==0,'owned acyclic damage queue')
                nodes.append(dict(pointer=p,hex=bytes(self.uc.mem_read(p,8)).hex()));p=self.get(p+4)
            queues.append(nodes)
        return dict(records=records,units=units,queues=queues,battle_seed=self.get(CTRL+0x2E70C),battle_draws=self.get(CTRL+0x2E710),CRT_seed=self.get(0x12621014))

    def code(self,uc,at,size,context):
        super().code(uc,at,size,context)
        if self.frame_observation is None:return
        if at not in OBSERVED and at!=0x48AD03 and at not in self.return_sites:return
        sp=uc.reg_read(UC_X86_REG_ESP)
        while self.pending_contracts and (at,sp)==(self.pending_contracts[-1]['caller'],self.pending_contracts[-1]['return_ESP']):
            event=self.pending_contracts.pop();event.update(after=self.boundary_state(),result=uc.reg_read(UC_X86_REG_EAX))
        if at in OBSERVED:
            n=OBSERVED[at];args=[self.get(sp+4+i*4) for i in range(n)]
            event=dict(entry=at,frame=self.frame_observation['index'],receiver=uc.reg_read(UC_X86_REG_ECX),caller=self.get(sp),args=args,return_ESP=sp+4+4*n,before=self.boundary_state())
            if at==0x48AAE0:event['input_packet']=bytes(uc.mem_read(args[2],12)).hex()
            self.contracts.append(event);self.pending_contracts.append(event)
            self.return_sites.add(event['caller'])
        if at==0x48AD03:
            event=next(e for e in reversed(self.pending_contracts) if e['entry']==0x48AAE0)
            event['resolved']=dict(self.hit_observations[-1]);self.hit_sides.append(dict(frame=self.frame_observation['index'],attacker=event['args'][0],victim=event['args'][1],hit_index=len(self.hit_observations)-1))

    def write_hook(self,uc,access,at,size,value,context):
        super().write_hook(uc,access,at,size,value,context)
        if self.running_update and at in (RECORD+0x16,RECORD+0x116):
            self.both_hp_writes.append(dict(frame=self.frame_observation['index'],pc=uc.reg_read(UC_X86_REG_EIP),address=at,bytes=size,value=value&65535))

    def run(self):
        self.native=NativeTLS(parent.world.parent.parent.TLS)
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
                    self.failure=dict(error=str(error),frame=i,CPU=self.cpu(),boundary=self.boundary_state(),pending=self.pending_contracts,
                                      last_contracts=self.contracts[-20:],hit=self.hit_observations,hit_sides=self.hit_sides)
                    raise
                finally:self.frame_observation=None;self.running_update=False
                need(not self.pending_contracts,'all nested contracts naturally returned');f['after']=self.state();frames.append(f)
                if i%32==0:print(self.cycle_input['name'],'world',i,flush=True)
                counts=[sum(s['attacker']==u for s in self.hit_sides) for u in (UNIT,TARGET)]
                done=(counts[0]>=2 and counts[1]>=int(self.cycle_input['player_active'])*2) if self.cycle_input['rounds'] else i==self.cycle_input['budget']-2
                if terminal is None and done:terminal=i
                elif terminal is not None:need(i==terminal+1,'one extra bilateral world');break
            else:raise ValueError('bilateral engagement frame budget')
            cleanup=[]
            for u in (UNIT,TARGET):
                cleanup.append(self.call(0x40AC90,(u+0x48,),self.get(u+0x44)))
                for off in (0x30,0x3C):
                    while self.get(u+0x48+off+4):cleanup.append(self.call(0x40BE20,(self.get(u+0x48+off+4),),parent.world.parent.parent.EVENT_CTRL))
                for j in range(5):cleanup.append(self.call(0x40AC90,(u+0xA0+j*88,),0x12620000))
            cleanup.append(self.call(0x439C60,receiver=FINE+0x18))
            popup_cleanup=[self.call(0x494D70,(parent.world.parent.parent.POPUP+j*16,)) for j in range(512) if self.get(parent.world.parent.parent.POPUP+j*16,'B')&128]
            row=dict(input=self.cycle_input,initial=initial,target_bind=dict(before=target_before,call=target_bind,after=target_after),roots=roots,
                     bind_before=before,bind=bind,bind_after=after,world_frames=frames,terminal_index=terminal,hit=self.hit_observations,hit_sides=self.hit_sides,
                     contracts=self.contracts,both_hp_writes=self.both_hp_writes,cleanup=cleanup,popup_cleanup=popup_cleanup,final_state=self.state(),
                     hp_writes=self.hp_writes,lifecycle_writes=self.lifecycle_writes,**self.common())
            row['platform']=dict(creation=self.native.creation,trace=self.native.trace,cleanup=self.native.close());row['blobs']=self.blobs;return row
        finally:
            if not self.native.closed:self.native.close()


def emit_case(task):
    c,out=task;m=BilateralMachine(c)
    try:r=m.run()
    except Exception:
        if hasattr(m,'failure'):parent.world.path.save(out+'.failure.json.gz',dict(input=c,source_contract=source_contract(),failure=m.failure,accepted=False))
        raise
    parent.world.path.save(out,dict(schema_version=1,source_contract=source_contract(),cases=[r],R3_complete=False,R4_complete=False,R6_complete=False))
    raw=(ROOT/out).read_bytes();print(c['name'],len(r['world_frames']),r['instructions'],len(r['hit']),flush=True)
    return dict(name=c['name'],path=out,bytes=len(raw),sha256=sha(raw))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);p.add_argument('--case');p.add_argument('--jobs',type=int,default=3);a=p.parse_args();out=ROOT/a.out
    need(not out.exists() and 1<=a.jobs<=3,'fresh bounded bilateral source')
    if a.case:
        cs=[c for c in corpus() if c['name']==a.case];need(len(cs)==1,'one declared bilateral case');emit_case((cs[0],a.out))
    else:
        need(out.suffix=='.json','bundle manifest');tasks=[(c,out.with_name(out.stem+'-'+c['name']+'.json.gz').relative_to(ROOT).as_posix()) for c in corpus()]
        need(all(not (ROOT/s).exists() for c,s in tasks),'all fresh case paths')
        with ProcessPoolExecutor(max_workers=a.jobs) as pool:refs=list(pool.map(emit_case,tasks))
        out.write_text(json.dumps(dict(schema_version=1,source_contract=source_contract(),case_reports=refs,R3_complete=False,R4_complete=False,R6_complete=False),indent=2)+'\n',encoding='utf8',newline='\n')
