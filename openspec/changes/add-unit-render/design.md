## Context

数值层（BattleMath/SimEngage/派生）与地图层（SimMapData/渲染/回显）已全部就位并有 26 项测试；
main.gd 是单文件场景脚本。原作战斗是 60fps 实时 + 速度档；本次把循环跑起来但**刻意从简**
（普攻/最近目标/直线步进），复杂度留给后续 AI/技能/寻路 change。

## Goals / Non-Goals

**Goals:**
- 完整闭环：布阵→接敌→普攻→死/撤→胜负，全链走真数据真公式
- 逐事件日志 + 整场确定性（后续回放/对照实机的地基）
- 战斗节奏"看起来像实时"（单位连续移动/掉血）

**Non-Goals:**
- 不做寻路绕障（穿 object 障碍可接受；可行走语义未定案，留给 pathfinding change）
- 不做技能/AI 策略/前后摇动画（普攻最近目标，tick 数模拟节拍）
- 不做多人多方阵营（就红蓝两队）

## Decisions

1. **逻辑固定步长 + 渲染解耦**：Battle.tick() 以固定逻辑步长推进（默认 1/30s 逻辑帧），
   main.gd 在 _physics_process 累积 delta×time_scale 调用；速度档=time_scale（不改变逻辑
   结果只改频率）。确定性测试离屏直接循环 tick，不依赖帧。
2. **移动 = 每 move_interval 个逻辑帧走一格，直线步进**：按 dx/dy 符号交替优先轴逼近
   （曼哈顿路径）；不做碰撞。move_interval 进 battle_setup.json（可调节奏=魔改友好）。
3. **攻击节拍 = attack_interval 帧一次结算**：不分前后摇动画，但 interval 常量可调；
   前后摇的真实帧数（攻击表 +0x0A/+0x0E）在演出 change 接入。
4. **事件日志是权威输出**：Battle 维护 `events: Array[String]`（move/attack/hit/miss/dead/
   withdraw/finish 带帧号与数值），渲染只消费状态；确定性测试 = 比日志。比"逐帧状态快照"
   轻且足够判等。
5. **单位绘制走既有菱形几何**（cell_to_world + 派生色，dead 变暗/withdrawn 半透明），
   头顶双条 draw_rect（屏幕空间，不吃 view_scale 形变——用换算后坐标画，宽度随 scale）。
   不引 Node2D/场景实例化：6~10 个单位直接在 main._draw 画，零节点开销。
6. **BattleUnit 包装不继承 SimUnit**（组合优于继承）：持 SimUnit 引用 + 战斗字段；
   SimUnit 保持纯数据可复用。
7. **battle_setup.json 首发阵容**：红蓝各 4 单位，属性取整可读值（如全 20/职业重戰士0 与
   剑士系对照），坐标对称布阵在 MAP01 中部——数值无需还原原作关卡（布阵工具/关卡数据是
   后续 change）。

## Risks / Trade-offs

- [直线步进穿越障碍物视觉违和] → v1 接受并记录；寻路 change 修正后重验
- [普攻最近目标会出现"拉锯"或集体围殴] → 可接受（模拟器阶段看重的是循环正确性）；
  若画面难看可在 setup 调 move_interval
- [逻辑帧率与渲染帧率耦合出不确定性] → 决策 1 已隔离：逻辑只在固定步长点推进，
  累积误差不进逻辑

## Migration Plan

新增 3 文件 + main.gd 扩展。回滚 = 还原 main.gd、删 battle_unit/battle/battle_setup。
