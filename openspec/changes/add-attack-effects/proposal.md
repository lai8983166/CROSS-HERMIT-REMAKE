## Why

当前战斗攻击表现与原版不符：单位进入攻击状态时仍播放待机动作，同时所有普通攻击都被无条件叠加 `01E#21`。进一步逆向确认，样例职业的普通攻击使用单位档 action 5，挥砍残影已经包含在单位动作的复合图层中，而攻击 101/103 的外置特效字段均为 0。

## What Changes

- 从原版单位动作表导出 action 5 的八方向攻击映射，并在每次攻击时从首帧播放一次，结束后视觉回到待机。
- 攻击时让单位朝向目标，保证方向动画与实际攻击方向一致。
- 攻击事件增加攻击条目 ID 与原版命中特效 ID，保留命中、伤害和双方格坐标。
- 外置 `##E` 特效改为显式 ID/配置映射；特效 ID 为 0 或没有已验证映射时不播放，不再为所有攻击套默认 `01E#21`。
- 保留 `##E` 解码与播放管线，供后续已完成语义标注的技能/命中特效使用。

## Capabilities

### New Capabilities

- `assets/attack-effects`: 单位八方向攻击动作、攻击事件中的原版效果标识，以及按明确映射播放一次的外置攻击特效。

### Modified Capabilities

无。

## Impact

- `tools/unit_anim_export.py`、`tools/dxanim_lib.py`：增加 action 5 八方向映射。
- `prototype/data/unit_sprites.json`：增加 `attack_by_dir`。
- `prototype/sim/battle_unit.gd`、`prototype/sim/battle.gd`：记录攻击条目、效果 ID、攻击起始帧与目标朝向。
- `prototype/main.gd`、`prototype/data/attack_effects.json`：攻击动作单次播放，外置特效由非零 ID 或显式职业覆盖驱动。
- 自动化测试及用户目检需要重新验收攻击动作与外置效果。
