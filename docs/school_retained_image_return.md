# 保留原IMAGE加载器自然返回

有限change为 `complete-retained-image-loader`，依据总规格R3实施。原IMAGE的前缀已在新CRT域内接通；本轮在同一个新堆/锁寿命内继续403BD0至4CC0D2，执行原像素复制和文件缓冲释放。全程无需交互桌面、解锁、新窗口或新输入，Godot未改。

## 接口记录和原函数边界

固定 `analysis/school-character-image-acceptance-20261013.json` 与其 `school-character-image-live-v3-20261013.json` 的SHA，独立重新验证原生COM回执、全纹理读回、资源大小和完整SC004像素。旧样本的分配、memcpy、free原语仅作为其历史边界保留，不用于声称本轮执行了原函数。

本轮重用已验cold.data及原57B9D0/576F60创建新堆和四锁，明确投影六区335字节CRT状态。保留其他全部内存和完整CPU，旧历史堆仍未恢复。原IMAGE从自然入口重新打开文件、分配、完整读取、关闭，再原向量/记录构造；没有接续已关闭的文件或已销毁的堆。

四个纹理调用仅回放历史成功响应：CreateTexture(256,512,1,0,25,1)、GetLevelDesc、LockRect、UnlockRect。新逻辑纹理域按对象、虚表、方法和像素指针翻译，所有旧原生指针仅作来源标识，不传Windows。**本轮没有新增原生GPU上传或显示输出。**

原403BD0/4046F0、512次原56D4D0和原428AD0逐条执行，不代用游戏或CRT函数结果，不改原代码/IAT，不新设前向游戏根。核对每行源/目标/长度，完整262144字节像素与原文件及历史上传一致；原free执行调试头/保护区检查、摘链及DD填充，真实助手释放文件缓冲。原IMAGE设置loaded标记1、恢复原SEH、ret8自然返回4CC0D2，PC仍252；资源分派、动画和完整任务尚未返回。

记录的两个未初始化填充字节保持CD。向量在IMAGE返回时仍是唯一新域存活分配，原调试链/统计和游戏记账独立核对。其他旧纹理没有新原生操作。

## 原容器清理

自然返回边界后，实验明确补充调用原41F4E0(slot32,this=renderer+844h)。原403730/403A00查询纹理大小并扣回字节计数，原COM Release清空纹理指针；原41F2A0/56DE40/41F890执行向量析构，原428AD0释放88字节向量，原登记表清空。查询描述重放同对象的已验描述响应，Release重放历史平台清理计数0；不声称这两个原清理调用点曾在旧原生样本中观测到。

最后原576FA0/57BA60销毁四锁与空堆，助手必须零文件、零块、零锁且无补充强制回收地正常退出。补充容器清理不是原handler进度；清理后的实验状态不得作为活资源检查点继续。

## 验证和复现

使用 `PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe`：

```
-m tools.school_retained_image_return --out analysis/<fresh>.json.gz --helper .venv-audit/<fresh>.exe
-m tools.school_retained_image_return_verification analysis/<fresh>.json.gz --out analysis/<fresh-proof>.json
-m unittest tools.tests.test_school_retained_image_return -v
-m tools.school_retained_image_return_preservation --out analysis/<fresh-preservation>.json
```

独立重放核对全部原指令/写入、每步完整CPU和全部映射、实际OS接口/所有权、历史响应来源/类型投影、512行及所有像素、原分配/释放/析构、原自然栈返回。输出路径必须是新的；失败记录和旧证据保持字节不变。

下一步是原资源handler及动画/就绪状态返回、外层世界同寿命连接。完整CRT历史、Big5 ANSI乱码、六条短编码、其他R3/R4/R5/R6工作仍未完成。2026-11-20目标不变。

六个分支均独立复核通过：每例在已验69440指令前缀后，追加163326条原IMAGE指令/136688次原写入；512次原memcpy逐行执行，原free自然释放文件缓冲并ret8返回。最终143个客体映射及完整CPU一致。补充原容器清理1434条指令、原初始化/堆锁销毁561条；每例44次真实OS叶调用及6次明确历史COM响应回放，正常助手退出。新增38项来源/像素/所有权/自然返回破坏测试通过。正式证据 `analysis/school-retained-image-return-v1-20261022.json.gz`，独立证明 `analysis/school-retained-image-return-proof-v1-20261022.json`。
