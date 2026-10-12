# REA / Cross Hermit 小规模试接入（2026-10-12）

结论：REA 6.4.0 在本机 Windows 上能够通过真实 MCP 会话调用 Ghidra，分析这个项目的 32 位 PE。适合作为函数与调用链的辅助查询入口，但必须补充已知函数入口；当前输出不能代替已有类型标注和原版运行验证。

## 范围与环境

- 目标：`analysis/hermit_game.exe`，5,980,160 字节，已整理的脱壳镜像。
- SHA-256：`588b4288e4c737dc489d2b9bc0652cca85e3d668b1784942ef4b4bda916f1005`。
- REA：npm `rea-agents@6.4.0`，临时安装到 `C:/Users/lai/AppData/Local/Temp/chaomofa-rea-pilot-20261012`。包完整性与 Windows 原生插件摘要见 `prerequisites.json`。
- Node.js 24.14.1、Ghidra 12.1.3、Temurin 64 位完整 JDK 21.0.12.1。
- REA 的 Ghidra 专项 doctor 检查全部通过。没有要求安装 Hopper、IDA 或其他分析引擎。
- 独立 Python MCP 客户端通过 stdio 启动 REA，执行 initialize、tools/list 和真实 tools/call；没有永久注册到 Codex 配置，也没有安装 REA 的个人 skill。
- 只分析三个已经研究过的函数：文字栅格化 `0x405160`、文字更新 `0x4CB220`、剧情 VM `0x4CE8F0`。没有运行游戏可执行文件。

## 两组真实查询

| 项目 | 带入口与标签 | 不带入口与标签（对照） |
| --- | --- | --- |
| 首次 overview，包括导入和自动分析 | 183.047 秒 | 168.625 秒 |
| 调用次数，包括打开、状态、关闭 | 26 | 26 |
| 查询错误 | 0 | 13，均为找不到指定函数 |
| 成功的后续查询中位耗时 | 0.0155 秒 | 0.015 秒，主要为名称与字节查询 |
| 成功的后续查询最大耗时 | 1.578 秒 | 0.594 秒 |
| 三个函数的伪代码、汇编、调用关系 | 都可读 | 都不可读 |
| 三个地址的原始字节 | 与 PE 完全一致 | 与 PE 完全一致 |
| 结束后的资源关闭 | 成功，服务器退出码 0 | 成功，服务器退出码 0 |

这是两个本地会话的观测，不是普遍性能基准。耗时很短的查询还受到本机计时精度和输出取整影响。

对照组确认：成功导入、完成自动分析和能读取地址字节，并不意味着 Ghidra 已创建那个地址的函数。因此 `unseeded/run.json` 保留 `completed: false` 和 13 次错误，不能把它写成 26 次成功查询。

`seeded/seeds.tsv` 引入三个函数入口，以及 `analysis/hermit_real_iat.json` 当前实际包含的 **214** 个标签。REA 返回的结果确认：创建 3 个函数、应用 214 个标签，失败和未映射数量均为 0。旧分析脚本的说明写着 249 槽，此次以当前 JSON 的实际记录数为准。

种子名称属于已有分析结论，不是 REA 独立发现。`run.json` 的 `seed_sha256` 是种子文件原始字节摘要；REA 的分析 profile 使用其规范化种子内容摘要，两者分别保留，不混为同一个摘要。

## 与已有结果的核对

| 函数 | 汇编指令数 | 最后一条指令 | 直接被调用函数数 |
| --- | --- | --- | --- |
| `0x405160` | 670 | `0x4059d1: RET 0x10` | 9 |
| `0x4CB220` | 241 | `0x4cb5d7: RET 0x8` | 2 |
| `0x4CE8F0` | 2087 | `0x4d03b6: RET` | 186 |

- 两组会话都正确识别 native x86 PE，并记录相同目标摘要。
- 三个入口各读取 32 字节，与按 PE 节表定位得到的文件字节逐字节一致。
- 带种子组的三个函数都包含末尾返回指令；已有反编译文本中具名的直接调用地址均能在 REA 的 callees 中找到。
- `0x4CB220` 函数体经过明确的名称、签名和空白归一化后，与已有导出一致。归一化规则见 `review.json`，这不等于对其他函数作语义等价证明。
- 三份原有反编译导出及目标 EXE 的摘要均保持不变。
- 关闭后未残留 `rea-ghidra-*` 临时工程目录或对应的 Java / cmd 进程。
- 离线复核共 79 项检查通过，其中包含对照组预期错误的检查。**这不是 79 项游戏功能测试。**

