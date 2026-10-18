"""Independent original texture calls/returns, actual interfaces and full-state checks."""
import json
import os
import struct
from functools import lru_cache
from pathlib import Path
import pefile
from tools.school_font_texture import *
from tools.school_font_texture_emulation import OWNER, STACK, TOP, RETURN, NATIVE
from tools.school_font_texture_bridge import SOURCE as BRIDGE_SOURCE, HELPER, COMPILER, sha, machine
from tools.school_owner_platform import SOURCE as PLATFORM_SOURCE, HELPER as PLATFORM_HELPER
from tools.school_owner_startup import IMPORTS
from tools.school_owner_startup_verification import verify_constructor, verify_device, verify_font
from tools.school_font_startup_verification import verify_factory, verify_trace
from tools.school_font_startup import font_constructor, cache_prefix
from tools.school_renderer_init_verification import verify_buffer


@lru_cache(maxsize=1)
def bodies():
    raw, md = SOURCE.read_bytes(), Cs(CS_ARCH_X86, CS_MODE_32)
    return {a: list(md.disasm(raw[a-BASE:b-BASE], a)) for a, b in NATIVE.items()}


def maps(state, objects):
    expected = {}
    def put(address, data):
        for offset, value in enumerate(data):
            at = address+offset
            expected.setdefault(at & ~4095, bytearray(4096))[at & 4095] = value
    raw = SOURCE.read_bytes()
    for slot in (*IMPORTS, 0x59246C):
        put(dword(raw, slot-BASE), b'\xc3')
    put(DEBUG_TARGET, b'\xc3')
    for obj in objects.values():
        if not obj['pointer'] or not obj['vtable']:
            raise ValueError('texture actual interface identity')
        put(obj['pointer'], struct.pack('<I', obj['vtable']))
        for slot, target in obj['methods'].items():
            put(obj['vtable']+int(slot), struct.pack('<I', target))
            put(target, b'\xc3')
    if [r['pointer'] for r in state['foreign_maps']] != sorted(expected):
        raise ValueError('texture exact external interface/debug maps')
    for row in state['foreign_maps']:
        verify_buffer({k: v for k, v in row.items() if k != 'pointer'}, expected[row['pointer']])


