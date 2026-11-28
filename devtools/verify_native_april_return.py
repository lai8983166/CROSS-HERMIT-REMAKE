"""Compare a played Godot sortie with the original x86 departure, score, growth and week routines."""
import argparse
import hashlib
import json
import struct
from pathlib import Path

from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.battle_preparation_emulation import CHAR_BASE, CHAR_STRIDE, PACKAGE_BASE, PACKAGE_STRIDE, PreparationEmulator
from tools.scene5_task_emulation import RESULT_TASK
from tools.school_adventure_preparation_emulation import SchoolAdventurePreparationEmulator
from tools.school_august_four_lesson_check import LessonCheck, relationship_address
from tools.school_course_settlement_emulation import TASK, TLS, source_rules
from tools.school_year_played_week import FIELDS, FLAGS, PlayedWeek
from tools.tactics_exit_emulation import RETURN, STACK

STATE = 0x7A50E8
SIZE = 0x306D4


def check(key, actual, expected):
    if actual != expected:
        raise ValueError(f'{key}: {actual!r} != {expected!r}')


def transfer(before, after):
    after.uc.mem_write(STATE, bytes(before.uc.mem_read(STATE, SIZE)))
    after.uc.mem_write(CHAR_BASE, bytes(before.uc.mem_read(CHAR_BASE, 65*CHAR_STRIDE)))


def prepare_native_school(raw):
    """Run the original readiness and round construction on verified school bytes."""
    school = SchoolAdventurePreparationEmulator()
    school.uc.mem_write(STATE,raw)
    local = 0x7BC6AC-STATE
    school.uc.mem_write(CHAR_BASE,raw[local:local+65*CHAR_STRIDE])
    school.phase='departure'
    school.clear_trace('departure_ready')
    school.call(0x4A7D30)
    check('departure ready', school.uc.reg_read(UC_X86_REG_EAX)&255,1)
    school.clear_trace('departure_rounds')
    school.call(0x4A6A10)
    return school, school.round_snapshot()


