# -*- coding: utf-8 -*-
"""表导出器: 从脱壳镜像按已知 VA 导出重制数据表 → prototype/data/*.json

用法:
    python tools/table_export.py level|attack|job|all

地址/字段依据:
    docs/REMAKE_BLUEPRINT.md §7 (总索引)
    docs/battle_mechanics.md   §1.1 (攻击表字段图)
    docs/character_growth.md   §3.2 (等级表) / §4 (职业表)

镜像节表 raw==VA → 文件偏移 = VA − 0x400000。
输出: prototype/data/<name>_table.json = {"_meta": {...}, "rows": [...]}
"""
import hashlib
import json
import os
import struct
import sys

EXE = 'analysis/hermit_game.exe'
OUTDIR = 'prototype/data'
TOOL_VER = '1.0'
BASE = 0x400000

# ── 攻击/技能表 0x6C2DC8 × 0x48 (字段图: battle_mechanics.md §1.1) ──────────
ATTACK_FIELDS = [
    ('id', 0x00, 'H'),            # 攻击/技能 ID
    ('category', 0x02, 'H'),      # 系别/类别 (5=回复辅助系)
    ('equip_series', 0x04, 'B'),  # 属性系别 1..12 (装备亲和/武器类别)
    ('attack_class', 0x05, 'B'),  # 1/4=物理 2=魔法 3=特殊
    ('use_condition', 0x06, 'B'), # 使用条件 (2=需特定系武器)
    ('job_threshold', 0x07, 'B'), # 职业可用阈值
    ('mp_cost', 0x08, 'H'),       # 消耗 MP
    ('cast_frames', 0x0A, 'H'),   # 前摇/蓄力帧
    ('u16_0x0c', 0x0C, 'H'),
    ('recovery_frames', 0x0E, 'H'),  # 后摇/硬直帧
    ('u8_0x10', 0x10, 'B'),       # →伤害记录+0x36 (候选: 异常持续)
    ('accuracy_base', 0x12, 'B'),    # 命中精度基础 (cap 0x20)
    ('accuracy_addend', 0x14, 'B'),  # 参与基数 (命中/威力两链)
    ('accuracy_scale', 0x15, 'B'),   # 命中属性成长系数
    ('aoe_radius', 0x16, 'B'),       # AoE 半径基础 (cap 32)
    ('aoe_scale', 0x17, 'B'),        # 半径属性成长系数
    ('targeting', 0x18, 'B'),        # 瞄准模式 0..6
    ('target_filter', 0x19, 'B'),    # 敌我筛选 1..5
    ('hit_effect', 0x1A, 'B'),       # 命中时演出 ID
    ('power_base', 0x1C, 'h'),       # 主威力基数
    ('power_scale', 0x1E, 'h'),      # 主威力属性成长系数
    ('power_a_base', 0x20, 'h'),     # 威力A 基数
    ('power_a_scale', 0x22, 'h'),    # 威力A 倍率%
    ('power_b_base', 0x24, 'h'),     # 威力B 基数
    ('power_b_scale', 0x26, 'h'),    # 威力B 倍率%
    ('power2_base', 0x28, 'h'),      # 威力2/等级成长基值
    ('growth2_scale', 0x2A, 'h'),    # 通用成长系数 (+0x20/+0x28 共用)
    ('growth_tri0_base', 0x2C, 'h'),
    ('growth_tri0_scale', 0x2E, 'h'),
    ('growth_tri1_base', 0x30, 'h'),
    ('growth_tri1_scale', 0x32, 'h'),
    ('u16_0x34', 0x34, 'H'),      # +0x34~0x3F 全库未观察到读取
    ('u16_0x36', 0x36, 'H'),
    ('u16_0x38', 0x38, 'H'),
    ('u16_0x3a', 0x3A, 'H'),
    ('u16_0x3c', 0x3C, 'H'),
    ('u16_0x3e', 0x3E, 'H'),
    ('level_points', 0x40, 'i'),  # 等级点贡献
]

