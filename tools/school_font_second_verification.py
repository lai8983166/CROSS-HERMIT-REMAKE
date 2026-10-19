"""Independent second-slot CPU/ABI/complete-memory and live trace checks."""
import argparse
import json
import struct
from tools.school_font_second import *
from tools.school_font_slots import SLOT
from tools.school_font_second_emulation import OWNER, TOP, COUNTER, dword, store
from tools.school_font_state_verification import verify_phase
from tools.school_font_glyph_upload_verification import (verify_prefix,verify_atlas,verify_gdi,
    verify_raster,verify_pixels,device_calls,platform_calls,verify_trace,unpack,verify_buffer)
from tools.school_font_state_gdi import SOURCE as GDI_SOURCE,HELPER as GDI_HELPER,COMPILER,sha,machine
from tools.school_font_state_device import SOURCE as DEVICE_SOURCE,HELPER as DEVICE_HELPER


def verify_second(c, phase, owner, image, objects):
    row = c['second_'+phase]
    previous = c[dict(loop='font_states',constructor='second_loop',atlas='second_constructor')[phase]]
    if row['phase'] != phase or row['before_cpu'] != previous['cpu']:
        raise ValueError('second font same pending original CPU')
    device = objects['device']['pointer']
    raw = SOURCE.read_bytes()
    expected_entries = []
    if phase == 'constructor':
        expected_entries = [(0x428A40,0x416047,216,1,[SIZE]),
            (0x401000,0x416083,224,SECOND,[0x592C9C,8,0]),
            (0x56CD90,0x40102A,320,SECOND,[SECOND,0x592C9C])]
    if phase == 'atlas':
        expected_entries = [(0x4010D0,0x4160DF,216,SECOND,[device])]
    if row['entries'] != [dict(va=hex(a),return_va=hex(b),sp=TOP-d,receiver=r,args=args)
                           for a,b,d,r,args in expected_entries]:
        raise ValueError('second font original constructor/caps entry ABI')
    returns = []
    if phase == 'constructor':
        returns = [(0x56CE82,0x428AC2,224,SECOND),(0x428AC5,0x416047,216,SECOND),
            (0x56CE61,0x40102A,320,SECOND),(0x56CE82,0x401087,232,SECOND),
            (0x40108A,0x416083,224,SECOND)]
    if phase == 'atlas':
        returns = [(0x56CE82,0x40117A,720,0)]
    if row['returns'] != [dict(va=hex(a),return_va=hex(b),sp=TOP-d,eax=e) for a,b,d,e in returns]:
        raise ValueError('second font original native returns/stack checks')
    allocations = []
    if phase == 'constructor':
        allocations = [dict(va='0x56e810',return_va='0x428a73',sp=TOP-320,
            args=[SIZE,1,0x594E28,struct.unpack_from('<h',raw,0x5FF6D8-BASE)[0]+3],
            pointer=SECOND,bytes=SIZE,initial_hex='cd'*SIZE,adapter='declared debug CRT allocation')]
    if row['allocations'] != allocations:
        raise ValueError('second font exact distinct bounded CRT allocation')
    cpu = dict(EIP=PHASES[phase][1],ESP=TOP-208,EBP=TOP-96,EAX=0,EBX=0x55667788,
               ECX=1,EDX=device,ESI=TOP-208,EDI=TOP-108,EFLAGS=151)
    pending = dict(va=hex(cpu['EIP']),sp=cpu['ESP'],first_instruction_executed=False)
    calls = row['api_calls']
    value = constructor(b'\xcd'*SIZE)
    if phase == 'constructor':
        cpu.update(ESP=TOP-216,EAX=device,ECX=SECOND,EDX=OWNER,EFLAGS=6)
        pending.update(sp=cpu['ESP'],return_va='0x4160df',receiver=SECOND,args=[device])
    if phase == 'atlas':
        target = objects['device']['methods']['28']
        caps = c['atlas_admission']['api_calls'][0]['result']
        expected = dict(op='caps',va=hex(target),return_va='0x401173',sp=TOP-728,
            args=[device,TOP-440],request=dict(pointer=device),result=caps,live_host_observed=True)
        if calls != [expected] or caps['hr'] != 0 or len(bytes.fromhex(caps['hex'])) != 212:
            raise ValueError('second font actual complete caps identity/ABI/bytes')
        maximum = dword(bytes.fromhex(caps['hex']),88)
        if maximum < 256:
            raise ValueError('second font accepted unscaled case prerequisite')
        value = atlas(value,device,maximum)
        cpu.update(ESP=TOP-748,EBP=TOP-220,EAX=device,ECX=device,
                   EDX=objects['device']['vtable'],ESI=TOP-716,EDI=TOP-220,EFLAGS=6)
        pending.update(sp=cpu['ESP'],method_target=objects['device']['methods']['80'],
            args=[device,256,256,1,0,26,1,SECOND+0x5C],platform_call_executed=False)
    elif calls:
        raise ValueError('second font loop/constructor no platform response')
    if row['cpu'] != cpu or row['pending'] != pending:
        raise ValueError('second font exact unexecuted boundary CPU/arguments')
    if row['loop_locals'] != dict(index=1,status=0,owner=OWNER):
        raise ValueError('second font original loop locals')
    trace = row['instruction_trace']
    visited = set(trace)
    md = Cs(CS_ARCH_X86,CS_MODE_32)
    valid = {i.address for a,b in RANGES.items() for i in md.disasm(raw[a-BASE:b-BASE],a)}
    if row['visited'] != sorted(visited) or not visited <= valid or cpu['EIP'] in visited:
        raise ValueError('second font original body and unexecuted stop')
    if phase == 'loop':
        if trace != LOOP_TRACE:
            raise ValueError('second font exact successful loop trace')
    else:
        required = ({0x41603D,0x416042,0x41605D,0x416068,0x416073,0x41607E,
                     0x4160A5,0x4160DA,0x401025,0x401033,0x40103C,0x401042,
                     0x40104C,0x401056,0x401060,0x40106D,0x56CD90,0x56CE01,
                     0x56CE21,0x56CE5A,0x56CE61} if phase=='constructor' else
                    {0x4010D0,0x4010F9,0x4010FF,0x401147,0x401151,0x401170,
                     0x401180,0x4011DE,0x4011E9,0x40120B})
        if not required <= visited or trace[0] != PHASES[phase][0]:
            raise ValueError('second font required original body/ANSI copy')
        expected_order = ([0x41603D,0x416042,0x428A40,0x416047,0x41605D,0x416068,
            0x416073,0x41607E,0x401000,0x401025,0x56CD90,0x40102A,0x40108A,
            0x416083,0x4160A5,0x4160DA] if phase=='constructor' else
            [0x4010D0,0x4010F9,0x4010FF,0x401147,0x401151,0x401170,0x401173,0x40117A,
             0x401180,0x4011DE,0x4011E9,0x40120B])
        if [at for at in trace if at in expected_order] != expected_order:
            raise ValueError('second font exact critical native order')
        for a,b,*_ in expected_entries:
            i = next(md.disasm(raw[b-BASE-5:b-BASE],b-5))
            if (i.mnemonic,i.op_str) != ('call',hex(a)):
                raise ValueError('second font original direct caller')
    projected_owner = bytearray(owner)
    projected_image = bytearray(image)
    if phase != 'loop':
        store(projected_owner,0x1094,SECOND)
        store(projected_image,COUNTER-BASE,dword(projected_image,COUNTER-BASE)+SIZE)
    verify_buffer(row['state']['owner'],projected_owner)
    if (row['state']['image_sha256'] != hashlib.sha256(projected_image).hexdigest()
            or row['state']['SEH'] != TOP-108 or row['state']['stack_guards_unchanged'] is not True
            or row['state']['foreign_maps'] != previous['state']['foreign_maps']):
        raise ValueError('second font full image/SEH/stack/maps')
    first = c['font_states']
    expected_heaps = first['heaps']+[first['slot_heap']]
    if (row['heaps'] != first['heaps'] or row['slot_heap'] != first['slot_heap']
            or row['retained_heaps'] != expected_heaps):
        raise ValueError('second font preserves every prior complete heap and guard')
    if (row['external_regions'] != first['external_regions']
            or row['external_regions_are_retained_snapshots'] is not True):
        raise ValueError('second font retains full pixel snapshots')
    if phase == 'loop':
        if row['second_heap'] is not None:
            raise ValueError('second font allocated before original request')
    else:
        expected = bytearray(b'\xa5'*12288)
        expected[4096:4096+SIZE] = value
        if row['second_heap']['pointer'] != SECOND-4096:
            raise ValueError('second font distinct declared guarded heap')
        verify_buffer({k:v for k,v in row['second_heap'].items() if k!='pointer'},expected)
    if row['first_additional_font_completed'] is not True:
        raise ValueError('second font preserves first completion')
    if row['second_additional_font_constructed'] is not (phase!='loop') or row['second_atlas_caps_queried'] is not (phase=='atlas'):
        raise ValueError('second font bounded completion authority')
    for k in ('second_atlas_texture_created','second_additional_font_completed','full415F50_returned',
              'GPU_drawing_or_Present','retained_VM_advanced'):
        if row[k] is not False:
            raise ValueError('second font unresolved next resource boundary')


