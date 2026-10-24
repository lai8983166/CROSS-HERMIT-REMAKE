"""Independent source model for isolated original path packets (not unit movement)."""
import hashlib
import struct
from tools.tactics_exit_emulation import SOURCE, SOURCE_SHA256

RANGES = ((0x437C90, 0x437D10), (0x437E40, 0x4385A0),
          (0x438610, 0x4387F0), (0x438860, 0x438D00),
          (0x4396E0, 0x439D10), (0x427990, 0x427B70),
          (0x427C90, 0x427DE0), (0x43BFA0, 0x43C1D0),
          (0x56CE80, 0x56CE83), (0x56CEC0, 0x56CF18))
TERRAIN = ((1, 1, 1, 1), (0, 0, 1, 0), (0, 1, 0, 1), (2, 2, 2, 2))


def source_contract():
    raw = SOURCE.read_bytes()
    if hashlib.sha256(raw).hexdigest() != SOURCE_SHA256:
        raise ValueError('original source identity')
    return dict(source_sha256=SOURCE_SHA256, ranges=[dict(start=a, end=b,
                sha256=hashlib.sha256(raw[a-0x400000:b-0x400000]).hexdigest()) for a, b in RANGES],
                neighbors=[list(struct.unpack_from('<hhi', raw, 0x5FF910-0x400000+i*8)) for i in range(8)],
                directions=[list(struct.unpack_from('<hh', raw, 0x5FF95C-0x400000+i*4)) for i in range(10)],
                barrier_base=struct.unpack_from('<i', raw, 0x5FF908-0x400000)[0],
                terrain=[list(row) for row in TERRAIN], expansion_limit=1001,
                declared_input_pool=True, game_function_results_stubbed=False,
                actual_unit_movement=False, native_scene_or_thread_connection=False)


def validate_case(c):
    if not isinstance(c, dict) or set(c) != {'name', 'grid', 'occupied', 'start', 'goal', 'mode', 'avoid', 'kind', 'direction'}:
        raise ValueError('exact declared path case fields')
    grid = c['grid']
    if not isinstance(c['name'], str) or not c['name'] or not isinstance(grid, list) or not 1 <= len(grid) <= 64:
        raise ValueError('case identity/grid')
    if not isinstance(grid[0], str) or not 1 <= len(grid[0]) <= 64 or any(not isinstance(r, str) or len(r) != len(grid[0]) or set(r)-set('0123') for r in grid):
        raise ValueError('rectangular declared terrain')
    w, h = len(grid[0]), len(grid)
    def cell(p):
        return isinstance(p, list) and len(p) == 2 and all(type(v) is int for v in p) and 0 <= p[0] < w and 0 <= p[1] < h
    if not cell(c['start']) or not cell(c['goal']) or not isinstance(c['occupied'], list) or any(not cell(p) for p in c['occupied']):
        raise ValueError('declared in-bounds cells')
    if len({tuple(p) for p in c['occupied']}) != len(c['occupied']):
        raise ValueError('duplicate occupancy')
    if type(c['mode']) is not int or c['mode'] not in range(5) or type(c['avoid']) is not bool:
        raise ValueError('terrain mode/occupancy switch')
    if c['kind'] not in ('search', 'direct', 'ray') or type(c['direction']) is not int or c['direction'] not in range(10):
        raise ValueError('declared operation/direction')
    if c['kind'] == 'ray' and c['direction'] not in (1, 2, 3, 4, 6, 7, 8, 9):
        raise ValueError('ray requires original nonzero keypad direction')
    return w, h


