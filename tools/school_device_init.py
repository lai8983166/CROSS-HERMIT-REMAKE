"""Original windowed device initialization, with live platform inputs kept separate."""
import hashlib
import struct
from functools import lru_cache

from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from tools.school_renderer_init import (
    SOURCE, SOURCE_SHA256, BASE, ROOT, constructor, u32, i32, dword, store,
)

FUNCTIONS = {
    0x40D7E0: 0x40D87C, 0x4107B0: 0x410824,
    0x413450: 0x41355B, 0x4136D0: 0x413726,
    0x413730: 0x413844, 0x413850: 0x4138A0,
    0x4138A0: 0x413B03, 0x413FA0: 0x414009,
    0x414010: 0x41408E, 0x414090: 0x41418C,
    0x414190: 0x414278, 0x526C40: 0x526C46,
    0x56CE80: 0x56CE83, 0x56CEC0: 0x56CF18,
}
ARG_COUNTS = {0x413450: 5, 0x413730: 2, 0x413850: 2,
              0x4138A0: 1, 0x526C40: 1, 0x56CEC0: 3}
ATTEMPTS = ((1, 0x40), (1, 0x20), (2, 0x40), (2, 0x20))
STOP = 0x415F50
SLOT = 0x59246C
FORMATS = (25, 24, 23, 21, 20, 22, 26, 27, 28, 29, 30,
           40, 41, 50, 51, 52, 60, 61, 62, 63, 64, 65)


@lru_cache(maxsize=1)
def source_contract():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('device original source SHA')
    descriptor = struct.unpack_from('<5I', raw, 0x1FD6A8)
    if (raw[descriptor[3]:].split(b'\0', 1)[0] != b'd3d8.dll'
            or descriptor[4]+BASE != SLOT):
        raise ValueError('original d3d8 import descriptor')
    thunk = dword(raw, descriptor[0])
    if raw[thunk+2:].split(b'\0', 1)[0] != b'Direct3DCreate8':
        raise ValueError('original factory import name')
    if struct.unpack_from('<23I', raw, 0x5FF4AC-BASE) != (*FORMATS, 0):
        raise ValueError('original preferred format list')
    checks = {
        0x413488: ('call', '0x4136d0'), 0x4136ED: ('push', '0xdc'),
        0x526C40: ('jmp', 'dword ptr [0x59246c]'),
        0x4134B1: ('call', '0x413730'), 0x413901: ('call', 'dword ptr [eax + 0x20]'),
        0x4139E8: ('or', 'al, 4'), 0x413A10: ('call', 'dword ptr [eax + 0x3c]'),
        0x414061: ('call', 'dword ptr [ecx + 0x1c]'),
        0x4140F8: ('call', 'dword ptr [edx + 0x40]'),
        0x414126: ('call', 'dword ptr [edx + 0x20]'),
        0x41414B: ('call', 'dword ptr [edx + 8]'),
        0x414226: ('call', 'dword ptr [ecx + 0x28]'),
        0x413AD1: ('call', 'dword ptr [eax + 0xa0]'),
        0x4134DE: ('call', '0x415f50'),
        0x413500: ('call', '0x40d970'), 0x41350E: ('call', '0x40dab0'),
    }
    decoder = Cs(CS_ARCH_X86, CS_MODE_32)
    proof = []
    for va, expected in checks.items():
        ins = next(decoder.disasm(raw[va-BASE:va-BASE+16], va))
        if (ins.mnemonic, ins.op_str) != expected:
            raise ValueError('device original instruction '+hex(va))
        proof.append(dict(va=hex(va), hex=ins.bytes.hex(), mnemonic=ins.mnemonic,
                          operands=ins.op_str))
    return dict(source_image_sha256=SOURCE_SHA256,
                import_identity=dict(descriptor='0x5fd6a8', slot=hex(SLOT),
                                     dll='d3d8.dll', symbol='Direct3DCreate8', sdk=220),
                functions=[dict(va=hex(a), end=hex(b),
                                sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest())
                           for a, b in FUNCTIONS.items()], instructions=proof,
                preferred_formats=list(FORMATS), attempts=[list(p) for p in ATTEMPTS],
                scope='declared original startup prefix with live x86 D3D8 calls; '
                      'stop at font initialization before owner/queue binding; '
                      'no retained VM advancement, draw, Present or fullscreen')


def presentation(width, height, format, window):
    return struct.pack('<13I', width, height, format, 1, 0, 1, window, 1, 0, 0, 0, 0, 0)


def project_owner(initial, width, height, window, calls):
    """Independent source stores and real API outputs to the font-call boundary."""
    if len(initial) != 0xC000:
        raise ValueError('complete declared startup owner required')
    after = bytearray(initial)
    store(after, 0xB278, width)
    store(after, 0xB27C, height)
    factory = next(c['result']['factory']['pointer'] for c in calls if c['op'] == 'factory')
    store(after, 0xB20C, factory)
    creates = [c for c in calls if c['op'] == 'create_device']
    if not 1 <= len(creates) <= 4:
        raise ValueError('original bounded device attempts')
    for number, row in enumerate(creates):
        kind, flags = ATTEMPTS[number]
        if row['request']['type'] != kind or row['request']['flags'] != flags | 4:
            raise ValueError('original device fallback ordering')
        if number < len(creates)-1 and i32(row['result']['hr']) >= 0:
            raise ValueError('original fallback stops on success')
    create = creates[-1]
    if i32(create['result']['hr']) < 0 or not create['result'].get('device'):
        raise ValueError('successful live device prerequisite')
    store(after, 0xB1F8, ATTEMPTS[len(creates)-1][0])
    store(after, 0xB1FC, ATTEMPTS[len(creates)-1][1])
    store(after, 0xB204, window)
    mode = [c for c in calls if c['op'] == 'display_mode'][-1]['result']
    after[0xB214:0xB224] = bytes.fromhex(mode['hex'])
    after[0xB234:0xB268] = bytes.fromhex(create['result']['presentation_hex'])
    store(after, 0xB210, create['result']['device']['pointer'])
    caps = next(c['result'] for c in calls if c['op'] == 'caps')
    after[0xB314:0xB3E8] = bytes.fromhex(caps['hex'])
    desc = next(c['result'] for c in calls if c['op'] == 'describe_surface')
    after[0xB3E8:0xB408] = bytes.fromhex(desc['hex'])
    store(after, 0xB234, dword(bytes.fromhex(desc['hex']), 24))
    store(after, 0xB238, dword(bytes.fromhex(desc['hex']), 28))
    checks = [c for c in calls if c['op'] == 'check_format']
    if not checks or [c['request']['format'] for c in checks] != list(FORMATS[:len(checks)]):
        raise ValueError('original format scan ordering')
    if any(i32(c['result']['hr']) >= 0 for c in checks[:-1]) or i32(checks[-1]['result']['hr']) < 0:
        raise ValueError('original format scan success boundary')
    store(after, 0xB268, checks[-1]['request']['format'])
    after[0xBA08:0xBA20] = struct.pack('<6I', 0, 0, width, height, 0, 0x3F800000)
    return bytes(after)
