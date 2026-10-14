"""Actual world clock/map suffix; declared finite input probes restore all state."""
import argparse,hashlib,json,pickle,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP
from tools.school_world_mode_emulation import (
 WorldModeEmulator,architectural_cpu,cpu_digest,PARENT as ADMISSION,PARENT_SHA as ADMISSION_SHA,
 CHECKPOINTS,parent_evidence,read_deployment,read_opening,ROOT,UNITCTRL,STACK,RETURN,ExitEmulator,TACT,MAPCTRL,SOURCE_SHA256,report_text)
from tools.school_world_map import RANGES,source_contract,clock_step,pointer_outputs,project_map_frame,MAP_STATE_BASE,MAP_STATE_BYTES

PARENT=ROOT/'analysis/school-world-mode-native-v6-20261014.json'
PARENT_SHA='82c951060f3200d2780d6d4456e6c541fc76bb1eefa3f92e3bbd258838af15f3'
CLOCK_CASES=[(1,1,5,7,0),(0,0,5,7,0),(0,1,5,7,0),(0,1,1,0,0x7FFFFFFF),
             (0,1,0,0x7FFFFFFF,0x7FFFFFFF),(0,128,-0x80000000,0,0),(255,1,5,7,-1),(0,1,-5,0,0)]
MOUSE_CASES=[(0,0),(31,29),(31,30),(31,599),(31,600),(31,605),(31,606),(-1,30),(2048,30)]


