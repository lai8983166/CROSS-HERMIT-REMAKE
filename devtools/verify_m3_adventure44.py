"""Compare the January campaign replay at the original departure, settlement and week routines."""
import argparse
import json
import struct
from pathlib import Path

from unicorn.x86_const import UC_X86_REG_EAX

from devtools.verify_school_year_acceptance import check, digest, load, pinned, sha
from devtools.verify_november_sortie_result import verify_rewards
from tools.school_adventure_preparation_emulation import SchoolAdventurePreparationEmulator
from tools.school_august_four_lesson_check import relationship_address, verify as verify_growth
from tools.school_year_played_week import PlayedWeek
from tools.school_job_menu_export import source_menu
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256, TASK
from tools.tests.test_school_twenty_two_battle import Objective


def departure(school):
    cpu = SchoolAdventurePreparationEmulator()
    cpu.phase = 'departure'
    for address, key in [(0x7A528E, 'month'), (0x7A5290, 'week'), (0x7A55FA, 'adventure_gate'),
                         (0x7AAB0A, 'lecture_active'), (0x7A5260, 'student_count'), (0x7A528A, 'teacher_count')]:
        cpu.write(address, school[key], 'h')
    for address, values in [(0x7A5210, school['raw_student_ids']), (0x7A5262, school['raw_teacher_ids']),
                            (0x7AAAA4, school['derived_teacher_ids']), (0x7AAAAE, school['derived_teacher_indices']),
                            (0x7AAAB8, sum(school['derived_student_ids'], [])),
                            (0x7AAAE0, sum(school['derived_student_indices'], []))]:
        cpu.uc.mem_write(address, struct.pack(f'<{len(values)}h', *values))
    cpu.uc.mem_write(0x7AAA12, bytes(school['group_raw_bytes']))
    for addr, value in zip((0x7AAB10, 0x7AAB12, 0x7AAB16, 0x7AAB14), school['lecture_work_fields'], strict=True):
        cpu.write(addr, value, 'h')
    for row in school['relationships']:
        cpu.write(relationship_address(row['from'], row['to']), row['value'], 'B')
    cpu.clear_trace('departure_ready')
    cpu.call(0x4A7D30)
    check(cpu.uc.reg_read(UC_X86_REG_EAX) & 255, 1, 'original departure readiness')
    cpu.clear_trace('departure_rounds')
    cpu.call(0x4A6A10)
    return cpu.round_snapshot()


def original_objective(sample):
    cpu = Objective()
    cpu._function_ranges += ((0x4360B0, 0x4361A0), (0x431D40, 0x431DCA), (0x469170, 0x469220))
    cpu.sub = -1
    cpu.write(TASK + 0x174, 0)
    cpu.write(TASK + 0x2E6F4, sample['remaining'])
    cpu.write(TASK + 0x2EF34, sample['losses'], 'B')
    slots = set()
    for slot, role, side, state in sample['actors']:
        if not 0 <= slot < 250 or slot in slots:
            raise ValueError(f'Invalid original actor slot {slot}')
        slots.add(slot)
        cpu.actor(slot, role, side, state)
    cpu.call(0x4360B0)
    check(cpu.sub, sample['sub'], f"original mission objective at tick {sample['tick']}")
    return {'tick': sample['tick'], 'last_tick': sample['last_tick'], 'remaining': sample['remaining'], 'losses': sample['losses'],
            'work_slots': len(slots), 'script_sub': cpu.sub, 'selector': cpu.read(TASK + 0x174),
            'actor_fields_sha256': digest(sample['actors'])}


def native_save_header(path):
    data = path.read_bytes()
    if len(data) != 0x306D4 or struct.unpack_from('<h', data)[0] != 7:
        raise ValueError(f'Unrecognized original save: {path}')
    checksum = sum(byte if byte < 128 else byte - 256 for byte in data[:44] + data[48:])
    check(checksum, struct.unpack_from('<i', data, 44)[0], 'original signed byte checksum')
    return {'path': path.relative_to(ROOT).as_posix(), 'bytes': len(data), 'sha256': sha(path),
            'date': list(struct.unpack_from('<hh', data, 0x1A6)),
            'students': struct.unpack_from('<h', data, 0x178)[0]}


