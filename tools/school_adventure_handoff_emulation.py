"""Actual fifth-school checkpoint commits and enters native first-round preparation.

The confirmed menu result, scheduler, configuration resources and combat-unit
derivation are explicit boundaries. Request10/16 and roster tables are native.
"""
import argparse
from copy import deepcopy
import hashlib
import json
import struct

from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.school_adventure_preparation_emulation import SchoolAdventurePreparationEmulator, source_rules as departure_rules
from tools.school_dispatch_emulation import GROUP_TASK
from tools.battle_result_emulation import PREP_TASK
from tools.adv_return_state_emulation import CONTROLLER
from tools.new_game_school_emulation import STATE, STATE_SIZE
from tools.battle_preparation_emulation import PACKAGE_BASE, PACKAGE_STRIDE
from tools.tactics_exit_emulation import BASE, ROOT, SOURCE, SOURCE_SHA256, TASK, STACK, RETURN, ExitEmulator, report_text
from tools.school_course_unlock_emulation import AUTHORITY

NATIVE = ((0x4A1920, 0x4A1C70), (0x4AA0E0, 0x4AA320),
          (0x4B8F20, 0x4B8F70), (0x4B8FF0, 0x4B9340), (0x4DA860, 0x4DAB10))
LEDGER, LEDGER_COUNT = 0x7A5662, 0x7A5B62
EVIDENCE = ROOT/'analysis/school-adventure-handoff-v1-20261009.json'
EVIDENCE_SHA256 = 'c995c6fe880e2cf3adc85158e0526a2ca579879317d922527e72cfc0b694bf46'


def ledger_snapshot(e):
    count = e.read(LEDGER_COUNT, 'h')
    if not 0 <= count <= 80:
        raise RuntimeError('adventure ledger count outside source capacity')
    return {'entries': [{'id': e.read(LEDGER+i*16, 'h'),
        'metadata': list(e.uc.mem_read(LEDGER+i*16+3, 3)),
        'busy': e.read(LEDGER+i*16+6, 'B'), 'limit': e.read(LEDGER+i*16+8, 'h'),
        'duration': e.read(LEDGER+i*16+10, 'h'), 'busy_elapsed': e.read(LEDGER+i*16+12, 'h'),
        'elapsed': e.read(LEDGER+i*16+14, 'h')} for i in range(count)]}


