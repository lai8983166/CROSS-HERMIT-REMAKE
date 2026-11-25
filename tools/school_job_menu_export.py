"""Read the original personal-screen job grid and Big5 names.

The fixed menu probes execute the grid initialization and candidate lookup
instructions from 4B12A0. They stop before the button drawing branch.
"""
import hashlib
import json
import struct

from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
from unicorn.x86_const import UC_X86_REG_EBP, UC_X86_REG_EIP

from tools.school_story_export import source_string
from tools.tactics_exit_emulation import ROOT, SOURCE, SOURCE_SHA256


def source_menu(probes=None):
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('source image mismatch')
    cpu = Uc(UC_ARCH_X86, UC_MODE_32)
    cpu.mem_map(0x4b1000, 0x1000)
    cpu.mem_write(0x4b1000, raw[0xb1000:0xb2000])
    cpu.mem_map(0x7cf000, 0x4000)
    cpu.mem_map(0x7d6000, 0x1000)
    cpu.mem_map(0x10000, 0x2000)
    frame, screen = 0x10800, 0x11000
    cpu.reg_write(UC_X86_REG_EBP, frame)
    cpu.mem_write(frame-4, struct.pack('<I', screen))
    cpu.emu_start(0x4b12e3, 0x4b133d, count=16)
    order = list(struct.unpack('<15H', cpu.mem_read(frame-0x58, 30)))
    variants = [raw[0x2f5088+member*0x4a0+0x72] for member in range(45)]
    cases = []
    if probes is None:
        probes = [(18, [2, 4, 5, 12, 14, 29, 30]), (32, [1, 3, 4, 11, 13, 22, 29])]
    for member, enabled in probes:
        cpu.mem_write(screen+0x69, bytes([variants[member]]))
        cpu.mem_write(screen+0x596, struct.pack('<H', member))
        flags = [int(job in enabled) for job in range(1, 31)]
        cpu.mem_write(0x7cf445+member*0x124, bytes(flags))
        selected = []
        for cell in range(15):
            row, col = divmod(cell, 5)
            cpu.mem_write(frame-0x24, struct.pack('<II', row, col))
            cpu.emu_start(0x4b13b3, 0x4b1428, count=40)
            if cpu.reg_read(UC_X86_REG_EIP) != 0x4b1428:
                raise ValueError('menu lookup exceeded its instruction bound')
            if struct.unpack('<h', cpu.mem_read(frame-0x60, 2))[0]:
                selected.append(struct.unpack('<H', cpu.mem_read(frame-0x38, 2))[0])
        cases.append({'member': member, 'flags': flags, 'selectable_jobs': selected})
    return {'source_image_sha256': SOURCE_SHA256, 'grid': order, 'member_variants': variants,
            'names': [source_string(raw, 0x616aac, job).decode('cp950') for job in range(31)],
            'lookup_probes': cases}


if __name__ == '__main__':
    path = ROOT/'prototype/data/school_job_menu.json'
    path.write_text(json.dumps(source_menu(), ensure_ascii=False, indent=2)+'\n', encoding='utf8', newline='\n')
