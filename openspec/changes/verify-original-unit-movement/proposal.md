# Proposal

## Why

已验寻路包尚未与原单位的下一格选择和定点坐标更新衔接。R4需要跨过这一行为连接，区分生成路径、实际移动、到位和阻挡。

## What Changes

- 在声明地图、单位及动画资源门输入下，执行路径消费/下一格、原移动速度与坐标更新、到位/阻挡检查的连贯路径段。
- 用独立规则核对定点坐标、分支、状态及完整内存/指令写入重放，记录实际支持与剩余AI边界。
- 保全上一单元及递归原始资料，更新总spec、完成有限change并本地提交归档。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

无需求变化；为既有reverse-engineering/completion的R4提供实现工具/研究证据，skip_specs=true。

## Impact

新增独立移动审计工具、测试和证据；复用已验寻路工具且保持冻结文件不变。无Godot、原存档或窗口输入改动。不是完整AI决策、战斗或原CRT/MAIN线程连接验收，2026-11-20目标保持。
