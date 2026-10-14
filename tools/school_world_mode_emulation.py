"""Natural world mode return and first nested entry update on actual school CPU.

Mode probes bind request bytes explicitly and restore all state. No complete
world tick, original opening completion, AI, waves or settlement is inferred.
"""
import argparse
import hashlib
import json
import pickle
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP, UC_X86_REG_ECX, UC_X86_REG_ESP
from unicorn import x86_const
from tools.school_world_admission import WorldAdmission, START, END, GLOBAL
from tools.school_world_mode import RANGES, source_contract, project, first_entry_update, admitted_request
from tools.school_entry_control_emulation import MAPCTRL, CONTROL, NATIVE as ENTRY_NATIVE, REGIONS as ENTRY_REGIONS, read_opening
from tools.school_scene_opening_emulation import read_deployment
from tools.school_deployment_tail_emulation import CHECKPOINTS,parent_evidence,ROOT,SOURCE_SHA256,UNITCTRL,STACK,RETURN,ExitEmulator
from tools.school_tactical_startup_emulation import TACT
from tools.tactics_exit_emulation import report_text

PARENT = ROOT/'analysis/school-night-world-admission-v2-20261014.json'
PARENT_SHA = 'f3c467f81c379a7998a1c11f343f6ee7fde5fc913a805e4b2741aa60b3d69c73'
PROBES = [(-1,0),(1,0),(1,1),(1,128),(2,0),(2,1),(2,255)]


def architectural_cpu(context):
    # UcContext raw buffers also contain host/internal cache fields; these are
    # not architectural register values and are not a valid equality oracle.
    names=('EAX EBX ECX EDX EBP ESP ESI EDI EIP EFLAGS CS DS ES FS GS SS '
           'CR0 CR2 CR3 CR4 DR0 DR1 DR2 DR3 DR6 DR7 FPCW FPSW FPTAG MXCSR '
           'GDTR IDTR LDTR TR').split()
    names += ['FP'+str(i) for i in range(8)]+['XMM'+str(i) for i in range(8)]
    return {name:context.reg_read(getattr(x86_const,'UC_X86_REG_'+name)) for name in names}


def cpu_digest(registers):
    return hashlib.sha256(json.dumps(registers,sort_keys=True,separators=(',',':')).encode('ascii')).hexdigest()


