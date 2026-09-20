# -*- coding: utf-8 -*-
"""DxAnim 共享解码库 (formats.md §10)

被 tools/unit_anim_export.py (单位档 {A..E}{0,1}A) 与 tools/fx_export.py (特效档 ##E)
共用：容器解析 / BMP 帧解码 / 块0～3 动画程序 / 块4 绘制描述符 / 块5 画布矩形。
"""
import struct


class DxAnimError(Exception):
    pass


def parse_dxanim(data: bytes):
    """容器级解析 + 自洽校验，返回块偏移表。

    校验: offs[0] == 8+4×块数; 偏移非递减 (相邻相等 = 空块); 头部总长 == 文件长度。
    (末块 块8 无 {len;n} 头 —— 前 4B 即数据, 不能对其做块长校验)
    """
    if len(data) < 12:
        raise DxAnimError(f'truncated DxAnim header: {len(data)} bytes')
    total, nblk = struct.unpack_from('<II', data, 0)
    if nblk < 1 or 8 + 4 * nblk > len(data):
        raise DxAnimError(f'invalid block count {nblk} for {len(data)} byte file')
    offs = list(struct.unpack_from(f'<{nblk}I', data, 8))
    if offs[0] != 8 + 4 * nblk:
        raise DxAnimError(f'offset table not self-consistent: offs[0]={offs[0]} != {8 + 4 * nblk}')
    if any(offs[i] > offs[i + 1] for i in range(nblk - 1)):
        raise DxAnimError('block offsets not increasing')
    if len(data) != total:
        raise DxAnimError(f'file size {len(data)} != header total {total}')
    if offs[-1] > len(data):
        raise DxAnimError(f'last block offset {offs[-1]} exceeds file size {len(data)}')
    return offs


def parse_container(data: bytes, base: int):
    """通用档案容器 {u32 len; u32 n; u32 offs[n]} → (块长, 条数, 偏移列表)"""
    if base < 0 or base + 8 > len(data):
        raise DxAnimError(f'truncated container header @{base}')
    clen, n = struct.unpack_from('<II', data, base)
    if n > (len(data) - base - 8) // 4:
        raise DxAnimError(f'truncated container offset table @{base}: count={n}')
    offs = list(struct.unpack_from(f'<{n}I', data, base + 8))
    header_size = 8 + 4 * n
    if any(off < header_size for off in offs):
        raise DxAnimError(f'container entry overlaps header @{base}')
    if any(offs[i] > offs[i + 1] for i in range(n - 1)):
        raise DxAnimError(f'container offsets not increasing @{base}')
    return clen, n, offs


def block_bounds(data: bytes, offs, block: int):
    """返回顶层块的 ``[start, end)``；相邻相等表示合法空块。"""
    if block < 0 or block >= len(offs):
        raise DxAnimError(f'block index {block} outside 0..{len(offs) - 1}')
    start = offs[block]
    end = offs[block + 1] if block + 1 < len(offs) else len(data)
    if start > end or end > len(data):
        raise DxAnimError(f'invalid block {block} bounds {start}..{end}')
    return start, end


def _program_ranges(data: bytes, offs, block: int):
    """解析块0～3的条目范围，并剥离原档允许的末尾 0 填充。"""
    start, end = block_bounds(data, offs, block)
    if start == end:
        return []
    _clen, count, entry_offs = parse_container(data, start)
    if any(off > end - start for off in entry_offs):
        raise DxAnimError(f'block {block} entry offset exceeds block end')
    ranges = []
    for index, rel_start in enumerate(entry_offs):
        rel_end = entry_offs[index + 1] if index + 1 < count else end - start
        size = rel_end - rel_start
        padding = size % 10
        if padding:
            if padding > 2 or any(data[start + rel_end - padding:start + rel_end]):
                raise DxAnimError(
                    f'block {block} animation {index} has truncated 10-byte instruction: size={size}'
                )
            rel_end -= padding
        ranges.append((start + rel_start, start + rel_end))
    return ranges


