"""Compare Chapter309's two join paths to the original opcode 144 and its helpers."""
import argparse
import json
import struct
from pathlib import Path

from tools.battle_preparation_emulation import CHAR_BASE, CHAR_STRIDE, PACKAGE_BASE, PACKAGE_STRIDE
from tools.roster_join_emulation import RosterJoinEmulator
from tools.scene5_script_emulation import SCRIPT, VM
from tools.school_sortie_week_story_export import GAME, SOURCE


def check(before, choice, observed):
    students = before['school']['raw_student_ids']
    teachers = before['school']['raw_teacher_ids']
    members = [20,21] if choice==0 else [19]
    cpu = RosterJoinEmulator()
    image = SOURCE.read_bytes()
    for identity in members:
        offset = 0x2f5088+identity*CHAR_STRIDE
        cpu.uc.mem_write(CHAR_BASE+identity*CHAR_STRIDE,image[offset:offset+CHAR_STRIDE])
        package = PACKAGE_BASE+identity*PACKAGE_STRIDE
        cpu.uc.mem_write(package,bytes(PACKAGE_STRIDE))
        progress = struct.unpack_from('<32h',image,0x351242+identity*0x42)
        cpu.uc.mem_write(package+0xd7,bytes([0]+[min(100,max(0,n)) for n in progress]))
    for addr, values in [(0x7a5210,students),(0x7a5262,teachers),(0x7aacac,before['item_flags'])]:
        cpu.uc.mem_write(addr,struct.pack('<'+'H'*len(values),*values))
    for addr, value in [(0x7a5260,17),(0x7a528a,6),(0x7a528c,before['school']['difficulty']),
                        (0x7a528e,12),(0x7a5290,1)]:
        cpu.write(addr,value,'h')
    cpu.uc.mem_write(0x7a5120,bytes(before['school']['availability']))
    cpu.uc.mem_write(SCRIPT,(GAME/'DAT/CHAPTER309.YBC').read_bytes())
    cpu.write(VM+0xc,SCRIPT)
    cpu.call(0x4ce560,(0,7),receiver=VM)
    cpu.write(VM+0x1c,(0x73e if choice==0 else 0xc54)-20)
    for identity in members:
        cpu.call_join_step()
    assert [row['character_id'] for row in cpu.join_entries]==members
    assert cpu.read(0x7a5260,'h')==17+len(members)
    assert list(struct.unpack('<40H',cpu.uc.mem_read(0x7a5210,80)))==observed['students']
    assert list(cpu.uc.mem_read(0x7a5120,121))==observed['availability']
    assert list(struct.unpack('<360H',cpu.uc.mem_read(0x7aacac,720)))==observed['items']
    for identity, row, history in zip(members,observed['participants'],observed['records'],strict=True):
        character, package = CHAR_BASE+identity*CHAR_STRIDE, PACKAGE_BASE+identity*PACKAGE_STRIDE
        vectors=[('equipped_skills',character+0x52,2,'h'),('equipped_items',character+0x62,2,'h'),
                 ('attributes',character+0xc,8,'B'),('growth_pools',character+0x10,8,'I'),
                 ('skill_statuses',character+0xb8,12,'B'),('unlock_flags',package+0xf9,1,'B'),
                 ('unlock_reserved_bytes',package+0x117,1,'B'),('job_progress',package+0xd7,1,'b')]
        for key,addr,stride,fmt in vectors:
            assert [cpu.read(addr+k*stride,fmt) for k in range(len(row[key]))]==row[key],(identity,key)
        assert cpu.read(character+6,'h')==row['job'] and cpu.read(character+0x50,'B')==row['level_50']
        assert cpu.read(package+0x20,'i')==row['staged_total']
        assert list(cpu.uc.mem_read(package+0xd7,33))==history['job_progress']
        assert list(cpu.uc.mem_read(package+0x24,177))==history['week_records']


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('settled',type=Path)
    parser.add_argument('observations',type=Path)
    args=parser.parse_args()
    before=json.loads(args.settled.read_text(encoding='utf8'))['after']
    observed=json.loads(args.observations.read_text(encoding='utf8'))
    for choice in (0,1):
        check(before,choice,observed[str(choice)])
    print('Original opcode 144 matches both Chapter309 choices and all three join records.')
