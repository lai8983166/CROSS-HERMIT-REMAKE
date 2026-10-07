"""Continue original course results through both scenes and native state7.

Same isolated CPU as the source new game/course audit. Presentation readiness,
4/4 date, result allocation and scheduler consumption remain declared boundaries.
"""
import argparse
from copy import deepcopy
import hashlib

from unicorn.x86_const import UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_course_result_handoff_emulation import (
    CourseResultHandoffEmulator, RESOURCE_ROOT, PATHS)
from tools.school_course_settlement_emulation import IDS
from tools.week_settlement_emulation import WEEK_NATIVE, WeekSettlementEmulator
from tools.adv_week_handoff_emulation import START_NATIVE
from tools.adv_chapter_emulation import CHAPTER_NATIVE
from tools.adv_return_state_emulation import CONTROLLER
from tools.scene5_script_emulation import Scene5Emulator, VM
from tools.battle_preparation_emulation import CHAR_BASE, CHAR_STRIDE, PACKAGE_BASE, PACKAGE_STRIDE
from tools.tactics_exit_emulation import ExitEmulator, ROOT, SOURCE_SHA256, TASK, STACK, report_text
from tools.week_settlement_fixture import fixture as week_fixture
from tools.school_course_unlock_emulation import AUTHORITY

RESOURCES = PATHS+('adv/dat/chapter017.ybc','adv/dat/ch001.ybc')
EVIDENCE = ROOT/'analysis/school-story-week-v3-20261008.json'
EVIDENCE_SHA256 = '582a3098b6bcf217c083c54f57e6c3d6b7ad0a81775c500b75aef64900d38bf1'


def exported_fixture(data):
    keys = ('name','story_completed','course_result','initial_week','after_story','before_week',
        'after_week','week_executed','consumed_request','course_request_consumed',
        'state_requests','active_path','stored_next_task','pending_flag','pending_state','stop_reason')
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,
        'source_image_sha256':SOURCE_SHA256,'week_rules':deepcopy(data['week_rules']),
        'cases':[{k:deepcopy(c[k]) for k in keys} for c in data['cases']],**AUTHORITY}


def exported_rules(data):
    initial = data['cases'][0]['initial_week']
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,
        'source_report_sha256':EVIDENCE_SHA256,'script_sha256':deepcopy(data['script_sha256']),
        'week_rules':deepcopy(data['week_rules']),
        'baseline':{'flags':deepcopy(initial['flags']),'availability':deepcopy(initial['availability']),
            'item_flags':deepcopy(initial['item_flags']),
            'participants':[{k:deepcopy(c[k]) for k in ('character_id','unlock_flags','equipped_skills','equipped_items')}
                for c in initial['participants']]},
        'baseline_scope':'Availability, equipment and unlocks are captured after source new-game joins. Flags are inherited declared probe inputs (0,8,0,99); not asserted as live game initial flags.',
        'entry':[4,4],'arrival':[4,5],'request_state':7,'next_script':'adv/dat/ch001.ybc',
        'next_task':8,**AUTHORITY}