def parse_instruction(raw: bytes, *, block=None, animation=None, pc=None):
    """解析一条 10B DxAnim 指令，不将打包描述符误作图片编号。"""
    if len(raw) != 10:
        where = f' block={block} animation={animation} pc={pc}'
        raise DxAnimError(f'truncated instruction ({len(raw)} bytes){where}')
    flags = raw[0]
    opcode = flags & 3
    instruction = {
        'opcode': opcode,
        'flags': flags,
        'terminal': bool(flags & 0x80),
        'arg_byte': raw[1],
        'arg0': struct.unpack_from('<h', raw, 2)[0],
        'arg1': struct.unpack_from('<h', raw, 4)[0],
        'arg2': struct.unpack_from('<h', raw, 6)[0],
        'arg3': struct.unpack_from('<h', raw, 8)[0],
        'raw': raw.hex(),
    }
    if opcode == 0:
        packed_high = struct.unpack_from('<H', raw, 6)[0]
        instruction['descriptors'] = [
            raw[2 + slot] | ((packed_high >> (slot * 4) & 0x0f) << 8)
            for slot in range(4)
        ]
        duration = struct.unpack_from('<h', raw, 8)[0]
        if duration <= 0:
            raise DxAnimError(
                f'invalid visible duration {duration} in block {block} animation {animation} pc {pc}'
            )
        instruction['duration_ticks'] = duration
    elif opcode == 1:
        instruction.update({
            'child_animation': struct.unpack_from('<h', raw, 2)[0],
            'x': struct.unpack_from('<h', raw, 4)[0],
            'y': struct.unpack_from('<h', raw, 6)[0],
        })
    elif opcode == 2:
        instruction['sound'] = struct.unpack_from('<h', raw, 8)[0]
    else:
        instruction.update({
            'repeat': raw[1],
            'jump': struct.unpack_from('<h', raw, 2)[0],
            'forward': bool(flags & 0x40),
        })
        if instruction['jump'] < 0:
            raise DxAnimError(
                f'negative jump {instruction["jump"]} in block {block} animation {animation} pc {pc}'
            )
    return instruction


def parse_program_blocks(data: bytes, offs=None):
    """解析块0～3的全部动画程序，返回 ``blocks[block][animation]``。"""
    offs = parse_dxanim(data) if offs is None else offs
    blocks = []
    for block in range(min(4, len(offs))):
        programs = []
        for animation, (start, end) in enumerate(_program_ranges(data, offs, block)):
            programs.append([
                parse_instruction(
                    data[pos:pos + 10], block=block, animation=animation, pc=(pos - start) // 10
                )
                for pos in range(start, end, 10)
            ])
        blocks.append(programs)
    while len(blocks) < 4:
        blocks.append([])
    return blocks


def parse_block4_descriptors(data: bytes, offs=None):
    """解析块4的 10B 绘制描述符。

    字段命名仅覆盖已被运行时代码证实的语义；其余原值保留，供后续研究与 Mod 使用。
    原档允许块尾最多 2B 的零填充。
    """
    offs = parse_dxanim(data) if offs is None else offs
    start, end = block_bounds(data, offs, 4)
    padding = (end - start) % 10
    if padding:
        if padding > 2 or any(data[end - padding:end]):
            raise DxAnimError(f'block 4 has truncated descriptor: size={end - start}')
        end -= padding
    descriptors = []
    for index, pos in enumerate(range(start, end, 10)):
        x, y, frame = struct.unpack_from('<hhh', data, pos)
        descriptors.append({
            'id': index,
            'x': x,
            'y': y,
            'frame': frame,
            'flags': data[pos + 6],
            'palette': data[pos + 7],
            'draw_group': struct.unpack_from('<h', data, pos + 8)[0],
            'raw': data[pos:pos + 10].hex(),
        })
    return descriptors


def resolve_visible_instruction(instruction, descriptors, *, block=0, animation=0, pc=0,
                                x=0, y=0, mirror_flags=0):
    """把 opcode0 的四个 12 位索引解析成按原引擎绘制顺序排列的图层。"""
    if instruction['opcode'] != 0:
        raise DxAnimError('only opcode 0 has visible descriptors')
    layers = []
    # FUN_40b0f0 从槽3倒序绘制到槽0；0xfff 是空槽。
    for slot in range(3, -1, -1):
        descriptor_id = instruction['descriptors'][slot]
        if descriptor_id == 0xfff:
            continue
        if descriptor_id >= len(descriptors):
            raise DxAnimError(
                f'descriptor {descriptor_id} out of range in block {block} animation {animation} pc {pc}'
            )
        descriptor = descriptors[descriptor_id]
        if descriptor['frame'] < 0:
            raise DxAnimError(
                f'negative frame {descriptor["frame"]} in descriptor {descriptor_id}'
            )
        layers.append({
            'frame': descriptor['frame'],
            'x': x + descriptor['x'],
            'y': y + descriptor['y'],
            'flip_x': bool(mirror_flags & 1),
            'flip_y': bool(mirror_flags & 2),
            'slot': slot,
            'descriptor': descriptor_id,
            'flags': descriptor['flags'],
            'palette': descriptor['palette'],
            'draw_group': descriptor['draw_group'],
        })
    return layers


