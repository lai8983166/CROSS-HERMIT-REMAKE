# CROSS HERMIT 数据格式档案

> 分析对象: `F:\project\chaomofa\CROSS HERMIT\CROSS HERMIT\`（光谱繁中版, 8108 文件 / 1.47GB）
> 结论: **全引擎无压缩无加密**，熵值 1.4~3.9，所有格式为裸结构体。

## 1. 裸位图容器 (.BIN, "DX" 图像) ✅已破解

`DATA/ADV/BIN/*.BIN`（背景/事件图, 261 个, 291MB）及多数单图 .BIN

```
偏移  类型    内容
0x00  u32     文件总长 (如 0x00200018 = 2097176)
0x04  u32     图像条目数 (=1)
0x08  u32     0x0C (表偏移?)
0x0C  4B      "DX\x02\x00" 魔数
0x10  u32     参数A (00040003 / 00018000 等, 疑似 mipmap/flag)
0x14  u32     参数B
0x18  像素体  1024×1024, X1RGB555 小端
```

- **像素格式: X1RGB555** — `bit15=alpha(1=不透明)`, R=bit14..10, G=bit9..5, B=bit4..0
- 内容区约 1024×784，底部约 240 行为透明填充（统计: 每图精确 75% 不透明 / 25% 全零）
- 渲染工具: `tools/render_dximg.py`（RGBA PNG 输出）
- 误诊教训: 按 RGB565 解码时透明区(bit15=0)表现为暗红色，UI 类图看起来"基本正常"但背景图噪点严重 → 统计 bit15 占比恒定 75% 确认为 alpha 位

### 像素体尺寸对照表 (已全量验证, 260/261 成功)

| 像素体 | 尺寸×bpp | 参数区特征 | 内容 |
|---|---|---|---|
| 2097152 | 1024×1024×16 | `00040003/00040004` | BG/BATTLE/HAN/KOJIN 大图 |
| 1048576 | 1024×512×16 | `00040002` | H-PART 教学标注 |
| 524288 | 512×512×16 | `00020002` | GYBC ADV界面框套件 |
| 262144 | 512×512×**8** | `00048000` (含0x80) | TC 系列日程文字蒙版 |
| 65536 | 256×256×**8** | `00018000` (含0x80) | B-PART 面板高光蒙版 |

- 参数低字节含 `0x80` → 8bit 强度/蒙版纹理; 否则 16bit X1RGB555
- 8bit 调色板不在文件内（索引 255≈白色字形, 0=透明底），推断用全局调色板或作纯 alpha 用
- `DUMMY.BIN`(128B 像素体) 为占位文件

## 2. 偏移表档案容器 (.BIN 多条目) ⚠️结构已知, 条目待枚举

`EDDATA.BIN / DEMODATA.BIN / MENU / WORKROOM / TACTSTART / TACTICSRESULT / ALLRESULT / SLPROG / COMING.BIN / DXANIM`

```
[u32 总长][u32 条目数 N][u32 首偏移][u32 偏移1]...[u32 偏移N][数据...]
```
- `COMING.BIN` 中直接内嵌标准 BMP（魔数 `BM`）
- `DEMODATA.BIN` 115MB / `OP` 合计 248MB — 疑为 OP 动画帧序列（X1RGB555 帧或多图层）

## 3. YBC 事件脚本格式 (.YBC) ✅已破解并全量反汇编 (2026-09-17)

`DATA/ADV/DAT(193)/BIG5(153) / ALLRESULT/DAT(15)/BIG5(14) / YSTEXT(9)/BIG5(8)`

容器（同 4cd700 读取器）— 之前的"MVP 型/CHAPTER 型"两形态猜测作废:
```
{u32 nblocks(1~8); u32 off[nblocks]}   头 20B = n=4 + 3 个块偏移的特例
block0 = YBC32 字节码 (与 T*.BIN 同一 VM, 分发器 4CE8F0, 编码见 §4)
block1 = 0x30 定长记录, NUL 路径串 (data\adv\bin\b-part001.bin 等 = 资源/子脚本引用)
block2 = 文本池 {u32 n; {u16 off; u16 prm}×n; NUL 串}  (同 §4 格式, prm>>5=話者ID)
```
块可缺失 (offs[2]==len 时无文本池, 如 MAP.YBC / BATTLE*.YBC)。

**语料统计** (反汇编器 `tools/ybc32_disasm.py` 直接吃 .YBC):
- 中文版 (BIG5 子目录 175 文件, 与顶层同名文件字节相同 — 顶层已被中文化) → `analysis/ybc_disasm/` 18,388 条文本
- 日文原版仅存 42 个无 BIG5 对应的文件: ADV/DAT 40 (BATTLE* 13, CH/HAN/KOJIN/MENU/MAP/MM/HATUBAI/SUBCHACK 27) + MVP.YBC + FUNCTIONEXP.YBC → `analysis/ybc_disasm_jp/` 1,642 条文本 (**编码 cp932**; 0x8740+=①②③)
- 共 217 文件 / 60,879 指令 / 58 种操作码 / 20,030 条文本

ADV 语料高频操作码 (与 T*.BIN 同名同语义, 详见 battle_scripts.md §2):
TEXT 19,951 (186 文件) / KEYWAIT 8,072 / TEXTWAITKB 7,999 / TEXTACTIVE 6,216 /
TEXTCLEAR 5,896 / BGM 5,073 / FADESETWAIT 1,088 / VWAIT 808 / CHARSET 564 / SCRIPTEXEC 413
ADV 特有: **op151 = FLAG_SET** (处理器 4d12d0): 取 cell 值 idx → 全局标志字节数组
`0x7D4F3C[idx]=1` (4e3170, idx 钳 0..0x7F, 同时存 VM+0x9250), 全部出现在淡出转场后 —
事件已读/解锁标志 (回想模式的开关位), 99 次/61 文件。

- 繁中 Big5 文本未混淆直存, `tools/extract_big5.py` / `tools/batch_extract.py` 全文可提取（392 份已导出）
- 文件名: CHAPTER*(章节) BATTLE*(战斗) MVP*(结算) ITEMEXP/FUNCTIONEXP*(物品/技能说明) KOJIN*(个人) HAN*(操作说明)

## 4. 战斗脚本 (T*.BIN, YBC32 字节码) ✅已破解并全量反汇编

`DATA/TACTICS/SCRIPT/T*.BIN`（45 个）— 战斗内事件/对白/胜负判定脚本。
VM 分发器 = 引擎 `0x4CE8F0`（`SCRIPT/BIG5/` 为安装器冗余副本, 逐字节同 `SCRIPT/`）。

```
文件  {u32 len; u32 nblocks; u32 block_off[nblocks]}
块    {u32 size; u32 rcnt=101; u32 sub_off[101]}    子记录 = 块+off, 未用槽填 "dmf\0"
子记录 {u32 type=4; u32 code_off; u32 data_off}     代码 = 子+code_off, 文本池 = 子+data_off
代码  [u16 op][u16 adv][payload(adv-4)] × N         op 0x13(19)=CODE_END 终止
```

- **操作数 cell** = `u32: 类型<<28 | 值` — `t2`=立即数, `t0`=变量引用 (VM 线程局部 @VM+0x3C / 全局 @0x7AAB1C)
- **跳转目标** = u32, 相对代码基 (子+code_off)
- **文本池** = `{u32 count; {u16 off; u16 prm}×count}` + NUL 结尾 **Big5 字符串直存**
  (prm/32 = 話者 ID 推断, 同一说话者行值一致)
- **操作码名表** = 引擎 VA `0x624850` 150 项 (索引==操作码, `CODE_*`); 158~167/172 由处理器反编译定名
  (158~165 = `ComYken.cpp` UNITWK 读写 32/16/8/BIT 族, 166/167 = VM 寄存器, 172 = 子脚本加载)

工具: `tools/ybc32_disasm.py` → `analysis/script_disasm/T*.BIN.txt` (45/45) +
`_texts.json` (**4,842 条战斗文本**, 最多 T0044=534 条 / T0013=441 条)
脚本典型流: APPEARGROUP 出现 → EVENTCELLWRITEPOS 布事件 → BORDPACKONWAIT 开对话框 →
TEXT 逐行对白 → 每回合循环 IFGOTO 查 UNITWK/事件开关 → TACTSETDESTROYSCRIPT/胜负迁出


## 5. 战斗地图 ✅玩法网格已破解

`DATA/TACTICS/MAP/` 每张地图一组文件:

| 文件 | 格式 | 状态 |
|---|---|---|
| `MAP##.BIN` | **地形网格**: 16B头 + 高×宽格 × 6B `[u16 地形ID][u16 ?][u16 ?]` | ✅ 50/50 验证 |
| `MAP##.BMP` | 172×128 8bpp 地块纹理集 | ✅ 标准 |
| `MAP##.MAP` | 6.3MB **3D 网格/高度场**（熵 5.4~5.9） | ⚠️ 表现层, 重制可替换 |
| `MAP##.VPT` | 8 段顶点表, 内含 float（如 19.78） | ⚠️ 表现层 |
| `MAP67.CEL` | 地图编辑器元数据, 魔数 `MapEditFlIDCode`, 含 Shift-JIS 作者路径 `D:\シナリオ...` | 🗑️ 无游戏价值 |

### MAP##.BIN 网格细节
```
头 16B: [u16 0x0800][u16 6=格字节数][u16 高][u16 宽][u16 256][u16 256][u16 0x0800][u16 6]
体:     高×宽 个 6B 格子, MAP01 = 64×96
```
- 头部乘积匹配 50/50 全部地图; 地图尺寸不一 (64×96, 96×144, 64×192...)
- MAP01 地形ID直方图: 11(2250格), 2(812), 10(772), 4(691), 1(558), 12(384), 9(347)... 
- 地形ID→地表类型对照待游戏截图比对（`extracted/render/map01_grid.png` 有首版上色图）

## 6. 音频 ✅全部标准格式零处理

- `SOUND/BGM/*.MP3` 32 首 66MB
- `SOUND/VOICE/V*/RV*/*.MP3` ~5000 个（角色语音按章节分目录）
- `SOUND/PLW/**/*.WAV` 782 个（单位音效/环境音/战斗音）

## 7. 可执行文件架构 ✅已脱壳 (2026-09-17)

`CROSS HERMIT.EXE` (1,515,520B) = **商业自调试保护壳 + 游戏**:

```
启动链: CHT.EXE (26KB 光谱启动器) → CROSS HERMIT.EXE (父, 调试器)
        → CreateProcess 自身 (子, 被调试) → 子进程内解密出游戏原镜像
