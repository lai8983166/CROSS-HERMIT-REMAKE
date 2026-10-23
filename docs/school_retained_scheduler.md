# 保留任务的原注册、当前事件与首次线程请求

有限change：`connect-retained-scheduler-ownership`。父雾层验收SHA256为`2b485ec36aec7e33a73f369abf67613ca8e65ccd4437fc50823da8cf5a708897`。本单元接自然422360入口，恢复原注册和首次调度的可验证拥有关系；等待体、真实原CRT工作线程和原MAIN连接仍未完成。

## 原来源与声明输入

原普通循环自然到422360时，TACT的manager(+08)、节点事件(+1C)、线程句柄(+20)和线程ID(+24)均为零。原422360会解引用manager并操作事件，不能把空字段视作已有调度寿命。

新声明的逻辑管理器位于65001000，4096字节初值A5；新调用栈是65300000起64KiB，栈顶6530F000。它们是独立输入，不称为原MAIN构造结果。原普通循环完整Unicorn上下文和原栈8192字节另存；新增根不覆盖该未返回帧，不把4539B0改装成451670虚回调，也不重跑场景构造器。

| 原根 | 输入 | 原指令 | 原写入 |
| --- | --- | ---: | ---: |
| 421540管理器构造 | 新管理器 | 66 | 34 |
| 421660初始化32桶 | 新管理器 | 426 | 121 |
| 4216C0任务注册 | TACT、bucket0、parameter0 | 1103 | 276 |
| 4217C0首次扫描前缀 | 新管理器 | 1709 | 525 |
| 合计 | 四个明确原调用根 | 3304 | 956 |

原4216C0自行写任务manager、链表、参数和标志；原421850创建节点事件。宿主没有给任务/线程/事件字段赋值，也没有改原代码或IAT。

无窗口x86平台仅创建和操作其自有真实CRITICAL_SECTION与两个auto-reset、初始未触发事件。原接口返回逻辑事件token65010000/65010010，分别投影到当前服务自己的实际句柄；旧进程句柄不送Windows。24字节锁内容是实际OS输出，void API的EAX规范化明确属于平台叶，不替代游戏/CRT函数。

## 原线程请求与真实边界

原4217C0→421850→421EA0→56E050连续执行。原`_beginthreadex`调用原`_calloc_dbg`分配116字节线程数据，当前原生堆实际raw块160字节，再运行原575390。完整116字节除了下表字段外均为零：

| 偏移 | 原值 |
| --- | --- |
| +04 | FFFFFFFF |
| +14 | 1 |
| +48 | 421F50原工作函数 |
| +4C | TACT |
| +50 | 761D68原数据地址 |

六分支完整线程数据SHA256均为`15ae2dcca1080a9f839cfd3be1fca0a2ba05beae4e03373cbbeff7283c25c866`。原calloc和上述写入均为机器码执行，非宿主构造的线程数据。

自然下一条系统调用是原56E0BE经IAT59221C的CreateThread，原返回56E0C4，六参数依次为`[0, 0, 56E110, 当前线程数据指针, 4, TACT+24h]`：挂起启动原CRT包装入口56E110，后者将进入421F50，再由原59A430虚表调用451670。保留任务的线程句柄和ID此时仍为零。

来源停在该IAT目标首指令前，没有执行CreateThread，没有伪造成功、替代451670，或创建一个只等事件的平台线程冒充原工作线程。IAT目标在冻结映像中经过保护层，不能凭目标地址把它称作系统DLL正文。

当前新平台服务的可执行映像不是原CRT/游戏映像，也没有原线程所需的TLS和场景回调寿命。直接把原入口地址交给它会调用错误代码；把旧逻辑内存指针交给另一原生进程同样无效。下一步需要在有效原执行环境中接通CRT包装入口、工作函数、回调、TLS和事件的完整关系，再连接保存的普通循环等待帧。当前独立注册和线程请求不等于完整外层调度已接通。

后继优先复用[已有原生场景路径](school_native_scene.md)：私有完整原版目录、原新局资料初始化、场景选择和MAIN事件入口已能得到真正的原MAIN/CRT场景线程。应在该路径核对保留逻辑与当前原生对象/输入和完整交互的关系，避免继续增加替代线程。既有原生关闭包含原TerminateThread，取消关闭与回调自然返回仍须分别报告。

## 清理、验证和保全

业务停点后明确补充原56F3B0(thread data, type2)释放线程块、原421D50解除注册、原4215F0析构管理器，分别538、127、526条原指令。节点事件尚无已建立的原工作线程负责关闭，因此仅补充CloseHandle已观察的自有节点事件；管理器事件与锁由原析构关闭。补充清理不计游戏前向推进。

原调试堆释放过程会先验证原数据，随后写DD释放标记，再调用真实HeapFree。线程内容应绑定首次验证时的完整原生sync读回；最终HeapFree前回执已经包含原DD标记，不能把它误当成初始化内容。

全部新增资源正常收束后，原普通循环完整上下文恢复且8192字节原栈未改；再执行父雾层、字形、角色容器及CRT锁堆清理。不会把恢复CPU说成等待已返回；新注册曾写入的任务头字段不被宿主回滚成旧值。

六分支完整父链和新增区间独立执行，核对完整CPU、所有映射/原队列、原栈、链表、CRT分配与116字节内容、实际API拥有者和精确线程停点。新进程重放原同步协议，验证真实事件初始未触发和正常关闭；未创建任何替代游戏工作线程。

专项测试默认可重复运行；只有设置`SCHOOL_RETAINED_SCHEDULER_PROOF_OUT`并提供新路径时才保存完整首例证明。正式六分支证明只复用源文件和验证器SHA均一致的已完成首例，其余逐例保存。父验收53份冻结文件及递归原资源/存档/检查点保全；总spec记录实际边界，R3/R6仍未完成，目标保持2026-11-20。本单元没有OS输入或解锁需求。

## 复现

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_scheduler --out analysis/NEW-scheduler-matrix.json --jobs 3
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_scheduler_verification analysis/NEW-scheduler-matrix.json --out analysis/NEW-scheduler-proof.json --jobs 3
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_retained_scheduler_analysis analysis/NEW-scheduler-matrix.json --out analysis/NEW-scheduler-source.json
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_retained_scheduler
```

独立验证v1因新增系统接口页仍使用旧导入清单而拒绝，v2因运行时整型分配键与JSON字符串键直接比较而拒绝。两次失败日志保留，v2验证器源码在修正前另存；后续仅修正私有导入视图及状态键格式，不改变任何分配值、原执行结果或父工具。

v3到原第五次分配时发现父验证器只覆盖四次分配和旧释放顺序。新验证器私有扩展为原raw尺寸262208/128/262208/128/160及用户释放尺寸262168/262168/116/88/88；新增三项API级预检验证精确160字节请求、116字节第三释放和原生DD回执，完整原链仍另行验证。失败v3及修正前源码保留。

最终40项新增与50项历史回归共90项通过，六分支正式独立证明及53份父验收冻结文件保全通过。三项任务完成，归档 `openspec/changes/archive/2026-10-24-connect-retained-scheduler-ownership/`；验收 `analysis/school-retained-scheduler-acceptance-v1-20261024.json`。原始字节、Git索引和HEAD逐项核对，本地提交，不push。
