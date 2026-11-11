"""Version 2 architectural 57-register projection of stopped TCG x86 state.

This is NOT the frozen Unicorn raw-register API contract: DR4/5 are DR6/7
aliases when CR4.DE=0; DE=1 is rejected. No synthetic padding value is used.
Only ordinary 32-bit protected-mode contexts fit this adapter. FIP/FDP
retain their actual 64-bit payload independently of instruction mode. No high
bits are truncated. A projection is not a CPU/machine checkpoint or replay proof.
"""
from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy

from tools.terminal_unit_frontends_trace import CPU_REGISTERS

SCHEMA = 'x86-architectural-canonical57-v2'
DR_POLICY = 'DE=0 aliases DR6/7; DE=1 undefined, not independent slots'
RAW_FIELDS = frozenset('schema fullstate_accepted vp_stopped cpu target_bits gpr eip '
    'eflags hflags efer segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt cr0_cr2_cr3_cr4 '
    'dr0_dr1_dr2_dr3_dr6_dr7 dr4_dr5_policy fp_control fp_status top '
    'fp_physical_low64_high16 fp_empty_mask fop fcs fds fip fdp mxcsr '
    'xmm_low64_high64'.split())
GP = ('EAX', 'ECX', 'EDX', 'EBX', 'ESP', 'EBP', 'ESI', 'EDI')
SEG = ('ES', 'CS', 'SS', 'DS', 'FS', 'GS', 'LDTR', 'TR', 'GDTR', 'IDTR')


class Canonical57Error(ValueError):
    """Explicitly unrepresentable or malformed source; never a partial result."""


def _fail(message):
    raise Canonical57Error(message)


def _uint(value, bits, name):
    if type(value) is not int or not 0 <= value < 1 << bits:
        _fail(f'{name}: unsigned {bits}-bit value required; no truncation')
    return value


def _hex(value, bits, name):
    if type(value) is not str or re.fullmatch('[0-9a-f]{16}', value) is None:
        _fail(f'{name}: exact 16-digit lowercase raw hex required')
    return _uint(int(value, 16), bits, name)


def _array(value, size, name):
    if type(value) is not list or len(value) != size:
        _fail(f'{name}: exact {size}-element array required')
    return value


def full_tag(physical_fp, empty_mask):
    """Reconstruct physical x87 full tags from actual 80-bit payloads/emptiness.

    Modern tag loads keep only empty/nonempty. TOP does not rotate this word.
    Empty payloads are retained, never overwritten or assumed zero.
    """
    _array(physical_fp, 8, 'physical FP')
    _uint(empty_mask, 8, 'empty mask')
    result = 0
    for i, pair in enumerate(physical_fp):
        mantissa, exponent = _array(pair, 2, f'FP{i}')
        _uint(mantissa, 64, f'FP{i}.mantissa')
        exp = _uint(exponent, 16, f'FP{i}.exponent') & 0x7fff
        tag = (3 if empty_mask & (1 << i) else
               1 if exp == 0 and mantissa == 0 else
               2 if exp in (0, 0x7fff) or not mantissa & (1 << 63) else 0)
        result |= tag << (2 * i)
    return result


def _canonical_widths(registers):
    if type(registers) is not dict or set(registers) != set(CPU_REGISTERS):
        _fail('exact canonical57 register names required')
    for name, value in registers.items():
        if name in ('GDTR', 'IDTR', 'LDTR', 'TR'):
            selector, base, limit, flags = _array(value, 4, name)
            _uint(selector, 16, name+'.selector')
            _uint(base, 32, name+'.base')
            _uint(limit, 16 if name in ('GDTR', 'IDTR') else 32, name+'.limit')
            _uint(flags, 32, name+'.flags')
            if name in ('GDTR', 'IDTR') and (selector or flags):
                _fail(name+': unused selector/flags must already be zero')
        elif re.fullmatch('FP[0-7]', name):
            mantissa, exponent = _array(value, 2, name)
            _uint(mantissa, 64, name+'.mantissa')
            _uint(exponent, 16, name+'.exponent')
        elif name.startswith('XMM'):
            _uint(value, 128, name)
        else:
            bits = (64 if name in ('FIP', 'FDP') else 11 if name == 'FOP' else 16 if name in
                    ('FPCW', 'FPSW', 'FPTAG', 'FCS', 'FDS', 'MXCSR',
                     'CS', 'DS', 'ES', 'FS', 'GS', 'SS') else 32)
            _uint(value, bits, name)
    if not registers['CR0'] & 1 or registers['EFLAGS'] & (1 << 17):
        _fail('ordinary protected mode required; real/v8086 mode unsupported')
    if registers['CR4'] & 8:
        _fail('CR4.DE=1: DR4/5 have no readable architectural value')
    if registers['DR4'] != registers['DR6'] or registers['DR5'] != registers['DR7']:
        _fail('DR4/5 must be architectural aliases, not raw API padding')
    empty = sum(((registers['FPTAG'] >> (2*i)) & 3 == 3) << i for i in range(8))
    if full_tag([registers[f'FP{i}'] for i in range(8)], empty) != registers['FPTAG']:
        _fail('full tag does not match physical FP80 classification')


