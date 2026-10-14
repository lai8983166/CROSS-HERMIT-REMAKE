"""Natural second-world action prefix, stopping before first student handler."""
import argparse,hashlib,json,pickle
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP
from tools.school_world_tail_emulation import WorldTailEmulator,ROOT,UNITCTRL,STACK,RETURN,ExitEmulator,report_text
from tools.school_world_tail_verification import REPORT as PARENT,REPORT_SHA as PARENT_SHA,verify_case as verify_tail
from tools.school_world_command_verification import load_verified_checkpoint
from tools.school_world_mode import RANGES as MODE_RANGES
from tools.school_entry_control_emulation import NATIVE as ENTRY_RANGES,TACT,MAPCTRL
from tools.school_world_map import RANGES as MAP_RANGES
from tools.school_world_lists import ranges as list_ranges
from tools.school_world_command import ranges as command_ranges,STRIDE
from tools.school_world_second import source_contract,ranges,project,NAMES
from tools.tactics_exit_emulation import SOURCE_SHA256,TASK

NATIVE=((0x46B470,0x46B663),)+MODE_RANGES+ENTRY_RANGES+MAP_RANGES+list_ranges()+command_ranges()+ranges()
ROOT_RETURNS={0x4678C0:0x46B4B2,0x499DA0:0x46B4C8,0x493630:0x46B4D0,0x467B60:0x46B4D8,
  0x46E9C0:0x46B4E0,0x49B180:0x46B4E8,0x46E520:0x46B4F0,0x46E730:0x46B4F8,
  0x48CD90:0x46B500,0x46EA10:0x46B508,0x46F440:0x46B510,0x46B760:0x46B584,
  0x48D720:0x46B7C9,0x48E2A0:0x46B7D5,0x475700:0x46B7E1,0x4751F0:0x475734,0x4697F0:0x475740}


