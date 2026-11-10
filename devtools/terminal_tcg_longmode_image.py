"""Pure ELF32/multiboot builder for a bounded 64-bit x87 pointer probe.

No process, file, network, VM, assembler or compiler operations occur here.
The BSP enters long mode, aliases the same physical 2 MiB at 4 GiB, and
executes from that alias. Two configured VPs do not imply SMP execution.

The host may stop at expected['stop'] (before the second FXSAVE64), read its
stopped-state endpoint twice, remove the stop and resume. All state changes,
including FNINIT/PXOR/LDMXCSR/FXRSTOR64, are guest instructions. No CPU state
is imported by the host. This is an x87/SSE subset roundtrip, never a complete
CPU/machine/resource restore or Windows admission test.
"""
import struct


BASE = 0x100000
HIGH = 0x100000000


def image(_root=None):
    """Return (ELF bytes, expected/layout dict); _root is runner compatibility."""
    memory = bytearray(4096)

    def u32(value):
        return struct.pack('<I', value)

    def put(offset, value):
        if not 0 <= offset <= len(memory) - len(value):
            raise ValueError('initialized ELF segment overflow')
        memory[offset:offset + len(value)] = value

    put(0, struct.pack('<III', 0x1badb002, 0, (-0x1badb002) & 0xffffffff))
    # Null, 32-bit code, data, 64-bit code. Selectors 8/16/24.
    put(0x800, bytes.fromhex(
        '0000000000000000ffff0000009bcf00'
        'ffff00000093cf00ffff0000009baf00'))
    put(0x830, struct.pack('<HI', 31, BASE + 0x800))
    put(0x900, struct.pack('<ff', 1.0, 2.0))
    patterns = [bytes.fromhex('00112233445566778899aabbccddeeff'),
                bytes.fromhex('ffeeddccbbaa99887766554433221100'),
                bytes.fromhex('13579bdf2468ace00123456789abcdef')]
    for offset, pattern in zip((0x920, 0x930, 0x950), patterns):
        put(offset, pattern)
    put(0x940, struct.pack('<II', 0x3f80, 0x1f80))
    # Multiboot enters protected mode, paging off. Establish our own GDT/CS.
    put(0x100, bytes.fromhex('fa0f0115') + u32(BASE + 0x830) +
        b'\xea' + u32(BASE + 0x120) + bytes.fromhex('0800'))
    boot = bytearray(bytes.fromhex('66b810008ed88ec08ed08ee08ee8bc00001100fc'))
    # Zero PML4/PDPT/PD, then write a 2 MiB identity mapping and the 4 GiB alias.
    boot += b'\xbf' + u32(0x101000) + b'\xb9' + u32(3072) + bytes.fromhex('31c0f3ab')
    for address, value in ((0x101000, 0x102003), (0x102000, 0x103003),
                           (0x102020, 0x103003), (0x103000, 0x83)):
        boot += bytes.fromhex('c705') + u32(address) + u32(value)
    # Actual CPUID receipts, not host-derived capability claims.
    for leaf, address in ((1, 0x109000), (7, 0x109010), (0x80000001, 0x109020)):
        boot += b'\xb8' + u32(leaf) + bytes.fromhex('31c90fa2')
        boot += b'\xa3' + u32(address)
        for modrm, offset in ((0x1d, 4), (0x0d, 8), (0x15, 12)):
            boot += bytes((0x89, modrm)) + u32(address + offset)
    # CR0.EM/TS off, MP/NE on; CR4.PAE/OSFXSR/OSXMMEXCPT on.
    boot += bytes.fromhex('0f20c083e0f383c8220f22c0')
    boot += bytes.fromhex('0f20e00d200600000f22e0')
    boot += b'\xb8' + u32(0x101000) + bytes.fromhex('0f22d8')
    boot += b'\xb9' + u32(0xc0000080) + bytes.fromhex('0f320d000100000f30')
    boot += bytes.fromhex('0f20c00d000000800f22c0')
    boot += b'\xea' + u32(BASE + 0x300) + bytes.fromhex('1800')
    if 0x120 + len(boot) > 0x300:
        raise ValueError('bootstrap overlaps long-mode entry')
    put(0x120, boot)
    # The low entry is long-mode code; jump to the >4 GiB alias before x87.
    put(0x300, bytes.fromhex('48b8') + struct.pack('<Q', HIGH + BASE + 0x320) +
        bytes.fromhex('ffe0'))
    code = bytearray()

    def rip_operand(opcode, target):
        here = HIGH + BASE + 0x320 + len(code)
        code.extend(opcode + struct.pack('<i', target - (here + len(opcode) + 4)))

    def absolute(opcode, address):
        # opcode includes ModRM+SIB for a sign-extended disp32 address.
        code.extend(opcode + u32(address))

    # Record control state in the final 32 bytes of the 80-byte metadata block.
    for cr_opcode, address in (('0f20c0', 0x109030), ('0f20d8', 0x109038),
                                ('0f20e0', 0x109040)):
        code += bytes.fromhex(cr_opcode)
        absolute(bytes.fromhex('48890425'), address)
    code += b'\xb9' + u32(0xc0000080) + bytes.fromhex('0f3248c1e2204809d0')
    absolute(bytes.fromhex('48890425'), 0x109048)
    # FS.base=4 GiB; FS selector stays 16. FADD accesses FS:[0x100904].
    code += b'\xb9' + u32(0xc0000100) + bytes.fromhex('31c0ba010000000f30')
    code += b'\xbf' + u32(0x108000) + b'\xb9' + u32(0x600 // 4)
    code += b'\xb8' + u32(0xa5a5a5a5) + bytes.fromhex('fcf3ab')
    rip_operand(bytes.fromhex('f30f6f05'), HIGH + BASE + 0x920)  # XMM0
    rip_operand(bytes.fromhex('f30f6f3d'), HIGH + BASE + 0x930)  # XMM7
    rip_operand(bytes.fromhex('f3440f6f3d'), HIGH + BASE + 0x950)  # XMM15
    rip_operand(bytes.fromhex('0fae15'), HIGH + BASE + 0x940)  # MXCSR=3f80
    code += bytes.fromhex('dbe3')
    rip_operand(bytes.fromhex('d905'), HIGH + BASE + 0x900)
    fip = HIGH + BASE + 0x320 + len(code)
    absolute(bytes.fromhex('64d80425'), BASE + 0x904)
    absolute(bytes.fromhex('480fae0425'), 0x108000)  # FXSAVE64 baseline
    code += bytes.fromhex('dbe3')
    # A memory FLD also re-seeds nonzero FCS/FDS after FNINIT, so the
    # subsequent FXRSTOR64 must actually clear them rather than inherit zero.
    rip_operand(bytes.fromhex('d905'), HIGH + BASE + 0x904)
    # Deliberately clobber every XMM, not merely FNINIT (which leaves them alone).
    for reg in range(16):
        code += bytes.fromhex('660fef' if reg < 8 else '66450fef')
        code += bytes((0xc0 + 9 * (reg & 7),))
    rip_operand(bytes.fromhex('0fae15'), HIGH + BASE + 0x944)  # MXCSR=1f80
    absolute(bytes.fromhex('480fae0c25'), 0x108000)  # FXRSTOR64
    stop = HIGH + BASE + 0x320 + len(code)
    absolute(bytes.fromhex('480fae0425'), 0x108200)  # FXSAVE64 restored
    absolute(bytes.fromhex('0fae0425'), 0x108400)  # 32-bit pointer-format FXSAVE
    for address, count in ((0x108000, 1536), (0x109000, 80)):
        code += b'\xbe' + u32(address) + b'\xb9' + u32(count) + bytes.fromhex('ace6e9e2fb')
    code += bytes.fromhex('b810000000e7f4f4ebfd')
    if 0x320 + len(code) > 0x800:
        raise ValueError('64-bit code overlaps GDT')
    put(0x320, code)
    elf = bytearray(4096)
    elf[:16] = bytes.fromhex('7f454c46010101000000000000000000')
    elf[16:52] = struct.pack('<HHIIIIIHHHHHH', 2, 3, 1, BASE + 0x100,
                            52, 0, 0, 52, 32, 1, 0, 0, 0)
    elf[52:84] = struct.pack('<IIIIIIII', 1, 4096, BASE, BASE,
                            len(memory), 0x12000, 7, 4096)
    expected = {
        'schema': 'tcg-longmode-image-v1', 'full57': False,
        'fip': fip, 'fdp': HIGH + BASE + 0x904, 'fcs': 0, 'fds': 0,
        'fop': 4, 'stop': stop, 'top': 7, 'fp_status': 0x3800,
        'fp_control': 0x37f, 'fp_empty_mask': 0x7f,
        'physical_st7_low64_high16': [0xc000000000000000, 0x4000],
        'mxcsr': 0x3f80, 'cs': 24, 'fs_selector': 16, 'fs_base': HIGH,
        'cr3': 0x101000, 'required_cr0_set': 0x80000023,
        'required_cr0_clear': 0xc, 'required_cr4_set': 0x620,
        'required_efer_set': 0x500,
        'xmm_patterns': {str(i): p.hex() for i, p in zip((0, 7, 15), patterns)},
        'exit_code': 33, 'output_bytes': 1616,
        'output_layout': {
            'fxsave64_before': [0, 512], 'fxsave64_after': [512, 512],
            'fxsave32_after': [1024, 512], 'cpuid_1_eax_ebx_ecx_edx': [1536, 16],
            'cpuid_7_0_eax_ebx_ecx_edx': [1552, 16],
            'cpuid_80000001_eax_ebx_ecx_edx': [1568, 16],
            'cr0_cr3_cr4_efer_u64': [1584, 32]},
        'fxsave64_written_spans': [[0, 5], [6, 32]] +
            [[32 + i * 16, 42 + i * 16] for i in range(8)] + [[160, 416]],
        'fxsave32_pointer_expectation': {
            'fip_low32': fip & 0xffffffff, 'fdp_low32': (BASE + 0x904),
            'fcs': 0, 'fds': 0, 'fop': 4},
        'requires_actual_cpuid': {'leaf1_edx_set': (1 << 24) | (1 << 25) | (1 << 26),
            'leaf80000001_edx_set': 1 << 29, 'leaf7_0_ebx_clear': (1 << 6) | (1 << 13)},
        'trace_filter': '0x100000..0x112000,0x100100000..0x100112000',
        'mapping': {'pml4': 0x101000, 'pdpt': 0x102000, 'pd': 0x103000,
                    'pdpt_indices': [0, 4], 'physical_2m_base': 0,
                    'linear_2m_bases': [0, HIGH]},
        'limitations': ['BSP only; no AP startup handshake',
            'No guest exception handler; fault/triple-fault is a failed bounded probe',
            'No XSAVE/XRSTOR, pending exception or complete CPU restore proof',
            'Expected is an implementation test contract, not observed execution'],
    }
    return bytes(elf + memory), expected
