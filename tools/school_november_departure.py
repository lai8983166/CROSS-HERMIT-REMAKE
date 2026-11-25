"""Check Chapter071's opening opcode against the original student removal routine."""
import hashlib
import json
import struct

from tools.battle_preparation_emulation import CHAR_BASE, CHAR_STRIDE, PACKAGE_BASE, PACKAGE_STRIDE
from tools.roster_join_emulation import RosterJoinEmulator
from tools.scene5_script_emulation import SCRIPT, VM
from tools.school_sortie_week_story_export import GAME, date_route


def verify():
    route = date_route('CH001', 11, 3)
    assert route['target'] == 'data/adv/dat/Chapter071.ybc'
    assert date_route('CH003', 11, 2)['target'] is None
    assert date_route('CH003', 11, 3)['target'] == 'data/adv/dat/Chapter072.ybc'
    chapter = (GAME/'DAT/Chapter071.ybc').read_bytes()
    rejoin = (GAME/'DAT/Chapter072.ybc').read_bytes()
    assert struct.unpack_from('<HHI', chapter, 20) == (145, 8, 0x20000002)
    assert struct.unpack_from('<HHI', rejoin, 20) == (144, 8, 0x20000002)
    cpu = RosterJoinEmulator()
    cpu._function_ranges += ((0x4D0990, 0x4D0A10), (0x4D4250, 0x4D45C0), (0x4D4770, 0x4D47B0))
    cpu.write(0x7A528E, 11, 'h')
    cpu.write(0x7A5290, 3, 'h')
    roster = [3,4,9,5,8,6,1,2,16,17,13,14,15,11,18,32]
    for i, member in enumerate(roster):
        cpu.write(0x7A5210+2*i, member, 'h')
    cpu.write(0x7A5260, len(roster), 'h')
    cpu.write(0x7A5122, 1, 'B')
    groups = [3,4,2,5]+[-1]*16
    def group_address(i):
        return 0x7AAA22+(i//4)*28+(i%4)*2
    for i, member in enumerate(groups):
        cpu.write(group_address(i), member, 'h')
    base = CHAR_BASE+2*CHAR_STRIDE
    package = PACKAGE_BASE+2*PACKAGE_STRIDE
    cpu.uc.mem_write(base, bytes(cpu.uc.mem_read(0x6F5088+2*CHAR_STRIDE, CHAR_STRIDE)))
    cpu.uc.mem_write(package+0x24, bytes([37])*177)
    cpu.uc.mem_write(package+0xd7, bytes([13])*33)
    for slot, item in enumerate([6,7]+[0]*6):
        cpu.write(base+0x62+2*slot, item, 'h')
    cpu.write(0x7AACAA+12, 0xA705, 'H')
    cpu.write(0x7AACAA+14, 0x7600, 'H')
    character_bytes = bytes(cpu.uc.mem_read(base, CHAR_STRIDE))
    package_bytes = bytes(cpu.uc.mem_read(package, PACKAGE_STRIDE))
    cpu.uc.mem_write(SCRIPT, chapter)
    cpu.write(VM+0xC, SCRIPT)
    cpu.call(0x4CE560, (0, 7), receiver=VM)
    for _ in range(2):
        cpu.write(VM+0x1C, 0)
        cpu.call_join_step()
        assert cpu.read(0x7A5260, 'h') == 15 and cpu.read(0x7A5122, 'B') == 0
        assert [cpu.read(0x7A5210+i*2, 'h') for i in range(16)] == [n for n in roster if n!=2]+[32]
        assert [cpu.read(group_address(i), 'h') for i in range(20)] == [-1 if n==2 else n for n in groups]
        assert [cpu.read(0x7AACAA+2*i, 'H') for i in (6,7)] == [0xA105,0x7600]
        assert cpu.uc.mem_read(base, CHAR_STRIDE) == character_bytes
        assert cpu.uc.mem_read(package, PACKAGE_STRIDE) == package_bytes
    cpu.uc.mem_write(SCRIPT, rejoin)
    cpu.write(VM+0xC, SCRIPT)
    cpu.call(0x4CE560, (0, 7), receiver=VM)
    cpu.call_join_step()
    assert cpu.read(0x7A5260, 'h') == 16 and cpu.read(0x7A5122, 'B') == 1
    assert cpu.read(0x7A5210+2*15, 'h') == 2
    assert cpu.uc.mem_read(package+0x24, 177) == bytes([37])*177
    assert cpu.uc.mem_read(package+0xd7, 33) == bytes([13])*33
    assert [cpu.read(base+0x62+2*i, 'h') for i in (0,1)] == [0,7]
    assert [cpu.read(0x7AACAA+2*i, 'H') for i in (6,7)] == [0xA105,0x7305]
    return {'chapter_sha256': hashlib.sha256(chapter).hexdigest(), 'opcode':145,
            'student':2, 'active_count':15, 'raw_first_inactive_slot':32,
            'duplicate_delivery_checked':True, 'rejoin_chapter_sha256':hashlib.sha256(rejoin).hexdigest(),
            'rejoin_index':15, 'history_and_progress_preserved':True}


if __name__ == '__main__':
    print(json.dumps(verify()))
