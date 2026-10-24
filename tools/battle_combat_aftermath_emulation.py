"""Complete original unit updates in the still-live basic hit/TLS lifetime."""
import argparse
import struct
import types
from unicorn import UC_PROT_READ,UC_PROT_WRITE
from unicorn.x86_const import UC_X86_REG_ESP,UC_X86_REG_EIP
from tools import battle_hit_damage_emulation as parent
from tools import battle_region_routing_emulation as region
from tools import battle_pathfinding_emulation as path
from tools.battle_combat_aftermath import corpus,validate

ROOT,SOURCE,need,sha=parent.ROOT,parent.SOURCE,parent.need,parent.sha
CTRL,UNIT,TARGET,RECORD,ANIM=parent.CTRL,parent.UNIT,parent.TARGET,parent.RECORD,parent.ANIM
TASK,EVENT_ENV,STATIC_PAGE=0x12700000,0x12730000,0x618000
VISIBLE,SEEN=0x12740000,0x12742000
REGIONS=parent.REGIONS+((TASK,0x30000),(EVENT_ENV,0x1000),(STATIC_PAGE,0x1000),(0x7F4000,0x1000),(VISIBLE,0x2000),(SEEN,0x2000))
EXTRA_RANGES=((0x430400,0x43072A),(0x430B20,0x430B9B),(0x43BB90,0x43BCF8),(0x43C470,0x43C530),
 (0x43D1A0,0x43D4E0),(0x468EB0,0x468F80),(0x469220,0x4692E0),(0x469480,0x469510),(0x46A5E0,0x46A6A0),(0x46B2C0,0x46B350),(0x46B760,0x46BC20),
 (0x46BE50,0x46BEB0),(0x472370,0x472550),(0x472770,0x4727F0),(0x475370,0x4753F0),(0x475460,0x4756A0),
 (0x476250,0x4763D0),(0x478850,0x479270),(0x4799C0,0x479E40),(0x48D720,0x48DC50),(0x48E2A0,0x48E483),
 (0x4902A0,0x4903C0),(0x490A50,0x490B30),(0x492E60,0x492E90),(0x493570,0x4935F0),(0x496E70,0x496F10),(0x5711E4,0x57128E))
RANGES=parent.RANGES+EXTRA_RANGES
ROOTS=parent.ROOTS|{0x46B760}
ENTRIES={0x46B760,0x48D720,0x48E2A0,0x490350,0x472370,0x472770,0x478850,0x478BC0,0x4799C0,0x46BA10,0x430B20,0x4305C0,0x43C470,0x475460}


