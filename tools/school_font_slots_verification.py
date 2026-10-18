"""Independent source, native constructor, live caps and complete-memory checks."""
import json
import struct
from copy import deepcopy
from tools.school_font_slots import *
from tools.school_font_cache import source_contract as cache_contract, FONT, COUNTER
from tools.school_font_cache_verification import verify_report as verify_cache
from tools.school_font_startup_verification import verify_trace
from tools.school_device_init_verification import unpack
from tools.school_font_slots_emulation import OWNER, TOP
from tools.school_renderer_init_verification import verify_buffer


def verify_stage(case, phase):
    row = case['slot_constructor' if phase == 'constructor' else 'atlas_admission']
    prior = case['font_return'] if phase == 'constructor' else case['slot_constructor']
    device = dword(unpack(case['font_return']['state']['owner']), 0xB210)
    if row['phase'] != phase or row['before_cpu'] != prior['cpu']:
        raise ValueError('font slots same original CPU continuation')
    entries = [(0x428A40, 0x416047, 216, 0, [SIZE]),
               (0x401000, 0x416083, 224, SLOT, [0x592CA4, 12, 1]),
               (0x56CD90, 0x40102A, 320, SLOT, [SLOT, 0x592CA4])] if phase == 'constructor' else [
               (0x4010D0, 0x4160DF, 216, SLOT, [device])]
    if row['entries'] != [dict(va=hex(a), return_va=hex(b), sp=TOP-d, receiver=c, args=args) for a, b, d, c, args in entries]:
        raise ValueError('font slots native constructor/caps entry ABI')
    raw, md = SOURCE.read_bytes(), Cs(CS_ARCH_X86, CS_MODE_32)
    for a, b, *_ in entries:
        i = next(md.disasm(raw[b-BASE-5:b-BASE], b-5))
        if i.mnemonic != 'call' or int(i.op_str, 16) != a:
            raise ValueError('font slots original direct caller source')
    returns = [(0x56CE82, 0x428AC2, 224), (0x428AC5, 0x416047, 216),
               (0x56CE7F, 0x40102A, 320), (0x56CE82, 0x401087, 232),
               (0x40108A, 0x416083, 224)] if phase == 'constructor' else [(0x56CE82, 0x40117A, 720)]
    expected_returns = [dict(va=hex(a), return_va=hex(b), sp=TOP-d, eax=SLOT if phase == 'constructor' else 0) for a, b, d in returns]
    if row['returns'] != expected_returns:
        raise ValueError('font slots native copy/constructor/stack-check returns')
    instructions = [i for a, b in RANGES.items() for i in md.disasm(raw[a-BASE:b-BASE], a)]
    valid = {i.address for i in instructions}
    required = ({0x416021, 0x41603D, 0x41605D, 0x416068, 0x416073, 0x4160A5, 0x4160DA,
                 0x401025, 0x401033, 0x40103C, 0x401042, 0x40104C, 0x401056, 0x401060,
                 0x40106D, 0x56CD90, 0x56CE01, 0x56CE21, 0x56CE78}
                if phase == 'constructor' else {0x4010D0, 0x4010F9, 0x4010FF, 0x401147, 0x401151,
                 0x401170, 0x401180, 0x4011DE, 0x4011E9, 0x40120B})
    visited = set(row['visited'])
    stop = 0x4010D0 if phase == 'constructor' else 0x40120C
    if row['visited'] != sorted(visited) or not required <= visited or not visited <= valid or stop in visited:
        raise ValueError('font slots executed original bodies and unexecuted boundary')
    if any(a not in visited or next(i for i in instructions if i.address == a).mnemonic != 'ret' for a, *_ in returns):
        raise ValueError('font slots original return instructions')
    expected_allocations = [dict(va='0x56e810', return_va='0x428a73', sp=TOP-320,
        args=[SIZE, 1, 0x594E28, struct.unpack_from('<h', raw, 0x5FF6D8-BASE)[0]+3], pointer=SLOT,
        bytes=SIZE, initial_hex='cd'*SIZE, adapter='declared debug CRT allocation')] if phase == 'constructor' else []
    if row['allocations'] != expected_allocations:
        raise ValueError('font slots exact bounded original CRT allocation')
    value = constructor(b'\xcd'*SIZE)
    calls = row['api_calls']
    if phase == 'constructor':
        if calls: raise ValueError('font slots constructor has no new platform calls')
        cpu = dict(EIP=stop, ESP=TOP-216, EBP=TOP-96, EAX=device, EBX=0x55667788, ECX=SLOT,
                   EDX=OWNER, ESI=TOP-208, EDI=TOP-108, EFLAGS=6)
        pending = dict(va=hex(stop), sp=TOP-216, first_instruction_executed=False,
                       return_va='0x4160df', args=[device], receiver=SLOT)
    else:
        if len(calls) != 1: raise ValueError('font slots exactly one live caps query')
        caps = case['factory']['cache_calls'][1]['result']['hex']
        # Every method address is source-mapped to the same owned device by the parent.
        method = case['sprite']['device_calls'][1]['va']
        if calls[0] != dict(op='caps', va=method, return_va='0x401173', sp=TOP-728,
                args=[device, TOP-440], request=dict(pointer=device), result=dict(hr=0, hex=caps), live_host_observed=True):
            raise ValueError('font slots actual caps buffer/method/ABI')
        maximum = dword(bytes.fromhex(caps), 88)
        if maximum < 256:
            raise ValueError('font slots fixed accepted live unscaled case prerequisite')
        value = atlas(value, device, maximum)
        # CreateTexture method comes from the preceding real native texture call.
        texture_target = int(case['texture']['api_calls'][-2]['va'], 16)
        cpu = dict(EIP=stop, ESP=TOP-748, EBP=TOP-220, EAX=device, EBX=0x55667788,
                   ECX=device, EDX=0, ESI=TOP-716, EDI=TOP-220, EFLAGS=6)
        # EDX holds the actual device vtable, obtained from its original foreign map.
        from tools.school_device_init_verification import unpack as buffer
        maps = case['font_return']['state']['foreign_maps']
        pointer_page = next(r for r in maps if r['pointer'] <= device < r['pointer']+4096)
        cpu['EDX'] = dword(buffer(pointer_page), device-pointer_page['pointer'])
        pending = dict(va=hex(stop), sp=TOP-748, first_instruction_executed=False,
                       method_target=texture_target, args=[device, 256, 256, 1, 0, 26, 1, SLOT+0x5C], platform_call_executed=False)
    if row['cpu'] != cpu or row['pending'] != pending:
        raise ValueError('font slots exact pending CPU and original resource arguments')
    owner = bytearray(unpack(case['font_return']['state']['owner']))
    store(owner, 0x1090, SLOT)
    verify_buffer(row['state']['owner'], owner)
    from tools.school_owner_startup_verification import verify_constructor
    _, image = verify_constructor(case)
    image = bytearray(image)
    store(image, COUNTER-BASE, dword(image, COUNTER-BASE)+288+SIZE)
    from tools.school_font_cache import CACHE, HEAD
    store(image, HEAD-BASE, CACHE)
    if row['state']['image_sha256'] != hashlib.sha256(image).hexdigest() or row['state']['SEH'] != TOP-108 or row['state']['stack_guards_unchanged'] is not True:
        raise ValueError('font slots full original image/SEH/stack retention')
    if row['state']['foreign_maps'] != case['font_return']['state']['foreign_maps'] or row['heaps'] != case['font_return']['heaps']:
        raise ValueError('font slots retained complete parent heaps/foreign maps')
    expected = bytearray(b'\xa5'*12288)
    expected[4096:4096+SIZE] = value
    if row['slot_heap']['pointer'] != SLOT-4096:
        raise ValueError('font slots declared guarded object address')
    verify_buffer({k: v for k, v in row['slot_heap'].items() if k != 'pointer'}, expected)
    if row['native_CRT_face_copy_executed'] is not (phase == 'constructor') or row['first_slot_bound'] is not True:
        raise ValueError('font slots actual native construction and binding authority')
    if any(row[k] is not False for k in ('second_slot_bound', 'atlas_texture_created', 'additional_fonts_completed',
             'full415F50_returned', 'state_blocks_created', 'retained_VM_advanced')):
        raise ValueError('font slots unresolved completion boundary')


