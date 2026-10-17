"""Independent original factory stores, live ABI, complete heaps and cache boundaries."""
import json
import struct
from tools.school_font_startup import *
from tools.school_font_startup_emulation import OWNER, STACK, TOP, RETURN
from tools.school_font_device_bridge import SOURCE as BRIDGE_SOURCE, HELPER, COMPILER, sha, machine
from tools.school_owner_platform import SOURCE as PLATFORM_SOURCE, HELPER as PLATFORM_HELPER
from tools.school_owner_startup_verification import verify_constructor, verify_device, verify_font, verify_state
from tools.school_renderer_init_verification import verify_buffer


def verify_factory(case, mode, owner, image, objects):
    row = case['factory']
    device = objects['device']['pointer']
    handle = case['font']['platform_calls'][0]['result']['result']
    if row['before_cpu'] != case['font']['native']['cpu']:
        raise ValueError('font actual pending factory CPU required')
    initial = bytearray(image)
    if mode == 'empty':
        store(initial, HEAD-BASE, 0)
    expected_declared = dict(mode=mode, inherited_head=source_contract()['inherited_head'],
                            initial_head=0 if mode == 'empty' else source_contract()['inherited_head'],
                            empty_cache_explicitly_declared=mode == 'empty',
                            retained_VM_or_source_file_changed=False, initial_image_sha256=sha(initial))
    if row['declared'] != expected_declared:
        raise ValueError('font inherited versus explicit empty-cache input')
    entries = [(0x52AE11, 0x52B015, 404, handle, [device, TOP-388, TOP-228]),
               (0x428A40, 0x52AE31, 428, handle, [80]),
               (0x53BB9E, 0x52AE3D, 424, FONT, []),
               (0x53B9F8, 0x52AE5B, 432, FONT, [device, TOP-388]),
               (0x548D89, 0x53BA15, 452, FONT, [device, FONT+72])]
    returns = [(0x56CE82, 0x428AC2, 436, FONT), (0x428AC5, 0x52AE31, 428, FONT),
               (0x53BBB8, 0x52AE3D, 424, FONT)]
    if mode == 'empty':
        entries += [(0x428A40, 0x548DAF, 468, FONT, [176]),
                    (0x5483B1, 0x548DBB, 464, CACHE, []),
                    (0x548735, 0x548DE0, 468, CACHE, [device]),
                    (0x54864C, 0x5487A5, 708, CACHE, [])]
        returns += [(0x56CE82, 0x428AC2, 476, CACHE), (0x428AC5, 0x548DAF, 468, CACHE),
                    (0x5483FB, 0x548DBB, 464, CACHE)]
    expected_entries = [dict(va=hex(va), return_va=hex(ret), sp=TOP-depth, receiver=receiver, args=args)
                        for va, ret, depth, receiver, args in entries]
    if row['entries'] != expected_entries:
        raise ValueError('font complete original calls and stack ABI')
    raw, md = SOURCE.read_bytes(), Cs(CS_ARCH_X86, CS_MODE_32)
    bodies = {a: list(md.disasm(raw[a-BASE:b-BASE], a)) for a, b in {**RANGES, 0x56CE80: 0x56CE83}.items()}
    for va, ret, _, _, _ in entries:
        ins = next(md.disasm(raw[ret-BASE-5:ret-BASE], ret-5))
        if ins.mnemonic != 'call' or int(ins.op_str, 16) != va:
            raise ValueError('font original E8 bytes and caller')
    expected_returns = [dict(va=hex(va), return_va=hex(ret), sp=TOP-depth, eax=eax)
                        for va, ret, depth, eax in returns]
    if row['returns'] != expected_returns:
        raise ValueError('font original natural returns and CRT stack check')
    allowed_entries = {r[0] for r in entries} | {0x56CE80}
    valid = {i.address for a in allowed_entries for i in bodies[a]}
    if (row['visited'] != sorted(set(row['visited'])) or not allowed_entries <= set(row['visited'])
            or any(a not in valid for a in row['visited']) or STOPS[mode] in row['visited']):
        raise ValueError('font original visited bodies and unexecuted boundary')
    for va, ret, _, _ in returns:
        if va not in row['visited'] or not any(i.address == va and i.mnemonic == 'ret' for body in bodies.values() for i in body):
            raise ValueError('font original return instruction')
    line = struct.unpack_from('<h', raw, 0x5FF6D8-BASE)[0]+3
    sizes = [80, 176] if mode == 'empty' else [80]
    allocations = [dict(va='0x56e810', return_va='0x428a73', sp=TOP-depth,
                        args=[size, 1, 0x594E28, line], pointer=ptr, bytes=size, initial_hex='cd'*size,
                        adapter='declared debug CRT allocation')
                   for ptr, size, depth in zip((FONT, CACHE), sizes, (532, 572))]
    if row['allocations'] != allocations:
        raise ValueError('font bounded CRT allocation inputs and lifetime')
    cache_calls = row['cache_calls']
    caps = None
    if mode == 'empty':
        ops = [('cache_addref', 4, 0x54875E, 712, [device]),
               ('cache_caps', 28, 0x54876E, 716, [device, TOP-700]),
               ('cache_creation', 36, 0x54877B, 716, [device, TOP-488])]
        if len(cache_calls) != 3:
            raise ValueError('font exact three actual cache device calls')
        for actual, (op, slot, ret, depth, args) in zip(cache_calls, ops):
            result = actual['result']
            if actual != dict(op=op, va=hex(objects['device']['methods'][str(slot)]), return_va=hex(ret),
                              sp=TOP-depth, args=args, request=dict(pointer=device), result=result,
                              live_host_observed=True):
                raise ValueError('font actual owned device method/ABI')
            if op == 'cache_addref':
                if result != dict(count=2):
                    raise ValueError('font exact new cache reference count')
            elif result['hr'] != 0:
                raise ValueError('font real cache queries must succeed')
        caps = bytes.fromhex(cache_calls[1]['result']['hex'])
        prior_caps = next(r['result']['hex'] for r in case['device']['native']['live_results'] if r['op'] == 'caps')
        creation = struct.pack('<4I', 0, 1, case['hello']['window'], 68).hex()
        if len(caps) != 212 or caps.hex() != prior_caps or cache_calls[2]['result']['hex'] != creation:
            raise ValueError('font complete actual device caps and creation parameters')
    elif cache_calls:
        raise ValueError('font inherited cache read cannot call device')
    expected_image = bytearray(image)
    counter = dword(image, COUNTER-BASE)+sum(sizes)
    store(expected_image, COUNTER-BASE, counter)
    if mode == 'empty':
        store(expected_image, HEAD-BASE, CACHE)
    verify_state(row['state'], owner, bytes(expected_image), TOP-108, objects.values())
    if len(row['heaps']) != 2:
        raise ValueError('font both full heap guard regions required')
    for r, ptr, size in zip(row['heaps'], (FONT, CACHE), (80, 176)):
        expected = bytearray(b'\xa5'*12288)
        if ptr == FONT:
            expected[4096:4096+size] = font_constructor(b'\xcd'*size)
        elif mode == 'empty':
            expected[4096:4096+size] = cache_prefix(b'\xcd'*size, device, caps)
        if r['pointer'] != ptr-4096:
            raise ValueError('font declared heap mapping')
        verify_buffer({k: v for k, v in r.items() if k != 'pointer'}, expected)
    if mode == 'inherited':
        expected_cpu = dict(EIP=0x548D95, ESP=TOP-456, EBP=TOP-408, EAX=source_contract()['inherited_head'],
                            EBX=TOP-228, ECX=FONT, EDX=counter, ESI=FONT, EDI=device, EFLAGS=2)
        pending = dict(va='0x548d95', first_instruction_executed=False, base=source_contract()['inherited_head'],
                       effective_address=source_contract()['inherited_head']+4, target_read=False, target_memory_mapped=False)
    else:
        expected_cpu = dict(EIP=0x52755E, ESP=TOP-776, EBP=TOP-712, EAX=CACHE+88,
                            EBX=CACHE+92, ECX=0, EDX=TOP-488, ESI=CACHE, EDI=CACHE+84,
                            EFLAGS=6 if dword(caps, 12) & 0x20000000 else 70)
        pending = dict(va='0x52755e', first_instruction_executed=False, return_va='0x5486a9',
                       sp=TOP-776, args=texture_arguments(device, caps))
    if row['cpu'] != expected_cpu or row['pending'] != pending:
        raise ValueError('font precise pending original CPU/stack/read boundary')
    if row['output_slot'] != dict(pointer=TOP-228, value=0xCCCCCCCC):
        raise ValueError('font factory output still unassigned')
    if any(row[k] is not False for k in ('font_initialization_complete', 'texture_body_executed', 'retained_VM_advanced')):
        raise ValueError('font factory completion authority')


