# 采集键盘与保留任务的离线连接

本单元 `connect-retained-keyboard-replay` 实施中。将2026-10-22已验的两个原版键盘采集流接到三个已恢复的逻辑案例，全部在客体中完成，不需要Windows保持解锁，不启动窗口或提交新系统输入。

冻结完整任务报告的67帧原指令先被完整独立重放，恢复矩形祖先的逻辑内存、原初始化覆盖与CPU，到PC248/opcode50文字就绪等待。随后继续原425DE0请求消化、原队列复位和完整454CF0；没有新增独立4CE8F0根。

宿主仅把固定采集样本的原始256字节写到客体声明的GetDeviceState输出区，再执行原4113D5–4116A4，派生前次、当前、按下、松开和连发缓冲。整个A00h对象与独立公式核对；PC、wait和派生按键位没有宿主赋值。原生采集对象的指针没有搬进旧场景。

新平台服务只在原调用方、原IAT目标和相同空输入前提成立时回放已记录的ImmGetOpenStatus(0)与lstrlenA(空字符串)返回。它们是记录回放，不是这次新执行的OS查询；原游戏函数全部运行原机器码。旧图形助手已退出，其原生句柄不复用，本次不声称新GPU或资源寿命。

验收范围为自然文本就绪、无输入确认对照、实际采集按下解除确认、实际采集松开及下一条opcode30处理函数4C61C0的自然入口。入口第一条指令保持未执行，完整外层线程/调度、世界与后继资源仍待后续连接；不能称完整R3完成。

复现需全新输出：

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_keyboard --out analysis/fresh-retained-keyboard.json.gz
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_keyboard_verification analysis/fresh-retained-keyboard.json.gz --out analysis/fresh-retained-keyboard-proof.json
```
