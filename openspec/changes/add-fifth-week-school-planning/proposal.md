# Proposal

## Why

第五周剧情已可阅读并保存，但结束后只能停在职务室入口。需要延续同一批成员与成长，进入职务室，再开放第五周学校编班与选课。

## What Changes

- 沿当前 4/4 授课到 4/5 Chapter018 的同一原版 CPU，验证实际 state8、CH002、state9 与学校初始化前缀。
- 保存职务室停留和进入学校的独立命令，保留已完成成长、关系、MVP与剧情；迁移原有 v1/v2/v3 试玩存档。
- 增加使用原版背景的职务室画面，提供进入学校、回顾、存档和战斗预览。
- 开放第五周五班成员调动与当前教师可用课程选择；本轮终点为第五周规划，不执行第二轮授课成长或后续剧情。

## Capabilities

### New Capabilities

- `school-fifth-week-planning`: 第五周职务室到学校的可保存续接，以及保留成长的班级与课程规划。

### Modified Capabilities

无。学校前置能力目前保存在已完成未归档的 change specs 中，主 specs 尚无学校能力。

## Impact

原版审计工具、SchoolPlayground 与学校会话、职务室资源导出和 Godot 图形界面、存档兼容测试与验收文档。仅本地 Git 提交，不改写原版存档，不 push。
