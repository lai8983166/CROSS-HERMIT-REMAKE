"""Actual opening visibility and complete display/category lists, before queue."""
import argparse,hashlib,json,pickle,struct
from copy import deepcopy
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ECX,UC_X86_REG_ESP
from tools.school_world_map_emulation import (
 WorldMapEmulator,PARENT as MODE_PARENT,PARENT_SHA as MODE_SHA,ADMISSION,ADMISSION_SHA,
 CHECKPOINTS,parent_evidence,read_deployment,read_opening,ROOT,UNITCTRL,STACK,RETURN,ExitEmulator,TACT,MAPCTRL,SOURCE_SHA256,report_text,
 architectural_cpu,cpu_digest)
from tools.school_world_lists import source_contract,ranges,project,viewport

PARENT=ROOT/'analysis/school-world-map-native-v4-20261014.json'
PARENT_SHA='7df722cc90844e668d9007d2da2e619aa3185e03476ffe3e0873b02994c82c41'
VIEW_PROBES=[(-64,-34),(1088,664),(-65,0),(1089,0),(0,-35),(0,665),(65536,65536)]
SORT_PROBES=[[(2<<16),(2<<16),(3<<16)],[(2<<16)]*3,[(100<<16)+1,(100<<16)+3,(100<<16)+2]]
WORK_OFFSET=0x80AEC;WORK_BYTES=0x520
LIST_RANGES=ranges()


