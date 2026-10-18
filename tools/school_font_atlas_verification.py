"""Independent original-prefix, extra atlas, source/ABI and lifetime verification."""
import json
import struct
from tools.school_font_atlas import *
from tools.school_font_atlas_emulation import OWNER, TOP
from tools.school_font_atlas_device import SOURCE as DEVICE_SOURCE, HELPER as DEVICE_HELPER, COMPILER, sha, machine
from tools.school_font_cache_platform import GDI_SOURCE, GDI_HELPER
from tools.school_owner_startup_verification import verify_constructor, verify_device, verify_font
from tools.school_font_startup_verification import verify_factory, verify_trace
from tools.school_font_texture_verification import verify_stage as verify_texture
from tools.school_font_cache_verification import verify_cache_stage, verify_maps
from tools.school_font_slots_verification import verify_stage as verify_slot
from tools.school_font_cache import FONT, CACHE, HEAD, COUNTER
from tools.school_device_init_verification import unpack
from tools.school_renderer_init_verification import verify_buffer


def verify_prefix(case):
    owner, image = verify_constructor(case)
    owner, objects = verify_device(case, owner, image)
    verify_font(case, owner, image, objects)
    owner = bytearray(owner); store(owner, 0xB26C, case['font']['platform_calls'][0]['result']['result'])
    verify_factory(case, 'empty', bytes(owner), image, objects)
    image = bytearray(image); store(image, COUNTER-BASE, dword(image, COUNTER-BASE)+256); store(image, HEAD-BASE, CACHE)
    objects = verify_texture(case, 'requirements', bytes(owner), bytes(image), objects)
    objects = verify_texture(case, 'texture', bytes(owner), bytes(image), objects)
    store(image, COUNTER-BASE, dword(image, COUNTER-BASE)+32)
    verify_cache_stage(case, 'sprite', bytes(owner), bytes(image), objects)
    verify_cache_stage(case, 'font', bytes(owner), bytes(image), objects)
    verify_slot(case, 'constructor'); verify_slot(case, 'atlas')
    store(image, COUNTER-BASE, dword(image, COUNTER-BASE)+SIZE)
    store(owner, 0xB270, FONT); store(owner, 0x1090, SLOT)
    return bytes(owner), bytes(image), objects


def verify_atlas(case, owner, image, objects):
    row = case['atlas_texture']; device = objects['device']['pointer']
    if row['phase'] != 'texture' or row['before_cpu'] != case['atlas_admission']['cpu']:
        raise ValueError('atlas original pending CPU continuation')
    if row['entries'] != [dict(va='0x56cec0', return_va='0x401237', sp=TOP-732, receiver=device, args=[TOP-488, 0, 40])]:
        raise ValueError('atlas original memset ABI')
    if row['returns'] != [dict(va='0x56ce82', return_va='0x401216', sp=TOP-720, eax=0),
                          dict(va='0x56cf12', return_va='0x401237', sp=TOP-732, eax=TOP-488)]:
        raise ValueError('atlas original native returns')
    calls = row['api_calls']
    if len(calls) != 1: raise ValueError('atlas exactly one native texture call')
    texture = calls[0]['result']['texture']
    if (not 0 < texture['pointer'] <= 0xFFFFFFFF or not 0 < texture['vtable'] <= 0xFFFFFFFF
            or set(texture['methods']) != {'8', '56', '64', '68'}
            or not all(0 < target <= 0xFFFFFFFF for target in texture['methods'].values())
            or texture['pointer'] in [obj['pointer'] for obj in objects.values()]):
        raise ValueError('atlas additional actual owned texture identity')
    result = dict(hr=0, texture=texture, inspection=dict(native_requested=False, method='GetLevelDesc', level=0,
        result=dict(hr=0, hex=struct.pack('<8I', 26, 1, 0, 1, 131072, 0, 256, 256).hex())))
    if calls != [dict(op='atlas_create', va=hex(objects['device']['methods']['80']), return_va='0x40120f', sp=TOP-752,
        args=[device, 256, 256, 1, 0, 26, 1, SLOT+0x5C],
        request=dict(pointer=device, width=256, height=256, levels=1, usage=0, format=26, pool=1), result=result, live_host_observed=True)]:
        raise ValueError('atlas exact actual texture arguments/description/ABI')
    raw, md = SOURCE.read_bytes(), Cs(CS_ARCH_X86, CS_MODE_32)
    instructions = [i for a, b in RANGES.items() for i in md.disasm(raw[a-BASE:b-BASE], a)]
    visited = set(row['visited'])
    required = {0x40120C, 0x401232, 0x40123A, 0x40124A, 0x401258, 0x40125E, 0x401267, 0x401271, 0x40127E, 0x56CF01, 0x56CF12}
    if row['visited'] != sorted(visited) or not required <= visited or not visited <= {i.address for i in instructions}:
        raise ValueError('atlas original native bodies/bitmap stores')
    if row['bitmap_header'] != dict(pointer=TOP-488, hex=bitmap_header().hex()):
        raise ValueError('atlas original complete stack bitmap header')
    stop = dword(raw, 0x592094-BASE)
    cpu = dict(EIP=stop, ESP=TOP-724, EBP=TOP-220, EAX=SLOT, EBX=0x55667788,
               ECX=0xFFFFFF00, EDX=256, ESI=TOP-716, EDI=TOP-220, EFLAGS=135)
    pending = dict(va=hex(stop), sp=TOP-724, first_instruction_executed=False,
                   return_va='0x401284', args=[0], platform_call_executed=False)
    if row['cpu'] != cpu or row['pending'] != pending or stop in visited:
        raise ValueError('atlas exact pending GDI original CPU/stack')
    verify_buffer(row['state']['owner'], owner)
    if row['state']['image_sha256'] != sha(image) or row['state']['SEH'] != TOP-108 or row['state']['stack_guards_unchanged'] is not True:
        raise ValueError('atlas complete image/SEH/stack retention')
    objects = dict(objects, atlas_texture=texture)
    verify_maps(row['state'], objects)
    if row['heaps'] != case['atlas_admission']['heaps']:
        raise ValueError('atlas complete retained parent heaps')
    expected = bytearray(b'\xa5'*12288)
    expected[4096:4096+SIZE] = texture_object(unpack(case['atlas_admission']['slot_heap'])[4096:4096+SIZE], texture['pointer'])
    if row['slot_heap']['pointer'] != SLOT-4096: raise ValueError('atlas declared slot address')
    verify_buffer({k: v for k, v in row['slot_heap'].items() if k != 'pointer'}, expected)
    if row['atlas_texture_created'] is not True or row['GDI_prepared'] is not False:
        raise ValueError('atlas actual completion boundary')
    for key in ('glyph_measurement_executed', 'DIB_pixels_read', 'glyph_upload_executed', 'full415F50_returned', 'state_blocks_created', 'retained_VM_advanced'):
        if row[key] is not False: raise ValueError('atlas bounded unresolved work')
    return objects


