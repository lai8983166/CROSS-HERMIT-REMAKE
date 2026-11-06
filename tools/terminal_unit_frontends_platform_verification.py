"""Independent CRT/D3D8 transaction boundary checker (no source-effect oracle).

Raw native addresses/uninitialized OS bytes are declared external inputs. API
requests, ownership, ABI, output extents and every host action are reconstructed
from the separate Replay's current CPU/RAM. GDI/TLS are deliberately unsupported.
The caller independently authenticates initial inputs, executable, helper builds,
file bytes and projection policy; this module alone is not a platform proof.
"""
import copy
import hashlib
import struct

from unicorn import x86_const as x86

IMPORTS = {
    0x592234: ('EnterCriticalSection', 4, 0x5770D3),
    0x592238: ('LeaveCriticalSection', 4, 0x5770F4),
    0x592144: ('HeapAlloc', 12, 0x57810C),
    0x59218C: ('HeapValidate', 12, 0x570170),
    0x592258: ('HeapFree', 12, 0x578915),
    0x592190: ('IsBadReadPtr', 8, 0x570018),
    0x592244: ('IsBadWritePtr', 8, 0x570030),
    0x592214: ('GetCurrentDirectoryA', 8, 0x42AC7A),
    0x5921EC: ('CreateFileA', 28, 0x42AC9C),
    0x5921F0: ('GetFileSize', 8, 0x42AD0D),
    0x5921E8: ('ReadFile', 20, 0x42AD82),
    0x592270: ('CloseHandle', 4, 0x42ADA5),
    0x59212C: ('HeapCreate', 12, 0x57B9EA),
    0x5922AC: ('GetVersionExA', 4, 0x57B7CE),
    0x59227C: ('InitializeCriticalSection', 4, None),
    0x592280: ('DeleteCriticalSection', 4, None),
    0x592174: ('HeapDestroy', 4, 0x57BB44),
}
HEAP = 0x61001000
LOCK_INIT = {0x80A498: 0x576F6F, 0x80A4C8: 0x576F7C,
             0x80A4B0: 0x576F89, 0x80A480: 0x576F95}
LOCK_DELETE = {0x80A4B0: 0x577015, 0x80A4C8: 0x577022,
               0x80A498: 0x57702F, 0x80A480: 0x57703B}
GPU_POP = {80: 32, 56: 12, 64: 20, 68: 8, 8: 4}
FILE_SIZES = {'data\\adv\\bin\\Gybc_00.bin': 524312,
              'data\\adv\\bin\\sc001.bin': 262168,
              'data\\adv\\bin\\sc002.bin': 262168,
              'data\\Tactics\\common.bin': 1793036,
              'data\\DxAnim\\b0a.bin': 1492764,
              'data\\DxAnim\\a0a.bin': 1308312}


def need(condition, message):
    if not condition:
        raise ValueError('platform: ' + message)


def word(raw, offset=0):
    return struct.unpack_from('<I', raw, offset)[0]


def pointer(value):
    need(type(value) is int and 0 < value < 0xFFFFFFFF, 'valid x86 opaque identity')
    return value


class Effects:
    """Predict ordered actions without changing Replay or consulting effects."""
    def __init__(self, replay):
        self.r = replay
        self.actions = []
        self.pages = {p for a, b, _ in replay.u.mem_regions()
                      for p in range(a, b+1, 4096)}
        self.writable = {p for a, b, perm in replay.u.mem_regions() if perm & 2
                         for p in range(a, b+1, 4096)}
        self.owned = []

    def map(self, address, size, fresh=False):
        need(address % 4096 == size % 4096 == 0 and size > 0, 'aligned bounded map')
        pages = set(range(address, address+size, 4096))
        need(not fresh or not pages & self.pages, 'fresh allocation mapping')
        self.actions.append(dict(kind='mem_map', address=address, bytes=size, permission=7))
        self.pages.update(pages)
        self.writable.update(pages)

    def map_new(self, address, size):
        need(0 < size <= 0x200000 and 0 <= address < address+size <= 0x100000000,
             'bounded output mapping')
        for p in range(address & -4096, (address+size+4095) & -4096, 4096):
            if p not in self.pages:
                self.map(p, 4096)

    def put(self, address, raw, map_new=False):
        if map_new:
            self.map_new(address, len(raw))
        need(raw and all(p in self.writable for p in range(address & -4096,
             (address+len(raw)+4095) & -4096, 4096)), 'output entirely mapped')
        self.actions.append(dict(kind='mem_write', address=address, hex=raw.hex()))

    def returns(self, sp, ret, pop, value):
        for name, v in (('EAX', value & 0xFFFFFFFF), ('ESP', sp+4+pop), ('EIP', ret)):
            self.actions.append(dict(kind='reg_write', register=getattr(x86, 'UC_X86_REG_'+name), value=v))


