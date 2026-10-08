"""Continue the real 4/5 CH001 load through Chapter018, before state8 body."""
import argparse
from copy import deepcopy
import hashlib
import struct

from unicorn.x86_const import UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_story_week_emulation import SchoolStoryWeekEmulator, RESOURCES
from tools.school_course_result_handoff_emulation import RESOURCE_ROOT
from tools.new_week_adv_emulation import NEW_ADV_NATIVE, MOVIE_STUBS, ADV_GLOBALS
from tools.adv_return_state_emulation import CONTROLLER
from tools.scene5_script_emulation import VM
from tools.tactics_exit_emulation import ExitEmulator, ROOT, SOURCE_SHA256, TASK, STACK, report_text
from tools.school_course_unlock_emulation import AUTHORITY

FIFTH_RESOURCES = RESOURCES+('adv/dat/chapter018.ybc',)
EVIDENCE = ROOT/'analysis/school-fifth-week-v2-20261008.json'
EVIDENCE_SHA256 = 'a7cf35d5e3bfe555e232a09917cb816f8daaf55a308cbf5345a2fd3451fc23f1'


def exported_fixture(data):
    keys = ('name','upstream','before','after','consumed_request','declared_readiness',
        'loads','movie_events','state_requests','active_path','next_task','vm_active',
        'pending_flag','pending_state','stop_reason','fifth_completed','workroom_body_executed')
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,
        'source_image_sha256':SOURCE_SHA256,
        'cases':[{k:deepcopy(c[k]) for k in keys} for c in data['cases']],**AUTHORITY}


def exported_rules(data):
    raw = (RESOURCE_ROOT/'adv/dat/chapter018.ybc').read_bytes()
    effects = []
    for at,op,operands in ((0xF90,151,[2,1]),(0xF9C,91,[6,2])):
        if struct.unpack_from('<HH',raw,at) != (op,12) or \
                list(struct.unpack_from('<2I',raw,at+4)) != [0x20000000+v for v in operands]:
            raise ValueError('Chapter018 effect tail differs')
        effects.append({'offset':at,'opcode':op,'operands':operands})
    return {'schema_version':1,'source_report_sha256':EVIDENCE_SHA256,
        'source_image_sha256':SOURCE_SHA256,'script_sha256':deepcopy(data['script_sha256']),
        'required_date':[4,5],'entry_script':'adv/dat/ch001.ybc','selected_script':'adv/dat/chapter018.ybc',
        'entry_state':6,'next_task':8,'exit_state':8,'effectful_tail':effects,
        'entry_adv_globals':deepcopy(data['cases'][0]['before']['adv_globals']),
        'flag_writes':{'0x7a55f6':2,'0x7e11a0':1},'adv_global_writes':{'0x7a5292':6},
        'source_handlers':{'opcode151':'0x4c4750','opcode91':'0x4d0da0'},
        'workroom_body_executed':False,**AUTHORITY}


