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
    if row['root'] != hex(root) or row['receiver'] != MANAGER or row['args'] != list(args):
        raise ValueError('renderer evidence root call mismatch')
    if [int(e['va'], 16) for e in row['entries']] != entries:
        raise ValueError('renderer evidence original call sequence')
    if not row['visited'] or len(set(row['visited'])) != len(row['visited']):
        raise ValueError('renderer evidence native instruction set')
    image = SOURCE.read_bytes()
    for va in row['visited']:
        if not any(a <= va < FUNCTIONS[a] for a in (*entries, 0x56CE80)):
            raise ValueError('renderer evidence unrelated instruction')
    for e in row['entries']:
        ret = int(e['return_va'], 16)
        va = int(e['va'], 16)
        if ret == RETURN:
            if e != dict(va=hex(root), return_va=hex(RETURN), sp=TOP,
                         receiver=MANAGER, args=list(args)):
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


def verify_initialization(report):
    if (report.get('source_contract') != source_contract()
            or report.get('schema_version') != 1
            or report.get('isolated_experiments') is not True
            or any(report.get(k) is not False for k in
                   ('retained_VM_advanced', 'D3D_initialized', 'GPU_executed', 'full_outer_frame'))):
        raise ValueError('renderer evidence source/scope mismatch')
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


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('report')
    a = p.parse_args()
    print(json.dumps(verify_initialization(json.loads((ROOT/a.report).read_text(encoding='utf-8')))))
