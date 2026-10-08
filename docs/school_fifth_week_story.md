# 第五周剧情续接

## 原版执行范围

`tools/school_fifth_week_emulation.py` 延续第四周原版初始化、授课、MVP、Chapter016/017 和周结算的同一 Unicorn CPU。真正的 state7 加载 CH001、存储 next8、请求 state6 后，声明的调度边界消费该请求；原版 `4D1A80` 和 VM 分派按 4/5 选择 Chapter018。

Chapter018 的末尾执行 opcode151 `(2,1)`、opcode91 `(6,2)` 和 END。原版处理函数 `4C4750` / `4D0DA0` 将 `7A55F6=2`、`7E11A0=1`、`7A5292=6`，随后请求状态8。角色能力、职业进度、资格、装备、可用成员、日期和MVP记录均保持原值。这些是剧情/流程标志，不能解释成已完成招生或学校初始化。

完整、按键等待、界面等待、淡入淡出等待四个实际原版执行案例记录在 `analysis/school-fifth-week-v2-20261008.json`。后续原版职务室 state8 本体和学校初始化尚未执行。保留原有声明的 4/4日期、探针标志、分配、绘制/音频就绪以及调度构造边界。所有原版写入只发生于隔离内存，没有修改原版存档；`live_witness` / `school_initialized` / `authorizes_persistent_write` 等权威字段仍为 false。

证据导出 `prototype/data/school_fifth_week_evidence.json`；运行规则 `school_fifth_week_rules.json` 只含来源、日期和状态边界、源指令操作数及三个写入规则，不包含期望完成快照。第五周写入保护只开放 VM及其展示槽、任务/控制器请求、已核验的临时区和上述三个全局标志，拒绝重新写入日期、成长、MVP和角色记录。

## 单独素材目录

`tools/school_fifth_story_export.py` 从本地中文 Chapter018 直接导出独立的 `prototype/assets/school_fifth_story/catalog.json`。旧剧情目录和指纹保持原字节。源剧情有162条文本，按键等待与说话者/资源切换整理成126页。第99条的 F9D8 字节是 Windows CP950 扩展字“裏”，使用严格 CP950 解码并记录扩展位置，不替换为乱码。

原版板配置表 `624520` 的槽5/6使用MC（大立绘512×768），槽7/8/9使用SC（小头像256×296）。MC资料表 `622250` 和SC资料表 `622668` 决定文件、面部裁剪与合成坐标；CHARSET会替换槽8/9角色资源，因此后段显示莉莉絲/謬菈与瑪貝菈/娜芙忒卡的实际替换图和姓名。

SC文件与TC蒙版同为262144字节像素体，但头部声明SC是256×512的16位X1RGB555；不能用按长度猜测的512×512灰度蒙版解码。导出器校验头部并按SC格式解码，再合成默认表情。目录包含3张MC、5张SC及背景47，共9张PNG，逐个保存源文件及输出SHA-256。TC0405仅记录原电影资源哈希，不声称已复现其播放、音频或淡入淡出时序。

## 验证命令

在项目根目录使用Git Bash：

```bash
PYTHONIOENCODING=utf-8 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_fifth_week_emulation tools.tests.test_school_fifth_story_export
```

原版执行和素材导出不要求用户手动操作旧游戏。

素材验证覆盖重新导出的JSON/PNG逐字节一致、162条文本全覆盖、资源替换后的说话者、MC/SC尺寸与表情合成像素，以及拒绝未知跳转和TC头部误作SC。原版证据SHA-256为 `a7cf35d5e3bfe555e232a09917cb816f8daaf55a308cbf5345a2fd3451fc23f1`。
