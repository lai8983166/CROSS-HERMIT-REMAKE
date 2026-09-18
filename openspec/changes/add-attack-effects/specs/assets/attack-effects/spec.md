## Purpose

把 DATA/DXANIM/##E.BIN 特效档（与单位档同容器格式）变成重制可用的攻击特效：
导出帧资产 + 播放配置，战斗攻击事件驱动视图播一次原版斩击演出。

## ADDED Requirements

### Requirement: 特效档导出
`tools/fx_export.py` 经共享解码库 `tools/dxanim_lib.py`（容器/BMP/序列解析，与
unit_anim_export 同源）导出 `##E` 档：`assets/fx/<档>/frame_*.png` +
`data/attack_effects.json`（帧表 schema 同 unit_sprites：frames/anims/锚点；
anim_map.PLAY = 播一次序列，挑全界内帧引用的 ≥4 帧序列，空白帧不否决——特效
的显隐是其演出语义）。

#### Scenario: 导出与复用
- **WHEN** 运行 fx_export
- **THEN** 01E 全帧导出无错、PLAY 序列引用界内；unit_anim_export 改用 dxanim_lib
  后产出与重构前逐字节一致（管线不回退）

#### Scenario: 配置驱动
- **WHEN** 手改 attack_effects.json 的 default/anim 或 battle_setup 的职业映射
- **THEN** 重载后攻击播放按新配置（无代码常量）

### Requirement: 特效事件流
`battle.gd` 维护 typed `fx_events: Array[Dictionary]`：`_attack()` 挂点写入
{type:"attack", frame, from_cell, to_cell, hit, damage}。事件只追加不改判——
战斗逻辑、确定性与既有测试不受影响。

#### Scenario: 攻击产事件
- **WHEN** 一次攻击结算（命中或 MISS）
- **THEN** fx_events 追加一条含双方格坐标的 attack 事件，字段可驱动特效播放

### Requirement: 视图播一次
视图消费 fx_events 生成特效实例：按 attack_effects 配置选序列，sim 时间推进，
播完即移除；锚点=画布底中对目标格心，攻→守方向 x 分量决定水平翻转。
表缺失/配置无效/资产缺失 → 不播不报错，战斗功能不损。

#### Scenario: 命中演出
- **WHEN** 攻击命中
- **THEN** 目标格播对应特效序列一次，时长=记录 dur 之和（dur_unit_seconds 计）

#### Scenario: 回退
- **WHEN** attack_effects.json 或 assets/fx/ 缺失
- **THEN** 无特效播放，无报错，战斗照常进行
