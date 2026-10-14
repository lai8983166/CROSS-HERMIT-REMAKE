"""Original remaining friendly units, continuous world loop to deferredslot215."""
import argparse,hashlib,json,pickle,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EAX
from tools.school_student_tail_emulation import StudentTailEmulator,ROOT,UNITCTRL,TACT,STACK,RETURN,MAPCTRL,ExitEmulator,report_text,NATIVE as TAIL_NATIVE
from tools.school_student_tail_verification import load_verified_checkpoint,REPORT as PARENT,REPORT_SHA as PARENT_SHA
from tools.school_student_action_emulation import NATIVE as STUDENT_NATIVE
from tools.school_world_second_emulation import NATIVE as SECOND_NATIVE
from tools.school_following_students import *

NATIVE=TAIL_NATIVE+STUDENT_NATIVE+SECOND_NATIVE+ranges()+((0x46B532,0x46B586),)
CALL_ARGS={0x46B760:2,0x48D720:2,0x48E2A0:1,0x475700:1,0x4751F0:1,0x4697F0:1,0x475D60:1,
  0x46C040:2,0x46BCC0:2,0x465040:3,0x409FF0:4,0x46BE50:4,0x465140:6,0x40AF40:8,
  0x40B5E0:0,0x40A800:1,0x40A100:1,0x482A30:2,0x482AC0:3,0x4918D0:2,0x491960:3,
  0x493450:1,0x472370:1,0x472770:1,0x430400:1,0x43BB90:2,0x4305C0:2,0x43D270:3,0x46B2C0:1}


