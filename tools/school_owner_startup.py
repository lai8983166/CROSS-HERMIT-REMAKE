"""Complete original renderer-owner construction and first font dependency boundary."""
import hashlib
import struct
from functools import lru_cache

from capstone import Cs, CS_ARCH_X86, CS_MODE_32
from tools.school_device_init import SOURCE, SOURCE_SHA256, BASE, ROOT, constructor, dword, store, u32, i32
from tools.school_device_init import FUNCTIONS as DEVICE_FUNCTIONS, ARG_COUNTS as DEVICE_ARGS

CTOR = 0x412E30
FONT_STOP = 0x52AE11
STARTS = (0x412E30, 0x409900, 0x420990, 0x41EAD0, 0x417530, 0x41EE30,
          0x410C20, 0x40BE70, 0x40C1A0, 0x40C140, 0x41D0D0, 0x41D2E0,
          0x41E6B0, 0x417C40, 0x417E00, 0x41AB10, 0x40B590, 0x415A90,
          0x4170C0, 0x414F90, 0x415370, 0x415530, 0x415F50, 0x416140,
          0x416320, 0x4162C0, 0x52AFE6)
IMPORTS = {0x59234C: ('GetDC', 0x5FD5E0, 0x412FCB, 1),
           0x592284: ('QueryPerformanceCounter', 0x5FD5CC, 0x41716C, 1),
           0x592288: ('QueryPerformanceFrequency', 0x5FD5CC, 0x4130EE, 1),
           0x5920A0: ('CreateFontA', 0x5FD5F4, 0x415FCA, 14),
           0x592068: ('GetObjectA', 0x5FD5F4, 0x52AFFB, 3)}
FONT_ARGS = [0, 0, 0, 0, 700, 0, 0, 0, 1, 5, 0, 0, 0, 0x592C9C]
ARGS = dict(DEVICE_ARGS, **{})
ARGS.update({0x56DDA0: 5, 0x4170C0: 1, 0x414F90: 1, 0x416320: 1,
             0x4162C0: 1, 0x52AFE6: 3})


@lru_cache(maxsize=1)
def source_contract():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('owner startup source SHA')
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    functions = dict(DEVICE_FUNCTIONS)
    for at in STARTS:
        for ins in md.disasm(raw[at-BASE:at-BASE+40000], at):
            if ins.mnemonic == 'ret':
                functions[at] = ins.address+ins.size
                break
        else:
            raise ValueError('owner finite native body')
    # Array construction includes its internal finally return and main ret20.
    functions[0x56DDA0] = 0x56DE40
    imports = []
    for slot, (name, at, ret, count) in IMPORTS.items():
        desc = struct.unpack_from('<5I', raw, at-BASE)
        ordinal = (slot-BASE-desc[4])//4
        thunk = dword(raw, desc[0]+ordinal*4)
        if raw[thunk+2:].split(b'\0', 1)[0] != name.encode('ascii'):
            raise ValueError('owner original import '+name)
        imports.append(dict(slot=hex(slot), descriptor=hex(at), symbol=name,
                            return_va=hex(ret), arguments=count,
                            dll=raw[desc[3]:].split(b'\0', 1)[0].decode('ascii')))
    if dword(raw, 0x799AD0-BASE) != 1 or dword(raw, 0x799AD4-BASE) != 1 or dword(raw, 0x5FF530-BASE):
        raise ValueError('owner inherited initialized timer globals')
    face = raw[0x592C9C-BASE:].split(b'\0', 1)[0]
    if face.hex() != 'b2d3a9fac5e920':
        raise ValueError('owner original font face bytes')
    checks = {0x412F28: ('mov', 'dword ptr [eax + 0xb270], 0'),
              0x412F35: ('mov', 'dword ptr [ecx + 0xb26c], 0'),
              0x412F5D: ('mov', 'dword ptr [ecx + eax*4 + 0x1090], 0'),
              0x4130B2: ('mov', 'word ptr [edx + 0xb28e], 1'),
              0x415F9B: ('call', '0x416140'), 0x415FFD: ('call', '0x4162c0'),
              0x4162EF: ('call', '0x52afe6'), 0x52B010: ('call', '0x52ae11')}
    proof = []
    for va, expected in checks.items():
        ins = next(md.disasm(raw[va-BASE:va-BASE+16], va))
        if (ins.mnemonic, ins.op_str) != expected:
            raise ValueError('owner original instruction '+hex(va))
        proof.append(dict(va=hex(va), hex=ins.bytes.hex(), mnemonic=ins.mnemonic, operands=ins.op_str))
    return dict(source_image_sha256=SOURCE_SHA256, functions=[dict(va=hex(a), end=hex(b),
                sha256=hashlib.sha256(raw[a-BASE:b-BASE]).hexdigest()) for a, b in functions.items()],
                imports=imports, instructions=proof, font_args=FONT_ARGS, face_hex=face.hex(),
                inherited_timer_globals_hex=raw[0x799AD0-BASE:0x799B10-BASE].hex(),
                scope='full owner constructor on inherited source globals; real device prefix and '
                      'GDI font/LOGFONT to unexecuted static font constructor; no retained VM repair')


