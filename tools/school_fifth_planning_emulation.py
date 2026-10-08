"""Actual 4/5 course-to-Chapter018 CPU continues through workroom and school.

Reuse only phase-specific API boundaries from the older return audit. Its
upstream initialization and campaign snapshots are never executed or copied.
"""
import argparse
from copy import deepcopy
import hashlib
import struct

from unicorn.x86_const import UC_X86_REG_EIP
from tools.school_fifth_week_emulation import SchoolFifthWeekEmulator, FIFTH_RESOURCES
from tools.workroom_return_emulation import (
    WorkroomReturnEmulator, WORKROOM, GRAPHICS, FONT_IMPORT, WORK_NATIVE, WORK_STUBS)
from tools.school_dispatch_emulation import (
    SchoolDispatchEmulator, GROUP_TASK, PERSON_TASK, SCHOOL_NATIVE, SCHOOL_STUBS)
from tools.school_boot_emulation import SchoolBootEmulator, BOOT_GRAPHICS, BOOT_NATIVE, BOOT_STUBS
from tools.school_course_result_handoff_emulation import RESOURCE_ROOT
from tools.adv_return_state_emulation import CONTROLLER
from tools.scene5_script_emulation import VM
from tools.tactics_exit_emulation import ExitEmulator, ROOT, SOURCE, SOURCE_SHA256, TASK, STACK, report_text
from tools.new_game_school_emulation import STATE, STATE_SIZE
from tools.battle_preparation_emulation import PACKAGE_BASE,PACKAGE_STRIDE
from tools.school_course_unlock_emulation import AUTHORITY

RESOURCES = FIFTH_RESOURCES+('adv/dat/ch002.ybc','adv/dat/chapter205.ybc')
EVIDENCE = ROOT/'analysis/school-fifth-planning-v2-20261008.json'
EVIDENCE_SHA256 = '56459f057bb1faa1d51e3b665449240e15fdd0c60e4161830c09e5deacc92e7c'


