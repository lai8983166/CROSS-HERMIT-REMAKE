# 原菜单到战斗的合法交接

本单元接续`connect-terminal-wait-and-battle-exit`的2.1。startup自然退役后的菜单仍是活动资源所有者，不能在菜单上叠加旧三根战斗构造。原战斗等待返回、结果消费和完整退出仍须分别取证，不以一次输入提交或菜单消失替代验收。

## 原交接合同

原菜单45EFB0调用45F810，以GAME+196C/1970坐标命中严格开区间矩形，读取GAME+199C的左键释放边沿。没有键盘确认分支；按住左键也不是已接受选择。菜单约3660次未选择循环后回到startup，不会自动进入battle。

新游戏项0逻辑中心(318,508)，原选择后执行4E1B60并发布event7；49F4E0推进周、加载CH001.YBC后发布event6，原ADV结束才进入event8职务室。读档项1中心(318,540)，原event13走实际文件枚举和4D75A0读取；现有ATWIKI_ALL_CHARACTERS.SAV的场次表为空，读档后先到学校，不能宣称直接取得T0004。

原学校确认必须实际形成场次和队伍，event10的4B8FF0生产者读取这些当前数据，执行原地图/单位准备再发布event16。生产者发布后还会yield一次才返回，因此它与新battle可能短暂合法并存；此原祖先重叠不同于旧菜单仍占有资源组90时叠加battle。菜单析构还会清理全部资源组，旧构造拒绝保持有效。

静态合同`devtools/terminal_menu_transition_contract.py`核对原指令、命中矩形、输入边沿和分派；12项局部原指令测试覆盖64种鼠标边沿组合等情况。合成内存中的局部执行不等于真实菜单交接。

## 自动输入边界

Computer Use可以识别并激活私有窗口，但启动和自然菜单阶段均出现`window capture timed out`，可访问树只有窗口。用户已于2026-11-07明确允许项目自动化测试覆盖技能的JS-only限制，使用受限Win32鼠标后备；原回复及当时实现身份保存在`terminal-menu-mouse-authorization-v1-20261107.json`。该授权不豁免验收，也不要求用户手工推进。用户随后解释Esc是为了离开Computer Use完成审批；不应把这个动作自动扩大为取消整个逆向任务。

后备默认禁用，显式启用后只在本工具当前Job的精确私有exe、PID/HWND、原MAIN窗口属性、解锁桌面和前台全部相符时执行。菜单必须是唯一注册任务、MAIN事件空闲、node+30为1，原45F065等待栈的selector this和45EE6A返回地址必须真实匹配。原鼠标producer、命中代码、矩形表、GetCursorPos/ScreenToClient实际IAT出口及输入HWND/坐标模式均核对后才允许移动和点击。

移动以原游戏坐标反馈为依据，未到目标不按左键；只提交一次80ms点击，失败不自动重试点击，异常也释放已按下的按钮。后台发送与前台只读采样分离，释放后额外采样100ms，保留原鼠标边沿、MAIN事件及时间。`released=true`只表示提交成功，必须另验菜单原worker退出码0、注销、原后继任务创建及相应脚本状态。

v4发现实际系统相对鼠标移动存在加速，四次反馈位置在目标两侧偏移，因未达到目标而拒绝左键；没有把“移动提交成功”误算选择。修正为虚拟桌面绝对坐标，核原窗口/客户端转换、当前桌面范围及WindowFromPoint归属。点击前无条件再次检查几何和遮挡，初始已经位于目标也不能跳过。相对移动受系统速度/阈值影响以及绝对坐标映射规则见[Microsoft MOUSEINPUT文档](https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-mouseinput)。

可选`--story-confirmations 192`复用既有扫描码39后备授权，只有唯一原ADV任务、真实CRT祖先及opcode51确认等待稳定1秒才发送。它不会驱动未知选择、学校操作或战斗字段；重复而未证明已推进的确认拒绝，动作和原键盘/VM变化另存。预算用尽后在下一个未消费的稳定确认等待封存，不能将预算停止写成章节结束。

