"""Bounded execution transactions for an independent original-instruction replay.

Records host boundary effects, not per-instruction CPU/memory dumps. Guest
instructions and writes are cumulatively hashed. Every transaction includes
all architectural registers and a digest of every mapped byte/permission.
"""
import hashlib
import struct

PAGE = 4096
BLOCK = 65536
SLICE = 250000
CPU_REGISTERS = tuple('EAX EBX ECX EDX ESI EDI EBP ESP EIP EFLAGS FPCW FPSW FPTAG FIP FDP FCS FDS FOP MXCSR CS DS ES FS GS SS CR0 CR2 CR3 CR4 GDTR IDTR LDTR TR'.split()) + tuple('FP'+str(i) for i in range(8)) + tuple('XMM'+str(i) for i in range(8)) + tuple('DR'+str(i) for i in range(8))


def complete_CPU(value):
    if type(value) is not dict or set(value) != set(CPU_REGISTERS):
        raise ValueError('canonical complete57 architectural CPU required')
    return value


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


class MemoryDigest:
    def __init__(self, uc):
        self.uc = uc
        self.pages = {}
        self.blocks = {}
        self.dirty = set()
        self.topology_dirty = True

    def write(self, address, size):
        if size:
            self.dirty.update(range(address & -PAGE, (address + size + PAGE - 1) & -PAGE, PAGE))

    def topology(self, address=None, size=None):
        self.topology_dirty = True
        # Unmap+map may occur between captures with identical final topology.
        # Such pages must be rehashed even though their addresses still exist.
        if address is None:
            self.dirty.update(self.pages)
        else:
            self.write(address, size)

    def capture(self):
        dirty_blocks = set()
        if self.topology_dirty:
            self.regions = list(self.uc.mem_regions())
            current = {p for a, b, _ in self.regions for p in range(a, b + 1, PAGE)}
            for p in self.pages.keys() - current:
                dirty_blocks.add(p & -BLOCK)
                del self.pages[p]
            self.dirty.update(current - self.pages.keys())
            self.valid_pages = current
            h = hashlib.sha256()
            for a, b, permission in self.regions:
                h.update(struct.pack('<III', a, b, permission))
            self.topology_hash = h.digest()
            self.topology_dirty = False
        for p in self.dirty & self.valid_pages:
            self.pages[p] = hashlib.sha256(bytes(self.uc.mem_read(p, PAGE))).digest()
            dirty_blocks.add(p & -BLOCK)
        self.dirty.clear()
        for block in dirty_blocks:
            h = hashlib.sha256()
            count = 0
            for p in range(block, block + BLOCK, PAGE):
                if p in self.pages:
                    h.update(struct.pack('<I', p) + self.pages[p])
                    count += 1
            if count:
                self.blocks[block] = h.digest()
            else:
                self.blocks.pop(block, None)
        h = hashlib.sha256(self.topology_hash)
        for block in sorted(self.blocks):
            h.update(struct.pack('<I', block) + self.blocks[block])
        return dict(sha256=h.hexdigest(), regions=len(self.regions), pages=len(self.pages),
                    bytes=sum(b-a+1 for a, b, _ in self.regions))


class TraceCount:
    def __init__(self):
        self.instructions = self.writes = 0
        self.ih = hashlib.sha256()
        self.wh = hashlib.sha256()
        self.write_PCs = set()

    def instruction(self, pc):
        self.instructions += 1
        self.ih.update(struct.pack('<I', pc))

    def write(self, pc, address, size, value):
        self.writes += 1
        self.write_PCs.add(pc)
        self.wh.update(struct.pack('<III', pc, address, size))
        self.wh.update((value & ((1 << (8*size))-1)).to_bytes(size, 'little'))

    def mark(self):
        return dict(instructions=self.instructions, writes=self.writes,
                    code_sha256=self.ih.hexdigest(), write_sha256=self.wh.hexdigest())