class SchoolFifthPlanningEmulator(SchoolFifthWeekEmulator):
    _raw_path = staticmethod(WorkroomReturnEmulator._raw_path)
    _thread = WorkroomReturnEmulator._thread
    _source_resource_event = SchoolBootEmulator._source_resource_event
    boot_control_snapshot = SchoolBootEmulator.boot_control_snapshot
    school_task_snapshot = SchoolDispatchEmulator.school_task_snapshot

    def __init__(self, *, continue_ready=True, school_key_ready=True):
        if any(type(v) is not bool for v in (continue_ready,school_key_ready)):
            raise ValueError('readiness must be boolean')
        super().__init__()
        self._function_ranges += WORK_NATIVE+SCHOOL_NATIVE
        self._stubs.update(WORK_STUBS | SCHOOL_STUBS | BOOT_STUBS)
        self.uc.mem_map(GRAPHICS,0x800000)
        self.uc.mem_map(GROUP_TASK,0x60000)
        self.uc.mem_map(BOOT_GRAPHICS,0x2800000)
        self.write(0x5920A0,FONT_IMPORT)
        self.continue_ready,self.school_key_ready = continue_ready,school_key_ready
        self.workroom_background_path = 'data/adv/bin/bg002_b.bin'
        self.work_consumed,self.ch002_consumed,self.school_consumed = None,None,None
        self.work_events,self.school_events,self.boot_events = [],[],[]
        self.work_yields = 0
        self.work_allocated = False
        self.school_allocated = []
        self.group_started,self.group_initialized = False,False
        self.person_started,self.person_resource_initialized = False,False
        self.person_idle_yields = 0
        self._ran_planning = False

    def _path(self,pointer):
        if getattr(self,'phase',None) not in ('workroom','ch002_adv'):
            return super()._path(pointer)
        path = self._raw_path(self.uc,pointer).removeprefix('data/')
        if path not in ('adv/dat/ch002.ybc','adv/dat/chapter205.ybc'):
            raise RuntimeError('undeclared fifth-week workroom ADV resource: '+path)
        return path

    def _write_hook(self,uc,access,address,size,value,context):
        if getattr(self,'stage',None) not in ('fifth_workroom','fifth_school'):
            return super()._write_hook(uc,access,address,size,value,context)
        if STACK <= address and address+size <= STACK+0x10000:
            return
        # Never permit a second date advance, growth, MVP or character rewrite.
        if address < 0x7A5292 and address+size > 0x7A528E:
            raise RuntimeError('planning write outside finite guard: calendar')
        if address < PACKAGE_BASE+45*PACKAGE_STRIDE and address+size > PACKAGE_BASE:
            raise RuntimeError('planning write outside finite guard: role package/MVP')
        allowed = [(0,4),(STATE,STATE+STATE_SIZE),(WORKROOM,WORKROOM+0x14580),
            (GROUP_TASK,GROUP_TASK+0x1419C),(PERSON_TASK,PERSON_TASK+0x3A5E4),
            (0x7D57C0,0x7D6A36),(0x7A4A0C,0x7A4AD0),
            (0x7A4AD4,0x7A4AE1),(0x7A4E18,0x7A4E20),
            (0x7A4E60,0x7A4E64),(0x7E11A0,0x7E11A2),(CONTROLLER+0x2C,CONTROLLER+0x34),
            (TASK+0x24,TASK+0x2C),(VM,VM+0x9400)]
        allowed += [(VM+0x446+i*0xAB8,VM+0x448+i*0xAB8) for i in range(56)]
        if not any(a <= address and address+size <= b for a,b in allowed):
            raise RuntimeError(f'planning write outside finite guard: {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        self.writes.append((address,size,value & ((1 << (size*8))-1)))

    def _hook(self,uc,address,size,context):
        phase = getattr(self,'phase',None)
        if phase == 'workroom' and WorkroomReturnEmulator._workroom_boundary(self,uc,address,size,context):
            return
        if phase == 'school_dispatch' and SchoolDispatchEmulator._school_dispatch_boundary(self,uc,address,size,context):
            return
        if phase in ('school_group_boot','school_person_boot') and SchoolBootEmulator._school_boot_boundary(self,uc,address,size,context):
            return
        if phase == 'ch002_adv':
            if address == 0x4D1A80:
                if self.ch002_consumed is not None or self.read(CONTROLLER+0x2C) != 1 \
                        or self.read(CONTROLLER+0x30) != 6 or self.active_path != 'adv/dat/ch002.ybc' \
                        or self.read(VM+4,'B') != 1 or self.read(VM+0x1C) != 0 or self.read(VM+0x92DC,'i') != 9:
                    raise RuntimeError('CH002 requires actual fifth-week workroom request6/next9')
                self.ch002_consumed = {'state':6,'pending_flag':1,'path':self.active_path,'next_task':9,
                    'driver_boundary':'consume_actual_request_without_scheduler_constructor'}
                self.write(CONTROLLER+0x2C,0)
            if address == 0x4D0750:
                return ExitEmulator._hook(self,uc,address,size,context)
            if address in (0x4DB270,0x4DB120,0x4DB230):
                self.stub_calls['declared_ch002_fade_'+hex(address)] += 1
                self._stub_return(1 if address == 0x4DB270 else 0,0)
                return
        if phase in ('workroom','school_dispatch','school_group_boot','school_person_boot') \
                and any(a <= address < b for a,b in WORK_NATIVE+SCHOOL_NATIVE+BOOT_NATIVE):
            return ExitEmulator._hook(self,uc,address,size,context)
        return super()._hook(uc,address,size,context)

    def run_planning(self,name):
        if self._ran_planning:
            raise RuntimeError('single-run fifth planning probe')
        self._ran_planning = True
        upstream = deepcopy(super().run_fifth(name))
        if not upstream['fifth_completed']:
            raise RuntimeError('missing actual Chapter018 END')
        before = {'school':self.school_snapshot(),'roles':self.fifth_snapshot(),'counts':self.counts()}
        self.fifth_phase = False
        self.phase = 'workroom'
        self.clear_trace('fifth_workroom')
        self.stop_reason = None
        requests,loads = len(self.state_requests),len(self.loads)
        self.call(0x49E2B0)
        if self.read(0x7A4AD4) != WORKROOM:
            raise RuntimeError('workroom not constructed')
        self._thread(0x4A1570,WORKROOM)
        work_state = {'visited':self.read(0x7A4E62,'h'),'flags':self.fifth_snapshot()['flags'],
            'phase':self.read(WORKROOM+0x30,'h'),'news_count':self.read(WORKROOM+0x1457C,'h')}
        work_coverage = self.coverage()
        if self.stop_reason is None:
            self.phase = 'ch002_adv'
            self.external['key_ready'] = self.school_key_ready
            self.max_yields = 6000 if self.school_key_ready else 1000
            self.yields,self.frame_index = 0,-1
            self.thread(0x4D1A80)
        before_boot = self.school_snapshot()
        constructed = False
        if self.stop_reason is None and self.read(CONTROLLER+0x2C) == 1 and self.read(CONTROLLER+0x30) == 9:
            self.clear_trace('fifth_school')
            self.phase = 'school_dispatch'
            self.call(0x49E2B0)
            constructed = self.school_allocated == [GROUP_TASK,PERSON_TASK]
            if not constructed:
                raise RuntimeError('school dispatch did not construct both tasks')
            self._function_ranges += BOOT_NATIVE
            self.phase = 'school_group_boot'
            self._thread(0x4AB7A0,GROUP_TASK)
            if not self.group_initialized:
                raise RuntimeError('missing school menu boundary')
            self.phase = 'school_person_boot'
            self.stop_reason = None
            self._thread(0x4B8D50,PERSON_TASK)
            if not self.person_resource_initialized:
                raise RuntimeError('missing person idle boundary')
        return {'name':name,'upstream':{'state_requests':upstream['state_requests'],'after':upstream['after']},
            'declared_inputs':{'continue_ready':self.continue_ready,'school_key_ready':self.school_key_ready},
            'before':before,'before_boot':before_boot,'after':{'school':self.school_snapshot(),
                'roles':self.fifth_snapshot(),'counts':self.counts()},
            'work_state':work_state,'work_consumed':self.work_consumed,'ch002_consumed':self.ch002_consumed,
            'school_consumed':self.school_consumed,'work_events':self.work_events,
            'school_events':self.school_events,'boot_events':self.boot_events,
            'state_requests':self.state_requests[requests:],'loads':deepcopy(self.loads[loads:]),
            'school_constructed':constructed,'school_data_prepared':self.group_initialized and self.person_resource_initialized,
            'school_control':self.boot_control_snapshot() if constructed else None,
            'pending_flag':self.read(CONTROLLER+0x2C),'pending_state':self.read(CONTROLLER+0x30),
            'active_path':self.active_path,'stop_reason':self.stop_reason,
            'work_coverage':work_coverage,'coverage':self.coverage(),**AUTHORITY}


def report():
    cases = []
    for name,inputs in [('complete',{}),('continue_wait',{'continue_ready':False}),
            ('key_wait',{'school_key_ready':False})]:
        cases.append(SchoolFifthPlanningEmulator(**inputs).run_planning(name))
        print('Actual fifth school case: '+name,flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,
        'evidence_kind':'same_cpu_4_5_workroom_ch002_school_data_prefix','cases':cases,
        'script_sha256':{p:hashlib.sha256((RESOURCE_ROOT/p).read_bytes()).hexdigest() for p in RESOURCES},
        'limitations':['Inherits actual course/Chapter016/017/week/Chapter018 CPU and all declared predecessor boundaries.',
            'Heap, scheduler registration, UI/font/drawing/audio and continue input are explicit API boundaries.',
            'Native school group initialization stops before menu body; personal task stops at native idle.',
            'School data prefix is not full original interactive menu or live witness; next course settlement is not executed.'],**AUTHORITY}


def exported_fixture(data):
    keys = ('name','before','before_boot','after','work_state','state_requests','loads',
        'work_consumed','ch002_consumed','school_consumed','school_data_prepared',
        'school_control','pending_flag','pending_state','active_path','stop_reason')
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,
        'source_report_sha256':hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),
        'cases':[{k:deepcopy(c[k]) for k in keys} for c in data['cases']],**AUTHORITY}


