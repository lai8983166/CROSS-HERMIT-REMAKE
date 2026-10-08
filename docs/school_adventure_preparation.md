# 第五周必修冒险：出发准备

用户2026-10-08继续指令承接按原版顺序推进的建议。第五周直接选课目标已修正为查看课程并保留必修gate；在既有职务室/编班变更内继续准备下一段冒险。上轮验收文件保留当时的“范围待确认”状态，不改写历史证据。

## 原版执行与当前边界

`tools/school_adventure_preparation_emulation.py`继承实际4/4授课、成长/MVP、Chapter016/017、周推进、4/5 Chapter018、职务室/CH002/Chapter205和学校初始化的同一CPU。继续执行原版4A7D30出发就绪和4A6A10参战准备。成员调动实际执行4A4680、4A5F40及4A95F0，鼠标命中/松开仍是显式API边界；没有用另一条返回路线的快照。

在必修gate=1时，4A7D30要求每个班评级为0（无教师）或2（有效冒险班），并至少有一个2。教师孤班评级1会阻断；全部教师待命也不可出发。任务5来源记录0x73BED0+5×256中round_count=1、scene_id=5、selection_word=1，因此4A6A10按班号/槽位顺序收集所有有效冒险班的教师与学生，记录各学生的原班号。这里的场景5来自配置，不把已有独立战斗预览认作本周冒险。

来源学校缓冲区0x7A5294记录任务ID，0x7A5296场次游标，0x7A5298场次数；0x7A529A起每场112字节，+0x0E学生班号、+0x36学生ID、+0x5E学生数、+0x60教师ID、+0x6A教师数、+0x6E场景ID。前14字节也保存五班评级的已定义字段；未初始化的栈字和缓冲区尾部不作为输出契约。

五种顺序案例都核对：初始班学生[3,4,9]；9待命后[3,4]；教师和3/4移到第五班后学生班号[4,4]；教师孤班不就绪；教师待命不就绪。准备前后完整角色、学校、日期、MVP和计数快照一致。有限写保护拒绝日期、角色包/MVP、角色记录及未知内存，只允许学校状态和评级临时输出。Python5项验证来源、逐字节再生成、名单、拒绝和写范围。

正式报告：`analysis/school-adventure-preparation-v1-20261008.json`，SHA256 `9149611a96178d9412acdb4c4a36c20bca899eb367ad5705f188a7882ec8ddff`。运行规则由原版表字节单独导出到school_adventure_preparation_rules.json；fixture仅供测试，不供运行时计算。首次诊断调用曾由授课结果祖先的按钮边界误接管成员调动，现明确在movement阶段使用旧验证过的移动hook；最终五种native案例与Python测试通过，首份失败日志保留。

尚未执行完整菜单时间线、学校提交4A1920、后继状态10、场景事件、实际战斗、完成奖励或授课解锁。live_witness与原版持久写入授权仍false。

## 重制接口

`SchoolAdventurePreparation.project(school, rules)`是当前第五周学校的纯投影；验证任务5、日期/gate/工作字段与来源记录，复用已验证评级，再生成ready、class_ratings和prepared.rounds。无有效班级时仍返回supported=true、ready=false与原因。非法来源或学校输入返回unsupported；输入不变。

`SchoolPlayground.adventure_preparation()`只在fifth_planning可调用，读取独立来源规则。它不加入保存重放指纹，不新增命令、不递增revision；version4和原有十项指纹保持原字节。准备页是当前班级的重复查看，编辑后重新生成。该输出尚未由战斗任务消费，不能清除gate或发奖励。