def _receipt(registers, source, context):
    _canonical_widths(registers)
    return dict(schema=SCHEMA, registers={k:registers[k] for k in CPU_REGISTERS},
                source=source, context=context, dr45_semantics='architectural-alias-DE0',
                fp_order='physical-R0-through-R7; independent of TOP',
                legacy_unicorn_raw_api_compatible=False, full_machine_state=False,
                replay_accepted=False, windows_admitted=False)


def from_tcg(raw, *, expected_cpu, expected_vcpus):
    """Project one exact stopped tcg-state-v1 record, retaining omitted context.

    expected_cpu/vcpus are required caller assertions, not inferred defaults.
    Source/build/memory/event authentication must be performed by the caller.
    This function does not establish that a JSON record is an actual capture.
    """
    if type(raw) is not dict or set(raw) != RAW_FIELDS:
        _fail('exact tcg-state-v1 fields required; missing/unknown fields refused')
    if raw['schema'] != 'tcg-state-v1' or raw['fullstate_accepted'] is not False:
        _fail('source schema or qualification marker')
    _uint(expected_cpu, 16, 'expected CPU')
    _uint(expected_vcpus, 16, 'expected VP count')
    if not 0 < expected_vcpus <= 256 or expected_cpu >= expected_vcpus:
        _fail('expected CPU topology')
    if type(raw['cpu']) is not int or raw['cpu'] != expected_cpu:
        _fail('source CPU identity mismatch')
    stops = _array(raw['vp_stopped'], expected_vcpus, 'VP stop records')
    for i, row in enumerate(stops):
        if (type(row) is not dict or set(row) != {'cpu','stopped'} or
            type(row['cpu']) is not int or row['cpu'] != i or row['stopped'] is not True):
            _fail('all expected VPs must be explicitly stopped, in index order')
    if type(raw['target_bits']) is not int or raw['target_bits'] not in (32, 64):
        _fail('TCG target width')
    slots = 16 if raw['target_bits'] == 64 else 8
    gpr = [_hex(v, 32, f'gpr[{i}]') for i,v in enumerate(_array(raw['gpr'], slots, 'gpr'))]
    xmm = []
    for i, pair in enumerate(_array(raw['xmm_low64_high64'], slots, 'XMM')):
        lo, hi = _array(pair, 2, f'XMM{i}')
        xmm.append(_hex(lo,64,f'XMM{i}.low') | (_hex(hi,64,f'XMM{i}.high') << 64))
    if any(gpr[8:]) or any(xmm[8:]):
        _fail('nonzero R8..15/XMM8..15 cannot be silently discarded by 32-bit projection')
    segments = []
    for name, row in zip(SEG, _array(raw['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'],10,'segments')):
        a,b,c,d = _array(row,4,name)
        segments.append([_hex(a,16,name+'.selector'),_hex(b,32,name+'.base'),
                         _hex(c,16 if name in ('GDTR','IDTR') else 32,name+'.limit'),
                         _hex(d,32,name+'.flags')])
    efer = _hex(raw['efer'],64,'EFER')
    hflags = _hex(raw['hflags'],32,'hflags')
    cs_flags = segments[1][3]
    if (efer & 0x500 or hflags & 0xc000 or not hflags & 0x10 or
        not hflags & 0x80 or cs_flags & 0x200000 or
        not cs_flags & 0x400000 or cs_flags & 0x9800 != 0x9800):
        _fail('ordinary 32-bit protected CS required; long/compatibility/16-bit context refused')
    fp = [[_hex(a,64,f'FP{i}.low'),_hex(b,16,f'FP{i}.high')]
          for i,pair in enumerate(_array(raw['fp_physical_low64_high16'],8,'FP'))
          for a,b in [_array(pair,2,f'FP{i}')]]
    status = _uint(raw['fp_status'],16,'FPSW')
    top = _uint(raw['top'],3,'TOP')
    if top != (status >> 11) & 7:
        _fail('TOP and FPSW disagree')
    registers = dict(zip(GP,gpr[:8]))
    registers.update(EIP=_hex(raw['eip'],32,'EIP'), EFLAGS=_hex(raw['eflags'],32,'EFLAGS'),
        FPCW=_uint(raw['fp_control'],16,'FPCW'), FPSW=status,
        FPTAG=full_tag(fp,raw['fp_empty_mask']), FIP=_hex(raw['fip'],64,'FIP'),
        FDP=_hex(raw['fdp'],64,'FDP'), FCS=_uint(raw['fcs'],16,'FCS'),
        FDS=_uint(raw['fds'],16,'FDS'), FOP=_uint(raw['fop'],11,'FOP'),
        MXCSR=_uint(raw['mxcsr'],16,'MXCSR'))
    registers.update({name:segments[i][0] for i,name in enumerate(SEG[:6])})
    registers.update({name:segments[i] for i,name in enumerate(SEG) if i>=6})
    registers.update({f'CR{i}':_hex(v,32,f'CR{i}') for i,v in
                      zip((0,2,3,4),_array(raw['cr0_cr2_cr3_cr4'],4,'control registers'))})
    registers.update({f'DR{i}':_hex(v,32,f'DR{i}') for i,v in
                      zip((0,1,2,3,6,7),_array(raw['dr0_dr1_dr2_dr3_dr6_dr7'],6,'debug registers'))})
    if raw['dr4_dr5_policy'] != DR_POLICY:
        _fail('unrecognized source debug-register semantics')
    registers.update(DR4=registers['DR6'],DR5=registers['DR7'])
    registers.update({f'FP{i}':v for i,v in enumerate(fp)})
    registers.update({f'XMM{i}':v for i,v in enumerate(xmm[:8])})
    encoded = json.dumps(raw,sort_keys=True,separators=(',',':')).encode()
    return _receipt(registers,dict(kind='tcg-state-v1',json_sha256=hashlib.sha256(encoded).hexdigest()),
        dict(cpu=expected_cpu, target_bits=raw['target_bits'], vps=deepcopy(stops),
             efer=efer, hflags=hflags, segment_caches=dict(zip(SEG,segments)),
             omitted_extended_gpr=gpr[8:], omitted_extended_xmm=xmm[8:],
             constraints='57-register projection only; hidden caches/events/memory need separate validation'))


