# 保留任务姓名纹理与肖像文件交接

有限 change `connect-retained-portrait-file-handoff` 接续上轮已验姓名位图，目标是原姓名纹理转换/清理、资源路径和原图像文件分配入口；本单元不创建窗口、发送输入或新建 GPU 设备，无需解锁。

## 来源与验收边界

- 最新姓名栅格验收固定为 `3d71a54fb3798de59f16f8464c36a580bbfcd3eca3503ff92d7c15c2c675bc88`。
- 历史真实姓名纹理报告 `school-character-name-texture-v3-20261013.json` 固定为 `de5d82eda44a0d3e773140c400bdacefd2fb4c06459fbc778b7de7ccf305ec56`；其原位图与上轮逐字节一致。仅以其成功的原生 D3D/GDI 回执作显式离线重放，不复用失效原生资源，不算新的实际 GPU 创建/上传。
- 不改原代码、IAT、现有纹理或外层调用栈，不新增游戏调用根，不代用原格式化/拼接函数。新增纹理对象和方法边界只来自实际记录的接口身份及明确的类型地址投影。
- 原图像加载器以实际只读文件打开/查询大小继续，在第一次 428A40 原分配请求首指令之前停止。未代用分配器返回，未执行原 ReadFile/CloseHandle；停点未关闭的文件由实验明确补充关闭和失效查询，不冒充原加载完成。

## 全肖像容器

清单覆盖此前静态脚本引用的全部21个角色文件及隔离副本，均为262168字节的一项容器、DX mode2、256×512、A1R5G5B5，共2752512个像素/10752行。独立读字节器复核每行哈希、全部像素数、透明/不透明计数、黑色不透明值、取值种类及可见边界。它是资源文件覆盖，不是动态场景可达性验收，也未覆盖所有游戏图像格式。

新证据路径使用 `analysis/school-retained-portrait-file-*`；禁止覆盖。原存档、旧检查点、旧工具与旧实验保持原字节。

## 连续执行结果

六分支的正式来源报告为 `analysis/school-retained-portrait-file-v2-20261022.json.gz`。每例第一段60670条原指令/9450次原写入，完成原创建/锁定/像素转换/解锁路径、原GDI清理、原CRT拼接和自然4CDE10入口；第二段2054条原指令/537次原写入，实际查询当前目录、只读打开源文件并查询262168字节长度，停于428A40首指令之前。合计62724条新原指令/9987次原写入，未声明新游戏根。

完整转换纹理8192字节，SHA256为 `03cb70a4b4bb98e0d07a7e8aee13a97e0ad51fa2703dc52d249c455a14f13a25`，与历史实际上传相同；原资源记账增加8192。最终126个映射、完整CPU及八层原调用栈纳入独立复核。一个尚未由原加载器关闭的真实文件由实验关闭，随后GetHandleInformation返回0/ERROR_INVALID_HANDLE(6)。这不表示原ReadFile/CloseHandle执行或图像加载完成。

初次v1在资源帧预期地址写成4CC273（原call的实际返回为4CC26D）时被校验拒绝；文件包装调用的返回地址也依据原call复核为42AE47。失败日志 `school-retained-portrait-file-run-v1-20261022.log` 原字节保留；该Python进程已载入旧模块，回溯输出时磁盘源文件已经修正，因此回显行含修正后的字面地址，不把它当作正式执行报告。v2才是正式来源报告。

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_portrait_file --out analysis/school-retained-portrait-file-v2-20261022.json.gz
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_portrait_file_verification analysis/school-retained-portrait-file-v2-20261022.json.gz --out analysis/school-retained-portrait-file-proof-v1-20261022.json
```

这些路径已留作证据；重跑必须换成全新输出路径。新独立验证器从未修改的上一验证器读出完整状态，另外推导接口身份、参数、像素/记账、自然栈、全映射与CPU。文件部分重放记录的真实接口输出，验证阶段不把已关闭的真实句柄传给Windows。

下一边界是原428A40/CRT堆分配的有效对象与锁状态；本单元没有返回代用内存，也未代用构造器。原ReadFile、图像容器构造/上传、完整肖像handler/动画、同一有效寿命的原外层世界连接、ANSI乱码和六条短编码仍属后续工作，R3/R6继续进行中，目标日期保持2026-11-20。

六分支的完整独立证明为 `analysis/school-retained-portrait-file-proof-v1-20261022.json`；新增39项检查和相邻34项姓名检查已通过。阶段转录快照为 `analysis/school-retained-portrait-file-targeted-proof-v1-20261022.json`，其中明确记录当时完整回归尚未结束；最终以整份原始日志和验收清单为准。