def oracle(c, contract=None):
    """Model uses coordinates/costs only, never guest addresses or executor output."""
    w, h = validate_case(c)
    s = contract or source_contract()
    start, goal = tuple(c['start']), tuple(c['goal'])
    mode = 0 if c['mode'] == 4 else c['mode']
    occupied = {tuple(p) for p in c['occupied']}
    def passable(p):
        return 0 <= p[0] < w and 0 <= p[1] < h and s['terrain'][int(c['grid'][p[1]][p[0]])][mode] != 0
    def clear(a, b):
        dx, dy = abs(b[0]-a[0]), abs(b[1]-a[1])
        sx, sy = 1 if b[0] >= a[0] else -1, 1 if b[1] >= a[1] else -1
        x, y = a
        error = 0
        for _ in range(max(dx, dy)):
            if dx < dy:
                y += sy
                error += dx
                if error >= dy: x += sx; error -= dy
            else:
                x += sx
                error += dy
                if error >= dx: y += sy; error -= dx
            if not passable((x, y)) or (c['avoid'] and (x, y) in occupied): return False
        return True
    result = dict(result=0, waypoints=[], popped=[], reopened=0, improved_open=0,
                  cost=None, limit_hit=False, workspace_clean=True)
    if c['kind'] == 'direct':
        if clear(start, goal): result.update(result=1, waypoints=[list(goal)])
        return result
    if c['kind'] == 'ray':
        dx, dy = s['directions'][c['direction']]
        p = start
        while True:
            q = p[0]+dx, p[1]+dy
            if not (0 <= q[0] < w and 0 <= q[1] < h) or not clear(start, q): break
            p = q
        if p != start: result.update(result=1, waypoints=[list(p)])
        return result
    # Original special case does NOT reject an impassable destination.
    if not passable(goal):
        result.update(result=1, waypoints=[list(goal)])
        return result
    nodes = {start: dict(g=0, h=(goal[0]-start[0])**2+(goal[1]-start[1])**2, parent=None, open=True)}
    queue = [start]
    def insert(p):
        score = nodes[p]['g']+nodes[p]['h']
        i = 0
        while i < len(queue) and nodes[queue[i]]['g']+nodes[queue[i]]['h'] < score: i += 1
        queue.insert(i, p)  # New equal f-score precedes existing nodes.
    while queue:
        p = queue.pop(0)
        result['popped'].append(list(p))
        n = nodes[p]
        if p == goal:
            chain = [p]
            while nodes[chain[-1]]['parent'] is not None: chain.append(nodes[chain[-1]]['parent'])
            chain.reverse()
            waypoints = []
            origin = 0
            while origin < len(chain)-1 and len(waypoints) < 100:
                best = origin+1
                if best < len(chain)-1:
                    for j in range(best, len(chain)):
                        if not clear(chain[origin], chain[j]): break
                        best = j
                waypoints.append(list(chain[best]))
                origin = best
            result.update(result=1, waypoints=waypoints, cost=n['g'])
            return result
        for dx, dy, normal_cost in s['neighbors']:
            q = p[0]+dx, p[1]+dy
            if q == p or q == n['parent'] or not (0 <= q[0] < w and 0 <= q[1] < h): continue
            step = normal_cost
            if q != goal:
                if not passable(q): step = s['barrier_base']**2
                if c['avoid'] and q in occupied: step = 100
            g = n['g']+step
            if q not in nodes:
                nodes[q] = dict(g=g, h=(goal[0]-q[0])**2+(goal[1]-q[1])**2, parent=p, open=True)
                insert(q)
            elif g < nodes[q]['g']:
                if nodes[q]['open']:
                    queue.remove(q)
                    result['improved_open'] += 1
                else: result['reopened'] += 1
                nodes[q].update(g=g, parent=p, open=True)
                insert(q)
        n['open'] = False
        if len(result['popped']) >= s['expansion_limit']:
            result.update(result=-1, limit_hit=True, workspace_clean=False)
            return result
    return result


def corpus():
    cases = []
    def add(name, grid, start, goal, **kw):
        c = dict(name=name, grid=grid, occupied=[], start=start, goal=goal, mode=0, avoid=False, kind='search', direction=0)
        c.update(kw); validate_case(c); cases.append(c)
    add('same_cell', ['000', '000', '000'], [1, 1], [1, 1])
    add('open_diagonal', ['000000']*6, [0, 0], [5, 5])
    add('open_reverse', ['000000']*6, [5, 5], [0, 0])
    add('blocked_destination', ['00000', '00001', '00000'], [0, 0], [4, 1])
    add('wall_gap', ['001000', '001000', '000000', '001000', '001000'], [0, 1], [5, 1])
    add('full_wall_penalty', ['00100']*5, [0, 2], [4, 2])
    add('blocked_start', ['1000', '0000', '0000'], [0, 0], [3, 2])
    for mode in range(5):
        add('terrain_mode_'+str(mode), ['00200', '00100', '00300', '00100'], [0, 1], [4, 1], mode=mode)
    for avoid in (False, True):
        add('occupancy_'+str(avoid), ['000000']*5, [0, 2], [5, 2], occupied=[[1, 2], [2, 2], [3, 2], [5, 2]], avoid=avoid)
        add('occupancy_overrides_barrier_'+str(avoid), ['00100']*5, [0, 2], [4, 2], occupied=[[2, 2]], avoid=avoid)
    for i, goal in enumerate(([4, 2], [4, 4], [2, 4], [0, 4], [0, 2], [0, 0], [2, 0], [4, 0], [2, 2])):
        add('direct_octant_'+str(i), ['00000']*5, [2, 2], list(goal), kind='direct')
    add('direct_blocked', ['00000', '00100', '00000'], [0, 1], [4, 1], kind='direct')
    add('direct_occupied', ['00000']*3, [0, 1], [4, 1], kind='direct', avoid=True, occupied=[[3, 1]])
    for d in (1, 2, 3, 4, 6, 7, 8, 9):
        add('ray_'+str(d), ['0000000']*7, [3, 3], [3, 3], kind='ray', direction=d)
    add('ray_immediate_block', ['000', '001', '000'], [1, 1], [1, 1], kind='ray', direction=6)
    # Deterministic LCG, independent of Python's random version/global RNG.
    state = 0xC205
    for i in range(40):
        rows = []
        for y in range(8):
            row = ''
            for x in range(9):
                state = (1664525*state+1013904223) & 0xFFFFFFFF
                row += '1' if state >> 28 < 5 else ('2' if state >> 28 == 5 else '0')
            rows.append(row)
        add('generated_'+str(i), rows, [i % 9, i % 8], [(8-i) % 9, (7-i) % 8], mode=i % 5,
            avoid=bool(i % 2), occupied=[[4, y] for y in range(1, 7)])
    add('expansion_limit', ['0'*35+'1'+'0'*4]*40, [0, 0], [39, 39])
    return cases
