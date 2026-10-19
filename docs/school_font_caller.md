# 原字体返回后的 manager、队列和 gamma 准备

2026-10-19，独立、明确声明空缓存初态的原版启动实验已从415F50返回点4134E3继续。原成功分支调用40D970，以这条启动链中构造的owner和实际设备绑定manager；随后40DAB0完成两次队列分配及全量原机器码清零，再生成三通道gamma表，停在416CFA设备调用指令执行前。原连续VM仍停40E2D0 / PC224 / wait1、manager owner0；本次独立实验没有修补或推进它。

365 来源：钉住原映像SHA和413450后缀、40D970/4142B0、40DAB0/40DB10/40DB90/40DBF0/40DC80、428A40/56CEC0及416C40/416CC0的完整相关字节。独立投影48KiB owner与1536字节gamma表，检查未修改的填充和其他字段。

366 绑定：原4134E3保存字体成功结果0，经原判断和413500调用，把实际owner写入manager+0；原4142B0读取owner+B210，写入manager+4。40D970自然ret4到413505，EAX0；原父栈、保存寄存器和完整owner均核对。没有从此前孤立队列实验拷贝对象，也没有手写manager绑定结果。

367 队列：原40DAB0依次调用40DB10(4096)、40DBF0(1048576)。两次428A40只在原56E810边界接受明确声明的调试CRT分配响应，参数大小、block type1、源文件地址、行号141、返回栈与初始CD字节均核对。原包装器更新分配计数；原56CEC0实际执行8192+262144次四字节清零，完整32KiB层表和1MiB命令区均为零，四侧4096字节保护区保持。原管理器容量、指针和cursor字段与独立投影相等，40DAB0自然返回0到413513。

368 gamma：原成功分支调用416C40，对256个索引各写三次16位值index<<8；原768次存储得到三个完整通道0…65280。随后原416CC0准备实际device、flags1和owner+B408参数，停在416CFA的call [vtable+48h]执行前。此时仍在原子调用栈中，既未读取该调用的目标，也未执行设备gamma调用、413450后续清理或完整返回。

每个640×480/A5、1024×768/CC案例各用一条连续原CPU轨迹和同一对实际拥有资源的助手寿命，从此前owner构造、真实设备和全部字体初始化一路运行到gamma调用前。三份小型边界证据以SHA绑定完整轨迹和各节点，均不是可复用旧句柄的恢复点。旧字体助手源码、可执行文件和拥有资源的清理顺序保持，所有COM/GDI资源在取证后平衡释放。

验证器不依赖记录中的trace来生成预期trace：它从原字节独立走成功/非空/对齐分支、实际调用返回和256次gamma循环，推导每个REP观察次数。三个节点分别核对96、270788和5470条原指令观察，以及精确调用ABI、返回、CPU、完整owner、原映像/计数、SEH0、外部接口映射、五份既有完整堆/保护区、三块像素快照和退休DIB证据。测试包含重算SHA后的对象、队列、保护区、gamma和旧前缀篡改，另作一次两案例新鲜连续重跑。

首轮实验记录完整保留：v1过早映射了仅用于新队列的审计内存，导致旧前缀的完整映射清单验证拒绝；它没有获准作为连续轨迹证据。实现将这两块映射延后到字体完整返回后，保留原前缀的映射清单。v2生成的第二案例连续六次遇到实际地址碰撞，被原有拥有边界规则拒绝；未修改助手、碰撞边界或重试上限。随后v3生成成功，旧前缀与新增三阶段均通过完整验证。v1报告、拒绝原因和v2失败日志保留，没有用后续成功覆盖它们。

369 验收包括11项本批测试与19项直接父链回归，以及30项严格规格检查。16,320个既有文件、十项存档规则和九份私有VM检查点保留；工作文件SHA与Git blob逐项核对。五个已列阶段分别本地提交、未push。369/369只表示已列任务数，不是整个游戏的逆向完成率。

证据：[来源](../analysis/school-font-caller-source-v1-20261019.json)、[连续轨迹v3](../analysis/school-font-caller-trajectory-v3-20261019.json)、[manager绑定](../analysis/school-font-caller-bind-v1-20261019.json)、[队列](../analysis/school-font-caller-queues-v1-20261019.json)、[gamma调用前](../analysis/school-font-caller-gamma-v1-20261019.json)、[首轮拒绝](../analysis/school-font-caller-v1-refusal-20261019.json)、[v2失败日志](../analysis/school-font-caller-trajectory-generation-v2-20261019.log)、[回归](../analysis/school-font-caller-regression-20261019.log)、[严格规格](../analysis/school-font-caller-strict-20261019.log)、[保留检查](../analysis/school-font-caller-preservation-20261019.json)、[验收](../analysis/school-font-caller-acceptance-20261019.json)。

下一步补齐真实拥有设备的gamma接口响应，执行原416CFA和413450成功后缀至自然返回；然后继续核对真实上游缓存、原外层调度与保留VM的衔接。Godot、原版存档、桌面gamma和保留VM未改变，也尚未实现可操作战场或GPU绘制/Present。