## 运行和证据

```bash
.venv-audit/Scripts/python.exe -B -X utf8 -m devtools.terminal_menu_handoff \
  --out analysis/terminal-menu-handoff-NEW.json.gz --seconds 900 \
  --menu-selection 0 --allow-owned-mouse --story-confirmations 192
```

参数只选择已有原菜单项，不写游戏输入位、结果、代码、IAT、寄存器或完成标志。资产在当前寿命重新哈希，只保存固定父清单引用；不复制游戏资源。旧采集实现变更前单独压缩封存，用于认证历史来源身份。

v1观察到自然菜单的真实选择等待，但未输入；v2在Computer Use停止信号后撤销待执行输入并结束私有测试，鼠标controller attempted=false，输入列表为空。取消来源及子进程终止必须作为取消记录，不能算正常游戏退出。四份已关闭控制/进度文件由明确退役清单清理，私有可写文件原字节已恢复。

v3暴露了前置观察器选择错误：原startup在115.109秒以0退出，菜单独存，但没有采到动画16204终点；动画专项观察器仍等待该终点，后来菜单自动回到新的startup，触发“同一startup寿命”拒绝。该例没有鼠标controller动作。不能将其写成游戏交接失败，也不能补造计数。

新增`terminal_menu_startup.py`作为流程前置，独立检查当前startup原线程、TLS/Event、实际signaled/退出码0、节点退役及菜单独存稳定1秒。动画终点和原鼠标按下样本单独记录，`retirement_trigger_proved`仍false；稀疏样本不证明具体触发原因或全部析构指令。原动画专项观察器及旧proof保持不变。流程继续的依据是同一当前所有者的退役和后继，完整线程/资源因果要求仍留在正式验收中。

本change保持2/8，完整战斗退出和资源寿命验收仍未完成。

## v5真实输入及独立复核

v5以一次受限绝对鼠标点击进入原ADV任务，并实际提交96次剧情确认。菜单原worker在284.672秒以0退出；同一分配地址被ADV重用，但线程ID由36684变为42132，按`(node, thread_id)`区分寿命，不能只按指针认作同一个任务。观察在475秒附近按96次预算有界停止，原生probe及清理均无错误，私有Job清空，四份可写文件恢复原字节。

独立验证重放冻结的原4128F0键盘查询，逐条核对实际按下、释放、PC推进及输入时间；96次均通过。343份保留快照的注册图、原线程祖先、PTD/TLS与事件所有者通过检查。源码执行过菜单就绪计时，但v5只保留到280.922秒的ready样本和281.187秒的决策，不能独立证明完整1秒；短命event7生产者也未采到。proof因此保持`partial_menu_observation`、`accepted=false`、完整menu handoff未证明，不将ADV后继观察冒充完整过渡调用轨迹。

复查命令：

```bash
.venv-audit/Scripts/python.exe -B -X utf8 -m devtools.terminal_menu_handoff_verification \
  --report analysis/terminal-menu-handoff-v5-20261107.json.gz \
  --sha256 b169a2aff7064e3e6eddf8aefd7c7470031ed826e441bfa18fdf6851bf5d08df \
  --allow-v5-archive --out analysis/terminal-menu-handoff-proof-v5-RECHECK.json
```

v5执行的collector/story原字节有固定SHA的zip封存；新实现身份不会代替旧来源身份。下一版本补存菜单首次ready与输入决策的完整快照。96次不足并非无变化空跑：末尾PC3398、代码到block1跨度5560，仅与现有CHAPTER003.YBC长度匹配，该文件静态包含153个opcode51；没有采程序原字节，脚本名只记候选。下一轮上限192、菜单阶段600秒、总观察900秒，原始JSON上限64MiB、压缩来源上限6MiB。相关候选/预算证据见`analysis/terminal-menu-story-budget-v1-20261107.json`。

