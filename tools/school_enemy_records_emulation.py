"""Native scene5 template records; actual school stops before enemy-loop work."""
import argparse
from copy import deepcopy
import hashlib
import struct
from unicorn.x86_const import UC_X86_REG_EIP,UC_X86_REG_ESP,UC_X86_REG_ECX
from tools.school_current_units_emulation import (
    SchoolCurrentUnitsEmulator,ROOT,SOURCE,SOURCE_SHA256,BASE,TACT,UNITCTRL,
    RECORD_OFFSET,WORK_OFFSET,WORK_BYTES,CHAR_BASE,STACK,RETURN,ExitEmulator,AUTHORITY,report_text)

NATIVE=((0x453540,0x45364E),(0x4DA450,0x4DA5E8),(0x4DA5F0,0x4DA70C),
        (0x4DFC20,0x4E0931),(0x4E0A00,0x4E1A07))
SCRATCH,SCRATCH_BYTES=0x7E11B0,48
CHARACTER_DEFINITION_BASE=0x6F5088


def scene_inputs():
    raw=SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA256:raise ValueError('enemy source identity')
    scene=5;pointer=struct.unpack_from('<I',raw,0x6A7F6C-BASE+scene*4)[0]
    count=struct.unpack_from('<h',raw,0x6A85AC-BASE+scene*2)[0]
    if count!=35 or not BASE<=pointer<BASE+len(raw)-count*84:raise ValueError('scene5 template bounds')
    return {'scene':scene,'pointer':pointer,'count':count,
        'templates':[raw[pointer-BASE+i*84:pointer-BASE+(i+1)*84].hex() for i in range(count)]}


