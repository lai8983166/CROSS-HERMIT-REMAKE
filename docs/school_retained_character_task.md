# 保留角色动画与完整原任务

有限change为 `connect-retained-character-task`，依据总规格R3实施。从原IMAGE返回4CC0D2继续原资源handler、层、VM与454CF0任务，然后由原请求消化、队列复位及完整任务推进动画就绪和第三句入口。无需解锁、交互桌面、新窗口或新OS输入；Godot未改。

## 原任务和动画

在同一新堆/锁寿命内复现已验原IMAGE读取、构造、复制和自然返回；沿原五层/完整任务栈继续，第一段不设新根。之后每次明确调用425DE0、40DB90、40DC80和454CF0原入口，绝不单独设置4CE8F0根。原PC、wait、动画计数和就绪结果均由原指令产生。

每例79次完整任务自然返回，另一次完整任务在第三句CreateFontA首指令前暂停。78步动画由原代码执行延迟30、渐变45、背景60的严格边界；PC252进入PC272等待，waiting_count达到77时原就绪判定解除等待，随后第三句激活并到PC280字体入口。四层原font/text/VM/task栈、14个API参数和原返回地址4CAD09核对。

旧 `school_character_animation_catalog.py` 的来源模型只比较八个逻辑区域及动画状态，原展示/入队、文字更新和任务尾声实际执行。每例新增2962747条原指令、1706706次原写入和2945次原展示调用；没有游戏、展示或CRT函数返回代用。

## 队列和平台边界

每个区间保存完整96字节manager、4096组head/tail和当前arena全部有效记录；整个1MB arena及所有映射由每步完整状态摘要和最终全量重读覆盖。原展示调用仅入队，尚未执行本帧D3D绘制/Present，部分静态图像仍待恢复；不能由入队成功声称画面已显示。

79次原请求消化和79次空串查询仅在原null/empty上下文下回放已验ImmGetOpenStatus/lstrlenA输出。肖像四个纹理接口和补充清理两个接口也仅回放已验历史契约，未把旧原生句柄传Windows。文件、CRT分配/保护区/释放及堆锁寿命仍由无窗口x86助手实际执行。

第三句Font尚未创建。验收边界后明确补充原41F4E0容器析构、原free、原576FA0/57BA60销毁锁堆，助手零文件/块/锁、无强制回收地正常退出。旧历史堆仍未恢复，原外层线程/世界同寿命连接和R3/R6整体未完成。

## 校验开销与完整性

原型v1每个区间重读全部约126MB内存；其完整记录保留为独立参考。正式工具按原写入范围使整个映射的摘要失效，独立验证器用不同的脏页集合算法重算；每条原指令仍实际执行并进入指令/写入摘要。原text完整核对后缓存只读指令字节，任何原代码写入被拒绝，平台只允许声明的输出；没有跳过游戏指令。

首次来源核对和最终全量重读覆盖所有映射，确认增量摘要与完整字节一致；独立验证器也重放v1全量参考和v2含原队列记录的试跑。首版验证器误要求“已经执行到IMAGE中途的任务尾段”再次访问前段425F34，原记录证明请求设置早已执行；修正该阶段范围检查，失败日志和当时验证器保留。

## 复现

使用 `PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe`：

```
-m tools.school_retained_character_task --out analysis/<fresh>.json.gz --helper .venv-audit/<fresh>.exe
-m tools.school_retained_character_task_verification analysis/<fresh>.json.gz --out analysis/<fresh-proof>.json
-m unittest tools.tests.test_school_retained_character_task -v
-m tools.school_retained_character_task_preservation --out analysis/<fresh-preservation>.json
```

所有输出使用新路径；既有存档、资源、私有检查点和已验工具/证据不改。下一步为第三句字体/栅格与实际显示，以及完整外层世界连接。Big5 ANSI乱码、六条短编码、其余R3/R4/R5/R6工作和2026-11-20目标保持。

六分支正式记录 `analysis/school-retained-character-task-v3-20261022.json.gz` 经最新验证器全部独立重放，证明为 `analysis/school-retained-character-task-proof-v4-20261022.json`。每例79次完整任务及1次第三句前缀，共2962747条新原指令、1706706次原写入，2945次原展示调用；317个原区间的完整CPU、143个映射及原队列记录一致，末端全字节重读通过。37项针对性测试通过。早期长驻验证模块尚未加载最后三项字体ABI拒绝检查，首次测试34过/3失败；保留原日志及运行时字节码，重载后重新验证全部六分支并通过全部37项，不修改来源报告。
