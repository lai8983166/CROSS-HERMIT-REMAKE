"""Independent full sprite/cache/font stores, live ABI, original returns and lifetimes."""
import json
import struct
from tools.school_font_cache import *
from tools.school_font_cache_emulation import OWNER, STACK, TOP
from tools.school_font_cache_platform import DEVICE_SOURCE, DEVICE_HELPER, GDI_SOURCE, GDI_HELPER, COMPILER, sha, machine
from tools.school_owner_startup import IMPORTS as OWNER_IMPORTS
from tools.school_owner_startup_verification import verify_constructor, verify_device, verify_font
from tools.school_font_startup_verification import verify_factory, verify_trace
from tools.school_font_startup import cache_prefix, font_constructor
from tools.school_font_texture_verification import verify_stage
from tools.school_font_texture import texture_cache, DEBUG_TARGET
from tools.school_renderer_init_verification import verify_buffer


def verify_maps(state, objects):
    expected = {}
    def put(address, data):
        for offset, value in enumerate(data):
            at = address+offset
            expected.setdefault(at & ~4095, bytearray(4096))[at & 4095] = value
    raw = SOURCE.read_bytes()
    for slot in {*OWNER_IMPORTS, *IMPORTS, 0x59246C}:
        put(dword(raw, slot-BASE), b'\xc3')
    put(DEBUG_TARGET, b'\xc3')
    for obj in objects.values():
        put(obj['pointer'], struct.pack('<I', obj['vtable']))
        for slot, target in obj['methods'].items():
            put(obj['vtable']+int(slot), struct.pack('<I', target))
            put(target, b'\xc3')
    if [r['pointer'] for r in state['foreign_maps']] != sorted(expected):
        raise ValueError('cache exact original imports and actual interface maps')
    for r in state['foreign_maps']:
        verify_buffer({k: v for k, v in r.items() if k != 'pointer'}, expected[r['pointer']])


