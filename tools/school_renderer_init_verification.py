"""Independently check renderer prerequisite evidence against source projections."""
import base64
import json
import zlib

from tools.school_renderer_init import *
from tools.school_renderer_init_emulation import (
    OWNER, MANAGER, HEADS, ARENA, TOP, RETURN, COUNTER, digest,
)


def verify_buffer(row, expected):
    if set(row) != {'bytes', 'sha256', 'zlib_base64'} or row['bytes'] != len(expected):
        raise ValueError('renderer evidence buffer schema/length')
    dec = zlib.decompressobj()
    raw = dec.decompress(base64.b64decode(row['zlib_base64'], validate=True),
                         len(expected)+1)
    if (raw != expected or not dec.eof or dec.unused_data or dec.unconsumed_tail
            or row['sha256'] != digest(expected)):
        raise ValueError('renderer evidence full buffer mismatch')


def verify_state(row, manager, heads, arena, counter, inputs):
    if set(row) != {'manager_hex', 'heads', 'arena', 'counter',
                    'retained_image_sha256', 'retained_owner_sha256', 'guards_unchanged'}:
        raise ValueError('renderer evidence state schema')
    if row['manager_hex'] != manager.hex() or row['counter'] != u32(counter):
        raise ValueError('renderer evidence manager/counter mismatch')
    verify_buffer(row['heads'], heads)
    verify_buffer(row['arena'], arena)
    owner = bytearray([0xA5])*0xC000
    store(owner, 0xB210, inputs['device'])
    struct.pack_into('<2I', owner, 0xB278, *map(u32, inputs['dimensions']))
    struct.pack_into('<H', owner, 0xB28E, inputs['gate'])
    if (row['retained_image_sha256'] != SOURCE_SHA256
            or row['retained_owner_sha256'] != digest(owner)
            or row['guards_unchanged'] is not True):
        raise ValueError('renderer evidence unowned memory retention')


def verify_call(row, root, args, entries, returned=True):
    if row['root'] != hex(root) or row['receiver'] != MANAGER or row['args'] != list(map(u32, args)):
        raise ValueError('renderer evidence root call mismatch')
    if [int(e['va'], 16) for e in row['entries']] != entries:
        raise ValueError('renderer evidence original call sequence')
    if not row['visited'] or sorted(set(row['visited'])) != row['visited']:
        raise ValueError('renderer evidence native instruction set')
    image = SOURCE.read_bytes()
    decoder = Cs(CS_ARCH_X86, CS_MODE_32)
    boundaries = {i.address for a in (*entries, 0x56CE80)
                  for i in decoder.disasm(image[a-BASE:FUNCTIONS[a]-BASE], a)}
    for va in row['visited']:
        if va not in boundaries:
            raise ValueError('renderer evidence unrelated instruction')
    if any(a not in row['visited'] for a in entries):
        raise ValueError('renderer evidence missing native entry instruction')
    for e in row['entries']:
        ret = int(e['return_va'], 16)
        va = int(e['va'], 16)
        if ret == RETURN:
            if e != dict(va=hex(root), return_va=hex(RETURN), sp=TOP,
                         receiver=MANAGER, args=list(map(u32, args))):
                raise ValueError('renderer evidence declared root stack')
        else:
            op = image[ret-BASE-5:ret-BASE]
            if len(op) != 5 or op[0] != 0xE8 or ret+struct.unpack_from('<i', op, 1)[0] != va:
                raise ValueError('renderer evidence original E8 caller')
        if not TOP-1024 <= e['sp'] <= TOP:
            raise ValueError('renderer evidence bounded stack')
    if returned:
        cpu = row['cpu']
        if row['status'] != 'returned' or row['pending'] is not None:
            raise ValueError('renderer evidence natural return required')
        expected = dict(EIP=RETURN, ESP=TOP+4+len(args)*4,
                        EBP=0x11223344, EBX=0x55667788,
                        ESI=0x88776655, EDI=0x44332211)
        if any(cpu.get(k) != v for k, v in expected.items()):
            raise ValueError('renderer evidence CPU return/ABI')