class SchoolFifthWeekEmulator(SchoolStoryWeekEmulator):
    def __init__(self, *, ui_ready=True, key_ready=True, fade_ready=True):
        if any(type(v) is not bool for v in (ui_ready,key_ready,fade_ready)):
            raise ValueError('readiness must be boolean')
        super().__init__()
        self._function_ranges += NEW_ADV_NATIVE
        self._stubs.update(MOVIE_STUBS)
        self.fifth_inputs = {'ui_ready':ui_ready,'key_ready':key_ready,'fade_ready':fade_ready}
        self.fifth_phase = False
        self.fifth_consumed = None
        self.movie_events = []
        self._ran_fifth = False

    def _path(self,pointer):
        if not self.fifth_phase:
            return super()._path(pointer)
        raw = bytes(self.uc.mem_read(pointer,256)).split(bytes([0]))[0]
        path = '/'.join(p for p in raw.decode('ascii').replace(chr(92),'/').lower().split('/') if p).removeprefix('data/')
        if len(raw) == 256 or path not in FIFTH_RESOURCES:
            raise RuntimeError('undeclared fifth-week resource: '+path)
        return path

    def _write_hook(self,uc,access,address,size,value,context):
        if getattr(self,'stage',None) == 'fifth_week':
            if STACK <= address and address+size <= STACK+0x10000:
                return
            allowed = [(a,a+2) for a in ADV_GLOBALS+(0x7A55F6,0x7E11A0)]
            allowed += [(0x7A4E18,0x7A4E20),(VM,VM+0x9400),
                (CONTROLLER+0x2C,CONTROLLER+0x34),(TASK+0x24,TASK+0x2C)]
            allowed += [(VM+0x446+i*0xAB8,VM+0x448+i*0xAB8) for i in range(56)]
            if any(a <= address and address+size <= b for a,b in allowed):
                self.writes.append((address,size,value & ((1 << (size*8))-1)))
                return
            raise RuntimeError(f'fifth-week write outside finite guard: {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        return super()._write_hook(uc,access,address,size,value,context)

    def fifth_snapshot(self):
        result = self.week_snapshot()
        result['adv_globals'] = {hex(a):self.read(a,'h') for a in ADV_GLOBALS}
        return result

    def _hook(self,uc,address,size,context):
        if getattr(self,'fifth_phase',False):
            sp = uc.reg_read(UC_X86_REG_ESP)
            if address == 0x4D1A80:
                if self.fifth_consumed is not None or self.read(CONTROLLER+0x2C) != 1 \
                        or self.read(CONTROLLER+0x30) != 6 or self.active_path != 'adv/dat/ch001.ybc' \
                        or self.read(VM+4,'B') != 1 or self.read(VM+0x1C) != 0 or self.read(VM+0x92DC,'i') != 8:
                    raise RuntimeError('requires actual pending6/CH001/next8 after native week')
                self.fifth_consumed = {'state':6,'pending_flag':1,'path':self.active_path,'next_task':8,
                    'driver_boundary':'consume_actual_request_without_scheduler_constructor'}
                self.write(CONTROLLER+0x2C,0)
            if address == 0x4D0750:
                # This END cleanup is native, not another course-confirmation
                # checkpoint. Keep the full fifth-week trace and write guard.
                return ExitEmulator._hook(self,uc,address,size,context)
            if address in (0x4DB270,0x4DB120,0x4DB230):
                self.stub_calls['declared_fifth_fade_'+hex(address)] += 1
                self._stub_return(int(self.fifth_inputs['fade_ready']) if address == 0x4DB270 else 0,0)
                return
            if address == 0x4128F0:
                if (self.read(sp+4),self.read(sp+8)) != (0x39,0):
                    raise RuntimeError('undeclared movie skip key')
                self.stub_calls['declared_fifth_movie_skip_key'] += 1
                self._stub_return(int(self.fifth_inputs['key_ready']),8)
                return
            if address in MOVIE_STUBS:
                name,pop = MOVIE_STUBS[address]
                self.stub_calls[name] += 1
                if name == 'movie_resource':
                    raw = bytes(uc.mem_read(self.read(sp+4),256)).split(bytes([0]))[0]
                    path = '/'.join(p for p in raw.decode('ascii').replace(chr(92),'/').lower().split('/') if p)
                    if path != 'data/adv/bin/tc0405.bin' or self.read(sp+8) != 0x15:
                        raise RuntimeError('undeclared fifth-week movie')
                    source = (RESOURCE_ROOT.parent/path).read_bytes()
                    self.movie_events.append({'path':path,'sha256':hashlib.sha256(source).hexdigest(),
                        'resource_slot':0x15,'body_executed':False})
                    self._stub_return(0,pop)
                else:
                    self._stub_return(self.read(sp+12),pop)
                return
            if any(a <= address < b for a,b in NEW_ADV_NATIVE):
                return ExitEmulator._hook(self,uc,address,size,context)
        return super()._hook(uc,address,size,context)

    def run_fifth(self,name):
        if self._ran_fifth:
            raise RuntimeError('single-run fifth-week probe')
        self._ran_fifth = True
        previous = deepcopy(super().run_continuation(name))
        if previous['stop_reason'] is not None or previous['active_path'] != 'adv/dat/ch001.ybc':
            raise RuntimeError('missing completed native 4/5 predecessor')
        before = self.fifth_snapshot()
        self.week_phase = False
        self.route_running = False
        self.result_running = True
        self.fifth_phase = True
        self.external.update(self.fifth_inputs)
        self.max_yields = 6000 if all(self.fifth_inputs.values()) else 1200
        self.yields = 0
        self.frame_index = -1
        self.stop_reason = None
        self.clear_trace('fifth_week')
        start,loads,requests = len(self.commands),len(self.loads),len(self.state_requests)
        self.thread(0x4D1A80)
        completed = self.stop_reason is None and self.active_path == 'adv/dat/chapter018.ybc' and self.read(VM+4,'B') == 0
        return {'name':name,'upstream':{'state_requests':previous['state_requests'][:],
                'after_week':deepcopy(previous['after_week']),'active_path':previous['active_path']},
            'before':before,'after':self.fifth_snapshot(),'consumed_request':self.fifth_consumed,
            'declared_readiness':self.fifth_inputs,'commands':deepcopy(self.commands[start:]),
            'loads':deepcopy(self.loads[loads:]),'movie_events':self.movie_events,
            'state_requests':self.state_requests[requests:],'active_path':self.active_path,
            'next_task':self.read(VM+0x92DC,'i'),'vm_active':self.read(VM+4,'B'),
            'pending_flag':self.read(CONTROLLER+0x2C),'pending_state':self.read(CONTROLLER+0x30),
            'stop_reason':self.stop_reason,'fifth_completed':completed,'coverage':self.coverage(),
            'workroom_body_executed':False,**AUTHORITY}


def report():
    cases = []
    for name,inputs in [('complete',{}),('key_wait',{'key_ready':False}),
            ('ui_wait',{'ui_ready':False}),('fade_wait',{'fade_ready':False})]:
        cases.append(SchoolFifthWeekEmulator(**inputs).run_fifth(name))
        print('Native fifth-week case: '+name,flush=True)
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,
        'evidence_kind':'same_cpu_course_to_4_5_ch001_chapter018_exit',
        'script_sha256':{p:hashlib.sha256((RESOURCE_ROOT/p).read_bytes()).hexdigest() for p in FIFTH_RESOURCES},
        'cases':cases,'limitations':['Shares original new-game/course/MVP/Chapter016/017/week CPU without resetting roles.',
            'Inherited 4/4 date, probe flags, allocation, presentation and scheduler boundaries remain explicit.',
            'Native CH001 date branches, Chapter018 effectful tail and pending8 execute.',
            'TC0405 movie filename/hash is witnessed but drawing, audio and portrait APIs remain simulated.',
            'Stops before state8 workroom constructor/control and school initialization; no live/save authority.'],**AUTHORITY}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True)
    args = parser.parse_args()
    target = ROOT/args.out
    if target.exists():
        parser.error('use a new evidence path')
    target.write_text(report_text(report()),encoding='utf-8',newline='\n')
    print(target)