def verify_trace(trace, calls, cleanup):
    expected = [dict(request=dict(id=i, op=op, **request), reply=dict(ok=True, id=i, result=result))
                for i, (op, request, result) in enumerate(calls, 1)]
    count = len(calls)+1
    expected.append(dict(request=dict(id=count, op='close'), reply=dict(ok=True, id=count, result=cleanup)))
    if trace != expected:
        raise ValueError('font full sequenced live platform trace')


def verify_report(report):
    mode = report['mode']
    if report['schema_version'] != 1 or mode not in STOPS or report['source_contract'] != source_contract():
        raise ValueError('font fixed source contract and experiment mode')
    for key in ('original_IAT_changed', 'game_helpers_stubbed', 'retained_VM_advanced', 'drawing_or_Present',
                'full_outer_frame', 'live_handles_resumable_after_cleanup'):
        if report[key] is not False:
            raise ValueError('font startup authority')
    if report['CRT_adapter_executed'] is not True:
        raise ValueError('font explicit CRT boundary required')
    for build, source, helper in ((report['device_build'], BRIDGE_SOURCE, HELPER),
                                  (report['platform_build'], PLATFORM_SOURCE, PLATFORM_HELPER)):
        if build != dict(source_sha256=sha(source.read_bytes()), helper_sha256=sha(helper.read_bytes()),
                         compiler_sha256=sha(COMPILER.read_bytes()), machine=machine(helper)) or machine(helper) != 0x14C:
            raise ValueError('font actual x86 helper build provenance')
    if [(c['fill'], c['hello']['width'], c['hello']['height']) for c in report['cases']] != [(0xA5, 640, 480), (0xCC, 1024, 768)]:
        raise ValueError('font declared cases')
    for case in report['cases']:
        if case['hello']['pointer_bytes'] != 4 or case['hello']['window_visible'] is not False or case['platform_hello']['pointer_bytes'] != 4:
            raise ValueError('font actual owned hidden x86 platform')
        owner, image = verify_constructor(case)
        owner, objects = verify_device(case, owner, image)
        verify_font(case, owner, image, objects)
        expected_owner = bytearray(owner)
        store(expected_owner, 0xB26C, case['font']['platform_calls'][0]['result']['result'])
        verify_factory(case, mode, bytes(expected_owner), image, objects)
        cleanup = dict(device_release_count=0, factory_release_count=0, window_destroyed=True, all_owned_resources_released=True)
        if mode == 'empty':
            cleanup['extra_reference_release_counts'] = [1]
        if case['device_cleanup'] != cleanup or case['platform_cleanup'] != dict(fonts_released=1, dcs_released=1, all_owned_resources_released=True):
            raise ValueError('font balanced live resource cleanup')
        device_calls = [(r['op'], r['request'], r['result']) for r in case['device']['native']['live_results']]
        device_calls += [(r['op'], r['request'], r['result']) for r in case['factory']['cache_calls']]
        verify_trace(case['device_trace'], device_calls, cleanup)
        platform_calls = case['constructor']['platform_calls']+case['font']['platform_calls']
        verify_trace(case['platform_trace'], [(r['name'], r['request'], r['result']) for r in platform_calls], case['platform_cleanup'])
        if len(case['refused_address_collisions']) > 5:
            raise ValueError('font bounded collision retry count')
        for refused in case['refused_address_collisions']:
            if (refused['error'] != 'live interface mapping collides with audit ownership'
                    or refused['cleanup']['all_owned_resources_released'] is not True
                    or refused['trace'][-1]['request']['op'] != 'close'
                    or refused['trace'][-1]['reply']['result'] != refused['cleanup']):
                raise ValueError('font refused address collision and cleanup')
    return dict(cases=2, mode=mode, full_owner_bytes=49152, heap_guard_bytes=24576,
                original_factory_calls=9 if mode == 'empty' else 5, retained_VM_advanced=False)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('report')
    args = parser.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/args.report).read_text(encoding='utf-8')))))