# ── 职业表 0x6B2D88 × 0x40 × 30 (character_growth.md §4 / battle_mechanics §1) ──
JOB_FIELDS = [
    ('base_attack', 0x00, 'H'),
    ('group', 0x02, 'B'),           # 类别字节 0..6 (4a8bf0 排序用)
    ('series_b', 0x03, 'B'),        # 第二类别字节
    ('attr_a', 0x04, 'B'),          # 转职演出写 unit+0x582
    ('attr_b', 0x05, 'B'),          # 转职演出写 unit+0x570
    ('hp_coef', 0x06, 'H'),         # HP 系数 (×/100)
    ('mp_coef', 0x08, 'H'),
    ('spirit_coef', 0x0A, 'H'),
    ('coef_0x0c', 0x0C, 'H'),
    ('coef_0x0e', 0x0E, 'H'),
    ('u16_0x10', 0x10, 'H'),
    ('ai_move_type', 0x12, 'B'),
    ('ai_0x13', 0x13, 'B'),
    ('ai_post_move_a', 0x14, 'B'),
    ('ai_post_move_b', 0x15, 'B'),
    ('ai_mem_pos', 0x16, 'B'),      # 记忆坐标标志
    ('u8_0x17', 0x17, 'B'),
    ('default_attack', 0x18, 'H'),  # 4b93c0 默认攻击 id
    ('u16_0x1a', 0x1A, 'H'),
    ('ai_chase', 0x1B, 'B'),        # 追击标志
    ('ai_stay_attack', 0x1C, 'B'),  # 原地攻击标志
    ('ai_post_action', 0x1D, 'B'),  # 攻击后行动
    ('u16_0x1e', 0x1E, 'H'),
    ('u16_0x20', 0x20, 'H'),
    ('u16_0x22', 0x22, 'H'),
    ('u16_0x24', 0x24, 'H'),
    ('u16_0x26', 0x26, 'H'),
    ('u16_0x28', 0x28, 'H'),
    ('u16_0x2a', 0x2A, 'H'),
    ('u16_0x2c', 0x2C, 'H'),
    ('u16_0x2e', 0x2E, 'H'),
    ('u16_0x30', 0x30, 'H'),
    ('u16_0x32', 0x32, 'H'),
    ('u16_0x34', 0x34, 'H'),
    ('u16_0x36', 0x36, 'H'),
    ('u16_0x38', 0x38, 'H'),
    ('u16_0x3a', 0x3A, 'H'),
    ('u16_0x3c', 0x3C, 'H'),
    ('u16_0x3e', 0x3E, 'H'),
]

ATTACK_VA = 0x6C2DC8
ATTACK_STRIDE = 0x48
ATTACK_UPPER = (0x6D4E58 - ATTACK_VA) // ATTACK_STRIDE  # 下一已知表为上界
JOB_VA = 0x6B2D88
JOB_STRIDE = 0x40
JOB_COUNT = 30
LEVEL_VA = 0x625300
LEVEL_COUNT = 50
ENGAGE_VA = 0x6E4528
ENGAGE_COUNT = 51
SKILL_ATTR_VA = 0x6D4E58
SKILL_ATTR_STRIDE = 7
SKILL_ATTR_COUNT = 101
SKILL_ATTR_FALLBACK_VA = 0x738AF0


def decode_engage(data, sha):
    """ENGAGE 时长表 (i32[51], 单位=分钟; battle_mechanics.md §8):
    lv0=0, lv1~6=5940 (99h 封顶), 每 3min/级降至 lv20, 再 2min/级至 lv50=540"""
    vals = list(struct.unpack_from(f'<{ENGAGE_COUNT}i', data, ENGAGE_VA - BASE))
    if vals[0] != 0 or vals[1] != 5940 or vals[50] != 540:
        sys.stderr.write(f'错误: ENGAGE 表 magic 校验失败 ({vals[0]},{vals[1]},{vals[50]}), '
                         '镜像可能已更换, 核对 0x6E4528\n')
        sys.exit(1)
    rows = [{'level': i, 'minutes': v} for i, v in enumerate(vals)]
    return {
        '_meta': {
            'table': 'engage', 'source_va': ENGAGE_VA, 'stride': 4, 'count': len(rows),
            'naming_ref': 'docs/battle_mechanics.md#8 (engage = mod_h*3600 + tbl[lv]*60 + mod_s, clamp 1..356400)',
            'image_sha1_8': sha, 'tool': f'table_export v{TOOL_VER}',
        },
        'rows': rows,
    }


def load_image():
    if not os.path.exists(EXE):
        sys.stderr.write(f'错误: 找不到镜像 {EXE} (先跑 tools/unpack_all.py)\n')
        sys.exit(1)
    data = open(EXE, 'rb').read()
    if len(data) < 0x5B4000:
        sys.stderr.write(f'错误: 镜像尺寸异常 {len(data):#x}\n')
        sys.exit(1)
    return data, hashlib.sha1(data).hexdigest()[:8]


def decode_rows(data, va, stride, fields):
    row = {}
    for key, off, fmt in fields:
        row[key], = struct.unpack_from('<' + fmt, data, va + off - BASE)
    return row


def decode_level(data, sha):
    vals = list(struct.unpack_from(f'<{LEVEL_COUNT}i', data, LEVEL_VA - BASE))
    if vals[0] != 149999 or vals[-1] != 8500000:
        sys.stderr.write(f'错误: 等级表 magic 校验失败 (首={vals[0]}, 末={vals[-1]}), '
                         '镜像可能已更换, 核对 0x625300\n')
        sys.exit(1)
    rows = [{'level': i + 2, 'points_required': v} for i, v in enumerate(vals)]
    return {
        '_meta': {
            'table': 'level', 'source_va': LEVEL_VA, 'stride': 4, 'count': len(rows),
            'naming_ref': 'docs/character_growth.md#3.2 (表 0x6252FC: 级1=0 起, 此处为后续 50 项, level=索引+2)',
            'image_sha1_8': sha, 'tool': f'table_export v{TOOL_VER}',
        },
        'rows': rows,
    }