def functions():
    return {int(r['va'], 16): int(r['end'], 16) for r in source_contract()['functions']}


def project_constructor(before, api):
    if len(before) != 0xC000:
        raise ValueError('full48KiB owner required')
    after = bytearray(before)
    def fields(base, values):
        for offset, value in values.items():
            store(after, base+offset, value)
    def zero(at, size):
        after[at:at+size] = bytes(size)
    def record(at):
        fields(at, {0: 0, 4: 0, 12: 0, 16: -1})
        after[at+8] = 255
    fields(0, {**{a: 0 for a in (0, 4, 8, 12, 16, 20, 44, 48, 52, 56, 60)}, 64: -1})
    record(24)
    zero(0x44, 100*8)
    zero(0x844, 256*8)
    record(0x1044)
    after[0x1058:0x10B8] = constructor(after[0x1058:0x10B8])
    zero(0x10B8, 12)
    fields(0x1A98, {0: 0, 4: 0, 8: 0, 12: 0, 16: 0})
    zero(0x1AAC, 0x7080)
    after[0x8B2C:0x8C2C] = bytes([255])*0x100
    zero(0x8C2C, 0x50)
    fields(0x8C80, {0: 0})
    for at in (0x8C88, 0x8F00):
        fields(at, {**{a: 0 for a in (*range(0, 32, 4), 0x248, 0x250, 0x258,
                                      0x260, 0x264, 0x268, 0x270)}, 0x25C: 0x3FF00000})
        zero(at+0x20, 4)
        after[at+0x26C:at+0x270] = struct.pack('<f', i32(dword(before, at+0x24C)))
    b = 0x9178
    fields(b, {**{a: 0 for a in (0, 4, 8, 0x134, 0x138, 0x16C, 0x1760, 0x1764,
                                 0x1768, 0x1774, 0x1778, 0x177C)}, 0x176C: -1})
    for offset, count in ((0x13C, 0x30), (0x174, 0xD0), (0x244, 0x150C),
                           (12, 256), (0x10C, 40), (0x1780, 0x880)):
        zero(b+offset, count)
    for offset in (0x170, 0x1770, 0x2000):
        after[b+offset] = 0
    fields(0, {**{a: 0 for a in (0xB200, 0xB26C, 0xB270, 0x1090, 0x1094,
                                0xB278, 0xB27C, 0xB284, 0xB280, 0xB204, 0xB20C,
                                0xB210, 0xB310, 0xB190, 0xB194, 0xB198, 0xB19C,
                                0xB1A0, 0xB1A8, 0xB1AC, 0xB1B0, 0xB1B4, 0xB1C0,
                                0xB1C4, 0xB1C8, 0xB1CC, 0xB1D0, 0xB1D8, 0xB1DC,
                                0xB1E0, 0xB1E4, 0xB1E8, 0xB1EC, 0xB1F4)},
               0xB1F8: 1, 0xB1FC: 64, 0xB180: 1, 0xB1F0: 10,
               0xB208: api['GetDC']['result']})
    zero(0xB234, 52)
    zero(0xB214, 16)
    zero(0xB274, 4)
    struct.pack_into('<4H', after, 0xB288, 0, 1, 0, 1)
    after[0xB17C] = 0
    frequency = bytes.fromhex(api['QueryPerformanceFrequency']['hex'])
    after[0xB188:0xB190] = frequency if api['QueryPerformanceFrequency']['result'] else bytes(8)
    return bytes(after)


def project_image(api):
    raw = bytearray(SOURCE.read_bytes())
    raw[0x765728-BASE:0x791728-BASE] = bytes(0x2C000)
    raw[0x791728-BASE:0x79172A-BASE] = bytes(2)
    raw[0x799AE0-BASE:0x799AE8-BASE] = bytes(8)
    raw[0x799AE8-BASE:0x799AF0-BASE] = bytes.fromhex(api['QueryPerformanceCounter']['hex'])
    raw[0x5FF530-BASE:0x5FF534-BASE] = bytes(4)
    return bytes(raw)
