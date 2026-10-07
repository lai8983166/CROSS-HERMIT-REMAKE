"""Native course result/MVP completion and bounded CH003 -> Chapter016 entry.

All writes are isolated. Presentation, button/lock readiness and 4/4 are
declared; real script bytes and control instructions determine completion.
"""
import argparse
from copy import deepcopy
import hashlib
import struct

from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_course_confirmation_emulation import CourseConfirmationEmulator
from tools.school_course_settlement_emulation import IDS
from tools.all_result_emulation import ALL_NATIVE, ALL_EXTERNAL
from tools.adv_route_emulation import NATIVE as ROUTE_NATIVE, RESOURCES
from tools.adv_return_state_emulation import FUNCTIONS as ADV_NATIVE, CONTROLLER
from tools.adv_chapter_emulation import PRESENTATION, TASK_STUBS
from tools.scene5_script_emulation import Scene5Emulator, VM, SCRIPT
from tools.battle_preparation_emulation import PACKAGE_BASE, PACKAGE_STRIDE
from tools.tactics_exit_emulation import ExitEmulator, ROOT, SOURCE, SOURCE_SHA256, TASK, STACK, RETURN, report_text
from tools.school_course_unlock_emulation import AUTHORITY

RESOURCE_ROOT = ROOT/'CROSS HERMIT/CROSS HERMIT/DATA'
PATHS = ('allresult/dat/mvp.ybc','allresult/dat/mvp003.ybc','allresult/dat/mvp004.ybc',
         'allresult/dat/mvp009.ybc','adv/dat/ch003.ybc','adv/dat/chapter016.ybc')
NATIVE = ALL_NATIVE+ROUTE_NATIVE+ADV_NATIVE+((0x4C00C0,0x4C0350),)


def source_rules():
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_SHA256:
        raise ValueError('source differs')
    fields = {'class_count':5,'slots_per_class':4,'eligible_id_limit':13,
        'initial_best':0,'count_cap':5,'month':4,'week':4,'request_state':6,
        'next_task':7,'chapter_number':16}
    signature = ':'.join(map(str,fields.values()))
    return {'source_image_sha256':SOURCE_SHA256,
        'result_fields_sha256':hashlib.sha256(signature.encode()).hexdigest(),
        **fields,'script_sha256':{path:hashlib.sha256((RESOURCE_ROOT/path).read_bytes()).hexdigest() for path in PATHS},
        'initial_counts':[{'character_id':i,'count':0} for i in IDS]}