## 后继职务室的原输入合同

`terminal_workroom_contract.py`仅准备原字节合同，不发送原生输入。原职务室vtable5A0904、state1的选择器49FD50在49FF57等待，返回父调用4A15D0；不能在淡入/淡出等待点误点。退出按钮矩形为(847,726,141,30)，逻辑中心(917,741)。原4D5EC0→4D5B70使用有符号16位差值且四边包含，读取GAME+1990按下边沿，和标题菜单的释放边沿/严格开区间不同。六项合成x86测试实际执行原命中函数、栈检查及RET14h，覆盖边界和仅按住/释放不选中。

原退出把选择器返回值4交回node+30，随后原回调先yield；第一次经7A4E62标志选择CH002.ybc、后继9并发布event6，后续则直接event9学校。此静态合同不证明当前职务室已就绪、已输入或已自然退役，也不能替代学校真实编队/场次准备及event10→event16生产者。

## v6开场剧情结束到职务室

v6实际执行178次确认，按当前VM的代码到block1跨度分布为5560/153次、920/16次、412/9次；分别与CHAPTER003、004、005的静态结构相符。003末尾SCRIPTEXEC引用004，004再引用005，因此153只是一段子脚本的数量。静态串联及资产SHA见`terminal-menu-story-chain-v1-20261107.json`；未采活程序原字节，候选脚本名称仍不作为完整身份认证。

实际菜单worker3384在284.437秒退出0；ADV worker43276在646.953秒退出0；647.093秒出现职务室节点82133408、原vtable5A0904、worker41656。独存超过10秒后在657.359秒结束观察，含清理共658.766秒，probe和lifecycle均无错误。最后原栈包含49FF57→4A15D0→421F8A→56E183，节点state1；已观察到真实职务室选择等待，没有发送职务室按钮输入。

本轮的连续功能进展是启动→菜单→开场剧情→职务室。下一步是为已核原字节的职务室退出补齐受限输入、原线程退役和CH002/学校后继验证，再准备真实学校编队/场次及battle生产者。当前没有执行战斗等待返回或结果消费，旧资源失效所在的非法battle构造仍拒绝；不能把本轮前置路径未报错写成完整资源寿命已验收。2/8正式任务状态不变。

独立v6 proof核到638份快照、637份任务TLS、178次输入中的2219次原键查询，菜单ready两份原样本跨度1.000秒。短命NEW_GAME节点仍未采，职务室原函数体未被本轮live代码范围完整覆盖（实际vtable、等待栈和PTD/TLS已核），故完整menu调用因果、职务室回调活字节认证、PTD释放、资源寿命和WinMain正常返回继续标false。采样中opcode先更新、PC后更新的合法瞬态按原4CE9DD/4CE9FB→4CFEF2/4CFF0C顺序校验，必须有真实按下及随后对应长度的PC推进，不能任意放过不一致状态。

```bash
.venv-audit/Scripts/python.exe -B -X utf8 -m devtools.terminal_menu_handoff_verification \
  --report analysis/terminal-menu-handoff-v6-20261107.json.gz \
  --sha256 af9e1d76f665ab06e913288b3e487f25d4777cd27acd98e6828bb1d991de7533 \
  --out analysis/terminal-menu-handoff-proof-v6-RECHECK.json
```

收尾验证：新增83项唯一回归均在普通及`-O`模式通过；已有相关149项回归通过，严格规格32/32。832份冻结小文件共58,598,492B重新SHA核对、13份大历史来源只核大小（不声称新哈希），本轮私有四份可写文件在v6清理后独立重哈希一致。清理10份已关闭的进度/停止控制文件共827B，不删除历史来源、资产或存档。全部新增本地证据及执行实现归档的大小、实际磁盘分配和SHA见`terminal-menu-evidence-inventory-v1-20261107.json`；所有原始采样仅存压缩来源，无持久化未压缩全量JSON。