def verify(observations):
    formal = ROOT/'.venv-audit/school-year-completion/corrected/formal'
    acceptance = load(ROOT/'analysis/school-year-loop-acceptance.json')
    check(sha(SOURCE), SOURCE_SHA256, 'original image')
    weeks = {tuple(row['date']): row for row in acceptance['calendar']}
    bindings = weeks[13, 2]['settlement']['original']
    school = load(observations/'school.json')
    before, after, returned = (school[key] for key in ('before', 'after', 'returned'))
    check(school['phase'], 'returned_school', 'normal school entry')
    check([returned['school']['month'], returned['school']['week']], [13, 3], 'return date')
    handoff = pinned(formal/'handoff-44.json', bindings['handoff_sha256'])
    check(school['handoff'], handoff, 'replayed school handoff')
    check({'before': before, 'after': after}, pinned(formal/'settled-13-2.json', bindings['settlement_input_sha256']), 'settlement')
    prepared = departure(before['school'])
    check(prepared, handoff['prepared'], 'original prepared squad and ratings')
    round_data, = prepared['rounds']
    ratings = prepared['class_ratings']
    observed = load(observations/'objective.json')
    facts = observed['facts']
    check(facts, pinned(formal.parent/'facts-44.json', bindings['facts_sha256']), 'independent battle replay')
    trace = pinned(formal.parent/'trace-44.json', bindings['trace_sha256'])
    saved = pinned(formal/'march-ending-v40.json', acceptance['ending_save']['sha256'])
    check(saved['commands'][1579], {'op': 'sortie_finish', 'trace': trace}, 'saved battle commands')
    samples = observed['samples']
    check(digest(samples), 'a28f946db8b49319e8a2617c42ff90095452700ac5aee86bce76aced62215e4a', 'recorded objective input sequence')
    next_tick = 1
    objectives = []
    for sample in samples:
        check(sample['tick'], next_tick, 'first tick of objective input interval')
        if sample['last_tick'] < next_tick:
            raise ValueError('Empty objective input interval')
        objectives.append(original_objective(sample))
        next_tick = sample['last_tick'] + 1
    check(next_tick, trace['ticks'] + 1, 'all objective evaluations covered')
    check(objectives[-1]['tick'], trace['ticks'], 'first terminal tick')
    check([r['selector'] for r in objectives], [0]*(len(samples)-1) + [facts['result_selector']], 'objective transitions')
    rewards = verify_rewards(before, after, round_data, ratings, facts)
    growth = verify_growth(before, after, round_data, ratings)
    week = load(formal/'original-week-13-3.json')
    for current, carried in zip(after['participants'], week['before']['participants'], strict=True):
        check({k: current[k] for k in carried}, carried, 'growth at original week entry')
    for key in ('flags', 'item_flags'):
        check(after[key], week['before'][key], f'{key} at week entry')
    check(after['school']['availability'][:45], week['before']['availability'], 'availability at week entry')
    cpu = PlayedWeek(week['before'])
    cpu.call_week(timeout_us=60_000_000)
    check(cpu.week_entry_snapshot, week['before'], 'original week input')
    native_week = cpu.week_snapshot()
    check(digest(native_week), week['expected_sha256'], 'original week output')
    check(digest(native_week), weeks[13, 3]['original_week']['native_state_sha256'], 'sealed week output')
    fields = tuple(week['before']['participants'][0])
    returned_rows = [{key: row[key] for key in fields} for row in returned['participants']]
    check(returned['school']['adventure_gate'], 1, 'next mandatory adventure active')
    check(returned['school']['lecture_work_fields'][2], 29, 'next mandatory adventure identity')
    chapter = ROOT/'CROSS HERMIT/CROSS HERMIT/DATA/ADV/DAT/CHAPTER229.YBC'
    check(sha(chapter), '0c79703017c0acba07627079181c71891edfa4c91fa2f8590e1f9f58f4c4785b', 'school entry chapter')
    op, size, music, mode = struct.unpack_from('<HHII', chapter.read_bytes(), 550)
    check((op, size, music >> 28, mode >> 28), (151, 12, 2, 2), 'school entry music operands')
    expected_flags = {**native_week['flags'], '0x7a55fa': 1, '0x7a4e62': 1,
                      '0x7a55f6': music & 0xfffffff, '0x7e11a0': mode & 0xfffffff}
    check(returned['flags'], expected_flags, 'mandatory school entry and Chapter229 flags')
    check(native_week['participants'], returned_rows, 'original students at school')
    check(native_week['availability'], returned['school']['availability'][:45], 'original availability at school')
    check(native_week['item_flags'], returned['item_flags'], 'original inventory at school')
    check([native_week['month'], native_week['week']], [13, 3], 'original return date')
    probes = [(r['character_id'], [i+1 for i, v in enumerate(r['unlock_flags']) if v == 1]) for r in returned_rows]
    menus = {str(row['member']): row['selectable_jobs'] for row in source_menu(probes)['lookup_probes']}
    check(menus, week['selectable_jobs'], 'original selectable jobs')
    week_result = {'date': [13, 3], 'original_state_sha256': digest(native_week),
                   'returned_students_sha256': digest(returned_rows), 'job_menus_sha256': digest(menus),
                   'inventory_words': len(native_week['item_flags']), 'qualification_bytes': sum(len(r['unlock_flags']) for r in returned_rows),
                   'school_entry_chapter_sha256': sha(chapter), 'original_week_exit_flags': native_week['flags'], 'returned_flags': returned['flags']}
    save_paths = sorted((ROOT/'CROSS HERMIT/CROSS HERMIT/SAVEDATA').glob('*.SAV'))
    save_paths += sorted((ROOT/'analysis/downloaded_saves').glob('*.SAV'))
    for key in ('records', 'counts'):
        check(returned[key], after[key], f'{key} carried to school')
    for key in ('global_total_511c', 'relationships'):
        check(returned['school'][key], after['school'][key], f'{key} carried to school')
    changes = []
    student_fields = ('character_id', 'job', 'attributes', 'growth_pools', 'level_50', 'skill_statuses', 'job_sums', 'staged_total')
    for prior, settled, final, visible in zip(before['growth'], after['growth'], returned['growth'], returned['participants'], strict=True):
        check([visible[k] for k in student_fields], [final[k] for k in student_fields], 'returned participant growth')
        check(final, settled, 'confirmed growth carried to school')
        changes.append({'student': final['character_id'], 'level_before': prior['level_50'], 'level_after': final['level_50'],
                        'attribute_delta': [b-a for a, b in zip(prior['attributes'], final['attributes'], strict=True)],
                        'returned_growth_sha256': digest(final)})
    return {'status': 'partial_original_comparison', 'original_full_fight_observed': False,
            'original_image_sha256': SOURCE_SHA256, 'campaign_sha256': sha(formal/'march-ending-v40.json'),
            'original_saves_examined': [native_save_header(path) for path in save_paths],
            'school_commands_one_based': [1578, 1585], 'prepared': prepared, 'trace_sha256': bindings['trace_sha256'],
            'commands': len(trace['commands']), 'ticks': trace['ticks'], 'battle_facts_source': 'Godot command replay',
            'original_objective': {'entry': '0x4360b0', 'godot_ticks_covered': trace['ticks'], 'original_calls': len(samples),
                                   'intervals_sha256': digest(objectives), 'first': objectives[0], 'last': objectives[-1]},
            'rng_seeds': [facts['clock_seed'], facts['growth_seed']], 'rewards': rewards, 'total_at_school': returned['school']['global_total_511c'],
            'mvp': after['sortie_result']['recipient'], 'growth_and_confirmation': growth,
            'return_week': week_result, 'students': changes}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('observations', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.observations), indent=2))
