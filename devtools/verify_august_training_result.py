"""Compare a played August training trace's terminal facts with original result code.

From the repository root, export a new JSON file from the accepted save:
  godot --headless --path prototype -s ../devtools/export_august_four_work.gd -- ABS_SAVE ABS_JSON mixed|adventure35
  python -m devtools.verify_august_training_result ABS_JSON

This only executes the three result preparation routines on declared inputs.
"""
import argparse
import json
from pathlib import Path

from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.battle_preparation_emulation import (
    CHAR_BASE, CHAR_STRIDE, PACKAGE_BASE, PACKAGE_STRIDE, PreparationEmulator,
)
from tools.scene5_task_emulation import RESULT_TASK
from tools.tactics_exit_emulation import RETURN, SOURCE_SHA256, STACK


def run_routine(cpu, address):
    sp = STACK + 0xff00
    cpu.write(sp, RETURN)
    cpu.uc.reg_write(UC_X86_REG_ESP, sp)
    cpu.uc.reg_write(UC_X86_REG_ECX, RESULT_TASK)
    cpu.uc.emu_start(address, RETURN, timeout=45_000_000, count=5_000_000)
    if cpu.uc.reg_read(UC_X86_REG_EIP) != RETURN or cpu.uc.reg_read(UC_X86_REG_ESP) != sp + 4:
        raise RuntimeError(f'{address:#x} did not return with balanced stack')


def load_participants(cpu, bundle, round_data, facts):
    ids = round_data['student_ids']
    if [unit['character_id'] for unit in facts['units']] != ids:
        raise ValueError('battle stats differ from the departure roster')
    growth = {row['character_id']: row for row in bundle['growth']}
    cpu.write(0x7a52f8, len(ids), 'h')
    for i, character in enumerate(ids):
        row = growth[character]
        base = CHAR_BASE + character * CHAR_STRIDE
        template = cpu.uc.mem_read(0x6f5088 + character * CHAR_STRIDE, CHAR_STRIDE)
        cpu.uc.mem_write(base, bytes(template))
        cpu.write(base + 6, row['job'], 'h')
        for k, pool in enumerate(row['growth_pools']):
            cpu.write(base + 0x10 + 8*k, pool)
            cpu.write(base + 0xc + 8*k, row['attributes'][k], 'B')
        for k, status in enumerate(row['skill_statuses']):
            cpu.write(base + 0xb8 + 12*k, status, 'B')
        cpu.uc.mem_write(PACKAGE_BASE + character*PACKAGE_STRIDE, bytes(PACKAGE_STRIDE))
        cpu.write(0x7a52d0 + 2*i, character, 'h')
        cpu.write(0x7a52a8 + 2*i, round_data['student_groups'][i], 'h')
        unit = facts['units'][i]
        for offset, key, fmt in [(0xaa, 'count_field_aa', 'h'), (0xac, 'contribution_field_ac', 'h'),
                                 (0xae, 'status_field_ae', 'B')]:
            cpu.write(0x7f4518 + 0xb0*i + offset, unit[key], fmt)
    school = bundle['school']
    students = school['student_ids'][:school['student_count']]
    for i, character in enumerate(students):
        cpu.write(0x7a5210 + 2*i, character, 'h')
    for group, slots in enumerate(school['derived_student_ids']):
        for slot, character in enumerate(slots):
            cpu.write(0x7aaae0 + group*8 + slot*2,
                      students.index(character) if character >= 0 else -1, 'h')


def verify(captured):
    bundle = captured['before']
    school = bundle['school']
    facts = captured['facts']
    scene_id = facts['scene_id']
    if (school['month'], school['week'], scene_id) not in [(8, 4, 17), (8, 5, 35)]:
        raise ValueError('expected scene 17 in August week 4 or scene 35 in week 5')
    cpu = PreparationEmulator(seed=facts['clock_seed'])
    cpu.write(0x7a5294, scene_id, 'h')
    cpu.write(0x7a54ca + scene_id, captured['grades'].get(str(scene_id), 5), 'B')
    cpu.write(0x7a528e, school['month'], 'h')
    cpu.write(0x7a5290, school['week'], 'h')
    cpu.write(0x7a528c, school['difficulty'], 'h')
    cpu.write(0x7a511c, school['global_total_511c'])
    for addr, key in [(0x7f450c, 'result_selector'), (0x7f450e, 'time_key'), (0x7f4510, 'unit_condition_key')]:
        cpu.write(addr, facts[key], 'h')
    for i, value in enumerate(facts['objective_slots']):
        cpu.write(0x7f44be + i, value, 'B')
    for i, value in enumerate(bundle['item_flags'], 1):
        cpu.write(0x7aacaa + 2*i, value, 'H')
    for group, rating in enumerate(captured['ratings']):
        cpu.write(0x7a529c + group*112, rating['relationship_mean'], 'h')
    load_participants(cpu, bundle, captured['round'], facts)
    for address in [0x4bd210, 0x4bca40, 0x4bbd40]:
        run_routine(cpu, address)

    packages = []
    for character in captured['round']['student_ids']:
        base = PACKAGE_BASE + character*PACKAGE_STRIDE
        packages.append({'character_id': character, 'staged_total': cpu.read(base + 0x20, 'i'),
                         'staged_package': [cpu.read(base + k*4, 'i') for k in range(8)]})
    loot = [[cpu.read(RESULT_TASK + 0x140 + g*20 + k*2, 'h') for k in range(10)] for g in range(7)]
    flags = [cpu.read(0x7aacaa + 2*i, 'H') for i in range(1, 361)]
    result = captured['after']['sortie_result']
    for name, actual, expected in [
        ('grade', cpu.read(0x7a54ca + scene_id, 'B'), result['task_grade']),
        ('score', cpu.read(RESULT_TASK + 0x40, 'i'), result['score']['total_delta']),
        ('total', cpu.read(0x7a511c, 'i'), result['score']['total_after']),
        ('packages', packages, result['score']['characters']), ('loot', loot, result['loot_groups']),
        ('flags', flags, captured['after']['item_flags']),
    ]:
        if actual != expected:
            raise ValueError(f'{name} mismatch: {actual!r} != {expected!r}')
    return {'image_sha256': SOURCE_SHA256, 'participants': len(packages), 'loot_slots': 70,
            'inventory_flags': len(flags), 'grade': result['task_grade'], 'score_delta': result['score']['total_delta']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('settled', type=Path)
    print(json.dumps(verify(json.loads(parser.parse_args().settled.read_bytes()))))