class PlatformVerifier:
    """Strict stateful CRT/GPU plugin; one instance per fresh Replay.

    ``files`` is an independently authenticated exact-path -> bytes mapping.
    ``projection_policy(domain,native,guest)`` must approve any nonstandard
    historical GPU namespace/alias. Default supports only overlay, unit, COMMON.
    It must not consult event effects. Unknown boundaries are never accepted.
    """
    def __init__(self, row, original_code, files, projection_policy=None):
        self.code = bytes(original_code)
        initial = row['unit_frontends']['initial_platform']
        self.hello = copy.deepcopy(initial['CRT'])
        gpu = initial['GPU']
        need(self.hello['pointer_bytes'] == gpu['pointer_bytes'] == 4,
             'x86 native owners')
        need(self.hello['heap'] == self.hello['critical'] == 0 and
             self.hello['critical_hex'] == '' and self.hello['GPU_created'] is False and
             self.hello['window_created'] is False, 'cold headless CRT owner')
        need(gpu['window_visible'] is False and gpu['max_textures'] == 1024 and
             gpu['max_creates'] == 1024 and initial['device'] == gpu['device'],
             'bounded actual GPU owner/device')
        self.traces = {k: row[k+'_trace'] for k in ('CRT', 'GPU')}
        self.cursor = dict(CRT=0, GPU=0)
        self.files = dict(files)
        for path, raw in self.files.items():
            need(path in FILE_SIZES and type(raw) is bytes and len(raw) == FILE_SIZES[path],
                 'independent complete allowed file input')
        self.heap = 0
        self.locks, self.blocks, self.open_files, self.textures = {}, {}, {}, {}
        self.lock_spins = {}
        self.native_thread = None
        self.depth = self.allocations = self.creates = 0
        self.projection_policy = projection_policy
        self.projections = {}
        self.reverse = {}
        self.used_projection = {}
        self.overlay_next = 0x64001000
        self.large_domains = []
        self.intervals = []
        ledger = row.get('typed_GPU_projection', [])
        if isinstance(ledger, dict):
            ledger = ledger['ledger']
        ledger = list(ledger) + row['unit_frontends'].get('image_input', {}).get('projection', [])
        ledger += row['unit_frontends'].get('minimap_input', {}).get('projection', [])
        for item in ledger:
            key = item['domain'], pointer(item['native'])
            guest = pointer(item['guest'])
            need(key not in self.projections or self.projections[key] == guest,
                 'consistent typed identity ledger')
            self.projections[key] = guest
        self.device_native = copy.deepcopy(initial['device'])
        self.device = self.identity('overlay', self.device_native, {80})
        self.methods = {p: 80 for p in self.device['methods'].values()}
        self.events = dict(CRT=0, GPU=0)

    def project(self, domain, native, bits_size=None):
        key = domain, pointer(native)
        need(key in self.projections, 'declared typed GPU identity')
        guest = self.projections[key]
        if key not in self.used_projection:
            count = sum(d == domain for d,p in self.used_projection)
            if domain.startswith('overlay-unit-frontends-'):
                pieces = domain.removeprefix('overlay-unit-frontends-').split('-')
                need(len(pieces) == 2 and all(s.isdecimal() for s in pieces), 'typed unit namespace')
                cache,index = map(int,pieces)
                need(0 <= cache < 2 and 0 <= index < 300, 'bounded unit namespace')
                base = 0x34000000+(cache*300+index)*0x20000
                if bits_size is not None:
                    if bits_size > 0x10000:
                        need(len(self.large_domains) < 40, 'bounded large surface projections')
                        self.large_domains.append(domain)
                        expected = 0x3B000000+(len(self.large_domains)-1)*0x40000
                    else:
                        expected = base+0x10000
                else:
                    need(count < 15, 'bounded unit interface identity slots')
                    expected = base+(count+1)*0x1000
            elif domain.startswith('overlay-battle-exit-common-'):
                index = int(domain.removeprefix('overlay-battle-exit-common-'))
                need(0 <= index < 580 and count < 31, 'bounded COMMON identity slots')
                expected = 0x20000000+index*0x80000+(0x20000 if bits_size is not None else (count+1)*0x1000)
            elif domain == 'overlay':
                expected = self.overlay_next
                self.overlay_next += 0x100000
                need(expected < 0x70000000, 'bounded original overlay projection cursor')
            else:
                need(self.projection_policy and self.projection_policy(domain,native,guest),
                     'unsupported historical identity projection requires independent policy')
                expected = guest
            need(guest == expected, 'independent deterministic typed projection address')
            self.used_projection[key] = guest
        prior = self.reverse.get(guest)
        need(prior is None or prior == key or
             (self.projection_policy and self.projection_policy(domain, native, guest)),
             'cross-domain identity alias refused')
        self.reverse[guest] = key
        return guest

    def identity(self, domain, native, slots):
        need(set(native) == {'pointer', 'vtable', 'methods'} and
             set(native['methods']) == {str(s) for s in slots}, 'typed complete COM identity')
        return dict(pointer=self.project(domain, native['pointer']),
                    vtable=self.project(domain, native['vtable']),
                    methods={str(s): self.project(domain, native['methods'][str(s)]) for s in sorted(slots)})

    def consume(self, channel, op, **args):
        i = self.cursor[channel]
        trace = self.traces[channel]
        need(i < len(trace), 'bounded '+channel+' wire cursor')
        t = trace[i]
        need(t['request'] == dict(id=i+1, op=op, **args) and
             t['reply']['id'] == i+1 and t['reply']['ok'] is True,
             'exact ordered '+channel+' request/reply '+op)
        self.cursor[channel] += 1
        return t['reply']['result']

    def locate(self, p, n=1):
        found = [(a, b) for a, b in self.blocks.items() if a <= p < p+n <= a+b['bytes']]
        need(len(found) == 1, 'live allocation ownership and exact range')
        return found[0]

    def sync(self, replay, p):
        b = self.blocks[p]
        raw = replay.read(p, b['bytes'])
        need(self.consume('CRT', 'sync', pointer=b['native'], hex=raw.hex()) ==
             dict(pointer=b['native'], hex=raw.hex()), 'whole native heap synchronization')
        return raw

    def observers(self, replay, channel, end):
        """Only side-effect-free, independently owned full readbacks may fill gaps."""
        while self.cursor[channel] < end:
            t = self.traces[channel][self.cursor[channel]]
            q = t['request']
            if channel == 'CRT':
                found = [p for p, b in self.blocks.items() if b['native'] == q.get('pointer')]
                need(len(found) == 1 and q['op'] in ('sync', 'readback'), 'owned CRT observer only')
                p = found[0]
                if q['op'] == 'sync':
                    self.sync(replay, p)
                else:
                    raw = replay.read(p, self.blocks[p]['bytes'])
                    need(self.consume('CRT', 'readback', pointer=q['pointer']) ==
                         dict(pointer=q['pointer'], hex=raw.hex()), 'entire CRT observer bytes')
            else:
                matches = [t for t in self.textures.values() if t['native'] == q.get('pointer')]
                need(q['op'] == 'readback' and len(matches) == 1 and not matches[0]['locked'],
                     'owned unlocked GPU observer only')
                self.readback(matches[0])
        need(self.cursor[channel] == end, 'exact observer cursor')

    def crt_slot(self, replay, pc):
        matches = [slot for slot in IMPORTS if len(self.code) >= slot-0x400000+4 and
                   word(self.code, slot-0x400000) == pc]
        if not matches:
            return None
        need(len(matches) == 1 and word(replay.read(matches[0], 4)) == pc,
             'unchanged original CRT IAT target')
        return matches[0]

    def handles(self, replay, event):
        return self.crt_slot(replay, event['pc']) is not None or event['pc'] in self.methods

    def validate_event(self, replay, event):
        need(event['before_CPU'] == replay.cpu() and event['pc'] == replay.cpu()['EIP'],
             'current independent architectural CPU at boundary')
        slot = self.crt_slot(replay, event['pc'])
        channel = 'CRT' if slot is not None else 'GPU'
        need(slot is not None or event['pc'] in self.methods, 'unsupported boundary (GDI/TLS not implemented)')
        wire = event['wire']
        need(set(wire) == {'CRT', 'GPU', 'GDI', 'TLS'} and
             all(type(v) is list and len(v) == 2 and 0 <= v[0] <= v[1] for v in wire.values()),
             'complete bounded boundary wire intervals')
        for name in wire:
            if name != channel:
                need(wire[name][0] == wire[name][1], 'no foreign-channel calls at boundary')
        for name in ('CRT', 'GPU'):
            self.observers(replay, name, wire[name][0])
        effects = Effects(replay)
        if slot is not None:
            value, sp, ret, pop = self.crt(replay, slot, effects)
        else:
            value, sp, ret, pop = self.gpu(replay, self.methods[event['pc']], event['pc'], effects)
        # CRT canonical critical-section outputs occur after the source leaf's
        # register return writes; crt() has already emitted that exact order.
        need(self.cursor[channel] == wire[channel][1], 'entire API wire interval consumed')
        expected_changes = {k: v for k, v in dict(EAX=value & 0xFFFFFFFF,
                            ESP=sp+4+pop, EIP=ret).items() if replay.cpu()[k] != v}
        need(event['CPU_changes'] == expected_changes and event['stop'] is False and
             event['continues_guest'] is False, 'exact stdcall return architectural changes')
        need(event['effects'] == effects.actions, 'independently predicted exact ordered host effects')
        for interval in effects.owned:
            if interval not in replay.mutable:
                replay.mutable.append(interval)
        self.events[channel] += 1

    def crt(self, r, slot, e):
        name, pop, caller = IMPORTS[slot]
        cpu = r.cpu()
        sp = cpu['ESP']; ret = word(r.read(sp, 4))
        a = [word(r.read(sp+4+i, 4)) for i in range(0, pop, 4)]
        need(caller is None or ret == caller, 'original CRT return address '+name)
        canonical = None
        if name == 'HeapCreate':
            need(a == [0,4096,0] and self.heap == 0 and word(r.read(0x80AB28,4)) == 0,
                 'fresh original heap initialization')
            q = self.consume('CRT','heap_create',flags=0,initial=4096,maximum=0)
            need(set(q) == {'pointer'}, 'heap create result shape')
            self.heap = pointer(q['pointer']); value = HEAP
        elif name == 'GetVersionExA':
            need(a == [cpu['EBP']-0x98], 'OSVERSIONINFOA original local')
            before = r.read(a[0],148); need(word(before) == 148, 'version structure size')
            q = self.consume('CRT','version',hex=before.hex()); raw = bytes.fromhex(q['hex'])
            need(set(q) == {'value','hex'} and q['value'] == 1 and len(raw) == 148 and word(raw) == 148 and
                 word(raw,4) >= 5 and word(raw,16) == 2, 'modern Windows OS input')
            e.put(a[0],raw); value = 1
        elif name == 'InitializeCriticalSection':
            need(a[0] in LOCK_INIT and LOCK_INIT[a[0]] == ret and a[0] not in self.locks,
                 'original unique static lock initialization')
            q = self.consume('CRT','initialize',guest=a[0]); raw = bytes.fromhex(q['hex'])
            native = pointer(q['pointer'])
            need(set(q) == {'pointer','hex'} and native not in self.locks.values() and len(raw) == 24 and
                 word(raw,4) == 0xFFFFFFFF and raw[8:20] == bytes(12), 'initialized native lock structure')
            self.locks[a[0]] = native; e.put(a[0],raw); canonical = (a[0],raw); value = 0
            self.lock_spins[a[0]] = word(raw,20)
        elif name == 'DeleteCriticalSection':
            need(a[0] in self.locks and LOCK_DELETE[a[0]] == ret and self.depth == 0,
                 'original balanced static lock destruction')
            need(self.consume('CRT','delete',guest=a[0],pointer=self.locks.pop(a[0])) == dict(value=1), 'native lock deletion')
            del self.lock_spins[a[0]]
            value = 0
        elif name == 'HeapDestroy':
            need(a == [HEAP] and self.heap and not self.blocks and not self.locks and not self.depth,
                 'empty owned heap destruction')
            need(self.consume('CRT','heap_destroy',heap=self.heap) == dict(value=1), 'native heap destruction')
            self.heap = 0; value = 1
        elif name in ('EnterCriticalSection','LeaveCriticalSection'):
            need(a == [0x80A4B0] and a[0] in self.locks, 'owned original lock9')
            self.depth += 1 if name.startswith('Enter') else -1
            need(0 <= self.depth <= 4, 'balanced bounded lock depth')
            q = self.consume('CRT','enter' if name.startswith('Enter') else 'leave',critical=self.locks[a[0]])
            raw = bytes.fromhex(q['critical_hex'])
            need(set(q) == {'depth','critical_hex'} and q['depth'] == self.depth and len(raw) == 24 and
                 word(raw,8) == self.depth and word(raw,20) == self.lock_spins[a[0]],
                 'native lock recursion structure/depth')
            # LockCount encodes Windows-version-specific contention state. It
            # remains an explicit opaque OS input, not a guessed depth formula.
            owner = word(raw,12)
            if self.depth:
                need(owner != 0 and (self.native_thread is None or self.native_thread == owner),
                     'owned single-helper-thread critical section')
                self.native_thread = owner
            else:
                need(owner == 0, 'unowned native lock after balanced final leave')
            e.put(a[0],raw); canonical = (a[0],raw); value = 0
        elif name == 'HeapAlloc':
            need(a[:2] == [HEAP,0] and self.heap and self.depth and
                 0 < a[2] <= 0x200000 and len(self.blocks) < 32, 'owned locked bounded allocation')
            q = self.consume('CRT','alloc',heap=self.heap,flags=0,bytes=a[2])
            raw = bytes.fromhex(q['hex']); native = pointer(q['pointer'])
            need(set(q) == {'pointer','bytes','hex'} and q['bytes'] == a[2] == len(raw) and all(b['native'] != native for b in self.blocks.values()),
                 'fresh complete opaque native allocation bytes')
            value = 0x50001000+self.allocations*0x200000; self.allocations += 1
            need(value+a[2] <= 0x61000000, 'bounded heap projection before native tokens')
            self.blocks[value] = dict(native=native,bytes=a[2])
            e.map(value,(a[2]+4095)&-4096,True); e.put(value,raw)
            e.owned.append((value,value+a[2]))
        elif name in ('HeapValidate','HeapFree','IsBadReadPtr','IsBadWritePtr'):
            check = name.startswith('IsBad')
            if check:
                need(a[1] == 32, 'original debug header pointer check extent')
                p,b = self.locate(a[0],a[1]); offset = a[0]-p
            else:
                need(a[:2] == [HEAP,0] and self.heap and self.depth, 'owned locked heap operation')
                p,b = self.locate(a[2]); need(p == a[2], 'exact raw heap block')
            raw = self.sync(r,p)
            if check:
                q = self.consume('CRT','badread' if name == 'IsBadReadPtr' else 'badwrite',
                                 pointer=b['native'],offset=offset,bytes=a[1])
                need(q == dict(value=0,pointer=b['native'],offset=offset,bytes=a[1]), 'native bounded pointer query')
                value = 0
            else:
                q = self.consume('CRT','validate' if name == 'HeapValidate' else 'free',
                                 heap=self.heap,flags=0,pointer=b['native'])
                need(q == dict(value=1,pointer=b['native'],before_hex=raw.hex()), 'native exact complete heap operation')
                if name == 'HeapFree':
                    del self.blocks[p]
                    # Guest allocation pages remain mapped, but original writes
                    # may no longer access this dead native allocation.
                    if (p,p+b['bytes']) in r.mutable:
                        r.mutable.remove((p,p+b['bytes']))
                value = 1
        elif name == 'GetCurrentDirectoryA':
            need(a == [260,0x7A0EBC], 'original MAX_PATH directory query')
            q = self.consume('CRT','directory',bytes=260); raw = bytes.fromhex(q['hex'])
            need(0 < q['value'] < 260 and len(raw) == q['value']+1 and raw[-1:] == b'\0' and
                 b'\0' not in raw[:-1], 'bounded complete native directory input')
            # Windows ANSI byte encoding is part of the raw OS input.
            need(raw[:-1].decode('mbcs') == self.hello['directory'], 'initial native working directory identity')
            e.put(a[1],raw); value = q['value']
        elif name == 'CreateFileA':
            path = self.text(r,a[0]).decode('ascii')
            need(path in self.files and a[1:] == [0x80000000,1,0,3,1,0] and not self.open_files,
                 'independent exact source path/read-only file flags')
            q = self.consume('CRT','open',path=path,access=a[1],share=a[2],security=a[3],
                             disposition=a[4],attributes=a[5],template=a[6])
            need(set(q) == {'handle'}, 'native file handle result shape')
            self.open_files[0x62001000] = dict(native=pointer(q['handle']),path=path); value = 0x62001000
        else:
            need(a[0] in self.open_files, 'owned live file handle')
            f = self.open_files[a[0]]; data = self.files[f['path']]
            if name == 'GetFileSize':
                need(a[1] == 0 and self.consume('CRT','size',handle=f['native'],high=0) ==
                     dict(value=len(data)), 'complete independent file size')
                value = len(data)
            elif name == 'CloseHandle':
                need(self.consume('CRT','file_close',handle=f['native']) == dict(value=1), 'owned file close')
                del self.open_files[a[0]]; value = 1
            else:
                need(name == 'ReadFile' and a[2] == len(data) and a[4] == 0, 'synchronous complete source read')
                p,b = self.locate(a[1],len(data)); need(a[1] == p+32, 'original debug user buffer offset')
                before = self.sync(r,p); after = before[:32]+data+before[32+len(data):]
                q = self.consume('CRT','read',handle=f['native'],pointer=b['native'],offset=32,bytes=len(data),overlapped=0)
                need(q == dict(value=1,read=len(data),pointer=b['native'],before_hex=before.hex(),after_hex=after.hex()),
                     'independent raw file bytes and all allocation padding')
                e.put(p,after); e.put(a[3],struct.pack('<I',len(data))); value = 1
        e.returns(sp,ret,pop,value)
        if canonical:
            p,raw = canonical; normalized = bytearray(raw)
            for off in (0,12,16):
                if word(raw,off) not in (0,0xFFFFFFFF):
                    struct.pack_into('<I',normalized,off,0x63000000+off+(p-0x80A480)*0x100)
            e.put(p,bytes(normalized))
        return value,sp,ret,pop

    @staticmethod
    def text(r,p):
        out = bytearray()
        for i in range(260):
            byte = r.read(p+i,1)[0]
            if byte == 0:
                return bytes(out)
            out.append(byte)
        raise ValueError('platform: unterminated bounded path')

    def surface(self, domain, native, size):
        maximum=(0x100000 if domain=='overlay' else 0x80000
                 if domain in ('unit-frontends-minimap-background','unit-frontends-minimap-fog') else 0x40000)
        need(0 < size <= maximum, 'complete bounded GPU surface')
        guest = self.project(domain,native,size)
        if domain.startswith('overlay-unit-frontends-'):
            pieces = domain.removeprefix('overlay-unit-frontends-').split('-')
            need(len(pieces) == 2 and all(s.isdecimal() for s in pieces), 'typed unit namespace')
            cache,index = map(int,pieces); need(0 <= cache < 2 and 0 <= index < 300,'two bounded unit caches')
            if size <= 0x10000:
                need(guest == 0x34000000+(cache*300+index)*0x20000+0x10000, 'unit small surface location')
            else:
                need(0x3B000000 <= guest < 0x3BA00000 and (guest-0x3B000000)%0x40000 == 0,
                     'bounded full large unit surface pool')
        elif domain.startswith('overlay-battle-exit-common-'):
            index = int(domain.removeprefix('overlay-battle-exit-common-'))
            need(0 <= index < 580 and guest == 0x20000000+index*0x80000+0x20000,
                 'full COMMON surface location')
        elif domain == 'overlay':
            need(0x64001000 <= guest < 0x70000000 and (guest-0x64001000)%0x100000 == 0,
                 'original overlay identity surface location')
        else:
            need(self.projection_policy and self.projection_policy(domain,native,guest),
                 'unsupported historical surface projection requires independent policy')
        need(all(not(a < guest+size and guest < b) for a,b in self.intervals), 'live surface alias refused')
        self.intervals.append((guest,guest+size))
        return guest

    def readback(self,t):
        need('upload' in t and not t['locked'], 'owned uploaded surface before readback')
        q = self.consume('GPU','readback',pointer=t['native']); raw = t['upload']
        need(q == dict(hr=0,unlock_hr=0,pitch=t['pitch'],hex=raw.hex(),
                       sha256=hashlib.sha256(raw).hexdigest()), 'entire GPU pitch/padding readback')

    def gpu(self,r,slot,pc,e):
        cpu = r.cpu(); sp = cpu['ESP']; bp = cpu['EBP']; ret = word(r.read(sp,4)); pop = GPU_POP[slot]
        a = [word(r.read(sp+4+i,4)) for i in range(0,pop,4)]
        callers = {80:(0x403C8A,),56:(0x403CBE,0x403A44),64:(0x40395E,),68:(0x4039D3,),8:(0x40378D,)}
        need(ret in callers[slot], 'original typed COM caller')
        table = word(r.read(a[0],4))
        need(word(r.read(table+slot,4)) == pc, 'actual current self/vtable/method dispatch')
        if slot == 80:
            need(a[0] == self.device['pointer'] and table == self.device['vtable'] and
                 a[3:7] == [1,0,25,1] and self.creates < 1024 and len(self.textures) < 1024,
                 'owned device original complete CreateTexture ABI')
            w,h = a[1:3]
            need(1 <= w <= 1024 and 1 <= h <= 512 and w&(w-1) == h&(h-1) == 0 and
                 (h <= 256 or w in (256,512)), 'source bounded power-of-two texture extent')
            q = self.consume('GPU','create',width=w,height=h,levels=1,usage=0,format=25,pool=1)
            need(set(q) == {'hr','texture'} and q['hr'] == 0, 'successful actual texture creation')
            native = pointer(q['texture']['pointer'])
            need(all(t['native'] != native for t in self.textures.values()), 'native texture lifetime not already live')
            candidates = [(d,g) for (d,p),g in self.projections.items() if p == native and
                          g not in self.textures and d != 'GDI']
            # A historical namespace may contain the same reused OS pointer.
            # The independent policy chooses among generations; effects do not.
            if len(candidates) != 1:
                candidates = [(d,g) for d,g in candidates if self.projection_policy and
                              self.projection_policy(d,native,g)]
            need(len(candidates) == 1, 'unambiguous typed native texture generation')
            domain,_ = candidates[0]; identity = self.identity(domain,q['texture'],{8,56,64,68})
            t = dict(native=native,identity=identity,domain=domain,width=w,height=h,locked=False,record=a[-1]-44)
            self.textures[identity['pointer']] = t; self.creates += 1
            for p in (identity['pointer'],identity['vtable'],*identity['methods'].values()):
                e.map_new(p,4)
            e.put(identity['pointer'],struct.pack('<I',identity['vtable']))
            for s,p in identity['methods'].items():
                e.put(identity['vtable']+int(s),struct.pack('<I',p)); self.methods[p] = int(s)
            e.put(a[-1],struct.pack('<I',identity['pointer']),True)
        else:
            need(a[0] in self.textures, 'owned live texture generation')
            t = self.textures[a[0]]
            need(table == t['identity']['vtable'] and word(r.read(t['record']+44,4)) == a[0],
                 'original record owns current texture')
            if slot == 56:
                need(a == [a[0],0,bp-(52 if ret == 0x403CBE else 36)], 'descriptor local ABI')
                q = self.consume('GPU','describe',pointer=t['native']); raw = bytes.fromhex(q['hex'])
                need(len(raw) == 32 and struct.unpack('<8I',raw) ==
                     (25,1,0,1,t['width']*t['height']*2,0,t['width'],t['height']) and
                     q == dict(hr=0,hex=raw.hex(),width=t['width'],height=t['height'],size=t['width']*t['height']*2),
                     'actual descriptor all fields')
                e.put(a[2],raw,True)
            elif slot == 64:
                need(a == [a[0],0,word(r.read(bp+8,4)),0,2048] and not t['locked'], 'owned original full LockRect ABI')
                q = self.consume('GPU','lock',pointer=t['native'],flags=2048); raw = bytes.fromhex(q['hex']); pitch=q['pitch']
                need(set(q) == {'hr','pitch','bits','hex'} and q['hr'] == 0 and
                     t['width']*2 <= pitch <= 4096 and pitch%2 == 0 and len(raw) == pitch*t['height'],
                     'actual complete native locked pitch/padding')
                if 'upload' in t:
                    need(raw==t['upload'],'same owned native texture retains whole prior upload before relock')
                if 'bits' in t:
                    old_interval=(t['bits'],t['bits']+t['length'])
                    need(old_interval in self.intervals,'same live texture owns its prior surface span')
                    self.intervals.remove(old_interval)
                bits = self.surface(t['domain'],pointer(q['bits']),len(raw))
                t.update(locked=True,bits=bits,pitch=pitch,length=len(raw))
                e.put(bits,raw,True); e.owned.append((bits,bits+len(raw)))
                e.put(a[2],struct.pack('<II',pitch,bits),True)
            elif slot == 68:
                need(a == [a[0],0] and t['locked'], 'owned locked texture original unlock ABI')
                raw = r.read(t['bits'],t['length'])
                need(self.consume('GPU','unlock',pointer=t['native'],hex=raw.hex()) ==
                     dict(hr=0,uploaded_sha256=hashlib.sha256(raw).hexdigest()), 'entire replay-derived GPU upload')
                t.update(locked=False,upload=raw); self.readback(t)
                interval = (t['bits'],t['bits']+t['length'])
                if interval in r.mutable:
                    r.mutable.remove(interval)
            else:
                need(a == [a[0]] and not t['locked'], 'owned unlocked original Release ABI')
                need(self.consume('GPU','release',pointer=t['native']) == dict(count=0), 'native final texture release')
                if 'bits' in t:
                    interval = (t['bits'],t['bits']+t['length']); self.intervals.remove(interval)
                    if interval in r.mutable: r.mutable.remove(interval)
                del self.textures[a[0]]
        e.returns(sp,ret,pop,0)
        return 0,sp,ret,pop

    def finish(self, replay, require_closed=True):
        for name in ('CRT','GPU'):
            end = len(self.traces[name])-(1 if require_closed else 0)
            self.observers(replay,name,end)
        if require_closed:
            need(not self.heap and not self.locks and not self.blocks and not self.open_files and
                 not self.depth and not self.textures, 'all original platform ownership naturally released')
            need(self.consume('CRT','close') == dict(all_owned_resources_released=True,
                 heap_destroyed=True,critical_deleted=True,open_files=0,allocations=0,depth=0,forced_cleanup=False),
                 'normal source-empty CRT owner close')
            need(self.consume('GPU','close') == dict(texture_releases=[],device_release_count=0,
                 factory_release_count=0,window_destroyed=True,all_owned_resources_released=True),
                 'normal source-empty GPU owner close')
        need(all(self.cursor[k] == len(v) for k,v in self.traces.items()), 'complete native transcript coverage')
        return dict(events=dict(self.events),wire=dict(self.cursor),CRT_GPU_only=True,
                    GDI_implemented=False,TLS_implemented=False,source_effects_used_as_oracle=False)