def verify_stage(case, phase, owner, image, objects):
    row = case[phase]
    before = case['factory']['cpu'] if phase == 'requirements' else case['requirements']['cpu']
    if row['phase'] != phase or row['before_cpu'] != before:
        raise ValueError('texture same pending CPU continuation required')
    device, factory = objects['device']['pointer'], objects['factory']['pointer']
    table_end, format_row, fvtable = 0x5D09D4, 0x5D03EC, objects['factory']['vtable']
    nested = phase == 'texture'
    delta = 48 if nested else 0
    entries = []
    if nested:
        entries.append((0x5275D7, 0x5486D7, 780, 21, 1, [device, 64, 16, 1, 512, 21, 0, CACHE+16]))
    entries += [(0x52755E, 0x527614 if nested else 0x5486A9, 824 if nested else 776,
                 21 if nested else 0, 1 if nested else TOP-488,
                 [device, TOP-772, TOP-768, TOP-764, 512, TOP-756, 0] if nested
                 else [device, CACHE+88, CACHE+92, 0, 512, CACHE+84, 0]),
                (0x527234, 0x52757F, 816+delta, 21 if nested else 0, 512,
                 [device, TOP-772, TOP-768, 0, TOP-764, TOP-756, 0, 3] if nested
                 else [device, CACHE+88, CACHE+92, 0, 0, CACHE+84, 0, 3]),
                (0x526C46, 0x52729E, 1060+delta, 21, 512, [21]),
                (0x526D4D, 0x5272A9, 1076+delta, table_end, 21, [device, 512, 3, format_row, 21]),
                (0x52B019, 0x526D64, 1332+delta, table_end, 21, [1]),
                (0x52B019, 0x526E27, 1332+delta, fvtable, fvtable, [0])]
    expected = [dict(va=hex(va), return_va=hex(ret), sp=TOP-depth, receiver=ecx, edx=edx, args=args)
                for va, ret, depth, ecx, edx, args in entries]
    if row['entries'] != expected:
        raise ValueError('texture exact source calls, registers and stack arguments')
    raw, md = SOURCE.read_bytes(), Cs(CS_ARCH_X86, CS_MODE_32)
    for va, ret, *_ in entries:
        ins = next(md.disasm(raw[ret-BASE-5:ret-BASE], ret-5))
        if ins.mnemonic != 'call' or int(ins.op_str, 16) != va:
            raise ValueError('texture original direct-call bytes')
    returns = [(0x526C69, 0x52729E, 1060+delta, format_row),
               (0x52B0A8, 0x526D64, 1332+delta, format_row),
               (0x52B0A8, 0x526E27, 1332+delta, 2),
               (0x526E2E, 0x5272A9, 1076+delta, 21),
               (0x52755D, 0x52757F, 816+delta, 0),
               (0x527583, 0x527614 if nested else 0x5486A9, 824 if nested else 776, 0)]
    if nested:
        returns += [(0x52763A, 0x5486D7, 780, 0), (0x548705, 0x5487A5, 708, 0)]
    if row['returns'] != [dict(va=hex(va), return_va=hex(ret), sp=TOP-depth, eax=eax) for va, ret, depth, eax in returns]:
        raise ValueError('texture exact natural original returns')
    valid = {i.address for body in bodies().values() for i in body}
    visited = set(row['visited'])
    if (row['visited'] != sorted(visited) or not {r[0] for r in entries} <= visited
            or any(at not in valid for at in visited) or STOPS[phase] in visited):
        raise ValueError('texture original bodies and unexecuted stop')
    for va, *_ in returns:
        if va not in visited or not any(i.address == va and i.mnemonic == 'ret' for body in bodies().values() for i in body):
            raise ValueError('texture original return instruction')
    api = row['api_calls']
    expected_ops = ['debug_mute', 'texture_factory', 'texture_caps', 'texture_mode',
                    'texture_format', 'texture_format', 'texture_factory_release', 'debug_mute', 'texture_caps']
    if nested:
        expected_ops += ['texture_create', 'texture_surface']
    if [r['op'] for r in api] != expected_ops:
        raise ValueError('texture actual platform sequence and source format candidates')
    parent_caps = case['factory']['cache_calls'][1]['result']['hex']
    caps = bytes.fromhex(parent_caps)
    parent_mode = next(r['result']['hex'] for r in case['device']['native']['live_results'] if r['op'] == 'display_mode')
    runtime = pefile.PE(str(Path(os.environ['WINDIR'])/'SysWOW64/d3d8.dll'))
    debug_rva = next(s.address for s in runtime.DIRECTORY_ENTRY_EXPORT.symbols if s.name == b'DebugSetMute')
    specifications = [
        (DEBUG_TARGET, 0x52B098, 1340+delta, [1], dict(value=1)),
        (objects['device']['methods']['24'], 0x526D76, 1336+delta, [device, TOP-1084-delta], dict(pointer=device)),
        (objects['device']['methods']['28'], 0x526D83, 1336+delta, [device, TOP-1312-delta], dict(pointer=device)),
        (objects['device']['methods']['32'], 0x526D8D, 1336+delta, [device, TOP-1100-delta], dict(pointer=device))]
    for candidate in (20, 21):
        args = [factory, 0, 1, dword(bytes.fromhex(parent_mode), 12), 512, 3, candidate]
        specifications.append((objects['factory']['methods']['40'], 0x526DCF, 1356+delta, args,
                               dict(pointer=factory, adapter=0, type=1, adapter_format=args[3], usage=512, resource_type=3, format=candidate)))
    specifications += [(objects['factory']['methods']['8'], 0x526E1C, 1332+delta, [factory], dict(pointer=factory)),
                       (DEBUG_TARGET, 0x52B098, 1340+delta, [0], dict(value=0)),
                       (objects['device']['methods']['28'], 0x52736D, 1064+delta, [device, TOP-1040-delta], dict(pointer=device))]
    if nested:
        texture_result, surface_result = api[9]['result'], api[10]['result']
        if texture_result['hr'] != 0 or surface_result['hr'] != 0:
            raise ValueError('texture real creation and surface success required')
        objects = dict(objects, texture=texture_result['texture'], texture_surface=surface_result['surface'])
        if set(objects['texture']['methods']) != {'8', '60'} or set(objects['texture_surface']['methods']) != {'8', '32'}:
            raise ValueError('texture actual bounded resource method identities')
        specifications += [(objects['device']['methods']['80'], 0x527631, 828,
                             [device, 64, 16, 1, 512, 21, 0, CACHE+16],
                             dict(pointer=device, width=64, height=16, levels=1, usage=512, format=21, pool=0)),
                            (objects['texture']['methods']['60'], 0x5486EC, 760,
                             [objects['texture']['pointer'], 0, CACHE+48], dict(pointer=objects['texture']['pointer'], level=0))]
        inspection = dict(native_requested=False, method='GetDesc', result=dict(hr=0, hex=struct.pack('<8I', 21, 1, 512, 0, 4096, 0, 64, 16).hex()))
        if surface_result['inspection'] != inspection:
            raise ValueError('texture inspection-only complete actual surface description')
    for index, (actual, (target, ret, depth, args, request)) in enumerate(zip(api, specifications)):
        result = actual['result']
        if actual != dict(op=expected_ops[index], va=hex(target), return_va=hex(ret), sp=TOP-depth,
                          args=args, request=request, result=result, live_host_observed=True):
            raise ValueError('texture exact original platform ABI and request')
        op = actual['op']
        if op == 'debug_mute':
            if (result.get('return_value_defined') is not False or result['export_pointer']-result['module_pointer'] != debug_rva
                    or result != dict(module_pointer=result['module_pointer'], export_pointer=result['export_pointer'], return_value_defined=False)):
                raise ValueError('texture actual current runtime debug export with undefined return')
        elif op == 'texture_caps':
            if result != dict(hr=0, hex=parent_caps):
                raise ValueError('texture complete actual caps retained')
        elif op == 'texture_mode':
            if result != dict(hr=0, hex=parent_mode):
                raise ValueError('texture actual full device display mode')
        elif op == 'texture_factory':
            if result != dict(hr=0, factory=objects['factory']):
                raise ValueError('texture borrowed original factory identity')
        elif op == 'texture_factory_release':
            if result != dict(count=2):
                raise ValueError('texture actual borrowed factory reference release')
        elif op == 'texture_format':
            if result != dict(hr=-2005530518 if request['format'] == 20 else 0):
                raise ValueError('texture actual rejected20 and selected21 format path')
    projection = requirements(64, 16, 1 if nested else 0, caps)
    if projection != dict(width=64, height=16, levels=1 if nested else 7, format=21):
        raise ValueError('texture independent original dimension/mipmap projection')
    verify_buffer(row['state']['owner'], owner)
    if row['state']['image_sha256'] != sha(image) or row['state']['SEH'] != TOP-108 or row['state']['stack_guards_unchanged'] is not True:
        raise ValueError('texture complete image/SEH/stack retention')
    maps(row['state'], objects)
    if len(row['heaps']) != 2:
        raise ValueError('texture full font/cache guards required')
    for observed, ptr, size in zip(row['heaps'], (FONT, CACHE), (80, 176)):
        value = font_constructor(b'\xcd'*80) if ptr == FONT else cache_prefix(b'\xcd'*176, device, caps)
        if nested and ptr == CACHE:
            value = texture_cache(value, objects['texture']['pointer'], objects['texture_surface']['pointer'])
        expected_heap = bytearray(b'\xa5'*12288)
        expected_heap[4096:4096+size] = value
        if observed['pointer'] != ptr-4096:
            raise ValueError('texture heap mapping identity')
        verify_buffer({k: v for k, v in observed.items() if k != 'pointer'}, expected_heap)
    if nested:
        cpu = dict(EIP=0x52AE80, ESP=TOP-716, EBP=TOP-472, EAX=CACHE+12, EBX=TOP-228,
                   ECX=CACHE+48, EDX=objects['texture']['vtable'], ESI=CACHE, EDI=device, EFLAGS=70)
        pending = dict(va='0x52ae80', return_va='0x5487b9', sp=TOP-716, args=[device, CACHE+12], first_instruction_executed=False)
    else:
        cpu = dict(EIP=0x5275D7, ESP=TOP-780, EBP=TOP-712, EAX=CACHE+16, EBX=CACHE+92,
                   ECX=21, EDX=1, ESI=CACHE, EDI=CACHE+84, EFLAGS=2)
        pending = dict(va='0x5275d7', return_va='0x5486d7', sp=TOP-780,
                       args=[device, 64, 16, 1, 512, 21, 0, CACHE+16], first_instruction_executed=False)
    if row['cpu'] != cpu or row['pending'] != pending or row['output_slot'] != dict(pointer=TOP-228, value=0xCCCCCCCC):
        raise ValueError('texture exact original pending CPU/stack/output')
    if any(row[k] is not False for k in ('font_initialization_complete', 'sprite_body_executed', 'retained_VM_advanced')):
        raise ValueError('texture startup scope authority')
    return objects


