"""Independent constructor stores, source call stacks and live startup boundaries."""
import json
import struct

from tools.school_owner_startup import *
from tools.school_owner_startup_emulation import OWNER, STACK, TOP, RETURN, MANAGER
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_verification import verify_buffer
from tools.school_owner_platform import HELPER, COMPILER, sha, machine


@lru_cache(maxsize=1)
def code():
    raw = SOURCE.read_bytes()
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    return {a: list(md.disasm(raw[a-BASE:b-BASE], a)) for a, b in functions().items()}


def frame(va):
    if va == 0x56DDA0:
        return 48
    if va == 0x52AFE6:
        return 64
    total, filled = 0, False
    for ins in code()[va]:
        if filled and not (ins.mnemonic == 'pop' and ins.op_str == 'ecx'):
            return total
        if ins.mnemonic == 'push':
            total += 4
        elif ins.mnemonic == 'pop':
            total -= 4
        elif ins.op_str.startswith('esp, '):
            n = int(ins.op_str.split(', ')[1], 0)
            if ins.mnemonic == 'sub':
                total += n
            elif ins.mnemonic == 'add':
                total -= n
        elif ins.mnemonic.startswith('rep stos'):
            filled = True
    raise ValueError('owner unsupported source frame')


def verify_native(native, root, sp, ret, receiver, args):
    raw = SOURCE.read_bytes()
    entries = native['entries']
    if not entries or entries[0] != dict(va=hex(root), sp=sp, return_va=hex(ret), receiver=receiver, args=args):
        raise ValueError('owner actual root/continuation stack')
    active = [(root, sp)]
    ranges = functions()
    for row in entries[1:]:
        va, result = int(row['va'], 16), int(row['return_va'], 16)
        parent = next(a for a, b in ranges.items() if a <= result-5 < b)
        while active and active[-1][0] != parent:
            active.pop()
        if not active:
            raise ValueError('owner native call nesting')
        op = raw[result-BASE-5:result-BASE]
        if result == 0x56DDF1:
            if va != 0x41D2E0 or raw[result-BASE-3:result-BASE] != b'\xff\x55\x14':
                raise ValueError('owner original array callback')
        elif op[0] != 0xE8 or result+struct.unpack_from('<i', op, 1)[0] != va:
            raise ValueError('owner original E8 bytes')
        expected_sp = active[-1][1]-frame(parent)-4-4*ARGS.get(va, 0)
        if row['sp'] != expected_sp or len(row['args']) != ARGS.get(va, 0):
            raise ValueError('owner original stack ABI')
        active.append((va, row['sp']))
    allowed = {int(e['va'], 16) for e in entries} | {0x56CE80}
    valid = {i.address for a in allowed for i in code()[a]}
    if native['visited'] != sorted(set(native['visited'])) or any(v not in valid for v in native['visited']):
        raise ValueError('owner original visited bodies')
    for row in entries:
        if int(row['va'], 16) not in native['visited']:
            raise ValueError('owner original entry missing')
    for row in native['returns']:
        va, result = int(row['va'], 16), int(row['return_va'], 16)
        if va not in valid or va not in native['visited'] or not any(i.address == va and i.mnemonic == 'ret' for a in allowed for i in code()[a]):
            raise ValueError('owner original return instruction')
        if va == 0x56CE82:
            op = raw[result-BASE-5:result-BASE]
            if op[0] != 0xE8 or result+struct.unpack_from('<i', op, 1)[0] != 0x56CE80:
                raise ValueError('owner source stack-check return')
        elif va == 0x56DE2C:
            array = next(e for e in entries if e['va'] == '0x56dda0')
            if result != 0x56DE0F or row['sp'] != array['sp']-52:
                raise ValueError('owner original array finally return')
        elif not any(row['sp'] == e['sp'] and row['return_va'] == e['return_va'] for e in entries):
            raise ValueError('owner natural helper return stack')


def verify_maps(state, objects=()):
    raw = SOURCE.read_bytes()
    expected = {}
    def put(at, data):
        for offset, value in enumerate(data):
            a = at+offset
            expected.setdefault(a & ~4095, bytearray(4096))[a & 4095] = value
    for slot in (*IMPORTS, 0x59246C):
        put(dword(raw, slot-BASE), b'\xc3')
    for obj in objects:
        put(obj['pointer'], struct.pack('<I', obj['vtable']))
        for slot, address in obj['methods'].items():
            put(obj['vtable']+int(slot), struct.pack('<I', address))
            put(address, b'\xc3')
    rows = state['foreign_maps']
    if [r['pointer'] for r in rows] != sorted(expected):
        raise ValueError('owner exact foreign maps')
    for row in rows:
        verify_buffer({k: v for k, v in row.items() if k != 'pointer'}, expected[row['pointer']])


def verify_state(state, owner, image, seh, objects=()):
    verify_buffer(state['owner'], owner)
    if state['image_sha256'] != sha(image) or state['SEH'] != seh or state['stack_guards_unchanged'] is not True:
        raise ValueError('owner source image/SEH/stack guards')
    verify_maps(state, objects)


