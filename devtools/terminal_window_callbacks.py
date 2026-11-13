"""Same-owner synchronous WNDPROC transport and CPU57 guest callback execution.

No launcher or UI admission is provided here. A native caller must already own
the original pending window API. Offline recorded responses are never a live
owner, nor a resumable native lifetime.
"""
from __future__ import annotations
import queue
import struct

from devtools import terminal_native_owner_probe as base
from devtools.terminal_scene_construction import SceneEngine

need = base.need
ENTRY = 0x424980
PROPERTY = b'CPP_CLASS\0'
IMPORTS = {0x5923dc: ('GetPropA', 2), 0x5923e8: ('SetPropA', 3),
           0x5923ec: ('GetWindowLongA', 2), 0x5923e0: ('DefWindowProcA', 4)}
CREATE_SLOT = 0x59240c
CLEANUP_IMPORTS = {0x5923e4: ('RemovePropA', 2), 0x59239c: ('PostQuitMessage', 1)}
CB_BASE, STRIDE = 0x66000000, 0x20000
MAX_DEPTH, MAX_CALLBACKS = 8, 128
DATA = {129: ('CREATESTRUCTA', 48), 1: ('CREATESTRUCTA', 48),
        131: ('RECT', 16), 70: ('WINDOWPOS', 28),
        71: ('WINDOWPOS', 28), 36: ('MINMAXINFO', 40)}


class WindowOwner(base.Owner):
    """Original reader/Job ownership, with authenticated synchronous C frames."""
    def __init__(self, *args, **kwargs):
        self.waiting = []
        self.callback_handler = None
        self.callback_packets = []
        self.callback_active = []
        super().__init__(*args, **kwargs)

    def consume_line(self, line):
        need(isinstance(line, str) and len(line) <= 66000, 'bounded owner line')
        parts = line.split()
        need(bool(parts), 'nonempty owner message')
        tag = parts[0]
        if tag == 'R':
            need(len(parts) >= 7, 'complete native response')
            row = dict(zip(('id', 'lane', 'tid', 'last_error', 'ok', 'result'), map(int, parts[1:7])))
            extra = parts[7:]
        elif tag == 'E':
            need(len(parts) >= 2, 'complete native event')
            row, extra = dict(event=parts[1]), parts[2:]
        else:
            need(tag == 'C', 'known owner message type')
            row, extra = {}, parts[1:]
        for item in extra:
            key, value = item.split('=', 1)
            need(key not in row, 'unique owner field')
            if value == '-' and (key == 'hex' or key.endswith('_hex')):
                value = ''
            row[key] = int(value) if value.isdecimal() and key != 'hex' and not key.endswith('_hex') else value
        self.trace.append(dict(direction='callback' if tag == 'C' else 'response', **row))
        if tag == 'E':
            self.events.append(row)
            return
        if tag == 'R':
            need(row['id'] in self.requests, 'unique outstanding response')
            lane, op = self.requests[row['id']]
            need(lane == row['lane'] and lane in (0, 1), 'request response lane')
            event = next(e for e in self.events if e['event'] == ('READY' if lane == 0 else 'WORKER_START'))
            tid, teb = (event['main_tid'], event['main_teb']) if lane == 0 else (event['worker_tid'], event['teb'])
            need((row['tid'], row['teb']) == (tid, teb), 'fixed native TID/TEB per lane')
            need(row['ok'] == 1, 'native rejection: ' + str(row))
            if op.startswith('CB_'):
                need(self.callback_active and row.get('callback_id') == self.callback_active[-1], 'matching active callback response')
            del self.requests[row['id']]
            self.responses[row['id']] = row
            return
        required = {'callback_id', 'parent_request', 'parent_callback_id', 'depth', 'lane', 'tid', 'teb',
                    'guest_entry', 'hwnd', 'message', 'wParam', 'lParam', 'data_kind', 'data_bytes', 'data_hex', 'last_error',
                    'tls_slot', 'tls_value', 'tls_tracked_value', 'tls_error', 'ptd_bytes', 'ptd_hex'}
        need(required <= row.keys(), 'complete native callback packet')
        need(all(isinstance(row[k], int) and 0 <= row[k] <= 0xffffffff
                 for k in required - {'data_kind', 'data_hex', 'ptd_hex'}), 'native callback unsigned32 fields')
        need(self.waiting and row['parent_request'] == self.waiting[-1], 'callback inside the actual pending request')
        lane, op = self.requests[row['parent_request']]
        need(lane == row['lane'] == 0 and op in ('CreateWindowExA', 'CB_DEFAULT', 'DestroyWindow'), 'callback-producing MAIN operation')
        ready = next(e for e in self.events if e['event'] == 'READY')
        need((row['tid'], row['teb']) == (ready['main_tid'], ready['main_teb']), 'callback same actual MAIN thread and TEB')
        need(row['callback_id'] == len(self.callback_packets) + 1 <= MAX_CALLBACKS, 'bounded monotonic actual callback ID')
        need(row['depth'] == len(self.callback_active) + 1 <= MAX_DEPTH, 'actual callback nesting')
        need(row['parent_callback_id'] == (self.callback_active[-1] if self.callback_active else 0), 'actual callback parent')
        need(self.callback_handler is not None, 'callback executor installed before native call')
        self.callback_packets.append(row)
        self.callback_active.append(row['callback_id'])
        try:
            value = self.callback_handler(row)
            reply = self.call('CB_RETURN', row['callback_id'], value)
            need(reply['result'] == 1 and reply['callback_result'] == value, 'exact native callback return acknowledged')
        finally:
            self.callback_active.pop()

    def poll(self, block=False):
        self.check()
        try:
            line = self.q.get(timeout=.025 if block else 0)
        except queue.Empty:
            return
        need(line is not None, 'owner pipe ended before callback completion')
        if isinstance(line, Exception):
            raise line
        self.consume_line(line)

    def wait_response(self, request_id):
        self.waiting.append(request_id)
        try:
            while request_id not in self.responses:
                self.poll(True)
            return self.responses.pop(request_id)
        finally:
            need(self.waiting.pop() == request_id, 'nested request stack restored')

    def call(self, op, *args):
        return self.wait_response(self.send(0, op, *args))


