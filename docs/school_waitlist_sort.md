# 学校待命学生排序

原版命令证据及边界见 `battle_return_audit.md` §70，报告为 `analysis/school-waitlist-v1-20261005.json`。证据生成命令拒绝已有目标文件：

```bash
python -m tools.school_waitlist_emulation --out analysis/<新的报告名>.json --godot-out prototype/data/<新的证据名>.json
python -m unittest tools.tests.test_school_waitlist_emulation -v
```

`school_waitlist_sort.gd` 的 `order(profiles, waiting_ids, mode, rules)` 是独立纯计算器。模式0为等级降序、1为原版职业类别0–5、2为七属性合计降序；数值采用原版嵌套交换，类别内保持输入顺序。空和单人列表也有独立源案例；当前目录模型支持角色ID1–12、职业1–30，拒绝重复/缺失待命成员、非整数或越界属性、无效模式及类别。职业类别表来自原映像，不使用职业ID代替类别。

`CampaignResultState.sort_school_waitlist(return_instance_id, mode)` 从自己持有的当前目录计算并发布，要求该返回已完成学校数据投影、目录版本仍归属此返回，且无其他准备/战果/返回待处理。当前仅支持教师人数为0、五班均空、所有学生均待命的已核对布局。调用方不能提交排序后的目录。

发布只改变 `school.school_control.idle_student_ids` 及可选 `idle_sort_mode`，添加一次 `school_waitlist_sort` 日志和一个版本。旧冻结学校初始化目录不添加模式字段；第一次显式排序记录模式，此后相同模式和相同顺序不发布。无效操作不改变目录、日志或版本；状态读取返回深拷贝，重复完成学校返回不覆盖已排序目录。

`CampaignReturnDemo.start` 新增可选第四来源路径参数，三份源文件均核对归档SHA。会话只保留新来源的规则，剔除其病例及期望输出。`sort_waitlist(mode)` 仅在school阶段转交目录操作，拒绝操作不会破坏原会话。重开舍弃排序和旧日志。原版实机、存档写入、完整学校就绪标记保持false。

目录验证：新增8项Godot测试覆盖所有源排序序列、交换并列、不同键、拒绝输入、提前操作、两路线全字段边界、重复/旧返回送达、待处理/过期目录、视图隔离和重开。完整40套件292项通过，无SCRIPT ERROR。旧冻结报告没有被改写。

窗口现已接入三种选项和共享待命顺序，保留学生选择、切页顺序和目录状态；操作见 `campaign_return_ui.md`。最新完整Godot40套件293项通过，两路线离屏79项/渲染86项检查通过；七张最终截图见 `analysis/school-waitlist-ui-final-20261005/`。
