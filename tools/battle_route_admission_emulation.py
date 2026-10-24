"""Original primary/local route admission, handoff, incremental search and movement."""
import argparse
import json
import struct
import types
from tools import battle_unit_movement_emulation as previous
from tools import battle_pathfinding_emulation as path

ROOT,SOURCE,need,sha=previous.ROOT,previous.SOURCE,previous.need,previous.sha
CTRL,UNIT,RECORD=previous.CTRL,previous.UNIT,previous.RECORD
FINDER=CTRL+0x2A634
REGIONS=previous.REGIONS
EXTRA_RANGES=((0x437D10,0x437E40),(0x438D00,0x438F70),(0x47D190,0x47D930))
RANGES=previous.RANGES+EXTRA_RANGES
ROOTS=previous.ROOTS|{0x47D210,0x47D570,0x47D730,0x47D830,0x47D190}


def source_contract():
    raw=SOURCE.read_bytes()
    return dict(parent=previous.source_contract(),extra_code=[dict(start=a,end=b,sha256=sha(raw[a-0x400000:b-0x400000])) for a,b in EXTRA_RANGES],
                declared_embedded_finder=FINDER,primary_packet=UNIT+0x2F4,secondary_packet=UNIT+0x3E0,
                initial_search_results_supplied=False,original_roots_per_step=1,far_region_graph_supported=False)


def validate(c):
    need(set(c)=={'movement','initial_phase','retry','cooldown','movement_type','unit_kind','ai_mode'},'declared admission fields')
    previous.validate(c['movement'])
    need(type(c['initial_phase']) is int and c['initial_phase'] in (0,1,4,5),'source initial admission phase')
    need(type(c['retry']) is int and -128<=c['retry']<=127,'signed retry byte')
    need(type(c['cooldown']) is int and 0<=c['cooldown']<=5,'declared cooldown')
    need(type(c['movement_type']) is int and c['movement_type'] in (0,4),'declared movement type')
    need(type(c['unit_kind']) is int and c['unit_kind'] in (0,1),'declared unit kind flag')
    need(type(c['ai_mode']) is int and c['ai_mode'] in (0,2,3),'declared AI mode')


class AdmissionMachine(previous.MovementMachine):
    def __init__(self,c):
        validate(c);super().__init__(c['movement']);self.route_input=c
        self.uc.mem_write(FINDER,bytes(self.uc.mem_read(path.OBJECT,0x100)))
        self.put(FINDER+0xB0,CTRL+0x3D68);self.put(path.LINKS,FINDER+0x90)
        self.put(path.OBJECT+0x94,0)  # Inactive parent descriptor is not a second owner.
        self.put(UNIT+0x293,c['initial_phase'],'B');self.put(UNIT+0x4E4,c['retry'],'b');self.put(UNIT+0x4E0,c['cooldown'],'h')
        self.put(UNIT+0x2A7,c['unit_kind'],'B');self.put(RECORD+0x9F,c['ai_mode'],'B');self.put(RECORD+0x30,c['movement_type'],'B')

    path_code=types.FunctionType(path.PathMachine.code.__code__,dict(path.PathMachine.code.__globals__,RANGES=RANGES))
    base_call=types.FunctionType(path.PathMachine.call.__code__,dict(path.PathMachine.call.__globals__,ROOTS=ROOTS))
    lists=types.FunctionType(path.PathMachine.lists.__code__,dict(path.PathMachine.lists.__globals__,OBJECT=FINDER))

    def code(self,uc,at,size,context):
        super().code(uc,at,size,context)
        if at in (0x47D210,0x47D570,0x47D730,0x47D830,0x47D190,0x438AD0,0x438D00,0x437D10,0x437D90,0x4380B0):
            self.entries[hex(at)]=self.entries.get(hex(at),0)+1

    def write_hook(self,uc,access,at,size,value,context):
        if FINDER<=at and at+size<=FINDER+0x100:
            self.writes+=1;self.write_hash.update(struct.pack('<IIQ',at,size,value&0xFFFFFFFFFFFFFFFF));return
        super().write_hook(uc,access,at,size,value,context)

    def run(self):
        c=self.route_input;initial=self.snapshot()
        roots=[self.call(0x437C90,(UNIT+off,),FINDER) for off in (0x2F4,0x3E0)]
        steps=[];stop='frame_budget'
        for i in range(c['movement']['frames']):
            before=self.unit();call=self.call(0x476680,(UNIT,0));after=self.unit();phase=self.get(UNIT+0x293,'B')
            steps.append(dict(index=i,before_hex=before,after_hex=after,calls=[call],phase=phase))
            if phase==8:stop='next_tile_blocked';break
            if phase==3 and self.get(UNIT+0x314,'H')==0:stop='secondary_only_arrived';break
            if before==after and phase in (0,3,4,5,6) and self.get(UNIT+0x4E0,'h')==0:
                stop='stationary_phase_'+str(phase);break
        cleanup=self.call(0x439C60,receiver=FINDER+0x18)
        return dict(input=c,initial=initial,final=self.snapshot(),roots=roots,steps=steps,stop=stop,cleanup=cleanup,
                    final_ownership=self.lists(),search_popped=self.popped,entries=dict(sorted(self.entries.items())),
                    instructions=self.instructions,writes=self.writes,code_trace_sha256=self.code_hash.hexdigest(),write_trace_sha256=self.write_hash.hexdigest(),
                    original_coordinate_write_count=self.coordinate_writes,host_unit_fields_changed_after_initialization=False,
                    game_or_math_results_stubbed=False,OS_input_submitted=False)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args()
    from tools.battle_route_admission import corpus
    need(not (ROOT/a.out).exists(),'fresh immutable admission output');cases=[]
    for c in corpus():
        row=AdmissionMachine(c).run();cases.append(row);print(c['movement']['name'],row['stop'],len(row['steps']),flush=True)
    path.save(a.out,dict(schema_version=1,source_contract=source_contract(),cases=cases,R3_complete=False,R4_complete=False,R6_complete=False))