def verify_report(report):
    phase = report['phase']
    if report['schema_version'] != 1 or phase not in PHASES or report['source_contract'] != source_contract():
        raise ValueError('second font fixed source contract')
    for build,source,helper in ((report['device_build'],DEVICE_SOURCE,DEVICE_HELPER),
                               (report['platform_build'],GDI_SOURCE,GDI_HELPER)):
        if build != dict(source_sha256=sha(source.read_bytes()),helper_sha256=sha(helper.read_bytes()),
                compiler_sha256=sha(COMPILER.read_bytes()),machine=0x14C) or machine(helper)!=0x14C:
            raise ValueError('second font unchanged actual x86 helper provenance')
    for k in ('original_IAT_changed','game_helpers_stubbed','retained_VM_advanced',
              'GPU_drawing_or_Present','full_outer_frame','live_handles_resumable_after_cleanup'):
        if report[k] is not False:
            raise ValueError('second font original authority')
    if report['explicit_empty_cache_experiment'] is not True or report['CRT_adapter_executed'] is not True:
        raise ValueError('second font explicit independent inputs')
    if [(c['fill'],c['hello']['width'],c['hello']['height']) for c in report['cases']] != [(0xA5,640,480),(0xCC,1024,768)]:
        raise ValueError('second font exact two cases')
    for c in report['cases']:
        if c['hello']['pointer_bytes']!=4 or c['hello']['window_visible'] is not False or c['platform_hello']['pointer_bytes']!=4:
            raise ValueError('second font hidden owned x86 platform')
        owner,image,objects = verify_prefix(c)
        objects = verify_atlas(c,owner,image,objects)
        verify_gdi(c,owner,image)
        dib = verify_raster(c,owner,image)
        verify_pixels(c,owner,image,objects,dib)
        for p in ('cleanup','vertex','states'):
            objects = verify_phase(c,p,owner,image,objects)
        verify_second(c,'loop',owner,image,objects)
        if phase != 'loop':
            verify_second(c,'constructor',owner,image,objects)
        if phase == 'atlas':
            verify_second(c,'atlas',owner,image,objects)
        dc = dict(atlas_texture_release_count=0,texture_surface_release_count=1,texture_release_count=0,
            extra_reference_release_counts=[3,2,1],device_release_count=0,factory_release_count=0,
            window_destroyed=True,all_owned_resources_released=True,font_texture_unbind_hr=0,
            font_vertex_buffer_release_count=0,font_state_block_delete_results=[0,0])
        pc = dict(native_atlas_fonts_released=1,native_atlas_dcs_released=1,native_atlas_bitmaps_released=1,
            native_bitmap_delete_issued=True,native_cleanup_completed=True,atlas_fonts_released=0,
            atlas_dcs_released=0,atlas_bitmaps_released=0,atlas_selection_restored=True,fonts_released=2,
            dcs_released=1,cache_bitmaps_released=1,cache_dcs_released=1,cache_selection_restored=True,
            all_owned_resources_released=True)
        if c['device_cleanup'] != dc or c['platform_cleanup'] != pc:
            raise ValueError('second font complete actual resource cleanup')
        d = device_calls(c)+c['pixel_upload']['api_calls']+c['font_vertex']['api_calls']+c['font_states']['api_calls']
        if phase == 'atlas':
            d += c['second_atlas']['api_calls']
        p = platform_calls(c)+c['font_cleanup']['api_calls']
        verify_trace(c['device_trace'],[(r['op'],r['request'],r['result']) for r in d],dc)
        verify_trace(c['platform_trace'],[(r['op'] if 'op' in r else r['name'],r['request'],r['result']) for r in p],pc)
        if len(c['refused_address_collisions']) > 5:
            raise ValueError('second font bounded address collision retries')
        for r in c['refused_address_collisions']:
            if (r['error']!='live interface mapping collides with audit ownership'
                    or r['cleanup']['all_owned_resources_released'] is not True
                    or r['trace'][-1]['reply']['result'] != r['cleanup']):
                raise ValueError('second font refused collision cleanup')
    return dict(cases=2,phase=phase,original_success_loop_executed=True,
        distinct_second_font_constructed=phase!='loop',second_caps_queried=phase=='atlas',
        retained_guarded_heap_bytes=49152,second_guarded_heap_bytes=0 if phase=='loop' else 12288,
        second_atlas_texture_created=False,full415F50_returned=False,retained_VM_advanced=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('report')
    a = p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf8')))))