class SchoolEnemyRecordsEmulator(SchoolCurrentUnitsEmulator):
    def __init__(self):
        self.enemy_loading=False
        super().__init__();self._function_ranges+=NATIVE
        self.enemy_code=frozenset(a for s,t in NATIVE for a in range(s,t))
        self.enemy_inputs=scene_inputs();self.enemy_record=None;self.enemy_mode=None;self.enemy_ordinal=0

    def _write_hook(self,uc,access,address,size,value,context):
        if not self.enemy_loading:return super()._write_hook(uc,access,address,size,value,context)
        allowed=[(STACK,STACK+0x10000),(0,4)]
        if self.enemy_record:
            at=self.enemy_record['record_pointer'];allowed.append((at,at+176))
            if self.enemy_record['identity']<200:allowed.append((SCRATCH,SCRATCH+SCRATCH_BYTES))
        if not any(a<=address and address+size<=b for a,b in allowed):
            raise RuntimeError(f'enemy record finite guard {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        if not STACK<=address<STACK+0x10000:
            self.writes.append((address,size,value&((1<<(size*8))-1)))

    def capture_retained(self,destination):
        excluded=[(STACK,STACK+0x10000),(0,4),(destination,destination+176)]
        if self.enemy_record['identity']<200:excluded.append((SCRATCH,SCRATCH+48))
        spans=[]
        for start,end,_ in self.uc.mem_regions():
            pieces=[(start,end+1)]
            for left,right in excluded:
                pieces=[p for a,b in pieces for p in ((a,min(b,left)),(max(a,right),b)) if p[0]<p[1]]
            spans.extend((a,bytes(self.uc.mem_read(a,b-a))) for a,b in pieces)
        return spans

    def begin_record(self,sp):
        source,destination=self.read(sp+4),self.read(sp+8)
        ordinal=self.enemy_ordinal;index=249-ordinal;inputs=self.enemy_inputs
        expected=UNITCTRL+RECORD_OFFSET+index*176
        caller=self.read(sp)
        if source!=inputs['pointer']+ordinal*84 or destination!=expected or not 0<=ordinal<inputs['count'] \
                or caller!=(0x45361B if self.enemy_mode=='actual_school' else RETURN):
            raise RuntimeError('enemy original template/destination/caller ownership')
        template=bytes(self.uc.mem_read(source,84));identity=struct.unpack_from('<h',template)[0]
        if template.hex()!=inputs['templates'][ordinal] or not 1<=identity<1024:
            raise RuntimeError('enemy template identity differs')
        self.enemy_record={'ordinal':ordinal,'index':index,'identity':identity,'template_pointer':source,
            'template_hex':template.hex(),'record_pointer':destination,'caller_return_va':hex(caller),
            'before_record_hex':bytes(self.uc.mem_read(destination,176)).hex(),
            'scratch_before_hex':bytes(self.uc.mem_read(SCRATCH,48)).hex(),'clears':[]}
        if identity<200:
            self.enemy_record['character_pointer']=CHARACTER_DEFINITION_BASE+identity*0x4A0
            self.enemy_record['character_input_hex']=bytes(self.uc.mem_read(CHARACTER_DEFINITION_BASE+identity*0x4A0,0x4A0)).hex()
            self.enemy_record['character_input_origin']='original_EXE_character_definition_not_persistent_directory'
        self.enemy_record['retained_before']=self.capture_retained(destination)

    def finish_record(self):
        r=self.enemy_record
        retained=r.pop('retained_before')
        if any(bytes(self.uc.mem_read(a,len(raw)))!=raw for a,raw in retained):
            raise RuntimeError('enemy record changed retained memory')
        r.update({'record_hex':bytes(self.uc.mem_read(r['record_pointer'],176)).hex(),
            'scratch_after_hex':bytes(self.uc.mem_read(SCRATCH,48)).hex(),
            'work_hex':bytes(self.uc.mem_read(UNITCTRL+WORK_OFFSET+r['index']*WORK_BYTES,WORK_BYTES)).hex(),
            'retained_ranges_unchanged':True,'retained_bytes':sum(len(raw) for _,raw in retained),
            'retained_ranges':[{'pointer':a,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()} for a,raw in retained],
            'unit_work_constructor_executed':False,'scene_placement_executed':False})
        if any(bytes.fromhex(r['work_hex'])):raise RuntimeError('enemy record unexpectedly created unit work')
        return deepcopy(r)

    def _hook(self,uc,address,size,context):
        if not self.enemy_loading:return super()._hook(uc,address,size,context)
        sp=uc.reg_read(UC_X86_REG_ESP)
        if address==0x453540:
            if self.enemy_mode!='actual_school' or uc.reg_read(UC_X86_REG_ECX)!=TACT or self.read(sp)!=0x453493 \
                    or self.read(0x7F4488,'h')!=5:raise RuntimeError('enemy natural school entry')
        if address==0x4DA450:self.begin_record(sp)
        if address==0x4DFC20:
            profile,destination=self.read(sp+4),self.read(sp+8)
            r=self.enemy_record;expected=SCRATCH if r['identity']<200 else 0x72ED88+(r['identity']-200)*48
            if (profile,destination,self.read(sp))!=(expected,r['record_pointer'],0x4DA48D):
                raise RuntimeError('enemy exact profile/numeric arguments')
            r.update({'profile_pointer':profile,'profile_hex':bytes(uc.mem_read(profile,48)).hex()})
        if address==0x4E0A00:
            if self.read(sp+4)!=self.enemy_record['record_pointer'] or self.read(sp)!=0x4E08C8:
                raise RuntimeError('enemy exact normalization arguments')
        if address==0x56CEC0:
            target,byte,count=[self.read(sp+i) for i in (4,8,12)];r=self.enemy_record
            allowed=[(r['record_pointer'],176,0x4DFC73)]
            if r['identity']<200:allowed.append((SCRATCH,48,0x4DA63D))
            if byte or (target,count,self.read(sp)) not in allowed:raise RuntimeError('enemy exact clear ownership')
            self.primitive_write(target,bytes(count));r['clears'].append({'pointer':target,'bytes':count,'caller_return_va':hex(self.read(sp))})
            self._stub_return(target,0);return
        if address==0x4680B0:
            if self.enemy_mode!='actual_school' or (uc.reg_read(UC_X86_REG_ECX),self.read(sp),self.read(sp+4))!=(UNITCTRL,0x453630,249):
                raise RuntimeError('enemy exact natural constructor stop')
            self.enemy_snapshot=self.finish_record();self.stop_reason='before_first_scene_unit_work_constructor';uc.emu_stop();return
        if address in self.enemy_code:self.visited.add(address);return
        if address==0x56CE80:return ExitEmulator._hook(self,uc,address,size,context)
        if address==RETURN:uc.emu_stop();return
        raise RuntimeError(f'undeclared enemy record code {address:#x}')

    def resources(self,name,commands=()):
        self.enemy_loading=False;result=super().resources(name,commands)
        result.update({'scene_unit_record_prepared':False,'scene_unit_record':None})
        if not result['ready']:return result
        self.enemy_mode='actual_school';self.enemy_ordinal=0;self.enemy_record=None;self.enemy_loading=True
        self.clear_trace('tactical_startup');self.stop_reason=None
        self.uc.emu_start(self.uc.reg_read(UC_X86_REG_EIP),RETURN,timeout=30_000_000,count=1_000_000)
        if self.stop_reason!='before_first_scene_unit_work_constructor':raise RuntimeError('enemy school missed exact boundary')
        self.enemy_loading=False
        result.update({'scene_unit_record_prepared':True,'scene_unit_record':self.enemy_snapshot,'stop_reason':self.stop_reason})
        result['phases'].append({'phase':'native_first_scene_template_record','coverage':self.coverage()})
        return result

    def declared_templates(self):
        records=[];self.enemy_mode='declared_template_driver';self.enemy_loading=True
        for ordinal in range(self.enemy_inputs['count']):
            self.enemy_ordinal=ordinal;sp=STACK+0xFF00;self.write(sp,RETURN)
            self.write(sp+4,self.enemy_inputs['pointer']+ordinal*84)
            self.write(sp+8,UNITCTRL+RECORD_OFFSET+(249-ordinal)*176)
            self.uc.reg_write(UC_X86_REG_ESP,sp);self.uc.reg_write(UC_X86_REG_ECX,0)
            self.clear_trace('tactical_startup')
            self.uc.emu_start(0x4DA450,RETURN,timeout=1_000_000,count=100_000)
            if self.uc.reg_read(UC_X86_REG_EIP)!=RETURN or self.uc.reg_read(UC_X86_REG_ESP)!=sp+4:
                raise RuntimeError('declared record native cdecl return/stack')
            r=self.finish_record();r['coverage']=self.coverage();records.append(r)
        self.enemy_loading=False
        return {'evidence_kind':'declared_scene5_template_record_driver','records':records,
            'input_character_directory':'original EXE character-definition table selected by4DA5F0; persistent school growth directory is not read',
            'school_enemy_loop_executed':False,'unit_work_constructors_executed':False,**AUTHORITY}


def report():
    e=SchoolEnemyRecordsEmulator()
    if not e.run_planning('enemy_record_upstream')['school_data_prepared']:raise RuntimeError('enemy school prefix missing')
    checkpoint=[(a,bytes(e.uc.mem_read(a,b-a+1))) for a,b,_ in e.uc.mem_regions()];cpu=e.uc.context_save()
    declared=e.declared_templates();cases=[]
    for name,commands in [('initial',()),('student9_waiting',[('student',9,-1)]),
        ('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1),('student',9,-1)]),
        ('teacher_only',[('student',3,-1),('student',4,-1),('student',9,-1)]),('teacher_waiting',[('teacher',101,-1)])]:
        for at,raw in checkpoint:e.uc.mem_write(at,raw)
        e.uc.context_restore(cpu);e.enemy_loading=False;e.enemy_record=None;e.stop_reason=None
        cases.append(e.resources(name,commands));print('Native scene record '+name+': '+str(cases[-1]['scene_unit_record_prepared']),flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,'scene_inputs':e.enemy_inputs,
        'declared_template_diagnostic':declared,'cases':cases,
        'boundary':'Actual first scene template record only; stop before4680B0 work. All35 record transformations use declared driver calls.',**AUTHORITY}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True);args=p.parse_args();path=ROOT/args.out
    if path.exists():p.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