class WorldModeEmulator(WorldAdmission):
    def __init__(self):
        self.flow_loading=False
        super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.flow_loading: return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.flow_allowed):
            raise RuntimeError('world mode forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.flow_loading: return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
        if address==0x493630:
            if self.flow_kind!='actual' or (recv,ret)!=(UNITCTRL,0x46B4D0): raise RuntimeError('world next natural call')
            self.pending={'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'first_instruction_executed':False}
            uc.emu_stop();return
        if address==0x4678C0:
            if recv!=UNITCTRL or ret!=(0x46B4B2 if self.flow_kind=='actual' else RETURN): raise RuntimeError('world mode root caller')
        if address==0x46B4B2:
            if self.flow_kind!='actual' or sp!=self.root_sp+4: raise RuntimeError('world mode natural return stack')
            self.calls.append({'va':hex(address),'kind':'mode_natural_return','sp':sp})
        if address==0x499DA0:
            if self.flow_kind!='actual' or (recv,ret)!=(UNITCTRL,0x46B4C8) or self.read(CONTROL+12,'B')!=0:
                raise RuntimeError('world actual nested controller caller')
            self.entry_before=self.entry_regions()
            self.calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp})
        if address==0x46B4C8:
            if self.flow_kind!='actual' or not hasattr(self,'entry_before'): raise RuntimeError('world nested entry return')
            self.entry_after=self.entry_regions()
            if first_entry_update(self.entry_before)!=self.entry_after: raise RuntimeError('world complete first entry bytes')
            self.calls.append({'va':hex(address),'kind':'entry_natural_return','sp':sp})
        if address in (0x43B400,0x43B460):
            expected=(0x499E3D,[304,264]) if address==0x43B400 else (0x43B444,[-208,-21])
            args=[self.read(sp+4,'i'),self.read(sp+8,'i')]
            if self.flow_kind!='actual' or recv!=MAPCTRL or (ret,args)!=expected: raise RuntimeError('world native camera call')
            self.calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'args':args})
        if address in (0x43B250,0x455160,0x4553E0,0x4558A0,0x455D00):
            if self.flow_kind!='probe': raise RuntimeError('actual idle mode unexpectedly invokes stores')
            kind,flag=self.probe_request
            on=kind==1 and flag!=0
            returns={0x43B250:0x467930 if on else 0x46798E if kind==1 else 0x4679FD,
                0x455160:0x467940 if on else 0x46799E if kind==1 else 0x467A0D,
                0x4553E0:0x455189,0x4558A0:0x455195,0x455D00:0x4551A1}
            argument=0 if on else 1 if address==0x43B250 else 0
            if address!=0x43B250: argument=1 if on else 0
            receiver=MAPCTRL if address==0x43B250 else TACT
            if (recv,ret,self.read(sp+4))!=(receiver,returns[address],argument): raise RuntimeError('mode actual source leaf stack')
            self.calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'args':[argument]})
        if address==0x56CE80: return ExitEmulator._hook(self,uc,address,size,context)
        ranges=RANGES+((START,END),)+ENTRY_NATIVE
        if any(a<=address<b for a,b in ranges): self.flow_visited.add(address);return
        raise RuntimeError('world mode undeclared instruction '+hex(address))

    def mode_regions(self):
        owner=self.read(TACT+0x60)
        if not owner: raise RuntimeError('world task flags owner')
        rows=[('control',UNITCTRL+0x108B30,50),('map_flags',MAPCTRL+0x26595,4),('task_flags',owner+0x20E8,329)]
        return [{'name':name,'pointer':at,'bytes':n,'hex':bytes(self.uc.mem_read(at,n)).hex()} for name,at,n in rows]

    def entry_regions(self):
        return [{'pointer':at,'bytes':n,'hex':bytes(self.uc.mem_read(at,n)).hex()} for at,n in ENTRY_REGIONS]

    def mode_allowed(self):
        owner=self.read(TACT+0x60)
        return [(UNITCTRL+o,UNITCTRL+o+1) for o in (0x108B34,0x108B35,0x108B36,0x108B38,0x108B39,0x108B3A,0x108B3B,0x108B3C)]+[
            (MAPCTRL+0x26595,MAPCTRL+0x26599)]+[(owner+o,owner+o+1) for o in (0x20E8,0x216C,0x2230)]

    def run_mode_probes(self):
        original=self.mode_regions();cpu=self.uc.context_save();stack=bytes(self.uc.mem_read(STACK,65536))
        # Compare both sides through the live x86 API. UcContext's generic read
        # API lacks x86 structure decoding for descriptor/80-bit FP registers.
        cpu_before=architectural_cpu(self.uc)
        retained=self.capture_scene_memory([(STACK,STACK+65536)]+self.mode_allowed())
        results=[];prior=self._function_ranges
        self.flow_allowed=[(STACK,STACK+65536)]+self.mode_allowed()
        self._function_ranges=prior+RANGES;self.flow_loading=True;self.flow_kind='probe'
        try:
            for kind,flag in PROBES:
                request=admitted_request(kind,flag)
                self.uc.mem_write(UNITCTRL+0x108B3B,bytes(request));before=self.mode_regions()
                self.probe_request=request;self.calls=[];self.flow_visited=set()
                self.call(0x4678C0,receiver=UNITCTRL)
                after=self.mode_regions()
                if after!=project(before,kind,flag): raise RuntimeError('world source complete mode region disagreement')
                if self.uc.reg_read(UC_X86_REG_EIP)!=RETURN or self.uc.reg_read(UC_X86_REG_ESP)!=STACK+0xFF04:
                    raise RuntimeError('world mode natural probe root return')
                result={'declared_request':[kind,flag],'before':before,'after':after,'calls':deepcopy(self.calls),
                    'visited':sorted(self.flow_visited),'return_sp':self.uc.reg_read(UC_X86_REG_ESP),**self.verify_scene_memory(retained)}
                for row in original:self.uc.mem_write(row['pointer'],bytes.fromhex(row['hex']))
                self.uc.mem_write(STACK,stack);self.uc.context_restore(cpu)
                if self.mode_regions()!=original: raise RuntimeError('world probe exact restoration')
                restored_stack=bytes(self.uc.mem_read(STACK,65536))
                restored_cpu=architectural_cpu(self.uc)
                if restored_stack!=stack or restored_cpu!=cpu_before:raise RuntimeError('world probe architectural CPU/stack restoration')
                result['restoration']={'stack_before_sha256':hashlib.sha256(stack).hexdigest(),
                    'stack_after_sha256':hashlib.sha256(restored_stack).hexdigest(),
                    'cpu_before_sha256':cpu_digest(cpu_before),'cpu_after_sha256':cpu_digest(restored_cpu),
                    'cpu_registers_before':cpu_before,'cpu_registers_after':restored_cpu,
                    'cpu_equality_scope':'50 x86 register values through live API; full saved context restored, host cache bytes and unsupported GS_BASE excluded'}
                result['captured_parent_restored']=True;results.append(result)
            return results
        finally:
            for row in original:self.uc.mem_write(row['pointer'],bytes.fromhex(row['hex']))
            self.uc.mem_write(STACK,stack);self.uc.context_restore(cpu)
            self.flow_loading=False;self._function_ranges=prior

    def run_actual_prefix(self):
        if (self.uc.reg_read(UC_X86_REG_EIP),self.read(UNITCTRL+0x108B3B,'b'))!=(0x4678C0,-1):
            raise RuntimeError('world actual pending child/idle state')
        self.root_sp=self.uc.reg_read(UC_X86_REG_ESP)
        before=self.mode_regions();self.calls=[];self.flow_visited=set();self.pending=None
        self.flow_allowed=[(STACK,STACK+65536),(CONTROL+12,CONTROL+13),(MAPCTRL+0x265A6,MAPCTRL+0x265AA)]
        retained=self.capture_scene_memory(self.flow_allowed)
        prior=self._function_ranges;self._function_ranges=prior+RANGES+ENTRY_NATIVE+((START,END),)
        self.flow_loading=True;self.flow_kind='actual'
        try:
            self.uc.emu_start(0x4678C0,RETURN,timeout=1_000_000,count=20000)
            if self.pending is None or self.uc.reg_read(UC_X86_REG_EIP)!=0x493630: raise RuntimeError('world next untouched boundary')
            after=self.mode_regions();expected=project(before,-1,0)
            # The next controller alone changes its state byte from0 to4.
            data=bytearray.fromhex(expected[0]['hex']);data[26]=4;expected[0]['hex']=data.hex()
            if after!=expected: raise RuntimeError('world complete mode retention after nested entry')
            return {'before':before,'after':after,'entry_before':self.entry_before,'entry_after':self.entry_after,
                'calls':deepcopy(self.calls),'visited':sorted(self.flow_visited),'pending':self.pending,
                'mode_request_consumed':False,'entry_controller_state':self.read(CONTROL+12,'B'),
                'opening_request':self.read(TACT+0x170,'B'),'opening_completion':self.read(TACT+0x171,'B'),
                'full_world_tick_executed':False,'AI_or_waves_executed':False,'mode_store_bodies_stubbed':False,
                **self.verify_scene_memory(retained)}
        finally:self.flow_loading=False;self._function_ranges=prior