def verify_scope(report):
    if (report.get('source_contract') != source_contract()
            or report.get('schema_version') != 1
            or report.get('isolated_experiments') is not True
            or any(report.get(k) is not False for k in
                   ('retained_VM_advanced', 'D3D_initialized', 'GPU_executed', 'full_outer_frame'))):
        raise ValueError('renderer evidence source/scope mismatch')


def verify_initialization(report):
    verify_scope(report)
    if len(report['cases']) != 2:
        raise ValueError('renderer initialization cases')
    counter = dword(SOURCE.read_bytes(), COUNTER-BASE)
    for case, device in zip(report['cases'], (0, 0x13572468)):
        inputs = dict(dimensions=[1024, 768], device=device, gate=1, owner=OWNER,
                      manager=MANAGER, heads=HEADS, arena=ARENA,
                      explicitly_declared_scratch_state=True)
        if case['inputs'] != inputs or [r['stage'] for r in case['stages']] != ['constructor', 'bind', 'queues']:
            raise ValueError('renderer explicit scratch inputs/stages')
        manager = constructor(bytes([0xA5])*96)
        stages = case['stages']
        heads = bytes([0xCD])*(LAYER_COUNT*8)
        arena = bytes([0xCD])*ARENA_BYTES
        verify_state(stages[0]['state'], manager, heads, arena, counter, inputs)
        verify_call(stages[0]['call'], 0x40D7E0, (), [0x40D7E0, 0x4107B0])
        manager = bind(manager, OWNER, device)
        verify_state(stages[1]['state'], manager, heads, arena, counter, inputs)
        verify_call(stages[1]['call'], 0x40D970, (OWNER,), [0x40D970, 0x4142B0])
        if stages[1]['call']['entries'][1]['receiver'] != OWNER:
            raise ValueError('renderer getter owner receiver')
        manager = initialize_queues(manager, HEADS, ARENA)
        verify_state(stages[2]['state'], manager, bytes(LAYER_COUNT*8), bytes(ARENA_BYTES),
                     counter+LAYER_COUNT*8+ARENA_BYTES, inputs)
        verify_call(stages[2]['call'], 0x40DAB0, (),
                    [0x40DAB0, 0x40DB10, 0x428A40, 0x40DB90, 0x56CEC0,
                     0x40DBF0, 0x428A40, 0x56CEC0, 0x40DC80])
        if [r['call']['cpu']['EAX'] for r in stages] != [MANAGER, 0, 0]:
            raise ValueError('renderer original return values')
        expected_calls = [(MANAGER, [4096]), (4096, [32768]),
                          (MANAGER, []), (HEADS, [HEADS, 0, 32768]),
                          (MANAGER, [ARENA_BYTES]), (ARENA_BYTES, [ARENA_BYTES]),
                          (ARENA, [ARENA, 0, ARENA_BYTES]), (MANAGER, [])]
        if [(r['receiver'], r['args']) for r in stages[2]['call']['entries'][1:]] != expected_calls:
            raise ValueError('renderer queue original arguments')
        line = struct.unpack_from('<h', SOURCE.read_bytes(), 0x5FF6D8-BASE)[0]+3
        expected_allocations = [dict(va='0x56e810', return_va='0x428a73',
                                     args=[size, 1, 0x594E28, line], result=pointer,
                                     adapter='declared debug CRT allocation')
                                for size, pointer in ((32768, HEADS), (ARENA_BYTES, ARENA))]
        if case['allocations'] != expected_allocations:
            raise ValueError('renderer bounded CRT response declaration')
    return dict(cases=2, full_manager_bytes=96, full_layer_bytes=32768,
                full_arena_bytes=ARENA_BYTES, isolated_only=True)


def entry(va, ret, sp, receiver, args):
    return dict(va=hex(va), return_va=hex(ret), sp=sp, receiver=receiver,
                args=list(map(u32, args)))