def verify_cache_stage(case, phase, owner, image, objects):
    row = case['sprite' if phase == 'sprite' else 'font_return']
    prior = case['texture']['cpu'] if phase == 'sprite' else case['sprite']['cpu']
    if row['phase'] != phase or row['before_cpu'] != prior:
        raise ValueError('cache same pending CPU continuation required')
    device = objects['device']['pointer']
    entries = [(0x52AE80, 0x5487B9, 716, CACHE+48, [device, CACHE+12]),
               (0x428A40, 0x52AEA7, 736, CACHE+48, [32]),
               (0x53C665, 0x52AEB3, 732, SPRITE, []),
               (0x53BC06, 0x52AECF, 736, SPRITE, [device])] if phase == 'sprite' else []
    if row['entries'] != [dict(va=hex(va), return_va=hex(ret), sp=TOP-depth, receiver=receiver, args=args)
                          for va, ret, depth, receiver, args in entries]:
        raise ValueError('cache original sprite entries and natural stack ABI')
    raw, md = SOURCE.read_bytes(), Cs(CS_ARCH_X86, CS_MODE_32)
    for va, ret, *_ in entries:
        ins = next(md.disasm(raw[ret-BASE-5:ret-BASE], ret-5))
        if ins.mnemonic != 'call' or int(ins.op_str, 16) != va:
            raise ValueError('cache original direct caller bytes')
    returns = [(0x56CE82, 0x428AC2, 744, SPRITE), (0x428AC5, 0x52AEA7, 736, SPRITE),
               (0x53C682, 0x52AEB3, 732, SPRITE), (0x53BC78, 0x52AECF, 736, 0),
               (0x52AEE9, 0x5487B9, 716, 0)] if phase == 'sprite' else [
               (0x548873, 0x548DE0, 468, 0), (0x548DFD, 0x53BA15, 452, 0),
               (0x53BA53, 0x52AE5B, 432, 0), (0x52AE7D, 0x52B015, 404, 0),
               (0x52B016, 0x4162F4, 324, 0), (0x56CE82, 0x416311, 224, FONT),
               (0x416314, 0x416002, 216, FONT)]
    if row['returns'] != [dict(va=hex(va), return_va=hex(ret), sp=TOP-depth, eax=eax) for va, ret, depth, eax in returns]:
        raise ValueError('cache natural complete factory returns')
    instructions = [i for a, b in RANGES.items() for i in md.disasm(raw[a-BASE:b-BASE], a)]
    valid, visited = {i.address for i in instructions}, set(row['visited'])
    stop = dword(raw, 0x592094-BASE) if phase == 'sprite' else 0x416021
    if (row['visited'] != sorted(visited) or not {r[0] for r in entries} <= visited
            or any(at not in valid for at in visited) or stop in visited):
        raise ValueError('cache original native bodies and unexecuted boundary')
    for va, *_ in returns:
        if va not in visited or not any(i.address == va and i.mnemonic == 'ret' for i in instructions):
            raise ValueError('cache original return instruction')
    allocation = [dict(va='0x56e810', return_va='0x428a73', sp=TOP-840,
                       args=[32, 1, 0x594E28, struct.unpack_from('<h', raw, 0x5FF6D8-BASE)[0]+3],
                       pointer=SPRITE, bytes=32, initial_hex='cd'*32, adapter='declared debug CRT allocation')] if phase == 'sprite' else []
    if row['allocations'] != allocation:
        raise ValueError('cache bounded original sprite CRT allocation')
    caps_hex = case['factory']['cache_calls'][1]['result']['hex']
    creation_hex = struct.pack('<4I', 0, 1, case['hello']['window'], 68).hex()
    device_rows = [('sprite_addref', 4, 0x53BC2B, 980, [device], dict(count=4)),
                   ('sprite_caps', 28, 0x53BC38, 984, [device, TOP-968], dict(hr=0, hex=caps_hex)),
                   ('sprite_creation', 36, 0x53BC45, 984, [device, TOP-756], dict(hr=0, hex=creation_hex))]
    if phase == 'font':
        device_rows = [('font_addref', 4, 0x53BA3C, 448, [device], dict(count=5))]
    expected_calls = [dict(op=op, va=hex(objects['device']['methods'][str(slot)]), return_va=hex(ret), sp=TOP-depth,
                           args=args, request=dict(pointer=device), result=result, live_host_observed=True)
                      for op, slot, ret, depth, args, result in device_rows]
    if row['device_calls'] != expected_calls:
        raise ValueError('cache actual sprite/font device ABI and complete buffers')
    gdi = row['gdi_calls']
    if phase == 'sprite':
        if gdi:
            raise ValueError('cache sprite stop precedes first GDI call')
    else:
        if [r['name'] for r in gdi] != [r[0] for r in IMPORTS.values()]:
            raise ValueError('cache exact original GDI request order')
        dc, bitmap, old_bitmap, bits, font_handle = (gdi[0]['result']['result'], gdi[1]['result']['result'],
                                                    gdi[5]['result']['result'], gdi[1]['result']['bits'], gdi[6]['result']['result'])
        if not all(isinstance(v, int) and 0 < v < 0xFFFFFFFF for v in (dc, bitmap, old_bitmap, bits, font_handle)):
            raise ValueError('cache actual32-bit owned GDI resources')
        logfont_hex = case['font']['LOGFONT']
        specifications = [(720, [0], {}, dict(result=dc)),
                           (740, [dc, CACHE+0x70, 0, CACHE+0xA0, 0, 0], dict(pointer=dc, header_hex=bitmap_header(True).hex()), dict(result=bitmap, bits=bits)),
                           (724, [dc, 2], dict(pointer=dc, value=2), dict(result=2)),
                           (724, [dc, 0], dict(pointer=dc, value=0), dict(result=0xFFFFFF)),
                           (724, [dc, 0xFFFFFF], dict(pointer=dc, value=0xFFFFFF), dict(result=0)),
                           (724, [dc, bitmap], dict(pointer=dc, object=bitmap), dict(result=old_bitmap)),
                           (448, [TOP-388], dict(logfont_hex=logfont_hex), dict(result=font_handle,
                            inspection=dict(native_requested=False, method='GetObjectA', result=60, hex=logfont_hex)))]
        for actual, (slot, (name, ret, _)), (depth, args, request, result) in zip(gdi, IMPORTS.items(), specifications):
            if actual != dict(name=name, slot=hex(slot), va=hex(dword(raw, slot-BASE)), return_va=hex(ret), sp=TOP-depth,
                              args=args, request=request, result=result, live_host_observed=True):
                raise ValueError('cache original GDI ABI/complete header/LOGFONT/inspection')
    caps, creation = bytes.fromhex(caps_hex), bytes.fromhex(creation_hex)
    cache_base = texture_cache(cache_prefix(b'\xcd'*176, device, caps), objects['texture']['pointer'], objects['texture_surface']['pointer'])
    cache = cache_before_gdi(cache_base) if phase == 'sprite' else cache_after_gdi(cache_base, dc, bitmap, old_bitmap, bits)
    font = font_constructor(b'\xcd'*80) if phase == 'sprite' else font_complete(device, font_handle, bytes.fromhex(case['font']['LOGFONT']))
    sprite_value = sprite(b'\xcd'*32, device, caps, creation)
    expected_owner = bytearray(owner)
    if phase == 'font':
        store(expected_owner, 0xB270, FONT)
    verify_buffer(row['state']['owner'], expected_owner)
    if row['state']['image_sha256'] != sha(image) or row['state']['SEH'] != TOP-108 or row['state']['stack_guards_unchanged'] is not True:
        raise ValueError('cache full original image/SEH/stack retention')
    verify_maps(row['state'], objects)
    if len(row['heaps']) != 3:
        raise ValueError('cache all three complete object/guard regions required')
    for observed, ptr, value in zip(row['heaps'], (FONT, CACHE, SPRITE), (font, cache, sprite_value)):
        expected = bytearray(b'\xa5'*12288)
        expected[4096:4096+len(value)] = value
        if observed['pointer'] != ptr-4096:
            raise ValueError('cache declared heap address')
        verify_buffer({k: v for k, v in observed.items() if k != 'pointer'}, expected)
    if phase == 'sprite':
        cpu = dict(EIP=stop, ESP=TOP-720, EBP=TOP-472, EAX=256, EBX=CACHE+112, ECX=0,
                   EDX=TOP-756, ESI=CACHE, EDI=0, EFLAGS=70)
        pending = dict(va=hex(stop), sp=TOP-720, first_instruction_executed=False, return_va='0x548805',
                       args=[0], platform_call_executed=False)
    else:
        cpu = dict(EIP=0x416021, ESP=TOP-208, EBP=TOP-96, EAX=OWNER, EBX=0x55667788, ECX=0,
                   EDX=OWNER, ESI=TOP-208, EDI=TOP-108, EFLAGS=6)
        pending = dict(va='0x416021', sp=TOP-208, first_instruction_executed=False)
    if row['cpu'] != cpu or row['pending'] != pending or row['output_slot'] != dict(pointer=TOP-228, value=FONT if phase == 'font' else 0xCCCCCCCC):
        raise ValueError('cache precise original return CPU/stack/font output')
    if row['first_static_font_completed'] is not (phase == 'font'):
        raise ValueError('cache actual first-font completion boundary')
    if any(row[k] is not False for k in ('full415F50_returned', 'state_blocks_created', 'DIB_bits_target_read', 'retained_VM_advanced')):
        raise ValueError('cache startup completion scope')


