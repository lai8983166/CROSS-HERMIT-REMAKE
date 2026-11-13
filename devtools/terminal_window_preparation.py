"""Original window preparation leaves on the existing MAIN native owner.

No UI gate, module acquisition, launcher, or desktop permission is implicit.
The live HINSTANCE must be a declared WinMain input before original execution.
"""
from __future__ import annotations
import struct
from devtools.terminal_window_callbacks import WindowEngine, base, need

PREPARATION = {0x59232c: ('FindWindowA', 2), 0x5923f8: ('SetRect', 5),
               0x5923fc: ('AdjustWindowRect', 3), 0x5923cc: ('LoadIconA', 2),
               0x5923c8: ('LoadCursorA', 2), 0x592084: ('GetStockObject', 1),
               0x592408: ('RegisterClassExA', 1)}


class PreparedWindowEngine(WindowEngine):
    def __init__(self):
        super().__init__()
        self.preparation_runs = []
        self.slots.update(PREPARATION)
        self.targets = {self.word(slot): slot for slot in self.slots}
        need(len(self.targets) == len(self.slots), 'unique original preparation import targets')
        for slot in PREPARATION:
            target = self.word(slot)
            if not any(a <= target <= b for a, b, _ in self.u.mem_regions()):
                self.u.mem_map(target & -4096, 4096)
            need(not 0x400000 <= target < 0x9b4000, 'external preparation import landing')
            self.put(target, b'\xc3')
        self.md.topology()
        self.shared_icons, self.shared_cursor, self.stock_brush, self.class_atom = [], 0, 0, 0

    def code(self, u, pc, size, user):
        super().code(u, pc, size, user)
        if not self.frames and pc not in (base.RETURN, self.stop) and pc not in self.targets:
            if self.preparation_runs and self.preparation_runs[-1]['va'] == pc:
                self.preparation_runs[-1]['count'] += 1
            else:
                self.preparation_runs.append(dict(va=pc, count=1))

    def buffer(self, raw, temporaries):
        reply = yield ('MEM_ALLOC', len(raw))
        pointer = reply['result']
        need(pointer, 'current native preparation buffer')
        temporaries.append(dict(native=pointer, bytes=len(raw), released=False))
        reply = yield ('MEM_WRITE', pointer, raw.hex())
        need(reply['result'] == len(raw), 'complete native preparation buffer mirror')
        return pointer

    def api(self, slot):
        if slot not in PREPARATION:
            yield from super().api(slot)
            return
        need(not self.frames and self.lane == 0 and self.window_owner and self.window_module,
             'window preparation bound to current original MAIN/module')
        name, argc = self.slots[slot]
        sp = self.reg('ESP')
        args = [self.word(sp + 4 + i * 4) for i in range(argc)]
        record = dict(name=name, slot=slot, sp=sp, ret=self.word(sp), args=args,
                      before=self.state(), wire_start=len(self.owner.trace), projections=[], outputs=[])
        self.records.append(record)
        temporaries = []
        record['temporary_buffers'] = temporaries
        record['failure_requires_Job_containment'] = True
        ptd = self.thread_ptd[0]
        if ptd:
            yield from self.sync(ptd)
            reply = yield ('MEM_READ', self.native(ptd), 116)
            need(reply['hex'] == self.read(ptd, 116).hex(), 'actual live MAIN PTD at preparation leaf')
            record['current_native_PTD'] = reply
        if name == 'FindWindowA':
            need(args == [0x7a2628, 0] and self.string(args[0]) == b'Cross Hermit\0', 'original duplicate-window query')
            pointer = yield from self.buffer(self.string(args[0]), temporaries)
            record['projections'].append(dict(guest=args[0], native=pointer, bytes=13))
            reply = yield (name, pointer, 0)
        elif name in ('SetRect', 'AdjustWindowRect'):
            need(args[1:] == ([0, 0, 1024, 768] if name == 'SetRect' else [0x90000000, 0]), 'original window geometry arguments')
            pointer = yield from self.buffer(self.read(args[0], 16), temporaries)
            record['projections'].append(dict(guest=args[0], native=pointer, bytes=16))
            reply = yield (name, pointer, *args[1:])
            need(reply['result'] == 1, 'actual rectangle operation succeeded')
            observed = yield ('MEM_READ', pointer, 16)
            raw = bytes.fromhex(observed['hex'])
            need(observed['result'] == len(raw) == 16, 'complete native RECT output')
            self.put(args[0], raw)
            record['outputs'].append(dict(pointer=args[0], hex=raw.hex()))
        elif name == 'RegisterClassExA':
            raw = self.read(args[0], 48)
            fields = list(struct.unpack('<12I', raw))
            need(len(self.shared_icons) == 2 and fields == [48, 0, 0x424980, 0, 0, self.window_module,
                 self.shared_icons[0], self.shared_cursor, self.stock_brush, 0, 0x7a2628, self.shared_icons[1]],
                 'complete original class structure with current owned resources')
            title = self.string(fields[10])
            need(title == b'Cross Hermit\0', 'original fixed class name')
            name_pointer = yield from self.buffer(title, temporaries)
            fields[10] = name_pointer
            pointer = yield from self.buffer(struct.pack('<12I', *fields), temporaries)
            record['projections'].append(dict(guest=args[0], native=pointer, original_hex=raw.hex(),
                                             class_name_native=name_pointer, only_class_name_pointer_adapted=True))
            reply = yield (name, pointer)
            self.class_atom = reply['result'] & 0xffff
            need(self.class_atom and reply['atom'] == self.class_atom, 'actual registered class ATOM and full original EAX')
        else:
            if name == 'LoadIconA':
                need(args == [self.window_module, 157] and len(self.shared_icons) < 2, 'actual current module original icon157')
            elif name == 'LoadCursorA':
                need(args == [0, 32512] and not self.shared_cursor, 'original shared system arrow')
            else:
                need(args == [4] and not self.stock_brush, 'original stock brush4')
            reply = yield (name, *args)
            need(reply['result'], 'actual original window resource')
            if name == 'LoadIconA':
                self.shared_icons.append(reply['result'])
            elif name == 'LoadCursorA':
                self.shared_cursor = reply['result']
            else:
                self.stock_brush = reply['result']
        value = reply['result']
        record['native_leaf'] = reply
        for temporary in reversed(temporaries):
            released = yield ('MEM_FREE', temporary['native'])
            need(released['result'] == 1, 'temporary native window buffer released')
            temporary['released'] = True
        record['failure_requires_Job_containment'] = False
        self.reg('EAX', value)
        self.reg('ESP', sp + 4 + argc * 4)
        self.reg('EIP', record['ret'])
        record.update(value=value, after=self.state(), wire_end=len(self.owner.trace))
