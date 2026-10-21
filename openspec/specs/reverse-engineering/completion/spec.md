# Cross Hermit reverse-engineering completion

## Purpose

规定 Cross Hermit 剩余逆向工作的整体范围、完成标准和月度里程碑，作为后续有限 change 的共同依据。这里描述研究应达到的结果；列出目标不表示已经实现，也不代表 Godot 重制已经完成。

## Delivery target and current baseline

- 用户于2026-10-20要求一个月内完成，目标日期为 **2026-11-20**。这是交付目标，尚非经实测确认的完工保证。
- 已验证基线：窗口客体完成17条真实创建回调及原HWND发布，停4504E1；另有两次同一自有原版进程从真实工厂前状态继续到游戏/字体缓存、设备/队列/管理器初始化及WinMain主循环，再经WM_CLOSE执行原游戏清理，三个全局清空、窗口/属性结束，整个进程树无强制终止地退出。原生状态/栈采样不等于完整客体逐指令/API重放；原版子进程的保护层状态C0000354与WinMain返回及游戏清理分开报告。
- 历史连续VM检查点仍保持 `40E2D0 / PC224 / wait1 / manager owner0`；R2已于2026-10-21完成：在新有效资源寿命内由原初始化重建渲染状态，恢复40E2A0祖先的逻辑内存和完整CPU，沿原栈完成矩形入队及VM/任务自然返回。三个保留案例另声明67次有界原VM根，推进至PC248，完成原GDI/像素转换/纹理上传、矩形与两行文字真实D3D8绘制和Present；每例1936299条原指令及完整写入独立重放一致，实际字形透明/混合像素核对通过，原生助手正常退出、资源/gamma恢复。它是明确的资源重建，非未修改检查点原地继续；旧文件/失效句柄不复用。
- R2不表示完整场景或主循环完成：静态精灵GPU纹理未恢复，本机ACP936对Big5原字节的ANSI绘字仍有乱码，Godot未改。R2完整任务曾在425F12→424F80断言处保留边界；2026-10-21来源复核纠正旧解释：FFFFFFFF来自待处理IME请求字节+630h的有符号扩展，非“输入索引−1”。该请求消化/任务边界已由下述单元接通；完整R3仍需实际输入、外层调度和场景资源后的交互/世界转换验证，不能以有界VM根代替。
- R3完整任务单元于2026-10-21通过：三个保留案例各执行67次原425DE0请求消化与完整454CF0任务，真实ImmGetOpenStatus(0)查询201次，FF→0→FF由原代码交替完成，PC224推进至两行文字后的PC248等待。每例2004237条原指令/完整写入及真实图像、正常资源寿命独立复核一致，未新增独立4CE8F0根。原49E540/4217C0事件/线程调度、物理键鼠捕获及46B470世界入口尚未接通，因此仅归档该有限change，R3整体仍未完成。
- R3调度寿命前提单元于2026-10-21通过：两轮各三个独立自有原版进程，原421540/421660构造清表、422290/4216C0构造注册、4217C0→421850→原CRT工作线程421F50及422330基类空回调、完成移除/析构均实际执行；合计14个工作线程实际退出、20次原事件关闭后失效查询、完整对象字节/原代码/虚表/IAT/ESP核对通过。原完成分支留下的线程句柄由实验明确补充关闭，六个进程均经原游戏正常清理退出。它仅验证独立私有调度对象：旧检查点MAIN+64h的11Ch字节仍全零；原49E540、场景任务4539B0、物理输入及46B470世界转换尚未与保留VM连接，R3整体仍未完成。
- R3场景bootstrap前提单元于2026-10-21通过：两轮零/A5填充的1194F0h派生对象实际执行451170构造、4216C0注册、禁用扫描、移除和451470析构，四份原字体真实创建/销毁核对通过；另两份独立422360(2)原生根调用实际阻塞，经原4217C0两次延迟tick使2→1→0后仍等待，实验释放真实事件后原函数返回。源码确认线程入口是59A430→451670，需经资源初始化/451A60状态2才调用4539B0。六份通过样本经原游戏正常清理退出；一次越界栈采样失败另存，不作验收。实验事件输入/释放不冒充原CRT场景回调或原调度器恢复，完整451670资源初始化与保留VM/49E540/物理输入/世界转换仍未连接，R3整体未完成。
- 历史change `add-fifth-week-school-planning` 已列任务1–422完成；423–428为未完成计划，迁入下表。历史任务数、脚本数、提交数及原指令数均不构成全游戏完成率。
- 完成范围包含原启动/渲染/输入/任务/脚本/世界流程、战斗行动/AI/技能/效果/死亡、场景事件、胜败/奖励、学校返回和后续主线推进。Godot实现与所有游戏组合的穷举另计；任何必需主线操作码、AI类别或流程缺口都不能据此排除。