def verify_report(report):
    phase = report['phase']
    if report['schema_version'] != 1 or phase not in ('sprite', 'font') or report['source_contract'] != source_contract():
        raise ValueError('cache fixed original source contract')
    for key in ('original_IAT_changed', 'game_helpers_stubbed', 'retained_VM_advanced', 'drawing_or_Present',
                'full_outer_frame', 'live_handles_resumable_after_cleanup'):
        if report[key] is not False:
            raise ValueError('cache original startup authority')
    if report['explicit_empty_cache_experiment'] is not True or report['CRT_adapter_executed'] is not True:
        raise ValueError('cache explicit experiment/CRT declarations')
    for build, source, helper in ((report['device_build'], DEVICE_SOURCE, DEVICE_HELPER), (report['platform_build'], GDI_SOURCE, GDI_HELPER)):
        if build != dict(source_sha256=sha(source.read_bytes()), helper_sha256=sha(helper.read_bytes()),
                         compiler_sha256=sha(COMPILER.read_bytes()), machine=machine(helper)) or machine(helper) != 0x14C:
            raise ValueError('cache actual x86 device/GDI build provenance')
    if [(c['fill'], c['hello']['width'], c['hello']['height']) for c in report['cases']] != [(0xA5, 640, 480), (0xCC, 1024, 768)]:
        raise ValueError('cache original two declared cases')
    for case in report['cases']:
        if case['hello']['pointer_bytes'] != 4 or case['hello']['window_visible'] is not False or case['platform_hello']['pointer_bytes'] != 4:
            raise ValueError('cache owned hidden x86 platform')
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
        objects = verify_stage(case, 'texture', bytes(owner), bytes(image), objects)
        store(image, COUNTER-BASE, dword(image, COUNTER-BASE)+32)
        verify_cache_stage(case, 'sprite', bytes(owner), bytes(image), objects)
        if phase == 'font':
            verify_cache_stage(case, 'font', bytes(owner), bytes(image), objects)
        device_cleanup = dict(texture_surface_release_count=1, texture_release_count=0,
                              extra_reference_release_counts=[3, 2, 1] if phase == 'font' else [2, 1],
                              device_release_count=0, factory_release_count=0, window_destroyed=True, all_owned_resources_released=True)
        platform_cleanup = dict(fonts_released=2 if phase == 'font' else 1, dcs_released=1,
                                cache_bitmaps_released=int(phase == 'font'), cache_dcs_released=int(phase == 'font'),
                                cache_selection_restored=True, all_owned_resources_released=True)
        if case['device_cleanup'] != device_cleanup or case['platform_cleanup'] != platform_cleanup:
            raise ValueError('cache complete COM/GDI selection/resource cleanup')
        device_calls = case['device']['native']['live_results']+case['factory']['cache_calls']+case['requirements']['api_calls']+case['texture']['api_calls']+case['sprite']['device_calls']
        if phase == 'font':
            device_calls += case['font_return']['device_calls']
        verify_trace(case['device_trace'], [(r['op'], r['request'], r['result']) for r in device_calls], device_cleanup)
        platform_calls = case['constructor']['platform_calls']+case['font']['platform_calls']
        if phase == 'font':
            platform_calls += case['font_return']['gdi_calls']
        verify_trace(case['platform_trace'], [(r['name'], r['request'], r['result']) for r in platform_calls], platform_cleanup)
        if len(case['refused_address_collisions']) > 5:
            raise ValueError('cache bounded live process collision retries')
        for refused in case['refused_address_collisions']:
            if (refused['error'] != 'live interface mapping collides with audit ownership'
                    or refused['cleanup']['all_owned_resources_released'] is not True
                    or refused['trace'][-1]['reply']['result'] != refused['cleanup']):
                raise ValueError('cache refused collision cleanup')
    return dict(cases=2, phase=phase, first_static_font_completed=phase == 'font',
                full_owner_bytes=49152, heap_guard_bytes=36864, retained_VM_advanced=False)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('report')
    a = p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf-8')))))