def clip_entries(rect, dimensions, sp=TOP, ret=RETURN):
    x, y, width, height = rect
    result = [entry(0x40E2A0, ret, sp, MANAGER, rect),
              entry(0x56DB00, 0x40E2F0, sp-108, OWNER, (x,))]
    if i32(abs(i32(x))) <= i32(dimensions[0]+i32(width)):
        result.append(entry(0x56DB00, 0x40E306, sp-108,
                            u32(dimensions[0]+i32(width)), (y,)))
    return result


def verify_debug(call, closed_gate=False):
    verify_call(call, 0x40DCD0, (4,), [0x40DCD0], returned=False)
    image = SOURCE.read_bytes()
    line = struct.unpack_from('<h', image, 0x5FF34C-BASE)[0]+(4 if closed_gate else 44)
    ret = 0x40DD1A if closed_gate else 0x40DE74
    expected = dict(va='0x424f80', return_va=hex(ret), sp=TOP-112,
                    args=[0x592BF0 if closed_gate else 0x5924D4, 0x592BBC, line, 0],
                    instruction_executed=False)
    if call['status'] != 'unexecuted_debug' or call['pending'] != expected:
        raise ValueError('renderer unexecuted debug caller/arguments')
    cpu = call['cpu']
    wanted = dict(EIP=0x424F80, ESP=TOP-112, EBP=TOP-4, EAX=line,
                  EBX=0x55667788, ECX=OWNER if closed_gate else 3,
                  EDX=0 if closed_gate else 1, ESI=0x88776655, EDI=TOP-4, EFLAGS=2)
    if cpu != wanted:
        raise ValueError('renderer original debug admission CPU')
    if any(va >= ret for va in call['visited']):
        raise ValueError('renderer instruction after unexecuted debug call')


