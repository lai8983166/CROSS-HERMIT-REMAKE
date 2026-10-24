"""Execute original search, smoothing, packet consumption and pool recycling."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
import struct
from unicorn import Uc, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_PROT_READ, UC_PROT_EXEC
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_ECX, UC_X86_REG_EIP, UC_X86_REG_ESP
from tools.battle_pathfinding import RANGES, TERRAIN, source_contract, validate_case, corpus
from tools.tactics_exit_emulation import ROOT, SOURCE

OBJECT, MAP, HEADER, TERR, OCC, OCC_PTR = 0x10000000, 0x10100000, 0x10200000, 0x10300000, 0x10400000, 0x10500000
LINKS, NODES, INDEX, PACKET, STACK, RETURN = 0x10600000, 0x10700000, 0x10800000, 0x10900000, 0x10A00000, 0x10B00000
REGIONS = ((OBJECT, 0x1000), (MAP, 0x27000), (HEADER, 0x7000), (TERR, 0x5000), (OCC, 0x3000),
           (OCC_PTR, 0x1000), (LINKS, 0xD000), (NODES, 0x1C000), (INDEX, 0x4000), (PACKET, 0x1000), (STACK, 0x10000))
ROOTS = {0x437C90, 0x437E40, 0x438AD0, 0x438BA0, 0x438860, 0x439C60}


def sha(b): return hashlib.sha256(b).hexdigest()
def need(ok, message):
    if not ok: raise ValueError(message)


class PathMachine:
    def __init__(self, case):
        self.case = case
        self.w, self.h = validate_case(case)
        source_contract()
        self.uc = Uc(UC_ARCH_X86, UC_MODE_32)
        raw = SOURCE.read_bytes()
        self.uc.mem_map(0x400000, (len(raw)+4095) & ~4095)
        self.uc.mem_write(0x400000, raw)
        self.uc.mem_protect(0x400000, (len(raw)+4095) & ~4095, UC_PROT_READ | UC_PROT_EXEC)
        for at, n in REGIONS: self.uc.mem_map(at, n)
        self.uc.mem_map(RETURN, 4096)
        # All these are declared isolation inputs, NOT an original constructor.
        self.put(OBJECT+0x48, self.w); self.put(OBJECT+0x4C, self.h)
        self.put(OBJECT+0xA0, INDEX); self.put(OBJECT+0xB0, MAP)
        self.put(MAP+0x2659C, HEADER); self.put(MAP+0x265A0, OCC_PTR); self.put(MAP+0x8C, TERR)
        self.put(HEADER+4, self.w, 'H'); self.put(HEADER+6, self.h, 'H'); self.put(OCC_PTR, OCC)
        for tile, modes in enumerate(TERRAIN):
            for mode, allowed in enumerate(modes): self.put(TERR+tile*76+12+mode*16, allowed)
        for y, row in enumerate(case['grid']):
            for x, tile in enumerate(row): self.put(HEADER+16+(y*self.w+x)*6, int(tile), 'B')
        for x, y in case['occupied']: self.put(OCC+1+(y*self.w+x)*2, 1, 'B')
        self.pool_size = self.w*self.h
        head = OBJECT+0x90
        self.put(head+4, LINKS)
        for i in range(self.pool_size):
            self.put(LINKS+i*12, head if i == 0 else LINKS+(i-1)*12)
            self.put(LINKS+i*12+4, LINKS+(i+1)*12 if i+1 < self.pool_size else 0)
            self.put(LINKS+i*12+8, NODES+i*28)
        self.code_hash = hashlib.sha256(); self.write_hash = hashlib.sha256()
        self.instructions = 0; self.writes = 0; self.visited = Counter(); self.popped = []; self.improved = 0; self.reopened = 0
        self.uc.hook_add(UC_HOOK_CODE, self.code)
        self.uc.hook_add(UC_HOOK_MEM_WRITE, self.write_hook)

    def put(self, at, n, fmt='I'): self.uc.mem_write(at, struct.pack('<'+fmt, n))
    def get(self, at, fmt='I'): return struct.unpack('<'+fmt, self.uc.mem_read(at, struct.calcsize(fmt)))[0]

    def code(self, uc, at, size, _):
        if at == RETURN: uc.emu_stop(); return
        need(any(a <= at < b for a, b in RANGES), 'undeclared original instruction '+hex(at))
        need(bytes(uc.mem_read(at, 1)) != b'\xcc', 'original assertion/padding reached '+hex(at))
        self.instructions += 1
        self.code_hash.update(struct.pack('<I', at))
        if at in {a for a, _ in RANGES} or at in (0x438610, 0x4388E0, 0x439B20, 0x439C20, 0x427D60, 0x427C90, 0x427D20): self.visited[hex(at)] += 1
        if at == 0x439C4F:
            link = uc.reg_read(UC_X86_REG_EAX)
            node = self.get(link+8)
            self.popped.append([self.get(node+2, 'h'), self.get(node+4, 'h')])
        if at == 0x427C90: self.improved += 1
        if at == 0x427D20: self.reopened += 1

    def write_hook(self, uc, access, at, size, value, _):
        mutable = ((OBJECT, OBJECT+0x100), (LINKS, LINKS+self.pool_size*12), (NODES, NODES+self.pool_size*28),
                   (INDEX, INDEX+self.pool_size*4), (PACKET, PACKET+0x100), (STACK, STACK+0x10000))
        need(any(a <= at and at+size <= b for a, b in mutable), 'forbidden original write '+hex(at))
        self.writes += 1
        self.write_hash.update(struct.pack('<IIQ', at, size, value & 0xFFFFFFFFFFFFFFFF))

    def call(self, entry, args=(), receiver=OBJECT):
        need(entry in ROOTS, 'undeclared audit root')
        sp = STACK+0xF000
        self.put(sp, RETURN)
        for i, arg in enumerate(args): self.put(sp+4+i*4, arg & 0xFFFFFFFF)
        self.uc.reg_write(UC_X86_REG_ESP, sp); self.uc.reg_write(UC_X86_REG_ECX, receiver)
        count = self.instructions
        self.uc.emu_start(entry, RETURN, timeout=60_000_000, count=10_000_000)
        need(self.uc.reg_read(UC_X86_REG_EIP) == RETURN, 'original root did not return')
        need(self.uc.reg_read(UC_X86_REG_ESP) == sp+4+len(args)*4, 'original ret/ESP mismatch')
        eax = self.uc.reg_read(UC_X86_REG_EAX)
        return dict(entry=entry, receiver=receiver, args=list(args), result=eax if eax < 0x80000000 else eax-0x100000000,
                    ESP_before=sp, ESP_after=self.uc.reg_read(UC_X86_REG_ESP), instructions=self.instructions-count)

    def snapshot(self): return [dict(pointer=a, bytes=n, hex=bytes(self.uc.mem_read(a, n)).hex()) for a, n in REGIONS]

    def lists(self):
        found = []
        for head in (OBJECT+0x5C, OBJECT+0x68, OBJECT+0x90):
            p = self.get(head+4); seen = []
            while p:
                need(p not in seen and p >= LINKS and (p-LINKS) % 12 == 0 and p < LINKS+self.pool_size*12, 'bounded own pool lists')
                # Pop-from-free deliberately leaves stale prev of remaining head.
                if head != OBJECT+0x90: need(self.get(p) == (head if not seen else seen[-1]), 'original list back-link')
                seen.append(p); p = self.get(p+4)
            found.append(dict(head=head, links=seen))
        flat = [p for row in found for p in row['links']]
        need(len(flat) == self.pool_size and len(set(flat)) == self.pool_size, 'all original pool nodes owned exactly once')
        return found

    def run(self):
        initial = self.snapshot()
        calls = [self.call(0x437C90, (PACKET,))]
        start, goal = self.case['start'], self.case['goal']
        kind = self.case['kind']
        if kind == 'ray':
            args = (*start, self.case['direction'], PACKET, self.case['mode'], int(self.case['avoid']))
            entry = 0x438BA0
        else:
            args = (*start, *goal, PACKET, self.case['mode'], int(self.case['avoid']))
            entry = 0x437E40 if kind == 'search' else 0x438AD0
        calls.append(self.call(entry, args))
        packet = bytes(self.uc.mem_read(PACKET, 236))
        count = self.get(PACKET+0x20, 'H')
        need(count <= 100, 'bounded compressed waypoint count')
        waypoints = [list(packet[0x22+i*2:0x24+i*2]) for i in range(count)]
        after_search = self.snapshot()
        owned_after_search = self.lists()
        # Consume only packets accepted by original call. Limit result leaves no usable packet.
        consume = []
        if calls[-1]['result'] == 1:
            for _ in range(count+2):
                self.put(PACKET+0xF0, 0xA55A, 'H'); self.put(PACKET+0xF2, 0x5AA5, 'H')
                row = self.call(0x438860, (PACKET, PACKET+0xF0, PACKET+0xF2))
                row.update(x=self.get(PACKET+0xF0, 'H'), y=self.get(PACKET+0xF2, 'H'), cursor=self.get(PACKET+0x1E, 'H'))
                consume.append(row)
        calls.append(self.call(0x439C60, receiver=OBJECT+0x18))
        final = self.snapshot()
        owned_final = self.lists()
        need(not owned_final[0]['links'] and not owned_final[1]['links'], 'explicit original workspace recycling')
        for before, after in zip(initial, final):
            if before['pointer'] in (MAP, HEADER, TERR, OCC, OCC_PTR): need(before == after, 'read-only declared map/terrain/occupancy')
        return dict(input=self.case, initial=initial, after_search=after_search, final=final,
                    calls=calls, result=calls[1]['result'], packet_hex=packet.hex(), waypoints=waypoints, consume=consume,
                    popped=self.popped, improved_open=self.improved, reopened=self.reopened,
                    ownership_after_search=owned_after_search, ownership_final=owned_final,
                    instructions=self.instructions, writes=self.writes, code_trace_sha256=self.code_hash.hexdigest(),
                    write_trace_sha256=self.write_hash.hexdigest(), visited=dict(sorted(self.visited.items())),
                    game_function_results_stubbed=False, unit_coordinates_updated=False, OS_input_submitted=False)


def report():
    contract = source_contract(); cases = []
    for c in corpus():
        row = PathMachine(c).run(); cases.append(row)
        print(c['name'], row['result'], len(row['popped']), row['waypoints'], flush=True)
    return dict(schema_version=1, source_contract=contract, cases=cases,
                scope='isolated declared map/pool: original search, smoothing, consumption and recycling; no original scene/AI/movement integration',
                R3_complete=False, R4_complete=False, R6_complete=False)


def save(path, value):
    path = ROOT/path; need(not path.exists(), 'fresh immutable report path')
    path.write_bytes(gzip.compress(json.dumps(value, separators=(',', ':')).encode(), mtime=0))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--out', required=True); a = p.parse_args()
    need(not (ROOT/a.out).exists(), 'fresh path before execution'); save(a.out, report())
