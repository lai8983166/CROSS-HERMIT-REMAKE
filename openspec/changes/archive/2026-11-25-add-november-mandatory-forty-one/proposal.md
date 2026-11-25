# Proposal

## Why

学年主线 `add-school-year-loop` 到达十一月第 3 周时，学校锁定必修冒险 41。玩家需要以实际编班进入该关、取得战果，才能依原版走完归队剧情并返回第 4 周的学校。

## What Changes

- 接通冒险 41 的出击、MAP41 战场、T0041 登场与增援、任务目标、结局和操作重放。
- 以该场实际回执结算奖励、成长、履历与 MVP。按原章节处理学生 2 归队、换周及返校。
- 验证已有十一月第 3 周存档可接续，完成后的存档能够独立重放。

## Capabilities

### New Capabilities

- `game-flow/november-mandatory-forty-one`：十一月第 3 周必修冒险从学校出发至战后返校的可玩流程。

### Modified Capabilities

无。

## Impact

复用现有 Godot 战斗、脚本导出、战果回放和学校存档。关卡增量引用原始地图和脚本哈希，正式存档留在本地。第四周返校后由学年 change 接续。
