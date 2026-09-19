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

## 2. 偏移表档案容器 (.BIN 多条目) ✅已全量枚举 (2026-09-17, tools/enum_container.py)

**统一格式**（单图 .BIN 即 N=1 特例, 与 §1 融合）:
```
[u32 总长=文件大小][u32 条目数 N][u32 偏移[N]]   首条目 = 8+4N, 末条目止于总长
```
全库 432 个容器 / 1,578 条目: DXIMG 478 / BMP 683 / TEXT 160 / 嵌套? 257
(清单: analysis/container_enum.json)

| 容器 | n | 内容 |
|---|---|---|
| DEMODATA.BIN | 57 | demo 演出 = **57 张 DX 图帧序列** |
| OPDATA.BIN / OPDATA_256.BIN | 48+48 | OP 动画 = 48 帧 DX图 + 同帧 8bpp BMP 版 |
| KOJINDATA.BIN | 47 | 个人状态 CG |
| COMMON.BIN | 580 | UI 图集: 461 BMP + 116 文本(含 Dm-No-MakeTe 构建标记) |
| HANDATA/EDDATA/ALLRESULT/SLPROG/TACTICSRESULT/WORKROOM/OPTION/NETDATA | 3~12 | 场景图组 |
| TITLE.BIN | 8 | 6 BMP + 2 DXIMG |
| TACTSTART*.BIN | 2~5 | 战斗开场图 |
| EFCT.BIN | 7 | 特效: 条目内又嵌 {u32 尺寸, u32 子数, ...} 子表 |
| **UNITPAL.BIN** | 70 | **8bit 纹理调色板库: 70×1024B = 256×4B(BGRX, 0号=透明黑)** → 关闭"调色板来源"开口项 |
| T*.BIN | 2 | 战斗脚本容器 (即 §4 的 {len, nblocks=2}) |

- `COMING.BIN` 内嵌标准 BMP ✓; T*.BIN 在 SCRIPT/ 与 SCRIPT/BIG5/ 各计一次 (安装器冗余副本)

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


## 5. 战斗地图 ✅加载链与全部格式定性 (2026-09-17)

`DATA/TACTICS/MAP/` 每图 4~5 件套。加载器 (MapCtrl.cpp/PathFind.cpp, yoshida):
`43a640`(BIN→MapCw 逻辑图) / `43a920`(MAP→gmp 表现图, 失败回退 BMP) / `44e440→44e4c0`(VPT→寻路 wk)。
文件名表 @0x6B13F0 = {bin,map,bmp,vpt}×50 交错指针数组 (步长 0x10)。**格 = 32×16px** (4404a0: W<<5, H<<4)。