class CourseResultHandoffEmulator(CourseConfirmationEmulator):
    def __init__(self, *, confirm=True, key_ready=True, max_yields=1200):
        super().__init__()
        if type(confirm) is not bool or type(key_ready) is not bool \
                or type(max_yields) is not int or not 1 <= max_yields <= 2000:
            raise ValueError('invalid declared readiness/budget')
        self._function_ranges += NATIVE
        self._stubs.update(RESOURCES)
        self._stubs.update(TASK_STUBS)
        self._stubs.update(ALL_EXTERNAL)
        self.confirm_input,self.max_yields = confirm,max_yields
        self.external.update(key_ready=key_ready,ui_ready=True)
        self.result_running = False
        self.route_running = False
        self.yields = 0
        self.stop_reason = None
        self.loads,self.state_requests,self.task_entries = [],[],[]
        self.active_path = None
        self.commands = []
        self.frame_index = -1
        self.growth_checkpoint = None
        self.confirmation_checkpoint = None
        self.mvp_coverage = None
        self.write(0x7A4A00,CONTROLLER)
        for index,pointer in enumerate((0x3100000,0x3100010)):
            if index == 0:
                self.uc.mem_map(pointer,0x1000)
            self.write(0x592234+index*4,pointer)
            self._stubs[pointer] = ('critical_section',4)

    def counts(self):
        return [{'character_id':i,'count':self.read(PACKAGE_BASE+i*PACKAGE_STRIDE+0x120,'h')} for i in IDS]

    def _write_hook(self,uc,access,address,size,value,context):
        if getattr(self,'stage',None) == 'course_settlement' and address == TASK+0x30 and size == 2:
            self.writes.append((address,size,value & 0xffff))
            return
        if getattr(self,'stage',None) not in ('course_result_presentation','course_result_route'):
            return super()._write_hook(uc,access,address,size,value,context)
        if STACK <= address and address+size <= STACK+0x10000:
            return
        allowed = [(VM,VM+0x9400),(SCRIPT,SCRIPT+0x10000),(TASK+0x30,TASK+0x34),
            (0x7E1180,0x7E11A0),(CONTROLLER+0x2C,CONTROLLER+0x34),
            (TASK+0x24,TASK+0x2C),(0x7A4E18,0x7A4E20)]
        allowed += [(PACKAGE_BASE+i*PACKAGE_STRIDE+0x120,PACKAGE_BASE+i*PACKAGE_STRIDE+0x122) for i in IDS]
        # Native4CD8D0 clears 56 presentation slots beyond the VM core.
        allowed += [(VM+0x446+i*0xAB8,VM+0x448+i*0xAB8) for i in range(56)]
        if not any(a <= address and address+size <= b for a,b in allowed):
            raise RuntimeError(f'result write outside finite guard: {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}, path={self.active_path}')
        self.writes.append((address,size,value & ((1 << (size*8))-1)))

    def _path(self,pointer):
        raw = bytes(self.uc.mem_read(pointer,256)).split(b'\0')[0]
        if len(raw) == 256:
            raise RuntimeError('unbounded resource path')
        parts = [part for part in raw.decode('ascii').replace('\\','/').lower().split('/') if part]
        if parts and parts[0] == 'data':
            parts.pop(0)
        path = '/'.join(parts)
        if path not in PATHS:
            raise RuntimeError('resource outside declared result/route chain: '+path)
        return path

    def _hook(self,uc,address,size,context):
        if getattr(self,'selection_probe',False) and address == 0x4C0400:
            # Selection-only counterfactual: staged growth is a declared input.
            self.stub_calls['selection_probe_omits_growth'] += 1
            self._stub_return(0,8)
            return
        if not getattr(self,'result_running',False) and not getattr(self,'route_running',False):
            return super()._hook(uc,address,size,context)
        sp = uc.reg_read(UC_X86_REG_ESP)
        if address in (0x4BD870,0x4BDAC0,0x4C1350,0x4D0750,0x4CE210,0x439E30):
            self.task_entries.append({'va':hex(address),'caller':hex(self.read(sp))})
        if address == 0x4BDAC0:
            self.growth_checkpoint = {'school':self.school_snapshot(),'records':self.growth_records(),
                'recipient':self.read(0x7E1180,'h'),'old_count':self.read(0x7E1182,'h'),
                'counts':self.counts(),'coverage':self.coverage()}
            self.clear_trace('course_result_presentation')
        if address == 0x4C1350:
            self.mvp_coverage = self.coverage()
            self.clear_trace('course_confirmation')
        if address == 0x4D0750:
            self.confirmation_checkpoint = {'school':self.school_snapshot(),'records':self.confirmation_records(),
                'coverage':self.coverage()}
            self.clear_trace('course_result_presentation')
        if address == 0x4D3510:
            raise RuntimeError('unexpected week execution in normal course result')
        if address == 0x439E30:
            self.state_requests.append(self.read(sp+4,'i'))
        if address == 0x422360:
            self.yields += 1
            if self.yields > self.max_yields:
                self.stop_reason = 'bounded_pending_result'
                uc.emu_stop()
                return
        if address == 0x4CE8F0:
            self.frame_index += 1
            if self.route_running and self.active_path == 'adv/dat/chapter016.ybc':
                self.stop_reason = 'chapter016_entry_boundary'
                uc.emu_stop()
                return
            count = len(self.commands)
            result = Scene5Emulator._hook(self,uc,address,size,context)
            if len(self.commands) > count:
                self.commands[-1]['path'] = self.active_path
            return result
        if address == 0x4D5EC0:
            buffer,x = self.read(sp+4),self.read(sp+8)
            if not STACK <= buffer <= STACK+0x10000-8 or x not in (0x2E1,0x1BA):
                raise RuntimeError('unexpected result button input')
            self.write(buffer,0)
            self.write(buffer+4,int(self.confirm_input and x == 0x2E1))
            self.stub_calls['declared_result_button'] += 1
            self._stub_return(0,20)
            return
        if address in RESOURCES:
            name,pop = RESOURCES[address]
            self.stub_calls[name] += 1
            value = 0
            if address == 0x42AE20 and self.stage == 'course_settlement':
                raw = bytes(uc.mem_read(self.read(sp+4),128)).split(b'\0')[0]
                if raw != b'data/AllResult/AllResult.bin':
                    raise RuntimeError('unexpected result graphics resource')
                self.stub_calls['declared_result_graphics_boundary'] += 1
                self._stub_return(0,0)
                return
            if name == 'resource_key':
                value = self.read(sp+4)
                self._path(value)
            elif name in ('resource_size','resource_bytes'):
                path = self._path(self.read(sp+4))
                source = (RESOURCE_ROOT/path).read_bytes()
                if len(source) > 0x10000:
                    raise RuntimeError('resource allocation exceeded')
                value = len(source) if name == 'resource_size' else SCRIPT
                if name == 'resource_bytes':
                    self.loads.append({'path':path,'sha256':hashlib.sha256(source).hexdigest()})
                    self.source,self.active_path = source,path
                    uc.mem_write(SCRIPT,source)
            self._stub_return(value,pop)
            return
        if any(a <= address < b for a,b in NATIVE):
            return ExitEmulator._hook(self,uc,address,size,context)
        if address in PRESENTATION:
            self.stub_calls[PRESENTATION[address]] += 1
            self._stub_return(self.read(sp+12),12)
            return
        if address in ALL_EXTERNAL or address in TASK_STUBS:
            name,pop = (ALL_EXTERNAL | TASK_STUBS)[address]
            if address == 0x4CE210:
                raise RuntimeError('native loader was masked')
            self.stub_calls[name] += 1
            value = int(self.external['ui_ready']) if name in ('ui_ready','chapter_fade_ready') else 0
            if address in (0x464C60,0x4075E0):
                value = uc.reg_read(UC_X86_REG_ECX)
            self._stub_return(value,pop)
            return
        return super()._hook(uc,address,size,context)

    def thread(self,entry):
        sp = STACK+0xFF00
        self.write(sp,RETURN)
        self.write(sp+4,0)
        self.uc.reg_write(UC_X86_REG_ESP,sp)
        self.uc.reg_write(UC_X86_REG_ECX,TASK)
        self.uc.emu_start(entry,RETURN,timeout=40_000_000,count=10_000_000)
        if self.stop_reason is None and (self.uc.reg_read(UC_X86_REG_EIP) != RETURN
                or self.uc.reg_read(UC_X86_REG_ESP) != sp+8):
            raise RuntimeError('result/route task exceeded instruction/time or ret4 bounds')

    def complete(self,name,*,count=0,waiting=(),probe=None):
        self.initialize()
        initialized_counts = self.counts()
        self.declare_date(4,4)
        for identity in waiting:
            self.run_move('declared_waiting','student',identity,-1)
        self.run('teaching','mode',group=0)
        self.run('assign','course',group=0,row=2)
        self.clear_trace('course_result_prepare')
        self.call(0x4A6A10)
        self.clear_trace('course_settlement')
        self.uc.mem_write(TASK+0x30,bytes(0x4F74-0x30))
        self.write(0x7F4491,0,'B')
        for identity in IDS:
            self.write(PACKAGE_BASE+identity*PACKAGE_STRIDE+0x120,count,'h')
        self.result_running = True
        self.thread(0x4C1AA0)
        result_completed = self.stop_reason is None
        result_coverage = self.coverage()
        result_requests = self.state_requests[:]
        after_result = {'school':self.school_snapshot(),'counts':self.counts(),
            'growth_records':self.growth_records(),
            'records':self.confirmation_records(),'stored_next_task':self.read(VM+0x92DC,'i'),
            'pending_state':self.read(CONTROLLER+0x30),'pending_flag':self.read(CONTROLLER+0x2C)}
        if result_completed:
            self.result_running = False
            self.route_running = True
            self.clear_trace('course_result_route')
            self.write(TASK,0x5C306C)
            self.write(VM+0x92E1,1,'B')
            self.thread(0x4D1A80)
        return {'name':name,'declared_inputs':{'confirm':self.confirm_input,
            'key_ready':self.external['key_ready'],'max_yields':self.max_yields,'count':count,
            'waiting_students':list(waiting),'counterfactual':probe},
            'initialized_counts':initialized_counts,'growth_checkpoint':self.growth_checkpoint,
            'confirmation_checkpoint':self.confirmation_checkpoint,'after_result':after_result,
            'result_completed':result_completed,'result_requests':result_requests,
            'stop_reason':self.stop_reason,'loads':deepcopy(self.loads),'commands':deepcopy(self.commands),
            'task_entries':deepcopy(self.task_entries),'result_coverage':result_coverage,'mvp_coverage':self.mvp_coverage,
            'route_coverage':self.coverage() if result_completed else None,
            'chapter_body_executed':False,'week_executed':False,**AUTHORITY}


