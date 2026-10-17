"""Independent constructor stores, source call stacks and live startup boundaries."""
import json
import os
import struct

from tools.school_owner_startup import *
from tools.school_owner_startup_emulation import OWNER, STACK, TOP, RETURN, MANAGER
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_verification import verify_buffer
from tools.school_owner_platform import HELPER, COMPILER, sha, machine
from tools.school_device_init import project_owner, presentation, FORMATS
from tools.school_device_init_emulation import EXTERNAL


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


def verify_device(case, owner, image):
    row = case['device']
    native = row['native']
    h = case['hello']
    w, height, window = h['width'], h['height'], h['window']
    args = [window, 1, 1, w, height]
    verify_native(native, 0x413450, TOP, RETURN, OWNER, args)
    calls = native['live_results']
    checks = [r for r in calls if r['op'] == 'check_format']
    expected_ops = ['factory', 'display_mode', 'create_device', 'caps', 'backbuffer',
                    'describe_surface', 'release_surface']+['check_format']*len(checks)+['viewport']
    if [r['op'] for r in calls] != expected_ops or len(calls) != len(native['platform_calls']):
        raise ValueError('owner device live operation sequence')
    expected_entries = [0x413450, 0x4136D0, 0x526C40, 0x413730, 0x413850, 0x4138A0,
                        0x56CEC0, 0x413FA0, 0x414010, 0x414090, 0x56CEC0, 0x414190, 0x56CEC0]
    if [int(r['va'], 16) for r in native['entries']] != expected_entries:
        raise ValueError('owner complete device helpers')
    objects = {name: next(r['result'][name] for r in calls if name in r['result'])
               for name in ('factory', 'device', 'surface')}
    f, d, s = (objects[k]['pointer'] for k in ('factory', 'device', 'surface'))
    mode = bytes.fromhex(calls[1]['result']['hex'])
    caps = bytes.fromhex(calls[3]['result']['hex'])
    desc = bytes.fromhex(calls[5]['result']['hex'])
    if (len(mode), len(caps), len(desc), len(bytes.fromhex(calls[2]['result']['presentation_hex']))) != (16, 212, 32, 52):
        raise ValueError('owner complete device platform buffers')
    runtime = calls[0]['result']
    path = ROOT.__class__(os.environ['WINDIR'])/'SysWOW64/d3d8.dll'
    if (ROOT.__class__(runtime['runtime_path']).resolve() != path.resolve()
            or machine(path) != 0x14C or sha(path.read_bytes()) != runtime['runtime_sha256']):
        raise ValueError('owner actual32-bit device runtime')
    native_args = dict(factory=[220], display_mode=[f, 0, OWNER+0xB214],
                       create_device=[f, 0, 1, window, 68, OWNER+0xB234, OWNER+0xB210],
                       caps=[d, OWNER+0xB314], backbuffer=[d, 0, 0, TOP-488],
                       describe_surface=[s, OWNER+0xB3E8], release_surface=[s],
                       viewport=[d, OWNER+0xBA08])
    requests = dict(factory=dict(sdk=220), display_mode=dict(pointer=f),
                    create_device=dict(pointer=f, type=1, flags=68,
                                       presentation_hex=presentation(w, height, dword(mode, 12), window).hex()),
                    caps=dict(pointer=d), backbuffer=dict(pointer=d), describe_surface=dict(pointer=s),
                    release_surface=dict(pointer=s), viewport=dict(pointer=d,
                       hex=struct.pack('<6I', 0, 0, w, height, 0, 0x3F800000).hex()))
    relative = dict(factory=184, display_mode=396, create_device=412, caps=572,
                    backbuffer=584, describe_surface=576, release_surface=572, check_format=596, viewport=392)
    slots = dict(display_mode=('factory', 32), create_device=('factory', 60), caps=('device', 28),
                 backbuffer=('device', 64), describe_surface=('surface', 32), release_surface=('surface', 8),
                 check_format=('factory', 40), viewport=('device', 160))
    for r, actual in zip(calls, native['platform_calls']):
        name, result = r['op'], r['result']
        if name == 'check_format':
            candidate = r['request']['format']
            request = dict(pointer=f, adapter=dword(caps, 4), type=dword(caps, 0), adapter_format=dword(desc, 0), format=candidate)
            args = [f, request['adapter'], request['type'], request['adapter_format'], 1, 1, candidate]
        else:
            request, args = requests[name], native_args[name]
        ret = next(ret for ret, (op, _) in EXTERNAL.items() if op == name)
        if name == 'factory':
            target, eax = dword(SOURCE.read_bytes(), 0x59246C-BASE), f
        else:
            kind, slot = slots[name]
            target = objects[kind]['methods'][str(slot)]
            eax = result['count'] if name == 'release_surface' else u32(result['hr'])
        if r['request'] != request or actual != dict(op=name, va=hex(target), return_va=hex(ret),
                sp=TOP-relative[name], args=args, result=eax, live_host_observed=True):
            raise ValueError('owner original device interface ABI/live response')
        if name not in ('factory', 'check_format', 'release_surface') and result['hr'] < 0:
            raise ValueError('owner device actual success required')
    expected = project_owner(owner, w, height, window, calls)
    verify_state(row['state'], expected, image, 0, objects.values())
    cpu = native['cpu']
    if native['boundary'] != '0x415f50' or any(cpu[k] != value for k, value in
            dict(EIP=0x415F50, ESP=TOP-92, EBP=TOP-4, EAX=0, ECX=OWNER,
                 EBX=0x55667788, ESI=0x88776655, EDI=TOP-4).items()):
        raise ValueError('owner original device font-entry CPU')
    if row['pending'] != dict(va='0x415f50', return_va='0x4134e3', sp=TOP-92,
                              receiver=OWNER, args=[], first_instruction_executed=False):
        raise ValueError('owner source font admission stack')
    for c in native['returns']:
        if c['va'] not in ('0x56ce82', '0x56cf12') and c['eax'] != 0:
            raise ValueError('owner native device helper return')
    return expected, objects