class WorldMapEmulator(WorldModeEmulator):
    def __init__(self):
        self.map_loading=False
        super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.map_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.map_allowed):
            raise RuntimeError('world map forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.map_loading:return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
        if address==0x49B180:
            if self.map_kind!='actual' or (recv,ret)!=(UNITCTRL,0x46B4E8):raise RuntimeError('world map next natural caller')
            self.map_pending={'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'first_instruction_executed':False}
            uc.emu_stop();return
        expected={0x493630:(UNITCTRL,0x46B4D0),0x467B60:(UNITCTRL,0x46B4D8),0x46E9C0:(UNITCTRL,0x46B4E0),
                  0x43B350:(MAPCTRL,0x46E9EB),0x481610:(UNITCTRL,0x46E9F3)}
        if address in expected and self.map_kind=='actual':
            if (recv,ret)!=expected[address]:raise RuntimeError('world time/map actual child stack')
            self.map_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp})
        if address==0x467B60 and self.map_kind=='clock':
            if (recv,ret)!=(UNITCTRL,RETURN):raise RuntimeError('declared clock root caller')
        if address in (0x43B530,0x43B710) and self.map_kind=='mouse' and (recv,ret)!=(MAPCTRL,RETURN):
            raise RuntimeError('declared mouse root caller')
        if address==0x415040:
            if self.map_kind!='clock' or (recv,ret,self.read(sp+4))!=(self.read(0x7A49FC),0x467BD2,1):
                raise RuntimeError('original clock identity increment stack')
            self.map_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'args':[1]})
        if address==0x56CEC0:
            args=[self.read(sp+4),self.read(sp+8),self.read(sp+12)]
            if self.map_kind!='actual' or ret!=0x43D10C or args!=[self.clear_pointer,0,6144]:
                raise RuntimeError('original exact owned memset caller')
            self.map_calls.append({'va':hex(address),'return_va':hex(ret),'args':args,'original_body_executed':True})
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in RANGES) or 0x46B4D0<=address<0x46B4E8:
            self.map_visited.add(address);return
        raise RuntimeError('world map undeclared instruction '+hex(address))

    def map_regions(self):
        slots=[self.read(MAPCTRL+o) for o in (0xA0,0xA4,0xA8)]
        if not all(slots) or len(set(slots))!=3:raise RuntimeError('actual map three buffers')
        rows=[('map_slots',MAPCTRL+0xA0,12),('map_state',MAPCTRL+MAP_STATE_BASE,MAP_STATE_BYTES),
              ('fog_history',slots[0],6144),('fog_current',slots[1],6144),('fog_previous',slots[2],6144),
              ('minimap_globals',0x7A2960,32)]
        return [{'name':n,'pointer':p,'bytes':b,'hex':bytes(self.uc.mem_read(p,b)).hex()} for n,p,b in rows]

    def fixed_regions(self,regions):
        return [{**r,'hex':bytes(self.uc.mem_read(r['pointer'],r['bytes'])).hex()} for r in regions]

    def restore_probe(self,regions,cpu,stack,registers):
        for row in regions:self.uc.mem_write(row['pointer'],bytes.fromhex(row['hex']))
        self.uc.mem_write(STACK,stack);self.uc.context_restore(cpu)
        current=architectural_cpu(self.uc)
        if current!=registers or bytes(self.uc.mem_read(STACK,65536))!=stack or self.fixed_regions(regions)!=regions:
            raise RuntimeError('world map full probe restoration')
        return {'cpu_before_sha256':cpu_digest(registers),'cpu_after_sha256':cpu_digest(current),
                'stack_before_sha256':hashlib.sha256(stack).hexdigest(),'stack_after_sha256':hashlib.sha256(bytes(self.uc.mem_read(STACK,65536))).hexdigest(),
                'register_count':len(registers),'complete_owned_input_restored':True}

    def run_probes(self):
        clock=UNITCTRL+0x2E6F4;input_owner=self.read(0x7A49FC)
        if not input_owner:raise RuntimeError('original input owner')
        clock_regions=[{'name':n,'pointer':p,'bytes':b,'hex':bytes(self.uc.mem_read(p,b)).hex()} for n,p,b in
            [('clock',clock,24),('opening_gate',UNITCTRL+0x108B48,1),('event_gate',UNITCTRL+0x108B3A,1)]]
        mouse_regions=[{'name':n,'pointer':p,'bytes':b,'hex':bytes(self.uc.mem_read(p,b)).hex()} for n,p,b in
            [('mouse',input_owner+0x196C,8),('camera_and_outputs',MAPCTRL+0x265A6,12)]]
        regions=clock_regions+mouse_regions;cpu=self.uc.context_save();stack=bytes(self.uc.mem_read(STACK,65536));registers=architectural_cpu(self.uc)
        probe_allowed=[(r['pointer'],r['pointer']+r['bytes']) for r in regions]
        retained=self.capture_scene_memory(probe_allowed);prior=self._function_ranges;self._function_ranges=prior+RANGES
        self.map_loading=True;self.map_allowed=[(STACK,STACK+65536)]+probe_allowed;clocks=[];mice=[]
        try:
            for opening,event,remaining,elapsed,limit in CLOCK_CASES:
                self.map_kind='clock';self.map_calls=[];self.map_visited=set()
                self.uc.mem_write(clock,struct.pack('<3i',remaining,elapsed,limit));self.write(UNITCTRL+0x108B48,opening,'B');self.write(UNITCTRL+0x108B3A,event,'B')
                before=self.fixed_regions(clock_regions);value=self.call(0x467B60,receiver=UNITCTRL);after=self.fixed_regions(clock_regions)
                expected=clock_step(opening,event,remaining,elapsed,limit)
                words=list(struct.unpack('<3i',bytes.fromhex(after[0]['hex'])[:12]))
                if words!=[expected[k] for k in ('remaining','elapsed','limit')] or value!=expected['return_eax']:
                    raise RuntimeError('original clock source arithmetic')
                if bool(self.map_calls)!=expected['increment_called']:raise RuntimeError('original clock source gate')
                result={'declared_input':[opening,event,remaining,elapsed,limit],'before':before,'after':after,'return_eax':value,
                        'calls':deepcopy(self.map_calls),'visited':sorted(self.map_visited),**self.verify_scene_memory(retained)}
                result['restoration']=self.restore_probe(regions,cpu,stack,registers);clocks.append(result)
            for x,y in MOUSE_CASES:
                self.map_kind='mouse';self.map_calls=[];self.map_visited=set()
                self.uc.mem_write(input_owner+0x196C,struct.pack('<2i',x,y));before=self.fixed_regions(mouse_regions)
                self.call(0x43B530,receiver=MAPCTRL);self.call(0x43B710,receiver=MAPCTRL)
                after=self.fixed_regions(mouse_regions);coords=list(struct.unpack('<4h',bytes.fromhex(after[1]['hex'])[4:12]))
                camera=struct.unpack('<2h',bytes.fromhex(before[1]['hex'])[:4]);expected=pointer_outputs((x,y),camera)
                if coords!=expected['tile']+expected['pixel']:raise RuntimeError('original pointer source boundaries')
                result={'declared_mouse':[x,y],'before':before,'after':after,'outputs':expected,'visited':sorted(self.map_visited),**self.verify_scene_memory(retained)}
                result['restoration']=self.restore_probe(regions,cpu,stack,registers);mice.append(result)
            return {'clock':clocks,'mouse':mice,'live_input_captured':False}
        finally:
            self.restore_probe(regions,cpu,stack,registers);self.map_loading=False;self._function_ranges=prior

    def run_map_suffix(self):
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x493630 or self.read(UNITCTRL+0x108B48,'B')!=1 or self.read(UNITCTRL+0x108B3A,'B')!=0:
            raise RuntimeError('actual pending map/time suffix')
        if self.read(UNITCTRL+0x2F156,'B')!=0 or self.read(UNITCTRL+0x2F15B,'B')!=0:raise RuntimeError('actual selection input mode')
        before=self.map_regions();clock=bytes(self.uc.mem_read(UNITCTRL+0x2E6F4,24));mode=self.mode_regions();self.clear_pointer=before[4]['pointer']
        input_owner=self.read(0x7A49FC);mouse=[self.read(input_owner+0x196C,'i'),self.read(input_owner+0x1970,'i')]
        self.map_allowed=[(STACK,STACK+65536),(MAPCTRL+0xA4,MAPCTRL+0xAC),(MAPCTRL+0x265AA,MAPCTRL+0x265B2),
            (MAPCTRL+0x265D8,MAPCTRL+0x265DC),(MAPCTRL+0x265E0,MAPCTRL+0x265F0),(self.clear_pointer,self.clear_pointer+6144),(0x7A2960,0x7A2980)]
        retained=self.capture_scene_memory(self.map_allowed);prior=self._function_ranges;self._function_ranges=prior+RANGES+((0x46B4D0,0x46B4E8),)
        self.map_loading=True;self.map_kind='actual';self.map_calls=[];self.map_visited=set();self.map_pending=None
        try:
            self.uc.emu_start(0x493630,RETURN,timeout=2_000_000,count=100000)
            after=self.fixed_regions(before)
            if self.map_pending is None or self.uc.reg_read(UC_X86_REG_EIP)!=0x49B180:raise RuntimeError('actual next map suffix boundary')
            if after!=project_map_frame(before,mouse) or bytes(self.uc.mem_read(UNITCTRL+0x2E6F4,24))!=clock or self.mode_regions()!=mode:
                raise RuntimeError('actual full source map/frame and unchanged clock/mode')
            return {'before':before,'after':after,'mouse':mouse,'clock_before_hex':clock.hex(),'clock_after_hex':bytes(self.uc.mem_read(UNITCTRL+0x2E6F4,24)).hex(),
                'mode_before':mode,'mode_after':self.mode_regions(),'calls':deepcopy(self.map_calls),'visited':sorted(self.map_visited),'pending':self.map_pending,
                'original_memset_body_executed':True,'full_world_tick_executed':False,'AI_or_waves_executed':False,'live_input_captured':False,
                **self.verify_scene_memory(retained)}
        finally:self.map_loading=False;self._function_ranges=prior


