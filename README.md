# 超魔法大战 (Cross Hermit) 研究工作区

2002 年 EnterBrain 出品的 SRPG+养成游戏，2004 年光谱资讯繁体中文版。
本工作区用于**私下研究**：黑盒规则逆向 + 素材格式分析 + 复刻原型。

## 目录

| 目录 | 用途 |
|---|---|
| `analysis/` | IDA/Ghidra 工程、内存 dump、Cheat Engine 表 |
| `docs/` | 规则逆向笔记（ET 系统、数值公式、关卡数据结构） |
| `extracted/` | 素材解包输出（图片/音频/文本，按来源目录分） |
| `tools/` | 分析脚本（封包扫描、熵分析、Big5 文本提取） |
| `prototype/` | Godot 复刻原型 |

## 本体就位后的工作流程

1. **安装前**：保留光盘原始镜像（.bin/.cue 或 .mds），音乐可能是 CD 音轨，镜像里才有完整素材
2. **安装后**：先对完整安装目录做一份未修改备份，并导出注册表
   - `reg export "HKLM\SOFTWARE\WOW6432Node" game_reg_backup.reg`
3. **第一轮分析**（不逆向代码）：
   - `python tools/scan_pack.py <游戏目录>` → 列出所有文件的头 16 字节 magic、大小、熵，判断哪些是打包文件、哪些压缩/加密
   - `python tools/extract_big5.py <文件>` → 从二进制中提取 Big5 中文文本串，定位剧情/对话脚本
4. **第二轮**：Cheat Engine 扫内存，逆出角色属性结构和伤害公式 → 记入 `docs/`
5. **第三轮**：Godot 搭原型，先复刻 ET（Element Time）实时指令冷却系统

## 运行环境

- Python 3.8+（脚本零第三方依赖）
- 分析工具建议：Ghidra、Cheat Engine、Tiled（地图）、Aseprite/PS（素材对照）
