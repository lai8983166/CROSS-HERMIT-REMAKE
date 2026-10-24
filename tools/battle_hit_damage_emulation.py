"""Original melee effect continuation, actual TLS APIs and HP application."""
import argparse
import struct
import types
from unicorn import UC_PROT_READ,UC_PROT_WRITE
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_EIP,UC_X86_REG_ESP
from tools import battle_attack_animation_emulation as parent
from tools import battle_pathfinding_emulation as path
from tools.battle_hit_damage import corpus,validate,animation_input,effect_resource
from tools.battle_hit_damage_platform import NativeTLS

ROOT,SOURCE,need,sha=parent.ROOT,parent.SOURCE,parent.need,parent.sha
CTRL,UNIT,RECORD,ANIM,FINE,EVENTS,EVENT_CTRL=parent.CTRL,parent.UNIT,parent.RECORD,parent.ANIM,parent.FINE,parent.EVENTS,parent.EVENT_CTRL
FXDATA,FXOBJ,TLS,TANIM,CRT_PAGE,API_PAGE=0x12600000,0x12620000,0x12621000,0x12622000,0x761000,0x7701E000
TARGET=UNIT+0x520
DAMAGE,POPUP=CTRL+0x2B6F0,CTRL+0x2C6F0
REGIONS=parent.REGIONS+((FXDATA,0x20000),(FXOBJ,0x1000),(TLS,0x1000),(TANIM,0x1000),(CRT_PAGE,0x1000),(API_PAGE,0x1000))
EXTRA_RANGES=((0x40AF40,0x40B0F0),(0x43B9E0,0x43BB90),(0x465140,0x465280),(0x467E00,0x467EB0),
 (0x468E10,0x468EB0),(0x4692E0,0x4693A0),(0x469730,0x4697F0),(0x469B90,0x469C60),(0x46A4C0,0x46A550),
 (0x46B3E0,0x46B470),(0x4753F0,0x475480),(0x4824D0,0x4826F0),(0x482D30,0x482E90),
 (0x48AAE0,0x48ADC0),(0x48B2E0,0x48B630),(0x4918D0,0x4922E0),(0x492DE0,0x492E20),(0x492F00,0x493570),
 (0x494D70,0x495140),(0x495630,0x495860),(0x49AD90,0x49B030),(0x4DE8F0,0x4DEAF0),(0x4DFA70,0x4DFB20),
 (0x570FE0,0x571040),(0x5753B0,0x575450))
RANGES=parent.RANGES+EXTRA_RANGES
ROOTS=parent.ROOTS|{0x4918D0,0x493450,0x494D70}
ENTRIES={0x48AAE0,0x48AC90,0x4824D0,0x482D60,0x465140,0x40AF40,0x4918D0,0x4919F0,0x491EF0,0x493090,0x493450,0x570FE0,0x5753B0,0x467E00,0x467E70,0x494DB0,0x494E70,0x495630}
APIS={0x7701E2B0:('GetLastError',0,0x5753BC),0x7701E1C0:('TlsGetValue',1,0x5753CB),0x7701E240:('SetLastError',1,0x575441)}


