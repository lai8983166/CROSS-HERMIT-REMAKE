"""Coordinate/float32 model of original AI movement phases 7, 8, 9."""
from copy import deepcopy
import math
import struct
from tools.battle_pathfinding import oracle as path_oracle, corpus as path_corpus


def f32(x): return struct.unpack('<f', struct.pack('<f', x))[0]
def div(x, d): return int(x/d)
def s16(x): return (x+32768) % 65536-32768


class Model:
    def __init__(self, c, contract):
        self.c, self.contract = c, contract
        self.unit = bytearray(0x520)
        self.put(0, 1, 'H'); self.put(0x44, 0x11300000); self.put(0x258, 0x11200000)
        self.put(0x293, 7, 'B'); self.put(0x14, c['status'], 'B')
        x, y = c['path']['start']; gx, gy = c['path']['goal']
        self.put(0x2EC, (x*32+16)*65536); self.put(0x2F0, (y*16+8)*65536)
        self.put(0x4D0, gx*32+16, 'h'); self.put(0x4D2, gy*16+8, 'h')
        predicted = path_oracle(c['path'])
        if predicted['result'] != 1: raise ValueError('declared successful path required')
        packet = bytearray(236); struct.pack_into('<HH', packet, 24, gx, gy); packet[28:30] = b'\xff\xff'
        if not predicted['popped']: packet[28:30] = bytes(c['path']['start'])
        struct.pack_into('<H', packet, 32, len(predicted['waypoints']))
        for i, p in enumerate(predicted['waypoints']): packet[34+i*2:36+i*2] = bytes(p)
        self.unit[0x3E0:0x4CC] = packet
        self.path_hex = packet.hex()
        self.last_events = []

    def get(self, off, fmt='I'): return struct.unpack_from('<'+fmt, self.unit, off)[0]
    def put(self, off, x, fmt='I'): struct.pack_into('<'+fmt, self.unit, off, s16(x) if fmt == 'h' else x)
    def pixels(self): return self.get(0x2EC, 'i') >> 16, self.get(0x2F0, 'i') >> 16
    def cell(self):
        x, y = self.pixels(); return div(x, 32), div(y, 16)
    def pair(self, off): return self.get(off, 'h'), self.get(off+2, 'h')
    def grid(self, off):
        x, y = self.pair(off); return div(x, 32), div(y, 16)
    def occupied(self, p): return list(p) in self.c['path']['occupied']
    def passable(self, p):
        rows = self.c['path']['grid']; x, y = p
        return 0 <= y < len(rows) and 0 <= x < len(rows[0]) and rows[y][x] in '03'
    def value(self, address): return self.contract['constants'][hex(address)]['value']

    def segment(self):
        self.last_events.append('segment')
        x, y = self.pixels(); self.put(0x28B, 255, 'B'); self.put(0x4D4, x, 'h'); self.put(0x4D6, y, 'h')
        cur, total = self.get(0x3FE, 'H'), self.get(0x400, 'H')
        if cur != total:
            gx, gy = self.unit[0x402+cur*2:0x404+cur*2]; self.put(0x3FE, cur+1, 'H')
        else:
            gx, gy = x, x  # Original 47D9D9/47D9E3 both read +4D4.
        self.put(0x4D8, gx*32+16, 'h'); self.put(0x4DA, gy*16+8, 'h')

    def next_tile(self):
        self.last_events.append('next_tile')
        current = self.cell(); origin = self.grid(0x4D4); goal = self.grid(0x4D8)
        if current == goal: raise ValueError('original next-tile assertion')
        dx, dy = abs(goal[0]-origin[0]), abs(goal[1]-origin[1])
        sx, sy = 1 if goal[0] >= origin[0] else -1, 1 if goal[1] >= origin[1] else -1
        x, y = origin; error = 0
        for _ in range(max(dx, dy)):
            found = (x, y) == current
            if dx < dy:
                y += sy; error += dx
                if error >= dy: x += sx; error -= dy
            else:
                x += sx; error += dy
                if error >= dx: y += sy; error -= dx
            if found: break
        self.put(0x4DC, x*32+16, 'h'); self.put(0x4DE, y*16+8, 'h')
        if not self.passable((x, y)): return 1
        if self.occupied((x, y)) and self.occupied(self.grid(0x4D0)):
            raise ValueError('nearest-free destination adjustment not in declared corpus')
        return 0

    def arrival(self):
        self.last_events.append('arrival')
        cell = self.cell()
        if cell != self.grid(0x4DC): return 0
        if cell != self.grid(0x4D8): return 4
        if self.get(0x3FE, 'H') != self.get(0x400, 'H'): return 3
        px, py = self.pixels(); tx, ty = self.pair(0x4DC)
        if abs(tx-px) > 2 or abs(ty-py) > 2: return 0
        if cell != self.grid(0x4D0): return 2
        return 1

    def angle(self, dy, dx):
        angle = math.atan2(dy, dx)
        degrees = f32(angle/self.value(0x592778))
        if degrees < 0: degrees = f32(degrees+self.value(0x59C670)+self.value(0x59C670))
        return angle, div(s16(int(degrees)), 1) % 360

    def move(self):
        self.last_events.append('move')
        px, py = self.pixels(); tx, ty = self.pair(0x4DC)
        angle, _ = self.angle(s16(ty-py), s16(tx-px)); angle = f32(angle)
        rate = self.c['terrain_rate'] if self.passable(self.cell()) else 50  # Original zero terrain rate fallback.
        speed = f32(self.c['speed']*self.value(0x59AC28))
        amount = f32(rate*self.value(0x59AC28)*speed)
        dx = f32(f32(math.cos(angle))*self.value(0x5924CC)*amount*self.value(0x5924CC))
        dy = f32(f32(math.sin(angle))*self.value(0x5924CC)*amount*self.value(0x5924CC))
        if self.c['status'] == 7:
            dx, dy = f32(dx*self.value(0x5924C4)), f32(dy*self.value(0x5924C4))
        dx, dy = min(abs(tx-px), dx), min(abs(ty-py), dy)
        ix, iy = int(f32(dx*65536)), div(int(f32(dy*65536)), 2)
        # Original stores integer->float32->integer after the identity 415040.
        ix, iy = int(f32(ix)), div(int(f32(int(f32(dy*65536)))), 2)
        sx, sy = self.grid(0x4D4); ex, ey = self.grid(0x4D8)
        _, heading = self.angle(ey-sy, ex-sx); self.put(0x4EC, heading, 'h')
        table = self.contract['angle_tables'][0 if heading % 90 in range(30, 61) else 1]
        direction = bytes.fromhex(table['hex'])[heading//11]
        if self.occupied(self.grid(0x4DC)) and self.cell() != self.grid(0x4DC):
            if not self.c['blocker_speed']: return
            if self.c['speed'] <= self.c['blocker_speed']: ix, iy = div(ix, 2), div(iy, 2)
        self.put(0x2EC, self.get(0x2EC, 'i')+ix, 'i'); self.put(0x2F0, self.get(0x2F0, 'i')+iy, 'i')
        self.put(0x4E2, self.get(0x4E2, 'h')+1, 'h')
        if self.get(0x54, 'h') != 3 or self.get(0x28A, 'B') != direction:
            self.put(0x28B, self.get(0x28A, 'B'), 'B'); self.put(0x28A, direction, 'B')
            self.put(0x4E2, 0, 'h')  # Original animation gate returns without resource reads.

    def step(self):
        self.last_events = []; phase = self.get(0x293, 'B')
        if self.get(0x4E0, 'h'):
            self.put(0x4E0, self.get(0x4E0, 'h')-1, 'h'); return
        if phase == 7: self.segment(); phase = 8
        if phase == 9:
            result = self.arrival()
            if result == 0: self.move()
            elif result == 1: phase = 3
            elif result == 2: phase = 4
            elif result == 3: self.segment(); phase = 8
            elif result == 4: phase = 8
        if phase == 8:
            result = self.next_tile()
            if result == 0: phase = 9
            elif result == 2: phase = 4
        self.put(0x293, phase, 'B')


def corpus():
    rows = []
    base = deepcopy(path_corpus()[1]); base.update(grid=['0000000']*7, start=[3, 3])
    def add(name, goal, **kw):
        p = deepcopy(base); p.update(name=name, goal=goal)
        row = dict(name=name, path=p, speed=500, terrain_rate=100, status=0, frames=256, blocker_speed=0)
        row.update(kw); rows.append(row); return row
    for i, point in enumerate(([3,0],[6,0],[6,3],[6,6],[3,6],[0,6],[0,3],[0,0])): add('direction_'+str(i), list(point))
    for speed in (1, 100, 999): add('speed_'+str(speed), [6, 3], speed=speed, frames=128)
    for rate in (25, 150, 200): add('terrain_'+str(rate), [6, 6], terrain_rate=rate)
    add('half_scale', [6, 6], status=7)
    row = add('wall_detour', [6, 2]); row['path'].update(start=[0,2], grid=['0010000', '0010000', '0010000', '0000000', '0010000', '0010000', '0010000'])
    row = add('blocked_destination', [6, 3]); row['path']['grid'] = ['0000000']*3+['0000001']+['0000000']*3
    row = add('blocking_wall', [6, 3]); row['path']['grid'] = ['0000100']*7
    for speed in (250, 750):
        row = add('ally_speed_'+str(speed), [6,3], blocker_speed=speed); row['path']['occupied'] = [[4,3]]
    row = add('missing_occupant_owner', [6,3], frames=8); row['path']['occupied'] = [[4,3]]
    return rows
