# 原场景任务构造、注册与协作等待

本单元为R3前提验证，change `verify-scene-task-bootstrap`。完整场景/保留VM/外层49E540/物理输入/世界转换仍未接通，Godot不变。

## 真实来源关系

451080分配1194F0h字节，调用451170构造，将对象发布到7A4174并设置autoDelete，然后以bucket0、parameter0调用MAIN+64h的4216C0。451170沿439EF0→422290建立基类，再构造内嵌渲染、世界、数组和文字所有者，发布59A430虚表。该表的线程回调为451670、析构入口为451630；后者调用451470。

451670先设置初始状态、画加载文字，通过4516D0→422360(0)让出，才继续资源初始化、场景加载与451A60状态分派。只有state2才在451AB7调用4539B0，后者调用完整454CF0任务、453F10、46B470世界更新并循环让出。4539B0自身没有参数，不是421F50的直接虚回调；不能把它直接塞进虚表替代451670。

## 派生对象原生实验

复用冻结R1观察器和调度器调用桥，新增派生客户端，只在自有Job原版初始化/正常关闭之间写新VirtualAllocEx缓冲。数据区2MiB，原对象1194F0h字节加32字节保护尾部。场景构造器451170、4216C0注册、422560禁用、4217C0跳过、421D50解除注册、451470析构及管理器析构均为原代码实际执行；没有调用发布到全局/真实管理器的451080，也没有运行451670或4539B0。

零填充与A5填充样本均成功。GetObjectA实际核对原构造器所建HFONT的完整LOGFONTA和保护尾部，字体高度10、weight400、源字节字体名；原析构DeleteObject之后同一句柄GetObjectA实际返回0且查询缓冲未被写入。原资源句柄不被宿主伪造。

独立模型核对完整注册/禁用扫描/移除/析构后的对象字节和32字节尾部，含脏字段保留；析构清理覆盖世界内嵌所有者、十个2Ch容器、字体、文本所有者及最终基类虚表。构造器完整结果是原生采样，另核对源码规定的零字段、循环除数4、虚表和真实字体；没有宣称整个构造器已逐指令独立重放。平台不透明CRITICAL_SECTION字节取实际OS输出。代码/虚表/所用IAT前后核对不变，原函数自然返回且ESP平衡。

## 协作等待协议

这是单独的原422360(2)根调用探针，节点/管理器由原代码构造注册；节点事件由实验实际CreateEvent与DuplicateHandle创建和传入，明确是声明的自有平台输入。源422560置active1，原422360写delay2、置10000h让出标志、Reset节点事件、Set管理器事件、等待节点事件。

实际等待线程保留完整WOW64上下文/128字节栈及42240D等待返回地址祖先。两次原4217C0扫描只使delay2→1→0，线程仍为WAIT_TIMEOUT/STILL_ACTIVE。实验实际SetEvent释放共享节点事件，原函数清10000h并自然返回；之后源清flags/移除/析构。节点事件由实验补充关闭，管理器事件由原析构关闭，两者经实际DuplicateHandle返回ERROR_INVALID_HANDLE(6)。这不是原CRT场景回调或原调度器第三次唤醒路径，不能充当场景/世界推进。

等待时并发调用限于独立参数槽的4217C0延迟tick；普通入口不得重用仍在等待线程的参数/代码。所有源入口真正结束后才释放新缓冲。失败时保留实际错误并交给自有Job清理，不将其算作正常验收。

`yield-v1`为未含上下文的早期样本；`yield-v2`在读取越过线程栈边界的512字节采样时失败，实际错误和自有Job强制清理均保留，不作通过样本。之后改为128字节采样，`yield-v3`通过完整复核；未改原代码或线程寄存器来绕过该错误。

## 复核与交接

```bash
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m unittest tools.tests.test_school_scene_bootstrap
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_scene_bootstrap --fill 165 --out analysis/new-scene-object.json.gz
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_scene_bootstrap --yield-probe --out analysis/new-scene-yield.json.gz
PYTHONPATH=. PYTHONUTF8=1 .venv-audit/Scripts/python.exe -m tools.school_scene_bootstrap_verification --report analysis/new-scene-yield.json.gz --out analysis/new-scene-proof.json
```

下一步需把451670的实际线程栈、首次让出后的资源初始化及场景状态接回保留逻辑上下文，再用原49E540/4217C0/事件唤醒推动454CF0/453F10/46B470，完成实际输入与有意义的交互/世界转换。当前等待探针中的外部事件释放不能代替该步骤。
