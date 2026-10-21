# 原版键盘状态与对白确认门

当前change为 `verify-native-dialogue-input`，继续R3，尚未完成系统输入集成验收。旧原生场景研究和原存档/检查点不修改；Godot不变。

## 已确认的来源

原49E540在49E78A调用GAME+10B8h的412A30，再调用411290键盘更新和411DF0鼠标更新。键盘更新经真实DirectInput设备虚表+24h读取256字节到对象+0Ch；4113D5之后复制上次状态到+380h，新状态高位规范化到+480h。按下边沿+580h为(old XOR new) AND new，松开+780h为(old XOR new) AND old，+680h保存含连发的按下状态。

保持全部256个键状态相同且至少一键按下时，+880h首次延迟、+884h重复间隔和+888h计数/+88Ch阶段控制连发；达到阈值发出连发并将计数重设后加1。状态改变或全部松开会清空计数/阶段。9组声明GetDeviceState缓冲的独立实验执行原4113D5–4116A4完整指令区，与独立公式预测的整个A00h对象一致；包含低位忽略、阈值、松开和计数最大值。这是平台边界后的客体执行，不是现场系统输入。

原4128F0的五种模式分别读取+480h当前、+580h按下、+680h连发、+380h前次、+780h松开；键码只保留低8位，状态取80h高位，非法模式返回0。测试直接执行原函数的五种模式/全部256个键，并验证ret8栈平衡及整个对象只读。

4CCE20确认等待以4128F0(39h,0)查询空格，另经4CCB30读取GAME+198Ch/+1990h鼠标字，按钮低三位可确认。39h是DirectInput扫描码，不是Win32虚拟键码。

## 原生无输入对照

完整独立原版目录、原MAIN事件/工厂/CRT场景循环沿用上一单元。新增观察器记录完整A00h输入对象、8字节鼠标字、实际时间戳及原输入代码哈希；主机对原对象保持只读，写入仍仅为新桥和参数。全程是否有人类物理输入不作声称。

正式76-v6在原T0007.BIN的opcode51之后停PC1164/wait1，连续1秒无空格/鼠标确认，原指令查询返回0；所有采样PC窗口、原线程/管理器/世界门、真实资源及正常关闭由独立验证器核对。另一个完整77-v1在T0009.BIN的opcode51之后停PC152，同样连续1秒无确认并正常关闭，由proof-v1独立通过。两个独立原进程的无输入证据仍不等于两个输入转换。输入源代码/IAT前后不变。主机没有写PC、等待值、键盘位或原代码。

正常显示启动新增原MAIN事件稳定空闲检查，等待已有事件自然消费，不清除事件字段。初始隐藏启动是旧观察器的研究配置；为允许系统输入的新实例使用正常初始显示。标题事件尚未消费时的失败保留。

## 尚未打通的系统输入

computer-use能定位唯一私有exe窗口并读取根可访问对象；截屏报 `FrameArrived timed out: timed out waiting on channel`。空格操作在激活阶段报 `failed to activate captured window`，重新绑定/激活及新实例的根对象Raise亦失败。没有工具成功返回，也没有观测到空格按下/松开或PC跨越，不能验收系统输入任务。

`analysis/school-native-dialogue-ui-failure-v1-20261021.json`为本轮工具结果的操作记录，明确不是原生逐API轨迹。76-v8即使原生命周期正常关闭，输入目标仍未达到，不能用error=None冒充成功。

76-v1原进程在对象读取中提前退出；v2暴露复制采样器时漏导入INSTALLED，已修正；v3隐藏窗口无法交互；v4/v7标题事件竞争；v5显示窗口的工具激活失败。所有原记录保持，未纳入输入验收。早期未满足采集完成条件的尝试保留其原错误和实际清理结果。

## 复现

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_native_dialogue --scene 76 --observe-only --notice .venv-audit/fresh-ready.json --out analysis/fresh-dialogue.json.gz
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_native_dialogue_verification --report analysis/fresh-dialogue.json.gz --out analysis/fresh-dialogue-proof.json
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_native_dialogue
```

去掉observe-only仅开启等待系统输入的观察模式，不会自行发送按键。需要computer-use在唯一返回的自有窗口完成实际操作；require-input验证必须提供成功computer-use操作回执（--action），核对真实HWND/私有exe/时间关联，并看到真实按下/松开和原PC跨越。无输入证据会被该模式拒绝。

下一步先恢复这个自有Direct3D窗口的工具激活/输入能力，完成两个独立进程的确认转换，然后接回保留执行。R3和2026-11-20总目标保持原标准；本change的输入任务未完成，不能归档。

验证记录：包含相邻启动/渲染/任务/调度/场景的115项回归通过；添加77样本及成功操作回执约束后，当前24项输入套件复核通过。一次CLI新增代码的换行转义语法错误由测试加载捕获并修正，失败tests-v2日志保留；两个正式证明由最终CLI重新生成v6b/v1b。严格规格32项通过，40个上轮原生文件及全链历史/存档/检查点/8105个原私有资源的前后保全通过。


## 2026-10-22续接：窗口已激活，短按尚未进入原版

同一change继续1/3，不归档。新增输入交接阶段，在工具激活/输入期间不Suspend原GUI或场景线程，进行独立的异步只读采样；交接前后仍用原完整冻结上下文/链表/世界与VM样本验原路径。异步多次ReadProcessMemory不是原子全状态，也不是逐指令/API轨迹。当前四次交接均正常结束，完整脚本、原代码/IAT和原游戏清理由独立验证器通过。

76-v9/v10/v12的sky.press_key成功返回。v10出现一次、v12三次GetAsyncKeyState(VK_SPACE)低位记录，采集时前台均为自有窗口；原输入对象的原始/当前/前次/边沿空格位保持0，确认PC仍1164。系统收到短按不等于原DirectInput已收到按下状态。时长太短或扫描码兼容性都是待验证解释，尚未区分。窗口激活错误本轮未再出现，不能仅据这一变化断言先前失败完全由线程暂停造成。

窗口诊断确认visible/enabled，非iconic/hung，DWM未cloaked，原窗口和观察器均在Default桌面。v11的根元素鼠标点击因coordinate input geometry is unavailable失败，不计成功。后续刷新窗口时观察器已正常关闭窗口的错误单独区分。

已准备受限Win32扫描码后端和独立验证入口；只在自有Job、精确私有原exe、原MAIN窗口属性及当前前台窗口全部相符时发送扫描码39h，保持120毫秒，异常也尝试释放。它不写游戏对象、代码、IAT或寄存器。默认不启用，当前未执行真实SendInput。9项惰性API测试覆盖包结构、归属/时长限制及异常释放。拟用命令、边界和待确认规则见[后备输入审查](school_native_dialogue_held_input_review.md)。

已发出用户确认请求：computer-use技能操作规则要求仅用其JS API自动操作Windows应用，需要用户明确同意Win32后备路径例外后才可执行。这个确认不是原游戏权限、系统安全设置或数据访问问题；未收到答复不当作同意。输入任务和最终归档保持未完成。
