"""Original path segment -> next tile -> fixed-point position, in declared isolation."""
import argparse
import hashlib
import json
import struct
import types
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EBX, UC_X86_REG_ECX, UC_X86_REG_EDX, UC_X86_REG_ESI, UC_X86_REG_EDI, UC_X86_REG_EBP, UC_X86_REG_ESP, UC_X86_REG_EIP, UC_X86_REG_EFLAGS, UC_X86_REG_FPCW
from tools import battle_pathfinding_emulation as parent
from tools.battle_pathfinding import RANGES as PATH_RANGES, source_contract as path_contract

ROOT, SOURCE, need, sha = parent.ROOT, parent.SOURCE, parent.need, parent.sha
CTRL, RECORD, ANIM = 0x11000000, 0x11200000, 0x11300000
UNIT = CTRL+0x80AEC
REGIONS = parent.REGIONS+((CTRL, 0x10A000), (RECORD, 0x1000), (ANIM, 0x1000))
EXTRA_RANGES = ((0x476680, 0x476CF0), (0x470250, 0x470620), (0x4707B0, 0x470D80), (0x47D930, 0x47DEC0),
                (0x47DEC0, 0x47E400), (0x47A8E0, 0x47A940), (0x43B8B0, 0x43B9E0),
                (0x490B30, 0x490CD0), (0x468D10, 0x468D80), (0x4698A0, 0x469950),
                (0x465040, 0x465140), (0x415040, 0x415070), (0x56CFCC, 0x56CFF3),
                (0x56D800, 0x56DB21), (0x5711B0, 0x5711C4), (0x576847, 0x576C00),
                (0x57C900, 0x57D000))
RANGES = PATH_RANGES+EXTRA_RANGES
ROOTS = parent.ROOTS | {0x476680, 0x47D930, 0x47DA30, 0x47DBD0, 0x47DEC0, 0x470250}
REGS = dict(EAX=UC_X86_REG_EAX, EBX=UC_X86_REG_EBX, ECX=UC_X86_REG_ECX, EDX=UC_X86_REG_EDX,
            ESI=UC_X86_REG_ESI, EDI=UC_X86_REG_EDI, EBP=UC_X86_REG_EBP, ESP=UC_X86_REG_ESP,
            EIP=UC_X86_REG_EIP, EFLAGS=UC_X86_REG_EFLAGS, FPCW=UC_X86_REG_FPCW)


def source_contract():
    raw = SOURCE.read_bytes()
    previous = path_contract()
    constants = {hex(a): dict(hex=raw[a-0x400000:a-0x400000+4].hex(), value=struct.unpack_from('<f', raw, a-0x400000)[0])
                 for a in (0x592778, 0x592774, 0x592770, 0x59AC28, 0x5924CC, 0x5924C4, 0x59C670)}
    return dict(parent=previous, extra_code=[dict(start=a, end=b, sha256=sha(raw[a-0x400000:b-0x400000])) for a, b in EXTRA_RANGES],
                constants=constants, angle_tables=[dict(pointer=a, hex=raw[a-0x400000:a-0x400000+36].hex()) for a in (0x618D80, 0x618DA4)],
                declared_animation_resource_gate=-1, declared_controller_and_record=True,
                declared_mode0_terrain='classes0/3 use requested terrain_rate; classes1/2 remain zero',
                game_or_math_function_results_stubbed=False, native_scene_or_world_frame=False)


def validate(c):
    need(set(c) == {'name', 'path', 'speed', 'terrain_rate', 'status', 'frames', 'blocker_speed'}, 'declared movement fields')
    parent.validate_case(c['path'])
    need(c['path']['kind'] == 'search' and c['path']['mode'] == 0, 'declared source path search/mode')
    need(type(c['speed']) is int and 1 <= c['speed'] <= 999, 'movement speed')
    need(type(c['terrain_rate']) is int and 1 <= c['terrain_rate'] <= 200, 'declared terrain rate')
    need(type(c['status']) is int and c['status'] in (0, 7), 'supported scaling status')
    need(type(c['frames']) is int and 1 <= c['frames'] <= 512, 'bounded movement frames')
    need(type(c['blocker_speed']) is int and 0 <= c['blocker_speed'] <= 999, 'declared occupant speed/owner')
    need(len(c['path']['occupied']) <= 8, 'bounded occupant input')


