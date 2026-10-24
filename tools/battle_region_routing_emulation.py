"""Actual MAP05 graph relocation/search and full original AI, in declared memory."""
import argparse
from collections import Counter
import hashlib
import struct
import types
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_WRITE,UC_PROT_EXEC
from unicorn.x86_const import UC_X86_REG_EAX,UC_X86_REG_FPCW
from tools import battle_unit_movement_emulation as movement
from tools import battle_route_admission_emulation as admission
from tools import battle_pathfinding_emulation as path
from tools.battle_region_routing import inputs,query_corpus,route_corpus

ROOT,SOURCE,need,sha=path.ROOT,path.SOURCE,path.need,path.sha
CTRL,UNIT,RECORD,ANIM=movement.CTRL,movement.UNIT,movement.RECORD,movement.ANIM
COARSE,FINE,MAP=CTRL+0x2A55C,CTRL+0x2A634,CTRL+0x3D68
HEADER,TERR,OCC,OCC_PTR,VPT=0x11400000,0x11500000,0x11600000,0x11700000,0x11800000
F_LINK,F_NODE,F_INDEX=0x11900000,0x11A00000,0x11B00000
C_LINK,C_NODE,C_INDEX=0x11C00000,0x11D00000,0x11E00000
PACKET,STACK,RETURN,SCRATCH=0x11F00000,0x12000000,0x12100000,0x7A3FA4
REGIONS=((CTRL,0x10A000),(RECORD,0x1000),(ANIM,0x1000),(HEADER,0xA000),(TERR,0x2000),(OCC,0x3000),(OCC_PTR,0x1000),
         (VPT,0x19000),(F_LINK,0x12000),(F_NODE,0x2A000),(F_INDEX,0x6000),(C_LINK,0x12000),(C_NODE,0x2A000),(C_INDEX,0x6000),
         (PACKET,0x1000),(STACK,0x20000),(0x7A3000,0x2000))
EXTRA_RANGES=((0x44E5D0,0x44E740),(0x44E9A0,0x44EA20),(0x44EA80,0x44F460),(0x44F680,0x44F870))
RANGES=admission.RANGES+EXTRA_RANGES
ROOTS=admission.ROOTS|{0x44E5D0,0x44E650,0x44E6E0,0x44E9A0,0x44EA80,0x44F680}


