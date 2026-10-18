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


def verify_gdi(case, owner, image):
    row, previous = case['GDI_preparation'], case['atlas_texture']
    if row['phase'] != 'gdi' or row['before_cpu'] != previous['cpu']:
        raise ValueError('atlas GDI same pending original CPU')
    calls = row['api_calls']
    if len(calls) != 10: raise ValueError('atlas exact ten original GDI calls')
    dc, bitmap, bits, font, old_bitmap, old_font = (calls[0]['result']['result'], calls[1]['result']['result'],
        calls[1]['result']['bits'], calls[4]['result']['result'], calls[5]['result']['result'], calls[6]['result']['result'])
    if not all(isinstance(v, int) and 0 < v < 0xFFFFFFFF for v in (dc, bitmap, bits, font, old_bitmap, old_font)):
        raise ValueError('atlas actual owned GDI resource identities')
    specs = [(724, [0], {}, dict(result=dc)),
        (744, [dc, TOP-488, 0, TOP-444, 0, 0], dict(pointer=dc, header_hex=bitmap_header().hex()), dict(result=bitmap, bits=bits)),
        (728, [dc, 1], dict(pointer=dc, value=1), dict(result=1)),
        (732, [12, 96, 72], dict(args=[12, 96, 72]), dict(result=16)),
        (776, [v & 0xFFFFFFFF for v in FONT_ARGS]+[SLOT], dict(args=FONT_ARGS, face_hex='4669786564537973'),
            dict(result=font, inspection=dict(native_requested=False, method='GetObjectA', result=60, hex=font_logfont().hex()))),
        (728, [dc, bitmap], dict(pointer=dc, object=bitmap), dict(result=old_bitmap)),
        (728, [dc, font], dict(pointer=dc, object=font), dict(result=old_font)),
        (728, [dc, 0xFFFFFF], dict(pointer=dc, value=0xFFFFFF), dict(result=0)),
        (728, [dc, 0], dict(pointer=dc, value=0), dict(result=0xFFFFFF)),
        (728, [dc, 0], dict(pointer=dc, value=0), dict(result=0))]
    raw = SOURCE.read_bytes()
    for actual, (slot, name, ret, count, op), (depth, args, request, result) in zip(calls, IMPORTS, specs):
        if actual != dict(op=op, name=name, slot=hex(slot), va=hex(dword(raw, slot-BASE)), return_va=hex(ret),
            sp=TOP-depth, args=args, request=request, result=result, live_host_observed=True):
            raise ValueError('atlas exact original GDI ABI/header/font/selection/inspection')
    if row['entries'] != [dict(va='0x56cfcc', return_va='0x4012f8', sp=TOP-724, receiver=dc, args=[])]:
        raise ValueError('atlas original native float-to-int entry')
    returns = [(0x56CE82, 0x40128B, 720, dc), (0x56CE82, 0x4012BB, 720, bitmap),
        (0x56CE82, 0x4012D9, 720, 1), (0x56CFF2, 0x4012F8, 724, 96),
        (0x56CE82, 0x40130D, 720, 16), (0x56CE82, 0x401385, 720, font),
        (0x56CE82, 0x4013BB, 720, old_bitmap), (0x56CE82, 0x4013D8, 720, old_font),
        (0x56CE82, 0x4013F3, 720, 0), (0x56CE82, 0x40140B, 720, 0xFFFFFF), (0x56CE82, 0x401423, 720, 0)]
    if row['returns'] != [dict(va=hex(a), return_va=hex(b), sp=TOP-d, eax=e) for a, b, d, e in returns]:
        raise ValueError('atlas original GDI stack-check and arithmetic returns')
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    instructions = [i for a, b in RANGES.items() for i in md.disasm(raw[a-BASE:b-BASE], a)]
    visited = set(row['visited'])
    required = {0x40128B, 0x4012BB, 0x4012F3, 0x40130D, 0x401322, 0x401328,
        0x401378, 0x4013AE, 0x4013CB, 0x401416, 0x401444, 0x40145C, 0x401472,
        0x56CFCC, 0x56CFE5, 0x56CFF2}
    if row['visited'] != sorted(visited) or not required <= visited or not visited <= {i.address for i in instructions} or 0x401491 in visited:
        raise ValueError('atlas original GDI/arithmetic bodies and unexecuted glyph call')
    cpu = dict(EIP=0x401491, ESP=TOP-732, EBP=TOP-220, EAX=dc, EBX=0x55667788,
               ECX=TOP-536, EDX=TOP-528, ESI=TOP-716, EDI=TOP-220, EFLAGS=147)
    pending = dict(va='0x401491', sp=TOP-732, first_instruction_executed=False, platform_call_executed=False,
        method_target=dword(raw, 0x5920BC-BASE), args=[dc, TOP-528, 1, TOP-536])
    if row['cpu'] != cpu or row['pending'] != pending:
        raise ValueError('atlas exact first glyph CPU/arguments/stack')
    if row['GDI_locals'] != dict(dc=dc, bitmap=bitmap, bits=bits, font=font, height=0xFFFFFFF0, weight=700,
        italic=0, x=0, y=0, text_hex='2000', character='20') or row['bitmap_header'] != previous['bitmap_header']:
        raise ValueError('atlas original local resources/font arithmetic/first character/header')
    verify_buffer(row['state']['owner'], owner)
    if row['state']['image_sha256'] != sha(image) or row['state']['SEH'] != TOP-108 or row['state']['stack_guards_unchanged'] is not True:
        raise ValueError('atlas GDI full image/SEH/stack retention')
    expected_maps = {r['pointer']: bytearray(unpack(r)) for r in previous['state']['foreign_maps']}
    for slot, *_ in IMPORTS:
        target = dword(raw, slot-BASE)
        expected_maps.setdefault(target & ~4095, bytearray(4096))[target & 4095] = 0xC3
    if [r['pointer'] for r in row['state']['foreign_maps']] != sorted(expected_maps):
        raise ValueError('atlas exact original import/COM maps')
    for observed in row['state']['foreign_maps']:
        verify_buffer({k: v for k, v in observed.items() if k != 'pointer'}, expected_maps[observed['pointer']])
    if row['slot_heap'] != previous['slot_heap'] or row['heaps'] != previous['heaps']:
        raise ValueError('atlas GDI all four complete heaps/guards retained')
    if row['atlas_texture_created'] is not True or row['GDI_prepared'] is not True:
        raise ValueError('atlas GDI actual completion boundary')
    for key in ('glyph_measurement_executed', 'DIB_pixels_read', 'glyph_upload_executed', 'full415F50_returned', 'state_blocks_created', 'retained_VM_advanced'):
        if row[key] is not False: raise ValueError('atlas GDI unresolved glyph/startup boundary')


