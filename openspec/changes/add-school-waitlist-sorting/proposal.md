# Proposal

## Why

学校返回页已有来源明确的学生目录，但只能浏览。原版待命名单排序无需教师，可作为当前无教师样例的第一个学校操作；编班仍需补教师前置条件。

## What Changes

- 执行原版 4A3CA0 的 0B/0C/0D 命令及 4A8BF0，冻结待命学生排序证据。
- 共享目录按等级、职业类别或七属性合计排序，保留原版交换排序的并列处理。
- 学校页显示待命顺序，支持排序并保留选中学生。
- 核对重复操作、无效输入、返回浏览和重开；每个验证阶段立即提交。

## Capabilities

### New Capabilities

- `game-flow/school-student-list`: 学校待命学生名单的来源约束、排序及目录发布。

### Modified Capabilities

无。

## Impact

新增独立 x86 审计工具和证据、纯排序计算器；扩展 CampaignResultState、返回演示适配器及学校页。使用现有 Unicorn/Godot 依赖，无原版进程或存档写入，不声明编班、排课或完整学校操作已完成。
