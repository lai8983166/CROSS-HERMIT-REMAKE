"""Whole original world root with natural 250-slot unit dispatch."""
import argparse
import struct
import types
from unicorn.x86_const import UC_X86_REG_ESP,UC_X86_REG_EIP,UC_X86_REG_EAX
from unicorn import UC_PROT_READ,UC_PROT_WRITE
from tools import battle_combat_aftermath_emulation as parent
from tools import battle_pathfinding_emulation as path
from tools.battle_world_update import corpus,validate

ROOT,SOURCE,need,sha=parent.ROOT,parent.SOURCE,parent.need,parent.sha
CTRL,UNIT,TARGET,RECORD,ANIM=parent.CTRL,parent.UNIT,parent.TARGET,parent.RECORD,parent.ANIM
VISIBLE_OTHER=0x12744000
REGIONS=parent.REGIONS+((VISIBLE_OTHER,0x2000),(0x7A2000,0x1000))
EXTRA_RANGES=((0x46B470,0x46B670),(0x4678C0,0x467C20),(0x46E520,0x46EA10),(0x46EA10,0x46ED90),
 (0x46F440,0x46F890),(0x49B180,0x49BA60),(0x490FC0,0x4912C0),(0x49CC60,0x49CCE0),
 (0x49C400,0x49C850),(0x466880,0x466910),(0x493630,0x4936A0),(0x493A30,0x493B80),(0x48CE60,0x48CEB0),
 (0x43B350,0x43B3C0),(0x43B530,0x43B8B0),(0x43C700,0x43CB00),(0x43D0C0,0x43D1A0),(0x4406F0,0x440980),
 (0x481610,0x4816C0),(0x49BA60,0x49BB20),(0x456B20,0x456B60),(0x46B130,0x46B1A0),(0x46A550,0x46A5E0),
 (0x46A950,0x46AA40),(0x4945B0,0x4947B0),(0x4947B0,0x4949E0),(0x48CD90,0x48CE60),
 (0x427DE0,0x427E30),(0x4128F0,0x412A10),(0x48D5D0,0x48D720),
 (0x46F170,0x46F440),(0x496450,0x496490),(0x49CE90,0x49D160))
RANGES=parent.RANGES+EXTRA_RANGES
ROOTS=parent.ROOTS|{0x46B470}
WORLD_ENTRIES={0x46B470,0x4678C0,0x493630,0x467B60,0x46E9C0,0x49B180,0x46E520,0x46E730,0x48CD90,0x46EA10,0x46F440,
               0x490FC0,0x49CC60,0x49C400,0x466880,0x493A30,0x48CE60}
STAGES={0x46B529:'before_units',0x46B586:'after_units',0x46B652:'world_return'}
# Every additional world-owned writable field is modeled; all other owned
# bytes retain the stricter frozen parent write policy.
WORLD_FIELDS=((parent.region.MAP+0xA4,8),(CTRL+0x2A30E,0x48),(CTRL+0x2F150,0x14),
 (CTRL+0x3098C,0x10),(CTRL+0xDC30C,0x197C),(CTRL+0x108B50,0x410),
 (CTRL+0x109D4E,2),(CTRL+0x10C680,10*0x520),(CTRL+0x115CB8,1),(0x7A2960,32))


def source_contract():
    raw=SOURCE.read_bytes()
    return dict(parent=parent.source_contract(),extra_code=[dict(start=a,end=b,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],
                complete_world_root=0x46B470,slot_count=250,unit_root_only_called_from_original_world=True,
                declared_empty_interaction_and_pending_sentinels=True,original_native_scheduler_or_rendering_connected=False)


class WorldMachine(parent.AftermathMachine):
    def __init__(self,c):
        validate(c);super().__init__(c['aftermath']);self.world_input=c;self.frame_observation=None
        self.uc.mem_map(VISIBLE_OTHER,0x2000);self.uc.mem_protect(0x7A2000,0x1000,UC_PROT_READ|UC_PROT_WRITE)
        self.put(parent.region.MAP+0xA8,VISIBLE_OTHER)
        self.put(CTRL+0x108B32,int(c['world_enabled']),'h');self.put(CTRL+0x108B3B,-1,'b');self.put(CTRL+0x108B3C,-1,'b')
        self.mutable += [(a,a+n) for a,n in WORLD_FIELDS]+[(VISIBLE_OTHER,VISIBLE_OTHER+0x2000)]

    base_call=types.FunctionType(path.PathMachine.call.__code__,dict(path.PathMachine.call.__globals__,ROOTS=ROOTS,STACK=parent.region.STACK,RETURN=parent.region.RETURN))
    source_code=types.FunctionType(parent.region.RegionMachine.code.__code__,dict(parent.region.RegionMachine.code.__globals__,RANGES=RANGES))
    snapshot=types.FunctionType(path.PathMachine.snapshot.__code__,dict(path.PathMachine.snapshot.__globals__,REGIONS=REGIONS))

    def state(self):
        s=super().state();s.update(all_unit_slots=bytes(self.uc.mem_read(UNIT,250*0x520)).hex(),
                                 world_fields={hex(a):bytes(self.uc.mem_read(a,n)).hex() for a,n in WORLD_FIELDS},
                                 visible_other=bytes(self.uc.mem_read(VISIBLE_OTHER,0x2000)).hex())
        return s

    def code(self,uc,at,size,context):
        super().code(uc,at,size,context);f=self.frame_observation
        if f is None:return
        if at in WORLD_ENTRIES:f['entries'].append(at)
        if at==0x468D10:
            sp=uc.reg_read(UC_X86_REG_ESP)
            if self.get(sp)==0x46B560:f['scanned_slots'].append(self.get(sp+4))
        if at==0x46B760:
            sp=uc.reg_read(UC_X86_REG_ESP);need(self.get(sp)==0x46B584,'natural world unit caller')
            f['unit_calls'].append(dict(unit=self.get(sp+4),index=self.get(sp+8),caller=self.get(sp),before=self.state(),cpu_before=self.cpu()))
        # Unused predicates branch to the same loop join. Capture a nested
        # return only once, while a genuine unit call is pending.
        if at==0x46B584 and f['unit_calls'] and 'cpu_after' not in f['unit_calls'][-1]:
            f['unit_calls'][-1].update(after=self.state(),cpu_after=self.cpu(),result=uc.reg_read(UC_X86_REG_EAX))
        if at in STAGES:f['stages'].append(dict(name=STAGES[at],state=self.state(),CPU=self.cpu()))

    def prefix(self):
        # Reuse the frozen hit/HP prefix, bypassing its manually chosen unit
        # update schedule; every following unit call comes from 46B470 itself.
        p=parent.parent.DamageMachine.prefix(self);frames=[]
        for i in range(self.world_input['frames']):
            f=dict(index=i,before=self.state(),entries=[],scanned_slots=[],unit_calls=[],stages=[]);self.frame_observation=f;self.running_update=True
            try:f['call']=self.call(0x46B470)
            finally:self.frame_observation=None;self.running_update=False
            f['after']=self.state();frames.append(f)
        p['world_frames']=frames;return p

    def run(self):
        r=super().run();r['input']=self.world_input;return r


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();need(not (ROOT/a.out).exists(),'fresh world source')
    rows=[]
    for c in corpus():
        r=WorldMachine(c).run();rows.append(r);print(c['name'],len(r['consume']['world_frames']),r['instructions'],flush=True)
    path.save(a.out,dict(schema_version=1,source_contract=source_contract(),cases=rows,R3_complete=False,R4_complete=False,R6_complete=False))
