# Proposal

## Why

R3保留任务已完成原IMAGE自然返回，但原资源handler、动画就绪和完整任务尚未接通。旧78步动画模型有来源，但展示函数代用和独立VM根不能代替连续原任务证据。

## What Changes

- 在有效新CRT域内复现原IMAGE返回，沿原资源/handler/VM/454CF0栈完成第一帧，再由原请求消化、队列复位及完整任务推进动画。
- 接通这段路径所需的原展示/队列代码和资源契约，验证延迟、渐变、背景及原就绪判定，推进至第三句的自然CreateFontA入口之前。
- 六分支逐原指令/接口/完整状态独立复核，明确历史平台响应与真实CRT资源寿命，原资源清理、保全及归档。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

无。执行既有reverse-engineering/completion要求，新增逆向工具和证据，skip_specs不改变要求。

## Impact

新增有限审计工具、测试、说明及不可变证据。禁止游戏函数代用或独立4CE8F0根；不改旧检查点、源代码/IAT或Godot。优先离线/无窗口接口，不需要新OS输入或交互桌面，R3/R6整体仍另计。
