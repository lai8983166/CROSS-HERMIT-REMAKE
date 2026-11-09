"""Conditional sparse-byte replay of one retained battle result tail, never acceptance.

No native execution or handle restoration. The pending WOW64 context is not a
post-syscall context: its existing EAX merely equals the separately observed
ETW status. OS wrapper bytes are a matching disk-image candidate, not live
authenticated code. Unknown reads stop BEFORE the instruction executes.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import struct

WINDOW_SHA = '9874fb2e589aafb1b3190c9a2a5aac7c7ee0e0a3179923cd10d463bee3fd680e'
PROOF_SHA = '72f66232fc2f0ee016115f3948f2bbc1f9ab666a52e154674b661c529653fc41'
IMAGE_SHA = '588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005'
DLL_SHA = '254d4a108d9873dd9b01ed9083cf1075951ee814739a9403db1fe6081715d5ca'
SNAPSHOT_SHA = 'c2566fcb100f0d078c047851196d6fbf5f0d10f0adb5d0dcd924c726f572a6b3'
CONTEXT_SHA = '621560ca232b816f0b61d5d40ff081c7e43c3f098e14cc4774aa614a54ea24b3'
INDEX = 15
EXCLUDED = (213, 239, 383, 419)
GDT = 0x10000
LIMIT = 4096
MEMORY_LIMIT = 1024 * 1024
REPORT_LIMIT = 256 * 1024
INTEGER_OFFSETS = dict(EDI=156, ESI=160, EBX=164, EDX=168, ECX=172,
                       EAX=176, EBP=180, EIP=184, EFLAGS=192, ESP=196)
SEGMENT_OFFSETS = dict(GS=140, FS=144, ES=148, DS=152, CS=188, SS=200)
WRAPPER_RANGES = ((0x77B68229, 0x77B6825C), (0x77B68298, 0x77B6829D),
                  (0x77B68182, 0x77B68186))
GAME_RANGES = ((0x422360, 0x422434), (0x422560, 0x4225DA),
               (0x56CE80, 0x56CE98), (0x4539B0, 0x453CFC),
               (0x451A60, 0x451B0F), (0x451670, 0x4519A3))


def need(ok, message):
    if not ok:
        raise ValueError(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def word(raw, offset=0):
    return struct.unpack_from('<I', raw, offset)[0]


def pinned(path, expected, maximum):
    path = Path(path)
    need(0 < path.stat().st_size <= maximum, 'bounded input: ' + str(path))
    raw = path.read_bytes()
    need(sha(raw) == expected, 'fixed input identity: ' + str(path))
    return raw, dict(path=str(path.resolve()), bytes=len(raw), sha256=expected)


def authenticate(window, proof):
    """Bind the pinned prior diagnostic, including its unrepaired exclusions."""
    need(proof['status'] == 'diagnostic_individual_waits_with_unproven_switch_snapshots'
         and proof['errors'] == [] and proof['accepted'] is False
         and proof['strict_full_window_verified'] is False, 'unchanged diagnostic limitations')
    need(proof['source']['sha256'] == WINDOW_SHA, 'proof binds exact source')
    analysis = proof['analysis']
    need(analysis['snapshots_checked'] == len(window['window_snapshots']) == 423
         and analysis['strict_single_switch_out_rule_for_every_counted_wait'] is True,
         'complete original snapshot accounting')
    excluded = analysis['unproven_switch_interval_snapshots']
    need(tuple(x['snapshot_index'] for x in excluded) == EXCLUDED
         and all(x['used_to_prove_wait'] is False for x in excluded),
         'all four crossing snapshots remain rejected')
    used = [i for row in analysis['waits'] for i in row['snapshot_indices']]
    need(len(used) == len(set(used)) == 419 and not set(used) & set(EXCLUDED),
         'exact 419 supported snapshots, none from four crossing intervals')
    pairs = [row for row in analysis['waits'] if INDEX in row['snapshot_indices']]
    need(len(pairs) == 1, 'one successful pair for the selected actual snapshot')
    pair = pairs[0]
    need(pair['snapshot_indices'] == [INDEX] and pair['global_indices'] == [16928, 19426]
         and pair['NTSTATUS'] == 0 and pair['semantic']['wait_return_site'] == 0x453CDD,
         'exact retained successful wait and original caller')
    snap = window['window_snapshots'][INDEX]
    need(sha(canonical(snap)) == SNAPSHOT_SHA, 'fixed complete selected snapshot')
    raw = bytes.fromhex(snap['frame']['context_hex'])
    need(len(raw) == 716 and sha(raw) == CONTEXT_SHA and word(raw) == 0x1003F,
         'fixed original 716-byte WOW64 context')
    need(pair['interval_ns'][0] < snap['snapshot_begin_ns'] <= snap['snapshot_end_ns']
         < pair['interval_ns'][1], 'selected snapshot lies within paired syscall')
    need(word(raw, 176) == pair['NTSTATUS'] == 0,
         'existing pending EAX equals conditional ETW input; never assign return value')
    need(word(raw, 160) == 0 and word(raw, 184) == snap['frame']['EIP'] == 0x77D13BFC,
         'exact pending integer path and original Nt return PC')
    need(snap['current_TLS']['owner_pid'] == window['subject']['pid']
         and snap['frame']['tid'] == snap['current_TLS']['thread_id'] == window['subject']['tid'],
         'same actual process and thread')
    return snap, pair


class Sparse:
    """Known original bytes only; mapped page padding never confers provenance."""
    def __init__(self):
        self.known = {}
        self.code = set()
        self.writable = set()

    def add(self, address, raw, *, code=False, writable=False):
        need(raw and 0 <= address < address + len(raw) <= 0x100000000, 'bounded region')
        for at, value in enumerate(raw, address):
            need(at not in self.known or self.known[at] == value, 'overlapping source bytes agree')
            self.known[at] = value
            if code:
                self.code.add(at)
            if writable:
                self.writable.add(at)

    def missing(self, address, size, allowed=None):
        allowed = self.known if allowed is None else allowed
        return next((at for at in range(address, address+size) if at not in allowed), None)


def prepare(window_path, proof_path, image_path, dll_path):
    import pefile
    packed, wid = pinned(window_path, WINDOW_SHA, 2*1024*1024)
    proof_raw, pid = pinned(proof_path, PROOF_SHA, 512*1024)
    image, iid = pinned(image_path, IMAGE_SHA, 8*1024*1024)
    dll, did = pinned(dll_path, DLL_SHA, 4*1024*1024)
    with gzip.GzipFile(fileobj=__import__('io').BytesIO(packed)) as stream:
        raw = stream.read(8*1024*1024+1)
    need(len(raw) <= 8*1024*1024, 'bounded expanded window')
    window, proof = json.loads(raw), json.loads(proof_raw)
    snap, pair = authenticate(window, proof)
    sparse = Sparse()
    for lo, hi in GAME_RANGES:
        row = next(r for r in window['original_code'] if r['pointer'] == lo)
        data = bytes.fromhex(row['hex'])
        need(len(data) == hi-lo and data == image[lo-0x400000:hi-0x400000],
             'live authenticated original game code')
        sparse.add(lo, data, code=True)
    nt = next(r for r in window['API_exports'] if r['name'] == 'NtWaitForSingleObject')
    data = bytes.fromhex(nt['entry_hex'])
    need(nt['target']+12 == snap['frame']['EIP'] and data[12:15] == b'\xc2\x0c\x00',
         'actual captured Nt ret12 instruction')
    sparse.add(nt['target']+12, data[12:15], code=True)
    base = window['TLS_implementation']['base']
    need(base == 0x77A40000 and window['TLS_implementation']['module_sha256'] == DLL_SHA,
         'actual retained kernelbase base and disk module identity')
    mapped = pefile.PE(data=dll).get_memory_mapped_image(ImageBase=base)
    wrappers = []
    for lo, hi in WRAPPER_RANGES:
        data = mapped[lo-base:hi-base]
        sparse.add(lo, data, code=True)
        wrappers.append(dict(pointer=lo, bytes=len(data), sha256=sha(data), live_authenticated=False))
    for row in snap['stack_regions']:
        sparse.add(row['pointer'], bytes.fromhex(row['hex']), writable=True)
    sparse.add(snap['node_pointer'], bytes.fromhex(snap['scene_head_hex']))
    sparse.writable.update(range(snap['node_pointer']+4, snap['node_pointer']+8))
    tls = snap['current_TLS']
    sparse.add(tls['TEB'], bytes.fromhex(tls['TEB_head_hex']))
    sparse.writable.update(range(tls['TEB'], tls['TEB']+4))
    need(not sparse.code & sparse.writable, 'source code is never writable')
    return dict(snapshot=snap, pair=pair, sparse=sparse, references=[wid, pid, iid, did],
                wrapper_candidates=wrappers)


def descriptor(base, limit, access, flags):
    return struct.pack('<HHBBBB', limit & 0xffff, base & 0xffff, (base >> 16) & 255,
                       access, ((limit >> 16) & 15) | flags, (base >> 24) & 255)


def execute(inputs):
    import unicorn as un
    from unicorn import x86_const as reg
    import capstone as cs
    from capstone import x86_const as x86
    sparse = inputs['sparse']
    snapshot = inputs['snapshot']
    source_cpu = bytes.fromhex(snapshot['frame']['context_hex'])
    tls = snapshot['current_TLS']
    uc = un.Uc(un.UC_ARCH_X86, un.UC_MODE_32)
    md = cs.Cs(cs.CS_ARCH_X86, cs.CS_MODE_32)
    md.detail = True
    pages = sorted({at & -4096 for at in sparse.known})
    need(GDT not in pages and (len(pages)+1)*4096 <= MEMORY_LIMIT, 'bounded isolated mapping')
    for page in pages:
        has_code = any(at in sparse.code for at in range(page, page+4096))
        has_data = any(at in sparse.writable for at in range(page, page+4096))
        need(not (has_code and has_data), 'code/data pages disjoint')
        uc.mem_map(page, 4096, un.UC_PROT_READ | (un.UC_PROT_EXEC if has_code else un.UC_PROT_WRITE))
    # Physical padding is only storage. Neither read nor execute guards accept it.
    for start, data in regions(sparse.known):
        uc.mem_write(start, data)
    gdt = bytearray(4096)
    selectors = {name:word(source_cpu, off) for name, off in SEGMENT_OFFSETS.items()}
    need(selectors == dict(GS=0x2b, FS=0x53, ES=0x2b, DS=0x2b, CS=0x23, SS=0x2b),
         'fixed source selectors')
    # Only FS descriptor is captured. Flat code/data are explicit conditional
    # platform inputs, not invented original descriptor evidence.
    gdt[0x20:0x28] = descriptor(0, 0xfffff, 0xfb, 0xc0)
    gdt[0x28:0x30] = descriptor(0, 0xfffff, 0xf3, 0xc0)
    # Unicorn's direct CS load does not establish ring-3 CPL; loading source
    # SS=2B therefore raises #GP. An explicit flat ring-0 stack descriptor gives
    # 32-bit address/stack semantics; its selector is NOT claimed restored.
    gdt[0x18:0x20] = descriptor(0, 0xfffff, 0x93, 0xc0)
    fs = bytes.fromhex(tls['selector_hex'])
    fs_base = int.from_bytes(fs[2:4], 'little') | (fs[4] << 16) | (fs[7] << 24)
    need(len(fs) == 8 and fs_base == tls['TEB'] and fs == bytes.fromhex('ff0f002030f34000'),
         'actual FS descriptor and original TEB base')
    gdt[0x50:0x58] = fs
    uc.mem_map(GDT, 4096, un.UC_PROT_READ | un.UC_PROT_WRITE)
    uc.mem_write(GDT, bytes(gdt))
    uc.reg_write(reg.UC_X86_REG_GDTR, (0, GDT, 4095, 0))
    effective_selectors = dict(selectors, SS=0x18)
    for name in ('CS', 'DS', 'ES', 'SS', 'GS', 'FS'):
        uc.reg_write(getattr(reg, 'UC_X86_REG_'+name), effective_selectors[name])
    uc.mem_protect(GDT, 4096, un.UC_PROT_READ)
    for name, offset in INTEGER_OFFSETS.items():
        uc.reg_write(getattr(reg, 'UC_X86_REG_'+name), word(source_cpu, offset))

    def cpu():
        return {name:uc.reg_read(getattr(reg, 'UC_X86_REG_'+name)) for name in INTEGER_OFFSETS}

    initial = cpu()
    need(initial == {name:word(source_cpu, offset) for name, offset in INTEGER_OFFSETS.items()},
         'all declared integer registers restored exactly without return-value substitution')
    need(uc.reg_read(reg.UC_X86_REG_FS_BASE) == tls['TEB'], 'Unicorn loaded actual FS base')
    initial_pages = {page:bytes(uc.mem_read(page, 4096)) for page in pages+[GDT]}
    instructions, writes, returns, reads = [], [], [], []
    frontier = None
    pending_return = None
    current = None
    trace = hashlib.sha256()
    write_trace = hashlib.sha256()

    def memory_check(address, size, mode):
        need(type(address) is int and 0 < size <= 16 and 0 <= address < address+size <= 0x100000000,
             'bounded integer memory operand')
        allowed = sparse.writable if mode == 'write' else sparse.known
        missing = sparse.missing(address, size, allowed)
        if missing is not None:
            return dict(kind='uncaptured_'+mode, PC=current['PC'], instruction_hex=current['hex'],
                        address=address, bytes=size, first_missing=missing,
                        instruction_executed=False, integer_CPU=cpu(), writes_before=len(writes))
        return None

    def effective(op, ins):
        mem = op.mem
        def value(register):
            if register == 0:
                return 0
            name = ins.reg_name(register).upper()
            need(name in INTEGER_OFFSETS and name not in ('EIP', 'EFLAGS'), 'only restored integer address registers')
            return uc.reg_read(getattr(reg, 'UC_X86_REG_'+name))
        segment = ins.reg_name(mem.segment) if mem.segment else ''
        need(segment in ('', 'fs', 'es', 'ds', 'ss'), 'unrestored segment use')
        offset = (value(mem.base) + value(mem.index)*mem.scale + mem.disp) & 0xffffffff
        return offset + (tls['TEB'] if segment == 'fs' else 0)

    def accesses(ins):
        mnemonic = ins.mnemonic
        allowed = {'mov', 'push', 'pop', 'call', 'ret', 'lea', 'add', 'sub', 'cmp',
                   'test', 'jne', 'je', 'js', 'jmp', 'xor', 'and', 'rep stosd'}
        need(mnemonic in allowed and ins.addr_size == 4, 'unsupported instruction/state: '+mnemonic)
        need(not any(ins.reg_name(r).startswith(('st', 'xmm', 'ymm', 'mm', 'cr', 'dr'))
                     for r in ins.regs_access()[0]+ins.regs_access()[1]), 'unrestored noninteger architectural state')
        for operand in ins.operands:
            if operand.type == x86.X86_OP_REG:
                name = ins.reg_name(operand.reg)
                need(name in ('eax','ebx','ecx','edx','esi','edi','ebp','esp'), 'unrestored explicit register')
        if mnemonic == 'rep stosd':
            need(cpu()['EFLAGS'] & 0x400 == 0, 'captured forward REP only')
            return [(cpu()['EDI'], 4, 'write')] if cpu()['ECX'] else []
        result = []
        for i, operand in enumerate(ins.operands):
            if operand.type != x86.X86_OP_MEM or mnemonic == 'lea':
                continue
            address = effective(operand, ins)
            if mnemonic == 'mov':
                modes = ('write',) if i == 0 else ('read',)
            elif mnemonic in ('cmp', 'test', 'push'):
                modes = ('read',)
            elif mnemonic in ('add', 'sub', 'xor', 'and'):
                modes = ('read', 'write') if i == 0 else ('read',)
            else:
                raise ValueError('unsupported indirect memory instruction')
            result.extend((address, operand.size, mode) for mode in modes)
        if mnemonic in ('push', 'call'):
            if mnemonic == 'call':
                need(ins.operands[0].type == x86.X86_OP_IMM, 'no inferred indirect call')
            result.append(((cpu()['ESP']-4) & 0xffffffff, 4, 'write'))
        elif mnemonic in ('pop', 'ret'):
            result.append((cpu()['ESP'], 4, 'read'))
        return result

    def code(_uc, address, size, _):
        nonlocal current, frontier, pending_return
        if pending_return is not None:
            need(address == pending_return['target'] and cpu()['ESP'] == pending_return['expected_ESP'],
                 'original RET naturally reaches captured address and stdcall stack')
            returns.append(pending_return)
            pending_return = None
        need(len(instructions) < LIMIT, 'bounded 4096 original instruction callbacks')
        need(sparse.missing(address, size, sparse.code) is None, 'uncaptured instruction fetch')
        raw = bytes(uc.mem_read(address, size))
        need(raw == bytes(sparse.known[a] for a in range(address, address+size)), 'original code unchanged')
        ins = next(md.disasm(raw, address), None)
        need(ins is not None and ins.size == size, 'complete decoded original instruction')
        current = dict(PC=address, hex=raw.hex())
        before = cpu()
        for target, count, mode in accesses(ins):
            missing = memory_check(target, count, mode)
            if missing:
                frontier = missing
                uc.emu_stop()
                need(cpu() == before, 'pre-execution unknown operand does not change integer context')
                return
        if ins.mnemonic == 'ret':
            sp = before['ESP']
            pop = ins.operands[0].imm if ins.operands else 0
            pending_return = dict(PC=address, source_ESP=sp, target=word(bytes(uc.mem_read(sp,4))),
                                  expected_ESP=sp+4+pop, immediate_pop=pop)
        instructions.append(current)
        trace.update(struct.pack('<I', address)+raw)

    def read(_uc, _access, address, size, _value, _):
        need(memory_check(address, size, 'read') is None, 'preflight missed an unknown data read')
        reads.append((address, size))

    def write(_uc, _access, address, size, value, _):
        need(memory_check(address, size, 'write') is None, 'preflight missed an unknown or forbidden write')
        before = bytes(uc.mem_read(address, size))
        after = (value & ((1 << (size*8))-1)).to_bytes(size, 'little')
        row = dict(PC=current['PC'], address=address, before_hex=before.hex(), after_hex=after.hex())
        writes.append(row)
        write_trace.update(canonical(row))

    def invalid(_uc, access, address, size, value, _):
        raise ValueError('unmapped access escaped instruction preflight: '+hex(address))

    uc.hook_add(un.UC_HOOK_CODE, code)
    uc.hook_add(un.UC_HOOK_MEM_READ, read)
    uc.hook_add(un.UC_HOOK_MEM_WRITE, write)
    uc.hook_add(un.UC_HOOK_MEM_INVALID, invalid)
    uc.emu_start(initial['EIP'], 0, timeout=0, count=0)
    need(frontier is not None and frontier['kind'] == 'uncaptured_read'
         and (frontier['PC'], frontier['address'], frontier['bytes']) == (0x451723, 0x7A49FC, 4),
         'exact first uncaptured original global, never supplied from disk default bytes')
    need(cpu() == frontier['integer_CPU'] and len(writes) == frontier['writes_before'],
         'blocked instruction has no CPU or write effect')
    need(pending_return is None, 'every executed RET verified at its natural successor')
    consumers = []
    # Addresses are derived from the actual source frame chain, not fabricated frames.
    for pc, return_va, offset in ((0x451ABC, 0x451716, 8), (0x451716, 0x421F8A, 12)):
        frame = next(f for f in snapshot['frame']['chain'] if f['return_va'] == return_va)
        address = frame['bp'] - offset
        hits = [r for r in writes if r['PC'] == pc and r['address'] == address]
        need(len(hits) == 1 and hits[0]['after_hex'] == '01000000', 'natural original result consumer write')
        consumers.append(hits[0])
    need(any(r['PC'] == 0x453CDD and r['hex'] == 'b801000000' for r in instructions),
         'result one comes from original MOV EAX,1')
    final_pages = {page:bytes(uc.mem_read(page,4096)) for page in pages+[GDT]}
    changed = {a for page, data in final_pages.items() for i,(x,y) in enumerate(zip(initial_pages[page],data))
               if x != y for a in (page+i,)}
    need(changed <= sparse.writable, 'no unknown padding, GDT or code bytes changed')
    known_final = [(start, bytes(uc.mem_read(start,len(data)))) for start,data in regions(sparse.known)]
    result = dict(initial_integer_CPU=initial, final_integer_CPU=cpu(), frontier=frontier,
        instruction_callbacks=len(instructions), instructions=instructions, instruction_sha256=trace.hexdigest(),
        write_count=len(writes), writes=writes, write_sha256=write_trace.hexdigest(),
        natural_returns=returns, original_result_consumer_writes=consumers,
        known_byte_count=len(sparse.known), mapped_storage_bytes=len(final_pages)*4096,
        known_sparse_final_sha256=sha(b''.join(struct.pack('<II',a,len(b))+b for a,b in known_final)),
        storage_page_sha256=[dict(pointer=p,sha256=sha(b)) for p,b in sorted(final_pages.items())],
        read_callbacks=len(reads), changed_known_bytes=len(changed), padding_read_or_written=False,
        segment_platform_inputs=dict(GDT_address=GDT, GDT_sha256=sha(bytes(gdt)),
            original_selectors=selectors, original_FS_descriptor_hex=fs.hex(), original_FS_base=fs_base,
            effective_selectors=effective_selectors, original_SS_selector_restored=False,
            other_descriptors='synthetic flat 32-bit code/data descriptors; actual originals not captured',
            complete_architectural_segments_restored=False))
    return result, final_pages


def regions(memory):
    start = previous = None
    data = bytearray()
    for address in sorted(memory):
        if previous is not None and address != previous+1:
            yield start, bytes(data)
            data.clear()
            start = None
        if start is None:
            start = address
        data.append(memory[address])
        previous = address
    if data:
        yield start, bytes(data)


def diagnose(inputs):
    import unicorn, capstone, pefile
    first, first_pages = execute(inputs)
    second, second_pages = execute(inputs)
    need(first == second and first_pages == second_pages,
         'two fresh Unicorn instances exactly agree on integer CPU, sparse bytes, storage pages and trace')
    PCs = {row['PC'] for row in first['instructions']}
    first_consumer = 0x453CB5 in PCs
    recording = 0x4967B0 in PCs
    three_handshakes = all(pc in PCs for pc in (0x453CB0, 0x453CCE, 0x453CD8))
    need(not first_consumer and not recording and not three_handshakes,
         'only third-wait return tail, not first consumer, recording or three handshakes')
    return dict(schema_version=1, kind='conditional_original_result_tail_development_replay',
        accepted=False, fullABI=False, fullstate=False, original_native_continuity=False,
        new_native_capture=False, historical_handles_restored=False, independent_full_replay=False,
        original_wait_completed_proved=False, continuous_native_result_consumption_proved=False,
        first_result_consumer_453CB5_executed=first_consumer,
        replay_record_4967B0_executed=recording, three_handshakes_executed=three_handshakes,
        references=inputs['references'], snapshot_index=INDEX, snapshot_sha256=SNAPSHOT_SHA,
        original_context_sha256=CONTEXT_SHA, bound_prior_ETW_pair=inputs['pair'],
        rejected_crossing_snapshots=list(EXCLUDED), wrapper_candidates=inputs['wrapper_candidates'],
        wrapper_live_code_authenticated=False, pending_context_is_actual_post_syscall_context=False,
        conditional_return_input=dict(NTSTATUS=0, existing_pending_EAX=0, register_overwritten=False,
            source='pinned earlier individual-wait ETW pairing; not fresh API/ABI verification'),
        limits=dict(instruction_callbacks=LIMIT, mapped_storage_bytes=MEMORY_LIMIT, report_bytes=REPORT_LIMIT),
        restored_fields=list(INTEGER_OFFSETS), unrestored_fields=['x87/FPU state','SIMD/XMM state',
            'debug registers','original non-FS segment descriptors','hidden processor state'],
        limitations=['Pending integer context plus matching ETW status is a conditional input, not authenticated post-return ABI.',
            'No contemporaneous after-wait state or concurrent scheduler effects are reconstructed.',
            'OS wrapper body is derived from a matching guest DLL; its live bytes were not captured.',
            'Uncaptured page padding is storage only; exact comparison is of a declared sparse-byte model.',
            'Only original consumer tail through the first uncaptured global is executed; no full wait/lifetime acceptance.'],
        runtime_versions=dict(unicorn=unicorn.__version__, capstone=capstone.__version__, pefile=pefile.__version__),
        second_fresh_Unicorn_exact_match=True, result=first)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('window', 'diagnostic-proof', 'image', 'guest-dll', 'out'):
        parser.add_argument('--'+name, type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists(), 'fresh output only')
    implementation = Path(__file__).read_bytes()
    inputs = prepare(args.window, args.diagnostic_proof, args.image, args.guest_dll)
    report = diagnose(inputs)
    report['implementation'] = dict(path=str(Path(__file__).resolve()), sha256=sha(implementation))
    need(Path(__file__).read_bytes() == implementation, 'implementation unchanged during bounded replay')
    raw = canonical(report)+b'\n'
    need(len(raw) <= REPORT_LIMIT, 'bounded complete report')
    with args.out.open('xb') as stream:
        stream.write(raw)
    print(json.dumps(dict(accepted=False, conditional_consumer_tail_executed=True,
                         frontier=report['result']['frontier'], output_bytes=len(raw))))
    return 2  # Deliberately never a full-acceptance success exit.


if __name__ == '__main__':
    raise SystemExit(main())
