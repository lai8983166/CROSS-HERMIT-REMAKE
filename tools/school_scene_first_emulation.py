"""Original scene217 initializer and terminal animation through natural return."""
import argparse,hashlib,pickle
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP,UC_X86_REG_EAX
from tools.school_deferred_units_emulation import DeferredUnitsEmulator,NATIVE as PRIOR_NATIVE,ROOT,UNITCTRL,STACK,RETURN,ExitEmulator,report_text
from tools.school_deferred_units_verification import load_verified_checkpoint as load_parent,REPORT as PARENT,REPORT_SHA as PARENT_SHA
from tools.school_following_students_emulation import CALL_ARGS as FRIENDLY_CALLS,MAPCTRL
from tools.school_following_students_verification import pending
from tools.school_scene_first import *

NATIVE=PRIOR_NATIVE+ranges()
CALL_ARGS={**FRIENDLY_CALLS,0x4761C0:1,0x480A60:1,0x46B0F0:2,0x46B0B0:2,0x46A430:1,0x46A5E0:1,0x490350:2,0x490A50:3}


class SceneFirstEmulator(DeferredUnitsEmulator):
    def __init__(self):self.scene_first_loading=False;super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.scene_first_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.scene_first_allowed):raise RuntimeError('scene first forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.scene_first_loading:return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp);w=UNITCTRL+0x80AEC+INDEX*STRIDE
        if address==0x40A100 and self.scene_first_phase=='initializer':
            if (recv,ret,sp,self.read(sp+4))!=(self.scene_first_inputs['main_binding']['owner'],0x46B80C,STACK+0xFF00-204,w+0x48):raise RuntimeError('scene original main animation entry')
            self.scene_first_pending={'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':[w+0x48],'first_instruction_executed':False};uc.emu_stop();return
        if address==0x46B760:
            index=self.read(sp+8);p=pending(index)
            if (recv,ret,sp,[self.read(sp+4),index])!=(p['receiver'],int(p['return_va'],16),p['sp'],p['args']):raise RuntimeError('scene natural unit entry')
            if self.scene_first_phase=='complete' and index==218:self.scene_first_pending=p;uc.emu_stop();return
            if self.scene_first_phase!='initializer' or index!=INDEX:raise RuntimeError('scene exact217/218 boundary')
        if address in CALL_ARGS:
            self.scene_first_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'args':[self.read(sp+4+n*4) for n in range(CALL_ARGS[address])]})
        if address in (0x475BDD,0x475C55,0x46B7E1,0x46B80C,0x46B85B,0x46BA07):
            self.scene_first_returns.append({'va':hex(address),'sp':sp,'eax':uc.reg_read(UC_X86_REG_EAX)})
        if address==0x468D10 and ret==0x46B560:self.scene_first_tests.append((self.read(sp+4)-UNITCTRL-0x80AEC)//STRIDE)
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in NATIVE):self.scene_first_visited.add(address);return
        raise RuntimeError('scene first undeclared original instruction '+hex(address))

    def inputs217(self):
        s=source_contract();w=UNITCTRL+0x80AEC+INDEX*STRIDE;owner=self.read(w+0x44);meta=self.read(owner);raw,identity,_=remaining_resource(406,0);n=s['main']['metadata_bytes']
        buf=bytes(self.uc.mem_read(meta,n))
        if buf!=raw[:n]:raise RuntimeError('scene complete26E metadata source binding')
        source,mapid=map_resource('map05.bin');header=self.read(MAPCTRL+0x2659C)
        if bytes(self.uc.mem_read(header,len(source)))!=source:raise RuntimeError('scene completeMAP05 source binding')
        rec=self.read(w+0x258)
        return {'record_pointer':rec,'record_hex':bytes(self.uc.mem_read(rec,176)).hex(),'main_binding':{'owner':owner,'metadata_pointer':meta,'metadata_bytes':n,
          'metadata_sha256':hashlib.sha256(buf).hexdigest(),'source_sha256':identity['sha256'],'controller_hex':bytes(self.uc.mem_read(owner,84)).hex()},
          'effect_controller':self.read(UNITCTRL+0x2A6E8),'team':self.read(UNITCTRL+0x2EF44,'B'),'relation_matrix_hex':bytes(self.uc.mem_read(UNITCTRL+0x115AAC,256)).hex(),
          'map_sha256':mapid['sha256'],'map_all_bytes_verified':len(source),'map_header_pointer':header}

    def run_phase(self,phase):
        begin=0x46B760 if phase=='initializer' else 0x40A100
        if self.uc.reg_read(UC_X86_REG_EIP)!=begin:raise RuntimeError('scene exact verified phase start')
        if phase=='initializer':self.scene_first_initial_before=self.following_regions();self.scene_first_inputs=self.inputs217()
        before=self.following_regions();expected=project(self.scene_first_inputs,self.scene_first_initial_before,phase);w=UNITCTRL+0x80AEC+INDEX*STRIDE
        self.scene_first_allowed=[(STACK,STACK+65536),(w,w+STRIDE),(0x7A49E0,0x7A49E4)]
        if phase=='complete':
            event=expected['event_region']
            if event<32:
                p=before[2]['pointer']+event*64+6*4;self.scene_first_allowed.append((p,p+4))
            if expected['vision_args'] is not None:self.scene_first_allowed += [(r['pointer'],r['pointer']+r['bytes']) for r in before[3:5]]
        retained=self.capture_scene_memory(self.scene_first_allowed);prior=self._function_ranges;self._function_ranges=prior+NATIVE
        self.scene_first_loading=True;self.scene_first_phase=phase;self.scene_first_calls=[];self.scene_first_returns=[];self.scene_first_tests=[];self.scene_first_visited=set();self.scene_first_pending=None
        try:
            self.uc.emu_start(begin,RETURN,timeout=5_000_000,count=200000);after=self.following_regions()
            if after!=expected['after']:
                diff=[]
                for a,b in zip(after,expected['after']):
                    aa,bb=bytes.fromhex(a['hex']),bytes.fromhex(b['hex']);diff.extend((a['name'],hex(a['pointer']+i),x,y) for i,(x,y) in enumerate(zip(aa,bb)) if x!=y)
                raise RuntimeError('scene full original/source bytes '+repr(diff[:20]))
            if self.scene_first_pending is None or self.scene_first_tests!=([218] if phase=='complete' else []):raise RuntimeError('scene original pending/loop')
            return {'phase':phase,'inputs':self.scene_first_inputs,'initial_before':self.scene_first_initial_before,'before':before,**expected,
              'calls':self.scene_first_calls,'returns':self.scene_first_returns,'tested_slots':self.scene_first_tests,'pending':self.scene_first_pending,'visited':sorted(self.scene_first_visited),
              'owned_bodies_stubbed':False,'next_unit_executed':False,'animation_release_executed':False,'VM_or_AI_completed':False,**self.verify_scene_memory(retained)}
        finally:self.scene_first_loading=False;self._function_ranges=prior

    def save_phase(self,name,phase):
        path=ROOT/f'.venv-audit/scene-first-{phase}-{name}.pkl'
        if path.exists():raise ValueError('fresh scene-first private path')
        eip=0x40A100 if phase=='initializer' else 0x46B760
        payload={'source_sha':SOURCE_SHA256,'parent_report_sha':PARENT_SHA,'case_name':name,'phase':phase,'evidence_kind':'private_original_scene_first_'+phase,'pending_eip':eip,
          'state':{k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')},'memory':[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()],'cpu':self.uc.context_save()}
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);path.write_bytes(raw)
        return {'path':path.relative_to(ROOT).as_posix(),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'pending_eip':hex(eip),'runtime_or_original_save':False}


def restored(name,phase='initializer'):
    if phase=='initializer':payload,cp=load_parent(name)
    else:
        from tools.school_scene_first_verification import load_verified_checkpoint
        payload,cp=load_verified_checkpoint(name,'initializer')
    e=SceneFirstEmulator();e.__dict__.update({k:v for k,v in payload['state'].items() if k!='uc' and not k.startswith('_audit_')})
    for at,buf in payload['memory']:
        if not any(a<=at and at+len(buf)<=b+1 for a,b,_ in e.uc.mem_regions()):e.uc.mem_map(at,len(buf))
        e.uc.mem_write(at,buf)
    e.uc.context_restore(payload['cpu']);return e,cp


def report(phase):
    cases=[]
    for name in ('initial','student9_waiting','fifth_class'):
        e,cp=restored(name,phase)
        if phase=='initializer':e.scene_first_parent_checkpoint=cp
        a=e.run_phase(phase);case={'name':name,'parent_checkpoint':e.scene_first_parent_checkpoint,'actual':a,'continuation_checkpoint':e.save_phase(name,phase)}
        if phase=='complete':case['initializer_checkpoint']=cp
        cases.append(case);print(name+': original scene217 '+phase+' verified',flush=True)
    return {'schema_version':1,'phase':phase,'source_contract':source_contract(),'parent_report':PARENT.relative_to(ROOT).as_posix(),'parent_sha256':PARENT_SHA,
      'cases':cases,'unit_completed':phase=='complete','world_completed':False,'original_opening_completed':False,'persistent_write_authority':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--phase',choices=('initializer','complete'),required=True);p.add_argument('--out',required=True);args=p.parse_args();path=ROOT/args.out
    if path.exists():p.error('fresh immutable evidence required')
    path.write_text(report_text(report(args.phase)),encoding='utf-8',newline='\n')