def verify_queue(report):
    verify_scope(report)
    inputs = dict(dimensions=[1024, 768], device=0x13572468, gate=1, owner=OWNER,
                  manager=MANAGER, heads=HEADS, arena=ARENA,
                  explicitly_declared_scratch_state=True)
    if report['inputs'] != inputs or len(report['insertions']) != len(RECTANGLE_PROBES):
        raise ValueError('renderer queue declared inputs/insertion count')
    manager = bytearray(initialize_queues(bind(constructor(bytes([0xA5])*96),
                                             OWNER, inputs['device']), HEADS, ARENA))
    heads, arena = bytearray(LAYER_COUNT*8), bytearray(ARENA_BYTES)
    counter = dword(SOURCE.read_bytes(), COUNTER-BASE)+LAYER_COUNT*8+ARENA_BYTES
    for row, (rect, layer, color, blend) in zip(report['insertions'], RECTANGLE_PROBES):
        args = (*rect, layer, color, blend)
        call = row['call']
        entries = [entry(0x410310, RETURN, TOP, MANAGER, args)]
        entries += clip_entries(rect, inputs['dimensions'], TOP-108, 0x410345)
        pointer = dword(manager, 0x30)
        index = layer & 65535
        old = dword(heads, index*8)
        entries += [entry(0x40DCD0, 0x410362, TOP-96, MANAGER, (4,)),
                    entry(0x40DF20, 0x4103CE, TOP-100, MANAGER, (pointer, index))]
        verify_call(call, 0x410310, args, [int(e['va'], 16) for e in entries])
        if call['entries'] != entries or call['cpu']['EAX'] != 0:
            raise ValueError('renderer rectangle original arguments/stack/return')
        if row['packet_pointer'] != pointer or row['previous_head'] != old:
            raise ValueError('renderer rectangle linked head')
        offset = pointer-ARENA
        arena[offset:offset+24] = rectangle_packet(arena[offset:offset+24], rect,
                                                 layer, color, blend, old)
        store(heads, index*8, pointer)
        store(manager, 0x30, pointer+24)
        store(manager, 0x1C, offset+24)
        verify_state(row['state'], manager, heads, arena, counter, inputs)
    row = report['clipped_rectangle']
    args = (2000, 0, 1, 1, 67, 0x223438, 1)
    entries = [entry(0x410310, RETURN, TOP, MANAGER, args)]
    entries += clip_entries(args[:4], inputs['dimensions'], TOP-108, 0x410345)
    verify_call(row['call'], 0x410310, args, [int(e['va'], 16) for e in entries])
    if row['call']['entries'] != entries or row['call']['cpu']['EAX'] != 0:
        raise ValueError('renderer rejected rectangle must skip allocation')
    verify_state(row['state'], manager, heads, arena, counter, inputs)
    row = report['reset_heads']
    verify_call(row['call'], 0x40DB90, (), [0x40DB90, 0x56CEC0])
    expected = [entry(0x40DB90, RETURN, TOP, MANAGER, ()),
                entry(0x56CEC0, 0x40DBD5, TOP-100, HEADS, (HEADS, 0, 32768))]
    if row['call']['entries'] != expected or row['call']['cpu']['EAX'] != 0:
        raise ValueError('renderer head reset original call')
    heads[:] = bytes(len(heads))
    verify_state(row['state'], manager, heads, arena, counter, inputs)
    row = report['reset_arena']
    verify_call(row['call'], 0x40DC80, (), [0x40DC80])
    if row['call']['cpu']['EAX'] != 0:
        raise ValueError('renderer arena reset return')
    store(manager, 0x30, ARENA)
    store(manager, 0x2C, 0)
    verify_state(row['state'], manager, heads, arena, counter, inputs)
    if len(report['clip_probes']) != len(CLIP_PROBES):
        raise ValueError('renderer clip probe count')
    for row, rect in zip(report['clip_probes'], CLIP_PROBES):
        expected = clip(rect, inputs['dimensions'])
        entries = clip_entries(rect, inputs['dimensions'])
        verify_call(row['call'], 0x40E2A0, rect, [int(e['va'], 16) for e in entries])
        if (row['expected'] != expected or row['call']['cpu']['EAX'] != expected
                or row['call']['entries'] != entries):
            raise ValueError('renderer signed clip expected value/branch')
        verify_state(row['state'], manager, heads, arena, counter, inputs)
    clean = initialize_queues(bind(constructor(bytes([0xA5])*96), OWNER,
                                   inputs['device']), HEADS, ARENA)
    if len(report['capacity_probes']) != 3:
        raise ValueError('renderer capacity probe count')
    for row, remaining in zip(report['capacity_probes'], (25, 24, 23)):
        pointer = ARENA+ARENA_BYTES-remaining
        pm = bytearray(clean)
        store(pm, 0x30, pointer)
        if row['declared_remaining_bytes'] != remaining or row['declared_cursor'] != pointer:
            raise ValueError('renderer declared capacity probe')
        if remaining > 24:
            verify_call(row['call'], 0x40DCD0, (4,), [0x40DCD0])
            if row['call']['cpu']['EAX'] != pointer:
                raise ValueError('renderer capacity admission pointer')
        else:
            verify_debug(row['call'])
        verify_state(row['state'], pm, bytes(LAYER_COUNT*8), bytes(ARENA_BYTES), counter, inputs)
    row = report['closed_gate']
    if row['inputs'] != dict(inputs, gate=0):
        raise ValueError('renderer closed gate input declaration')
    verify_debug(row['call'], closed_gate=True)
    verify_state(row['state'], clean, bytes(LAYER_COUNT*8), bytes(ARENA_BYTES),
                 counter, row['inputs'])
    return dict(rectangles=4, clip_probes=12, capacity_probes=3, resets=2,
                debug_bodies_executed=0, isolated_only=True)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('report')
    p.add_argument('--queue', action='store_true')
    a = p.parse_args()
    report = json.loads((ROOT/a.report).read_text(encoding='utf-8'))
    print(json.dumps(verify_queue(report) if a.queue else verify_initialization(report)))
