"""Execute original nearest-free selection and occupied-destination rerouting."""
import argparse
import json
import struct
import types
from capstone import Cs,CS_ARCH_X86,CS_MODE_32
from unicorn.x86_const import UC_X86_REG_ESP,UC_X86_REG_ECX,UC_X86_REG_EIP,UC_X86_REG_EAX
from tools import battle_route_admission_emulation as previous
from tools import battle_pathfinding_emulation as path
from tools.battle_nearest_free import selection_corpus,movement_corpus

ROOT,SOURCE,need,sha=previous.ROOT,previous.SOURCE,previous.need,previous.sha
CTRL,UNIT,RECORD,FINDER=previous.CTRL,previous.UNIT,previous.RECORD,previous.FINDER
MAP=CTRL+0x3D68
TABLE,DIST=0x11400000,0x11500000
REGIONS=previous.REGIONS+((TABLE,0x7000),(DIST,0x3000))
EXTRA_RANGES=((0x43B110,0x43B245),(0x43BE60,0x43BFA0),(0x43D4E0,0x43D970),(0x468D80,0x468E10))
RANGES=previous.RANGES+EXTRA_RANGES
ROOTS=previous.ROOTS|{0x43B110,0x43D660,0x43D4E0,0x43D530,0x43D5B0,0x470840,0x4709D0}
FLOOD_INSTRUCTIONS=frozenset(i.address for a,b in ((0x43B110,0x43B245),(0x56CE80,0x56CE83))
    for i in Cs(CS_ARCH_X86,CS_MODE_32).disasm(SOURCE.read_bytes()[a-0x400000:b-0x400000],a) if i.mnemonic!='int3')


def declared_table():
    """43AB10-derived initialization INPUT, not execution of its allocator/body."""
    points=[[x,y,abs(x)+abs(y),0] for y in range(-32,33) for x in range(-32,33)]
    for distance in range(65):
        rank=0
        for point in reversed(points):
            if point[2]==distance:point[3]=((distance*256)+rank)&65535;rank+=1
    for p in points:
        if p[0]%2!=p[1]%2 and abs(p[0])<7 and abs(p[1])<7:p[3]=(p[3]-32768)&65535
    # Same exchange comparison as source; deliberately separate from oracle sort.
    for i in range(len(points)-1):
        for j in range(i+1,len(points)):
            if points[j][3]<points[i][3]:points[i],points[j]=points[j],points[i]
    return b''.join(struct.pack('<bbHH',x,y,d,i) for i,(x,y,d,_) in enumerate(points))


def source_contract():
    raw=SOURCE.read_bytes()
    return dict(parent=previous.source_contract(),extra_code=[dict(start=a,end=b,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],
                table_builder_reference=dict(start=0x43AB10,end=0x43B110,sha256=sha(raw[0x3AB10:0x3B110]),executed=False),
                table_input='derived 65x65 table, not original allocator/constructor output',table_pointer=TABLE,
                view_table=dict(pointer=0x59558C,hex=raw[0x19558C:0x19558C+66].hex()),
                original_flood_root=0x43B110,full_original_constructor_executed=False,native_scene_or_world_frame=False)


def validate_selection(c):
    need(set(c)=={'name','grid','occupied','mode','seed','view','counter','reservations','calls','reset'},'declared selection fields')
    p=dict(name=c['name'],kind='search',direction=0,grid=c['grid'],occupied=c['occupied'],start=[0,0],goal=[0,0],mode=min(c['mode'],3),avoid=False)
    path.validate_case(p)
    need(type(c['mode']) is int and 0<=c['mode']<=4,'source selection mode')
    need(type(c['view']) is int and 0<=c['view']<=32,'source view 0..32')
    need(type(c['counter']) is int and 0<=c['counter']<=4,'declared rotation counter')
    need(type(c['calls']) is int and 1<=c['calls']<=40,'declared bounded selection calls')
    need(type(c['reset']) is bool and len(c['reservations'])<=40,'declared reservation capacity')
    need(len(c['seed'])==2 and all(type(v) is int and -32<=v<=64 for v in c['seed']),'declared seed')
    need(all(len(p)==2 and all(type(v) is int and -32768<=v<=32767 for v in p) for p in c['reservations']),'declared reservation points')


class NearestMachine(previous.AdmissionMachine):
    def __init__(self,c,table=None):
        base=dict(c);faction=base.pop('faction',0);need(type(faction) is int and faction in (0,4),'declared faction gate')
        super().__init__(base);self.route_input=c;self.put(RECORD+0xA4,faction,'B')
        for at,n in REGIONS[len(previous.REGIONS):]:self.uc.mem_map(at,n)
        self.uc.mem_write(TABLE,declared_table() if table is None else table)
        self.put(MAP+0x263B8,TABLE);self.put(MAP+0x263C0,65,'h');self.put(MAP+0x263C2,65,'h')
        gx,gy=c['movement']['path']['goal'];self.put(UNIT+0x4CC,gx*32+16,'h');self.put(UNIT+0x4CE,gy*16+8,'h')

    path_code=types.FunctionType(path.PathMachine.code.__code__,dict(path.PathMachine.code.__globals__,RANGES=RANGES))
    base_call=types.FunctionType(path.PathMachine.call.__code__,dict(path.PathMachine.call.__globals__,ROOTS=ROOTS))
    snapshot=types.FunctionType(path.PathMachine.snapshot.__code__,dict(path.PathMachine.snapshot.__globals__,REGIONS=REGIONS))

    def code(self,uc,at,size,context):
        if getattr(self,'flood_active',False):
            if at==path.RETURN:uc.emu_stop();return
            need(at in FLOOD_INSTRUCTIONS,'undeclared original flood instruction '+hex(at))
            self.instructions+=1;self.code_hash.update(struct.pack('<I',at));return
        super().code(uc,at,size,context)
        if at in (0x43B110,0x43BE60,0x43D4E0,0x43D530,0x43D5B0,0x43D660,0x470840,0x4709D0,0x468D80):
            self.entries[hex(at)]=self.entries.get(hex(at),0)+1

    def write_hook(self,uc,access,at,size,value,context):
        allowed=((MAP+0x263C4,MAP+0x263C6),(MAP+0x263C8,MAP+0x2646C),(DIST,DIST+0x3000),(path.STACK,path.STACK+0x10000))
        if any(a<=at and at+size<=b for a,b in allowed):
            self.writes+=1;self.write_hash.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF));return
        super().write_hook(uc,access,at,size,value,context)

    def reservation_state(self):
        n=self.get(MAP+0x263C8);need(n<=40,'bounded original reservation count')
        return dict(counter=self.get(MAP+0x263C4,'h'),points=[[self.get(MAP+0x263CC+i*4,'h'),self.get(MAP+0x263CE+i*4,'h')] for i in range(n)],
                    work_hex=bytes(self.uc.mem_read(MAP+0x263C8,0xA4)).hex())


