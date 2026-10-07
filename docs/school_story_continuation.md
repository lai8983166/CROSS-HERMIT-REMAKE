# 授课后的剧情与周推进

原版证据：analysis/school-story-week-v3-20261008.json。复跑命令：

    python -m tools.school_story_week_emulation --out analysis/新的审计文件名.json

这次在同一隔离CPU中执行新局初始化、课程10授课成长、确认、MVP、CH003、Chapter016、Chapter017以及state7周函数。Chapter017原版END后实际请求7；驱动消费请求，原版4D3510将4/4推进为4/5，做职业解锁、物品和技能清理，随后state7原版载入CH001、保存next8并请求6。两个中文剧情的TEXT执行顺序与源指令逐条一致。

4/4日期、seed4660、结果任务分配、图形/音频就绪和任务调度器消费均为声明边界。继承审计环境的四个周标记值(0,8,0,99)是声明输入；不把它们称作原版真实初始标记。学生可用性、初始装备、职业解锁则取同次源初始化后的记录。源游戏SAV未改动，也没有直播画面见证或原版持久写入授权。CH001正文和第五周学校初始化尚未执行。

淡出未就绪时，周函数已完成，但CH001还未加载；剧情按键未就绪时没有周函数执行。守卫拒绝非参与者的技能写入和MVP计数写入，避免重复或越界结算。历史审计保持原字节。

prototype/data/school_story_week_rules.json只包含规则和声明的初始辅助字段；成长能力、技能状态与职业进度必须由当前试玩记录组装。原版前后期望快照单独放在school_story_week_evidence_v1.json供测试比较。

## 剧情素材导出

    python -m tools.school_story_export
    python -m unittest tools.tests.test_school_story_export

输出prototype/assets/school_story：109页、162条原文、两张背景和三张组合立绘。Chapter016/017的普通目录与BIG5目录字节相同。按TEXTACTIVE和角色板编号确定说话者，连续TEXT合并到按键页；同一个原版按键等待内切换说话者时拆页，使用重制点击节奏。不会从文本池参数猜角色。

背景8/52经原版0x621bbc表定位为BG002_D/BG013_D。角色4/7/130经0x622250表定位MC004/MC007/MC130；名字取0x621f2c。130是夏朧的场景造型。MC素材实际尺寸512×1024，不能沿用相同字节长度H-PART的1024×512。按4C9690裁512×768身体，按4C97A0裁expression0的128×128表情，并用源表坐标合成。catalog记录源文件和PNG的SHA、坐标及展示边界。背景、人物可见性、文字顺序来自源脚本；布局、点击节奏是重制界面，暂未播放音频和还原渐变。

六条繁体中文文本保留了日文全角空格字节8140，导出时只将这一明确字节序列转为Big5全角空格A140，其余严格解码，拒绝替换字符和未知控制分支。

## 阅读会话与存档

playground的旧4/4源会话保持原契约，新增续篇拥有阅读游标与周结果。story_start开始，story_next逐页推进，story_prev重读，story_skip直接完成109页。阅读不改成长、职业进度、关系和MVP。进入故事后锁住课程命令，完成后week只结算一次；周输入从当前成长/确认记录组合到源初始化辅助字段，不能从期望快照恢复。

新存档version2使用school_playground_story_4_4上下文和六个规则/剧情资源指纹。载入时在候选会话重放命令并核对完整状态SHA，验证成功才发布。version1按原四个指纹、原状态哈希和仅旧命令验证，随后保存时写version2；已验证的旧完成存档固定为school_playground_legacy_v1.json回归素材。原路径、备份恢复与坏文件留存行为保持。