def report():
    def pinned(p,sha):
        raw=p.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('world map pinned parent '+p.name)
        return json.loads(raw)
    parent=pinned(PARENT,PARENT_SHA);admission=pinned(ADMISSION,ADMISSION_SHA)
    placement=parent_evidence();deployment=read_deployment();opening=read_opening();cases=[]
    for index,(name,sha) in enumerate(CHECKPOINTS):
        raw=(ROOT/f'.venv-audit/formation-actual-checkpoint-{index}.pkl').read_bytes()
        if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('world map checkpoint identity')
        payload=pickle.loads(raw)
        if payload['source_sha']!=SOURCE_SHA256 or payload['evidence_kind']!='private_actual_cpu_after_full35_before_placement':raise ValueError('world map provenance')
        e=WorldMapEmulator();e.__dict__.update({k:v for k,v in payload['state'].items() if not k.startswith('_audit_') and k!='uc'})
        for at,data in payload['memory']:e.uc.mem_write(at,data)
        e.uc.context_restore(payload['cpu'])
        if e.run_placement()!=placement['cases'][index]['formation_placement']:raise ValueError('world map parent placement')
        original_start=e.uc.emu_start
        def start(begin,until,**kwargs):
            if begin==0x468A49:kwargs['timeout']=60_000_000
            return original_start(begin,until,**kwargs)
        e.uc.emu_start=start
        try:tail=e.run_deployment_tail()
        finally:e.uc.emu_start=original_start
        if tail!=deployment['cases'][index]['deployment_tail']:raise ValueError('world map parent deployment')
        if e.run_initialization_and_opening()!=opening['cases'][index]['scene_opening']:raise ValueError('world map parent opening')
        if e.audit_world_entry()!=admission['cases'][index]['world_admission']:raise ValueError('world map parent admission')
        mode_probes=e.run_mode_probes();prefix=e.run_actual_prefix()
        # The old immutable JSON represents descriptor/FP register tuples as
        # arrays. Compare the same published representation, without dropping fields.
        if json.loads(json.dumps(mode_probes))!=parent['cases'][index]['declared_mode_probes'] or prefix!=parent['cases'][index]['actual_world_prefix']:
            raise ValueError('world map complete mode parent')
        probes=e.run_probes();suffix=e.run_map_suffix()
        cases.append({'name':name,'checkpoint_sha256':sha,'complete_parent_equality':True,'declared_probes':probes,'actual_map_suffix':suffix})
        print(name+': original clock/map suffix and memset; 8 clock + 9 mouse probes restored',flush=True)
    return {'schema_version':1,'source_contract':source_contract(),'parent_sha256':PARENT_SHA,'parent_report':PARENT.relative_to(ROOT).as_posix(),
        'cases':cases,'world_tick_completed':False,'original_opening_completed':False,'persistent_write_authority':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('use a new immutable report path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