class WorldSecondEmulator(WorldTailEmulator):
    def __init__(self):
        self.second_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.second_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.second_allowed):raise RuntimeError('second world forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.second_loading:return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
        if address==0x475D60:
            if (recv,ret,sp,self.read(sp+4))!=(UNITCTRL,0x4757A3,STACK+0xFF00-316,UNITCTRL+0x80AEC):raise RuntimeError('second natural first student handler stack')
            self.second_pending={'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':[self.read(sp+4)],'first_instruction_executed':False};uc.emu_stop();return
        if address==0x46B470:
            if (recv,ret,sp)!=(UNITCTRL,RETURN,STACK+0xFF00):raise RuntimeError('second declared root world call')
            self.second_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'declared_root':True})
        if address in ROOT_RETURNS:
            if recv!=UNITCTRL or ret!=ROOT_RETURNS[address]:raise RuntimeError('second world natural receiver/caller '+hex(address))
            row={'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp}
            if address in (0x46B760,0x48D720):row['args']=[self.read(sp+4),self.read(sp+8)]
            elif address in (0x48E2A0,0x475700,0x4751F0,0x4697F0):row['args']=[self.read(sp+4)]
            self.second_calls.append(row)
        if address==0x415070:
            if (recv,ret,self.read(sp+4))!=(TASK,0x49A068,180):raise RuntimeError('second native180 delay caller')
            self.second_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':[180]})
        if address==0x43D270:
            args=[self.read(sp+4+i*4,'i') for i in range(3)]
            if (recv,ret,args)!=(MAPCTRL,0x49BA3E,[9,16,0]):raise RuntimeError('second opening native visibility caller')
            self.second_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':args})
        if address==0x427DE0:
            if (recv,ret)!=(UNITCTRL+0x1798,0x48CDC8):raise RuntimeError('second empty command queue caller')
            self.second_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp})
        if address==0x468D10 and ret==0x46B560:
            if (recv,self.read(sp+4))!=(UNITCTRL,UNITCTRL+0x80AEC):raise RuntimeError('second first work occupancy test')
            self.second_tested.append(0)
        if address==0x56CEC0:
            args=[self.read(sp+4+i*4) for i in range(3)]
            expected={0x43D10C:[self.second_clear_pointer,0,6144],0x46F46F:[UNITCTRL+0x3098C,0,10],0x46B526:[UNITCTRL+0x2E714,0,2048]}
            if ret not in expected or args!=expected[ret]:raise RuntimeError('second native exact clear bounds')
            self.second_clears.append({'return_va':hex(ret),'args':args})
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in NATIVE):self.second_visited.add(address);return
        raise RuntimeError('second world undeclared instruction '+hex(address))

    def second_regions(self):
        cmd=self.command_regions();maps=self.map_regions();lists=self.list_regions()
        rows=[{'name':'task','pointer':TACT,'bytes':400,'hex':bytes(self.uc.mem_read(TACT,400)).hex()},
          {'name':'control','pointer':UNITCTRL+0x108B30,'bytes':50,'hex':bytes(self.uc.mem_read(UNITCTRL+0x108B30,50)).hex()},
          {'name':'clock','pointer':UNITCTRL+0x2E6F4,'bytes':24,'hex':bytes(self.uc.mem_read(UNITCTRL+0x2E6F4,24)).hex()}]
        rows+=maps+[lists[0],lists[3],lists[4],cmd[1],cmd[2],cmd[3],cmd[4],cmd[0],cmd[7],cmd[8]]
        if [r['name'] for r in rows]!=NAMES:raise RuntimeError('second full captured region identity')
        return rows

    def second_inputs(self):
        c=self.command_inputs()
        return {'mouse':[self.read(TASK+0x196C,'i'),self.read(TASK+0x1970,'i')],'map_state':c['map_state'],
          'task_input':c['task_mouse'],'ctrl_keys':c['ctrl_keys'],'lists':self.list_inputs()}

    def run_second_prefix(self):
        if self.uc.reg_read(UC_X86_REG_EIP)!=RETURN or self.uc.reg_read(UC_X86_REG_ESP)!=STACK+0xFF00+4:raise RuntimeError('second requires verified first world return CPU')
        before=self.second_regions();inputs=self.second_inputs();expected=project(inputs,before);self.second_clear_pointer=before[7]['pointer']
        self.second_allowed=[(STACK,STACK+65536),(TACT+0x170,TACT+0x171),(UNITCTRL+0x108B34,UNITCTRL+0x108B35),
          (UNITCTRL+0x108B4A,UNITCTRL+0x108B4B),(UNITCTRL+0x108B4C,UNITCTRL+0x108B4E),
          (MAPCTRL+0xA4,MAPCTRL+0xAC),(UNITCTRL+0x2F157,UNITCTRL+0x2F158),(UNITCTRL+0x80AEC+8,UNITCTRL+0x80AEC+9)]
        for i in (4,5,7,8,10,11,13,14,15,18):
            r=before[i];self.second_allowed.append((r['pointer'],r['pointer']+r['bytes']))
        for r in inputs['lists']['works']:
            if r['used_word']:self.second_allowed.append((r['pointer']+0x28C,r['pointer']+0x28D))
        retained=self.capture_scene_memory(self.second_allowed);prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.second_loading=True;self.second_calls=[];self.second_clears=[];self.second_tested=[];self.second_visited=set();self.second_pending=None
        try:
            # This explicit driver call stops in a natural nested original handler.
            self.write(STACK+0xFF00,RETURN);self.uc.reg_write(UC_X86_REG_ESP,STACK+0xFF00);self.uc.reg_write(UC_X86_REG_ECX,UNITCTRL)
            self.uc.emu_start(0x46B470,RETURN,timeout=10_000_000,count=400000)
            after=self.fixed_regions(before)
            if after!=expected['after'] or self.second_pending is None or self.second_tested!=[0] or self.uc.reg_read(UC_X86_REG_EIP)!=0x475D60:raise RuntimeError('second complete independent source/native prefix equality')
            return {'inputs':inputs,'before':before,**expected,'calls':deepcopy(self.second_calls),'native_clears':self.second_clears,
              'native_tested_indices':self.second_tested,'visited':sorted(self.second_visited),'pending':self.second_pending,
              'root_call_declared':True,'controller_in_original_world_order':True,'second_world_body_completed':False,
              'student_handler_executed':False,'active_animation_executed':False,'180_enabled_world_updates_executed':False,
              'VM_or_AI_completed':False,'owned_bodies_stubbed':False,**self.verify_scene_memory(retained)}
        finally:self.second_loading=False;self._function_ranges=prior

    def save_checkpoint(self,name):
        path=ROOT/f'.venv-audit/world-second-before-student-{name}.pkl'
        if path.exists():raise ValueError('fresh private continuation required')
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x475D60:raise ValueError('student checkpoint EIP')
        payload={'source_sha':SOURCE_SHA256,'parent_report_sha':PARENT_SHA,'case_name':name,'evidence_kind':'private_actual_second_world_before_student_handler',
          'pending_eip':0x475D60,'state':{k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')},
          'memory':[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],'cpu':self.uc.context_save()}
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);path.write_bytes(raw)
        return {'path':path.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'pending_eip':'0x475d60','runtime_or_original_save':False}


def report():
    raw=PARENT.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=PARENT_SHA:raise ValueError('second pinned tail report')
    parent=json.loads(raw);cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        previous=next(r for r in parent['cases'] if r['name']==name);verify_tail(previous)
        payload,cp=load_verified_checkpoint(name);e=WorldSecondEmulator()
        e.__dict__.update({k:v for k,v in payload['state'].items() if k!='uc' and not k.startswith('_audit_')})
        for at,data in payload['memory']:
            if not any(a<=at and at+len(data)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(data))
            e.uc.mem_write(at,data)
        e.uc.context_restore(payload['cpu']);tail=e.run_tail()
        if tail!=previous['actual_tail']:raise ValueError('second complete pinned actual first tail equality')
        actual=e.run_second_prefix();saved=e.save_checkpoint(name)
        cases.append({'name':name,'parent_checkpoint':cp,'complete_actual_tail_equality':True,'actual_second_prefix':actual,'continuation_checkpoint':saved})
        print(name+': natural state4 to5/action1/delay180; first student status dispatch verified',flush=True)
    return {'schema_version':1,'source_contract':source_contract(),'parent_report':PARENT.relative_to(ROOT).as_posix(),'parent_sha256':PARENT_SHA,
      'driver':'pinned first tail replay then declared next46B470 invocation; natural nested controller/unit calls',
      'cases':cases,'second_world_body_completed':False,'original_opening_completed':False,'persistent_write_authority':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('fresh immutable report path required')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