| 文件 | 格式 | 状态 |
|---|---|---|
| `MAP##.BIN` | **逻辑格图**: 16B头 + cellW×cellH×3 层 u16 | ✅ 头部已解 |
| `MAP##.BMP` | 172×128 8bpp 回退纹理 (+1KB 调色板) | ✅ 标准 |
| `MAP##.MAP` | **纹理页图集 + 表**: 48×256×256 u16 页 | ✅ 页定位已解 |
| `MAP##.VPT` | **寻路数据容器** (PathFind.cpp) | ✅ 容器已解 |
| `MAP67.CEL` | MapEdit 编辑器工程数据 (魔数 `MapEditFlIDCode`, 含 `D:\` 开发路径) | 🗑️ 无游戏价值 |

### BIN (逻辑格图) — 交错格式定案 (2026-09-18 修正)
```
头 16B = 8×u16: [pxW][pxH][cellW][cellH][tileW=256][tileH=256][pageX][pageY]
  MAP01: 2048×1536px = 64×96 格 (格 32×16 ✓) ; 页 8×6
体: cellW×cellH × 3×u16, **cell-major 交错** — 第 k 格 = [terrain][variant][object]
  (MAP01 = 6144 格 × 6B, 共 36,880 ✓)
  修正前误读为"3 个 W×H 平面" — 平面切法重排后产生 x+64y≡0 (mod 3) 伪条带
  (与旧"object 每 3 行横条"伪像同源), 实机截图对照定案交错 (analysis/map_window_match.md)
MAP01 修正后实测: terrain 全格有值 {1..5,9..13,17} (11 占 37%),
  variant 仅 35 格非零, object 全 0; 层值非贴片 ID (同值格在图集分散取样)
引擎只把其中一层抽成 MapCm->data (W×H×2, 43a640)
```

### MAP (表现图集)
**投影定案 (2026-09-18, add-map-composition)**: 世界 = **直角网格** — 图集即世界图 (2048×1536 == px 头);
格 (x,y) = 像素矩形 [32x,16y,32,16]; 引擎 x>>21/y>>20 线性整除为原始证据, iso 8 朝向相关全灭 (≤0.113 vs 0.488) 反证。
"菱形观感"来自贴片绘制而非坐标投影。

**实机窗口验证 (2026-09-18, analysis/map_window_match.md)**: 用户实机截图 (1024×768) 模板匹配证明
屏幕 ≈ 图集 [520,500]-[1400,1100] 窗口 ×1.02 平移 (+428,+434) — **窗口内世界像素=图集像素, 逐格 NCC 0.9+**;
dy 全高恒 434 无跳变。例外 = 两条 48px 竖直缝带 (图集 x≈592/870 处, 非页边界) 从别处取样 —
即世界 = "图集大块平移拷贝 + 少数缝带另行拼贴", 页边界的断裂 (列差/基线 2~6×) 多为真实缝带/素材页交界,
**非页序错误** (行优先 0.488 仍最优: 列优先/翻转/转置 ≤0.354)。缝带取样源开口 (需第二相机位置截图)。
地图头部的 255×4B 三元组表 (a,b,c 对角爬升) 与 53×(u16,u16) 步长表语义**仍开口** (疑高度/条带数据, 非贴图映射)。
```
头 8B = [u16 pageW][u16 pageH][u16 xy 字节对(疑起始格, 0xFF00=无)][u16 y]
表区 (变长): 255×4B (u,v,变体) 索引表 → 0x404 起 DX 对象头 (53×(u16,u16) 步长表等)
纹理页: pageW×pageH × 256×256 u16, 步长 0x2000C (每页 12B 头 "DX\2"+256×4 + 0x20000 像素)
  (MAP01: 0x4D8 起 48 页, 文件恰在末页像素结束; MAP02: 0x404 起 108 页)
```
- 页定位法: 连续 256 u16 全 bit15 置位 (严格门限); 像素格式 = **X1RGB555** (与 §1 全引擎 DX 图像
  一致; 实测 bit15 100% 置位, 主色暗灰棕系石地色; 验证渲染 analysis/_page0_555.png)
- gmp 内存对象 = 文件原样 (42ac50 仅 ReadFile 无解压); +0x404 = 内嵌 DX 子系统对象 (4167e0 初始化)
- **渲染验证 (2026-09-17)**: 48 页按行优先拼合 2048×1536 (`analysis/map01_atlas.png`),
  与回退 BMP 缩略相关性 0.488 (行优先) vs -0.012 (列优先) → 页序=行优先确证;
  相关性未达 0.9 系 BMP 尺寸非严格等比 (172/2048≠128/1536) 且疑为风格化小图
- 小地图黑区 = 战争迷雾 (开局未探索), 非世界形状 (terrain 全格有值佐证)

### VPT (寻路容器) ✅结构定案 (2026-09-17)
```
[u32 总长=文件大小][u32 n=8][u32 偏移[8]]  数据从 0x28 起
条目 0~3 (相同×4 = 4 路并行寻路工作区): 序列化导航图
  {16B "MapEditFlIDCode " 魔数 | u32 28 | u32 节点数 N | u32 相对指针[N] (44e5d0 重定位+基址)}
  节点子对象变长 0x10~0x58: 含 float 坐标 (格级小数, 如 42.92) + 邻接链
  MAP01: N=73 节点 / 0x2108B; MAP02: N≈? / 0x2980B
条目 4~7 (相同×4): 每格→导航节点 id, u16[cellW×cellH] (值域=节点数)
  MAP01: 73 个不同值 ✓; MAP02: 0x6C00 = 96×144×2 ✓
```
重制建议: 无需解析图结构 — 用 BIN 可行走层重新生成导航网格 (HPA* 簇图)。
字段级解码入口: findpath 模块 437c10~4398d0 (31 函数)。

### 开口
- [ ] 大纹理 this+0xdc (MapCtrl 嵌于战斗控制器 BigObj+0x3ef8, DxTex 类 403xxx) 的内容构造处 —
      绘制函数 0 引用之谜 (疑内联/精灵系统分发); 布局已三重定案不阻塞
- [ ] BIN 层值语义: terrain {1..5,9..13,17} = 地面参数表索引 (0x4C/值 ×5 组×4 参数, 表源 mapcom.bin,
      43b8b0/43b9e0/43be60) / variant 35 格非零 (43bb90/43bd00 读写) — 战术参数, 非贴图选择
- [ ] 阴影动态算法 (43d270 印章 33 形状 + 43fd80 绘制; 运行时计算非文件)
- [ ] MAP 头区 0x10..0x404 的 253×3B 爬升表 (值域 7..248, 与页布局无关)

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

## 10. DxAnim 动画容器 (DATA/DXANIM/*.BIN) ✅单位档已定案 (2026-09-18, tools/unit_anim_export.py)

文件分三类 (色相量化 + 视觉目检定案):
- **`{A..E}{0,1}A.BIN` (10 档) = 单位精灵**: 每档一个角色全动作集 (本体+挥砍特效混装),
  121 动画 × 138~251 帧, 帧最大 215×280, 多色相 (肤/发/衣料)
- **`##E.BIN` (01E..53E) = 特效档**: 全档单色相 (如 01E = 品红斩击 + 蓝色光球), E = Effect。同容器 9 块格式; 块0 动画为**播一次序列** (首帧 dur=20 定格 + 后续 dur=6 降序帧串); 01E 实测: #14..#28 帧引用把 5..93 分成连续带 = 各特效帧带 (视觉标注: #15=紫月斩 (帧5..10, 唯一已验真斩击) #28=光球弹丸 (帧88..93); 帧11..30=软泥怪素材带 (23..26=史莱姆本体, 两次误标斩击事故源) 31..75=蓝色弹体/软泥带)), #1..#13 全为外部引用 (帧号 ≥ 本档帧数, 跨档续编语义开口) — tools/fx_export.py
- **`EFCT.BIN`** = 7 块嵌套子表的特效合集; `TACTICS/COMMON.BIN` (580 条) = 头像 50×50×96 +
  技能图标 36×36×288 + UI, 与单位精灵无关

容器 = §2 档案容器惯例 `{u32 总长; u32 块数; u32 offs[块数]}` (offs[0]==8+4n 自洽; 相邻相等=空块):

| 块 | 语义 | 状态 |
|---|---|---|
| 0 | 动画定义表 `{len; n; offs[n]}`, 条目 = k×10B 记录 `(i16 画布w, i16 b, i16 -1, i16 d, i16 时长)`; **b≤-2 → 帧索引(-b)**, b==-1 → 空白帧, b≥0 → 控制/终止记录 (0x0801 头 / 32643=0x7F63 终止符); 记录顺序=播放顺序 | ✅ |
| 1 | 合成动画表 (A0A 27 条, 头记录 2049=0x0801, 内嵌控制记录) | ⬜开口 |
| 2 | (常为空块) | — |
| 3 | 未知小表 | ⬜开口 |
| 4 | 运动步进字节码: 5×i16 记录 `(op, 7, dx, dy, 单元id)`, op ∈ {0xFF06, 0x7F06} | ⬜开口 |
| 5 | **帧数×8B 直排无头**: `(画布w, 画布h, 帧x, 帧y)` i16 — 帧在画布中的摆放 | ✅ |
| 6 | 帧容器 `{len; n; offs[n]}`, 每帧 = **标准 8bpp BMP** ("BM"+DIB40+内嵌 1024B 调色板+底上行序+4 对齐 stride, 索引 0 = 透明) | ✅ |
| 7 | 换色调色板 `{len; n; offs[n]}`: 单位档 40×1024B / 特效档 6×1024B。**[0]=基色** (==身体帧内嵌, dist=0; 各档身体帧占比 55~87%, 余为特效帧独立调色板); [9]=黑影红边特殊版; 分组见步长9 ({10,19,28,37} 等); 引擎选择字段未定位 → 重制侧 battle_setup 手配 (tools/unit_recolor_export.py) | ✅导出/⬜选择字段 |
| 8 | (帧数+1)×u8 标志 (0/1), 语义未定 | ⬜开口 |

- **引擎单位表 (EXE VA 0x610538, 2026-09-18 定案)**: 31 条 `{char* 文件名; u32 0x20000|槽位}`，
  **按 job_id 索引**: 0=b1a(特殊) | 1=**b0a=重甲巨剑骑士(重战士)** | 2=b1a | 3=**a0a=剑盾兵(剑士)**
  | 4=a1a | 5=c0a(男弓手) | 6=c1a(女弓手) | 7=e0a | 8=e1a(僧侣,持杖) | 9=d0a(法师)
  实机截图对照 (2026-09-18): 重战士前排=**b1a 全甲长柄型** (b0a=巨剑型变体, 成对 job1/2);
  ~~B1A 曾被误判为"幽灵怪"(盔羽误读)~~
  | 10=d1a | 11..30 循环复用 1..10 的档。~~视觉鉴定~~ B0A 曾被误判为"魔法阵"——那是 IDLE
  挑帧误选特效帧, 行走帧视觉验证=全甲骑士; 单位↔档映射开口**已闭合**
- 特效 ano 编码 (UnitAnim.cpp 0x465280): `ano = q*1000 + r`, q∈0..3 选 0x60F890 处
  4×200 指针表的子表, r∈0..199 表内序号; 文件名表 @0x610630 起 (##e)
- **块1 = 合成动画表 (定案 2026-09-19)**: `{len;27;offs[]}`, 条目 = 10B 记录序列 —
  `(0x0801/0x0601/0x0501, X, dx, dy, 0)` 引用块0动画#(X+5) 带位移; `(0,-帧,-1,d,dur)` 直接帧;
  `(2,...)` 控制记录。引擎 off=1 的朝向播块1条目 (off=0 播块0#(号+5)); 展平导出为 composites[]
- **汇编链闭合 (2026-09-19)**: 0x464d70/0x465040(表A@0x60D160+布局@0x610510) → (b0=号, off=b1&3)
  → 0x409ff0 → 0x40a400 → 0x409f70(manager->0x1c 字段[off]=块[off]) → 0x4214f0(块, 号)=条目;
  调色板选择字段亦闭合: 0x409b70 `pindex≥1 → 块7[pindex-1]` (单位表 0x610538 第二字段 0x20000|slot 的 slot)
- **引擎动画编址 (EXE 逆向定案 2026-09-18, 全档统一语义槽位)**: UnitAnim 0x464d70/0x465040 —
  表A@0x60E850(结构@0x60D160) + 布局表@0x610510(dir 1..9→基址) + 表B@0x60F070(恒等);
  **引擎动画号 → 块0 下标 = +5** (引擎0=空→块0#5; 引擎6..10→块0#11..#15 五条行走带)。
  动作 no=2(移动): d5/8→#11(左) d7/9→#12(右,mirror) d4/6→#13(右斜,mirror) d1→#14(左斜)
  d2/3→#15(正面,mirror=背面); 动作 no=1(待机): #7(正面站) 等。walk_by_dir8 已写进
  unit_sprites.json (W/E/N/S/NW/NE/SW/SE → 块0槽位+镜像位), 视图按移动向量 8 向选带
- A0A 实测: 块0 121 动画含 5 组 6 帧行走循环 (帧 194..223) + 5 组 4 帧循环 (17..36 / 196..215) +
  带停顿的复合循环 (#89: 30/58 帧空白→8 帧行走) — 视觉验证 224..239 连续帧 = 完整持剑盾行走循环
- 锚点定案: **画布底中 = 脚底**, 帧内偏移 = `(画布w/2 − 帧x, 画布h − 帧y)` (数据推导)
- 导出: `tools/unit_anim_export.py` → `prototype/assets/unit/<档>/frame_*.png + _preview.png` +
  `prototype/data/unit_sprites.json` (帧表/锚点/动画序列/anim_map 启发式默认, 全 JSON 可改)
- 开口: 动画语义标签 (哪个 anim id = 何动作/朝向) 未从引擎定案; UNITPAL.BIN 70 调色板疑为
  战场单位阵营换色 (与 DxAnim 帧内嵌调色板无关)

## 提取产出 (2026-09-17)

- `extracted/img/` — 260 张 PNG（含 alpha），67MB
- `extracted/text/` — 392 份 YBC 提取文本（UTF-8, 带偏移），2.2MB
- `extracted/manifest.csv` — 全量 8101 文件清单
- 音频 (MP3/WAV) 与地图 BMP 为标准格式，原地使用不复制

## 待办
- [x] ~~多条目容器条目枚举器~~ → 已解: tools/enum_container.py, 432 容器/1,578 条目 (见 §2)
- [x] TACTICS SCRIPT 字节码反汇编（见 §4, 45/45 + 4,842 条文本提取）
- [ ] MAP/VPT/CEL 布局解析（对照 BMP 纹理拼图验证）
- [ ] YBC 分段表结构（X/Y 字段含义）
- [x] ~~8bit 纹理的调色板来源定位~~ → UNITPAL.BIN 70×256×4B (见 §2; 与具体 8bit 纹理的绑定关系待查)