def exported_rules(data):
    image = SOURCE.read_bytes()
    # Source adventure5 is the first native 4/5 offer. Store table inputs,
    # never the fixture's generated school snapshot.
    base = 0x73BED0-0x400000+5*0x100
    template = {'id':5,'enabled':image[base+1],'month':image[base+2],'week':image[base+3],
        'metadata':image[base+4],'limit':image[base+5],'kind':image[base+6],
        'ordinal':image[base+7],'condition':image[base+14],
        'record_sha256':hashlib.sha256(image[base:base+0x100]).hexdigest()}
    if [template[k] for k in ('enabled','month','week','kind','ordinal','condition')] != [1,4,5,4,5,1]:
        raise ValueError('fifth-week adventure template differs')
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,
        'source_report_sha256':hashlib.sha256(EVIDENCE.read_bytes()).hexdigest(),
        'script_sha256':deepcopy(data['script_sha256']),'required_date':[4,5],
        'entry_state':8,'adv_state':6,'school_state':9,'workroom_background_id':6,
        'selected_school_story':'adv/dat/chapter205.ybc','adventure_template':template,
        'source_functions':{'workroom':'0x4a1570','group_prefix':'0x4a5ce0',
            'adventure_unlock':'0x4a17b0','adventure_list':'0x4a1c70','course_unlock':'0x4a2ba0',
            'reconcile':'0x4a5f40','person':'0x4b8d50'},
        'original_menu_body_executed':False,**AUTHORITY}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True)
    args = parser.parse_args()
    path = ROOT/args.out
    if path.exists():
        parser.error('use a new evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
