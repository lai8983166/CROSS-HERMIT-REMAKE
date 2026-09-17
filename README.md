# 超魔法大战 (Cross Hermit) 研究工作区

2002 年 EnterBrain 出品的 SRPG+养成游戏，2004 年光谱资讯繁体中文版。
本工作区用于**私下研究**：黑盒规则逆向 + 素材格式分析 + 复刻原型（Godot）。

## 当前状态 (2026-09-17)

逆向主体完成（21 提交）。入口文档：

- **`docs/REMAKE_BLUEPRINT.md`** — 重制蓝图总览（按模块组织，公式结论+分档案指针）
- `docs/formats.md` — 数据格式档案（脚本 VM/地图/容器/图像/音频）
- `docs/battle_mechanics.md` — 战斗公式/AI/攻击表字段图/ENGAGE TIME
- `docs/character_growth.md` — 成长/课程/转职/道具/加成链
- `docs/battle_scripts.md` + `ybc32_opcodes.md` — YBC32 字节码档案

## 目录

| 目录 | 用途 |
|---|---|
| `analysis/` | 脱壳镜像、全量反编译（`decomp_all/` 按地址命名）、脚本反汇编语料、JSON 表 |
| `docs/` | 逆向笔记 + 蓝图（见上） |
| `extracted/` | 素材解包输出（PNG/文本，`manifest.csv` 全清单） |
| `tools/` | 分析脚本（脱壳管线、YBC32 反汇编、容器枚举、纹理渲染） |
| `prototype/` | Godot 复刻原型（待启动，建议从战斗模拟器起步） |

## 关键工具

| 工具 | 用途 |
|---|---|
| `tools/unpack_all.py` | 自调试壳脱壳（抓子进程 + 重建 PE） |
| `tools/ghidra_analyze.py` | PyGhidra 标注 + 全量反编译 |
| `tools/ybc32_disasm.py` | T*.BIN / .YBC 脚本反汇编（`-e cp932` 处理日文原版） |
| `tools/enum_container.py` | 偏移表容器枚举（432 容器/1,578 条目） |
| `tools/render_dximg.py` | DX 图像 (X1RGB555) → PNG |

原版游戏目录（`CROSS HERMIT/`、`超魔法大戰繁体中文版/`）不入库（.gitignore）。

## 运行环境

- Python 3.8+（PIL 用于图像渲染）
- Ghidra 12.1.3 + JDK21（仅重新反编译时需要，产出已入库）
