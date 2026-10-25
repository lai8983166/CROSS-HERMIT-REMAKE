# Proposal

## Why

前驱已验终局请求、暂停和显式工作处理器，但原454CF0/4CE8F0尚未在当前战斗实例实际接入。应先执行真实任务与输入复位，定位首个表现资源边界，避免继续以处理器补充根代替VM推进。

## What Changes

- 两例新战斗实例自然生成中性/到时终局请求后，执行原输入请求复位及两帧完整454CF0→453F10→世界→事件根顺序。
- 第三原任务自然进入VM，执行原首条167并构造固定覆盖层包，停于原407870资源查询入口，保留完整CPU、原栈、SEH、包和全部拥有内存。
- 实际执行空字符串lstrlenA及null上下文ImmGetOpenStatus，原IAT保持；独立状态/栈/包规则和新实例完整重放，完成相关回归、前驱保全与归档。

## Capabilities

### New Capabilities

无。

### Modified Capabilities

无。落实reverse-engineering/completion的R3/R5连续任务/VM来源和验收要求，只有研究工具及证据变化，skip_specs为true。

## Impact

主机只声明原根顺序及资源入口停点，不伪造资源记录或清等待/改PC，不关闭绘制门。新输入缓冲、null IME及覆盖层原点/owner是明确初始方法输入，未称原加载或渲染初始化。停止时第三VM/任务未返回，不执行后续结算或原清理；实际拥有TLS资源单独结束。完整显示、VM脚本完成、外层线程、任务退出/奖励仍待完成，无OS输入/解锁/Godot改动。