## Milestone roadmap

| 标识（原任务） | 目标日期 | 功能结果 | 状态 |
| --- | --- | --- | --- |
| R1（423） | 2026-10-25 | 窗口创建自然返回、原HWND发布；所需游戏/缓存初始化与资源寿命闭环 | 已完成（2026-10-20）；原生完整启动/游戏清理已验，R2客体/连续VM连接另计 |
| R2（424） | 2026-10-29 | 原渲染初始化接回连续VM，矩形/文字路径继续并得到真实绘制结果 | 已完成（2026-10-21）；三个案例矩形/两行文字/Present及资源寿命闭环，完整输入/世界与场景视觉另计 |
| R3（425） | 2026-11-03 | 输入、外层调度、任务、脚本和世界更新跨越实质性开场/交互转换 | 进行中；完整任务/文字、独立原调度寿命、场景派生构造注册/等待协议已验，完整场景回调资源初始化与保留VM/外层调度/物理输入/世界转换待连接 |
| R4（426） | 2026-11-10 | 移动/寻路/行动/AI/技能/效果/伤害/死亡类别与战斗生命周期闭环 | 待完成 |
| R5（427） | 2026-11-16 | 场景事件、胜败、奖励、学校交接、后续主线与存档连续性闭环 | 待完成 |
| R6（428） | 2026-11-20 | 全主线脚本/规则类别覆盖清单及集成验收完成，必需游戏路径缺口归零 | 待完成 |

日期和状态由实际证据更新；不得自动把旧预测或已到日期当作完成。检查点落后时记录具体缺口、对最终日期的影响及调整后的关键路径；未经用户同意，不缩减上述范围或悄悄推迟目标日期。

## Requirements

### Requirement: Source-backed integrated startup and presentation
逆向成果 SHALL 解释并验证原版启动、窗口、对象初始化、渲染资源和原连续执行路径的连接，明确区分独立实验与已经接通的游戏流程。

#### Scenario: Original initialization resumes retained execution
- **WHEN** R1和R2接受验收
- **THEN** 原窗口创建及发布自然完成，所需对象具有可证明的初始化与存活来源，原渲染路径接回先前停点并产生可检查的真实输出
- **AND** 已结束助手中的句柄、缺失旧堆对象、关闭的绘制门或独立工厂成功，均不能代替集成执行证据

### Requirement: Mainline script and gameplay rule coverage
逆向成果 SHALL 为全部主线场景数据、脚本操作码和游戏规则类别建立可追溯来源的覆盖清单，包含连续输入/任务/世界调用，以及战斗和事件结算规则。关键类别 SHALL 有代表性原代码对照。

#### Scenario: Coverage distinguishes observed and derived behavior
- **WHEN** R3至R5核对脚本、角色、技能、AI或场景规则
- **THEN** 每类记录来源、输入输出、已执行样本和未覆盖分支，区分原生执行、来源推导和重制实现
- **AND** 寻路/选敌/行动时机、技能效果、伤害死亡、事件触发、胜败奖励及学校交接均纳入范围；未支持的必需类别保留为完成阻塞项

### Requirement: Reproducible evidence and persistent integrity
逆向工作 SHALL 保留可复核的来源身份、真实接口契约、相关状态及错误路径证据，保护既有存档和私有检查点。资源所有权及原生寿命 SHALL 被如实记录。

#### Scenario: Integrated milestone validation
- **WHEN** 一个功能里程碑形成稳定结果
- **THEN** 执行受影响路径和相关回归、严格规格、历史/存档/检查点保全检查，并保留可重放的证据与实际剩余边界
- **AND** 不得通过全局清零、代用游戏函数结果、伪造对象或复用失效句柄绕过依赖，也不得将进程终止写成原版正常清理

