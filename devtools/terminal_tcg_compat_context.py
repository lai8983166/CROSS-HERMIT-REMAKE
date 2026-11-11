"""Lossless envelope for one stopped tcg-state-v1 compatibility-mode record.

The versioned 57-name view is NOT a legacy Unicorn32 load format: GPRs expose
low32, but control/debug registers and descriptor bases retain 64 bits. Original
raw strings, extended registers and all hidden-cache fields remain in raw64.
A caller-supplied digest anchors this record; it does not authenticate capture,
build identity, memory or events. No engine writes or replay admission occur.
"""
from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import re

from devtools.terminal_tcg_canonical57_v2 import (
    CPU_REGISTERS, DR_POLICY, GP, RAW_FIELDS, SEG, full_tag,
)

SCHEMA = 'x86-compat-context-v1'
VIEW_SCHEMA = 'x86-compat32-visible57-v1'


class CompatContextError(ValueError):
    """Malformed, inconsistent, changed or unsupported capture."""


def _fail(message):
    raise CompatContextError(message)


def _uint(value, bits, name):
    if type(value) is not int or not 0 <= value < (1 << bits):
        _fail(f'{name}: unsigned {bits}-bit integer required')
    return value


def _hex(value, bits, name):
    if type(value) is not str or re.fullmatch('[0-9a-f]{16}', value) is None:
        _fail(f'{name}: exact lowercase 16-digit raw hex required')
    return _uint(int(value, 16), bits, name)


def _array(value, count, name):
    if type(value) is not list or len(value) != count:
        _fail(f'{name}: exact {count}-element list required')
    return value


def source_digest(raw):
    """Hash canonical JSON, NOT the original file bytes or a capture signature."""
    try:
        encoded = json.dumps(raw, sort_keys=True, separators=(',', ':'),
                             ensure_ascii=True, allow_nan=False).encode('ascii')
    except (TypeError, ValueError, UnicodeError) as exc:
        raise CompatContextError('source is not canonical JSON data') from exc
    return hashlib.sha256(encoded).hexdigest()


