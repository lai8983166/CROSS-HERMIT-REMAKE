"""Real melee metadata, original binding/attack/animation and effect boundary."""
import argparse
import struct
import types
import unicorn.x86_const as x86
from unicorn import UC_PROT_READ,UC_PROT_WRITE
from unicorn.x86_const import UC_X86_REG_ESP,UC_X86_REG_ECX,UC_X86_REG_EIP
from tools import battle_attack_launch_emulation as parent
from tools import battle_pathfinding_emulation as path
from tools.battle_attack_animation import resource,corpus,validate,attack_input,basic

ROOT,SOURCE,need,sha=parent.ROOT,parent.SOURCE,parent.need,parent.sha
CTRL,UNIT,RECORD,FINE,ANIM=parent.CTRL,parent.UNIT,parent.RECORD,parent.FINE,parent.parent.previous.ANIM
DATA,EVENTS,SOUND=0x12300000,0x12400000,0x12500000
POOL,PAGE=0x765728,0x765000
EVENT_CTRL=CTRL+0x2F164
REGIONS=parent.REGIONS+((DATA,0x10000),(EVENTS,0x2000),(SOUND,0x3000),(PAGE,0x2D000))
EXTRA_RANGES=((0x409EF0,0x40A1E0),(0x40A400,0x40AF50),(0x40B5E0,0x40B6D0),(0x40B990,0x40BA20),
 (0x40BD10,0x40BE70),(0x40D390,0x40D4D0),(0x415070,0x4150A0),(0x4214F0,0x421540),(0x42B2D0,0x42B310),
 (0x466DA0,0x466F00),(0x467020,0x4671F0),(0x46A430,0x46A4D0),(0x46BD30,0x46BE20),(0x482A30,0x482D30))
RANGES=parent.RANGES+EXTRA_RANGES
ROOTS=parent.ROOTS|{0x467020,0x475270,0x40A100,0x482A30,0x40AC90,0x40BE20,0x409FF0}
ENTRIES={0x467020,0x409EF0,0x409FF0,0x40A100,0x40A520,0x40A800,0x40ADA0,0x40B5E0,0x40B990,0x40D390,0x40BD10,0x40BD80,0x40BDD0,0x482A30,0x482AC0,0x482B50,0x40BE20}
BOUNDARY=0x48AAE0
CPU_EXTRA_NAMES=('FPSW','FPTAG','FIP','FDP','FCS','FDS','FOP','MXCSR','CS','DS','ES','FS','GS','SS',
                 'CR0','CR2','CR3','CR4','GDTR','IDTR','LDTR','TR')+tuple('FP'+str(i) for i in range(8))+tuple('XMM'+str(i) for i in range(8))+tuple('DR'+str(i) for i in range(8))