class SchoolAdventureHandoffEmulator(SchoolAdventurePreparationEmulator):
    def __init__(self):
        super().__init__()
        self._function_ranges += NATIVE
        if not any(a <= PREP_TASK and PREP_TASK+0xFFF <= b for a,b,_ in self.uc.mem_regions()):
            self.uc.mem_map(PREP_TASK, 0x1000)
        self.group_checkpoint = None
        self.handoff_events = []
        self.prep_allocated = False

    def _write_hook(self, uc, access, address, size, value, context):
        if getattr(self, 'stage', '') not in ('handoff_commit', 'handoff_group', 'handoff_dispatch', 'handoff_round'):
            return super()._write_hook(uc, access, address, size, value, context)
        if STACK <= address and address+size <= STACK+0x10000:
            return
        if address < 0x7A5292 and address+size > 0x7A528E:
            raise RuntimeError('handoff write outside finite guard: calendar')
        if address < PACKAGE_BASE+45*PACKAGE_STRIDE and address+size > PACKAGE_BASE:
            raise RuntimeError('handoff write outside finite guard: role package/MVP')
        ranges = [(STATE, STATE+STATE_SIZE), (GROUP_TASK, GROUP_TASK+0x1419C),
            (TASK+0xA0000, TASK+0xA00A0), (0x7A4E60, 0x7A4E62),
            (CONTROLLER+0x2C, CONTROLLER+0x34)]
        if self.stage == 'handoff_dispatch':
            ranges += [(0, 4), (PREP_TASK, PREP_TASK+0x30), (0x7A4AE4, 0x7A4AE8)]
        if self.stage == 'handoff_round':
            ranges += [(0x7A4AE8, 0x7A4BB4), (0x7F4488, 0x7F44CE)]
        if not any(a <= address and address+size <= b for a, b in ranges):
            raise RuntimeError(f'handoff write outside finite guard: {address:#x}/{size} at {uc.reg_read(UC_X86_REG_EIP):#x}')
        self.writes.append((address, size, value & ((1 << (size*8))-1)))

    def _hook(self, uc, address, size, context):
        if getattr(self, 'phase', '') == 'school_group_boot' and address == 0x4A7C40:
            self.group_checkpoint = (uc.context_save(), bytes(uc.mem_read(STACK, 0x10000)),
                                     uc.reg_read(UC_X86_REG_ESP))
        stage = getattr(self, 'stage', '')
        if not stage.startswith('handoff_'):
            return super()._hook(uc, address, size, context)
        sp = uc.reg_read(UC_X86_REG_ESP)
        receiver = uc.reg_read(UC_X86_REG_ECX)
        if address == 0x439E30:
            state = self.read(sp+4, 'i')
            self.handoff_events.append({'kind': 'native_request', 'state': state, 'va': hex(address)})
        if stage == 'handoff_group':
            if address == 0x4A7C40:
                if receiver != GROUP_TASK or self.read(sp) != 0x4AB7F1:
                    raise RuntimeError('resume not at captured source group menu')
                self.handoff_events.append({'kind': 'confirmed_menu_return_boundary', 'value': 8,
                                            'commit_executed_separately': True})
                self._stub_return(8, 0)
                return
            if address in (0x4DB230, 0x4DB270, 0x4DB120, 0x41D280, 0x4D6710):
                self.handoff_events.append({'kind': 'presentation_scheduler_boundary', 'va': hex(address)})
                self._stub_return(1 if address == 0x4DB270 else 0, 0)
                return
        if stage == 'handoff_dispatch':
            if address == 0x428A40:
                if self.prep_allocated or self.read(sp+4) != 0x30 or 0x4B9120 not in self.visited:
                    raise RuntimeError('undeclared preparation allocation')
                uc.mem_write(PREP_TASK, bytes(0x30))
                self.prep_allocated = True
                self.handoff_events.append({'kind': 'allocation_boundary', 'size': 0x30,
                    'pointer': hex(PREP_TASK), 'caller_return_va': hex(self.read(sp))})
                self._stub_return(PREP_TASK, 0)
                return
            if address == 0x439EF0:
                if receiver != PREP_TASK or not self.prep_allocated:
                    raise RuntimeError('preparation base constructor outside allocation')
                self._stub_return(receiver, 0)
                return
            if address == 0x4216C0:
                if [self.read(sp+i) for i in (4,8,12)] != [PREP_TASK,0,2] \
                        or self.read(PREP_TASK) != 0x5A0C38 or self.read(PREP_TASK+0x28,'B') != 1:
                    raise RuntimeError('native preparation registration mismatch')
                self.handoff_events.append({'kind': 'scheduler_registration_boundary',
                    'pointer': hex(PREP_TASK), 'vtable': hex(self.read(PREP_TASK)), 'active': 1})
                self._stub_return(0, 0)
                return
        if stage == 'handoff_round' and address in (0x4DAB10, 0x4B9340):
            event = {'kind': 'unresolved_configuration_resources' if address == 0x4DAB10
                     else 'unresolved_combat_unit_derivation', 'va': hex(address)}
            if address == 0x4B9340:
                event.update(character_id=self.read(sp+4,'h'), ordinal=self.read(sp+8,'h'))
            self.handoff_events.append(event)
            self._stub_return(0, 0)
            return
        return ExitEmulator._hook(self, uc, address, size, context)

    def first_round_snapshot(self):
        return {'current': self.read(0x7A5296,'h'), 'total': self.read(0x7A5298,'h'),
            'temp_roster': [self.read(0x7A4AEC+2*i,'h') for i in range(100)],
            'temp_count': self.read(0x7A4AE8,'h'), 'combat_count': self.read(0x7F448D,'B'),
            'scene_id': self.read(0x7F4488,'h'),
            'configuration_bytes': bytes(self.uc.mem_read(0x7F4488,0x46)).hex()}

    def handoff(self, name, commands=()):
        probe = self.probe(name, commands)
        before_ledger = ledger_snapshot(self)
        print('Native ledger before '+name+': '+json.dumps(before_ledger),flush=True)
        before_records = deepcopy(probe['after'])
        self.handoff_events = []
        self.prep_allocated = False
        phases = []
        prepared = round_before = round_after = None
        if probe['ready']:
            self.clear_trace('handoff_commit')
            self.call(0x4A1920, receiver=GROUP_TASK)
            phases.append({'phase': 'commit', 'coverage': self.coverage()})
            self.clear_trace('handoff_group')
            cpu, stack, sp = self.group_checkpoint
            self.uc.context_restore(cpu)
            self.uc.mem_write(STACK, stack)
            self.stop_reason = None
            self.uc.emu_start(0x4A7C40, RETURN, timeout=20_000_000, count=2_000_000)
            if self.uc.reg_read(UC_X86_REG_EIP) != RETURN or self.uc.reg_read(UC_X86_REG_ESP) != STACK+0xFF08:
                raise RuntimeError('resumed group failed ret4/stack bound')
            if [self.read(CONTROLLER+0x2C), self.read(CONTROLLER+0x30)] != [1,10]:
                raise RuntimeError('source group did not request10')
            prepared = self.round_snapshot()
            phases.append({'phase': 'group', 'coverage': self.coverage()})
            self.clear_trace('handoff_dispatch')
            self.call(0x49E2B0)
            if self.read(CONTROLLER+0x2C) != 0 or self.read(0x7A4AE4) != PREP_TASK or not self.prep_allocated:
                raise RuntimeError('actual request10 was not consumed/constructed')
            phases.append({'phase': 'dispatch10', 'coverage': self.coverage()})
            self.clear_trace('handoff_round')
            round_before = self.first_round_snapshot()
            self.stop_reason = None
            self._thread(0x4B8FF0, PREP_TASK, timeout=20_000_000)
            round_after = self.first_round_snapshot()
            if [self.read(CONTROLLER+0x2C), self.read(CONTROLLER+0x30)] != [1,16]:
                raise RuntimeError('first round did not request16')
            phases.append({'phase': 'round', 'coverage': self.coverage()})
        after_records = {'school':self.school_snapshot(),'roles':self.fifth_snapshot(),'counts':self.counts()}
        if before_records != after_records:
            raise RuntimeError('handoff changed retained school/role/date/MVP records')
        return {'name': name, 'commands': deepcopy(probe['commands']), 'ready': probe['ready'],
            'before': before_records, 'after': after_records,
            'ledger_before': before_ledger, 'ledger_after': ledger_snapshot(self),
            'prepared': prepared, 'round_before': round_before, 'round_after': round_after,
            'events': deepcopy(self.handoff_events), 'phases': phases,
            'requested_states': [x['state'] for x in self.handoff_events if x['kind']=='native_request'],
            'pending_flag': self.read(CONTROLLER+0x2C), 'pending_state': self.read(CONTROLLER+0x30),
            'combat_units_ready': False, 'resources_resolved': False, **AUTHORITY}