### Requirement: Bounded changes follow the master roadmap
后续执行 SHALL 依据本总规格选择有限功能change，持续推进其未完成任务；仅在独立目标、里程碑转换或实际范围变化时创建新change。归档change SHALL 作为历史记录保留，不继续追加实施任务。

#### Scenario: User requests further progress
- **WHEN** 用户要求继续推进逆向
- **THEN** 先读取本路线图和当前有效change；存在对应未完成任务时接续执行，否则为下一个待完成里程碑建立有限change
- **AND** 不为每条消息、每个接口或每次对话新建change；优先复用已验证工具，在同一有效寿命内推进兼容调用链

#### Scenario: Historical change is archived with transferred work
- **WHEN** 旧change的计划任务迁入总路线图后归档
- **THEN** 未完成任务仍保留未完成状态并能映射到R1–R6，历史原始文件和证据保持可定位，归档操作本身不增加功能完成量

### Requirement: Completion and deadline claims match evidence
R6 SHALL 仅在全部必需主线路径已闭合、覆盖清单完成并通过代表性集成验收后标记完成。交付 SHALL 明示研究覆盖、残余限制和Godot实现边界。

#### Scenario: Final completion review
- **WHEN** 目标日期到达或申请逆向完成验收
- **THEN** 审查代表性启动、脚本、战斗、事件、结果和后续推进的连续路径及关键失败分支，并核对全主线规则类别覆盖清单
- **AND** 存在必需缺口时报告尚未完成及日期影响；单场景演示、独立初始化成功或历史任务数量不足以宣告完成

## Historical references

- [已完成的场景bootstrap前提单元](../../../changes/archive/2026-10-21-verify-scene-task-bootstrap/tasks.md)、[真实构造注册/字体/协作等待与下一步](../../../../docs/school_scene_bootstrap.md)、[场景bootstrap验收](../../../../analysis/school-scene-bootstrap-acceptance-v1-20261021.json)：独立原对象与明确探针，R3整体仍未完成。

- [已完成的调度寿命前提单元](../../../changes/archive/2026-10-21-close-original-scheduler-lifetime/tasks.md)、[来源/真实线程与事件/场景交接](../../../../docs/school_scheduler_lifetime.md)、[调度寿命验收](../../../../analysis/school-scheduler-lifetime-acceptance-v1-20261021.json)：独立原对象闭环，R3整体仍未完成。

- [已完成的R3任务帧单元](../../../changes/archive/2026-10-21-connect-original-task-frame/tasks.md)、[来源校正/完整任务/下一调度边界](../../../../docs/school_task_frame.md)、[任务帧验收](../../../../analysis/school-task-frame-acceptance-v1-20261021.json)：单元3/3完成，R3总体保持进行中。
- [已完成R2归档](../../../changes/archive/2026-10-21-connect-retained-vm-rendering/tasks.md)、[原渲染/保留VM集成说明与R3交接](../../../../docs/school_retained_rendering.md)、[R2验收](../../../../analysis/school-retained-render-acceptance-v1-20261021.json)：3/3完成，后续为R3建立有限change。
- [已完成R1归档](../../../changes/archive/2026-10-20-close-original-startup/tasks.md)、[窗口创建证据](../../../../docs/school_startup_window.md)与[完整启动/寿命证据及R2交接](../../../../docs/school_startup_lifetime.md)：R1任务3/3完成，后续为R2建立有限change，不继续追加已归档任务。
- [已同步的第五周与原生审计契约](../../school-fifth-week-planning/spec.md)
- [旧change归档](../../../changes/archive/2026-10-20-add-fifth-week-school-planning/tasks.md)：422项已完成、6项未完成的历史原貌保留；后续执行以本路线图为准。
- [归档路径与内容校验映射](../../../changes/archive/2026-10-20-add-fifth-week-school-planning/archive-migration.json)：旧报告中的原路径可据此定位；原始报告和检查点不因目录迁移而改写。
- [最后一次原窗口消息验收](../../../../analysis/school-window-events-acceptance-20261020.json)：归档前真实研究边界；不是已完成完整启动或全游戏的证明。
