# 首战结算后的入队、换周与返校数据

2026-11-15。school_postbattle_return.gd 使用本次学校会话的教师101、学生3/4/9、实际参战成长和确认记录，承接 Chapter020 入队、Chapter021 结束后的 state7 换周、Chapter022/208 职务室以及 CH002 后的5月第1周学校准备。它是重制的纯数据投影；不代表原生场景、原脚本等待、资源或完整学校验收。STOPPED_SCOPE_GUARD 与正式2/8保持不变。

调用接口依次为 join(bundle)、next_week(joined.after)、school_return(week.after)。bundle 携带 school（确认后学校）、完整三人的 growth（当前记录仅按参与者覆盖）、records、counts、participants（当前学校入口的装备/技能/职业解锁字段）、flags 和 item_flags。每步返回独立的 after，拒绝错序；上层负责真实剧情边界和命令去重。输出阶段为 chapter020_joined、week_advanced、school_returned。教师、已有三人历史、成长和人际不来自旧期望世界；周结算使用既有 WeekSettlementReplay.project 的学生字段视图，教师101保留在学校视图中。

入队依据原 Chapter020.ybc:0x14 的 opcode144 和 0x4D3E90。新规则只保存从认证原镜像提取的法娜模板、初始化职业进度及8条与当前成员的原人际。镜像 SHA-256 为588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005；角色5模板位于0x6F5088 + 5*0x4A0，模板 SHA-256 为44fd41834cc7329a5c1dbd6ebc75eb693cd409294e7d562a711fd7f302f750bf。初始职业进度按49E930从0x751242+5*0x42读取32个word、限制到0..100并写入progress[1..32]；历史的177字节在新局状态清零中归零，未复制历史fixture。

法娜原属性为17/69/11/33/12/33/34、职业4、装备技能11、无装备物品。4D3E90对难度0和1保留技能并将状态置6；只有其它难度清空装备技能。新实现按当前学校难度执行该分支，重新算级别和解锁。旧RosterJoinReplay仍保留其0/2、无教师的严格旧入口；旧SchoolReturnContinuation、SchoolBootReplay同样未修改。

字段可直接从同一原镜像重提：模板内job是+6的有符号word，attributes为+0xC+8k字节，growth_pools为+0x10+8k的little-endian uint32，level为+0x50字节，8个装备技能/物品word分别始于+0x52/+0x62，84项技能状态为+0xB8+12k字节。关系取0x74E4B0+row*68+1+column字节，教师101映射46；只补双方至少一人为5的8项。job_sums按既有school_course_settlement_emulation.runtime_rules的每类六项职业进度求和。JSON内candidate、history、relationships是这些独立源字段，不含旧case的before/expected_after世界。

现有已认证的new_game_school_rules负责5月第1周教师101课程开放：新增1..5，保留10/11/12，累计8项。Groups、Student、Teacher、Sort纯内核负责实际教师与班级保留、待机列表和排序，四人排名按严格大于计算。教师所在班级原有学生保持；未指定班级入队的法娜在待机列表。move_member(bundle,{kind,member_id,target_group,target_slot})仅封装已实现的学生/教师移动及清理，不增加课程结算或出击。

冒险列表仅提供newly_dated_adventures=[8]，并明确adventure_catalog_complete=false。旧当前学校模型未携带80条冒险工作记录及4月4日已开放、无限期的17号记录，不能据旧teacherless boot的新鲜空表声称完整菜单只有8号。5号是4月5日、duration1的必修冒险；原4A1920在使用/过期时移除，4A5CE0在返校时清除失效的原冒险选择。完整冒险存量、8号出击、新课程授课/结算、原菜单和资源等待仍未开放。interactive_school_ready和native_equivalence_verified均为false。

Chapter020的opcode153（0xBA8，三个立即数1/6/0）经42F460读取通用全局槽、经4C1F40尝试写目的引用；目的类型2的case直接返回0，不写学校字段。Chapter208的9/1音乐字段与CH002的11/0保持阶段区分；本模块最终学校阶段设置CH002后的11/0，不伪造音频播放完成。

本轮已接入school_postbattle_flow和纯文字剧情界面：Chapter020为281页、Chapter021为43页、Chapter022为79页、Chapter208为8页，共411页。流程为post_story→new_week_story→post_workroom→returned_school；阅读到边界或明确跳过时才推进阶段，上一页不重新应用入队或周结算。Chapter208结束保留音乐9/1及背景8，职务室继续后应用CH002返校字段。这里是原文的文字呈现，不声称原镜头、图片、电影、音频和等待时序等价。

v5试玩存档保存合法战斗命令、逻辑tick、后续操作及状态摘要，通过school_battle_record从出发学校状态重新计算战斗、奖励与后继，再核对摘要后整体替换。它不信任保存的奖励快照，不写原版存档；v1–v4保留原恢复分支。成功回放缓存仅减少同一记录的重复计算：每次命中前仍执行Combat.open源准入，缓存键还含确认阶段另读两份规则文件的当前摘要。同格移动直接记录一次stop，避免同一输入在重放时额外生成记录。

本轮自动合法命令记录实际在9227 tick到达squad_defeated，再从出发状态独立重放并接通战后剧情、5月第1周及返校；这是重制模型的失败结局通路，不是自动胜利证明，更不是原程序实测。入队/换周/返校的3项针对测试已通过headless验证。完整自动胜利、真正原生场景连续执行及完整冒险目录仍不能由这些结果推出；正式原生验收仍为2/8，STOPPED_SCOPE_GUARD保持。

来源认证沿用原镜像、既有反编译4D3E90、49E930、4D3510、4A5CE0、4A5F40、4A1920、4A2BA0、4C1F40及原规则文件摘要。运行时只消费其规则，不选择历史测试案例。法娜源字段JSON约5KB；没有新增原生采集、截图或大型转储。针对测试覆盖实际首战结算合并、待机学生不获战斗奖励、难度1入队技能、历史保留、换周、课程、四人编班/教师移动以及错序/坏输入拒绝；整体UI、v5兼容及本轮新增文件体积以主Agent最终验收记录为准。