def _validate(raw, expected_cpu, expected_vcpus):
    if type(raw) is not dict or set(raw) != RAW_FIELDS:
        _fail('exact tcg-state-v1 field set required')
    if raw['schema'] != 'tcg-state-v1' or raw['fullstate_accepted'] is not False:
        _fail('source schema/qualification mismatch')
    _uint(expected_cpu, 16, 'expected CPU')
    _uint(expected_vcpus, 16, 'expected VP count')
    if not 0 < expected_vcpus <= 256 or expected_cpu >= expected_vcpus:
        _fail('expected topology invalid')
    if type(raw['cpu']) is not int or raw['cpu'] != expected_cpu:
        _fail('source CPU mismatch')
    if type(raw['target_bits']) is not int or raw['target_bits'] != 64:
        _fail('64-bit TCG target required')
    for i, row in enumerate(_array(raw['vp_stopped'], expected_vcpus, 'VP records')):
        if (type(row) is not dict or set(row) != {'cpu', 'stopped'} or
                type(row['cpu']) is not int or row['cpu'] != i or
                row['stopped'] is not True):
            _fail('all expected VPs must be explicitly stopped in index order')
    gpr = [_hex(v, 64, f'GPR{i}') for i, v in enumerate(_array(raw['gpr'], 16, 'GPR'))]
    xmm = []
    for i, pair in enumerate(_array(raw['xmm_low64_high64'], 16, 'XMM')):
        lo, hi = _array(pair, 2, f'XMM{i}')
        xmm.append(_hex(lo, 64, f'XMM{i}.low') | (_hex(hi, 64, f'XMM{i}.high') << 64))
    segments = []
    for name, row in zip(SEG, _array(raw['segments_es_cs_ss_ds_fs_gs_ldt_tr_gdt_idt'], 10, 'segments')):
        selector, base, limit, flags = _array(row, 4, name)
        segments.append([_hex(selector, 16, name+'.selector'), _hex(base, 64, name+'.base'),
                         _hex(limit, 16 if name in ('GDTR', 'IDTR') else 32, name+'.limit'),
                         _hex(flags, 32, name+'.flags')])
    cr = {n: _hex(v, 64, f'CR{n}') for n, v in zip((0, 2, 3, 4),
          _array(raw['cr0_cr2_cr3_cr4'], 4, 'CR'))}
    dr = {n: _hex(v, 64, f'DR{n}') for n, v in zip((0, 1, 2, 3, 6, 7),
          _array(raw['dr0_dr1_dr2_dr3_dr6_dr7'], 6, 'DR'))}
    if raw['dr4_dr5_policy'] != DR_POLICY:
        _fail('unknown DR4/5 source semantics')
    eip = _hex(raw['eip'], 32, 'compatibility EIP')
    flags = _hex(raw['eflags'], 32, 'EFLAGS')
    hflags = _hex(raw['hflags'], 32, 'hflags')
    efer = _hex(raw['efer'], 64, 'EFER')
    cs = segments[1]
    if (efer & 0x500 != 0x500 or cr[0] & 0x80000001 != 0x80000001 or
            not cr[4] & 0x20 or flags & 0x20000 or
            cs[3] & 0x200000 or not cs[3] & 0x400000 or
            cs[3] & 0x9800 != 0x9800 or not cs[0] & 0xfffc):
        _fail('active IA-32e compatibility32 CS/PE/PG/PAE required')
    if (hflags & 0xc090 != 0x4090 or hflags & 3 != cs[0] & 3 or
            bool(hflags & 0x20) != bool(segments[2][3] & 0x400000) or
            (hflags >> 9) & 7 != (cr[0] >> 1) & 7 or
            bool(hflags & (1 << 22)) != bool(cr[4] & (1 << 9))):
        _fail('hflags disagree with architectural mode/control/segment state')
    fp = []
    for i, pair in enumerate(_array(raw['fp_physical_low64_high16'], 8, 'physical FP')):
        lo, hi = _array(pair, 2, f'FP{i}')
        fp.append([_hex(lo, 64, f'FP{i}.low'), _hex(hi, 16, f'FP{i}.high')])
    cw = _uint(raw['fp_control'], 16, 'FPCW')
    sw = _uint(raw['fp_status'], 16, 'FPSW')
    top = _uint(raw['top'], 3, 'TOP')
    empty = _uint(raw['fp_empty_mask'], 8, 'physical empty mask')
    if top != (sw >> 11) & 7:
        _fail('TOP/FPSW mismatch')
    fop = _uint(raw['fop'], 11, 'FOP')
    fcs = _uint(raw['fcs'], 16, 'FCS')
    fds = _uint(raw['fds'], 16, 'FDS')
    fip = _hex(raw['fip'], 64, 'FIP')
    fdp = _hex(raw['fdp'], 64, 'FDP')
    mxcsr = _uint(raw['mxcsr'], 16, 'MXCSR')
    registers = dict(zip(GP, (v & 0xffffffff for v in gpr[:8])))
    registers.update(EIP=eip, EFLAGS=flags, FPCW=cw, FPSW=sw,
                     FPTAG=full_tag(fp, empty), FIP=fip, FDP=fdp,
                     FCS=fcs, FDS=fds, FOP=fop, MXCSR=mxcsr)
    registers.update({name: segments[i][0] for i, name in enumerate(SEG[:6])})
    registers.update({name: segments[i] for i, name in enumerate(SEG) if i >= 6})
    registers.update({f'CR{n}': v for n, v in cr.items()})
    registers.update({f'DR{n}': v for n, v in dr.items()})
    if cr[4] & 8:
        # Explicit unavailability is not a numeric zero or an independent slot.
        registers.update({f'DR{n}': {'readable': False, 'reason': 'CR4.DE=1: #UD'} for n in (4, 5)})
        dr_policy = 'DE1-unreadable'
    else:
        registers.update(DR4=dr[6], DR5=dr[7])
        dr_policy = 'DE0-architectural-aliases-DR6-DR7'
    registers.update({f'FP{i}': v for i, v in enumerate(fp)})
    registers.update({f'XMM{i}': v for i, v in enumerate(xmm[:8])})
    if set(registers) != set(CPU_REGISTERS):
        _fail('internal 57-name mapping mismatch')
    return dict(schema=VIEW_SCHEMA,
                registers={name: registers[name] for name in CPU_REGISTERS},
                semantics=dict(gpr='low32-visible; original high32 retained in raw64',
                    control_debug_and_descriptor_bases='full64; not legacy UC_MODE_32 API',
                    fp_order='physical R0..R7; logical ST(i)=R((TOP+i)&7)',
                    fip_fdp='full64 independent of current instruction mode',
                    dr45=dr_policy),
                retained_context=dict(gpr_upper32=[v >> 32 for v in gpr[:8]],
                    extended_gpr_r8_r15=gpr[8:], extended_xmm8_xmm15=xmm[8:],
                    segment_caches=dict(zip(SEG, segments)), efer=efer, hflags=hflags,
                    top=top, physical_empty_mask=empty))


def pack(raw, *, expected_cpu, expected_vcpus, expected_source_sha256):
    """Validate and wrap a record whose canonical-JSON digest is pinned outside.

    Authenticate the containing artifact/build/capture independently before
    computing that expected digest. Matching a caller-chosen hash alone proves
    neither authenticity nor actual hardware correctness.
    """
    view = _validate(raw, expected_cpu, expected_vcpus)
    if (type(expected_source_sha256) is not str or
            re.fullmatch('[0-9a-f]{64}', expected_source_sha256) is None or
            source_digest(raw) != expected_source_sha256):
        _fail('external source digest mismatch')
    return dict(schema=SCHEMA, source=dict(schema='tcg-state-v1', cpu=expected_cpu,
                    vcpus=expected_vcpus, canonical_json_sha256=expected_source_sha256),
                raw64=deepcopy(raw), view32=view, capture_lossless=True,
                legacy_unicorn32_load_format=False, unicorn32_replay_admitted=False,
                full_machine_state=False, windows_admitted=False)


def _same(actual, expected):
    if type(actual) is not type(expected):
        return False
    if type(expected) is dict:
        return (set(actual) == set(expected) and
                all(type(k) is str and _same(actual[k], expected[k]) for k in expected))
    if type(expected) is list:
        return len(actual) == len(expected) and all(_same(a, b) for a, b in zip(actual, expected))
    return actual == expected


def unpack(envelope, *, expected_cpu, expected_vcpus, expected_source_sha256):
    """Re-derive the view and qualifications; return a detached exact raw dict."""
    if type(envelope) is not dict or 'raw64' not in envelope:
        _fail('envelope with original raw64 required')
    rebuilt = pack(envelope['raw64'], expected_cpu=expected_cpu,
                   expected_vcpus=expected_vcpus, expected_source_sha256=expected_source_sha256)
    if not _same(envelope, rebuilt):
        _fail('envelope metadata/view/qualification changed or inconsistent')
    return deepcopy(rebuilt['raw64'])