def report():
    probes = selection_probes()
    cases = []
    for emulator,args in [
            (CourseResultHandoffEmulator(),{'name':'course10_complete'}),
            (CourseResultHandoffEmulator(),{'name':'waiting3_complete','waiting':(3,)}),
            (CourseResultHandoffEmulator(),{'name':'count5_cap','count':5,'probe':'declared_prior_count'}),
            (CourseResultHandoffEmulator(confirm=False,max_yields=900),{'name':'confirm_wait'}),
            (CourseResultHandoffEmulator(key_ready=False,max_yields=900),{'name':'mvp_key_wait'})]:
        cases.append(emulator.complete(**args))
        print('Native case complete: '+args['name'],flush=True)
    return {'schema_version':1,'evidence_kind':'isolated_native_course_result_mvp_and_adv_entry',
        'rules':source_rules(),'cases':cases,
        'selection_probes':probes,
        'limitations':['Source new game and course10 run in one CPU; date4/4, zero result task, clock4660 and presentation readiness are declared.',
            'Real MVP dispatch/replacement/dialogue waits/END and result confirmation/count/CH003 load/request6 execute.',
            'Actual CH003 dispatch stops before Chapter016 first instruction; Chapter016/017 body and task7/week do not execute.',
            'Resource I/O/audio/drawing/locks are simulated using exact allowlisted local YBC bytes.',
            'No original save, live gameplay witness or chronological first four weeks.'],**AUTHORITY}


