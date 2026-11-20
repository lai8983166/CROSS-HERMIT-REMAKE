"""Small static scene 8/17 projection using the existing YBC parser; no runner."""
import hashlib
import json
import struct
from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from capstone.x86_const import X86_OP_MEM
from tools.ybc32_disasm import parse, load_pool
from tools.tactics_exit_emulation import SOURCE, SOURCE_SHA256, ROOT


def catalog(scene_ids=(8, 17), extra_ops=()):
    image = SOURCE.read_bytes()
    assert hashlib.sha256(image).hexdigest() == SOURCE_SHA256
    def read(va, fmt):
        return struct.unpack_from('<' + fmt, image, va - 0x400000)
    md = Cs(CS_ARCH_X86, CS_MODE_32); md.detail = True
    pointer_instruction = next(md.disasm(image[0x5356b:0x5357b], 0x45356b))
    # This address is the original MOV table operand, not an inferred scene layout.
    assert pointer_instruction.mnemonic == 'mov' and pointer_instruction.operands[1].type == X86_OP_MEM
    pointer_va = pointer_instruction.operands[1].mem.disp
    scenes = {}
    for sid in scene_ids:
        path = ROOT / f'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/SCRIPT/T{sid:04}.BIN'
        raw = path.read_bytes()
        scripts = []
        for block, sub, pc, pool in parse(raw):
            texts = load_pool(raw, pool)
            commands, pages, page = [], [], []
            while True:
                op, advance = struct.unpack_from('<HH', raw, pc)
                assert advance >= 4 and pc + advance <= len(raw)
                if op == 17:
                    index = struct.unpack_from('<H', raw, pc + 4)[0]
                    page.append({'offset': pc, 'text': texts[index][2]})
                elif op == 51:
                    pages.append(page); page = []
                elif op in (113, 124, 130, 133, 136, 163, 165) + extra_ops:
                    cells = list(struct.unpack_from('<' + 'I' * ((advance - 4)//4), raw, pc + 4))
                    commands.append({'offset': pc, 'opcode': op, 'cells': cells,
                        'values': [v & 0xfffffff for v in cells]})
                if op == 19:
                    break
                pc += advance
            assert not page
            scripts.append({'block': block, 'sub': sub, 'pages': pages, 'commands': commands})
        ptr = read(pointer_va + sid * 4, 'I')[0]
        count = read(0x6a85ac + sid * 2, 'h')[0]
        templates = image[ptr - 0x400000:ptr - 0x400000 + count * 84]
        map_raw = (ROOT / f'CROSS HERMIT/CROSS HERMIT/DATA/TACTICS/MAP/MAP{sid:02}.BIN').read_bytes()
        width, height = struct.unpack_from('<2H', map_raw, 4)
        assert len(map_raw) == 16 + width * height * 6
        scenes[str(sid)] = {'script_sha256': hashlib.sha256(raw).hexdigest(),
            'script_bytes': len(raw), 'scripts': scripts, 'template_pointer': ptr,
            'template_count': count, 'template_sha256': hashlib.sha256(templates).hexdigest(),
            'map_sha256': hashlib.sha256(map_raw).hexdigest(),
            'event1_cells': [[i % width, i // width] for i in range(width * height) if map_raw[18 + i * 6] == 1],
            'templates_hex': [templates[i*84:(i+1)*84].hex() for i in range(count)]}
    return {'schema_version': 1, 'source_image_sha256': SOURCE_SHA256, 'scenes': scenes,
        'scene8_objective_lists': {hex(a): list(read(a, f'{n}h')) for a,n in ((0x5ff788,4),(0x5ff790,2),(0x5ff794,3))},
        'scene17_ambush_rows': [list(read(0x5ff7d4+i*4,'4b')) for i in range(4)],
        'scene17_repeat_rows': [list(read(0x5ff7e4+i*4,'4b')) for i in range(4)],
        'scope': 'Static source scripts/templates only; opcode names are not semantic authority. No native lifetime, UI, reward, or full replay claim.'}


if __name__ == '__main__':
    out = ROOT / 'prototype/data/school_adventure_scene_rules.json'
    out.write_text(json.dumps(catalog(), ensure_ascii=False, indent=2) + '\n', encoding='utf8', newline='\n')
    print(out, out.stat().st_size)
