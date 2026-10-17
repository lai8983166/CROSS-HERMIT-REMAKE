"""Independent full-owner, original ABI and live-platform startup evidence checks."""
import base64
import json
import os
import zlib
from pathlib import Path

from tools.school_device_init import *
from tools.school_device_init_emulation import OWNER, MANAGER, STACK, TOP, RETURN, EXTERNAL
from tools.school_device_init_bridge import COMPILER, machine, sha
from tools.school_renderer_init_verification import verify_buffer


def unpack(row):
    size = row['bytes']
    if not 0 <= size <= 65536:
        raise ValueError('bounded startup evidence buffer')
    dec = zlib.decompressobj()
    raw = dec.decompress(base64.b64decode(row['zlib_base64'], validate=True), size+1)
    if len(raw) != size or not dec.eof or dec.unused_data or dec.unconsumed_tail or sha(raw) != row['sha256']:
        raise ValueError('startup full buffer length/hash')
    return raw


def verify_native(native, root, args, receiver, pending=False):
    image = SOURCE.read_bytes()
    decoder = Cs(CS_ARCH_X86, CS_MODE_32)
    instructions = {a: list(decoder.disasm(image[a-BASE:b-BASE], a)) for a, b in FUNCTIONS.items()}
    valid = {i.address for seq in instructions.values() for i in seq}
    visited = native['visited']
    if visited != sorted(set(visited)) or any(a not in valid for a in visited):
        raise ValueError('startup native instruction boundary')
    if any(a in visited for a in (STOP, 0x40D970, 0x40DAB0)):
        raise ValueError('startup crossed font/owner/queue boundary')
    entries = native['entries']
    wanted = dict(va=hex(root), return_va=hex(RETURN), sp=TOP, receiver=receiver, args=args)
    if not entries or entries[0] != wanted:
        raise ValueError('startup declared root call')
    active = [(root, TOP)]
    for row in entries[1:]:
        va, ret = int(row['va'], 16), int(row['return_va'], 16)
        op = image[ret-BASE-5:ret-BASE]
        if len(op) != 5 or op[0] != 0xE8 or ret+struct.unpack_from('<i', op, 1)[0] != va:
            raise ValueError('startup original E8 caller')
        parent = next(a for a, b in FUNCTIONS.items() if a <= ret-5 < b)
        while active and active[-1][0] != parent:
            active.pop()
        if not active:
            raise ValueError('startup retained original call nesting')
        local = next(i for i in instructions[parent][:5] if i.mnemonic == 'sub' and i.op_str.startswith('esp, '))
        frame = 20+int(local.op_str.split(', ')[1], 0)
        expected_sp = active[-1][1]-frame-4*ARG_COUNTS.get(va, 0)
        if row['sp'] != expected_sp or len(row['args']) != ARG_COUNTS.get(va, 0) or va not in visited:
            raise ValueError('startup original stack ABI')
        active.append((va, row['sp']))
    for row in native['returns']:
        at, ret = int(row['va'], 16), int(row['return_va'], 16)
        ins = next((i for seq in instructions.values() for i in seq if i.address == at), None)
        if ins is None or ins.mnemonic != 'ret' or at not in visited:
            raise ValueError('startup original return instruction')
        if at == 0x56CE82:
            op = image[ret-BASE-5:ret-BASE]
            if op[0] != 0xE8 or ret+struct.unpack_from('<i', op, 1)[0] != 0x56CE80:
                raise ValueError('startup original stack-check return')
        else:
            call = next((c for c in entries if c['sp'] == row['sp'] and c['return_va'] == row['return_va']), None)
            if call is None:
                raise ValueError('startup original helper return stack')
            expected = call['args'][0] if int(call['va'], 16) == 0x56CEC0 else MANAGER if root == 0x40D7E0 else 0
            if row['eax'] != expected:
                raise ValueError('startup original helper return value')
    cpu = native['cpu']
    expected = dict(EIP=STOP if pending else RETURN, ESP=TOP-92 if pending else TOP+4,
                    EBP=TOP-4 if pending else 0x11223344, EBX=0x55667788,
                    ESI=0x88776655, EDI=TOP-4 if pending else 0x44332211)
    if any(cpu[k] != v for k, v in expected.items()) or native['boundary'] != hex(expected['EIP']):
        raise ValueError('startup final CPU boundary/ABI')
    if pending and (cpu['EAX'] != 0 or cpu['ECX'] != OWNER):
        raise ValueError('startup original font-call CPU')


