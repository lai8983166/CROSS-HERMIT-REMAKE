"""Compare a MAP41 or MAP31 settlement with original scoring, loot, growth and school confirmation."""
import argparse
import json
from pathlib import Path

from unicorn.x86_const import UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP

from tools.battle_preparation_emulation import CHAR_BASE, CHAR_STRIDE, PACKAGE_BASE, PACKAGE_STRIDE, PreparationEmulator
from tools.scene5_task_emulation import RESULT_TASK
from tools.school_august_four_lesson_check import check, verify as verify_growth
from tools.tactics_exit_emulation import RETURN, STACK


def verify_rewards(before, after, round_data, ratings, facts):
    school = before['school']
    summary = after['sortie_result']
    score = summary['score']
    scene_id = facts['scene_id']
    assert (school['month'], school['week'], scene_id) in ((11,3,41), (12,1,31))
    cpu = PreparationEmulator(seed=facts['clock_seed'])
    cpu.write(0x7A5294, scene_id, 'h')
    cpu.write(0x7A528C, school['difficulty'], 'h')
    cpu.write(0x7A528E, school['month'], 'h')
    cpu.write(0x7A5290, school['week'], 'h')
    cpu.write(0x7A511C, school['global_total_511c'])
    cpu.write(0x7A54CA+scene_id, 5, 'B')
    for i, key in enumerate(('result_selector','time_key','unit_condition_key')):
        cpu.write(0x7F450C+2*i, facts[key], 'h')
    cpu.uc.mem_write(0x7F44BE, bytes(facts['objective_slots']))
    ids = round_data['student_ids']
    check('round units', [u['character_id'] for u in facts['units']], ids)
    cpu.write(0x7A52F8, len(ids), 'h')
    for i, identity in enumerate(school['student_ids']):
        cpu.write(0x7A5210+2*i, identity, 'h')
    for i, rating in enumerate(ratings):
        cpu.write(0x7A529C+112*i, rating['relationship_mean'], 'h')
        for slot, index in enumerate(school['derived_student_indices'][i]):
            cpu.write(0x7AAAE0+8*i+2*slot, index, 'h')
    for i, (member, group, unit) in enumerate(zip(ids,round_data['student_groups'],facts['units'],strict=True)):
        cpu.write(0x7A52D0+2*i, member, 'h')
        cpu.write(0x7A52A8+2*i, group, 'h')
        for addr, key, fmt in [(0x7F45C2,'count_field_aa','h'),(0x7F45C4,'contribution_field_ac','h'),
                               (0x7F45C6,'status_field_ae','B')]:
            cpu.write(addr+0xb0*i, unit[key], fmt)
        student = next(row for row in before['participants'] if row['character_id']==member)
        base = CHAR_BASE+member*CHAR_STRIDE
        cpu.write(base+6, student['job'], 'h')
        for j,(attribute,pool) in enumerate(zip(student['attributes'],student['growth_pools'],strict=True)):
            cpu.write(base+0xc+8*j,attribute,'B')
            cpu.write(base+0x10+8*j,pool)
        for j, status in enumerate(student['skill_statuses']):
            cpu.write(base+0xb8+12*j,status,'B')
    for i,value in enumerate(before['item_flags'],1):
        cpu.write(0x7AACAA+2*i,value,'H')
    for address in (0x4BD210,0x4BCA40,0x4BBD40):
        sp = STACK+0xff00
        cpu.write(sp, RETURN)
        cpu.uc.reg_write(UC_X86_REG_ECX,RESULT_TASK)
        cpu.uc.reg_write(UC_X86_REG_ESP,sp)
        cpu.uc.emu_start(address,RETURN,timeout=60_000_000,count=2_000_000)
        check('original return',cpu.uc.reg_read(UC_X86_REG_EIP),RETURN)
        check('stack',cpu.uc.reg_read(UC_X86_REG_ESP),sp+4)
    check('grade',cpu.read(0x7A54CA+scene_id,'B'),score['task_grade'])
    for offset, key, fmt in [(0x34,'grade_index','h'),(0x36,'time_display','h'),(0x38,'unit_display','h'),
                             (0x3c,'total_after','i'),(0x40,'total_delta','i')]:
        check(key,cpu.read(RESULT_TASK+offset,fmt),score[key])
    for row in score['characters']:
        package = PACKAGE_BASE+row['character_id']*PACKAGE_STRIDE
        check('staged package',[cpu.read(package+4*k,'i') for k in range(8)],row['staged_package'])
        check('staged total',cpu.read(package+0x20,'i'),row['staged_total'])
    check('inventory',[cpu.read(0x7AACAA+2*i,'H') for i in range(1,361)],after['item_flags'])
    check('loot groups',[[cpu.read(RESULT_TASK+0x140+g*20+2*k,'h') for k in range(10)] for g in range(7)],summary['loot_groups'])
    return {'students':len(ids),'grade':score['task_grade'],'total_delta':score['total_delta']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('settlement',type=Path)
    parser.add_argument('submission',type=Path)
    args = parser.parse_args()
    case = json.loads(args.settlement.read_bytes())
    entry = json.loads(args.submission.read_bytes())
    print('rewards',verify_rewards(case['before'],case['after'],entry['round'],entry['ratings'],entry['facts']),flush=True)
    print('growth',verify_growth(case['before'],case['after'],entry['round'],entry['ratings']))
