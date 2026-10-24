"""Full original attack dispatcher through release, with declared empty clips."""
import argparse
import types
from unicorn.x86_const import UC_X86_REG_ESP
from tools import battle_target_acquisition_emulation as parent
from tools import battle_pathfinding_emulation as path
from tools.battle_attack_launch import corpus, charge_corpus, target_input, validate

ROOT,SOURCE,need,sha=parent.ROOT,parent.SOURCE,parent.need,parent.sha
CTRL,UNIT,RECORD,FINE=parent.CTRL,parent.UNIT,parent.RECORD,parent.FINE
REGIONS=parent.REGIONS
EXTRA_RANGES=((0x4695D0,0x469660),(0x46B0B0,0x46B140),(0x46BCC0,0x46BD30),(0x46C040,0x46C290),(0x46C930,0x46C9F0),
 (0x472550,0x472770),(0x477980,0x4787B0),(0x47BA20,0x47C200),(0x48CAE0,0x48CD40),
 (0x490CD0,0x490F90),(0x4DDC60,0x4DDD50))
RANGES=parent.RANGES+EXTRA_RANGES
ROOTS=parent.ROOTS|{0x46C930,0x46C990}
ENTRIES={0x477980,0x47BA20,0x47BC90,0x47BED0,0x4DDC60,0x48CAE0,0x490CD0,0x46C120,0x46BCC0,0x46C930,0x46C990,0x472550}


def source_contract():
    raw=SOURCE.read_bytes()
    return dict(parent=parent.source_contract(),extra_code=[dict(start=a,end=b,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],
                root=0x475700,empty_animation_resource=-1,stop_phase=22,full_world_frame=False,hit_or_damage_verified=False,
                skill_range_record_offset=0x37,skill_mode6_range_offset=0x44)


class AttackMachine(parent.TargetMachine):
    def __init__(self,c):
        validate(c);super().__init__(target_input(c));self.config=c;self.events=[]
        self.put(UNIT+0x290,6,'B');self.put(UNIT+0x292,6 if c['pending'] else 0,'B')
        if c['pending']:self.put(UNIT+0x290,4,'B')
        self.put(UNIT+0x4EE,1,'h');self.put(UNIT+0x4F2,c['skill'],'h')
        self.put(UNIT+0x4F0,c['cell'][0],'B');self.put(UNIT+0x4F1,c['cell'][1],'B')
        self.put(UNIT+0x14,c['status'],'B')
        for off,v,fmt in ((0x14,100,'h'),(0x16,100,'h'),(0x1A,c['max_mp'],'h'),(0x1C,c['mp'],'h'),
                          (0x32,c['windup'],'h'),(0x34,c['recovery'],'h'),(0x37,c['range'],'B'),(2,c['actor_id'],'H')):
            self.put(RECORD+off,v,fmt)
        self.mutable += [(RECORD+0x1C,RECORD+0x1E)]
        if c['selection']:
            self.put(UNIT+0x290,4,'B');self.put(UNIT+0x4EE,-1,'h');self.put(UNIT+0x4F2,-1,'h')

    base_call=types.FunctionType(path.PathMachine.call.__code__,dict(path.PathMachine.call.__globals__,ROOTS=ROOTS,STACK=parent.previous.STACK,RETURN=parent.previous.RETURN))
    source_code=types.FunctionType(parent.previous.RegionMachine.code.__code__,dict(parent.previous.RegionMachine.code.__globals__,RANGES=RANGES))

    def code(self,uc,at,size,context):
        self.source_code(uc,at,size,context)
        if at in parent.ENTRIES|ENTRIES:self.entries[hex(at)]+=1
        if at in (0x46BCC0,0x46C120,0x46C990):
            sp=uc.reg_read(UC_X86_REG_ESP);n=3 if at==0x46C120 else 2
            raw=[self.get(sp+4+i*4) for i in range(n)];args=raw[:]
            if at==0x46C120:args[1:]=[(v+32768)%65536-32768 for v in args[1:]]
            self.events.append(dict(entry=at,args=args,raw_args=raw))

    def common(self):return dict(**super().common(),action_events=self.events)

    def record(self):return bytes(self.uc.mem_read(RECORD,0x100)).hex()

    def charge(self):
        initial=self.snapshot();roots=[self.call(0x437C90,(UNIT+off,),FINE) for off in (0x2F4,0x3E0)]
        before=self.unit();rec=self.record();gate=self.call(0x46C930,(UNIT,self.config['skill']))
        charge=self.call(0x46C990,(UNIT,self.config['skill'])) if gate['result'] else None
        cleanup=[self.call(0x439C60,receiver=FINE+0x18)]
        return dict(input=self.config,initial=initial,roots=roots,before_hex=before,after_hex=self.unit(),record_before=rec,
                    record_after=self.record(),gate=gate,charge=charge,cleanup=cleanup,**self.common())

    def run(self):
        c=self.config;initial=self.snapshot();steps=[]
        roots=[self.call(0x437C90,(UNIT+off,),FINE) for off in (0x2F4,0x3E0)]
        waits=0
        for i in range(c['calls']):
            before=self.unit();rec=self.record();call=self.call(0x475700,(UNIT,))
            steps.append(dict(index=i,before_hex=before,after_hex=self.unit(),record_before=rec,record_after=self.record(),call=call))
            if self.get(UNIT+0x292,'B') not in (0,6):stop='pending_command';break
            if self.get(UNIT+0x293,'B')==22:
                waits+=1
                if waits==4:stop='release_then_three_waits';break
        else:stop='call_budget'
        cleanup=[self.call(0x439C60,receiver=FINE+0x18)]
        return dict(input=c,initial=initial,roots=roots,steps=steps,stop=stop,cleanup=cleanup,**self.common())


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();need(not (ROOT/a.out).exists(),'fresh attack source')
    rows=[]
    for c in corpus():
        r=AttackMachine(c).run();rows.append(r);print(c['name'],len(r['steps']),r['stop'],flush=True)
    charges=[]
    for c in charge_corpus():
        charges.append(AttackMachine(c).charge());print(c['name'],'MP helper roots',flush=True)
    path.save(a.out,dict(schema_version=1,source_contract=source_contract(),cases=rows,charge_cases=charges,R3_complete=False,R4_complete=False,R6_complete=False))