class MovementMachine(parent.PathMachine):
    def __init__(self, c):
        validate(c); super().__init__(c['path']); self.input = c
        for at, size in REGIONS[len(parent.REGIONS):]: self.uc.mem_map(at, size)
        # Embedded MAP shares only read-only input pointers with the search MAP.
        self.uc.mem_write(CTRL+0x3D68, bytes(self.uc.mem_read(parent.MAP, 0x27000)))
        self.put(CTRL+0x3D68+0x8C, parent.TERR)
        # Same terrain rate is used for the source mode0 table, with 0 blocked preserved.
        for tile in range(4):
            self.put(parent.TERR+tile*76+12, c['terrain_rate'] if tile in (0, 3) else 0)
        self.put(UNIT, 1, 'H'); self.put(UNIT+0x258, RECORD); self.put(UNIT+0x44, ANIM)
        self.put(UNIT+0x293, 7, 'B')
        self.put(ANIM+0x48, -1, 'h'); self.put(UNIT+0x14, c['status'], 'B')
        self.put(RECORD+0x2E, c['speed'], 'H'); self.put(RECORD+0x30, 0, 'B')
        if c['blocker_speed']:
            self.put(CTRL+0xDC8EC, len(c['path']['occupied']))
            for i, (bx, by) in enumerate(c['path']['occupied']):
                other = UNIT+(i+1)*0x520; rec = RECORD+(i+1)*0x100
                self.put(other, 1, 'H'); self.put(other+0x258, rec); self.put(rec+0x2E, c['blocker_speed'], 'H')
                self.put(other+0x2EC, (bx*32+16)*65536); self.put(other+0x2F0, (by*16+8)*65536)
                self.put(CTRL+0xDC8F0+i*4, other)
        x, y = c['path']['start']; gx, gy = c['path']['goal']
        self.put(UNIT+0x2EC, (x*32+16)*65536); self.put(UNIT+0x2F0, (y*16+8)*65536)
        self.put(UNIT+0x4D0, gx*32+16, 'h'); self.put(UNIT+0x4D2, gy*16+8, 'h')
        self.uc.reg_write(UC_X86_REG_FPCW, 0x27F)
        self.entries = {}
        self.coordinate_writes = 0

    def code(self, uc, at, size, context):
        self.path_code(uc, at, size, context)
        if at in {a for a, _ in EXTRA_RANGES} or at in (0x47D930, 0x47DA30, 0x47DBD0, 0x47DEC0, 0x470A50):
            self.entries[hex(at)] = self.entries.get(hex(at), 0)+1

    path_code = types.FunctionType(parent.PathMachine.code.__code__, dict(parent.PathMachine.code.__globals__, RANGES=RANGES))
    base_call = types.FunctionType(parent.PathMachine.call.__code__, dict(parent.PathMachine.call.__globals__, ROOTS=ROOTS))
    snapshot = types.FunctionType(parent.PathMachine.snapshot.__code__, dict(parent.PathMachine.snapshot.__globals__, REGIONS=REGIONS))

    def write_hook(self, uc, access, at, size, value, context):
        if UNIT <= at and at+size <= UNIT+0x520:
            if at < UNIT+0x2F4 and at+size > UNIT+0x2EC: self.coordinate_writes += 1
            self.writes += 1; self.write_hash.update(struct.pack('<IIQ', at, size, value & 0xFFFFFFFFFFFFFFFF)); return
        super().write_hook(uc, access, at, size, value, context)

    def cpu(self): return {name: self.uc.reg_read(reg) for name, reg in REGS.items()}

    def call(self, entry, args=(), receiver=CTRL):
        before = self.cpu(); row = self.base_call(entry, args, receiver); after = self.cpu()
        for name in ('EBX', 'ESI', 'EDI', 'EBP'): need(before[name] == after[name], 'original callee-saved register '+name)
        row.update(cpu_before=before, cpu_after=after)
        return row

    def unit(self): return bytes(self.uc.mem_read(UNIT, 0x520)).hex()

    def run(self):
        initial = self.snapshot(); roots = []
        roots.append(self.call(0x437C90, (UNIT+0x3E0,), parent.OBJECT))
        c = self.input; p = c['path']; x, y = p['start']; gx, gy = p['goal']
        roots.append(self.call(0x437E40, (x, y, gx, gy, UNIT+0x3E0, 0, int(p['avoid'])), parent.OBJECT))
        need(roots[-1]['result'] == 1, 'source path accepted')
        path_hex = bytes(self.uc.mem_read(UNIT+0x3E0, 236)).hex()
        steps = []; stop = 'frame_budget'
        for i in range(c['frames']):
            before = self.unit()
            calls = [self.call(0x476680, (UNIT, 0))]
            phase = self.get(UNIT+0x293, 'B')
            steps.append(dict(index=i, before_hex=before, after_hex=self.unit(), calls=calls, phase=phase))
            if phase in (3, 4, 8): stop = {3:'arrived', 4:'retry_boundary', 8:'next_tile_blocked'}[phase]; break
        cleanup = self.call(0x439C60, receiver=parent.OBJECT+0x18)
        final = self.snapshot(); owned = self.lists()
        return dict(input=c, initial=initial, final=final, roots=roots, path_hex=path_hex, steps=steps, stop=stop, cleanup=cleanup,
                    final_ownership=owned, entries=dict(sorted(self.entries.items())), instructions=self.instructions, writes=self.writes,
                    code_trace_sha256=self.code_hash.hexdigest(), write_trace_sha256=self.write_hash.hexdigest(),
                    game_or_math_results_stubbed=False, OS_input_submitted=False, original_coordinate_write_count=self.coordinate_writes,
                    host_unit_coordinates_changed_after_initialization=False)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('--out', required=True); a = p.parse_args()
    from tools.battle_unit_movement import corpus
    out = ROOT/a.out; need(not out.exists(), 'fresh immutable movement output'); cases = []
    for c in corpus():
        row = MovementMachine(c).run(); cases.append(row); print(c['name'], row['stop'], len(row['steps']), flush=True)
    parent.save(a.out, dict(schema_version=1, source_contract=source_contract(), cases=cases, R3_complete=False, R4_complete=False, R6_complete=False))
