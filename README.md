# 超魔法大战 (Cross Hermit) 研究工作区

2002 年 EnterBrain 出品的 SRPG+养成游戏，2004 年光谱资讯繁体中文版。
本工作区用于**私下研究**：黑盒规则逆向 + 素材格式分析 + 复刻原型（Godot）。

## 当前状态 (2026-10-02)

已建立素材解析工具和 Godot 离屏战斗原型。当前战后转接变更完成 10/13；七组原版收尾函数隔离回放及 Godot 逐帧核对已建立，VM 完成与外部输入仍为合成前提，不授权持久事务。最新记录见 `docs/battle_return_audit.md` §16。

入口文档：

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
| `prototype/` | Godot 复刻原型、离屏战斗模拟器及测试 |

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

### 启动原版取证

```bash
python tools/launch_original.py --check  # 检查本地原版与关键资源
python tools/launch_original.py          # 使用安装快捷方式对应的中文启动入口
python tools/launch_original.py --direct-game  # 仅在明确诊断时直接启动游戏 EXE
```

启动器由自身位置解析原版路径，因此可以从其他目录调用。默认入口为 `CROSS HERMIT CHT.EXE`，与安装快捷方式一致，工作目录固定为其所在的游戏目录。不要把项目根目录当作原版的工作目录：原版使用当前目录解析资源。2026-10-02 排查中，不显式指定工作目录的直接启动出现 `DXAudio.CPP:568 / DMUS_E_LOADER_FAILEDOPEN / RegistWaveData()`；显式指定游戏目录后错误消失，用户确认可见标题菜单。用户随后检查两个入口并确认没有区别，显示问题已停止追查。启动成功不等于战斗/结算流程已完成，详见 `docs/battle_return_audit.md` §8–9。

### 原版退出函数的隔离核对

```bash
python -m venv --system-site-packages .venv-audit
.venv-audit/Scripts/python.exe -m pip install -r tools/requirements-audit.txt
.venv-audit/Scripts/python.exe tools/tactics_exit_emulation.py --out analysis/new-exit-report.json --godot-out analysis/new-exit-fixture.json
.venv-audit/Scripts/python.exe -m unittest discover -s tools/tests
```

该工具在隔离内存中执行经 SHA-256 核对的原版 x86 指令，不需要启动或操作游戏。输出必须使用新文件名；时间、动画及 VM 等外部输入明确模拟，不代表真实场景已经走通，也不授权角色或日历写入。Godot 模块 `prototype/sim/tactics_exit_handshake.gd` 只复现已核对的脚本完成后收尾部分，其七组逐帧期望值由上述原版指令执行导出。尚未接入学校持久事务。

- Python 3.8+（PIL 用于图像渲染）
- Ghidra 12.1.3 + JDK21（仅重新反编译时需要，产出已入库）
