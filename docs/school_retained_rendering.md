# 原初始化与保留场景渲染（R2）

当前 change：`connect-retained-vm-rendering`。R2仍未完成；不以初始化成功或透明矩形的黑色读回作为可见输出验收。

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

## 当前边界

真实矩形draw已执行，但alpha0导致黑色输出，尚未接受为R2实际画面完成。下一步继续原文字的GDI、动态纹理、顶点和真实绘制。完整下一任务帧在425F17触发424F80调试断言，源于输入对象索引−1；它属于R3输入/外层调度初始化，不能伪造断言返回绕过。R2可明确声明新的有界原VM调用根推进渲染样本，不能称作全外层帧已贯通。