class Recorder:
    """Attach after all declared constructor inputs, before the first guest root.

    The machine's code/write hooks call begin_code/end_code and guest_write.
    A complete runtime validator must classify all recorded host effects; this
    recorder by itself is never an independent proof or an acceptance decision.
    """
    def __init__(self, machine):
        self.m, self.uc = machine, machine.uc
        self.memory = MemoryDigest(self.uc)
        self.count = TraceCount()
        self.initial_memory = machine.snapshot()
        self.initial_CPU = complete_CPU(machine.cpu())
        self.initial_regions = [list(x) for x in self.uc.mem_regions()]
        self.initial_mutable = [list(x) for x in machine.mutable]
        self.initial_memory_digest = self.memory.capture()
        self.transactions = []
        self.driver = []
        self.running = False
        self.callback = False
        self.current_event = None
        self.host_budget_stop = False
        self.stopped = False
        self.current_pc = None
        self.original = {}
        self.native_original = []
        for name in ('mem_write', 'reg_write', 'mem_map', 'mem_protect', 'mem_unmap', 'emu_stop', 'emu_start'):
            self.original[name] = getattr(self.uc, name)
        for name in ('mem_write', 'reg_write', 'mem_map', 'mem_protect', 'mem_unmap'):
            setattr(self.uc, name, self._wrapper(name))
        self.uc.emu_stop = self._stop
        self.uc.emu_start = self._run
        # An observer can issue a native sync/readback without changing guest
        # RAM/registers. Capture its actual instruction boundary too, before
        # later original instructions can alter the inspected buffer.
        for owner, method in ((getattr(machine,'live',None),'request'),
                              (getattr(machine,'gpu',None),'request'),
                              (getattr(machine,'name_platform',None),'call')):
            if owner is not None and callable(getattr(owner,method,None)):
                original = getattr(owner,method)
                self.native_original.append((owner,method,original))
                setattr(owner,method,self._native_wrapper(original))

    def _start_event(self):
        if self.current_event is None:
            self.current_event = dict(pc=self.current_pc, before_CPU=self.m.cpu(), effects=[])
            if hasattr(self.m, 'boundary_identity'):
                self.current_event['boundary'] = self.m.boundary_identity(self.current_pc)
            if self.wire_before is None and hasattr(self.m, 'boundary_wire_counts'):
                self.wire_before = self.m.boundary_wire_counts()

    def _native_wrapper(self, original):
        def call(*args, **kwargs):
            if self.running:
                if not self.callback:
                    raise ValueError('native request outside declared instruction boundary')
                self._start_event()
            return original(*args, **kwargs)
        return call

    def _effect(self, action):
        if not self.running:
            self.driver.append(action)
            return
        if not self.callback:
            raise ValueError('host state change outside declared code callback')
        self._start_event()
        self.current_event['effects'].append(action)

    def _wrapper(self, name):
        def call(*args, **kwargs):
            if kwargs:
                raise ValueError('explicit positional guest state API required: ' + name)
            if name == 'mem_write':
                action = dict(kind=name, address=args[0], hex=bytes(args[1]).hex())
            elif name == 'reg_write':
                value = list(args[1]) if isinstance(args[1], tuple) else args[1]
                action = dict(kind=name, register=args[0], value=value)
            elif name == 'mem_unmap':
                action = dict(kind=name, address=args[0], bytes=args[1])
            else:
                action = dict(kind=name, address=args[0], bytes=args[1],
                              permission=args[2] if len(args) > 2 else 7)
            self._effect(action)
            result = self.original[name](*args)
            if name == 'mem_write':
                self.memory.write(args[0], len(args[1]))
            elif name in ('mem_map', 'mem_protect', 'mem_unmap'):
                self.memory.topology(args[0], args[1])
            return result
        return call

    def _stop(self):
        self.stopped = True
        return self.original['emu_stop']()

    def begin_code(self, pc):
        if not self.running:
            raise ValueError('unrecorded guest execution')
        if self.count.instructions - self.slice_first >= SLICE:
            self.host_budget_stop = True
            self.original['emu_stop']()
            return False
        self.current_pc = pc
        self.current_event = None
        self.wire_before = None
        if not 0x400000 <= pc < 0x9B4000 and hasattr(self.m, 'boundary_wire_counts'):
            self.wire_before = self.m.boundary_wire_counts()
        self.stopped = False
        self.callback = True
        return True

    def end_code(self, pc):
        after = self.m.cpu() if self.current_event is not None or self.stopped else None
        continues = not self.stopped and (after is None or after['EIP'] == pc)
        if self.current_event is not None or self.stopped:
            event = self.current_event or dict(pc=pc, before_CPU=after, effects=[])
            event['CPU_changes'] = {k:v for k,v in after.items() if v != event['before_CPU'][k]}
            event.update(stop=self.stopped, continues_guest=continues)
            if self.wire_before is not None:
                end = self.m.boundary_wire_counts()
                event['wire'] = {k:[v, end[k]] for k,v in self.wire_before.items()}
            self.events.append(event)
        if continues:
            self.count.instruction(pc)
        self.callback = False

    def guest_write(self, pc, address, size, value):
        self.memory.write(address, size)
        self.count.write(pc, address, size, value)

    def _run(self, begin, end, timeout=0, count=0):
        if self.running:
            raise ValueError('nested Unicorn execution is not a supported transaction')
        row = dict(entry=begin, end=end, requested_timeout=timeout, requested_count=count,
                   engine_timeout=0, engine_count=0, driver=self.driver,
                   before_CPU=self.m.cpu(), before_memory=self.memory.capture(),
                   before_trace=self.count.mark())
        if hasattr(self.m,'boundary_wire_counts'):
            row['wire_before'] = self.m.boundary_wire_counts()
        self.driver = []
        self.events = []
        self.running = True
        try:
            for _ in range(8192):
                self.host_budget_stop = False
                self.slice_first = self.count.instructions
                self.original['emu_start'](begin, end, timeout=0, count=0)
                if not self.host_budget_stop:
                    break
                begin = self.m.cpu()['EIP']
            else:
                raise ValueError('finite transaction host-slice budget exceeded')
        finally:
            self.running = self.callback = False
        row.update(events=self.events, after_CPU=self.m.cpu(),
                   after_memory=self.memory.capture(), after_trace=self.count.mark())
        if hasattr(self.m,'boundary_wire_counts'):
            row['wire_after'] = self.m.boundary_wire_counts()
        self.transactions.append(row)

    def finish(self):
        if self.running:
            raise ValueError('finish only at a quiescent guest boundary')
        return dict(schema_version=2, initial_memory=self.initial_memory,
                    initial_CPU=self.initial_CPU, initial_regions=self.initial_regions,
                    initial_mutable=self.initial_mutable,
                    initial_memory_digest=self.initial_memory_digest,
                    transactions=self.transactions, final_driver=self.driver,
                    final_CPU=self.m.cpu(), final_memory_digest=self.memory.capture(),
                    final_trace=self.count.mark(), engine_timeouts_disabled=True,
                    write_PCs=sorted(self.count.write_PCs),
                    host_budget_before_observation=True,
                    includes_host_effects_for_independent_validation=True,
                    accepted=False)

    def detach(self):
        for name, fn in self.original.items():
            setattr(self.uc, name, fn)
        for owner, name, fn in self.native_original:
            setattr(owner,name,fn)