def source_contract():
    raw=SOURCE.read_bytes()
    return dict(parent=parent.source_contract(),extra_code=[dict(start=a,end=b,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],
                effect_source=effect_resource()['identity'],IAT_unchanged=True,actual_current_thread_TLS_leaves=True,
                TLS_guest_slot_role=51,TLS_guest_context_token=TLS,CRT_getptd_and_rand_bodies_executed=True,
                platform_implementation_sha256=sha((ROOT/'tools/battle_hit_damage_platform.py').read_bytes()),
                fresh_combat_fields_declared_before_first_root=True,unmodified_legacy_checkpoint_resumed=False,death_world_or_GPU_complete=False)


class DamageMachine(parent.AnimationMachine):
    def __init__(self,c):
        validate(c);super().__init__(animation_input(c));self.combat_input=c;self.hit_observations=[];self.hp_writes=[];self.native=None
        for at,n in REGIONS[len(parent.REGIONS):]:
            if at==CRT_PAGE:self.uc.mem_protect(at,n,UC_PROT_READ|UC_PROT_WRITE)
            else:self.uc.mem_map(at,n)
        r=effect_resource();self.uc.mem_write(FXDATA,r['raw']);self.put(FXOBJ,FXDATA)
        for i,o in enumerate(r['offsets'][:5]):self.put(FXOBJ+4+i*4,FXDATA+o)
        self.put(FXOBJ+0x48,0,'h');self.put(FXOBJ+0x40,0);self.put(CTRL+0x2A6E8,FXOBJ)
        self.uc.mem_write(TANIM,bytes(self.uc.mem_read(ANIM,0x1000)))
        cache=CTRL+0x2A6F8;palette=SOURCE.read_bytes()[0x218090+11+c['job']*40];palette=palette+1 if palette else 0
        self.put(cache,1,'B');self.put(cache+1,palette,'B');self.put(cache+2,c['job'],'h');self.put(cache+4,TANIM)
        self.put(0x761BC0,51);self.put(TLS+0x14,c['crt_seed']);self.put(CTRL+0x2E70C,c['seed']);self.put(CTRL+0x2E710,0)
        for off,value in ((0x3A,c['power']),(0x3C,c['spread']),(0x38,c['accuracy'])):self.put(RECORD+off,value,'H')
        for off,value,fmt in ((0xC,c['job'],'H'),(0x4C,c['evasion'],'B'),(0x4D,c['armor'],'B'),(0x52,c['mental'],'H'),
                              (0x14,c['max_hp'],'h'),(0x16,c['hp'],'h'),(0x54,c['threshold'],'H')):self.put(RECORD+0x100+off,value,fmt)
        self.put(TARGET+6,int(c['target_attacking']),'B')
        self.put(TARGET+0x28A,6,'B')
        self.mutable += [(RECORD+0x116,RECORD+0x118),(RECORD+0x1A6,RECORD+0x1A8),(CTRL+0x2E70C,CTRL+0x2E714),
                         (DAMAGE,DAMAGE+512*8),(POPUP,POPUP+512*16),(TLS+0x14,TLS+0x18)]

    base_call=types.FunctionType(path.PathMachine.call.__code__,dict(path.PathMachine.call.__globals__,ROOTS=ROOTS,STACK=parent.parent.parent.previous.STACK,RETURN=parent.parent.parent.previous.RETURN))
    snapshot=types.FunctionType(path.PathMachine.snapshot.__code__,dict(path.PathMachine.snapshot.__globals__,REGIONS=REGIONS))
    source_code=types.FunctionType(parent.parent.parent.previous.RegionMachine.code.__code__,dict(parent.parent.parent.previous.RegionMachine.code.__globals__,RANGES=RANGES))

    def code(self,uc,at,size,context):
        if at in APIS:
            name,n,ret=APIS[at];sp=uc.reg_read(UC_X86_REG_ESP);need(self.get(sp)==ret,'actual original CRT API caller')
            args=[self.get(sp+4+i*4) for i in range(n)];value=self.native.leaf(name,args)
            uc.reg_write(UC_X86_REG_EAX,value or 0);uc.reg_write(UC_X86_REG_ESP,sp+4+n*4);uc.reg_write(UC_X86_REG_EIP,ret);return
        super().code(uc,at,size,context)
        if at in ENTRIES:self.entries[hex(at)]+=1
        if at==0x48AD03:
            ebp=uc.reg_read(parent.x86.UC_X86_REG_EBP)
            self.hit_observations.append(dict(kind=uc.reg_read(UC_X86_REG_EAX),attack=bytes(uc.mem_read(ebp-0x3C,44)).hex(),
                                              defense=bytes(uc.mem_read(ebp-0x68,44)).hex(),seed=self.get(CTRL+0x2E70C),draws=self.get(CTRL+0x2E710)))

    def state(self):
        s=super().state()
        s.update(target_record=bytes(self.uc.mem_read(RECORD+0x100,256)).hex(),damage_pool=bytes(self.uc.mem_read(DAMAGE,512*8)).hex(),
                 popup_pool=bytes(self.uc.mem_read(POPUP,512*16)).hex(),battle_seed=self.get(CTRL+0x2E70C),battle_draws=self.get(CTRL+0x2E710),
                 CRT_seed=self.get(TLS+0x14),platform_error=self.native.last_error if self.native else 0x1234)
        return s

    def write_hook(self,uc,access,at,size,value,context):
        super().write_hook(uc,access,at,size,value,context)
        if at==RECORD+0x116:self.hp_writes.append(dict(pc=uc.reg_read(UC_X86_REG_EIP),address=at,bytes=size,value=value&65535))

    def prefix(self):
        # Existing prefix returns before executing any effect instruction;
        # resume on its actual stack/registers, without a new game root.
        p=super().prefix();count=self.instructions;before=self.state();cpu=self.cpu()
        self.uc.emu_start(parent.BOUNDARY,parent.parent.parent.previous.RETURN,timeout=60_000_000,count=1_000_000)
        need(self.uc.reg_read(UC_X86_REG_EIP)==parent.parent.parent.previous.RETURN,'whole original attack consumer naturally returned')
        continuation=dict(before=before,cpu_before=cpu,cpu_after=self.cpu(),after=self.state(),instructions=self.instructions-count,returned=True)
        damage_before=self.state();damage_call=self.call(0x4918D0,(TARGET,1));damage_after=self.state()
        hp_before=self.state();hp_call=self.call(0x493450,(TARGET,));hp_after=self.state()
        ticks=[]
        for i in range(128):
            if not self.get(TARGET+0xA0+0x20):break
            b=self.state();call=self.call(0x40A100,(TARGET+0xA0,),ANIM);ticks.append(dict(before=b,call=call,after=self.state()))
        need(not self.get(TARGET+0xA0+0x20),'source EFCT end budget')
        return dict(frontier=p,continuation=continuation,damage=dict(before=damage_before,call=damage_call,after=damage_after),
                    hp=dict(before=hp_before,call=hp_call,after=hp_after),effect_ticks=ticks,hit=self.hit_observations)

    def run(self):
        self.native=NativeTLS(TLS)
        try:
            # Bind target in the same declared loaded-resource lifetime before
            # the original actor binding/request/attack sequence.
            initial=self.snapshot();target_before=self.state();target_bind=self.call(0x467020,(TARGET,self.combat_input['job']));target_after=self.state()
            r=super().run();r['input']=self.combat_input;r['initial']=initial
            r['target_bind']=dict(before=target_before,call=target_bind,after=target_after)
            popup_cleanup=[]
            for i in range(512):
                if self.get(POPUP+i*16,'B')&128:popup_cleanup.append(self.call(0x494D70,(POPUP+i*16,)))
            r['popup_cleanup']=popup_cleanup;r['final_state']=self.state();r['hp_writes']=self.hp_writes;r.update(self.common())
            r['platform']=dict(creation=self.native.creation,trace=self.native.trace,cleanup=self.native.close())
            return r
        finally:
            if not self.native.closed:self.native.close()


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();need(not (ROOT/a.out).exists(),'fresh hit damage source')
    rows=[]
    for c in corpus():
        r=DamageMachine(c).run();rows.append(r);print(c['name'],r['consume']['hit'][0]['kind'],struct.unpack_from('<h',bytes.fromhex(r['consume']['hp']['after']['target_record']),0x16)[0],flush=True)
    path.save(a.out,dict(schema_version=1,source_contract=source_contract(),cases=rows,R3_complete=False,R4_complete=False,R6_complete=False))