def from_unicorn(uc):
    """Read the new architectural57 contract from a local UC_MODE_32 engine.

    Read DR6/7 once and derive their DR4/5 aliases; never read raw DR4/5 slots.
    Descriptor memory is read to reject 16-bit/long CS; it does not prove hidden
    segment-cache equality. The caller must retain that separate prerequisite.
    No register or memory writes are performed by this adapter.
    """
    from unicorn import UC_ARCH_X86, UC_MODE_32, UC_QUERY_ARCH, UC_QUERY_MODE
    from unicorn import x86_const as x
    if uc.query(UC_QUERY_ARCH) != UC_ARCH_X86 or uc.query(UC_QUERY_MODE) != UC_MODE_32:
        _fail('Unicorn x86 UC_MODE_32 engine required')
    registers = {}
    for name in CPU_REGISTERS:
        if name in ('DR4','DR5'):
            continue
        value = uc.reg_read(getattr(x,'UC_X86_REG_'+name))
        registers[name] = list(value) if type(value) is tuple else value
    registers.update(DR4=registers['DR6'],DR5=registers['DR7'])
    _canonical_widths(registers)
    efer = uc.msr_read(0xc0000080)
    if efer & 0x500:
        _fail('Unicorn long/compatibility context cannot be projected')
    selector = registers['CS']
    if not selector & 0xfffc:
        _fail('null protected CS cannot establish 32-bit descriptor semantics')
    table = registers['LDTR'] if selector & 4 else registers['GDTR']
    offset = selector & ~7
    if offset + 7 > table[2]:
        _fail('CS descriptor lies outside table limit')
    if table[1] + offset + 7 > 0xffffffff:
        _fail('CS descriptor address overflows 32-bit context')
    descriptor = bytes(uc.mem_read(table[1]+offset,8))
    if len(descriptor) != 8:
        _fail('short CS descriptor read')
    flags = int.from_bytes(descriptor[4:8],'little') & 0x00f0ff00
    if flags & 0x200000 or not flags & 0x400000 or flags & 0x9800 != 0x9800:
        _fail('32-bit present code descriptor required')
    return _receipt(registers,dict(kind='unicorn-architectural-read-v2'),
                    dict(efer=efer, cs_descriptor_hex=descriptor.hex(),
                         constraints='descriptor memory is not proof of hidden cached segment state'))