def selection(c,table=None):
    validate_selection(c)
    p=dict(name=c['name'],kind='search',direction=0,grid=c['grid'],occupied=[],start=[0,0],goal=[0,0],mode=0,avoid=False)
    movement=dict(name=c['name'],path=p,speed=999,terrain_rate=100,status=0,frames=1,blocker_speed=0)
    declaration=dict(movement=movement,initial_phase=4,retry=0,cooldown=0,movement_type=0,unit_kind=0,ai_mode=0)
    m=NearestMachine(declaration,table);m.put(MAP+0x263C4,c['counter'],'h')
    for x,y in c['occupied']:m.put(path.OCC+1+(y*len(c['grid'][0])+x)*2,1,'B')
    # Selection mode0 only needs nonzero terrain values; movement-specific rates
    # remain 100, equivalent to the declared parent table for this predicate.
    for i,pair in enumerate(c['reservations']):
        m.put(MAP+0x263CC+i*4,pair[0],'h');m.put(MAP+0x263CE+i*4,pair[1],'h')
    m.put(MAP+0x263C8,len(c['reservations']));initial=m.snapshot();calls=[]
    if c['reset']:calls.append(dict(kind='reset',call=m.call(0x43D4E0,receiver=MAP),state=m.reservation_state()))
    for i in range(c['calls']):
        # Declared output sentinels are caller arguments, never selected results.
        m.put(path.PACKET+0xF0,0xA55A,'H');m.put(path.PACKET+0xF2,0x5AA5,'H')
        call=m.call(0x43D660,(*c['seed'],c['view'],c['mode'],path.PACKET+0xF0,path.PACKET+0xF2),MAP)
        calls.append(dict(kind='select',call=call,output=[m.get(path.PACKET+0xF0,'H'),m.get(path.PACKET+0xF2,'H')],state=m.reservation_state()))
    return dict(input=c,initial=initial,final=m.snapshot(),calls=calls,instructions=m.instructions,writes=m.writes,
                code_trace_sha256=m.code_hash.hexdigest(),write_trace_sha256=m.write_hash.hexdigest(),entries=m.entries,
                OS_input_submitted=False,game_function_results_stubbed=False)


def flood(table=None):
    m=NearestMachine(movement_corpus()[0],table);initial=m.snapshot()
    # This recursive root is much longer than one selection. Resume only the
    # actual EIP/CPU after each host budget; never restart or synthesize a return.
    args=(DIST,65,65,32,32,64);sp=path.STACK+0xF000;before=m.cpu();m.put(sp,path.RETURN)
    for i,arg in enumerate(args):m.put(sp+4+i*4,arg)
    m.uc.reg_write(UC_X86_REG_ESP,sp);m.uc.reg_write(UC_X86_REG_ECX,MAP);m.flood_active=True
    entry=0x43B110;chunks=[]
    for _ in range(100):
        count=m.instructions;m.uc.emu_start(entry,path.RETURN,timeout=0,count=1_000_000)
        entry=m.uc.reg_read(UC_X86_REG_EIP);chunks.append(dict(instructions=m.instructions-count,next_EIP=entry))
        if entry==path.RETURN:break
    need(entry==path.RETURN,'original recursive flood budget exhausted');after=m.cpu()
    call=dict(entry=0x43B110,receiver=MAP,args=list(args),result=m.uc.reg_read(UC_X86_REG_EAX),ESP_before=sp,ESP_after=after['ESP'],
              instructions=m.instructions,cpu_before=before,cpu_after=after)
    return dict(initial=initial,final=m.snapshot(),call=call,distances_hex=bytes(m.uc.mem_read(DIST,65*65*2)).hex(),
                instructions=m.instructions,writes=m.writes,code_trace_sha256=m.code_hash.hexdigest(),write_trace_sha256=m.write_hash.hexdigest(),
                budget_chunks=chunks)


def report():
    table=declared_table();rows=[]
    for c in selection_corpus():
        row=selection(c,table);rows.append(row);print('selection',c['name'],row['calls'][-1]['output'],flush=True)
    routes=[]
    for c in movement_corpus():
        row=NearestMachine(c,table).run();routes.append(row);print('route',c['movement']['name'],row['stop'],len(row['steps']),flush=True)
    distance=flood(table);print('flood',distance['instructions'],flush=True)
    return dict(schema_version=1,source_contract=source_contract(),declared_table_hex=table.hex(),selection=rows,routes=routes,flood=distance,
                R3_complete=False,R4_complete=False,R6_complete=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args()
    need(not (ROOT/a.out).exists(),'fresh immutable source report');path.save(a.out,report())
