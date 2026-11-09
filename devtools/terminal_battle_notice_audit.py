"""Reproduce the retained battle-stop diagnosis without running the game."""
import argparse
import gzip
import json
from pathlib import Path
from devtools import terminal_battle_notice as notice

ROOT=notice.base.ROOT
PARENT=ROOT/'analysis/terminal-school-handoff-guest-v4-20261108.json.gz'
PARENT_SHA='889d6e65dd163c5ab831af32363b553adfbf03981b184b269b758f00545a3335'


def audit():
    need=notice.base.need;word=notice.base.word
    packed=PARENT.read_bytes();need(len(packed)==9004187 and notice.base.sha(packed)==PARENT_SHA,'fixed rejected parent observation')
    with gzip.open(PARENT,'rb')as stream:raw=stream.read(192*1024*1024+1)
    need(len(raw)<=192*1024*1024,'bounded retained observation')
    p=json.loads(raw)['probe'];row=p['dependency_sample'];task=row['tasks'][0]
    head=bytes.fromhex(task['scene_head_hex']);vm=bytes.fromhex(row['VM_hex'])
    activity=bytes.fromhex(task['battle_gates']['controller_activity_hex'])
    need(len(row['tasks'])==1 and task['vtable']==notice.battle.BATTLE,'actual retained battle')
    need(vm[4]==0 and word(vm,28)==2046,'retained VM already terminated')
    state=dict(scene_phase=head[0x44],scene_signal=head[0x58],script_gate=head[0x43],
        script_stage=head[0x59],controller_notice_active=activity[0x16],
        controller_phase=activity[0x18],interaction_enabled=activity[8])
    need(list(state.values())==[3,0,1,2,1,9,0],'retained exact post-script dependency')
    program=p['story_phases'][2]['actions'][-1]['before_sample']['program_code']
    asset=program['assets'][0];data=(ROOT/asset['path']).read_bytes()
    need(len(data)==asset['bytes'] and notice.base.sha(data)==asset['sha256'],'fixed script asset bytes')
    code=data[asset['code_offset']:asset['code_offset']+asset['code_bytes']]
    need(notice.base.sha(code)==program['sha256'] and code[2046:2050]==bytes.fromhex('13000400'),
         'original final opcode19 in the observed opening script')
    image=notice.base.SOURCE.read_bytes()
    return dict(schema_version=1,accepted=False,parent=notice.base.identity(PARENT),
        parent_complete_handoff_proof='rejected_missing_title_and_workroom_edges',
        old_stop=p['stop_reason'],old_state=state,VM_active=vm[4],VM_PC=word(vm,28),
        original_program=program,source_contract=notice.source_contract(image),
        branch_probes=[notice.branch_probe(image,mouse_pressed=m,keyboard_action=k)
                       for m,k in ((0,0),(1,0),(2,0),(0,0x8000),(0,1))],
        missing_old_observation='controller+30998 notification structure was not sampled',
        inferred_next_step='sample exact mode0/state2 and ownership before one normal mouse confirmation',
        VM_already_terminated=True,old_notification_state2_proved=False,
        wait_return_proved=False,result_consumption_proved=False,full_battle_exit_accepted=False,
        implementation=[notice.base.identity(Path(__file__)),notice.base.identity(Path(notice.__file__))])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--out',type=Path,required=True)
    output=parser.parse_args().out.resolve()
    if not output.is_relative_to(ROOT/'analysis')or output.exists():raise ValueError('new owned small report required')
    result=audit()
    with output.open('x',encoding='utf8',newline='\n')as stream:json.dump(result,stream,indent=2);stream.write('\n')
    print(json.dumps(notice.base.identity(output)))