def source_rules():
    image = SOURCE.read_bytes()
    if hashlib.sha256(image).hexdigest() != SOURCE_SHA256:
        raise ValueError('source image differs')
    raw = image[0x6AD1D0-BASE+5*42:0x6AD1D0-BASE+6*42]
    return {'schema_version':1, 'source_image_sha256':SOURCE_SHA256, 'departure':departure_rules(),
        'configuration_table_va':'0x6ad1d0', 'configuration_stride':42, 'configuration_id':5,
        'configuration_record_hex':raw.hex(), 'configuration_record_sha256':hashlib.sha256(raw).hexdigest(),
        'functions':{'commit':'0x4a1920','group':'0x4ab7a0','dispatch':'0x49e2b0',
            'constructor':'0x4b9120','round':'0x4b8ff0','configuration':'0x4da8e0'},
        'unresolved_functions':['0x4dab10','0x4b9340'], **AUTHORITY}


def report():
    e = SchoolAdventureHandoffEmulator()
    upstream = e.run_planning('handoff_upstream')
    if not upstream['school_data_prepared'] or e.group_checkpoint is None:
        raise RuntimeError('missing actual fifth-school/group checkpoint')
    ranges = [(BASE,(SOURCE.stat().st_size+0xFFF)&~0xFFF),(TASK,0x120000),
              (GROUP_TASK,0x60000),(STACK,0x10000)]
    checkpoint = [(a,bytes(e.uc.mem_read(a,n))) for a,n in ranges]
    cpu = e.uc.context_save()
    cases = []
    for name,commands in [('initial',()),('student9_waiting',[('student',9,-1)]),
        ('fifth_class',[('teacher',101,4),('student',3,4,0),('student',4,4,1),('student',9,-1)]),
        ('teacher_only',[('student',3,-1),('student',4,-1),('student',9,-1)]),
        ('teacher_waiting',[('teacher',101,-1)])]:
        for address,data in checkpoint:
            e.uc.mem_write(address,data)
        e.uc.context_restore(cpu)
        cases.append(e.handoff(name,commands))
        print('Native handoff: '+name+' states='+str(cases[-1]['requested_states']),flush=True)
    return {'schema_version':1, 'source_image_sha256':SOURCE_SHA256,
        'evidence_kind':'actual_fifth_school_checkpoint_commit_group_dispatch_and_first_round',
        'upstream':{'state_requests':upstream['state_requests'],'school_data_prepared':True,
                    'source_report':'school-fifth-planning-v2-20261008.json'},
        'source_rules':source_rules(),'cases':cases,
        'limitations':['Branches fork the same actual fourth-course/fifth-school isolated CPU checkpoint.',
            'Confirmation/menu return8 is declared; 4A1920 runs before restoring the captured group coroutine.',
            'Native group creates request10 and source round tables; original dispatcher constructs state10.',
            '4DAB10 resources and 4B9340 unit derivation are unresolved; count is not unit readiness.',
            'Request16 remains pending: no tactical constructor, live battle, event, completion, reward or gate clearance.'],
        **AUTHORITY}


def exported_fixture(data):
    if hashlib.sha256(EVIDENCE.read_bytes()).hexdigest() != EVIDENCE_SHA256 or hashlib.sha256(report_text(data).encode()).hexdigest() != EVIDENCE_SHA256:
        raise ValueError('frozen handoff evidence differs')
    return {'schema_version':1,'source_image_sha256':SOURCE_SHA256,
        'source_report_sha256':hashlib.sha256(report_text(data).encode()).hexdigest(),
        'cases':[{k:deepcopy(c[k]) for k in ('name','commands','ready','before','after',
            'ledger_before','ledger_after','prepared','round_before','round_after','requested_states',
            'combat_units_ready','resources_resolved')} for c in data['cases']], **AUTHORITY}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',required=True)
    args=parser.parse_args()
    path=ROOT/args.out
    if path.exists(): parser.error('use a new immutable evidence path')
    path.write_text(report_text(report()),encoding='utf-8',newline='\n')