def report():
    contract=source_contract();raw=PARENT.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=PARENT_SHA:raise ValueError('world mode pinned admission report')
    previous=json.loads(raw);parents=parent_evidence();deployment=read_deployment();opening=read_opening();cases=[]
    for index,(name,sha) in enumerate(CHECKPOINTS):
        checkpoint=(ROOT/f'.venv-audit/formation-actual-checkpoint-{index}.pkl').read_bytes()
        if hashlib.sha256(checkpoint).hexdigest()!=sha:raise ValueError('world mode checkpoint identity')
        payload=pickle.loads(checkpoint)
        if payload['source_sha']!=SOURCE_SHA256 or payload['evidence_kind']!='private_actual_cpu_after_full35_before_placement':
            raise ValueError('world mode checkpoint provenance')
        e=WorldModeEmulator()
        e.__dict__.update({k:v for k,v in payload['state'].items() if not k.startswith('_audit_') and k!='uc'})
        for at,data in payload['memory']:e.uc.mem_write(at,data)
        e.uc.context_restore(payload['cpu'])
        if e.run_placement()!=parents['cases'][index]['formation_placement']:raise ValueError('world mode parent placement')
        # Added callback guards cost host time. Enlarge only the parent suffix's
        # wall-time budget; preserve its original instruction cap and semantics.
        original_start=e.uc.emu_start
        def parent_start(begin,until,**kwargs):
            if begin==0x468A49:kwargs['timeout']=60_000_000
            return original_start(begin,until,**kwargs)
        e.uc.emu_start=parent_start
        try:
            tail=e.run_deployment_tail()
        except RuntimeError:
            print('parent suffix stopped at '+hex(e.uc.reg_read(UC_X86_REG_EIP))+', allocations '+str(len(e.deployment_allocations))+', calls '+str(len(e.deployment_calls)),flush=True)
            raise
        finally:e.uc.emu_start=original_start
        if tail!=deployment['cases'][index]['deployment_tail']:raise ValueError('world mode parent deployment')
        if e.run_initialization_and_opening()!=opening['cases'][index]['scene_opening']:raise ValueError('world mode parent opening')
        if e.audit_world_entry()!=previous['cases'][index]['world_admission']:raise ValueError('world mode full parent admission')
        probes=e.run_mode_probes();actual=e.run_actual_prefix()
        cases.append({'name':name,'checkpoint_sha256':sha,'complete_parent_equality':True,'declared_mode_probes':probes,'actual_world_prefix':actual})
        print(name+': original mode return, first natural entry update, 7 isolated mode probes',flush=True)
    return {'schema_version':1,'source_contract':contract,'parent_report':PARENT.relative_to(ROOT).as_posix(),
        'parent_sha256':PARENT_SHA,'cases':cases,'world_tick_completed':False,'original_opening_completed':False,'persistent_write_authority':False}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',required=True);args=parser.parse_args()
    path=ROOT/args.out
    if path.exists():parser.error('use a new immutable report path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
