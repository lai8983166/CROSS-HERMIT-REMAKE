# Proposal

## Why

R2已将原矩形/文字接回有效设备，但后续仅调用VM根。完整任务的425ED0断言实际检查待处理IME请求标志；需要恢复原输入请求重置和任务调用顺序，推进R3的真实任务边界。

## What Changes

- 核实425DE0→425E60→425C70/IMM32及425ED0的原契约，纠正“输入索引−1”的旧解释；调用真实ImmGetOpenStatus，不使用旧声明结果。
- 在R2同一有效资源寿命与保留逻辑场景内，按原帧顺序运行输入请求重置、队列重置、完整454CF0任务及实际绘制，跨越面板/两行文字/等待转换，区别于只调用4CE8F0。
- 独立重放、三个案例、生命周期/相关回归及历史保全通过后本地提交、更新总规格并归档本有限change。

## Capabilities

### New Capabilities

无，研究工具实施；skip_specs。

### Modified Capabilities

无，不改变reverse-engineering/completion既有要求。

## Impact

复用R2初始化、原生桥、执行和复核工具，增加输入/完整任务驱动与来源证据。此change是R3的完整任务接通单元；原49E540/4217C0多线程外层调度、实际键鼠捕获、静态精灵GPU资源和完整世界交互仍需后续有限单元，不能因此标R3完成。R4–R6、Godot、原存档与既有检查点不改，不push。
