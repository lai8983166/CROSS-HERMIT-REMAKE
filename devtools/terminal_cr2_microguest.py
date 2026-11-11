"""Own 32-bit guest: two same-value MOV CR2 writes and one real page fault."""
import struct


def image():
    base = 0x100000
    data = bytearray(4096)
    word = lambda n: struct.pack('<I', n)
    def put(offset, value):
        if offset + len(value) > len(data):
            raise ValueError('guest image budget')
        data[offset:offset + len(value)] = value
    put(0, struct.pack('<III', 0x1badb002, 0, (-0x1badb002) & 0xffffffff))
    put(0x800, bytes.fromhex('0000000000000000ffff0000009bcf00ffff00000093cf00'))
    put(0x820, struct.pack('<HI', 23, base + 0x800))
    put(0x828, struct.pack('<HI', 0x7ff, base + 0x1000))
    put(0x100, bytes.fromhex('fa0f0115') + word(base + 0x820) + b'\xea' + word(base + 0x120) + bytes.fromhex('0800'))
    code = bytes.fromhex('66b810008ed88ec08ed0bc00401000')
    gate = struct.pack('<HHBBH', 0x400, 8, 0, 0x8e, 0x10)
    for offset in (0, 4):
        code += bytes.fromhex('c705') + word(0x101000 + 14 * 8 + offset) + gate[offset:offset + 4]
    code += bytes.fromhex('0f011d') + word(base + 0x828)
    # Guest-created page directory: first 4 MiB identity mapped, next absent.
    code += bytes.fromhex('c7050050100083000000')
    code += bytes.fromhex('b8005010000f22d80f20e083c8100f22e00f20c00d000000800f22c0')
    code += b'\xe9' + word(0x100300 - (0x100120 + len(code) + 5))
    put(0x120, code)
    body = bytes.fromhex('b8785634120f22d00f22d0a100004000')
    end = 0x100300 + len(body)
    body += bytes.fromhex('b043e6e9b810000000e7f4f4ebfd')
    put(0x300, body)
    # #PF frame: error, EIP, CS, EFLAGS. Skip only the known 5-byte MOV load.
    put(0x400, bytes.fromhex('ff0500201000834424040583c404cf'))
    elf = bytearray(4096)
    elf[:16] = bytes.fromhex('7f454c46010101000000000000000000')
    elf[16:52] = struct.pack('<HHIIIIIHHHHHH', 2, 3, 1, base + 0x100, 52, 0, 0, 52, 32, 1, 0, 0, 0)
    elf[52:84] = struct.pack('<IIIIIIII', 1, 4096, base, base, len(data), 0x7000, 7, 4096)
    return bytes(elf + data), dict(a=0x100300, b=end, mov_pcs=[0x100305, 0x100308],
                                  pf_pc=0x10030b, pf_address=0x400000, cr3=0x105000,
                                  mov_value=0x12345678, handler=0x100400)
