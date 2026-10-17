"""Source-derived renderer prerequisites; isolated experiments, not VM continuation."""
import hashlib
import struct
from functools import lru_cache

from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from tools.school_vm_graphics import SOURCE, SOURCE_SHA256, BASE, ROOT

# Exact original bodies. Jump tables are data and are pinned separately.
FUNCTIONS = {
    0x40D7E0: 0x40D87C, 0x4107B0: 0x410824,
    0x40D970: 0x40D9BA, 0x4142B0: 0x4142DD,
    0x40DAB0: 0x40DB10, 0x40DB10: 0x40DB81,
    0x40DB90: 0x40DBEB, 0x40DBF0: 0x40DC76,
    0x40DC80: 0x40DCCC, 0x428A40: 0x428AC6,
    0x40E2A0: 0x40E32F, 0x56DB00: 0x56DB21,
    0x410310: 0x4103E3, 0x40DCD0: 0x40DE91,
    0x40DF20: 0x40E14C, 0x56CEC0: 0x56CF18,
    0x56CE80: 0x56CE83,
}
ARG_COUNTS = {0x40D970: 1, 0x40DB10: 1, 0x40DBF0: 1,
              0x428A40: 1, 0x40E2A0: 4, 0x56DB00: 1,
              0x410310: 7, 0x40DCD0: 1, 0x40DF20: 2, 0x56CEC0: 3}
ZERO_FIELDS = (0, 4, 0x10, 0x14, 0x30, 0x1C, 0x34, 0x24,
               0x40, 0x44, 0x48, 0x4C, 0x50, 0x54, 0x58, 0x5C)
LAYER_COUNT = 4096
ARENA_BYTES = 1048576
PACKET_BYTES = 24
RECTANGLE_PROBES = (
    ((274, 580, 473, 154), 67, 0x223438, 1),
    ((10, 20, 30, 40), 67, 0xAABBCCDD, 2),
    ((-15, 25, 32, 41), 0x10044, 0x01020304, 0x101),
    ((1, 2, 3, 4), 4095, 0, 255),
)
CLIP_PROBES = (
    (274, 580, 473, 154), (1297, 0, 273, 1), (1298, 0, 273, 1),
    (-1297, 0, 273, 1), (-1298, 0, 273, 1),
    (0, 769, 1, 1), (0, 770, 1, 1), (0, -770, 1, 1),
    (0x80000000, 0, 0, 0), (0, 0x80000000, 0, 0),
    (0, 0, 0x7FFFFFFF, 0), (0, 0, 0, 0x7FFFFFFF),
)


def u32(value):
    return value & 0xFFFFFFFF


def i32(value):
    value = u32(value)
    return value - 0x100000000 if value & 0x80000000 else value


def dword(raw, offset):
    return struct.unpack_from('<I', raw, offset)[0]


def store(raw, offset, value):
    struct.pack_into('<I', raw, offset, u32(value))


@lru_cache(maxsize=1)
def source_contract():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('original renderer image SHA mismatch')
    decoder = Cs(CS_ARCH_X86, CS_MODE_32)
    checks = {
        0x412EAD: ('call', '0x40d7e0'),
        0x413473: ('mov', 'dword ptr [eax + 0xb278], ecx'),
        0x41347F: ('mov', 'dword ptr [edx + 0xb27c], eax'),
        0x413500: ('call', '0x40d970'),
        0x41350E: ('call', '0x40dab0'),
        0x40D993: ('mov', 'dword ptr [eax], ecx'),
        0x40D99A: ('call', '0x4142b0'),
        0x4142D0: ('mov', 'eax, dword ptr [eax + 0xb210]'),
        0x40DACD: ('push', '0x1000'),
        0x40DAE5: ('push', '0x100000'),
        0x428A6E: ('call', '0x56e810'),
        0x49E5A4: ('call', '0x425de0'),
        0x49E5CD: ('call', '0x40db90'),
        0x49E5DE: ('call', '0x40dc80'),
        0x49E60F: ('call', '0x4217c0'),
        0x49E685: ('call', '0x414c30'),
        0x49E6D9: ('call', '0x40e330'),
        0x49E734: ('call', '0x414de0'),
        0x49E7B7: ('call', '0x4152c0'),
        0x40DDC7: ('jae', '0x40ddd4'),
        0x4103C9: ('call', '0x40df20'),
    }
    proof = []
    for va, expected in checks.items():
        ins = next(decoder.disasm(raw[va-BASE:va-BASE+16], va))
        if (ins.mnemonic, ins.op_str) != expected:
            raise ValueError('renderer source instruction mismatch: ' + hex(va))
        proof.append(dict(va=hex(va), hex=ins.bytes.hex(), mnemonic=ins.mnemonic,
                          operands=ins.op_str))
    tables = []
    for at, fourth in ((0x40DE91, 0x40DDBB), (0x40E14C, 0x40E034)):
        data = raw[at-BASE:at-BASE+36]
        if struct.unpack('<9I', data)[3] != fourth:
            raise ValueError('rectangle kind4 source dispatch mismatch')
        tables.append(dict(va=hex(at), hex=data.hex()))
    bodies = [dict(va=hex(a), end=hex(b), bytes=b-a,
                   sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest())
              for a, b in FUNCTIONS.items()]
    return dict(source_image_sha256=SOURCE_SHA256, functions=bodies,
                instructions=proof, jump_tables=tables,
                queue=dict(layers=LAYER_COUNT, layer_bytes=LAYER_COUNT*8,
                           arena_bytes=ARENA_BYTES, rectangle_bytes=PACKET_BYTES,
                           allocator='0x56e810', allocator_kind='debug CRT adapter'),
                scope='isolated prerequisite probes; no pending VM state repair, '
                      'D3D initialization, GPU execution or full outer frame')


def constructor(before):
    if len(before) != 96:
        raise ValueError('renderer manager requires full96 bytes')
    after = bytearray(before)
    for offset in ZERO_FIELDS:
        store(after, offset, 0)
    store(after, 0x18, 1)
    store(after, 0x20, 1)
    return bytes(after)


def bind(before, owner, device):
    if not owner or len(before) != 96:
        raise ValueError('isolated owner must be explicitly declared')
    after = bytearray(before)
    store(after, 0, owner)
    store(after, 4, device)
    return bytes(after)


def initialize_queues(before, heads, arena):
    after = bytearray(before)
    for offset, value in ((8, LAYER_COUNT), (0xC, ARENA_BYTES), (0x10, heads),
                          (0x14, arena), (0x30, arena), (0x2C, 0)):
        store(after, offset, value)
    return bytes(after)


def clip(rect, dimensions):
    """Original rejection predicate, including signed overflow/INT_MIN abs."""
    if len(rect) != 4 or len(dimensions) != 2:
        raise ValueError('rectangle/dimensions shape')
    x, y, width, height = map(i32, rect)
    sw, sh = map(i32, dimensions)
    # 56DB00 negates in32 bits; INT_MIN remains negative.
    ax, ay = i32(abs(x)), i32(abs(y))
    return int(ax > i32(sw + width) or ay > i32(sh + height))


def rectangle_packet(before, rect, layer, color, blend, previous):
    if len(before) != PACKET_BYTES:
        raise ValueError('full24-byte rectangle packet required')
    after = bytearray(before)
    store(after, 0, previous)
    store(after, 4, 4)
    after[8] = blend & 255
    # Byte9 is padding retained from the declared allocator bytes.
    struct.pack_into('<5H', after, 10, *(u32(x) & 65535 for x in (*rect, layer)))
    store(after, 20, color)
    return bytes(after)
