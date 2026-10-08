# Design

## Context

见 proposal.md。已有第四周会话不可变的结果是迁移存档的重放基础；第五周出口保存在单独 continuation 字段。旧职务室和学校前缀审计有可复用的 API 边界，但其上游日期与成员不同。

## Goals / Non-Goals

Goals: 扩展实际 4/5 同一 CPU 的 state8→CH002→state9→学校数据前缀；保留旧会话作为成长回顾，创建独立第五周规划会话，复用已经验证的调动、解锁与查看操作；核对原版4A7D30就绪与4A6A10参战准备，提供当前队伍的出发准备页。

Non-Goals: 不模拟原版完整任务调度器、音视频或所有职务室菜单；不执行第二次成长、冒险战斗或第五周后续剧情。准备画面与已实际执行的战斗分开，必修gate保持有效。

## Decisions

- 将现有三个边界 hook 的阶段处理提取为无继承副作用的 helper，沿现有第五周 CPU 调用；不多重继承两个不同上游初始化器。
- 先记录 native before/after 与有限写范围，再用 source rules 对当前成员计算学校数据。fixture 仅用于测试，不作为运行时目标快照。保留动态成长、关系、班级；原版前缀是否重置字段由实际证据决定。
- 第四周 session 保持不变，增加 fifth_session 与 workroom/school continuation；界面选择 active planning session。旧成长回顾继续从第四周 session 读取。
- 新存档版本增加规则指纹。迁移逐版本验证原有 state hash；v3 迁移使用捕获于模型修改前的两个真实 fixture（剧情中、出口）。保留精确 CRLF/LF alias。
- 职务室使用独立 source background/catalog；不生成仿制游戏美术。返回、保存、战斗预览沿用当前事务机制。

- 出发准备由当前第五周school snapshot纯计算生成，读取独立来源规则并验证；不把native fixture复制到运行时，不改角色/日历/gate，不发奖励。准备页为当前班级的可重复查看投影，不新增持久命令或改变version4存档指纹；修改班级后重算。
- 原版同一CPU前缀继续执行4A7D30与4A6A10，保留就绪条件和defined rating/round字段，覆盖原班、换班、成员待命与教师孤班。战斗状态10、准备场景/事件执行留待后续链路接入。

## Risks / Trade-offs

- 原版学校前缀处理多个共享缓冲区 → 在独立 CPU 中限定写范围，比较所有当前角色与学校字段，拒绝意外 growth/date/MVP 写入。
- 旧存档 hash 随新增 state 字段改变 → 保存原有 v3 state 构建路径，只给 v4 添加字段。
- 新一周课程可能更多 → 必修冒险完成前只查看实际当前教师可用课程；素材名称缺失时采用描述性名称，声明命名来源。
- 原版菜单正文未完整执行 → 将学校数据准备与原版菜单可操作性分开标记，图形规划由重制项目提供。

## Migration Plan

捕获 v3 fixture；验证并提交 source audit；实现原子续接和 v4 重放；接图形职务室与第五周规划；完成兼容、窗口与视觉验收。新功能仅在用户主动进入职务室/学校时执行。可回退本轮 commits，既有 v1/v2/v3 fixture 与源规则均保留。
