"""Check an August or September Godot settlement against bounded original x86 calls.

From the project root, run the Godot console in headless mode with --path
prototype -s ../devtools/export_august_four_work.gd -- PARENT OUT MODE
using absolute paths and MODE course, mixed, adventure35 or september. Then run:
python -m tools.school_august_four_lesson_check OUT
In week 5 the original class dispatcher consumes the scored battle packages,
then applies the saved lessons. Week 4 retains its declared battle RNG prefix.
"""
import argparse
import json
import struct
from pathlib import Path

from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.school_course_confirmation_emulation import CourseConfirmationEmulator
from tools.school_course_settlement_emulation import CHAR, STRIDE, PACKAGE_BASE, PACKAGE_STRIDE, TASK, STACK, TLS, source_rules
from tools.tactics_exit_emulation import RETURN


def check(label, actual, expected):
    if actual != expected:
        raise AssertionError((label, actual, expected))


def relationship_address(source, target):
    def index(member):
        return member-55 if member > 100 else member
    return 0x7D3D71 + 68*index(source) + index(target)


class LessonCheck(CourseConfirmationEmulator):
    def __init__(self):
        self.executed = {'course_settlement':0, 'course_confirmation':0}
        super().__init__()

    def _hook(self, uc, address, size, context):
        super()._hook(uc, address, size, context)
        stage = getattr(self, 'stage', None)
        if stage in self.executed and address in self.visited:
            self.executed[stage] += 1

    def _write_hook(self, uc, access, address, size, value, context):
        if self.stage == 'course_confirmation':
            if any(lo <= address and address+size <= hi for lo,hi in self.confirm_ranges):
                return
            raise RuntimeError(f'original confirmation write outside guard: {address:#x}/{size}')
        return super()._write_hook(uc, access, address, size, value, context)

    def invoke(self, address, args=()):
        # The original entry, finite budgets and callee-popped stack are checked.
        if address not in (0x4C0400, 0x4C1350, 0x4C00C0):
            raise ValueError('invalid lesson entry')
        sp = STACK+0xFF00
        self.write(sp, RETURN)
        for i, value in enumerate(args):
            self.write(sp+4+4*i, value)
        self.uc.reg_write(UC_X86_REG_ECX, TASK)
        self.uc.reg_write(UC_X86_REG_ESP, sp)
        self.uc.emu_start(address, RETURN, timeout=120_000_000, count=8_000_000)
        check('original return', self.uc.reg_read(UC_X86_REG_EIP), RETURN)
        check('callee stack', self.uc.reg_read(UC_X86_REG_ESP), sp+4+4*len(args))

    def load_bundle(self, before, seed, ratings):
        school = before['school']
        if (school['month'], school['week']) not in [(8,4),(8,5),(9,1)]:
            raise ValueError('expected an August week 4/5 or September week 1 settlement')
        history = ((school['month']-4)*5+school['week']-1)*3
        self.participant_ids = school['student_ids'][:school['student_count']]
        check('accepted roster', self.participant_ids, [3,4,9,5,8,6,1,2,16,17,13])
        self.uc.mem_write(TASK+0x34, bytes(0x1430-0x34))
        for category, row in enumerate(source_rules()['skill_grid']):
            for ordinal, skill in enumerate(row):
                self.write(TASK+0x136E+2*(category+12*ordinal), skill, 'h')
        self.write(TLS+0x14, seed, 'I')
        self.write(0x7A528C, school['difficulty'], 'h')
        self.write(0x7A528E, school['month'], 'h')
        self.write(0x7A5290, school['week'], 'h')
        self.write(0x7A5260, len(self.participant_ids), 'h')
        for i, member in enumerate(self.participant_ids):
            self.write(0x7A5210+2*i, member, 'h')
        self.uc.mem_write(0x7AAA12, bytes(school['group_raw_bytes']))
        for group, rating in enumerate(ratings):
            words = [rating['state'],rating['relationship_mean'],rating['relationship_rank'],*rating['work_fields']]
            self.uc.mem_write(0x7A529A+112*group, struct.pack('<7h', *words))
            for slot, index in enumerate(school['derived_student_indices'][group]):
                self.write(0x7AAAE0+8*group+2*slot,index,'h')
        self.confirm_ranges = [(STACK,STACK+0x10000), (TASK+0x1138,TASK+0x136E)]
        for career, growth, count in zip(before['records'], before['growth'], before['counts']):
            member = career['character_id']
            check('roster join', [growth['character_id'],count['character_id']], [member,member])
            pkg, base = PACKAGE_BASE+member*PACKAGE_STRIDE, CHAR+member*STRIDE
            self.uc.mem_write(pkg+0x24, bytes(career['week_records']))
            self.uc.mem_write(pkg+0xD7, bytes(career['job_progress']))
            self.write(pkg+0x120, count['count'], 'h')
            self.write(pkg+0x20, growth['staged_total'], 'i')
            self.write(base+6, growth['job'], 'h')
            self.write(base+0x50, growth['level_50'], 'B')
            for k in range(7):
                self.write(base+0xC+8*k, growth['attributes'][k], 'B')
                self.write(base+0x10+8*k, growth['growth_pools'][k], 'I')
            for k, status in enumerate(growth['skill_statuses']):
                self.write(base+0xB8+12*k, status, 'B')
            self.confirm_ranges += [(pkg+0x24+history,pkg+0x24+history+3),(pkg+0xD7+growth['job'],pkg+0xD8+growth['job'])]
        for relation in school['relationships']:
            addr = relationship_address(relation['from'],relation['to'])
            self.write(addr, relation['value'], 'B')
            self.confirm_ranges.append((addr,addr+1))

    def set_round(self, round_data, grade):
        self.write(0x7A5298, int(round_data is not None), 'h')
        if round_data:
            for name,addr,count in [('student_ids',0x7A52D0,0x7A52F8),('teacher_ids',0x7A52FA,0x7A5304)]:
                self.write(count, len(round_data[name]), 'h')
                for i, member in enumerate(round_data[name]):
                    self.write(addr+2*i, member, 'h')
            self.write(0x7A5306, grade, 'h')