class SchoolStoryWeekEmulator(CourseResultHandoffEmulator):
    def __init__(self, *, story_key_ready=True, week_fade_ready=True):
        super().__init__()
        if type(story_key_ready) is not bool or type(week_fade_ready) is not bool:
            raise ValueError('readiness must be boolean')
        self._function_ranges += CHAPTER_NATIVE+WEEK_NATIVE+START_NATIVE
        self._stubs[0x4DB230] = ('week_fade_start',0)
        self.story_key_ready,self.week_fade_ready = story_key_ready,week_fade_ready
        self.week_phase = False
        self.week_entry_snapshot = None
        self.week_events,self.week_start_events = [],[]
        self.consumed_request = None
        self.initial_week = None
        self.course_request_consumed = None

    def initialize(self):
        result = super().initialize()
        self.initial_week = self.week_snapshot()
        return result

    def week_snapshot(self):
        return WeekSettlementEmulator.week_snapshot(self)

    def _path(self,pointer):
        raw = bytes(self.uc.mem_read(pointer,256)).split(b'\0')[0]
        if len(raw) == 256:
            raise RuntimeError('unbounded path')
        path = '/'.join(p for p in raw.decode('ascii').replace(chr(92),'/').lower().split('/') if p).removeprefix('data/')
        if path not in RESOURCES:
            raise RuntimeError('undeclared story/week resource: '+path)
        return path

    def _write_hook(self,uc,access,address,size,value,context):
        if getattr(self,'stage',None) != 'story_week':
            return super()._write_hook(uc,access,address,size,value,context)
        if STACK <= address and address+size <= STACK+0x10000:
            return
        allowed = [(0x7A528E,0x7A5292),(TASK+0x24,TASK+0x2C),
            (CONTROLLER+0x2C,CONTROLLER+0x34),(VM,VM+0x9400)]
        allowed += [(VM+0x446+i*0xAB8,VM+0x448+i*0xAB8) for i in range(56)]
        allowed += [(a,a+2) for a in (0x7A55FA,0x7A4E62,0x7A55F6,0x7E11A0)]
        allowed += [(0x7AACAA+2,0x7AACAA+722)]
        for identity in IDS:
            package = PACKAGE_BASE+identity*PACKAGE_STRIDE
            allowed.append((package+0xF9,package+0xF9+30))
            allowed += [(CHAR_BASE+identity*CHAR_STRIDE+0xB8+k*12,
                         CHAR_BASE+identity*CHAR_STRIDE+0xB9+k*12) for k in range(84)]
        if not any(a <= address and address+size <= b for a,b in allowed):
            raise RuntimeError(f'week write outside finite guard: {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        self.writes.append((address,size,value & ((1 << (size*8))-1)))

    def _hook(self,uc,address,size,context):
        sp = uc.reg_read(UC_X86_REG_ESP)
        if getattr(self,"route_running",False) and address == 0x4D1A80:
            if self.course_request_consumed is not None or self.read(CONTROLLER+0x2C) != 1 \
                    or self.read(CONTROLLER+0x30) != 6:
                raise RuntimeError('ADV requires actual unconsumed course next6 request')
            self.course_request_consumed = {'state':6,'pending_flag':1,
                'driver_boundary':'consume_pending_request_without_scheduler_constructor'}
            self.write(CONTROLLER+0x2C,0)
        if getattr(self,"route_running",False) and address == 0x4CE8F0:
            # Replace only the earlier stop-before-Chapter016 observation policy.
            self.external['key_ready'] = self.story_key_ready
            self.max_yields = 6000 if self.story_key_ready else 200
            self.frame_index += 1
            count = len(self.commands)
            result = Scene5Emulator._hook(self,uc,address,size,context)
            if len(self.commands) > count:
                self.commands[-1]['path'] = self.active_path
            return result
        if getattr(self,"week_phase",False):
            if address == 0x49F4E0:
                if self.consumed_request is not None or self.read(VM+4,'B') != 0 \
                        or self.read(CONTROLLER+0x2C) != 1 or self.read(CONTROLLER+0x30) != 7:
                    raise RuntimeError('requires actual unconsumed Chapter017 next7 request')
                self.consumed_request = {'state':7,'pending_flag':1,'adv_active':0,
                    'source':'native_439e30_after_chapter017_end',
                    'driver_boundary':'consume_pending_request_without_scheduler_constructor'}
                self.write(CONTROLLER+0x2C,0)
            if address in (0x4DB230,0x4DB270,0x4DB120):
                name = {0x4DB230:'fade_start',0x4DB270:'fade_ready',0x4DB120:'fade_release'}[address]
                self.week_start_events.append({'kind':name,'va':hex(address)})
                self.stub_calls['declared_week_'+name] += 1
                self._stub_return(int(self.week_fade_ready) if address == 0x4DB270 else 0,0)
                return
            if address == 0x422360:
                self.yields += 1
                if self.yields > 4:
                    self.stop_reason = 'week_fade_pending_after_settlement'
                    uc.emu_stop()
                    return
            if address in (0x4D3510,0x4D3AA0,0x4D31F0,0x4D34A0):
                event = {'va':hex(address),'caller':hex(self.read(sp))}
                if address == 0x4D3AA0:
                    event['character_id'] = self.read(sp+4,'h')
                self.week_events.append(event)
                if address == 0x4D3510:
                    if self.week_entry_snapshot is not None:
                        raise RuntimeError('duplicate week')
                    self.week_entry_snapshot = self.week_snapshot()
            if any(a <= address < b for a,b in WEEK_NATIVE+START_NATIVE):
                return ExitEmulator._hook(self,uc,address,size,context)
        return super()._hook(uc,address,size,context)

    def run_continuation(self,name):
        course = super().complete(name)
        after_story = self.week_snapshot()
        story_completed = self.stop_reason is None and self.read(VM+4,'B') == 0 \
            and self.active_path == 'adv/dat/chapter017.ybc' and self.state_requests == [6,7]
        story_commands = deepcopy(self.commands)
        story_loads = deepcopy(self.loads)
        story_coverage = self.coverage()
        if story_completed:
            self.route_running = False
            self.week_phase = True
            # Keep the source loader/resource policy active during state7.
            self.result_running = True
            self.yields = 0
            self.week_events.clear()
            self.clear_trace('story_week')
            self.thread(0x49F4E0)
        return {'name':name,'declared_inputs':{'story_key_ready':self.story_key_ready,
            'week_fade_ready':self.week_fade_ready},'course_result':course['after_result'],
            'initial_week':self.initial_week,'after_story':after_story,
            'story_completed':story_completed,'commands':story_commands,'story_loads':story_loads,
            'story_coverage':story_coverage,'consumed_request':self.consumed_request,
            'course_request_consumed':self.course_request_consumed,
            'before_week':self.week_entry_snapshot,'after_week':self.week_snapshot(),
            'week_executed':self.week_entry_snapshot is not None,
            'week_events':self.week_events,'week_start_events':self.week_start_events,
            'loads':deepcopy(self.loads),'state_requests':self.state_requests,
            'active_path':self.active_path,'stored_next_task':self.read(VM+0x92DC,'i'),
            'pending_flag':self.read(CONTROLLER+0x2C),'pending_state':self.read(CONTROLLER+0x30),
            'week_coverage':self.coverage() if story_completed else None,'stop_reason':self.stop_reason,
            'ch001_body_executed':False,**AUTHORITY}


def report():
    cases = []
    for name,inputs in [('complete',{}),('fade_wait',{'week_fade_ready':False}),
                        ('story_wait',{'story_key_ready':False})]:
        cases.append(SchoolStoryWeekEmulator(**inputs).run_continuation(name))
        print('Native continuation complete: '+name,flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,
        'evidence_kind':'isolated_same_cpu_course_story_week_continuation',
        'script_sha256':{p:hashlib.sha256((RESOURCE_ROOT/p).read_bytes()).hexdigest() for p in RESOURCES},
        'week_rules':week_fixture()['rules'],'cases':cases,
        'limitations':['Inherits declared 4/4 date, seed4660, fresh result task and presentation/resource readiness.',
            'Original initialization, course growth/confirmation/MVP and Chapter016/017 control flow share one CPU.',
            'Native pending7 is consumed by a declared driver; task scheduler construction is not executed.',
            'Native state7 performs full week body then loads CH001 with next8 and requests6 when fade ready.',
            'CH001 body and fifth-week school initialization do not execute; no live/original save authority.'],
        **AUTHORITY}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True)
    args = parser.parse_args()
    target = ROOT/args.out
    if target.exists():
        parser.error('use a new evidence path')
    target.write_text(report_text(report()),encoding='utf-8',newline='\n')
    print(target)