```

- 父进程驻留保护壳 (0x40e000~0x47xxxx): 原 .text/.rdata/.data 全零, 壳代码在高位段
- 子进程 = 真游戏: **原始 .text (1.6MB, VC6 debug 构建, 3841 函数)** 在原 RVA 位置解密就位
- 脱壳产出: `analysis/hermit_game.exe` (ImageBase 0x400000, 节表 raw=VA 修正)
- **游戏真 IAT 在 .rdata 起始 0x592000** (249 槽, 1065 个调用点): GDI 全套 (BitBlt/StretchBlt/
  PatBlt/CreateDIBSection/TextOutA/ExtTextOutA/CreateFontA) + WINMM (timeGetTime/wave) +
  QUARTZ (DirectShow 播片) + **D3D8** (3D 战斗表现层) + COMCTL32 ImageList (MDI 拖放 UI)
- 引擎是 **MDI 架构** (DefFrameProcA/DefMDIChildProcA), 主消息循环 `WinMain_message_loop` = 0x49DD70
- 关键函数地址表: `analysis/game_function_api_map.json`; IAT 名表: `analysis/hermit_real_iat.json`
- 反编译: `tools/ghidra_analyze.py` (PyGhidra), 产出 `analysis/decomp/*.c` + 全量 `analysis/decomp_all/`(按函数地址命名)
- **帧率控制器** `timing_fn_C` (0x415610): QueryPerformanceCounter 高精度 / timeGetTime 兜底双模式;
  游戏主工作结构体字段: +0xb17c 速度档(1/2/3), +0xb188 QPF 频率, +0xb1d8/0xb1e0 当前/上次时间(64bit),
  +0xb1e8 累计预算(64bit), +0xb1f0/0xb1f4 帧计数/跳帧计数; DAT_007a4a00 = 主工作对象指针 (帧更新 = 0x49E2B0)
- 窗口: 1024×768 (0x400×0x300) WS_POPUP 全屏; 主窗口过程 0x49E850, 第二窗口 0x424980; MDI 框架过程 0x424A90
- VC6 debug 构建: 栈填 0xCC、__chkesp 遍布、FUN_0042b2d0 = debug 日志器 (消息名/结构体地址都往 DbgLog 打)
- 游戏本体运行: 父进程 24016 调试子进程 34888 (两进程都叫 CROSS HERMIT.EXE)

脱壳工具链: `tools/unpack_all.py` (按游戏目录路径前缀抓全部相关进程 + 模块外私有可执行内存) →
`tools/make_clean_pe.py` (重建 PE 头) → `tools/ghidra_analyze.py` (标注+反编译)

## 8. 战斗机制 (反编译提取) ✅核心公式已还原

→ 详见 **`docs/battle_mechanics.md`**： 物理/魔法/固定伤害公式、属性缩放 12 模式、
命中-回避-倍率机制、AI 行动/移动双状态机、附加状态概率表、战后好感度结算、
全局数据表坐标(攻击表 0x6C2DC8/技能表 0x611538/职业表 0x6B2D88/单位数组 0x80AEC×0x520)
开口项: EXP 每级消耗曲线 (属性块字段语义已解 → `docs/character_growth.md`)

## 9. 其他

- 根目录: `CROSS HERMIT.EXE`(1.5MB 主程序), `CROSS HERMIT CHT.EXE`(26KB 启动器/转区壳?), `.ISU`（Inno 卸载信息）, `SAVEDATA/*.TXT`
- 光谱中文化只动文本层（ADV/DAT、YSTEXT、SCRIPT 均保留日文原目录结构 + BIG5 子目录副本）

## 提取产出 (2026-09-17)

- `extracted/img/` — 260 张 PNG（含 alpha），67MB
- `extracted/text/` — 392 份 YBC 提取文本（UTF-8, 带偏移），2.2MB
- `extracted/manifest.csv` — 全量 8101 文件清单
- 音频 (MP3/WAV) 与地图 BMP 为标准格式，原地使用不复制

## 待办
- [ ] 多条目容器条目枚举器（对照 OP/MENU 验证内嵌 BMP 或 X1RGB555 帧）
- [x] TACTICS SCRIPT 字节码反汇编（见 §4, 45/45 + 4,842 条文本提取）
- [ ] MAP/VPT/CEL 布局解析（对照 BMP 纹理拼图验证）
- [ ] YBC 分段表结构（X/Y 字段含义）
- [ ] 8bit 纹理的调色板来源定位
