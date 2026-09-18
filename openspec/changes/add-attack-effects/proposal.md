## Why

单位层（精灵+配色）落地后，战斗表现力的最大缺口是**攻击特效**：攻击命中只有日志和血条
变化，画面上无事发生。而素材侧零成本——侦察定案：
- `##E.BIN`（01E 实测）与单位档**同容器 9 块格式**：块0 #1..#121 全是 9 记录播放序列
  （首帧 dur=20 + 后续 dur=6 的降序帧串，播一次的斩击演出），块5=帧数×8、块6=98 帧
  BMP、块7=6 张换色板——`unit_anim_export` 的解码逻辑直接复用
- `battle.gd _attack()` 是现成事件源（挂 typed 事件即可）

攻击时在目标格播原版斩击特效，是当前 ROI 最高的一步。

## What Changes

- **解码复用重构**：抽 `tools/dxanim_lib.py`（容器/BMP/序列解析），`unit_anim_export.py`
  改为调用它；新 `tools/fx_export.py` 导出 `##E` 档 → `assets/fx/<档>/frame_*.png` +
  `data/attack_effects.json`（同帧表 schema，anim_map 为 PLAY 播一次序列）。
- **战斗事件**：`battle.gd` 增 typed `fx_events: Array[Dictionary]`（attack 事件：
  帧/攻方格/守方格/命中/伤害），`_attack()` 挂点写入；纯数据不动逻辑。
- **视图播放**：main.gd 特效实例表（sim 时间驱动，播一次即移除），锚点=画布底中对
  目标格心，按攻→守方向水平翻转；帧纹理走既有 `_frame_tex`（特效表并入同一注册表，
  换色/缓存路径复用）。
- **配置**：`data/attack_effects.json` {effects: {名字: {file, anim}}, default} +
  `battle_setup.json` 可选 `attack_effects: {"<job_id>": 名字}` 职业覆盖；资产/表缺失
  → 无特效不报错。

## Capabilities

### New Capabilities
- `assets/attack-effects` — ##E 特效档导出、特效事件流与播放配置（数据驱动）

（battle.gd 的 typed 特效事件与视图播放都归入本 capability，不动既有 battle-sim 规约）

## Impact

- 新增 `tools/dxanim_lib.py`、`tools/fx_export.py`、`prototype/assets/fx/`、
  `prototype/data/attack_effects.json`
- `prototype/sim/battle.gd`（事件数组 + 挂点）、`prototype/main.gd`（特效实例绘制）、
  `prototype/data/battle_setup.json`（可选职业映射）
- 测试：特效表加载/播一次选序列/事件→实例生成/回退；全量 runner 绿
- 风险：##E 动画语义（哪档哪条是何种斩击）未标注 → 默认映射可配置，语义标注记开口