class WindowEngine(SceneEngine):
    def __init__(self):
        self.frames = []
        super().__init__()
        self.callbacks = []
        self.window_owner = 0
        self.window_module = 0
        self.window_handle = 0
        self.slots.update({**IMPORTS, **CLEANUP_IMPORTS, CREATE_SLOT: ('CreateWindowExA', 12)})
        self.targets = {self.word(s): s for s in self.slots}
        need(len(self.targets) == len(self.slots), 'unique frozen callback imports')
        for target in self.targets:
            if not any(a <= target <= b for a, b, _ in self.u.mem_regions()):
                self.u.mem_map(target & -4096, 4096)
        for slot in (*IMPORTS, *CLEANUP_IMPORTS, CREATE_SLOT):
            target = self.word(slot)
            need(not 0x400000 <= target < 0x9b4000, 'external callback import landing page')
            # Bounded decode sentinel on a declared foreign landing page. The
            # instruction hook stops before it; original IAT/code never changes.
            self.put(target, b'\xc3')
        for depth in range(MAX_DEPTH):
            start = CB_BASE + depth * STRIDE
            self.u.mem_map(start, 0x14000)
            self.u.mem_write(start, b'\xda' * 0x14000)
        self.md.topology()

    def code(self, u, pc, size, user):
        super().code(u, pc, size, user)
        if self.frames and pc != base.RETURN and pc not in self.targets:
            runs = self.frames[-1]['instruction_runs']
            if runs and runs[-1]['va'] == pc:
                runs[-1]['count'] += 1
            else:
                runs.append(dict(va=pc, count=1))
            self.frames[-1]['count'] += 1
            need(self.frames[-1]['count'] <= 100000, 'bounded original callback instructions')

    def write(self, u, access, pointer, size, value, user):
        if self.frames:
            frame = self.frames[-1]
            start = frame['stack_start']
            owned = self.window_owner
            # Callback writes stay on its own stack, captured lParam buffer, or
            # its original MAIN object. Outer stacks and unrelated globals fail.
            need(start + 4096 <= pointer and pointer + size <= start + 0x11000 or
                 frame['shadow'] <= pointer and pointer + size <= frame['shadow'] + frame['packet']['data_bytes'] or
                 owned <= pointer and pointer + size <= owned + 0x1110,
                 'callback write has current stack/data/MAIN ownership')
        super().write(u, access, pointer, size, value, user)

    def bind_window(self, owner, module, hwnd=0):
        need(owner and module and not self.frames and not self.window_owner, 'one declared window owner lifetime')
        self.owned(owner, 0x1110)
        self.window_owner, self.window_module, self.window_handle = owner, module, hwnd

    def run_generator(self, gen):
        try:
            request = next(gen)
            while True:
                response = self.owner.call(*request)
                request = gen.send(response)
        except StopIteration:
            return

    def drive(self):
        need(not self.pending and not self.frames, 'single MAIN original root drive')
        self.lane = 0
        self.u.context_restore(self.ctx[0])
        while not self.done[0]:
            self.owner.check()
            self.u.emu_start(self.reg('EIP'), 0, count=50000, timeout=250000)
            pc = self.reg('EIP')
            if pc in (base.RETURN, self.stop):
                self.done[0] = True
            elif pc in self.targets:
                self.run_generator(self.api(self.targets[pc]))
        self.ctx[0] = self.u.context_save()

    def api(self, slot):
        if slot == CREATE_SLOT:
            need(not self.frames and self.window_owner and self.window_module, 'original pending creation with bound current MAIN/module')
            sp = self.reg('ESP')
            args = [self.word(sp + 4 + 4 * i) for i in range(12)]
            need(self.word(sp) == 0x4504d5 and args[:4] == [0, 0x7a2628, 0x7a2628, 0x90000000] and
                 args[8:] == [0, 0, self.window_module, self.window_owner] and
                 self.string(args[1]) == b'Cross Hermit\0', 'original CreateWindowExA frame and owned class/module')
            row = dict(name='CreateWindowExA', slot=slot, sp=sp, ret=self.word(sp), args=args,
                       before=self.state(), wire_start=len(self.owner.trace))
            self.records.append(row)
            ptd = self.thread_ptd[0]
            if ptd:
                yield from self.sync(ptd)
                actual = yield ('MEM_READ', self.native(ptd), 116)
                need(actual['hex'] == self.read(ptd, 116).hex(), 'actual current MAIN PTD before synchronous creation')
                row['current_native_PTD'] = actual
            reply = yield ('CreateWindowExA', *args)
            need(reply['result'] and reply['result'] == self.window_handle, 'actual callback HWND equals original CreateWindowExA return')
            self.reg('EAX', reply['result'])
            self.reg('ESP', sp + 52)
            self.reg('EIP', row['ret'])
            row.update(native_leaf=reply, value=reply['result'], after=self.state(), wire_end=len(self.owner.trace))
            return
        if slot not in IMPORTS and slot not in CLEANUP_IMPORTS:
            need(not self.frames, 'unadmitted platform leaf inside original callback')
            yield from super().api(slot)
            return
        need(self.frames and self.lane == 0, 'callback API inside original MAIN callback')
        frame = self.frames[-1]
        packet = frame['packet']
        name, argc = self.slots[slot]
        sp, ret = self.reg('ESP'), self.word(self.reg('ESP'))
        args = [self.word(sp + 4 + 4 * i) for i in range(argc)]
        if name != 'PostQuitMessage':
            need(args[0] == packet['hwnd'], 'current callback HWND')
        cid = packet['callback_id']
        row = dict(name=name, slot=slot, sp=sp, ret=ret, args=args,
                   callback_id=cid, before=self.state(), wire_start=len(self.owner.trace))
        self.records.append(row)
        frame['API_calls'].append(row)
        if name == 'PostQuitMessage':
            need(packet['message'] == 2 and args == [0], 'original destruction quit notification only')
            reply = yield ('CB_POST_QUIT', cid, 0)
        elif name == 'RemovePropA':
            need(packet['message'] in (2, 130) and args[1] == 0x594ab4 and self.read(args[1], 10) == PROPERTY,
                 'original property removal during current window destruction')
            reply = yield ('CB_REMOVE_PROP', cid, args[0])
            need(reply['result'] in (0, self.window_owner) and reply['observed_property'] == 0, 'actual property removal readback')
        elif name in ('GetPropA', 'SetPropA'):
            need(args[1] == 0x594ab4 and self.read(args[1], 10) == PROPERTY, 'original fixed property name')
            if name == 'GetPropA':
                reply = yield ('CB_GET_PROP', cid, args[0])
                need(reply['result'] in (0, self.window_owner), 'property is current original MAIN or absent')
            else:
                need(args[2] == self.window_owner, 'original MAIN opaque property')
                reply = yield ('CB_SET_PROP', cid, args[0], args[2])
                need(reply['result'] == 1 and reply['observed_property'] == self.window_owner, 'actual original property installed')
        elif name == 'GetWindowLongA':
            need(args[1] in (4, 0xfffffffc), 'original callback window-long index')
            reply = yield ('CB_GET_LONG', cid, *args)
            if args[1] == 0xfffffffc:
                need(reply['result'] == ENTRY and reply['reverse_translated'] == 1 and reply['host_result'], 'owned WNDPROC projection')
        else:
            expected = [packet['hwnd'], packet['message'], packet['wParam'],
                        frame['shadow'] if packet['data_bytes'] else packet['lParam']]
            need(args == expected, 'exact original DefWindowProc arguments')
            before = self.read(frame['shadow'], packet['data_bytes'])
            need(before.hex() == frame['data_hex'], 'no untransported guest lParam writes')
            reply = yield ('CB_DEFAULT', cid, *args[:3], packet['lParam'])
            need(reply['before_hex'] == before.hex(), 'actual default-procedure input bytes')
            after = bytes.fromhex(reply['after_hex'])
            need(len(after) == len(before), 'complete default-procedure output bytes')
            self.put(frame['shadow'], after)
            frame['data_hex'] = after.hex()
        self.reg('EAX', reply['result'])
        self.reg('ESP', sp + 4 + 4 * argc)
        self.reg('EIP', ret)
        row.update(native_leaf=reply, value=reply['result'], after=self.state(), wire_end=len(self.owner.trace))

    def callback(self, packet):
        need(self.window_owner and self.window_module, 'current window inputs bound before callback')
        need(packet['guest_entry'] == ENTRY and packet['lane'] == self.lane == 0, 'original MAIN WNDPROC entry')
        need(packet['callback_id'] == len(self.callbacks) + 1 <= MAX_CALLBACKS, 'original callback sequence')
        depth = len(self.frames)
        need(packet['depth'] == depth + 1 <= MAX_DEPTH, 'bounded callback depth')
        need(packet['parent_callback_id'] == (self.frames[-1]['packet']['callback_id'] if depth else 0), 'callback parent continuity')
        need(packet['hwnd'] and (not self.window_handle or packet['hwnd'] == self.window_handle), 'current original HWND')
        ptd = self.thread_ptd[0]
        if ptd:
            need(packet['tls_slot'] != 0xffffffff and packet['tls_error'] == 0 and
                 packet['tls_value'] == packet['tls_tracked_value'] == self.native(ptd) and
                 packet['ptd_bytes'] == 116 and packet['ptd_hex'] == self.read(ptd, 116).hex(),
                 'actual same MAIN TLS and full live PTD at callback entry')
        else:
            need(packet['tls_slot'] == 0xffffffff and packet['tls_value'] == packet['tls_tracked_value'] == 0 and
                 packet['ptd_bytes'] == 0 and packet['ptd_hex'] == '', 'explicit no tracked TLS in declared offline fixture')
        kind, length = DATA.get(packet['message'], ('opaque', 0))
        need(packet['message'] != 131 or packet['wParam'] == 0, 'NCCALCSIZE extended payload unadmitted')
        raw = bytes.fromhex(packet['data_hex'])
        need((packet['data_kind'], packet['data_bytes'], len(raw)) == (kind, length, length), 'complete recognized lParam payload')
        if length:
            need(packet['lParam'], 'actual nonnull lParam data')
        if kind == 'CREATESTRUCTA':
            need(struct.unpack_from('<II', raw) == (self.window_owner, self.window_module), 'actual creation MAIN/module identity')
        if kind == 'WINDOWPOS':
            need(struct.unpack_from('<I', raw)[0] == packet['hwnd'], 'actual WINDOWPOS HWND')
        self.window_handle = packet['hwnd']
        start, saved = CB_BASE + depth * STRIDE, self.u.context_save()
        shadow = start + 0x12000
        buffers = self.read(start, 0x14000)
        caller = self.state()
        outer_stack = self.read(base.cold.old.STACK, 65536)
        original = self.read(0x400000, 0x1ff000)
        stop = self.stop
        self.stop = None
        frame = dict(packet=dict(packet), stack_start=start, shadow=shadow, data_hex=raw.hex(),
                     suspended_caller=caller, declared_ABI_not_host_register_capture=True,
                     instruction_runs=[], API_calls=[], count=0)
        self.callbacks.append(frame)
        self.frames.append(frame)
        try:
            self.put(start, b'\xda' * 0x14000)
            sp = start + 0x10000
            args = [packet['hwnd'], packet['message'], packet['wParam'], shadow if length else packet['lParam']]
            self.put(sp, struct.pack('<5I', base.RETURN, *args))
            self.put(shadow, raw)
            # Retain the full declared guest FP/SIMD/segment/control state;
            # only ABI argument/entry registers differ from the suspended call.
            for key, value in dict(EIP=ENTRY, ESP=sp, EFLAGS=0x202).items():
                self.reg(key, value)
            frame['entry'] = self.state()
            while self.reg('EIP') != base.RETURN:
                self.owner.check()
                self.u.emu_start(self.reg('EIP'), 0, count=50000, timeout=250000)
                if self.reg('EIP') in self.targets:
                    self.run_generator(self.api(self.targets[self.reg('EIP')]))
            result = self.reg('EAX')
            need(self.reg('ESP') == sp + 20, 'original callback stdcall return')
            need(all(self.reg(k) == caller['cpu'][k] for k in ('EBP', 'EBX', 'ESI', 'EDI')), 'original callback callee-saved ABI')
            need(self.read(base.cold.old.STACK, 65536) == outer_stack, 'suspended original MAIN stack unchanged')
            need(self.read(0x400000, len(original)) == original, 'original code/imports/constants unchanged')
            need(self.read(start, 4096) == b'\xda' * 4096 and
                 self.read(start + 0x11000, 4096) == b'\xda' * 4096 and
                 self.read(shadow + length, 0x2000 - length) == b'\xda' * (0x2000 - length), 'callback stack/data guards')
            frame.update(result=result, returned=self.state())
        finally:
            self.frames.pop()
            self.stop = stop
            self.u.context_restore(saved)
            self.put(start, buffers)
            frame['restored_caller'] = self.state()
            need(frame['restored_caller']['cpu'] == caller['cpu'], 'all CPU57 caller fields restored')
            need(self.read(start, len(buffers)) == buffers, 'callback scratch restored')
        return result
