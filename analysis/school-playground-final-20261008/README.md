# 学校养成试玩最终验收

2026-10-08，Godot4.7.2，1024×768，Windows/OpenGL/NVIDIA RTX3060Ti。

| 项目 | 输入检查 | 窗口渲染检查 | 最终截图 |
|---|---:|---:|---:|
| 编班与课程 | 80 | 83 | 3 |
| 成长/MVP/保存恢复 | 73 | 81 | 8 |
| 学校↔战斗往返 | 26 | 28 | 2 |

全量56套件371项零失败；旧学校导航22项、旧MVP窗口73项输入及73项实际渲染检查通过。所有日志无脚本错误，最终13张截图逐一检查。OpenSpec严格27项全部通过，6个展示文件逐字节再生成一致，课程显示重点与源成长表匹配。

- [学校编班](planning/initial_class.png)
- [课程安排](planning/course_selected.png)
- [本次MVP](results/mvp.png)
- [不同安排的MVP](results/alternate_mvp.png)
- [战斗预览](navigation/battle_preview.png)
- [返回学校并完成另一课程](navigation/returned_school.png)

默认启动为school_playground.tscn。试玩日期4月第4周，教师101/学生3、4、9；没有前四周真实经历、章节正文播放或下一周推进。战斗预览保留旧场景，与本段学校没有共享出战/奖励。保存为重制自有格式，原版SAV与原始证据保持原字节。详见[操作说明](../../docs/school_playground.md)。
