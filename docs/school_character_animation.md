# 角色动画与第三句对白入口

本阶段沿第五周实际编班取证链，继续前轮 `SC004.BIN` 真实纹理加载后的原版 CPU。输入仍是三个隔离实际案例：initial、student9_waiting、fifth_class；前置八阶段逐字节重放核对。Godot 可玩界面未在本阶段修改。

## 来源规则

原版 opcode30 的实际分派来自 `4D03CF` 表，等待分派来自 `4D06AB → 4D066F`；不能依赖反编译器的 case 名称。配置8选择图层5，style5六片边框来自 `6247E8`，角色主体及表情来自 `622758`。

从 `4CC0D2` 原始栈继续执行图像加载调用者和 opcode30 尾部。背景设置为 mode3、时限60；对白框设置为 mode6、延迟30、淡入时限45。后续更新为显式调用原版 VM，不能当作世界主循环或真实帧时钟。

| 更新索引（从0开始） | 原版状态转移 |
|---|---|
| 0–29 | 对白框延迟递增，角色背景淡入 |
| 30 | 延迟计数超过30，框转 mode3，此次尚不绘制框 |
| 31–60 | 框淡入，背景继续淡入 |
| 61 | 背景使用递增前计数61判断超过60，转 mode2 |
| 62–75 | 背景稳定，框继续淡入 |
| 76 | 框使用递增后计数46判断超过45，转 mode2；此帧仍走淡入分支 |
| 77 | 两个原版 readiness 均返回1，等待清零；框稳态呈现姓名 |

每次等待更新执行 `4CD060` 和 `4CD120`，分别检查所有活动层的框状态与背景状态，不能用某一层局部计时替代。总计78次更新、154次真实来源 readiness 调用。

终端边界分别记录六片边框、填充矩形、主体、表情与姓名参数。`4CA860 → 4077C0` 的姓名绑定及颜色/标志写入实际执行；`408F90` 绘图队列函数在入口被精确终端适配，未执行 GPU 绘制。旧图层7两条对白继续按原版更新和来源参数呈现；图层5文字对象在动画期间仍为空。

## 第三句对白

原解释器每次更新只执行一条指令。解除等待后，下一次更新执行 opcode43/config8，选中图层5并完成稳态呈现；再下一次更新执行 opcode17/text index2，完成文字查找、Big5成对分行和首记录前缀，停在自然 `CreateFontA` 入口。最终 PC280、wait0、opcode17/size6。

完整比较激活时和最终八个程序区域、四个自然调用输入、单行文字字节及指针、14个字体参数、VM/文字/字体帧与 SP；此前图层7文字和四张真实纹理全部保持。第三句字体 API、栅格、纹理创建、文字处理器完成和第三句淡入尚未执行。

## 验证与重放

规则：`tools/school_character_animation_catalog.py`。实际执行：`tools/school_character_animation_emulation.py`。独立比较：`tools/school_character_animation_verification.py`。

```bash
.venv-audit/Scripts/python.exe -m tools.school_character_animation_emulation --out analysis/new-character-animation.json
.venv-audit/Scripts/python.exe -m tools.school_character_animation_verification
```

报告使用全新路径，保存全部更新的完整区域及参数。父阶段四张纹理、设备、工厂、隐藏窗口、实际只读文件和三个剩余测量 DC 的释放由原有外层所有权管理；新增阶段没有新分配平台资源。独立比较拒绝被篡改的计数/等待、透明度、readiness、更新顺序、字体栈、文字字节、真实像素、清理结果及越界执行声明。

本阶段没有原版绘图队列、GPU draw/Present、世界调度或完整连续对白证明。下一步是从第三句字体入口完成真实栅格和纹理，再核对其自然淡入/等待，然后实现已经核对的角色图层图形演出。
