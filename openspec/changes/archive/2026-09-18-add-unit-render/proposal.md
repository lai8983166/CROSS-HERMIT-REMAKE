# Proposal: add-unit-render

## Why

战斗模拟器成型里程碑：数值层（add-battle-math）与地图层（add-map-data）已就绪，现在让**单位上地图
实时互殴**——把已有公式/数据串成完整战斗循环。完成后窗口里第一次出现"两队按原作规则打的实时战斗"，
sim 从静态视图升级为可运行模拟器。

## What Changes

- `prototype/sim/battle_unit.gd`（BattleUnit：格坐标/阵营/HP·MP 现值/ENGAGE 剩余秒/
  状态机 idle→move→attack→dead|withdrawn；包装 SimUnit 数据 + 派生上限 + 默认攻击）
- `prototype/sim/battle.gd`（Battle 控制器：布阵两队、逐帧 tick——选最近敌→直线步进→
  射程 1 内 BattleMath.physical 结算→HP≤0 阵亡；ENGAGE 归零撤退；一方全灭结算胜负；
  种子 RNG 注入，输出事件日志）
- `main.gd` 接入：单位按阵营菱形着色绘制 + 头顶 HP/ENGAGE 双条；点击单位显示属性面板；
  战斗结束 HUD 显示胜负与耗时；`R` 重开（新种子）
- 布阵与参战单位参数进 `prototype/data/battle_setup.json`（魔改友好：改阵容/属性=改 JSON）
- 不含：寻路绕障（直线步进）、技能/AI 策略（普攻最近目标）、原版贴图、攻击前后摇演出

## Capabilities

### New Capabilities
- `battle-sim/battle-loop`: 实时战斗循环——单位状态机、移动接敌、普攻结算、ENGAGE 计时撤退、胜负判定，整体确定性可测

### Modified Capabilities
- `battle-sim/map-render`: 主场景从静态数据视图升级为战斗场景承载（渲染单位与状态条、单位点选）

## Impact

- 新文件：`sim/battle_unit.gd`、`sim/battle.gd`、`data/battle_setup.json`
- 修改：`main.gd`（接入 Battle tick 与单位绘制，保留地图三层渲染与既有交互）
- 依赖：既有 SimMapData / SimTables / SimUnit / SimDerive / BattleMath / SimEngage 全链
- 风险：直线步进可能穿过 object 障碍（可行走语义未定案）——v1 接受穿墙，寻路 change 修正