def decode_bmp(data: bytes, s: int):
    """块6 内单帧 (标准 8bpp BMP, 内嵌调色板) → (w, h, 索引 bytes, 调色板[256][4 RGBA])"""
    if data[s:s + 2] != b'BM':
        raise DxAnimError(f'not a BMP frame @{s}: {data[s:s + 2]!r}')
    w, h = struct.unpack_from('<ii', data, s + 18)
    px_off = struct.unpack_from('<I', data, s + 10)[0]
    if px_off != 54 + 1024:
        raise DxAnimError(f'BMP pixel offset {px_off} != 54+1024 (no embedded 1024B palette)')
    stride = (w + 3) // 4 * 4
    rows = []
    for y in range(h):  # 底上行序 → 顶向下
        rows.append(data[s + px_off + y * stride: s + px_off + y * stride + w])
    idx = b''.join(reversed(rows))
    pal = [tuple(data[s + 54 + c * 4: s + 54 + c * 4 + 3]) + (0 if c == 0 else 255,)
           for c in range(256)]  # BGRX → 保留 BGR, 索引0 透明
    return w, h, idx, pal


def write_png(path: str, w: int, h: int, idx: bytes, pal) -> None:
    from PIL import Image
    import numpy as np
    a = np.frombuffer(idx, np.uint8).reshape(h, w)
    p = np.array(pal, np.uint8)  # (256,4) BGRA
    rgba = p[a][:, :, [2, 1, 0, 3]]  # → RGBA
    Image.fromarray(rgba).save(path)


def parse_block5_rects(data: bytes, b5: int, frame_count: int):
    """块5 = 帧数×8B 直排 (无头): (画布w, 画布h, 帧x, 帧y) i16 —— 与帧数校验"""
    if (len(data) - b5) < frame_count * 8:
        raise DxAnimError(f'block5 too small for {frame_count} frames')
    return [struct.unpack_from('<4h', data, b5 + i * 8) for i in range(frame_count)]


def frame_anchor(rect):
    """画布底中 = 脚底 → 画布底中在帧图像内的像素偏移 (cw/2 - fx, ch - fy)"""
    cw, ch, fx, fy = rect
    return {'x': cw / 2 - fx, 'y': ch - fy}


def _instance_key(instance):
    # ``serial`` is an allocation identity, not VM state.  Sustained effects
    # commonly loop by spawning the same short-lived child every cycle; keeping
    # the ever-increasing serial in the signature made those stable loops look
    # non-convergent forever.  Repeated structural keys are intentionally kept
    # in the surrounding tuple, so simultaneous identical children still
    # contribute their multiplicity.
    return (
        instance['block'], instance['animation'], instance['pc'],
        instance['wait'], instance['loop_remaining'], instance['x'], instance['y'],
        instance['mirror_flags'], instance['done'],
    )