def verify_case(case):
    hello = case['hello']
    width, height, window = hello['width'], hello['height'], hello['window']
    if hello != dict(pointer_bytes=4, window=window, window_visible=False, width=width, height=height) or not window:
        raise ValueError('startup live hidden window')
    declared = bytearray([0xA5])*0xC000
    declared[0xB20C:0xB214] = bytes(8)
    verify_buffer(case['declared_owner'], declared)
    initial = bytearray(declared)
    initial[0x1058:0x10B8] = constructor(initial[0x1058:0x10B8])
    verify_buffer(case['initial_owner'], initial)
    verify_native(case['constructor'], 0x40D7E0, [], MANAGER)
    if [r['va'] for r in case['constructor']['entries']] != ['0x40d7e0', '0x4107b0']:
        raise ValueError('startup constructor native call sequence')
    if case['constructor']['platform_calls'] or case['constructor']['live_results']:
        raise ValueError('startup constructor has no platform dependency')
    ctor_child = case['constructor']['entries'][1]
    if ctor_child['receiver'] != MANAGER or ctor_child['args']:
        raise ValueError('startup constructor native receiver')
    args = [window, 1, 1, width, height]
    if case['root_args'] != args:
        raise ValueError('startup original windowed root arguments')
    native = case['actual']
    verify_native(native, 0x413450, args, OWNER, pending=True)
    calls = native['live_results']
    ops = [r['op'] for r in calls]
    checks = [r for r in calls if r['op'] == 'check_format']
    if ops != ['factory', 'display_mode', 'create_device', 'caps', 'backbuffer',
               'describe_surface', 'release_surface']+['check_format']*len(checks)+['viewport']:
        raise ValueError('startup live API order (observed first-device-success path)')
    if len(calls) != len(native['platform_calls']) or len(case['bridge_trace']) != len(calls)+1:
        raise ValueError('startup complete live IPC trace')
    identities = {k: next(r['result'][k] for r in calls if k in r['result'])
                  for k in ('factory', 'device', 'surface')}
    factory, device, surface = (identities[k]['pointer'] for k in ('factory', 'device', 'surface'))
    # Every API response is tied to the actual sequenced IPC request and native caller.
    relative_sp = dict(factory=-184, display_mode=-396, create_device=-412, caps=-572,
                       backbuffer=-584, describe_surface=-576, release_surface=-572,
                       check_format=-596, viewport=-392)
    slots = dict(display_mode=('factory', 32), create_device=('factory', 60),
                 caps=('device', 28), backbuffer=('device', 64),
                 describe_surface=('surface', 32), release_surface=('surface', 8),
                 check_format=('factory', 40), viewport=('device', 160))
    mode = bytes.fromhex(calls[1]['result']['hex'])
    caps = bytes.fromhex(calls[3]['result']['hex'])
    desc = bytes.fromhex(calls[5]['result']['hex'])
    pp = bytes.fromhex(calls[2]['result']['presentation_hex'])
    if (len(mode), len(caps), len(desc), len(pp)) != (16, 212, 32, 52):
        raise ValueError('startup complete live ABI buffers')
    # This archive covers the observed first successful device attempt. The four
    # fallback pairs remain source-bound, without inventing failed host results.
    wanted_entries = [0x413450, 0x4136D0, 0x526C40, 0x413730, 0x413850, 0x4138A0,
                      0x56CEC0, 0x413FA0, 0x414010, 0x414090, 0x56CEC0, 0x414190, 0x56CEC0]
    if [int(e['va'], 16) for e in native['entries']] != wanted_entries:
        raise ValueError('startup complete original helper sequence')
    for e in native['entries'][1:]:
        va, ret = int(e['va'], 16), int(e['return_va'], 16)
        receiver, arguments = OWNER, []
        if va == 0x526C40:
            arguments = [220]
        elif va in (0x413730, 0x413850):
            arguments = [window, 1]
        elif va == 0x4138A0:
            arguments = [window]
        elif va == 0x56CEC0:
            at, count = {0x413994: (OWNER+0xB244, 4),
                         0x4140D6: (OWNER+0xB3E8, 32),
                         0x413A56: (OWNER+0xBA08, 24)}[ret]
            receiver = OWNER if ret == 0x413994 else at
            arguments = [at, 0, count]
        if e['receiver'] != receiver or e['args'] != arguments:
            raise ValueError('startup original helper receiver/arguments')
    expected_requests = {
        'factory': dict(sdk=220), 'display_mode': dict(pointer=factory),
        'create_device': dict(pointer=factory, type=1, flags=68,
                              presentation_hex=presentation(width, height, dword(mode, 12), window).hex()),
        'caps': dict(pointer=device), 'backbuffer': dict(pointer=device),
        'describe_surface': dict(pointer=surface), 'release_surface': dict(pointer=surface),
        'viewport': dict(pointer=device, hex=struct.pack('<6I', 0, 0, width, height, 0, 0x3F800000).hex()),
    }
    expected_args = dict(factory=[220], display_mode=[factory, 0, OWNER+0xB214],
                         create_device=[factory, 0, 1, window, 68, OWNER+0xB234, OWNER+0xB210],
                         caps=[device, OWNER+0xB314], backbuffer=[device, 0, 0, TOP-488],
                         describe_surface=[surface, OWNER+0xB3E8], release_surface=[surface],
                         viewport=[device, OWNER+0xBA08])
    for index, (row, external, trace) in enumerate(zip(calls, native['platform_calls'], case['bridge_trace']), 1):
        op, response = row['op'], row['result']
        request = expected_requests.get(op)
        arguments = expected_args.get(op)
        if op == 'check_format':
            fmt = row['request']['format']
            request = dict(pointer=factory, adapter=dword(caps, 4), type=dword(caps, 0),
                           adapter_format=dword(desc, 0), format=fmt)
            arguments = [factory, request['adapter'], request['type'], request['adapter_format'], 1, 1, fmt]
        if row['request'] != request or trace != dict(request=dict(id=index, op=op, **request), reply=dict(ok=True, id=index, result=response)):
            raise ValueError('startup live request/response trace')
        ret = next(r for r, (name, n) in EXTERNAL.items() if name == op)
        if op == 'factory':
            address, result = dword(SOURCE.read_bytes(), SLOT-BASE), factory
        else:
            kind, slot = slots[op]
            address = identities[kind]['methods'][str(slot)]
            result = response['count'] if op == 'release_surface' else u32(response['hr'])
        expected = dict(op=op, va=hex(address), return_va=hex(ret), sp=TOP+relative_sp[op],
                        args=arguments, result=result, live_host_observed=True)
        if external != expected:
            raise ValueError('startup original external caller/ABI/live result')
        if op not in ('factory', 'check_format', 'release_surface') and i32(result) < 0:
            raise ValueError('startup successful observed host call')
    runtime = calls[0]['result']
    path = Path(os.environ['WINDIR'])/'SysWOW64/d3d8.dll'
    if (Path(runtime['runtime_path']).resolve() != path.resolve()
            or machine(path) != 0x14C or sha(path.read_bytes()) != runtime['runtime_sha256']):
        raise ValueError('startup actual32-bit runtime provenance')
    expected_owner = project_owner(bytes(initial), width, height, window, calls)
    verify_buffer(case['after_owner'], expected_owner)
    # Independently reconstruct every copied interface cell and unexecuted trap page.
    maps = {}
    def put(at, raw):
        for offset, value in enumerate(raw):
            address = at+offset
            maps.setdefault(address & ~4095, bytearray(4096))[address & 4095] = value
    target = dword(SOURCE.read_bytes(), SLOT-BASE)
    put(target, b'\xC3')
    for obj in identities.values():
        put(obj['pointer'], struct.pack('<I', obj['vtable']))
        for slot, pointer in obj['methods'].items():
            put(obj['vtable']+int(slot), struct.pack('<I', pointer))
            put(pointer, b'\xC3')
    if [r['pointer'] for r in case['foreign_maps']] != sorted(maps):
        raise ValueError('startup exact foreign map set')
    for row in case['foreign_maps']:
        verify_buffer({k: v for k, v in row.items() if k != 'pointer'}, maps[row['pointer']])
    if (case['source_image_sha256'] != SOURCE_SHA256 or case['original_IAT_target'] != target
            or case['original_IAT_unchanged'] is not True or case['stack_guards_unchanged'] is not True):
        raise ValueError('startup retained image/IAT/stack')
    if case['pending_font'] != dict(va=hex(STOP), return_va='0x4134e3', sp=TOP-92,
                                    receiver=OWNER, args=[], first_instruction_executed=False):
        raise ValueError('startup original pending font stack')
    for key in ('retained_VM_advanced', 'owner_bound', 'queues_initialized',
                'drawing_or_Present', 'live_pointers_resumable_after_cleanup'):
        if case[key] is not False:
            raise ValueError('startup authority boundary')
    cleanup = case['cleanup']
    if cleanup != dict(device_release_count=0, factory_release_count=0,
                       window_destroyed=True, all_owned_resources_released=True):
        raise ValueError('startup complete live cleanup')
    close = case['bridge_trace'][-1]
    seq = len(calls)+1
    if close != dict(request=dict(id=seq, op='close'), reply=dict(ok=True, id=seq, result=cleanup)):
        raise ValueError('startup sequenced close response')
    return dict(dimensions=[width, height], selected_format=dword(expected_owner, 0xB268),
                live_calls=len(calls), full_owner_bytes=len(expected_owner), font_executed=False)


def verify_report(report):
    if report['source_contract'] != source_contract() or report['schema_version'] != 1:
        raise ValueError('startup source contract')
    for key in ('original_helpers_stubbed', 'retained_VM_advanced', 'drawing_or_Present', 'full_outer_frame'):
        if report[key] is not False:
            raise ValueError('startup report authority boundary')
    if report['live_device_initialization_executed'] is not True:
        raise ValueError('startup actual platform required')
    build = report['bridge_build']
    if (build['source_sha256'] != sha((ROOT/'tools/school_device_init_bridge.cs').read_bytes())
            or build['compiler_sha256'] != sha(COMPILER.read_bytes())
            or build['helper_sha256'] != sha((ROOT/'.venv-audit/school-device-init-bridge.exe').read_bytes())
            or build['machine'] != 0x14C):
        raise ValueError('startup fixed bridge build provenance')
    if len(report['cases']) != 2 or [(c['hello']['width'], c['hello']['height']) for c in report['cases']] != [(640, 480), (1024, 768)]:
        raise ValueError('startup two declared cases')
    return [verify_case(c) for c in report['cases']]


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('report')
    a = p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf-8')))))
