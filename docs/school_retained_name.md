# 保留任务姓名栅格连接

本单元 `connect-retained-name-raster` 接续已验肖像前缀：从原 CreateFontA 请求继续至原 403BD0 纹理创建入口之前。全程仅用内存 DC 和 DIB，不创建窗口、不操作前台、不发送输入、不开 GPU，计划不依赖解锁。

## 资源与来源

- 上一单元验收 SHA256：`8322ecbd5a3d56b26e5e7426212f2aa9152d7c15ee6552c85853697d0f25fb29`。六分支均先通过未修改的旧验证器，才读出完整内存和 CPU。
- 不声明新游戏调用根，不改代码/IAT/原调用栈。原字体调用、姓名格式化 CRT 56D810/575940、414440 取测量 DC、405160 栅格函数均执行原机器码；不代用游戏函数返回。
- 历史 owner 中的测量 DC 已失效。原 414440 仍返回其逻辑 token，仅在 GDI 接口处显式映射到新建 CreateCompatibleDC(NULL)。历史 token 从未传给 Windows。这是资源重建，不是原生同一寿命延续；历史 GPU 指针只是逻辑参数，停止于创建函数首指令前，不传给原生 GPU。
- 每个分支新建一个字体、两个内存 DC、一个 DIB；清理前恢复选入对象，全部资源释放。原接口参数、DC 翻译、真实接口结果及内存输出逐项保留。

## 记录与复核

`tools/school_retained_name_raster.py` 生成六个连续来源分支。`school_retained_name_corpus.py` 对清单中全部 21 个原始 Big5 姓名及原字体参数另做真实离屏实验，记录清底、阴影、前景三阶段像素。这 21 项不是动态场景可达性的证明。

`school_retained_name_verification.py` 的独立重放器检查原接口/调用者/全部参数、完整写入、全部内存映射及完整 CPU；原分支的位图必须与独立姓名实验三阶段完全一致。姓名实验另由验证器自己的实现重新创建资源绘制，不使用旧句柄或生产器的 raster 方法。

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_name_raster --out analysis/school-retained-name-raster-v2-20261022.json.gz
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_name_corpus --out analysis/school-retained-name-corpus-v2-20261022.json.gz
```

输出路径不可覆盖；重跑必须选择全新路径。v1 初次实验保留，与补齐防护/三阶段记录后的 v2 正式报告分开。

## 编码与剩余工作

本机 ACP936，实际选中字形为“宋体”。保留 Big5 原字节经过 ANSI API 的行为，未转换为 Unicode，未修复乱码。本单元完成也不表示字体纹理已上传、肖像 sc004.bin 已载入，或外层线程/世界更新接入同一有效原生寿命。六条肖像短编码和 R3/R6 总体仍未完成，Godot 未改。