## 实际限制

1. **不能直接复用已有工程。** REA 启动临时 Ghidra 工程，此次种子只带入入口和名称，没有导入我们已有的函数签名、IAT 指针数据类型、注释或其他数据属性。
2. **标签存在，API 伪代码仍退化。** `address_name(0x5920bc)` 正确返回 `API_GDI32_DLL_GetTextExtentPoint32A`，但 `0x405160` 的伪代码里没有保留已有的 15 个 API 名称，而出现 `(*(code *)0x76bd5230)(...)` 等快照地址调用。名称种子不足以恢复指针类型和调用签名。
3. **调用约定恢复不足。** 原有 `0x4CB220` 导出带 `__thiscall` 对象参数，`0x4CE8F0` 带 `__fastcall` 参数；此次 REA 输出将它们保留为 `in_ECX`，不能照着新签名实现调用。
4. **VM 中有一处实质性的表达式差异。** 原有输出读取 `DAT_007a49fc + 0x196c` / `+ 0x1970`，此次输出变成 `CONCAT22(0x4d7,_DAT_04d719d4)` / `_DAT_04d719d8`。这体现了新工程对快照指针的常量折叠，不能当作已经验证的运行时地址。
5. **调用图有覆盖边界。** 此次 VM 的 callers 是空数组；这不能证明 VM 没有调用者，函数表、间接调用和未识别入口仍需现有方法追踪。文字栅格函数还报告了终止调用的分析假设，必须结合汇编和原版执行核对。
6. **每个新会话都会重新导入。** 批量查询应共享一个会话；关闭后不能假设仍保留本次分析。Windows 的只读接口目前也无法在查询过程中补齐上述类型和签名。

建议保留此次脚本作为辅助入口：研究陌生函数时先补充已知入口，再批量读取汇编、直接调用和交叉引用。文字淡入、就绪状态及下一条脚本是否自然执行，继续由已有 Unicorn / 原生平台桥接和内存、像素核对验证。完整日常 MCP 注册暂不属于此次隔离试验。

## 重现

从仓库根目录在 Git Bash 执行。安装在独立目录，避免向本仓库添加 `node_modules`。

```bash
npm install --prefix C:/Users/lai/AppData/Local/Temp/chaomofa-rea-pilot-20261012 --ignore-scripts --no-audit --no-fund rea-agents@6.4.0

python tools/rea_native_pilot.py \
  --rea-root C:/Users/lai/AppData/Local/Temp/chaomofa-rea-pilot-20261012/node_modules/rea-agents \
  --output analysis/rea-pilot-rerun/seeded --seed

# 此对照预期退出码为 1：保留缺少函数入口的查询错误。
python tools/rea_native_pilot.py \
  --rea-root C:/Users/lai/AppData/Local/Temp/chaomofa-rea-pilot-20261012/node_modules/rea-agents \
  --output analysis/rea-pilot-rerun/unseeded

# 已保存的本次证据可独立复核，不需要再启动 Ghidra。
python tools/rea_native_pilot_review.py --results analysis/rea-pilot-20261012
```

查询脚本拒绝覆盖已有结果目录。重新采集时使用新目录；离线复核脚本会重写其结果目录内的 `review.json` 和 `artifact-manifest.json`。

文件：`seeded/` 和 `unseeded/` 保留实际 MCP 返回值、输入 schema、耗时、通知及关闭结果；`baselines.json` 记录试验前入口字节及已有导出摘要；`review.json` 是复核结果；`artifact-manifest.json` 是本目录证据文件摘要表。

上游说明：[安装与 Ghidra 种子](https://github.com/morluto/rea/blob/main/docs/installation.md)、[Windows Ghidra 边界](https://github.com/morluto/rea/blob/main/docs/windows-ghidra-p0.md)、[MCP 会话与首次查询](https://github.com/morluto/rea/blob/main/docs/mcp-contracts.md)。本报告的结论以此次本机实际返回值为准。
