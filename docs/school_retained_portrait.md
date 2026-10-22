# 保留任务的肖像资源入口与全脚本清单

change `trace-retained-portrait-resources` 实施中，全程离线，不需要保持解锁。

清单解析安装包全部45份脚本：334个具有代码区的VM段、4210个仅含 `dmf\0` 的四字节标记段，22377条指令、57类原分派入口。这里的“全部”限定安装文件静态出现，不表示主线可达性、全部操作码语义或R6完成。

326条opcode30引用4种配置、21个角色姓名/肖像文件。320条有完整20字节四参数编码；另6条只有12字节两个参数。原4C61C0在+4/+8/+12/+16固定读取DWORD；清单保留这六条位置和20字节源读取窗口，缺失参数保持未决，不能把后继指令头当作声明的表情参数。这六条是否可达及实际运行语义待核验，原脚本不改写。

首轮清单预检曾误把四字节标记要求为零，实际来源是 `dmf\0`；第二轮严格四参数预检发现上述短编码。失败日志保留，第三版清单是正式候选。资源文件均与独立原私有副本逐字节一致，姓名保留原Big5字节和源指针。

当前执行目标是上轮六个已验完整任务分支，从4C61C0第一条指令连续到原IAT5920A0的CreateFontA入口。原配置8选择图层5/角色4“瑟希莉絲”，后继图像为sc004.bin。名字体请求高20、字重700；API首条指令不执行，新字体/姓名栅格/图像加载及完整外层世界另计。

复现使用新输出路径：

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_portrait_catalog --out analysis/fresh-portrait-catalog.json
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_portrait_verification analysis/fresh-portrait-catalog.json --catalog --out analysis/fresh-portrait-catalog-proof.json
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_portrait --out analysis/fresh-portrait.json.gz
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_portrait_verification analysis/fresh-portrait.json.gz --out analysis/fresh-portrait-proof.json
```