def decode_attack(data, sha):
    rows = []
    for i in range(ATTACK_UPPER):
        va = ATTACK_VA + i * ATTACK_STRIDE
        r = decode_rows(data, va, ATTACK_STRIDE, ATTACK_FIELDS)
        rows.append(r)
    # 尾部全零截断
    while rows and all(v == 0 for k, v in rows[-1].items()):
        rows.pop()
    if not 10 <= len(rows) <= 4096:
        sys.stderr.write(f'错误: 攻击表条数异常 ({len(rows)}), 上界推定失效\n')
        sys.exit(1)
    anchors = [rows[0]['level_points'], rows[1]['level_points'], rows[2]['level_points']]
    if anchors != [40, 16000, 36000]:
        sys.stderr.write(f'错误: 攻击表锚点不符 (entry0/1/2 level_points={anchors}, 应为 40/16000/36000)\n')
        sys.exit(1)
    return {
        '_meta': {
            'table': 'attack', 'source_va': ATTACK_VA, 'stride': ATTACK_STRIDE, 'count': len(rows),
            'naming_ref': 'docs/battle_mechanics.md#1.1 (字段图); u*_0xNN = 未定名字段原样保留',
            'upper_bound': ATTACK_UPPER, 'image_sha1_8': sha, 'tool': f'table_export v{TOOL_VER}',
        },
        'rows': rows,
    }


def decode_job(data, sha):
    rows = [decode_rows(data, JOB_VA + i * JOB_STRIDE, JOB_STRIDE, JOB_FIELDS)
            for i in range(JOB_COUNT)]
    bad = [r['group'] for r in rows if not 0 <= r['group'] <= 11]
    if bad:
        sys.stderr.write(f'错误: 职业 group 值越界 {bad}, 职业表地址需核对\n')
        sys.exit(1)
    return {
        '_meta': {
            'table': 'job', 'source_va': JOB_VA, 'stride': JOB_STRIDE, 'count': len(rows),
            'naming_ref': 'docs/character_growth.md#4 + battle_mechanics.md#1 (职业表行)',
            'image_sha1_8': sha, 'tool': f'table_export v{TOOL_VER}',
        },
        'rows': rows,
    }


def decode_skill_attributes(data, sha):
    """Skill calculation bytes selected by 4DE8F0 (ids 0..100; otherwise fallback row)."""
    rows = []
    for i in range(SKILL_ATTR_COUNT):
        raw = data[SKILL_ATTR_VA + i * SKILL_ATTR_STRIDE - BASE:
                   SKILL_ATTR_VA + (i + 1) * SKILL_ATTR_STRIDE - BASE]
        if len(raw) != SKILL_ATTR_STRIDE:
            sys.stderr.write(f'error: skill-attribute row {i} is truncated\n')
            sys.exit(1)
        rows.append({'id': i, 'bytes': list(raw)})
    fallback = data[SKILL_ATTR_FALLBACK_VA - BASE:
                    SKILL_ATTR_FALLBACK_VA - BASE + SKILL_ATTR_STRIDE]
    if len(fallback) != SKILL_ATTR_STRIDE:
        sys.stderr.write('error: skill-attribute fallback row is truncated\n')
        sys.exit(1)
    return {
        '_meta': {
            'table': 'skill_attributes', 'source_va': SKILL_ATTR_VA,
            'stride': SKILL_ATTR_STRIDE, 'count': len(rows),
            'fallback_va': SKILL_ATTR_FALLBACK_VA,
            'selector_ref': '0x4DE8F0 (id < 101 uses indexed row; id >= 101 uses fallback)',
            'naming_ref': 'docs/battle_mechanics.md#1 (raw bytes; per-field names remain conservative)',
            'image_sha1_8': sha, 'tool': f'table_export v{TOOL_VER}',
        },
        'rows': rows,
        'fallback': {'bytes': list(fallback)},
    }


TABLES = {
    'level': decode_level,
    'attack': decode_attack,
    'job': decode_job,
    'engage': decode_engage,
    'skill_attributes': decode_skill_attributes,
}


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in (*TABLES, 'all'):
        sys.stderr.write('用法: python tools/table_export.py level|attack|job|all\n'
                         f'已注册表: {", ".join(TABLES)}\n')
        sys.exit(2)
    data, sha = load_image()
    os.makedirs(OUTDIR, exist_ok=True)
    names = list(TABLES) if sys.argv[1] == 'all' else [sys.argv[1]]
    for name in names:
        out = TABLES[name](data, sha)
        path = os.path.join(OUTDIR, f'{name}_table.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
        print(f'{name}: {out["_meta"]["count"]} 条 -> {path}')


if __name__ == '__main__':
    main()