def verify_font(case, owner, image, objects):
    row = case['font']
    native = row['native']
    if row['before_cpu'] != case['device']['native']['cpu']:
        raise ValueError('owner font must resume the actual pending CPU')
    verify_native(native, 0x415F50, TOP-92, 0x4134E3, OWNER, [])
    calls = row['platform_calls']
    if [r['name'] for r in calls] != ['CreateFontA', 'GetObjectA']:
        raise ValueError('owner first font actual platform sequence')
    handle = calls[0]['result']['result']
    if not 0 < handle <= 0xFFFFFFFF:
        raise ValueError('owner actual32-bit owned HFONT')
    device = objects['device']['pointer']
    expected_entries = [
        (0x415F50, 0x4134E3, 92, OWNER, []),
        (0x416140, 0x415FA0, 212, OWNER, []),
        (0x416320, 0x41616F, 320, OWNER, [0]),
        (0x4162C0, 0x416002, 216, OWNER, [handle]),
        (0x52AFE6, 0x4162F4, 324, handle, [device, handle, TOP-228])]
    if native['entries'] != [dict(va=hex(va), return_va=hex(ret), sp=TOP-depth,
                                  receiver=receiver, args=args)
                              for va, ret, depth, receiver, args in expected_entries]:
        raise ValueError('owner font original null cleanup and nested source stack')
    expected_returns = [(0x56CE82, 0x416367, 328, 0), (0x41636A, 0x41616F, 320, 0),
                        (0x56CE82, 0x416251, 220, 0), (0x416254, 0x415FA0, 212, 0),
                        (0x56CE82, 0x415FD1, 212, handle)]
    if native['returns'] != [dict(va=hex(va), return_va=hex(ret), sp=TOP-depth, eax=eax)
                              for va, ret, depth, eax in expected_returns]:
        raise ValueError('owner font exact original completed helper returns')
    face = bytes.fromhex(source_contract()['face_hex'])+b'\0'
    logfont = struct.pack('<5i8B', *FONT_ARGS[:-1])+face+b'\xcc'*(32-len(face))
    expected_calls = [
        (0x5920A0, 268, FONT_ARGS, dict(args=FONT_ARGS[:-1], face_hex=face[:-1].hex()),
         dict(result=handle)),
        (0x592068, 404, [handle, 60, TOP-388], dict(pointer=handle, before_hex='cc'*60),
         dict(result=60, hex=logfont.hex()))]
    raw = SOURCE.read_bytes()
    for actual, (slot, depth, args, request, result) in zip(calls, expected_calls):
        name, _, ret, _ = IMPORTS[slot]
        if actual != dict(name=name, slot=hex(slot), va=hex(dword(raw, slot-BASE)),
                          return_va=hex(ret), sp=TOP-depth, args=args, request=request,
                          result=result, live_host_observed=True):
            raise ValueError('owner original font API ABI and complete live LOGFONT')
    if row['LOGFONT'] != logfont.hex():
        raise ValueError('owner full60-byte LOGFONT including untouched face tail')
    expected = bytearray(owner)
    store(expected, 0xB26C, handle)
    verify_state(row['state'], bytes(expected), image, TOP-108, objects.values())
    expected_cpu = dict(EIP=FONT_STOP, ESP=TOP-404, EBP=TOP-328, EAX=TOP-388,
                        EBX=0x55667788, ECX=handle, EDX=OWNER, ESI=TOP-208,
                        EDI=TOP-220, EFLAGS=6)
    if native['cpu'] != expected_cpu or native['boundary'] != hex(FONT_STOP):
        raise ValueError('owner original static font admission CPU')
    if row['pending'] != dict(va=hex(FONT_STOP), return_va='0x52b015', sp=TOP-404,
                              args=[device, TOP-388, TOP-228], first_instruction_executed=False):
        raise ValueError('owner unexecuted static font body source stack')
    if native['platform_calls'] or native['live_results'] or FONT_STOP in native['visited']:
        raise ValueError('owner no static font body or new D3D execution')
    if any(row[k] is not False for k in ('font_object_constructed', 'owner_bound', 'queues_initialized')):
        raise ValueError('owner font prefix authority')


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
    device_build = report['device_build']
    if (device_build['source_sha256'] != sha((ROOT/'tools/school_device_init_bridge.cs').read_bytes())
            or device_build['helper_sha256'] != sha((ROOT/'.venv-audit/school-device-init-bridge.exe').read_bytes())
            or device_build['compiler_sha256'] != sha(COMPILER.read_bytes()) or device_build['machine'] != 0x14C):
        raise ValueError('owner immutable device helper provenance')
    if [(c['fill'], c['hello']['width'], c['hello']['height']) for c in report['cases']] != [(0xA5, 640, 480), (0xCC, 1024, 768)]:
        raise ValueError('owner two declared dirty cases')
    phase = report['phase']
    if phase not in ('constructor', 'device', 'font'):
        raise ValueError('owner known audit phase')
    for c in report['cases']:
        if c['hello']['pointer_bytes'] != 4 or c['hello']['window_visible'] is not False or c['platform_hello']['pointer_bytes'] != 4:
            raise ValueError('owner actual hidden window/platform ABI')
        owner, image = verify_constructor(c)
        device_calls = []
        if phase != 'constructor':
            owner, objects = verify_device(c, owner, image)
            device_calls = c['device']['native']['live_results']
        if phase == 'font':
            verify_font(c, owner, image, objects)
        if c['platform_cleanup'] != dict(fonts_released=int(phase == 'font'), dcs_released=1, all_owned_resources_released=True):
            raise ValueError('owner constructor platform cleanup')
        expected_cleanup = dict(window_destroyed=True, all_owned_resources_released=True)
        if phase != 'constructor':
            expected_cleanup.update(device_release_count=0, factory_release_count=0)
        if c['device_cleanup'] != expected_cleanup:
            raise ValueError('owner constructor hidden window cleanup')
        calls = c['constructor']['platform_calls'] + (c['font']['platform_calls'] if phase == 'font' else [])
        expected_trace = [dict(request=dict(id=i, op=r['name'], **r['request']),
                               reply=dict(ok=True, id=i, result=r['result'])) for i, r in enumerate(calls, 1)]
        sequence = len(calls)+1
        expected_trace.append(dict(request=dict(id=sequence, op='close'), reply=dict(ok=True, id=sequence, result=c['platform_cleanup'])))
        if c['platform_trace'] != expected_trace:
            raise ValueError('owner actual sequenced platform trace')
        device_trace = [dict(request=dict(id=i, op=r['op'], **r['request']),
                             reply=dict(ok=True, id=i, result=r['result'])) for i, r in enumerate(device_calls, 1)]
        sequence = len(device_calls)+1
        device_trace.append(dict(request=dict(id=sequence, op='close'),
                                 reply=dict(ok=True, id=sequence, result=c['device_cleanup'])))
        if c['device_trace'] != device_trace:
            raise ValueError('owner device complete live trace')
    return dict(cases=2, full_owner_bytes=49152, source_calls_each=42, inherited_globals=True)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('report')
    a = p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf-8')))))