def selection_probes():
    e = CourseResultHandoffEmulator()
    e.initialize()
    e.declare_date(4,4)
    e.run('teaching','mode',group=0)
    e.run('assign','course',group=0,row=2)
    e.selection_probe = True
    result = []
    for name,totals,first in [('tie_3_first',[100,100,100],3),
            ('tie_4_first',[100,100,100],4),('zero_no_recipient',[0,0,0],4),
            ('later_higher',[100,100,101],4)]:
        if first == 4 and name == 'tie_4_first':
            e.clear_trace('planning_rate')
            e.run_move('declared_swap','student',4,0,0)
        for identity,total in zip(IDS,totals):
            e.write(PACKAGE_BASE+identity*PACKAGE_STRIDE+0x20,total,'i')
        e.clear_trace('course_settlement')
        e.write(0x7E1180,-1,'h')
        e.write(0x7E1184,0,'i')
        before = e.school_snapshot()
        records = e.growth_records()
        sp = STACK+0xFF00
        e.write(sp,RETURN)
        e.uc.reg_write(UC_X86_REG_ESP,sp)
        e.uc.reg_write(UC_X86_REG_ECX,TASK)
        e.uc.emu_start(0x4C00C0,RETURN,timeout=15_000_000,count=2_000_000)
        if e.uc.reg_read(UC_X86_REG_EIP) != RETURN or e.uc.reg_read(UC_X86_REG_ESP) != sp+4:
            raise RuntimeError('selection probe exceeded bounds')
        result.append({'name':name,'declared_staged_totals':totals,'before':before,
            'records':records,'counts':e.counts(),'recipient':e.read(0x7E1180,'h'),
            'best':e.read(0x7E1184,'i'),'coverage':e.coverage(),
            'counterfactual':True,'growth_executed':False,**AUTHORITY})
    return result


def fixture(data):
    value = deepcopy(data)
    value['source_report_sha256'] = hashlib.sha256(report_text(data).encode()).hexdigest()
    for row in value['cases']:
        for key in ('result_coverage','route_coverage','task_entries','mvp_coverage'):
            row.pop(key)
        for key in ('growth_checkpoint','confirmation_checkpoint'):
            if row[key] is not None:
                row[key].pop('coverage')
    for row in value['selection_probes']:
        row.pop('coverage')
    return value


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out')
    p.add_argument('--godot-out')
    p.add_argument('--rules-out')
    a = p.parse_args()
    if a.rules_out and not a.out and not a.godot_out:
        outputs = [(ROOT/a.rules_out,source_rules())]
    elif a.out and a.godot_out and not a.rules_out:
        paths = [ROOT/a.out,ROOT/a.godot_out]
        if paths[0].resolve() == paths[1].resolve() or any(path.exists() for path in paths):
            p.error('use distinct new output paths')
        data = report()
        outputs = list(zip(paths,(data,fixture(data))))
    else:
        p.error('use --rules-out alone, or --out with --godot-out')
    for path,value in outputs:
        payload = report_text(value)
        with path.open('x',encoding='utf-8',newline='\n') as f:
            f.write(payload)
        print(f'{path}: SHA-256 {hashlib.sha256(payload.encode()).hexdigest()}')


if __name__ == '__main__':
    main()