def verify(before, after, round_data=None, submitted_ratings=None):
    school = before['school']
    date = [school['month'], school['week']]
    summary = after['sortie_result' if round_data else 'course_result']
    roster = school['student_ids'][:school['student_count']]
    for bundle in (before,after):
        for key in ('growth','records','counts'):
            check(f'{key} roster', [row['character_id'] for row in bundle[key]], roster)
    check('confirmed date', [after['school']['month'],after['school']['week']], date)
    relations = [(row['from'],row['to']) for row in school['relationships']]
    check('relationship coverage', [(row['from'],row['to']) for row in after['school']['relationships']], relations)
    lessons = summary['lessons'] if round_data else summary
    reported = {row['character_id']:row for row in after['growth']}
    seed = summary['growth_seed'] if round_data else summary['declared_clock_seed']
    full_dispatch = not round_data or before['school']['week']==5
    if round_data and not full_dispatch:
        prefix = len(summary['learning_draws'])-len(lessons['learning_draws'])
        for draw in summary['learning_draws'][:prefix]:
            seed = (seed*214013+2531011)&0xFFFFFFFF
            check('shared battle RNG prefix', (seed>>16)&32767, draw)
    original = LessonCheck()
    ratings = submitted_ratings if round_data else before['ratings']
    original.load_bundle(before, seed, ratings)
    if round_data and full_dispatch:
        original._function_ranges += ((0x4C0C10,0x4C1350),)
        for row in summary['score']['characters']:
            pkg = PACKAGE_BASE+row['character_id']*PACKAGE_STRIDE
            original.uc.mem_write(pkg, struct.pack('<9i', *row['staged_package'], row['staged_total']))
    original.clear_trace('course_settlement')
    attendees = []
    for g,rating in enumerate(ratings):
        if rating['state']==4:
            for member in before['school']['derived_student_ids'][g]:
                if member>=0:
                    attendees.append(member)
                    if not full_dispatch:
                        original.invoke(0x4C0400, (member,g))
    if full_dispatch:
        original.write(0x7E1180, -1, 'h')
        original.write(0x7E1184, 0, 'i')
        original.invoke(0x4C00C0)
        check('MVP', original.read(0x7E1180,'h'), summary['recipient'])
        check('prior MVP count', original.read(0x7E1182,'h'), summary['old_mvp_count'])
        for previous, current in zip(before['counts'], after['counts']):
            earned = int(previous['character_id']==summary['recipient'])
            check('confirmed MVP count', current['count'], min(previous['count']+earned,5))
    packets = [{k:v for k,v in row.items() if k not in ('return_va','output_pointer')} for row in original.packet_events]
    check('growth packets', packets, lessons['packets'])
    check('learning draws', original.draws, summary['learning_draws'] if full_dispatch else lessons['learning_draws'])
    check('final RNG state', original.read(TLS+0x14), summary['rand_state'])
    check('bonus', original.read(TASK+0x34), lessons['bonus'])
    if not round_data:
        check('course date', summary['date'], date)
        check('course history slot', summary['history_index'], (date[0]-4)*5+date[1]-1)
        check('confirmed total', after['school']['global_total_511c'],
              min(school['global_total_511c']+original.read(TASK+0x34),999999999))
    if not round_data or not full_dispatch:
        check('skill display', original.read(TASK+0x142C,'h'), lessons['skill_display_needed'])
    for row in original.growth_records():
        member = row['character_id']
        if member in attendees or (round_data and full_dispatch and member in round_data['student_ids']):
            for key in ('job','attributes','growth_pools','skill_statuses','staged_total','level_50'):
                check((member,key), row[key], reported[member][key])
        else:
            # Battle growth is a separate oracle. Confirmation reads the level.
            original.write(CHAR+member*STRIDE+0x50, reported[member]['level_50'], 'B')
    original.set_round(round_data, summary['score']['grade_index'] if round_data else 0)
    original.clear_trace('course_confirmation')
    original.invoke(0x4C1350)
    check('ordered relationship calls', original.relationship_calls, summary['relationship_calls'])
    for row in after['records']:
        pkg = PACKAGE_BASE+row['character_id']*PACKAGE_STRIDE
        check('history', list(original.uc.mem_read(pkg+0x24,177)), row['week_records'])
        check('career', list(original.uc.mem_read(pkg+0xD7,33)), row['job_progress'])
    for row in original.growth_records():
        check('job sums', row['job_sums'], reported[row['character_id']]['job_sums'])
    for row in after['school']['relationships']:
        check('relationship', original.read(relationship_address(row['from'],row['to']),'B'), row['value'])
    return {'attendees':attendees, 'packets':len(packets), 'lesson_draws':len(lessons['learning_draws']), 'verified_draws':len(original.draws),
            'original_instructions':original.executed, 'bonus':lessons['bonus'], 'career_and_history_records':len(reported),
            'relationship_calls':len(original.relationship_calls), 'relationship_values':len(after['school']['relationships'])}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('settled',type=Path)
    parser.add_argument('--round',type=Path)
    args = parser.parse_args()
    bundles = json.loads(args.settled.read_bytes())
    submission = json.loads(args.round.read_bytes()) if args.round else bundles
    print(json.dumps(verify(bundles['before'],bundles['after'],submission.get('round'),submission.get('ratings'))))
