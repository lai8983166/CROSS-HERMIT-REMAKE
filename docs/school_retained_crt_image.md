# 保留任务的原CRT域与肖像构造

本单元为 `connect-retained-crt-image`，依据逆向总规格R3实施。目标是六个已验保留分支从自然IMAGE入口4CDE10连续完成SC004文件读取/关闭、原分配和容器/向量构造，停在首个肖像纹理构造403BD0之前。无需交互桌面、解锁、窗口或新GPU。Godot未改。

## 来源和重建边界

- 固定原代码 `analysis/hermit_game.exe`；实测post-unpack冷.data和独立复核沿用 `analysis/school-crt-init-probe-v2-20261022.json.gz` 及对应proof，既有验收保持字节不变。
- 用原57B9D0及576F60创建新堆及四静态锁，平台助手初始没有预创建的堆/锁。仅投影六区335字节CRT控制/锁表/调试列表/统计/锁本体/堆模式；每区保存原值与实际原初始化来源值。
- 保留其他全部内存及完整CPU、原帧，79FC74游戏记账不清零。历史首尾节点仍未恢复；所有旧对象仍属于旧资源域，任何将旧对象交给新堆free的尝试必须被所有权检查拒绝。
- 这是有来源的新CRT资源域重建，不能写成“旧检查点原样恢复”“旧堆历史恢复”或“原生同一寿命”。全CRT/C++初始化尚未逐指令重放。

## 连续原执行和真实OS边界

三个保留分支initial/student9_waiting/fifth_class分别接入76/77采集来源。私有验证器副本只观察旧验收中的第一步IMAGE入口，不修改历史验证器，也不接续其已关闭的文件句柄。原代码在本轮平台助手内重新执行GetCurrentDirectoryA、只读CreateFileA、GetFileSize、262168字节分配、完整ReadFile和CloseHandle。

原416790/41F0E0继续分配88字节，原56DDA0和41F830/403620/41F930构造一个84字节记录。原调试头、链表、FD前后保护区、CD初始化及DD释放都保留。记录偏移46h的两个字节未被构造函数写入，保持分配器CD填充值；不能套用旧简化工具的全零填充模型。

平台只处理真实Win32叶调用，按所有权翻译新堆/锁地址，完整原生缓冲在消费前同步、边界后读回。游戏/CRT函数无返回代用，原代码和IAT不改，无新游戏根；原调用栈继续到4050AF→403BD0。

## 明确的实验清理

403BD0第一条指令尚未执行，VM保持PC252、IMAGE loaded标记尚为0。边界后明确用两个补充428AD0根释放本轮文件缓冲和向量，再原576FA0及57BA60销毁四锁和新堆。它们是补充实验清理，不是原IMAGE/handler自然返回；保留的临时renderer指针只用于已结束实验，不能作为后继活检查点。助手必须在零文件/零块/零锁/堆已销毁时正常退出，强制清理或失败尝试不算验收。

## 复核命令

使用 `PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe` 运行：

```
-m tools.school_retained_crt_image --out analysis/<fresh>.json.gz --helper .venv-audit/<fresh>.exe
-m tools.school_retained_crt_image_verification analysis/<fresh>.json.gz --out analysis/<fresh-proof>.json
-m unittest tools.tests.test_school_retained_crt_image -v
-m tools.school_retained_crt_image_preservation --out analysis/<fresh-preservation>.json
```

每次输出必须使用新路径。独立重放核对每条原指令和完整写入摘要、每个原IAT调用/ABI/所有权、每步完整CPU/全部映射、全文件与记录内容。历史存档、资源和私有检查点通过累计保全链保护。

## 尚未完成

肖像GPU创建/上传、原IMAGE/handler动画返回、原外层线程/世界与保留状态同一有效寿命连接、Big5 ANSI乱码、六条短编码及R3/R4/R5/R6剩余工作继续保留。目标日期2026-11-20不变。

六个分支均独立复核通过：每例连续69440条原指令/66886次原写入，另初始化与补充清理67546条原指令，共44次真实OS叶调用；最终136个客体映射和完整CPU一致。335字节限域投影之外的保留内存、原CPU和游戏记账保持。新增34项完整来源/投影/内容/所有权破坏测试通过。正式来源 `analysis/school-retained-crt-image-v3-20261022.json.gz`，独立证明 `analysis/school-retained-crt-image-proof-v1-20261022.json`。
