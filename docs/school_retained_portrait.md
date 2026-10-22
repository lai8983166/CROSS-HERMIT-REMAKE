# 保留任务的肖像资源入口与全脚本清单

change `trace-retained-portrait-resources` 已完成2/3任务，集成验收进行中，全程离线，不需要保持解锁。

清单解析安装包全部45份脚本：334个具有代码区的VM段、4210个仅含 `dmf\0` 的四字节标记段，22377条指令、57类原分派入口。这里的“全部”限定安装文件静态出现，不表示主线可达性、全部操作码语义或R6完成。

326条opcode30引用4种配置、21个角色姓名/肖像文件。320条有完整20字节四参数编码；另6条只有12字节两个参数。原4C61C0在+4/+8/+12/+16固定读取DWORD；清单保留这六条位置和20字节源读取窗口，缺失参数保持未决，不能把后继指令头当作声明的表情参数。这六条是否可达及实际运行语义待核验，原脚本不改写。

首轮清单预检曾误把四字节标记要求为零，实际来源是 `dmf\0`；第二轮严格四参数预检发现上述短编码。失败日志保留，第三版清单是正式候选。资源文件均与独立原私有副本逐字节一致，姓名保留原Big5字节和源指针。

实际已在上轮六个已验完整任务分支，从4C61C0第一条指令连续到原IAT5920A0的CreateFontA入口。原配置8选择图层5/角色4“瑟希莉絲”，后继图像为sc004.bin。名字体请求高20、字重700；API首条指令不执行，新字体/姓名栅格/图像加载及完整外层世界另计。

复现使用新输出路径：

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_portrait_catalog --out analysis/fresh-portrait-catalog.json
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_portrait_verification analysis/fresh-portrait-catalog.json --catalog --out analysis/fresh-portrait-catalog-proof.json
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_portrait --out analysis/fresh-portrait.json.gz
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_portrait_verification analysis/fresh-portrait.json.gz --out analysis/fresh-portrait-proof.json
```


## 配置来源

| 配置索引 | 原图层 | 框位置 | 主体位置 |
| --- | --- | --- | --- |
| 7 | 4 | 42/190 | 38/36 |
| 8 | 5 | 254/368 | 736/214 |
| 9 | 6 | 42/546 | 38/392 |
| 10 | 4 | 142/310 | 138/156 |

清单与独立证明：`analysis/school-retained-portrait-catalog-v3-20261022.json`、`analysis/school-retained-portrait-catalog-proof-v1-20261022.json`。六条短编码位于T0080的段10以及T0090的段2/3，各在一对肖像命令上缺少两个声明参数；清单未用跨边界字节补造参数。角色30的依赖仍按已经存在的前两个literal记录，并与短编码风险关联。

来源与清单任务已完成，13项定向测试通过，已本地提交cea7b3f。实际六个分支均无新增原VM/handler根、无新增平台返回，进入相同名字体入口；独立机器码复核已通过，24项本单元正例/边界/篡改测试均已通过（见定向完成快照），相邻回归仍在进行。


完整文件SHA覆盖全部字节；清单的结构/语义统计对象是VM代码区与肖像依赖。字符串/其他数据区的完整语义、脚本可达性和其他57类操作码的完整规则不因本次静态清单而自动验收。


## 连续任务前缀的独立复核

六分支各执行1070条新原指令、608次原写入，无新根或平台响应，完整八区域符合独立源模型，所有118个最终映射和完整CPU独立一致。自然栈依次为name→layer→handler→VM→task，原返回地址分别为4CC1DE、4C62D4、4CEDA7、454D90和声明任务根返回；原API返回位置4CA7CB及14参数均核对。最终独立证明为 `analysis/school-retained-portrait-proof-v1-20261022.json`。

这是从已验证架构状态恢复后的连续原调用栈，不是已结束原生助手中的句柄复用或同一原生寿命重启。完整字体/姓名像素/肖像加载与原外层/世界仍为后续工作。
