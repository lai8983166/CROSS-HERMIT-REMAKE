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