class Replay:
    """A separate Unicorn execution, never a source after-state restoration.

    Mandatory validators check driver scaffolding/recorded raw inputs and OS,
    CRT or COM boundary semantics before effects are applied. Supplying a
    permissive validator is not an independent platform proof; callers must
    bind audited implementations and disclose their identities.
    """
    def __init__(self, report, original_code, ranges, validate_initial, validate_driver, validate_event):
        from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
        import unicorn.x86_const as x86
        if not all(callable(x) for x in (validate_initial, validate_driver, validate_event)):
            raise ValueError('independent initial-input, driver and platform validators required')
        complete_CPU(report['initial_CPU'])
        validate_initial(report, original_code, ranges)
        self.report, self.original_code, self.ranges = report, original_code, ranges
        # Some frozen CRT ranges deliberately denote one observed instruction
        # start, rather than every byte in that instruction. Authenticate every
        # fetched byte below, and independently compile these admitted starts.
        self.allowed = frozenset(pc for lo,hi in ranges for pc in range(lo,hi))
        self.validate_driver, self.validate_event = validate_driver, validate_event
        self.x86 = x86
        self.u = Uc(UC_ARCH_X86, UC_MODE_32)
        regions = report['initial_regions']
        snapshots = report['initial_memory']
        if len(regions) != len(snapshots):
            raise ValueError('initial whole memory partition mismatch')
        previous_end = -1
        for (a, b, permission), row in zip(regions, snapshots):
            raw = bytes.fromhex(row['hex'])
            if a <= previous_end or (row['pointer'], row['bytes'], len(raw)) != (a, b-a+1, b-a+1):
                raise ValueError('invalid initial complete memory')
            self.u.mem_map(a, b-a+1, 7)
            self.u.mem_write(a, raw)
            self.u.mem_protect(a, b-a+1, permission)
            previous_end = b
        self.register_names = list(CPU_REGISTERS)
        for name, value in report['initial_CPU'].items():
            reg = getattr(x86, 'UC_X86_REG_'+name)
            desired = tuple(value) if type(value) is list else value
            # Loading an already-default null segment selector can itself
            # fault in protected mode; retain matching architectural defaults.
            if self.u.reg_read(reg) != desired:
                self.u.reg_write(reg, desired)
        self.memory = MemoryDigest(self.u)
        self.count = TraceCount()
        self.history = [self.cpu()]
        self.mutable = [tuple(x) for x in report['initial_mutable']]
        self.u.hook_add(UC_HOOK_CODE, self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)
        if self.cpu() != report['initial_CPU'] or self.memory.capture() != report['initial_memory_digest']:
            raise ValueError('independent initial full CPU/memory mismatch')

    def cpu(self):
        out = {}
        for name in self.register_names:
            value = self.u.reg_read(getattr(self.x86, 'UC_X86_REG_'+name))
            out[name] = list(value) if type(value) is tuple else value
        return out

    def read(self, address, size):
        return bytes(self.u.mem_read(address, size))

    def apply(self, actions):
        for action in actions:
            kind = action['kind']
            if kind == 'mem_write':
                raw = bytes.fromhex(action['hex'])
                self.u.mem_write(action['address'], raw)
                self.memory.write(action['address'], len(raw))
            elif kind == 'reg_write':
                value = action['value']
                self.u.reg_write(action['register'], tuple(value) if type(value) is list else value)
            elif kind in ('mem_map', 'mem_protect'):
                getattr(self.u, kind)(action['address'], action['bytes'], action['permission'])
                self.memory.topology(action['address'], action['bytes'])
            elif kind == 'mem_unmap':
                self.u.mem_unmap(action['address'], action['bytes'])
                self.memory.topology(action['address'], action['bytes'])
            else:
                raise ValueError('unknown host effect')

    def code(self, uc, pc, size, context):
        if self.count.instructions - self.slice_first >= SLICE:
            self.budget_stop = True
            uc.emu_stop()
            return
        if self.event_index < len(self.events) and self.events[self.event_index]['pc'] == pc:
            event = self.events[self.event_index]
            if self.cpu() != event['before_CPU']:
                raise ValueError('independent full CPU differs before host boundary')
            self.validate_event(self, event)
            self.apply(event['effects'])
            expected = dict(event['before_CPU'], **event['CPU_changes'])
            if self.cpu() != expected:
                raise ValueError('independent full CPU differs after host boundary')
            self.event_index += 1
            if event['stop']:
                uc.emu_stop()
                return
            if not event['continues_guest']:
                if self.cpu()['EIP'] == pc:
                    raise ValueError('noncontinuing leaf did not return')
                return
            if self.cpu()['EIP'] != pc:
                raise ValueError('continuing original instruction PC changed')
        if pc not in self.allowed:
            raise ValueError('independent undeclared original instruction '+hex(pc))
        offset = pc-0x400000
        if offset < 0 or self.read(pc, size) != self.original_code[offset:offset+size]:
            raise ValueError('independent original executable bytes changed')
        if self.original_code[offset] == 0xCC:
            raise ValueError('original assertion/padding is not admissible')
        self.count.instruction(pc)

    def write(self, uc, access, address, size, value, context):
        if not any(a <= address and address+size <= b for a, b in self.mutable):
            raise ValueError('independent original write escapes owned ranges '+hex(address))
        pc = uc.reg_read(self.x86.UC_X86_REG_EIP)
        self.memory.write(address, size)
        self.count.write(pc, address, size, value)

    def run(self):
        for i, row in enumerate(self.report['transactions']):
            complete_CPU(row['before_CPU'])
            complete_CPU(row['after_CPU'])
            self.validate_driver(self, row['driver'], row, self.history)
            self.apply(row['driver'])
            if (self.cpu(), self.memory.capture(), self.count.mark()) != (
                    row['before_CPU'], row['before_memory'], row['before_trace']):
                raise ValueError('independent transaction start differs '+str(i))
            self.events, self.event_index = row['events'], 0
            begin = row['entry']
            for _ in range(8192):
                self.slice_first = self.count.instructions
                self.budget_stop = False
                self.u.emu_start(begin, row['end'], timeout=0, count=0)
                if not self.budget_stop:
                    break
                begin = self.cpu()['EIP']
            else:
                raise ValueError('independent transaction instruction budget exceeded')
            if self.event_index != len(self.events):
                raise ValueError('independent execution omitted host boundaries')
            if (self.cpu(), self.memory.capture(), self.count.mark()) != (
                    row['after_CPU'], row['after_memory'], row['after_trace']):
                raise ValueError('independent transaction full state/digests differ '+str(i))
            self.history.append(self.cpu())
        self.validate_driver(self, self.report['final_driver'], None, self.history)
        self.apply(self.report['final_driver'])
        if (self.cpu(), self.memory.capture(), self.count.mark()) != (
                self.report['final_CPU'], self.report['final_memory_digest'], self.report['final_trace']):
            raise ValueError('independent final complete state differs')
        if 'write_PCs' in self.report and sorted(self.count.write_PCs) != self.report['write_PCs']:
            raise ValueError('independent actual original write PCs differ')
        return dict(transactions=len(self.report['transactions']),
                    complete_CPU_and_mapped_memory_compared_at_every_transaction=True,
                    all_cumulative_original_digests_reproduced=True,
                    final_trace=self.count.mark(), final_memory=self.memory.capture())