def interpret_animation(data: bytes, block: int, animation: int, *, offs=None,
                        mirror_flags=0, max_ticks=10000, max_steps=100000):
    """离线解释一条 DxAnim 动画，输出渲染就绪的时间轴。

    opcode1 创建的块3实例与父实例共享时间轴；opcode2 的音效副作用被跳过；opcode3 按
    原运行时的重复计数与前/后跳转执行。状态重复时以 ``loop_from`` 标出稳定循环。
    """
    offs = parse_dxanim(data) if offs is None else offs
    programs = parse_program_blocks(data, offs)
    descriptors = parse_block4_descriptors(data, offs)
    if block < 0 or block >= len(programs) or animation < 0 or animation >= len(programs[block]):
        raise DxAnimError(f'animation block={block} id={animation} does not exist')

    serial = 0

    def new_instance(program_block, program_animation, x, y, depth):
        nonlocal serial
        if program_block >= len(programs) or program_animation >= len(programs[program_block]):
            raise DxAnimError(
                f'child animation block={program_block} id={program_animation} does not exist'
            )
        result = {
            'serial': serial,
            'block': program_block,
            'animation': program_animation,
            'pc': 0,
            'wait': 0,
            'loop_remaining': 0,
            'x': x,
            'y': y,
            'depth': depth,
            'mirror_flags': mirror_flags,
            'done': False,
        }
        serial += 1
        return result

    instances = [new_instance(block, animation, 0, 0, 0)]
    operation_count = 0

    def current_instruction(instance):
        program = programs[instance['block']][instance['animation']]
        if instance['pc'] < 0 or instance['pc'] >= len(program):
            raise DxAnimError(
                f'pc {instance["pc"]} outside block {instance["block"]} '
                f'animation {instance["animation"]} ({len(program)} instructions)'
            )
        return program[instance['pc']]

    def prepare(instance):
        """执行零时长控制指令，停在可见 opcode0 或终止。"""
        nonlocal operation_count
        spawned = []
        while not instance['done'] and instance['wait'] == 0:
            operation_count += 1
            if operation_count > max_steps:
                raise DxAnimError(
                    f'animation did not converge within {max_steps} operations: '
                    f'block={block} animation={animation}'
                )
            instruction = current_instruction(instance)
            opcode = instruction['opcode']
            if opcode == 0:
                instance['wait'] = instruction['duration_ticks']
                break
            if opcode == 1:
                child_animation = instruction['child_animation']
                if child_animation != -1 and instance['depth'] < 8:
                    dx = instruction['x']
                    dy = instruction['y']
                    if mirror_flags & 1:
                        dx = -dx
                    if mirror_flags & 2:
                        dy = -dy
                    spawned.append(new_instance(
                        3, child_animation, instance['x'] + dx, instance['y'] + dy,
                        instance['depth'] + 1,
                    ))
                if instruction['terminal']:
                    instance['done'] = True
                else:
                    instance['pc'] += 1
                continue
            if opcode == 2:
                if instruction['terminal']:
                    instance['done'] = True
                else:
                    instance['pc'] += 1
                continue

            if instance['loop_remaining'] == 0:
                repeat = instruction['repeat']
                instance['loop_remaining'] = 0x7f if repeat == 0x7f else repeat + 1
            remaining = instance['loop_remaining']
            if remaining != 0x7f and remaining <= 1:
                instance['loop_remaining'] = 0
                if instruction['terminal']:
                    instance['done'] = True
                else:
                    instance['pc'] += 1
                continue
            if remaining != 0x7f:
                instance['loop_remaining'] -= 1
            delta = instruction['jump'] if instruction['forward'] else -instruction['jump']
            if delta == 0:
                raise DxAnimError(
                    f'zero-distance loop in block {instance["block"]} '
                    f'animation {instance["animation"]} pc {instance["pc"]}'
                )
            instance['pc'] += delta
        return spawned

    def prepare_all():
        pending = list(instances)
        while pending:
            instance = pending.pop(0)
            children = prepare(instance)
            if children:
                instances.extend(children)
                pending.extend(children)

    prepare_all()
    ticks = []
    seen = {}
    loop_tick = None
    for tick in range(max_ticks):
        instances[:] = [instance for instance in instances if not instance['done']]
        if not instances:
            break
        state = tuple(_instance_key(instance) for instance in instances)
        if state in seen:
            loop_tick = seen[state]
            break
        seen[state] = tick

        layers = []
        for instance in instances:
            instruction = current_instruction(instance)
            if instruction['opcode'] == 0:
                layers.extend(resolve_visible_instruction(
                    instruction, descriptors,
                    block=instance['block'], animation=instance['animation'], pc=instance['pc'],
                    x=instance['x'], y=instance['y'], mirror_flags=instance['mirror_flags'],
                ))
        ticks.append(layers)

        for instance in list(instances):
            if instance['done']:
                continue
            instruction = current_instruction(instance)
            if instruction['opcode'] != 0:
                raise DxAnimError('interpreter internal error: instance not prepared')
            instance['wait'] -= 1
            if instance['wait'] == 0:
                if instruction['terminal']:
                    instance['done'] = True
                else:
                    instance['pc'] += 1
        prepare_all()
    else:
        raise DxAnimError(
            f'animation did not converge or loop within {max_ticks} ticks: '
            f'block={block} animation={animation}'
        )

    # 无限循环指令首次到达时，VM 的内部 repeat 状态会从 0 变为 0x7f；若这造成两个完全
    # 相同的可见周期，折叠为单周期并从 0 循环，避免官方 JSON 重复保存同一组画面。
    if loop_tick and loop_tick * 2 == len(ticks) and ticks[:loop_tick] == ticks[loop_tick:]:
        ticks = ticks[:loop_tick]
        loop_tick = 0

    steps = []
    loop_from = None
    for tick, layers in enumerate(ticks):
        # 循环点必须落在 step 边界；即使前后画面相同也不能跨边界压缩。
        force_split = loop_tick is not None and tick == loop_tick
        if steps and steps[-1]['layers'] == layers and not force_split:
            steps[-1]['duration_ticks'] += 1
        else:
            if force_split:
                loop_from = len(steps)
            steps.append({'duration_ticks': 1, 'layers': layers})
    if loop_tick == 0:
        loop_from = 0
    return {'steps': steps, 'loop_from': loop_from, 'duration_ticks': len(ticks)}