class FollowingStudentsEmulator(StudentTailEmulator):
    def __init__(self):
        self.following_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.following_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.following_allowed):raise RuntimeError('following forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.following_loading:return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
        if address==0x46B760:
            args=[self.read(sp+4),self.read(sp+8)]
            if (recv,ret,sp)!=(UNITCTRL,0x46B584,STACK+0xFF00-100) or args[0]!=UNITCTRL+0x80AEC+args[1]*STRIDE:raise RuntimeError('following natural occupied entry stack')
            if args[1]==215:
                self.following_pending={'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':args,'first_instruction_executed':False};uc.emu_stop();return
            if args[1] not in self.following_indices or args[1] in self.following_entries:raise RuntimeError('following exact current unit order')
            self.following_entries.append(args[1])
        if address in CALL_ARGS:
            self.following_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':[self.read(sp+4+i*4) for i in range(CALL_ARGS[address])]})
        if address==0x468D10 and ret==0x46B560:
            i=(self.read(sp+4)-UNITCTRL-0x80AEC)//STRIDE
            if recv!=UNITCTRL or self.read(sp+4)!=UNITCTRL+0x80AEC+i*STRIDE:raise RuntimeError('following original work test')
            self.following_tests.append(i)
        if address==0x46BA07:
            if (ret,sp)!=(0x46B584,STACK+0xFF00-100):raise RuntimeError('following original unit ret8')
            self.following_returns.append({'index':self.following_entries[-1],'va':hex(address),'return_va':hex(ret),'sp':sp,'eax':uc.reg_read(UC_X86_REG_EAX)})
        if address==0x56CEC0:
            args=[self.read(sp+4+i*4) for i in range(3)]
            if ret!=0x409F1A or args[1:]!=[0,88] or args[0] not in self.following_nodes:raise RuntimeError('following exact original pool node clear')
            self.following_clears.append({'return_va':hex(ret),'args':args})
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in NATIVE):self.following_visited.add(address);return
        raise RuntimeError('following undeclared original instruction '+hex(address))

    def following_regions(self):
        rows=self.regions();rows[1]={'name':'records','pointer':UNITCTRL+0xD0C2C,'bytes':176*COUNT,'hex':bytes(self.uc.mem_read(UNITCTRL+0xD0C2C,176*COUNT)).hex()}
        return rows

    def following_inputs(self):
        s=source_contract();units=[]
        for i in (1,2):
            w=UNITCTRL+0x80AEC+i*STRIDE
            if not self.read(w,'h'):continue
            rec=self.read(w+0x258);record=bytes(self.uc.mem_read(rec,176));rule=s['jobs'][str(struct.unpack_from('<H',record,2)[0])];bindings=[]
            for owner,p,identity in ((self.read(w+0x44),rule['main'],rule['main_source']),(self.read(UNITCTRL+0x2A6E8),rule['attachments'][0],rule['effect_source'])):
                meta=self.read(owner);raw=(ROOT/identity['local_file']).read_bytes();buf=bytes(self.uc.mem_read(meta,p['metadata_bytes']))
                if buf!=raw[:p['metadata_bytes']]:raise RuntimeError('following complete source metadata binding')
                bindings.append({'owner':owner,'metadata_pointer':meta,'metadata_bytes':len(buf),'metadata_sha256':hashlib.sha256(buf).hexdigest(),'source_sha256':identity['sha256'],'controller_hex':bytes(self.uc.mem_read(owner,84)).hex()})
            units.append({'index':i,'record_pointer':rec,'record_hex':record.hex(),'bindings':bindings})
        raw,identity=map_resource('map05.bin');header=self.read(MAPCTRL+0x2659C)
        if bytes(self.uc.mem_read(header,len(raw)))!=raw:raise RuntimeError('following complete MAP05 identity')
        return {'units':units,'team':self.read(UNITCTRL+0x2EF44,'B'),'map_sha256':identity['sha256'],'map_header_pointer':header,'map_all_bytes_verified':len(raw)}

    def run_following(self):
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x46B760 or self.read(self.uc.reg_read(UC_X86_REG_ESP)+8)!=1:raise RuntimeError('following verifiedslot1 start')
        before=self.following_regions();inputs=self.following_inputs();expected=project(inputs,before)
        self.following_indices=[u['index'] for u in expected['units']];self.following_nodes=[p for u in expected['units'] for p in u['allocated_nodes']]
        self.following_allowed=[(STACK,STACK+65536),(0x7A49E0,0x7A49E4)]+[(UNITCTRL+0x80AEC+i*STRIDE,UNITCTRL+0x80AEC+(i+1)*STRIDE) for i in self.following_indices]
        self.following_allowed += [(p,p+NODE) for p in self.following_nodes]+[(r['pointer'],r['pointer']+r['bytes']) for r in before[2:5]]
        retained=self.capture_scene_memory(self.following_allowed);prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.following_loading=True;self.following_calls=[];self.following_entries=[];self.following_tests=[];self.following_returns=[];self.following_clears=[];self.following_visited=set();self.following_pending=None
        try:
            self.uc.emu_start(0x46B760,RETURN,timeout=10_000_000,count=350000);after=self.following_regions()
            if after!=expected['after']:
                diffs=[]
                for a,b in zip(after,expected['after']):
                    aa,bb=bytes.fromhex(a['hex']),bytes.fromhex(b['hex']);diffs.extend((a['name'],hex(a['pointer']+n),av,bv) for n,(av,bv) in enumerate(zip(aa,bb)) if av!=bv)
                raise RuntimeError('following complete source/native bytes differ '+repr(diffs[:20]))
            if self.following_entries!=self.following_indices or self.following_tests!=list(range(2,216)) or self.following_pending is None:raise RuntimeError('following natural unit/empty-slot loop')
            return {'inputs':inputs,'before':before,**expected,'calls':self.following_calls,'unit_entries':self.following_entries,'tested_slots':self.following_tests,'unit_returns':self.following_returns,
              'native_clears':self.following_clears,'pending':self.following_pending,'visited':sorted(self.following_visited),'owned_bodies_stubbed':False,'deferred_unit_executed':False,'VM_or_AI_completed':False,**self.verify_scene_memory(retained)}
        finally:self.following_loading=False;self._function_ranges=prior

    def save_following(self,name):
        path=ROOT/f'.venv-audit/following-students-before-slot215-{name}.pkl'
        if path.exists():raise ValueError('fresh following private checkpoint')
        payload={'source_sha':SOURCE_SHA256,'parent_report_sha':PARENT_SHA,'case_name':name,'evidence_kind':'private_original_following_students_before_slot215','pending_eip':0x46B760,
          'state':{k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')},'memory':[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],'cpu':self.uc.context_save()}
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);path.write_bytes(raw)
        return {'path':path.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'pending_eip':'0x46b760','runtime_or_original_save':False}


def restored(name):
    payload,cp=load_verified_checkpoint(name);e=FollowingStudentsEmulator();e.__dict__.update({k:v for k,v in payload['state'].items() if k!='uc' and not k.startswith('_audit_')})
    for at,buf in payload['memory']:
        if not any(a<=at and at+len(buf)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(buf))
        e.uc.mem_write(at,buf)
    e.uc.context_restore(payload['cpu']);return e,cp


def report():
    cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        e,cp=restored(name);a=e.run_following();cases.append({'name':name,'parent_checkpoint':cp,'actual':a,'continuation_checkpoint':e.save_following(name)})
        print(name+': remaining friendly units returned; stopped before215',flush=True)
    return {'schema_version':1,'source_contract':source_contract(),'parent_report':PARENT.relative_to(ROOT).as_posix(),'parent_sha256':PARENT_SHA,'cases':cases,'remaining_friendly_units_completed':True,'world_completed':False,'original_opening_completed':False,'persistent_write_authority':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);args=p.parse_args();path=ROOT/args.out
    if path.exists():p.error('fresh immutable evidence required')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