def source_contract():
    raw=SOURCE.read_bytes()
    return dict(parent=admission.source_contract(),original_inputs=inputs()['identity'],
                extra_code=[dict(start=a,end=b,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],
                declared_controller=CTRL,declared_fine_finder=FINE,declared_coarse_finder=COARSE,independent_declared_pools=True,
                original_relocation_roots=True,original_file_API_or_allocator_executed=False,global_scratch=[SCRATCH,200],
                game_function_results_stubbed=False,OS_input_submitted=False,native_scene_or_world_frame=False)


def validate_query(c):
    need(set(c)=={'name','mode','start','goal','avoid','occupied'},'declared region query fields')
    need(isinstance(c['name'],str) and c['name'],'region query name')
    need(type(c['mode']) is int and 0<=c['mode']<4 and type(c['avoid']) is bool,'four graph modes/avoidance')
    need(isinstance(c['occupied'],list) and len({tuple(p) for p in c['occupied']})==len(c['occupied']),'unique occupancy')
    for p in [c['start'],c['goal']]+c['occupied']:
        need(isinstance(p,list) and len(p)==2 and all(type(v) is int for v in p) and 0<=p[0]<64 and 0<=p[1]<96,'real map query coordinates')


class RegionMachine(movement.MovementMachine):
    def __init__(self,c):
        validate_query(c);source_contract();self.case=c;self.w,self.h=64,96;self.pool_size=6144
        raw=SOURCE.read_bytes();self.uc=Uc(UC_ARCH_X86,UC_MODE_32);self.uc.mem_map(0x400000,(len(raw)+4095)&~4095)
        self.uc.mem_write(0x400000,raw);self.uc.mem_protect(0x400000,(len(raw)+4095)&~4095,UC_PROT_READ|UC_PROT_EXEC)
        self.uc.mem_protect(0x7A3000,0x2000,UC_PROT_READ|UC_PROT_WRITE)
        for at,n in REGIONS:
            if at!=0x7A3000:self.uc.mem_map(at,n)
        self.uc.mem_map(RETURN,0x1000)
        data=inputs();self.uc.mem_write(HEADER,data['logical']);self.uc.mem_write(TERR,data['terrain']);self.uc.mem_write(VPT,data['vpt'])
        self.put(MAP+0x2659C,HEADER);self.put(MAP+0x265A0,OCC_PTR);self.put(MAP+0x8C,TERR);self.put(OCC_PTR,OCC)
        for x,y in c['occupied']:self.put(OCC+(y*64+x)*2+1,1,'B')
        for obj,off,links,nodes,index in ((FINE,0x18,F_LINK,F_NODE,F_INDEX),(COARSE,0x10,C_LINK,C_NODE,C_INDEX)):
            self.put(obj+off+0x30,64);self.put(obj+off+0x34,96);self.put(obj+off+0x88,index)
            self.put(obj+off+0x7C,links)
            for i in range(6144):
                self.put(links+i*12,obj+off+0x78 if i==0 else links+(i-1)*12)
                self.put(links+i*12+4,links+(i+1)*12 if i+1<6144 else 0);self.put(links+i*12+8,nodes+i*28)
        self.put(FINE+0xB0,MAP);self.put(COARSE+0xA8,MAP)
        for i,o in enumerate(data['parsed']['offsets']):self.put(COARSE+0xB4+i*4,VPT+o)
        self.put(UNIT,1,'H');self.put(UNIT+0x258,RECORD);self.put(UNIT+0x44,ANIM);self.put(ANIM+0x48,-1,'h')
        self.put(RECORD+0x2E,999,'H');self.put(RECORD+0x30,c['mode'],'B')
        x,y=c['start'];gx,gy=c['goal'];self.put(UNIT+0x2EC,(x*32+16)*65536);self.put(UNIT+0x2F0,(y*16+8)*65536)
        self.put(UNIT+0x4D0,gx*32+16,'h');self.put(UNIT+0x4D2,gy*16+8,'h');self.uc.reg_write(UC_X86_REG_FPCW,0x27F)
        self.code_hash=hashlib.sha256();self.write_hash=hashlib.sha256();self.instructions=0;self.writes=0
        self.entries=Counter();self.coordinate_writes=0;self.popped={'fine':[],'coarse':[]};self.improved=0;self.reopened=0
        self.mutable=[(UNIT,UNIT+0x520),(COARSE,COARSE+0xD8),(FINE,FINE+0x100),(SCRATCH,SCRATCH+200),(PACKET,PACKET+0x100),(STACK,STACK+0x20000)]
        self.mutable += [(a,a+n) for a,n in REGIONS if a in (F_LINK,F_NODE,F_INDEX,C_LINK,C_NODE,C_INDEX)]
        self.mutable += [(VPT+o+24,VPT+o+24+len(r)*4) for o,r in zip(data['parsed']['offsets'][:4],data['parsed']['relative_records'])]
        self.uc.hook_add(UC_HOOK_CODE,self.code);self.uc.hook_add(UC_HOOK_MEM_WRITE,self.write_hook)

    base_call=types.FunctionType(path.PathMachine.call.__code__,dict(path.PathMachine.call.__globals__,ROOTS=ROOTS,STACK=STACK,RETURN=RETURN))
    snapshot=types.FunctionType(path.PathMachine.snapshot.__code__,dict(path.PathMachine.snapshot.__globals__,REGIONS=REGIONS))

    def code(self,uc,at,size,context):
        if at==RETURN:uc.emu_stop();return
        need(any(a<=at<b for a,b in RANGES),'undeclared original instruction '+hex(at))
        need(bytes(uc.mem_read(at,1))!=b'\xcc','original assertion/padding '+hex(at))
        self.instructions+=1;self.code_hash.update(struct.pack('<I',at))
        if at in ROOTS or at in (0x44ED40,0x44F1E0,0x4380B0,0x47DA30,0x47DEC0):self.entries[hex(at)]+=1
        if at==0x439C4F:
            link=uc.reg_read(UC_X86_REG_EAX);node=self.get(link+8);kind='coarse' if C_LINK<=link<C_LINK+0x12000 else 'fine'
            self.popped[kind].append([self.get(node+2,'h'),self.get(node+4,'h')])
        if at==0x427C90:self.improved+=1
        if at==0x427D20:self.reopened+=1

    def write_hook(self,uc,access,at,size,value,context):
        need(any(a<=at and at+size<=b for a,b in self.mutable),'forbidden original write '+hex(at))
        if at<UNIT+0x2F4 and at+size>UNIT+0x2EC:self.coordinate_writes+=1
        self.writes+=1;self.write_hash.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF))

    def lists_for(self,kind):
        obj,offset,links,nodes=(COARSE,0x10,C_LINK,C_NODE) if kind=='coarse' else (FINE,0x18,F_LINK,F_NODE)
        found=[]
        for delta in (0x44,0x50,0x78):
            head=obj+offset+delta;p=self.get(head+4);seen=[];unique=set()
            while p:
                need(p not in unique and links<=p<links+6144*12 and (p-links)%12==0,'own finite '+kind+' pool')
                if delta!=0x78:need(self.get(p)==(head if not seen else seen[-1]),'original pool prev link')
                need(self.get(p+8)==nodes+(p-links)//12*28,'matching pool node data')
                unique.add(p);seen.append(p);p=self.get(p+4)
            found.append(dict(head=head,links=seen))
        flat=[p for r in found for p in r['links']];need(len(flat)==len(set(flat))==6144,'exactly one pool owner per node')
        return found

    def relocate(self):return [self.call(0x44E5D0,(mode,),COARSE) for mode in range(4)]

    def common(self):
        return dict(final=self.snapshot(),ownership={k:self.lists_for(k) for k in ('coarse','fine')},popped=self.popped,
                    entries=dict(sorted(self.entries.items())),instructions=self.instructions,writes=self.writes,
                    improved=self.improved,reopened=self.reopened,original_coordinate_writes=self.coordinate_writes,
                    code_trace_sha256=self.code_hash.hexdigest(),write_trace_sha256=self.write_hash.hexdigest(),
                    game_function_results_stubbed=False,OS_input_submitted=False,host_unit_fields_changed_after_initialization=False)

    def query(self):
        c=self.case;initial=self.snapshot();roots=self.relocate();roots.append(self.call(0x44E9A0,(PACKET,),COARSE))
        call=self.call(0x44EA80,(*c['start'],*c['goal'],PACKET,c['mode'],int(c['avoid'])),COARSE)
        packet=bytes(self.uc.mem_read(PACKET,236)).hex()
        cleanup=[self.call(0x439C60,receiver=COARSE+0x10),self.call(0x439C60,receiver=FINE+0x18)]
        return dict(input=c,initial=initial,roots=roots,call=call,packet_hex=packet,cleanup=cleanup,**self.common())

    def route(self,c):
        initial=self.snapshot();roots=self.relocate()+[self.call(0x437C90,(UNIT+off,),FINE) for off in (0x2F4,0x3E0)]
        steps=[];stop='frame_budget'
        for i in range(c['frames']):
            before=self.unit();call=self.call(0x476680,(UNIT,0));after=self.unit();phase=self.get(UNIT+0x293,'B')
            steps.append(dict(index=i,before_hex=before,after_hex=after,call=call,phase=phase))
            if phase==8:stop='next_tile_blocked';break
            if before==after and phase in (0,3,4,5,6) and self.get(UNIT+0x4E0,'h')==0:stop='stationary_phase_'+str(phase);break
        cleanup=[self.call(0x439C60,receiver=COARSE+0x10),self.call(0x439C60,receiver=FINE+0x18)]
        return dict(input=c,initial=initial,roots=roots,steps=steps,stop=stop,cleanup=cleanup,**self.common())


def run_route(c):
    need(set(c)=={'name','start','goal','frames'} and type(c['frames']) is int and 1<=c['frames']<=1024,'declared route fields/budget')
    query=dict(name=c['name'],start=c['start'],goal=c['goal'],mode=0,avoid=False,occupied=[])
    return RegionMachine(query).route(c)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();need(not (ROOT/a.out).exists(),'fresh source output')
    queries=[];routes=[]
    for c in query_corpus():
        row=RegionMachine(c).query();queries.append(row);print('query',c['name'],row['call']['result'],len(row['popped']['coarse']),flush=True)
    for c in route_corpus():
        row=run_route(c);routes.append(row);print('route',c['name'],row['stop'],len(row['steps']),flush=True)
    path.save(a.out,dict(schema_version=1,source_contract=source_contract(),queries=queries,routes=routes,R3_complete=False,R4_complete=False,R6_complete=False))