def verify(raw, source_sha, case):
    check('source', hashlib.sha256(raw).hexdigest(), source_sha)
    check('save size', len(raw), SIZE)
    check('checksum', sum(v if v<128 else v-256 for v in raw[:44]+raw[48:]), struct.unpack_from('<i',raw,44)[0])
    score, facts, state = (case[k] for k in ('score','facts','state'))
    sid = facts['scene_id']
    check('April mission', list(struct.unpack_from('<hh',raw,0x1a6)), [4,sid])
    school, prepared = prepare_native_school(raw)
    units=prepared['rounds'][0]['student_ids']
    check('combatants',units,[row['character_id'] for row in facts['units']])
    reward=PreparationEmulator(seed=facts['clock_seed'])
    transfer(school,reward)
    # The completed tactical round has advanced the zero-based departure cursor.
    reward.write(0x7A5296,1,"h")
    for i,key in enumerate(('result_selector','time_key','unit_condition_key')):
        reward.write(0x7F450C+2*i,facts[key],'h')
    reward.uc.mem_write(0x7F44BE,bytes(facts['objective_slots']))
    for i,row in enumerate(facts['units']):
        for offset,key,kind in [(0x7F45C2,'count_field_aa','h'),(0x7F45C4,'contribution_field_ac','h'),(0x7F45C6,'status_field_ae','B')]:
            reward.write(offset+0xB0*i,row[key],kind)
    for va in (0x4BD210,0x4BCA40,0x4BBD40):
        sp=STACK+0xFF00
        reward.write(sp, RETURN)
        reward.uc.reg_write(UC_X86_REG_ECX,RESULT_TASK)
        reward.uc.reg_write(UC_X86_REG_ESP,sp)
        try:
            reward.uc.emu_start(va,RETURN,timeout=60_000_000,count=2_000_000)
        except Exception as exc:
            raise RuntimeError(f"Original {va:#x} stopped at {reward.uc.reg_read(UC_X86_REG_EIP):#x}") from exc
        check('return',reward.uc.reg_read(UC_X86_REG_EIP),RETURN)
        check('stack',reward.uc.reg_read(UC_X86_REG_ESP),sp+4)
    for off,key,kind in [(0x34,'grade_index','h'),(0x36,'time_display','h'),(0x38,'unit_display','h'),(0x3C,'total_after','i'),(0x40,'total_delta','i')]:
        check(key,reward.read(RESULT_TASK+off,kind),score[key])
    for row in score['characters']:
        p=PACKAGE_BASE+row['character_id']*PACKAGE_STRIDE
        check('staged growth',list(struct.unpack('<9i',reward.uc.mem_read(p,36))),row['staged_package']+[row['staged_total']])
    check('loot',[[reward.read(RESULT_TASK+0x140+20*g+2*k,'h') for k in range(10)] for g in range(7)],state['last_result']['loot'])
    grown=LessonCheck()
    transfer(reward,grown)
    roster=state['school']['student_ids']
    check('roster',list(struct.unpack_from('<'+'h'*len(roster),raw,0x128)),roster)
    grown.participant_ids=roster
    grown.uc.mem_write(TASK+0x34, bytes(0x1430-0x34))
    for category, row in enumerate(source_rules()['skill_grid']):
        for ordinal,skill in enumerate(row):grown.write(TASK+0x136E+2*(category+12*ordinal),skill,'h')
    grown.write(TLS+0x14,facts['growth_seed'],'I')
    grown._function_ranges+=((0x4C0C10,0x4C1350),)
    grown.write(0x7E1180,-1,'h')
    grown.write(0x7E1184,0,'i')
    grown.clear_trace('course_settlement')
    grown.invoke(0x4C00C0)
    mvp=grown.read(0x7E1180,'h')
    check('MVP',mvp,state['last_result']['mvp'])
    grown.set_round(prepared['rounds'][0],score['grade_index'])
    history=(sid-1)*3
    grown.confirm_ranges=[(STACK,STACK+0x10000),(TASK+0x1138,TASK+0x136E)]
    for member in roster:
        p=PACKAGE_BASE+member*PACKAGE_STRIDE
        job=grown.read(CHAR_BASE+member*CHAR_STRIDE+6,'h')
        grown.confirm_ranges += [(p+0x24+history,p+0x27+history),(p+0xD7+job,p+0xD8+job)]
    for row in state['school']['relationships']:
        a=relationship_address(row['from'],row['to'])
        grown.confirm_ranges.append((a,a+1))
    grown.clear_trace('course_confirmation')
    grown.invoke(0x4C1350)
    for row in state['school']['relationships']:
        check('relationship',grown.read(relationship_address(row['from'],row['to']),'B'),row['value'])
    week_rows=[]
    for member in roster:
        row=state['members'][str(member)]
        p=PACKAGE_BASE+PACKAGE_STRIDE*member
        base=CHAR_BASE+CHAR_STRIDE*member
        check(('history',member),list(grown.uc.mem_read(p+0x24,177)),row['week_records'])
        check(('growth pools',member),[grown.read(base+0x10+8*i,'I') for i in range(7)],row['growth_pools'])
        check(('level',member),grown.read(base+0x50,'B'),row['level_50'])
        old_count=struct.unpack_from('<h',raw,p-STATE+0x120)[0]
        check(('MVP count',member),min(5,old_count+int(member==mvp)),row['mvp_count'])
        snapshot={'character_id':member}
        for key,address,stride,offset,step,count,kind in FIELDS:
            snapshot[key]=[grown.read(address+stride*member+offset+step*i,kind) for i in range(count)]
        week_rows.append(snapshot)
    week=PlayedWeek({'participants':week_rows,'month':4,'week':sid,'availability':list(grown.uc.mem_read(0x7A5120,45)),
                     'item_flags':list(struct.unpack('<360H',grown.uc.mem_read(0x7AACAC,720))),
                     'flags':{hex(a):grown.read(a,'h') for a in FLAGS}})
    week.call_week(timeout_us=60_000_000)
    returned=week.week_snapshot()
    check('returned date',[returned['month'],returned['week']],[state['school']['month'],state['school']['week']])
    check('inventory',returned['item_flags'],state['item_flags'])
    for row in returned['participants']:
        member=row['character_id']
        for key in row:check((member,key),row[key],state['members'][str(member)][key])
    return {'scene':sid,'score_delta':score['total_delta'],'mvp':mvp,'growth_packages':len(units),
            'roster':len(roster),'history_bytes':177*len(roster),'inventory_words':360,
            'relationships':len(state['school']['relationships']),'returned_date':[returned['month'],returned['week']]}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('save',type=Path)
    parser.add_argument('source_sha256')
    parser.add_argument('observations',type=Path)
    args=parser.parse_args()
    print(json.dumps(verify(args.save.read_bytes(),args.source_sha256,json.loads(args.observations.read_bytes()))))