def verify_report(report):
    phase = report['phase']
    if report['schema_version'] != 1 or phase not in ('constructor', 'atlas') or report['source_contract'] != source_contract():
        raise ValueError('font slots fixed source contract')
    prefix = deepcopy(report)
    prefix['source_contract'], prefix['phase'] = cache_contract(), 'font'
    for case in report['cases']:
        calls = (case['device']['native']['live_results']+case['factory']['cache_calls']+
                 case['requirements']['api_calls']+case['texture']['api_calls']+
                 case['sprite']['device_calls']+case['font_return']['device_calls'])
        extra = case['atlas_admission']['api_calls'] if phase == 'atlas' else []
        verify_trace(case['device_trace'], [(r['op'], r['request'], r['result']) for r in calls+extra], case['device_cleanup'])
    # Validate the immutable parent with its exact request prefix; validate the real
    # longer sequence above, including its untouched final close id and cleanup.
    for case in prefix['cases']:
        if phase == 'atlas':
            case['device_trace'] = case['device_trace'][:-2]+[dict(request=dict(id=len(case['device_trace'])-1, op='close'),
                reply=dict(ok=True, id=len(case['device_trace'])-1, result=case['device_cleanup']))]
    verify_cache(prefix)
    for case in report['cases']:
        verify_stage(case, 'constructor')
        if phase == 'atlas': verify_stage(case, 'atlas')
    return dict(cases=2, phase=phase, first_additional_slot_constructed=True,
                full_slot_bytes=1656, heap_guard_bytes=49152, real_caps_queried=phase == 'atlas',
                atlas_texture_created=False, retained_VM_advanced=False)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('report')
    a = p.parse_args()
    print(json.dumps(verify_report(json.loads((ROOT/a.report).read_text(encoding='utf-8')))))
