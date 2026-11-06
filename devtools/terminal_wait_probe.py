"""Authenticated guest-only wait diagnostic. Never restores a native owner.

The completed parent proof is authenticated, not replayed. The tiny tail is
executed twice from that exact diagnostic RAM, stopping BEFORE the first OS
call. This is intentionally not a new functional acceptance or native resume.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
from pathlib import Path
import struct
import time

ROOT = Path(__file__).resolve().parents[1]
CASES = (
    ('neutral', 'v10', '0ee7bdb3d00d9bf9bce2ac0818297b382eff51f511725fd7be620712c6297f40'),
    ('timeout', 'v8', 'dafc3c9e4edd3b380e4546837b21230c1c256c3f34f68cef3017af4a3ca86c05'),
)
WAIT = 0x422360
FIRST_OS_CALL = 0x4223A8
STACK = 0x12000000
MAIN = 0x12A00000
RANGES = ((0x422360, 0x422434), (0x422560, 0x42260A))


def need(value, message):
    if not value:
        raise ValueError(message)


def identity(path):
    path = Path(path)
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1048576), b''):
            h.update(block)
    return dict(path=path.relative_to(ROOT).as_posix(), bytes=path.stat().st_size,
                sha256=h.hexdigest())


def compact_regions(regions):
    compact = []
    for a, b, permission in regions:
        need(a % 4096 == 0 and (b+1) % 4096 == 0 and a <= b
             and (not compact or a > compact[-1][1]), 'ordered page-aligned regions')
        if compact and compact[-1][1]+1 == a and compact[-1][2] == permission:
            compact[-1][1] = b
        else:
            compact.append([a, b, permission])
    return compact


class PartitionView:
    """Keep the parent's partition hash after equivalent physical map grouping.

    Every actual mapped byte and page permission must have the same coverage.
    The original partition is retained solely for comparing the frozen digest;
    this changes no emulated address, bytes, permissions, CPU or instruction.
    """
    def __init__(self, uc, partition):
        self.uc, self.partition = uc, partition

    def mem_regions(self):
        need(compact_regions(self.uc.mem_regions()) == compact_regions(self.partition),
             'actual Unicorn byte coverage and every page permission equal source partition')
        return iter(self.partition)

    def mem_read(self, address, size):
        return self.uc.mem_read(address, size)


def topology_at_wait(execution):
    pages = {}

    def update(kind, address, size, permission=None):
        need(type(address) is int and type(size) is int and address >= 0
             and address % 4096 == size % 4096 == 0 and size > 0
             and address+size <= 0x100000000, 'aligned bounded topology extent')
        if kind != 'mem_unmap':
            need(type(permission) is int and 0 <= permission <= 7, 'valid page permissions')
        for page in range(address, address+size, 4096):
            need((page not in pages) if kind == 'mem_map' else (page in pages),
                 'topology page ownership: '+kind)
            if kind == 'mem_unmap':
                del pages[page]
            else:
                pages[page] = permission

    for a, b, permission in execution['initial_regions']:
        update('mem_map', a, b-a+1, permission)

    def topology(actions):
        for a in actions:
            if a['kind'] in ('mem_map', 'mem_protect'):
                update(a['kind'], a['address'], a['bytes'], a['permission'])
            elif a['kind'] == 'mem_unmap':
                update(a['kind'], a['address'], a['bytes'])

    for ordinal, tx in enumerate(execution['transactions']):
        topology(tx['driver'])
        for i, event in enumerate(tx['events']):
            topology(event['effects'])
            if event['pc'] == WAIT:
                need(i == len(tx['events'])-1 and event['stop'] is True
                     and event['continues_guest'] is False and not event['effects']
                     and not event['CPU_changes'], 'exact untouched parent wait stop')
                return ordinal, tx, pages
    raise ValueError('missing authenticated parent wait transaction')


def restore(row, source, progress=None):
    from unicorn import Uc, UC_ARCH_X86, UC_MODE_32
    from unicorn import x86_const as x86
    from tools.terminal_unit_frontends_trace import CPU_REGISTERS, MemoryDigest

    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    ordinal, tx, pages = topology_at_wait(row['unit_frontends']['execution'])
    if progress: progress('topology reconstructed')
    memory = row['forward_memory']
    previous_end = -1
    partition = []
    for capture in memory:
        a, size = capture['pointer'], capture['bytes']
        need(a > previous_end and a % 4096 == size % 4096 == 0 and size > 0,
             'ordered disjoint aligned forward memory regions')
        permission = pages.get(a)
        need(permission is not None and all(pages.get(p) == permission for p in range(a, a+size, 4096)),
             'forward region matches all reconstructed page permissions')
        partition.append((a, a+size-1, permission))
        for p in range(a, a+size, 4096):
            del pages[p]
        previous_end = a+size-1
    need(not pages, 'all authenticated forward memory regions')
    for a, b, permission in compact_regions(partition):
        uc.mem_map(a, b-a+1, permission)
    uc._wait_partition = partition
    regions = list(PartitionView(uc, partition).mem_regions())
    need(len(regions) == len(memory), 'all authenticated forward memory regions')
    for (a, b, _permission), capture in zip(regions, memory):
        raw = bytes.fromhex(capture['hex'])
        need((capture['pointer'], capture['bytes'], len(raw)) == (a, b-a+1, b-a+1),
             'exact forward memory extent')
        uc.mem_write(a, raw)
    if progress: progress('all forward bytes restored')
    expected = row['forward_CPU']
    need(set(expected) == set(CPU_REGISTERS) and expected == tx['after_CPU']
         and expected['EIP'] == WAIT and expected['ECX'] == source.previous.TASK,
         'complete parent CPU at the untouched wait target')
    for name, value in expected.items():
        reg = getattr(x86, 'UC_X86_REG_'+name)
        value = tuple(value) if isinstance(value, list) else value
        if uc.reg_read(reg) != value:
            uc.reg_write(reg, value)
    need(cpu(uc) == expected, 'all57 restored architectural registers')
    if progress: progress('all57 registers restored')
    need(MemoryDigest(PartitionView(uc, partition)).capture() == tx['after_memory'],
         'entire diagnostic RAM and permissions match authenticated wait transaction')
    if progress: progress('all RAM/permissions authenticated')
    need(bytes(uc.mem_read(STACK, 0x20000)).hex() == row['frontier']['stack_hex'],
         'whole authenticated scene stack')
    return uc, dict(transaction=ordinal, memory=tx['after_memory'], trace=tx['after_trace'],
                    source_regions=len(partition), diagnostic_regions=len(list(uc.mem_regions())),
                    mapping_representation='adjacent equal-permission regions merged; source partition retained for hash',
                    all_actual_bytes_and_permissions_preserved=True)


def cpu(uc):
    from unicorn import x86_const as x86
    from tools.terminal_unit_frontends_trace import CPU_REGISTERS
    out = {}
    for name in CPU_REGISTERS:
        value = uc.reg_read(getattr(x86, 'UC_X86_REG_'+name))
        out[name] = list(value) if isinstance(value, tuple) else value
    return out


def word(uc, address):
    return struct.unpack('<I', uc.mem_read(address, 4))[0]


def fields(uc, task, ctrl):
    sp = cpu(uc)['ESP']
    return dict(task=task, task_header_hex=bytes(uc.mem_read(task, 0x30)).hex(),
                flags=word(uc, task+4), scheduler=word(uc, task+8),
                delay=word(uc, task+0x14), event=word(uc, task+0x1C),
                thread=word(uc, task+0x20), thread_id=word(uc, task+0x24),
                original_MAIN_scheduler=MAIN+0x64,
                original_MAIN_scheduler_hex=bytes(uc.mem_read(MAIN+0x64, 0x120)).hex(),
                stack_top_hex=bytes(uc.mem_read(sp, 32)).hex(),
                pending_scene_result=word(uc, STACK+0xF000-12),
                replay_record_enabled=bytes(uc.mem_read(ctrl+0x117C3C, 1)).hex())


def probe(row, source, progress=None):
    from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
    from unicorn import x86_const as x86
    from tools.terminal_unit_frontends_trace import MemoryDigest, TraceCount

    uc, parent = restore(row, source, progress)
    task, ctrl = source.previous.TASK, source.previous.CTRL
    memory, count = MemoryDigest(PartitionView(uc, uc._wait_partition)), TraceCount()
    before_cpu, before_fields = cpu(uc), fields(uc, task, ctrl)
    before_memory = memory.capture()
    instructions, writes, stop = [], [], []

    def code(_uc, pc, size, _context):
        need(any(a <= pc and pc+size <= b for a, b in RANGES),
             'diagnostic remains inside exact original wait/flag bodies')
        raw = bytes(uc.mem_read(pc, size))
        need(raw == source.previous.CODE[pc-0x400000:pc-0x400000+size]
             and raw[0] != 0xCC, 'unmodified original instructions')
        if pc == FIRST_OS_CALL:
            sp = uc.reg_read(x86.UC_X86_REG_ESP)
            stop.append(dict(kind='unowned_scheduler_critical_section', PC=pc,
                             instruction_hex=raw.hex(), import_slot=0x592234,
                             import_target=word(uc, 0x592234),
                             args=[word(uc, sp)], instruction_executed=False,
                             native_API_called=False))
            uc.emu_stop()
            return
        need(count.instructions < 4096, 'bounded tail instruction budget')
        instructions.append(dict(PC=pc, hex=raw.hex()))
        count.instruction(pc)

    def write(_uc, _access, address, size, value, _context):
        need(STACK <= address and address+size <= STACK+0x20000
             or task+4 <= address and address+size <= task+8
             or task+0x14 <= address and address+size <= task+0x18,
             'wait writes only its real stack/flags/delay')
        pc = uc.reg_read(x86.UC_X86_REG_EIP)
        writes.append(dict(PC=pc, address=address, bytes=size,
                           before_hex=bytes(uc.mem_read(address, size)).hex(),
                           value=value & ((1 << (8*size))-1)))
        memory.write(address, size)
        count.write(pc, address, size, value)

    uc.hook_add(UC_HOOK_CODE, code)
    uc.hook_add(UC_HOOK_MEM_WRITE, write)
    uc.emu_start(WAIT, 0, timeout=0, count=0)
    if progress: progress('original tail stopped before first OS call')
    need(len(stop) == 1 and cpu(uc)['EIP'] == FIRST_OS_CALL,
         'exact first unsupported current OS boundary')
    need(before_fields['scheduler'] == before_fields['event'] == before_fields['thread']
         == before_fields['thread_id'] == 0 and stop[0]['args'] == [0x100],
         'observed current fixture has no scheduler/event/worker owner')
    return dict(parent=parent, before_CPU=before_cpu, before_memory=before_memory,
                before_fields=before_fields, instructions=instructions, writes=writes,
                trace=count.mark(), after_CPU=cpu(uc), after_memory=memory.capture(),
                after_fields=fields(uc, task, ctrl), frontier=stop[0],
                wait_body_prefix_executed=True, wait_body_completed=False,
                outer_result_consumed=False, complete_battle_exit=False,
                native_execution=False, native_handles_restored_as_live=False)


def run(index):
    from tools import terminal_unit_frontends_proof as frozen
    from tools import terminal_unit_frontends_corpus as corpus
    from tools import terminal_unit_frontends_emulation as source
    name, version, checkpoint_sha = CASES[index]
    prefix = ROOT/('analysis/terminal-unit-frontends-source-v6-'+name+'-20261105')
    checkpoint = ROOT/('analysis/terminal-unit-frontends-proof-'+version+'-'+name+'-20261105.json')
    started = time.monotonic()
    data, process = frozen.authenticate_source(prefix)
    print('authenticated source', name, flush=True)
    row = corpus.read_case(prefix, index)
    proof, resumed = frozen.resume_source_proof(checkpoint, checkpoint_sha, data, process, row, index)
    print('authenticated parent full proof; bounded guest-only tail', name, flush=True)
    print('forward regions', len(row['forward_memory']), 'bytes',
          sum(r['bytes'] for r in row['forward_memory']), flush=True)
    # Keep the authenticated tree explicitly alive during diagnostic execution;
    # defer unrelated cyclic collection until after the tiny tail.
    was_enabled = gc.isenabled()
    gc.disable()
    def progress(stage):
        print(name, stage, round(time.monotonic()-started, 3), flush=True)
    try:
        first, second = probe(row, source, progress), probe(row, source, progress)
    finally:
        if was_enabled:
            gc.enable()
    need(first == second, 'two diagnostic executions have identical full CPU/RAM/trace/observations')
    return dict(schema_version=1, kind='authenticated_guest_only_wait_diagnostic',
                accepted=False, case_index=index, case_name=row['input']['name'],
                source_process=process, source_artifacts=data['artifacts'],
                reused_parent_proof=resumed, parent_proof_full_state_checked=proof[
                    'complete_CPU_and_mapped_memory_compared_at_every_transaction'],
                implementation=identity(Path(__file__)), original=identity(source.previous.overlay.SOURCE),
                result=first, identical_second_execution=True,
                independent_platform_proof=False, fresh_native_lifetime=False,
                historical_case_tree_loaded=False, source_v6_decoded_once=True,
                duration_seconds=round(time.monotonic()-started, 3))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', type=int, choices=(0, 1), required=True)
    parser.add_argument('--out', required=True)
    args = parser.parse_args()
    path = Path(args.out).resolve()
    need(path.is_relative_to(ROOT/'analysis') and not path.exists(), 'fresh owned analysis report')
    result = run(args.case)
    encoded = json.dumps(result, ensure_ascii=False, indent=2).encode('utf8')+b'\n'
    need(len(encoded) < 1024*1024, 'bounded small diagnostic report')
    with path.open('xb') as stream:
        stream.write(encoded)
    print(json.dumps(identity(path)), flush=True)


if __name__ == '__main__':
    main()