class WorldListsEmulator(WorldMapEmulator):
    def __init__(self):
        self.lists_loading=False
        super().__init__()

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.lists_loading:return super()._write_hook(uc,access,address,size,value,context)
        if not any(a<=address and address+size<=b for a,b in self.lists_allowed):
            raise RuntimeError('world lists forbidden write '+hex(address)+' at '+hex(uc.reg_read(UC_X86_REG_EIP)))

    def _hook(self,uc,address,size,context):
        if not self.lists_loading:return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP);recv=uc.reg_read(UC_X86_REG_ECX);ret=self.read(sp)
        if address==0x48CD90:
            if self.lists_kind!='actual' or (recv,ret)!=(UNITCTRL,0x46B500):raise RuntimeError('lists next natural queue call')
            self.lists_pending={'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp,'first_instruction_executed':False};uc.emu_stop();return
        expected={0x49B180:0x46B4E8,0x46E520:0x46B4F0,0x46E730:0x46B4F8}
        # Source wrapper return addresses are checked below against image bytes.
        if address in expected:
            if recv!=UNITCTRL or ret!=(expected[address] if self.lists_kind=='actual' else RETURN):raise RuntimeError('actual/declared list root caller')
            self.lists_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'sp':sp})
        if address==0x43D270:
            args=[self.read(sp+4+i*4,'i') for i in range(3)]
            if recv!=MAPCTRL or args!=self.lists_inputs['origin']+[self.lists_inputs['view']] or ret!=0x49BA3E:raise RuntimeError('source opening vision caller')
            self.lists_calls.append({'va':hex(address),'receiver':recv,'return_va':hex(ret),'args':args})
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if any(a<=address<b for a,b in LIST_RANGES) or 0x46B4E8<=address<0x46B504:
            self.lists_visited.add(address);return
        raise RuntimeError('world lists undeclared instruction '+hex(address))

    def list_regions(self):
        rows=[('window',UNITCTRL+0x2F150,20),('fog_current',self.read(MAPCTRL+0xA4),6144),
              ('fog_history',self.read(MAPCTRL+0xA0),6144),('visible',UNITCTRL+0xDC30C,1004),('categories',UNITCTRL+0xDC8EC,5020)]
        return [{'name':n,'pointer':p,'bytes':b,'hex':bytes(self.uc.mem_read(p,b)).hex()} for n,p,b in rows]

    def list_inputs(self):
        rows=[]
        for i in range(250):
            p=UNITCTRL+WORK_OFFSET+i*WORK_BYTES;used=self.read(p,'h');record=self.read(p+0x258)
            rows.append({'index':i,'pointer':p,'used_word':used,'x_fixed':self.read(p+0x2EC,'i'),'y_fixed':self.read(p+0x2F0,'i'),
                         'record_pointer':record,'record_hex':bytes(self.uc.mem_read(record,176)).hex() if used else None})
        return {'works':rows,'team':self.read(UNITCTRL+0x2EF44,'B'),'relation_hex':bytes(self.uc.mem_read(UNITCTRL+0x115AAC,256)).hex(),
            'opening':self.read(UNITCTRL+0x108B48,'B'),'event':self.read(UNITCTRL+0x108B3A,'B'),'dimensions':[64,96],
            'origin':[self.read(UNITCTRL+0x108B40,'h'),self.read(UNITCTRL+0x108B42,'h')],'view':self.read(UNITCTRL+0x108B4B,'b'),
            'camera':[self.read(MAPCTRL+0x265A6,'h'),self.read(MAPCTRL+0x265A8,'h')]}

    def mask_bindings(self):
        rows=[]
        for source in source_contract()['masks']:
            ptr=self.read(MAPCTRL+8+source['view']*4)
            data=bytes(self.uc.mem_read(ptr,source['payload_bytes']))
            if data.hex()!=source['payload_hex']:raise RuntimeError('original complete mask binding bytes')
            rows.append({'view':source['view'],'pointer':ptr,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
        return rows

    def run_list_suffix(self):
        if self.uc.reg_read(UC_X86_REG_EIP)!=0x49B180:raise RuntimeError('actual pending selection/list suffix')
        before=self.list_regions();inputs=self.list_inputs();bindings=self.mask_bindings();expected=project(inputs,before)
        self.lists_inputs=inputs;self.lists_calls=[];self.lists_visited=set();self.lists_pending=None
        self.lists_allowed=[(STACK,STACK+65536),(UNITCTRL+0x2F157,UNITCTRL+0x2F158)]+[(r['pointer'],r['pointer']+r['bytes']) for r in before[1:]]
        retained=self.capture_scene_memory(self.lists_allowed);prior=self._function_ranges;self._function_ranges=prior+ranges()+((0x46B4E8,0x46B504),)
        self.lists_loading=True;self.lists_kind='actual'
        try:
            self.uc.emu_start(0x49B180,RETURN,timeout=5_000_000,count=150000)
            after=self.list_regions()
            if self.lists_pending is None or self.uc.reg_read(UC_X86_REG_EIP)!=0x48CD90 or after!=expected['after']:
                raise RuntimeError('source complete original list bytes/next queue boundary')
            return {'inputs':inputs,'before':before,'after':after,'mask_bindings':bindings,
                'display_indices':expected['display_indices'],'category_counts':expected['category_counts'],
                'occupied_slots':expected['occupied_slots'],'display_state1_slots':expected['display_state1_slots'],
                'calls':deepcopy(self.lists_calls),'visited':sorted(self.lists_visited),'pending':self.lists_pending,
                'full_world_tick_executed':False,'AI_or_waves_executed':False,'predicates_stubbed':False,**self.verify_scene_memory(retained)}
        finally:self.lists_loading=False;self._function_ranges=prior

    def run_list_probes(self):
        original=self.list_regions();inputs=self.list_inputs();used=[r for r in inputs['works'] if r['used_word']]
        chosen=[r for r in used if bytes.fromhex(r['record_hex'])[15]==1][:3]
        if len(chosen)!=3:raise RuntimeError('declared three display candidates')
        # Explicit synthetic record-state/position inputs; no battle activation.
        bound=[{'pointer':r['record_pointer']+15,'bytes':1,'hex':bytes(self.uc.mem_read(r['record_pointer']+15,1)).hex()} for r in used]
        bound += [{'pointer':r['pointer']+0x2EC,'bytes':8,'hex':bytes(self.uc.mem_read(r['pointer']+0x2EC,8)).hex()} for r in chosen]
        restore=original+bound;cpu=self.uc.context_save();stack=bytes(self.uc.mem_read(STACK,65536));regs=architectural_cpu(self.uc)
        allowed=[(r['pointer'],r['pointer']+r['bytes']) for r in restore];retained=self.capture_scene_memory(allowed)
        prior=self._function_ranges;self._function_ranges=prior+ranges();self.lists_allowed=[(STACK,STACK+65536)]+allowed
        self.lists_loading=True;self.lists_kind='probe';views=[];sorts=[]
        try:
            for x,y in VIEW_PROBES:
                value=self.call(0x46B130,[x&0xFFFFFFFF,y&0xFFFFFFFF],receiver=UNITCTRL)
                if value!=int(viewport(x,y)):raise RuntimeError('original viewport source short bounds')
                views.append({'declared_xy':[x,y],'return_eax':value})
            for depths in SORT_PROBES:
                for r in used:self.write(r['record_pointer']+15,0,'B')
                for r,y in zip(chosen,depths):
                    self.write(r['record_pointer']+15,1,'B');self.uc.mem_write(r['pointer']+0x2EC,struct.pack('<2i',100<<16,y))
                before=self.list_regions();source_inputs=self.list_inputs();self.lists_inputs=source_inputs;self.lists_calls=[];self.lists_visited=set()
                for function in (0x49B180,0x46E520,0x46E730):self.call(function,receiver=UNITCTRL)
                after=self.list_regions();p=project(source_inputs,before)
                if after!=p['after']:raise RuntimeError('original declared sort full source bytes')
                result={'declared_depths':depths,'selected_indices':[r['index'] for r in chosen],'inputs':source_inputs,'before':before,'after':after,
                        'display_indices':p['display_indices'],'category_counts':p['category_counts'],**self.verify_scene_memory(retained)}
                result['restoration']=self.restore_probe(restore,cpu,stack,regs);sorts.append(result)
            proof=self.restore_probe(restore,cpu,stack,regs)
            return {'viewport':views,'sorting':sorts,'final_restoration':proof,'live_input_captured':False,**self.verify_scene_memory(retained)}
        finally:
            self.restore_probe(restore,cpu,stack,regs);self.lists_loading=False;self._function_ranges=prior

    def save_verified_checkpoint(self,name,parent_case):
        path=ROOT/f'.venv-audit/world-lists-before-queue-{name}.pkl'
        if path.exists():raise ValueError('use a fresh private checkpoint name')
        state={k:v for k,v in self.__dict__.items() if k!='uc' and not k.startswith('_audit_')}
        case_hash=hashlib.sha256(report_text(parent_case).encode('utf-8')).hexdigest()
        payload={'source_sha':SOURCE_SHA256,'evidence_kind':'private_actual_school_after_verified_lists_before_queue',
            'parent_report_sha':PARENT_SHA,'case_name':name,'parent_case_sha':case_hash,'pending_eip':0x48CD90,
            'state':state,'memory':[(a,bytes(self.uc.mem_read(a,b-a+1))) for a,b,_ in self.uc.mem_regions()], 'cpu':self.uc.context_save()}
        raw=pickle.dumps(payload,protocol=pickle.HIGHEST_PROTOCOL);path.write_bytes(raw)
        return {'path':path.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),
                'parent_case_sha256':case_hash,'evidence_kind':payload['evidence_kind'],'pending_eip':'0x48cd90','runtime_or_original_save':False}


def report():
    def pinned(p,sha):
        raw=p.read_bytes()
        if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('list pinned parent '+p.name)
        return json.loads(raw)
    parent=pinned(PARENT,PARENT_SHA);mode=pinned(MODE_PARENT,MODE_SHA);admission=pinned(ADMISSION,ADMISSION_SHA)
    placement=parent_evidence();deployment=read_deployment();opening=read_opening();cases=[]
    for index,(name,sha) in enumerate(CHECKPOINTS):
        raw=(ROOT/f'.venv-audit/formation-actual-checkpoint-{index}.pkl').read_bytes()
        if hashlib.sha256(raw).hexdigest()!=sha:raise ValueError('lists checkpoint identity')
        payload=pickle.loads(raw)
        if payload['source_sha']!=SOURCE_SHA256 or payload['evidence_kind']!='private_actual_cpu_after_full35_before_placement':raise ValueError('lists checkpoint provenance')
        e=WorldListsEmulator();e.__dict__.update({k:v for k,v in payload['state'].items() if k!='uc' and not k.startswith('_audit_')})
        for at,data in payload['memory']:e.uc.mem_write(at,data)
        e.uc.context_restore(payload['cpu'])
        if e.run_placement()!=placement['cases'][index]['formation_placement']:raise ValueError('lists parent placement')
        start=e.uc.emu_start
        def bounded(begin,until,**kwargs):
            if begin==0x468A49:kwargs['timeout']=90_000_000
            return start(begin,until,**kwargs)
        e.uc.emu_start=bounded
        try:tail=e.run_deployment_tail()
        finally:e.uc.emu_start=start
        if tail!=deployment['cases'][index]['deployment_tail']:raise ValueError('lists parent deployment')
        if e.run_initialization_and_opening()!=opening['cases'][index]['scene_opening']:raise ValueError('lists parent opening')
        if e.audit_world_entry()!=admission['cases'][index]['world_admission']:raise ValueError('lists parent admission')
        mp=e.run_mode_probes();prefix=e.run_actual_prefix()
        if json.loads(json.dumps(mp))!=mode['cases'][index]['declared_mode_probes'] or prefix!=mode['cases'][index]['actual_world_prefix']:raise ValueError('lists complete mode parent')
        probes=e.run_probes();suffix=e.run_map_suffix()
        if probes!=parent['cases'][index]['declared_probes'] or suffix!=parent['cases'][index]['actual_map_suffix']:raise ValueError('lists complete map parent')
        actual=e.run_list_suffix();local=e.run_list_probes();checkpoint=e.save_verified_checkpoint(name,parent['cases'][index])
        cases.append({'name':name,'checkpoint_sha256':sha,'complete_parent_equality':True,'actual_list_suffix':actual,'declared_probes':local,'continuation_checkpoint':checkpoint})
        print(name+': '+str(actual['occupied_slots'])+' occupied / '+str(actual['display_state1_slots'])+' display-state1; lists and vision verified',flush=True)
    return {'schema_version':1,'source_contract':source_contract(),'parent_report':PARENT.relative_to(ROOT).as_posix(),'parent_sha256':PARENT_SHA,
        'cases':cases,'world_tick_completed':False,'original_opening_completed':False,'persistent_write_authority':False}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);a=p.parse_args();path=ROOT/a.out
    if path.exists():p.error('use a new immutable report path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