def verify_constructor(case):
    fill = case['fill']
    if fill not in (0xA5, 0xCC):
        raise ValueError('owner declared dirty input')
    row = case['constructor']
    native = row['native']
    verify_native(native, CTOR, TOP, RETURN, OWNER, [])
    expected = [0x412E30, 0x409900, 0x420990, 0x41EAD0, 0x417530, 0x420990,
                0x41EE30, 0x420990, 0x41EAD0, 0x40D7E0, 0x4107B0, 0x410C20,
                0x40BE70, 0x420990, 0x56CEC0, 0x40C1A0, 0x56CEC0, 0x40C140,
                0x41D0D0, 0x56DDA0, 0x41D2E0, 0x41E6B0, 0x41D2E0, 0x41E6B0,
                0x417C40, 0x417E00, *([0x56CEC0]*5), 0x41AB10, 0x56CEC0,
                0x56CEC0, 0x56CEC0, 0x40B590, 0x56CEC0, 0x415A90, 0x4170C0,
                0x414F90, 0x415370, 0x415530]
    if [int(e['va'], 16) for e in native['entries']] != expected:
        raise ValueError('owner complete constructor call sequence')
    memset = {0x40BEEB: (0x1AAC, 0x7080), 0x40C1CF: (0x8C2C, 80),
              0x417E81: (0x92B4, 48), 0x417EFC: (0x92EC, 208),
              0x417F15: (0x93BC, 0x150C), 0x417F2B: (0x9184, 256),
              0x417F41: (0x9284, 40), 0x41AB42: (0xA8F8, 0x880),
              0x412F7D: (0xB234, 52), 0x413008: (0xB214, 16)}
    for e in native['entries']:
        va, ret = int(e['va'], 16), int(e['return_va'], 16)
        if va == 0x56CEC0:
            pointer, count = (0x765728, 0x2C000) if ret == 0x40B5C7 else (OWNER+memset[ret][0], memset[ret][1])
            if e['args'] != [pointer, 0, count]:
                raise ValueError('owner complete source memset arguments')
        elif va == 0x56DDA0:
            if e['args'] != [OWNER+0x8C88, 632, 2, 0x41D2E0, 0x41D3C0]:
                raise ValueError('owner source array constructor inputs')
        elif va == 0x4170C0 and e['args'] != [1] or va == 0x414F90 and e['args'] != [0]:
            raise ValueError('owner source timer/mode inputs')
    api_rows = row['platform_calls']
    if [r['name'] for r in api_rows] != ['GetDC', 'QueryPerformanceCounter', 'QueryPerformanceFrequency']:
        raise ValueError('owner real platform calls')
    source = SOURCE.read_bytes()
    for r in api_rows:
        slot = int(r['slot'], 16)
        name, desc, ret, count = IMPORTS[slot]
        sp = TOP-(392 if name == 'QueryPerformanceCounter' else 112)
        args = [TOP-236] if name == 'QueryPerformanceCounter' else [OWNER+0xB188] if name == 'QueryPerformanceFrequency' else [0]
        if (r['va'] != hex(dword(source, slot-BASE)) or r['return_va'] != hex(ret)
                or r['sp'] != sp or r['args'] != args or r['request'] != {} or r['live_host_observed'] is not True):
            raise ValueError('owner actual original platform ABI')
        result = r['result']
        if name == 'GetDC':
            if not 0 < result['result'] <= 0xFFFFFFFF:
                raise ValueError('owner real32-bit screen DC')
        elif result['result'] != 1 or len(bytes.fromhex(result['hex'])) != 8:
            raise ValueError('owner complete real timer sample')
    api = {r['name']: r['result'] for r in api_rows}
    owner = project_constructor(bytes([fill])*0xC000, api)
    image = project_image(api)
    verify_state(row['state'], owner, image, 0)
    cpu = native['cpu']
    values = dict(EIP=RETURN, ESP=TOP+4, EBP=0x11223344, EAX=OWNER,
                  EBX=0x55667788, ESI=0x88776655, EDI=0x44332211)
    if any(cpu[k] != v for k, v in values.items()) or native['boundary'] != hex(RETURN):
        raise ValueError('owner original constructor CPU return')
    if native['platform_calls'] or native['live_results']:
        raise ValueError('owner constructor has no D3D calls')
    return owner, image


def verify_report(report):
    if report['source_contract'] != source_contract() or report['schema_version'] != 1:
        raise ValueError('owner startup source contract')
    for key in ('original_helpers_stubbed', 'retained_VM_advanced', 'drawing_or_Present',
                'full_outer_frame', 'live_handles_resumable_after_cleanup'):
        if report[key] is not False:
            raise ValueError('owner startup authority')
    if report['inherited_source_globals'] is not True:
        raise ValueError('owner inherited process globals required')
    build = report['platform_build']
    if (build['source_sha256'] != sha((ROOT/'tools/school_owner_platform.cs').read_bytes())
            or build['helper_sha256'] != sha(HELPER.read_bytes()) or build['machine'] != machine(HELPER)
            or build['compiler_sha256'] != sha(COMPILER.read_bytes())):
        raise ValueError('owner live platform build identity')
    if [c['fill'] for c in report['cases']] != [0xA5, 0xCC]:
        raise ValueError('owner two declared dirty cases')
    for c in report['cases']:
        verify_constructor(c)
        if c['platform_cleanup'] != dict(fonts_released=0, dcs_released=1, all_owned_resources_released=True):
            raise ValueError('owner constructor platform cleanup')
        if c['device_cleanup'] != dict(window_destroyed=True, all_owned_resources_released=True):
            raise ValueError('owner constructor hidden window cleanup')
        calls = c['constructor']['platform_calls']
        expected_trace = [dict(request=dict(id=i, op=r['name'], **r['request']),
                               reply=dict(ok=True, id=i, result=r['result'])) for i, r in enumerate(calls, 1)]
        expected_trace.append(dict(request=dict(id=4, op='close'), reply=dict(ok=True, id=4, result=c['platform_cleanup'])))
        if c['platform_trace'] != expected_trace:
            raise ValueError('owner actual sequenced platform trace')
    return dict(cases=2, full_owner_bytes=49152, source_calls_each=42, inherited_globals=True)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('report')
    a = p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf-8')))))
