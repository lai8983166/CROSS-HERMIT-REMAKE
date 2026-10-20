# 原初始化与保留场景渲染（R2）

R2已于2026-10-21完成验收，change `connect-retained-vm-rendering` 3/3完成并归档。三个保留案例均通过原矩形和两行文字实际输出、独立机器码重放及资源寿命验证；55项回归、严格规格和保全检查通过。初始化成功或透明矩形的黑色读回本身不构成R2可见输出。

## 已验证的逻辑重建

`analysis/school-retained-render-reconstruction-v1-20261021.json.gz` 保存一次完整有效寿命实验。使用声明的新加载输入（游戏全局与字体缓存全局初值0），原412E30和413450在1000000h游戏根上执行，建立真实设备、两套字体/图集/顶点缓冲、状态块、队列和管理器，完整自然返回。没有在旧停点清零或手写owner/绘制门。

随后恢复经身份校验的initial/rectangle祖先检查点逻辑内存。仅保留原初始化实际产生的七段渲染/构造/缓存/计时状态，逐一记录来源、字节和42段完整逻辑内存的父/重建SHA。完整CPU上下文恢复，包括整数寄存器、栈、标志、浮点/SIMD及系统寄存器。平台指针使用有域、可逆的显式地址映射；助手中的对象始终由实际创建它的进程持有。

这属于资源重建后接回保留逻辑场景，**不是**零改动的旧检查点原地继续，也不恢复旧进程的失效句柄。原九份检查点不修改。最初的浮点/SIMD复核另行恢复同一CPU上下文并复核，记录明确标为稍后复核；后续执行在首次重建时直接记录该核对。

原机器码从40E2A0沿原栈执行裁剪/矩形入队、VM返回454D90，最后选中任务自然返回3000000h/EAX0。独立验证器重新加载检查点和初始化的实际队列状态，不代用游戏或平台函数，核对完整原指令流及所有原写入摘要。矩形命令是type4、274/580/473/154、layer67、color00223438；alpha为0。

实际原生平台全部正常释放，设备与桌面gamma恢复。初次图像读回超出旧3MiB桥上限的实验保留在私有失败记录中，不能用于正常寿命验收；专用有界桥扩至16MiB。

复核：

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_rendering_verification analysis/school-retained-render-reconstruction-v1-20261021.json.gz --out analysis/school-retained-render-reconstruction-proof-v1-20261021.json
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_retained_rendering
```

## 首轮实验边界（已由下述文字输出推进）

首轮真实矩形draw执行时alpha0导致黑色输出，未接受为R2实际画面完成；随后继续原文字的GDI、动态纹理、顶点和真实绘制，结果见下节。完整下一任务帧在425F17触发424F80调试断言，源于输入对象索引−1；它属于R3输入/外层调度初始化，不能伪造断言返回绕过。R2明确声明新的有界原VM调用根推进渲染样本，不能称作全外层帧已贯通。

## 原文字到真实设备输出

三个案例`initial`、`student9_waiting`、`fifth_class`分别从经校验的rectangle祖先出发。每例先执行原完整初始化、恢复逻辑内存和完整CPU，沿保留栈返回VM和任务，再声明67次4CE8F0有界VM根及原队列重置调用。原面板动画自然结束，PC224继续至文字激活、两行文字生成和PC248等待；没有写入PC、wait或绘制门来推动进度。

每行原4CAD09/405160路径自行调用真实CreateFontA、测量、DIB绘字，再由原403C87/40395B/405869/4039D0创建、锁定、转换、上传A1R5G5B5纹理。两张实际纹理尺寸256×32与256×64。原代码也执行字体、DIB及私有DC清理。初始屏幕DC由原构造GetDC得到，实际拥有它的Python进程服务后续GDI调用；GetDC的完整64位原生返回值保留用于ReleaseDC，x86源程序仍接收32位句柄。

随后执行原414C30（BeginScene、Clear、状态）、40E330（完整队列）、414DE0（EndScene和Present）。文字经原40F系列生成索引三角形及32字节顶点，实际DrawIndexedPrimitiveUP两次；矩形自然渐变到CC223438。真实1024×768帧缓冲以CopyRects/LockRect读回，PNG保留全部实际RGB像素。独立像素核对以源纹理透明/白色掩码、原矩形背景和原顶点alpha验证11929个透明像素、30个白色字形像素（混合容差2级，透明背景1级）。

原输入文字字节未转码，按Big5解读为“瑟希莉絲、伊里安。”与“再跟你們確認一次這次的作戰目的。”；本机ANSI ACP936使原CreateFontA/ANSI绘字回退到宋体，因此PNG仍有乱码。这如实保留了本机原ANSI调用结果，不表示已解决语言环境兼容。旧场景的静态精灵GPU纹理仍未恢复，当前边框中有空纹理产生的白块；本验收覆盖原矩形/文字渲染，不代表完整场景视觉还原、输入或世界帧已完成，也没有修改Godot。

专用原生桥v4补齐文字需要的8参数索引绘制，清理结果缓存避免`close`与进程finally重复释放。两次辅助错误请求分别验证未知设备身份和非原文字格式会被协议拒绝，属于平台边界拒绝，**不是**伪造的原D3D失败分支。v2漏接口、重复清理和屏幕DC符号扩展的开发失败原样保留为私有诊断；initial首轮用实际重试释放DC，记录`screen_release_attempts=[0,0,1]`，其余两例由修复后的工具无交互正常完成。

复现与独立复核（每例使用新的报告/图像路径）：

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_render_pipeline --case initial --out analysis/new-report.json.gz --image analysis/new-frame.png
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_render_pipeline_verification analysis/new-report.json.gz --out analysis/new-proof.json
```

验证器从原检查点独立建立Unicorn，恢复完整CPU、源初始化字段、实际队列及接口身份；仅注入已记录的真实平台返回/输出，全部游戏函数执行原机器码。逐根比对所有原指令、所有原写入、参数/完整几何/像素上传、CPU及自然边界。保留的原VM/任务返回与后续新根分开标明。

三例各207段执行、204个明确声明的新根，独立重放1936299条原指令一致；帧缓冲SHA均为`8bc242da1c4b3b2bd1db8d22cdc2f91cf11691a40f952e42353f3f197eb54613`。首例增加构造/设备/七段重建独立检查的v2复核与另两例均通过。验收文件为`analysis/school-retained-render-acceptance-v1-20261021.json`；保全审计确认16589份历史原始文件、20份R1前单元冻结材料（两份按既有R1归档位置解析）、9份原私有VM检查点和10份规则数据不变，安装存档的字节/时间戳及下载存档均不变。整体验收不改变R3–R6完成状态。

## R3交接

- 直接完整任务454CF0调用在425F17→424F80断言停止，ECX为FFFFFFFF，输入状态未初始化；保留原栈/寄存器诊断，禁止代用断言返回。下一change应定位原输入初始化和启动调用关系，连接真实输入/外层调度后再执行完整任务/世界帧。
- 连续执行已有文字等待逻辑，下一步需要真实输入捕获和后续交互/开场转换；R2的67次有界VM根不等于完整主循环。
- 在同一有效资源寿命建立旧资源表的实际纹理，恢复场景精灵和背景；旧记录中纹理指针0不能变成已恢复的图片。记录ACP936/Big5兼容问题，在后续环境兼容验收中处理，不能修改原字节并隐瞒。
- R4–R6战斗、事件、胜败奖励、后续主线与集成覆盖仍保持总规格未完成状态。目标日期2026-11-20不变。