def verify_report(report):
    if report['schema_version'] != 1 or report['phase'] != 'texture' or report['source_contract'] != source_contract():
        raise ValueError('atlas exact source contract')
    for key in ('original_IAT_changed', 'game_helpers_stubbed', 'retained_VM_advanced', 'drawing_or_Present', 'full_outer_frame', 'live_handles_resumable_after_cleanup'):
        if report[key] is not False: raise ValueError('atlas original authority')
    if report['explicit_empty_cache_experiment'] is not True or report['CRT_adapter_executed'] is not True:
        raise ValueError('atlas declared experiment inputs')
    for build, source, helper in ((report['device_build'], DEVICE_SOURCE, DEVICE_HELPER), (report['platform_build'], GDI_SOURCE, GDI_HELPER)):
        if build != dict(source_sha256=sha(source.read_bytes()), helper_sha256=sha(helper.read_bytes()), compiler_sha256=sha(COMPILER.read_bytes()), machine=0x14C) or machine(helper) != 0x14C:
            raise ValueError('atlas actual immutable x86 build provenance')
    if [(c['fill'], c['hello']['width'], c['hello']['height']) for c in report['cases']] != [(0xA5, 640, 480), (0xCC, 1024, 768)]:
        raise ValueError('atlas two declared cases')
    for case in report['cases']:
        if case['hello']['pointer_bytes'] != 4 or case['hello']['window_visible'] is not False or case['platform_hello']['pointer_bytes'] != 4:
            raise ValueError('atlas owned hidden x86 platform')
        owner, image, objects = verify_prefix(case)
        verify_atlas(case, owner, image, objects)
        cleanup = dict(atlas_texture_release_count=0, texture_surface_release_count=1, texture_release_count=0,
                       extra_reference_release_counts=[3, 2, 1], device_release_count=0, factory_release_count=0,
                       window_destroyed=True, all_owned_resources_released=True)
        platform_cleanup = dict(fonts_released=2, dcs_released=1, cache_bitmaps_released=1,
                               cache_dcs_released=1, cache_selection_restored=True, all_owned_resources_released=True)
        if case['device_cleanup'] != cleanup or case['platform_cleanup'] != platform_cleanup:
            raise ValueError('atlas complete real resource cleanup')
        device_calls = (case['device']['native']['live_results']+case['factory']['cache_calls']+
            case['requirements']['api_calls']+case['texture']['api_calls']+case['sprite']['device_calls']+
            case['font_return']['device_calls']+case['atlas_admission']['api_calls']+case['atlas_texture']['api_calls'])
        platform_calls = case['constructor']['platform_calls']+case['font']['platform_calls']+case['font_return']['gdi_calls']
        verify_trace(case['device_trace'], [(r['op'], r['request'], r['result']) for r in device_calls], cleanup)
        verify_trace(case['platform_trace'], [(r['name'], r['request'], r['result']) for r in platform_calls], platform_cleanup)
        if len(case['refused_address_collisions']) > 5: raise ValueError('atlas bounded collision retries')
        for refused in case['refused_address_collisions']:
            if refused['error'] != 'live interface mapping collides with audit ownership' or refused['cleanup']['all_owned_resources_released'] is not True or refused['trace'][-1]['reply']['result'] != refused['cleanup']:
                raise ValueError('atlas refused process cleanup')
    return dict(cases=2, phase='texture', atlas_texture_created=True, GDI_prepared=False,
                full_slot_bytes=1656, heap_guard_bytes=49152, retained_VM_advanced=False)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('report'); a = p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf-8')))))