def verify_report(report):
    phase = report['phase']
    if report['schema_version'] != 1 or phase not in STOPS or report['source_contract'] != source_contract():
        raise ValueError('texture original source contract')
    for key in ('original_IAT_changed', 'game_helpers_stubbed', 'retained_VM_advanced', 'drawing_or_Present',
                'full_outer_frame', 'live_handles_resumable_after_cleanup'):
        if report[key] is not False:
            raise ValueError('texture report authority')
    if report['explicit_empty_cache_experiment'] is not True or report['CRT_adapter_executed'] is not True:
        raise ValueError('texture explicit experiment declarations')
    for build, source, helper in ((report['device_build'], BRIDGE_SOURCE, HELPER), (report['platform_build'], PLATFORM_SOURCE, PLATFORM_HELPER)):
        if build != dict(source_sha256=sha(source.read_bytes()), helper_sha256=sha(helper.read_bytes()),
                         compiler_sha256=sha(COMPILER.read_bytes()), machine=machine(helper)) or machine(helper) != 0x14C:
            raise ValueError('texture real x86 platform provenance')
    if [(c['fill'], c['hello']['width'], c['hello']['height']) for c in report['cases']] != [(0xA5, 640, 480), (0xCC, 1024, 768)]:
        raise ValueError('texture two declared original dirty cases')
    for case in report['cases']:
        if case['hello']['pointer_bytes'] != 4 or case['hello']['window_visible'] is not False or case['platform_hello']['pointer_bytes'] != 4:
            raise ValueError('texture actual hidden x86 platform')
        owner, image = verify_constructor(case)
        owner, objects = verify_device(case, owner, image)
        verify_font(case, owner, image, objects)
        owner = bytearray(owner)
        store(owner, 0xB26C, case['font']['platform_calls'][0]['result']['result'])
        verify_factory(case, 'empty', bytes(owner), image, objects)
        image = bytearray(image)
        store(image, COUNTER-BASE, dword(image, COUNTER-BASE)+256)
        store(image, HEAD-BASE, CACHE)
        objects = verify_stage(case, 'requirements', bytes(owner), bytes(image), objects)
        if phase == 'texture':
            objects = verify_stage(case, 'texture', bytes(owner), bytes(image), objects)
        cleanup = dict(extra_reference_release_counts=[1], device_release_count=0, factory_release_count=0,
                       window_destroyed=True, all_owned_resources_released=True)
        if phase == 'texture':
            cleanup.update(texture_surface_release_count=1, texture_release_count=0)
        if case['device_cleanup'] != cleanup or case['platform_cleanup'] != dict(fonts_released=1, dcs_released=1, all_owned_resources_released=True):
            raise ValueError('texture complete additional-reference and resource cleanup')
        calls = case['device']['native']['live_results']+case['factory']['cache_calls']+case['requirements']['api_calls']
        if phase == 'texture':
            calls += case['texture']['api_calls']
        verify_trace(case['device_trace'], [(r['op'], r['request'], r['result']) for r in calls], cleanup)
        platform = case['constructor']['platform_calls']+case['font']['platform_calls']
        verify_trace(case['platform_trace'], [(r['name'], r['request'], r['result']) for r in platform], case['platform_cleanup'])
        if len(case['refused_address_collisions']) > 5:
            raise ValueError('texture bounded collision retries')
        for refused in case['refused_address_collisions']:
            if (refused['error'] != 'live interface mapping collides with audit ownership'
                    or refused['cleanup']['all_owned_resources_released'] is not True
                    or refused['trace'][-1]['reply']['result'] != refused['cleanup']):
                raise ValueError('texture refused collision cleanup')
    return dict(cases=2, phase=phase, texture_created=phase == 'texture', full_owner_bytes=49152,
                heap_guard_bytes=24576, native_calls_each=13 if phase == 'texture' else 6,
                actual_texture_calls_each=20 if phase == 'texture' else 9, retained_VM_advanced=False)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('report')
    a = p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf-8')))))