def source_contract():
    raw=SOURCE.read_bytes()
    return dict(parent=parent.source_contract(),extra_code=[dict(start=a,end=b,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],
                assets=[resource(j)['identity'] for j in range(1,5)],CPU_extra_registers=list(CPU_EXTRA_NAMES),declared_loaded_cache=True,original_binding_root=0x467020,
                original_animation_root=0x40A100,effect_boundary=BOUNDARY,full_world_frame=False,host_animation_completion_written=False,
                original_file_GPU_sound_device_initialization_executed=False,hit_damage_death_verified=False)


class AnimationMachine(parent.AttackMachine):
    def __init__(self,c):
        validate(c);super().__init__(attack_input(c));self.animation_input=c;self.prefix_mode=False
        for at,n in REGIONS[len(parent.REGIONS):]:
            if at==PAGE:self.uc.mem_protect(at,n,UC_PROT_READ|UC_PROT_WRITE)
            else:self.uc.mem_map(at,n)
        self.uc.mem_write(POOL,bytes(2048*88));r=resource(c['job']);self.uc.mem_write(DATA,r['raw'])
        raw=SOURCE.read_bytes();j=c['job'];typ=j+8
        self.put(ANIM,DATA)
        for i,o in enumerate(r['offsets'][:5]):self.put(ANIM+4+i*4,DATA+o)
        self.put(ANIM+0x48,j,'h');self.put(ANIM+0x4C,struct.unpack_from('<I',raw,0x20E850+typ*4)[0]);self.put(ANIM+0x50,struct.unpack_from('<I',raw,0x20F070+typ*4)[0])
        self.put(ANIM+0x40,0);self.put(0x7A49FC,SOUND)
        palette=raw[0x218090+10+j*40];palette=palette+1 if palette else 0
        cache=CTRL+0x2A6F0
        self.put(cache,1,'B');self.put(cache+1,palette,'B');self.put(cache+2,j,'h');self.put(cache+4,ANIM)
        self.put(UNIT+0x290,2,'B');self.put(UNIT+0x28A,6,'B');self.put(UNIT+0x2F0,(5*16+8)*65536)
        self.put(RECORD+0xC,j,'H');self.put(UNIT+0x4F2,basic(j),'h')
        # Declared event pool; original functions perform every later pop/link.
        self.put(EVENT_CTRL+0x1C,EVENTS)
        for i in range(16):
            at=EVENTS+i*12;self.put(at,EVENT_CTRL+0x18 if i==0 else at-12);self.put(at+4,at+12 if i<15 else 0);self.put(at+8,EVENTS+0x1000+i*12)
        self.mutable += [(UNIT+0x520,UNIT+0xA40),(POOL,POOL+2048*88),(EVENT_CTRL,EVENT_CTRL+0x24),(EVENTS,EVENTS+16*12),(EVENTS+0x1000,EVENTS+0x1000+16*12)]

    base_call=types.FunctionType(path.PathMachine.call.__code__,dict(path.PathMachine.call.__globals__,ROOTS=ROOTS,STACK=parent.parent.previous.STACK,RETURN=parent.parent.previous.RETURN))
    snapshot=types.FunctionType(path.PathMachine.snapshot.__code__,dict(path.PathMachine.snapshot.__globals__,REGIONS=REGIONS))
    source_code=types.FunctionType(parent.parent.previous.RegionMachine.code.__code__,dict(parent.parent.previous.RegionMachine.code.__globals__,RANGES=RANGES))

    def code(self,uc,at,size,context):
        if self.prefix_mode and at==BOUNDARY:uc.emu_stop();return
        super().code(uc,at,size,context)
        if at in ENTRIES:self.entries[hex(at)]+=1

    def cpu(self):
        result=super().cpu()
        for name in CPU_EXTRA_NAMES:
            v=self.uc.reg_read(getattr(x86,'UC_X86_REG_'+name));result[name]=list(v) if isinstance(v,tuple) else v
        return result

    def state(self):
        children=bytes(self.uc.mem_read(POOL,2048*88))
        return dict(unit=self.unit(),children=children[:8*88].hex(),children_sha256=sha(children),
                    events=bytes(self.uc.mem_read(EVENTS,0x2000)).hex(),event_controller=bytes(self.uc.mem_read(EVENT_CTRL,0x24)).hex(),
                    record=self.record(),target=bytes(self.uc.mem_read(UNIT+0x520,0x520)).hex())

    def prefix(self):
        sp=parent.parent.previous.STACK+0xF000;self.put(sp,parent.parent.previous.RETURN)
        for i,a in enumerate((UNIT,0)):self.put(sp+4+i*4,a)
        self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,CTRL)
        before=self.cpu();count=self.instructions;self.prefix_mode=True
        self.uc.emu_start(0x482A30,parent.parent.previous.RETURN,timeout=60_000_000,count=1_000_000);self.prefix_mode=False
        need(self.uc.reg_read(UC_X86_REG_EIP)==BOUNDARY,'natural original effect boundary')
        return dict(entry=0x482A30,receiver=CTRL,args=[UNIT,0],cpu_before=before,cpu_after=self.cpu(),
                    instructions=self.instructions-count,stack_pointer=self.uc.reg_read(UC_X86_REG_ESP),
                    stack_hex=bytes(self.uc.mem_read(self.uc.reg_read(UC_X86_REG_ESP),sp+16-self.uc.reg_read(UC_X86_REG_ESP))).hex(),
                    returned=False,boundary=BOUNDARY,state=self.state(),memory=self.snapshot())

    def run(self):
        c=self.animation_input;initial=self.snapshot();roots=[self.call(0x437C90,(UNIT+off,),FINE) for off in (0x2F4,0x3E0)]
        bind_before=self.state();bind=self.call(0x467020,(UNIT,c['job']));bind_after=self.state()
        request=self.call(0x475270,(UNIT,6));steps=[];released=False
        for i in range(128):
            before=self.state();call=self.call(0x475700,(UNIT,));after=self.state()
            need(not self.get(UNIT+0x292,'B'),'no attack abort while reaching release')
            released=self.get(UNIT+0x293,'B')==22
            # Tick only after release; preparation clips are replaced by the
            # original attack state machine, not claimed as world updates.
            steps.append(dict(index=i,before=before,call=call,after=after))
            if released:break
        need(released,'source release budget')
        ticks=[]
        for i in range(128):
            before=self.state();call=self.call(0x40A100,(UNIT+0x48,),ANIM);after=self.state();ticks.append(dict(index=i,before=before,call=call,after=after))
            if c['consume']=='cancel' and self.get(UNIT+0x48+0x20):break
            if c['consume']=='early_boundary' and self.get(UNIT+0x48+0x34):break
            if not self.get(UNIT+0x48+4) and not self.get(UNIT+0x48+0x20):break
        else:raise ValueError('source animation end budget')
        consume=None;invalidation=[]
        if c['consume'] in ('boundary','early_boundary'):consume=self.prefix()
        elif c['consume'] in ('target_inactive','actor_inactive'):
            actor=UNIT+0x520 if c['consume']=='target_inactive' else UNIT
            invalidation=[self.call(0x475270,(actor,12)),self.call(0x4751F0,(actor,))]
            consume=dict(before=self.state(),call=self.call(0x482A30,(UNIT,0)),after=self.state(),returned=True)
        cleanup=[self.call(0x40AC90,(UNIT+0x48,),ANIM)]
        for off in (0x30,0x3C):
            while self.get(UNIT+0x48+off+4):cleanup.append(self.call(0x40BE20,(self.get(UNIT+0x48+off+4),),EVENT_CTRL))
        cleanup.append(self.call(0x439C60,receiver=FINE+0x18))
        return dict(input=c,initial=initial,roots=roots,bind_before=bind_before,bind=bind,bind_after=bind_after,request=request,
                    steps=steps,ticks=ticks,invalidation=invalidation,consume=consume,cleanup=cleanup,final_state=self.state(),**self.common())


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();need(not (ROOT/a.out).exists(),'fresh animation output')
    rows=[]
    for c in corpus():
        r=AnimationMachine(c).run();rows.append(r);print(c['name'],len(r['steps']),len(r['ticks']),flush=True)
    path.save(a.out,dict(schema_version=1,source_contract=source_contract(),cases=rows,R3_complete=False,R4_complete=False,R6_complete=False))
