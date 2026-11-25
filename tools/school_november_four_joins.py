"""Compare Godot's four November joins to the original opcode 144 instruction bodies."""
import argparse
import json
from pathlib import Path
import struct

from tools.battle_preparation_emulation import CHAR_BASE, CHAR_STRIDE, PACKAGE_BASE, PACKAGE_STRIDE
from tools.roster_join_emulation import RosterJoinEmulator
from tools.scene5_script_emulation import SCRIPT, VM
from tools.school_november_four import GAME
from tools.school_sortie_week_story_export import SOURCE


def check(before, observed, stage):
    chapter = 72 if stage=='equipment' else int(stage)
    identity = {72:2,74:7,307:28}[chapter]
    cpu = RosterJoinEmulator()
    data = observed[stage]
    old = before['chapter071_absent']
    character = CHAR_BASE+identity*CHAR_STRIDE
    package = PACKAGE_BASE+identity*PACKAGE_STRIDE
    image = SOURCE.read_bytes()
    cpu.uc.mem_write(character,image[0x2f5088+identity*CHAR_STRIDE:0x2f5088+(identity+1)*CHAR_STRIDE])
    cpu.uc.mem_write(package,bytes(PACKAGE_STRIDE))
    if identity==2:
        row = old['participants']
        cpu.write(character+6,row['job'],'h')
        cpu.write(character+0x50,row['level_50'],'B')
        for k in range(7):
            cpu.write(character+0xc+8*k,row['attributes'][k],'B')
            cpu.write(character+0x10+8*k,row['growth_pools'][k])
        for k,value in enumerate(row['skill_statuses']):
            cpu.write(character+0xb8+12*k,value,'B')
        for offset, values in [(0x52,row['equipped_skills']),(0x62,row['equipped_items'] if stage!='equipment' else [6,7]+[0]*6)]:
            cpu.uc.mem_write(character+offset,struct.pack('<8h',*values))
        cpu.uc.mem_write(package+0xf9,bytes(row['unlock_flags']+row['unlock_reserved_bytes']))
        cpu.write(package+0x20,row['staged_total'],'i')
        history=old['records']
    else:
        initial=struct.unpack_from('<32h',image,0x351242+identity*0x42)
        history={'job_progress':[0]+[min(max(n,0),100) for n in initial],'week_records':[0]*177}
    cpu.uc.mem_write(package+0xd7,bytes(history['job_progress']))
    cpu.uc.mem_write(package+0x24,bytes(history['week_records']))
    cpu.write(0x7a528c,before['school']['difficulty'],'h')
    cpu.write(0x7a528e,11,'h')
    cpu.write(0x7a5290,4 if chapter==307 else 3,'h')
    students=before['school']['student_ids'][:15]+([] if chapter==72 else [2] if chapter==74 else [2,7])
    teachers=before['school']['teacher_ids'][:5]
    for base, values in [(0x7a5210,students),(0x7a5262,teachers)]:
        cpu.uc.mem_write(base,struct.pack('<'+'h'*len(values),*values))
    cpu.write(0x7a5260,len(students),'h')
    cpu.write(0x7a528a,len(teachers),'h')
    cpu.uc.mem_write(0x7a5120,bytes(int(n in students+teachers) for n in range(121)))
    flags=list(before['item_flags'] if chapter==72 else observed['72']['item_flags'] if chapter==74 else observed['before307_items'])
    if stage=='equipment':
        flags[5:7]=[0xa105,0x7600]
    cpu.uc.mem_write(0x7aacac,struct.pack('<360H',*flags))
    cpu.uc.mem_write(SCRIPT,(GAME/f'DAT/CHAPTER{chapter:03}.YBC').read_bytes())
    cpu.write(VM+0xc,SCRIPT)
    cpu.call(0x4ce560,(0,7),receiver=VM)
    cpu.call_join_step()
    if chapter==307:
        cpu.call_join_step()
    assert [e['character_id'] for e in cpu.join_entries] == ([107,28] if chapter==307 else [identity])
    for base, size_at, key in [(0x7a5210,0x7a5260,'students'),(0x7a5262,0x7a528a,'teachers')]:
        count=cpu.read(size_at,'h')
        assert [cpu.read(base+n*2,'h') for n in range(count)]==data[key]
    row=data['participant']
    vectors=[('equipped_skills',character+0x52,2,'h'),('equipped_items',character+0x62,2,'h'),
             ('attributes',character+0xc,8,'B'),('growth_pools',character+0x10,8,'I'),
             ('skill_statuses',character+0xb8,12,'B'),('unlock_flags',package+0xf9,1,'B'),
             ('unlock_reserved_bytes',package+0x117,1,'B'),('job_progress',package+0xd7,1,'b')]
    for key, addr, stride, fmt in vectors:
        assert [cpu.read(addr+k*stride,fmt) for k in range(len(row[key]))]==row[key], (stage,key)
    assert cpu.read(character+6,'h')==row['job'] and cpu.read(character+0x50,'B')==row['level_50']
    assert cpu.read(package+0x20,'i')==row['staged_total']
    assert list(cpu.uc.mem_read(package+0xd7,33))==data['history']['job_progress']
    assert list(cpu.uc.mem_read(package+0x24,177))==data['history']['week_records']
    assert list(struct.unpack('<360H',cpu.uc.mem_read(0x7aacac,720)))==data['item_flags']


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('settlement',type=Path)
    parser.add_argument('observations',type=Path)
    args=parser.parse_args()
    before=json.loads(args.settlement.read_text(encoding='utf8'))['after']
    observed=json.loads(args.observations.read_text(encoding='utf8'))
    for stage in ('72','equipment','74','307'):
        check(before,observed,stage)
    print('Original opcode 144 matches for 2, 7, 107, 28 and the occupied/free equipment case.')