def source_contract():
    raw=SOURCE.read_bytes()
    return dict(parent=parent.source_contract(),extra_code=[dict(start=a,end=b,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],
                complete_unit_update_root=0x46B760,declared_task_map_and_empty_event_environment=True,declared_consistent_initial_occupancy=True,
                no_host_completion_or_timer_writes=True,original_world_outer_scheduler_or_full_frame=False)


class AftermathMachine(parent.DamageMachine):
    def __init__(self,c):
        validate(c);super().__init__(c['combat']);self.aftermath_input=c;self.update_entries=[];self.lifecycle_writes=[];self.running_update=False
        for at,n in REGIONS[len(parent.REGIONS):]:
            if at in (STATIC_PAGE,0x7F4000):self.uc.mem_protect(at,n,UC_PROT_READ|UC_PROT_WRITE)
            else:self.uc.mem_map(at,n)
        self.put(CTRL+0x108B32,1,'h');self.put(CTRL+0x108B34,1,'B');self.put(CTRL+0x117C38,TASK)
        self.put(TASK+0x3EF8+0x2659C,region.HEADER);self.put(0x7A49F4,TASK);self.put(0x7A49F8,EVENT_ENV)
        self.put(region.MAP+0xA4,VISIBLE);self.put(region.MAP+0xA0,SEEN)
        self.put(RECORD+0xAA,c['actor_kills'],'h');self.put(RECORD+0xAC,c['actor_points'],'h');self.put(RECORD+0x1AE,c['target_deaths'],'b')
        self.put(RECORD+0x1A8,c['kill_points'],'h')
        self.put(CTRL+0x2EF14,c['score'],'h');self.put(CTRL+0x2E714,c['region_count'],'h')
        for u in (UNIT,TARGET):
            x=(self.get(u+0x2EC,'i')>>16)//32;y=(self.get(u+0x2F0,'i')>>16)//16
            for o,v in ((0x4E7,x),(0x4E8,y),(0x4E9,x),(0x4EA,y)):self.put(u+o,v,'B')
            self.put(region.OCC+(y*64+x)*2+1,self.get(region.OCC+(y*64+x)*2+1,'B')+1,'B')
        self.mutable += [(RECORD,RECORD+512),(region.OCC,region.OCC+0x3000),(CTRL+0x2E714,CTRL+0x2EF44),
                         (0x7A49E0,0x7A49E4),(0x618CF0,0x618CF8),(VISIBLE,VISIBLE+0x2000),(SEEN,SEEN+0x2000)]

    base_call=types.FunctionType(path.PathMachine.call.__code__,dict(path.PathMachine.call.__globals__,ROOTS=ROOTS,STACK=region.STACK,RETURN=region.RETURN))
    snapshot=types.FunctionType(path.PathMachine.snapshot.__code__,dict(path.PathMachine.snapshot.__globals__,REGIONS=REGIONS))
    source_code=types.FunctionType(region.RegionMachine.code.__code__,dict(region.RegionMachine.code.__globals__,RANGES=RANGES))

    def code(self,uc,at,size,context):
        super().code(uc,at,size,context)
        if at in ENTRIES:
            self.entries[hex(at)]+=1
            if self.running_update:self.update_entries.append(at)

    def write_hook(self,uc,access,at,size,value,context):
        super().write_hook(uc,access,at,size,value,context)
        if self.running_update and (UNIT<=at<UNIT+0xA40 or RECORD<=at<RECORD+512 or region.OCC<=at<region.OCC+0x3000 or CTRL+0x2E714<=at<CTRL+0x2EF44):
            self.lifecycle_writes.append(dict(pc=uc.reg_read(UC_X86_REG_EIP),address=at,bytes=size,value=value&((1<<(size*8))-1)))

    def state(self):
        s=super().state();s.update(occupancy=bytes(self.uc.mem_read(region.OCC,0x3000)).hex(),
                                 world_stats=bytes(self.uc.mem_read(CTRL+0x2E714,0x830)).hex(),
                                 last_updated=self.get(0x7A49E0),motion_scratch=bytes(self.uc.mem_read(0x618CF0,8)).hex(),
                                 visible=bytes(self.uc.mem_read(VISIBLE,0x2000)).hex(),seen=bytes(self.uc.mem_read(SEEN,0x2000)).hex())
        return s

    def prefix(self):
        p=super().prefix();updates=[];actor_done=False;target_done=False
        target_needs_update=bool(self.get(TARGET+0x292,'B')) or self.get(RECORD+0x116,'h')==0
        for i in range(256):
            for u,done in ((UNIT,actor_done),(TARGET,target_done)):
                if done:continue
                if u==TARGET and not target_needs_update and i>0:target_done=True;continue
                b=self.state();entries=len(self.update_entries);writes=len(self.lifecycle_writes);self.running_update=True
                try:call=self.call(0x46B760,(u,0 if u==UNIT else 1))
                finally:self.running_update=False
                updates.append(dict(round=i,unit=u,before=b,call=call,after=self.state(),entries=self.update_entries[entries:],writes=self.lifecycle_writes[writes:]))
                if u==UNIT:actor_done=self.get(UNIT+0x292,'B')!=0 or self.get(UNIT+0x290,'B')!=6 or self.get(UNIT+0x293,'B')==24
                else:target_done=(self.get(TARGET+0x290,'B')==11 or self.get(TARGET+0x292,'B') not in (0,8,9,13)) or (self.get(TARGET+0x290,'B') in (8,9) and self.get(TARGET+0x2A6,'B')==0)
            if actor_done and target_done:break
        need(actor_done and target_done,'source attack/reaction/death update budget')
        p['aftermath']=updates;return p

    def run(self):
        r=super().run();r['input']=self.aftermath_input;r['lifecycle_writes']=self.lifecycle_writes;r['final_state']=self.state();return r


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();need(not (ROOT/a.out).exists(),'fresh combat aftermath source')
    rows=[]
    for c in corpus():
        r=AftermathMachine(c).run();rows.append(r);print(c['name'],len(r['consume']['aftermath']),bytes.fromhex(r['final_state']['target'])[0x290:0x294].hex(),flush=True)
    path.save(a.out,dict(schema_version=1,source_contract=source_contract(),cases=rows,R3_complete=False,R4_complete=False,R6_complete=False))
