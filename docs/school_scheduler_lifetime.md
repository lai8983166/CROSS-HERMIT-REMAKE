# 原调度管理器和线程寿命

当前change：`close-original-scheduler-lifetime`，R3总体仍在进行中。本单元验证真实原版运行时中的独立调度对象，不宣称保留场景/VM/世界已交由原调度器驱动。

## 来源和对象前提

SHA核验的initial/rectangle检查点中，7A4A00指向1080000，MAIN+64h的32组链表和同步字段均为0。4217C0扫描这些链表，为每个节点执行421850；空表不会调度已有战斗任务。原4216C0才会清节点flags、写manager/parameter、注册到指定桶，不能手写链表并称注册已完成。

421850在首次执行时创建节点事件，421EA0调用原CRT56E050(_beginthreadex)，创建入口421F50的挂起线程；随后原代码设置事件、ResumeThread并等待管理器事件。421F50通过原节点虚表调用任务，返回后由原代码清flags1、置flags4、Reset节点事件、Set管理器事件，执行56E1E0(_endthreadex)。完成分支实际GetExitCodeThread，关闭节点事件并调用421D50移除链。原基类422290构造器发布594A54虚表，回调422330本身为空；本单元用它闭合同步/完成路径，绝不把空回调标成战斗推进。

## 调用和所有权

复用冻结R1启动/正常关闭观察器的私有函数globals副本，只在原WinMain初始化完成且Job/HWND/属性归属再次核验后、原WM_CLOSE之前进行实验。新进程由本实验创建和独占，发现既有原版窗口时拒绝运行，不发送消息给用户窗口。

桥仅写VirtualAllocEx新分配的私有缓冲，代码从RW写入后转RX并刷新缓存；白名单原入口、参数数目、私有manager/node地址、桶0–31和禁用flag2均在调用前核对。通用x86桥保存寄存器，逆序压入0–3个参数、设置ECX并直接调用原函数，记录实际EAX和调用前后ESP，远程入口线程必须真实结束才复用缓冲。禁止改原游戏代码/IAT和已有对象/寄存器；前后逐字节核对原函数及导入槽。

原对象的线程句柄+20h在原完成分支没有关闭。实验复制该实际句柄来确认线程已结束和实际退出码0，再补充CloseHandle，明确记为实验所有者清理。禁止关闭未观察的外部句柄，不能把补充关闭称作原析构已完成。

## 复核入口

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_scheduler_lifetime
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_scheduler_lifetime --out analysis/new-scheduler-evidence.json
```

纯调用约束测试拒绝外部进程、非白名单入口、错误ABI/桶、非私有写入和未观察的句柄；Unicorn独立执行原构造器与三参数注册验证桥的完整压栈、callee-saved寄存器、ESP平衡及完整节点字节。真实Windows线程/事件来源由原生实验单独验证，不能用模拟器ABI测试代替。

## 原生结果与独立复核

`analysis/school-scheduler-lifetime-contract-v1-20261021.json`固定了来源代码和旧检查点空调度图。`native-v1`是早期原生样本，尚未加入实际事件失效查询和虚表前后采样，不作为最终验收；`native-v2`及其`proof-v2`覆盖全部最终观察项。

| 填充值 | 注册桶 | 首次禁用 | 实际原CRT工作线程 | 事件关闭后失效观察 |
| --- | --- | --- | --- | --- |
| 00 | 0 | 无 | 1 | 2 |
| A5 | 0、0、31 | 节点1 | 3 | 4 |
| CC | 31、5、5 | 节点0 | 3 | 4 |

三个独立原版进程均正常执行初始化、WM_CLOSE、原游戏析构和窗口/全局清理，无强制终止。线程实际等待为signaled、实际退出码0。节点事件在调度结束后、管理器事件在析构后经DuplicateHandle返回ERROR_INVALID_HANDLE(6)；该只读查询不伪造关闭结果。原代码和594A54虚表、实际IAT前后保持相同，未将保护层转发地址误认成系统DLL函数地址。

独立验证器不导入执行器的对象变换逻辑：按来源注册/桶扫描/禁用/移除规则重建每阶段的512字节管理器和每个128字节节点，连未写的脏字段、保护尾部、被移除节点仍保留的next指针也完整比较；外部API生成的句柄/线程ID及不透明24字节CRITICAL_SECTION输出明确取实际观察值，分别与实际线程/失效查询对应，不伪造其来源。它不是逐条原生指令/API追踪，也不能据快照证明所有可能的线程交错顺序。

20项测试包含真实x86桥ABI测试和错误证据变异：脏尾部改写、清除原本保留的next、禁用节点改变、线程未退出/句柄错配、事件仍有效、漏关线程、ESP不平、代码/IAT变化、未记录写入/未释放缓冲、额外调用和强制退出均被拒绝。

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_scheduler_lifetime_verification --report analysis/school-scheduler-lifetime-native-v2-20261021.json --out analysis/new-scheduler-proof.json
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_scheduler_lifetime tools.tests.test_school_scheduler_verification
```
