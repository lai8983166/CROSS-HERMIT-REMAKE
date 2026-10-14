"""Resume original empty queue through complete paused work loop, before490FC0."""
import argparse,hashlib,pickle,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP
from tools.school_world_lists_emulation import WorldListsEmulator,UNITCTRL,MAPCTRL,STACK,RETURN,ROOT,ExitEmulator,architectural_cpu,report_text
from tools.school_world_lists_verification import load_verified_checkpoint,REPORT as PARENT,REPORT_SHA as PARENT_SHA
from tools.school_world_lists import ranges as list_ranges
from tools.school_world_command import source_contract,ranges,project,normalize_selection,STRIDE,COUNT
from tools.tactics_exit_emulation import SOURCE_SHA256,TASK

NATIVE=ranges()+list_ranges()+((0x46B500,0x46B620),(0x56CEC0,0x56CF18))
PROBES=((0,1,240,215),(1,240,215),(240,215),(215,))


class WorldCommandEmulator(WorldListsEmulator):
    def __init__(self):
        self.command_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.command_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.command_allowed):
            raise RuntimeError('command forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.command_loading:return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
        if address==0x490FC0:
            if self.command_kind!='actual' or (recv,ret,sp)!=(UNITCTRL,0x46B620,STACK+0xFF00-92):raise RuntimeError('next natural suffix boundary')
            self.command_pending={'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'first_instruction_executed':False};uc.emu_stop();return
        roots={0x48CD90:0x46B500,0x46EA10:0x46B508,0x46F440:0x46B510}
        if address in roots:
            if self.command_kind!='actual' or (recv,ret,sp)!=(UNITCTRL,roots[address],STACK+0xFF00-92):raise RuntimeError('actual command caller')
            self.command_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp})
        if address==0x427DE0:
            if (recv,ret)!=(UNITCTRL+0x1798,0x48CDC8):raise RuntimeError('queue source ownership/caller')
            self.command_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp})
        if address==0x46F170 and (recv!=UNITCTRL or ret!=(0x46EC70 if self.command_kind=='actual' else RETURN)):raise RuntimeError('selection normalization caller')
        if address==0x468D10 and ret==0x46B560:
            p=self.read(sp+4);index=(p-UNITCTRL-0x80AEC)//STRIDE
            if recv!=UNITCTRL or p!=UNITCTRL+0x80AEC+index*STRIDE:raise RuntimeError('work loop exact pointer')
            self.command_tested.append(index)
        if address==0x46B760:
            p,index=self.read(sp+4),self.read(sp+8)
            if self.command_kind!='actual' or (recv,ret,sp)!=(UNITCTRL,0x46B584,STACK+0xFF00-100) or p!=UNITCTRL+0x80AEC+index*STRIDE:
                raise RuntimeError('work update natural args/stack')
            self.command_units.append(index)
        if address==0x43D270:
            args=[self.read(sp+4+i*4,'i') for i in range(3)]
            if (recv,ret)!=(MAPCTRL,0x46B95B):raise RuntimeError('unit vision natural caller')
            self.command_vision.append({'index':self.command_units[-1],'args':args})
        if address==0x43C470:
            args=[self.read(sp+4+i*4) for i in range(3)]
            if recv!=MAPCTRL or ret not in (0x46B9C3,0x46B9EB):raise RuntimeError('unit cell occupancy caller')
            self.command_cells.append({'index':self.command_units[-1],'args':args})
        if address==0x56CEC0:
            args=[self.read(sp+4+i*4) for i in range(3)]
            if (ret,args) not in ((0x46F46F,[UNITCTRL+0x3098C,0,10]),(0x46B526,[UNITCTRL+0x2E714,0,2048])):raise RuntimeError('native exact memset bounds')
            self.command_clears.append({'return_va':hex(ret),'args':args})
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in NATIVE):self.command_visited.add(address);return
        raise RuntimeError('command undeclared instruction '+hex(address))

    def command_regions(self):
        owner=self.read(MAPCTRL+0x265A0);occupancy=self.read(owner)
        if owner==0 or self.read(MAPCTRL+0x2659C)==0:raise RuntimeError('actual source occupancy ownership')
        rows=[('queue',UNITCTRL+0x1798,20),('works',UNITCTRL+0x80AEC,STRIDE*COUNT),
          ('selection',UNITCTRL+0x108B50,1016),('cursor',UNITCTRL+0x3098C,10),('scratch',UNITCTRL+0x2E714,2048),
          ('fog_current',self.read(MAPCTRL+0xA4),6144),('fog_history',self.read(MAPCTRL+0xA0),6144),
          ('occupancy',occupancy,12288),('current_work',0x7A49E0,4)]
        return [{'name':n,'pointer':p,'bytes':b,'hex':bytes(self.uc.mem_read(p,b)).hex()} for n,p,b in rows]

    def command_inputs(self):
        rows=self.list_inputs()['works']
        if self.read(0x7A49FC)!=TASK:raise RuntimeError('original input receiver')
        return {'record_hex':[r['record_hex'] for r in rows],'team':self.read(UNITCTRL+0x2EF44,'B'),
          'work_base':UNITCTRL+0x80AEC,'relations':bytes(self.uc.mem_read(UNITCTRL+0x115AAC,256)).hex(),
          'gates':[self.read(UNITCTRL+0x108B32,'h')]+[self.read(UNITCTRL+i,'b') for i in (0x108B34,0x108B36,0x108B38,0x108B39,0x108B3A)],
          'map_state':self.read(UNITCTRL+0x2A340),'task_mouse':[self.read(TASK+i) for i in (0x1990,0x194C,0x19B8)],
          'ctrl_keys':[self.read(TASK+0x10B8+0x480+i,'B')&128 for i in (0x9D,0x1D)]}

    def reset_trace(self):
        self.command_calls=[];self.command_tested=[];self.command_units=[];self.command_vision=[];self.command_cells=[];self.command_clears=[]
        self.command_visited=set();self.command_pending=None

    def run_suffix(self):
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x48CD90:raise RuntimeError('command checkpoint pending EIP')
        before=self.command_regions();inputs=self.command_inputs();expected=project(inputs,before)
        writable=[r for r in before if r['name'] not in ('queue','works')]
        self.command_allowed=[(STACK,STACK+65536)]+[(r['pointer'],r['pointer']+r['bytes']) for r in writable]
        for i in expected['occupied_indices']:
            p=UNITCTRL+0x80AEC+i*STRIDE;self.command_allowed.append((p+0x28C,p+0x28D))
        for i in expected['active_indices']:
            p=UNITCTRL+0x80AEC+i*STRIDE;self.command_allowed.append((p+0x4E7,p+0x4EB))
        retained=self.capture_scene_memory(self.command_allowed);prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.command_loading=True;self.command_kind='actual';self.reset_trace()
        try:
            self.uc.emu_start(0x48CD90,RETURN,timeout=10_000_000,count=400000)
            after=self.command_regions()
            cells=[{'index':r['index'],'args':a} for r in expected['cell_changes'] for a in r['calls']]
            if self.command_pending is None or after!=expected['after'] or self.command_tested!=list(range(250)) or self.command_units!=expected['occupied_indices'] or self.command_vision!=expected['vision_calls'] or self.command_cells!=cells:
                raise RuntimeError('original complete command/unit source equality')
            return {'inputs':inputs,'before':before,**expected,'calls':deepcopy(self.command_calls),'tested_indices':self.command_tested,
              'updated_indices':self.command_units,'native_vision_calls':self.command_vision,'native_cell_calls':self.command_cells,'native_clears':self.command_clears,
              'visited':sorted(self.command_visited),'pending':self.command_pending,'full_world_tick_executed':False,'action_animation_AI_executed':False,
              'nonempty_queue_consumed':False,'input_injected':False,'owned_bodies_stubbed':False,**self.verify_scene_memory(retained)}
        finally:self.command_loading=False;self._function_ranges=prior

    def run_selection_probes(self):
        originals=self.command_regions();restore=[r for r in originals if r['name'] in ('works','selection')]
        cpu=self.uc.context_save();stack=bytes(self.uc.mem_read(STACK,65536));regs=architectural_cpu(self.uc);inputs=self.command_inputs()
        allowed=[(r['pointer'],r['pointer']+r['bytes']) for r in restore];retained=self.capture_scene_memory(allowed)
        self.command_allowed=[(STACK,STACK+65536),(UNITCTRL+0x108B50,UNITCTRL+0x108B50+1016)]
        used=project(inputs,originals)['occupied_indices']
        self.command_allowed += [(UNITCTRL+0x80AEC+i*STRIDE+0x28C,UNITCTRL+0x80AEC+i*STRIDE+0x28D) for i in used]
        prior=self._function_ranges;self._function_ranges=prior+NATIVE;self.command_loading=True;self.command_kind='probe';results=[]
        try:
            for declared in PROBES:
                for i in used:self.write(UNITCTRL+0x80AEC+i*STRIDE+0x28C,int(i in declared),'B')
                before=self.command_regions();self.reset_trace();expected=project(inputs,before)
                self.call(0x46F170,receiver=UNITCTRL);after=self.command_regions()
                # Only selection and work flags are affected by this isolated call.
                wanted=deepcopy(before)
                for row in wanted:
                    if row['name']=='selection':row['hex']=expected['after'][2]['hex']
                    if row['name']=='works':row['hex']=normalize_selection(bytes.fromhex(before[1]['hex']),[bytes.fromhex(r) if r else None for r in inputs['record_hex']],inputs['team'])[0].hex()
                if after!=wanted:raise RuntimeError('source selection probe full buffers')
                result={'declared_indices':list(declared),'inputs':inputs,'before':before,'after':after,
                  'selected_indices':expected['selected_indices'],'selection_kind':expected['selection_kind'],'visited':sorted(self.command_visited),**self.verify_scene_memory(retained)}
                result['restoration']=self.restore_probe(restore,cpu,stack,regs);results.append(result)
            return {'live_input_captured':False,'selection':results,'final_restoration':self.restore_probe(restore,cpu,stack,regs)}
        finally:self.restore_probe(restore,cpu,stack,regs);self.command_loading=False;self._function_ranges=prior

    def save_checkpoint(self,name):
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x490FC0:raise RuntimeError('next checkpoint CPU')
        path=ROOT/f'.venv-audit/world-command-before-effects-{name}.pkl'
        if path.exists():raise ValueError('fresh continuation path required')
        payload={'source_sha':SOURCE_SHA256,'parent_report_sha':PARENT_SHA,'case_name':name,
          'evidence_kind':'private_actual_school_after_paused_unit_loop','pending_eip':0x490FC0,
          'state':{k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')},
          'memory':[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],'cpu':self.uc.context_save()}
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);path.write_bytes(raw)
        return {'path':path.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),
                'pending_eip':'0x490fc0','runtime_or_original_save':False}


def restore_case(name):
    payload,cp=load_verified_checkpoint(name);e=WorldCommandEmulator()
    e.__dict__.update({k:v for k,v in payload['state'].items() if k!='uc' and not k.startswith('_audit_')})
    for at,data in payload['memory']:
        if not any(a<=at and at+len(data)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(data))
        e.uc.mem_write(at,data)
    e.uc.context_restore(payload['cpu']);return e,cp


def report():
    cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        e,cp=restore_case(name);actual=e.run_suffix();probes=e.run_selection_probes();saved=e.save_checkpoint(name)
        cases.append({'name':name,'parent_checkpoint':cp,'actual_suffix':actual,'declared_probes':probes,'continuation_checkpoint':saved})
        print(name+': 250 occupancy tests / '+str(len(actual['updated_indices']))+' occupied updates; paused full bytes verified',flush=True)
    return {'schema_version':1,'source_contract':source_contract(),'parent_report':PARENT.relative_to(ROOT).as_posix(),'parent_sha256':PARENT_SHA,
      'driver':'pinned verified CPU/all-memory restoration; upstream initialization not replayed this run','cases':cases,
      'world_tick_completed':False,'original_opening_completed':False,'persistent_write_authority':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable report path required')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