def verify_report(report):
    phase = report['phase']
    if report['schema_version'] != 1 or phase not in ('texture', 'gdi') or report['source_contract'] != source_contract():
        raise ValueError('atlas exact source contract')
    for key in ('original_IAT_changed', 'game_helpers_stubbed', 'retained_VM_advanced', 'drawing_or_Present', 'full_outer_frame', 'live_handles_resumable_after_cleanup'):
        if report[key] is not False: raise ValueError('atlas original authority')
    if report['explicit_empty_cache_experiment'] is not True or report['CRT_adapter_executed'] is not True:
        raise ValueError('atlas declared experiment inputs')
    from tools.school_font_atlas_gdi import SOURCE as ATLAS_GDI_SOURCE, HELPER as ATLAS_GDI_HELPER
    for build, source, helper in ((report['device_build'], DEVICE_SOURCE, DEVICE_HELPER),
            (report['platform_build'], GDI_SOURCE if phase == 'texture' else ATLAS_GDI_SOURCE, GDI_HELPER if phase == 'texture' else ATLAS_GDI_HELPER)):
        if build != dict(source_sha256=sha(source.read_bytes()), helper_sha256=sha(helper.read_bytes()), compiler_sha256=sha(COMPILER.read_bytes()), machine=0x14C) or machine(helper) != 0x14C:
            raise ValueError('atlas actual immutable x86 build provenance')
    if [(c['fill'], c['hello']['width'], c['hello']['height']) for c in report['cases']] != [(0xA5, 640, 480), (0xCC, 1024, 768)]:
        raise ValueError('atlas two declared cases')
    for case in report['cases']:
        if case['hello']['pointer_bytes'] != 4 or case['hello']['window_visible'] is not False or case['platform_hello']['pointer_bytes'] != 4:
            raise ValueError('atlas owned hidden x86 platform')
        owner, image, objects = verify_prefix(case)
        verify_atlas(case, owner, image, objects)
        if phase == 'gdi': verify_gdi(case, owner, image)
        cleanup = dict(atlas_texture_release_count=0, texture_surface_release_count=1, texture_release_count=0,
                       extra_reference_release_counts=[3, 2, 1], device_release_count=0, factory_release_count=0,
                       window_destroyed=True, all_owned_resources_released=True)
        platform_cleanup = dict(fonts_released=2, dcs_released=1, cache_bitmaps_released=1,
                               cache_dcs_released=1, cache_selection_restored=True, all_owned_resources_released=True)
        if phase == 'gdi': platform_cleanup.update(atlas_fonts_released=1, atlas_dcs_released=1,
            atlas_bitmaps_released=1, atlas_selection_restored=True)
        if case['device_cleanup'] != cleanup or case['platform_cleanup'] != platform_cleanup:
            raise ValueError('atlas complete real resource cleanup')
        device_calls = (case['device']['native']['live_results']+case['factory']['cache_calls']+
            case['requirements']['api_calls']+case['texture']['api_calls']+case['sprite']['device_calls']+
            case['font_return']['device_calls']+case['atlas_admission']['api_calls']+case['atlas_texture']['api_calls'])
        platform_calls = case['constructor']['platform_calls']+case['font']['platform_calls']+case['font_return']['gdi_calls']
        verify_trace(case['device_trace'], [(r['op'], r['request'], r['result']) for r in device_calls], cleanup)
        if phase == 'gdi': platform_calls += case['GDI_preparation']['api_calls']
        verify_trace(case['platform_trace'], [(r['op'] if 'op' in r else r['name'], r['request'], r['result']) for r in platform_calls], platform_cleanup)
        if len(case['refused_address_collisions']) > 5: raise ValueError('atlas bounded collision retries')
        for refused in case['refused_address_collisions']:
            if refused['error'] != 'live interface mapping collides with audit ownership' or refused['cleanup']['all_owned_resources_released'] is not True or refused['trace'][-1]['reply']['result'] != refused['cleanup']:
                raise ValueError('atlas refused process cleanup')
    return dict(cases=2, phase=phase, atlas_texture_created=True, GDI_prepared=phase == 'gdi',
                full_slot_bytes=1656, heap_guard_bytes=49152, retained_VM_advanced=False)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('report'); a = p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf-8')))))