def parse_block0_anims(data: bytes, b0: int):
    """块0 动画定义表 → [{id, records: [{frame, dur}]}]

    10B 记录 (i16 画布w, b, i16, i16, i16 时长):
      b <= -2 → 帧索引(-b); b == -1 → 空白帧 (隐身 dur, 特效的显隐演出语义);
      控制/终止记录 (a=32643 终止符 / a=2049 头 / b>=0) 跳过不进序列。
    """
    _, n, aoffs = parse_container(data, b0)
    aoffs = aoffs + [struct.unpack_from('<I', data, b0)[0]]
    anims = []
    for ai in range(n):
        s, e = b0 + aoffs[ai], b0 + aoffs[ai + 1]
        recs = []
        for k in range((e - s) // 10):
            cw, b, c, d_field, dur = struct.unpack_from('<5h', data, s + k * 10)
            if cw == 32643 or cw == 2049 or b >= 0:
                continue
            frame = -b if b <= -2 else -1
            recs.append({'frame': frame, 'dur': dur})
        anims.append({'id': ai, 'records': recs})
    return anims


def load_frames(data: bytes, offs):
    """块6 全帧解码 → (foffs, [(w,h,idx,pal), ...])"""
    b6 = offs[6]
    _, nf, foffs = parse_container(data, b6)
    frames = [decode_bmp(data, b6 + foffs[i]) for i in range(nf)]
    return foffs, frames


def pick_play_sequence(anims, frame_count, min_frames=4):
    """挑播一次序列 (fx PLAY): 帧引用全部界内 (无外部引用) 的 ≥min_frames 帧序列,
    取有效帧最多者。与 unit 的 MOVE 纯循环不同: 空白帧不否决 (特效显隐是演出语义)。"""
    best = None
    for a in anims:
        recs = a['records']
        if any(r['frame'] >= frame_count for r in recs):   # 外部引用 → 排除
            continue
        valid = [r for r in recs if r['frame'] >= 0]
        if len(valid) < min_frames:
            continue
        if best is None or len(valid) > sum(1 for r in best['records'] if r['frame'] >= 0):
            best = a
    return best


def flatten_composite(data, b1, eo, idx, block0_anims, block0_plus=5, sub_cap=8):
    """块1[idx] → [{frame,dur}] 展平序列

    记录语义 (0x409b70/0x4214f0 链 + 结构对比定案):
      (0x0801=2049 / 0x0601=1537 / 0x0501=1281, X, dx, dy, 0) = 引用块0动画 #(X+block0_plus), 带位移
      (0, -帧, -1, d, dur) = 直接帧;  (2,...) = 控制记录 (v1 跳过)
    引用内联取子动画前 sub_cap 帧; 位移(dx,dy) v1 不应用 (开口)。
    """
    s, e = b1 + eo[idx], b1 + eo[idx + 1]
    out = []
    for k in range((e - s) // 10):
        a, b, c, d_field, dur = struct.unpack_from('<5h', data, s + k * 10)
        if a in (2049, 1537, 1281):
            ref = b + block0_plus
            if 0 <= ref < len(block0_anims):
                for r in block0_anims[ref]['records'][:sub_cap]:
                    out.append((r['frame'], r['dur']))
        elif a == 0 and b <= -2:
            out.append((-b, dur))
    return [{'frame': f, 'dur': du} for f, du in out]


## ── 引擎动画表 (EXE .data 逆向定案 2026-09-19) ─────────────────────────────
## UnitAnim.cpp 0x465040 从动作 no=3 的表项取 (动画号, 镜像标志)，随后直接调用
## 0x409ff0(manager, block=0, animation, flags)。表项低两位是 x/y 镜像，绝不是块号。
## 角度表 0x618d80/0x618da4: 0°=d6(E), 45°=d3(SE), 90°=d2(S), 135°=d1(SW),
## 180°=d4(W), 225°=d7(NW), 270°=d8(N), 315°=d9(NE)；d5 是中心位。
ENGINE_DIR8 = {
    # 罗盘: (原版 dir, block0 动画号, 镜像标志)
    'W':  (4, 13, 0),
    'E':  (6, 13, 1),
    'NW': (7, 12, 0),
    'NE': (9, 12, 1),
    'S':  (2, 15, 0),
    'N':  (8, 11, 0),
    'SW': (1, 14, 0),
    'SE': (3, 14, 1),
}
ENGINE_MOVE_ACTION = 3

# 同一方向表中 action 5 的普通攻击映射。UnitCtrlAi.cpp 从技能明细表
# 0x611538 的 byte +1 取到动作号 5；UnitAnim.cpp 0x465040 再按方向查表。
ENGINE_ATTACK_DIR8 = {
    'W':  (4, 23, 0),
    'E':  (6, 23, 1),
    'NW': (7, 22, 0),
    'NE': (9, 22, 1),
    'S':  (2, 25, 0),
    'N':  (8, 21, 0),
    'SW': (1, 24, 0),
    'SE': (3, 24, 1),
}
ENGINE_ATTACK_ACTION = 5

ENGINE_ACTION_DIRECTIONS = {
    # direction: (engine direction number, animation offset, mirror flags)
    'W':  (4, 2, 0),
    'E':  (6, 2, 1),
    'NW': (7, 1, 0),
    'NE': (9, 1, 1),
    'S':  (2, 4, 0),
    'N':  (8, 0, 0),
    'SW': (1, 3, 0),
    'SE': (3, 3, 1),
}


def _engine_action_dir_map(anims, direction_table, action, *, omit_blank=False):
    mapped = {}
    for direction, (dir_no, animation, flags) in direction_table.items():
        if animation >= len(anims):
            continue
        entry = anims[animation]
        records = entry.get('records', entry.get('steps', []))
        if not records:
            continue
        if omit_blank and 'steps' in entry and not any(step.get('layers', []) for step in records):
            continue
        mapped[direction] = {
            'block': 0,
            'anim': animation,
            'flags': flags,
            'flip_x': bool(flags & 1),
            'flip_y': bool(flags & 2),
            'engine_dir': dir_no,
            'action': action,
        }
    return mapped


def engine_dir_map(anims, composites=None, frame_count=None):
    """生成经审计的八向 MOVE 映射。

    ``composites`` 参数仅为旧调用方兼容保留；方向标志不再选择块1。idle 在任务2接入正式
    动作表前沿用首个可用单帧动画，由导出 JSON 覆盖。
    """
    return _engine_action_dir_map(anims, ENGINE_DIR8, ENGINE_MOVE_ACTION), {}


def engine_attack_dir_map(anims, frame_count=None):
    """生成原版 action 5 的八方向普通攻击映射。"""
    return _engine_action_dir_map(anims, ENGINE_ATTACK_DIR8, ENGINE_ATTACK_ACTION)


def engine_action_dir_map(anims, action):
    """Map an original unit action to its eight directional block-0 programs.

    Actions 11 through 16 occupy consecutive five-program groups.  East-facing
    directions mirror their west-facing counterpart exactly as the executable's
    direction table specifies.  Archives may contain intentionally blank action
    slots; those directions are omitted so the runtime can fall back to idle.
    """
    if not 11 <= action <= 16:
        raise DxAnimError(f'unsupported skill action {action}; expected 11..16')
    base_animation = action * 5 - 4
    direction_table = {
        direction: (engine_direction, base_animation + offset, flags)
        for direction, (engine_direction, offset, flags) in ENGINE_ACTION_DIRECTIONS.items()
    }
    return _engine_action_dir_map(anims, direction_table, action, omit_blank=True)
