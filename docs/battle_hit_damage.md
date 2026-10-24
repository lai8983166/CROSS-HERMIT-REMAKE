# 原基础近战命中、受击事件与HP（2026-10-24）

本单元把已验原48AAE0效果入口接到实际HP写入。34份声明战斗记录/种子从首次原根前设置，重新执行已验绑定/攻击动画前缀，在同一实例自然停48AAE0后沿原CPU/栈继续；没有在旧报告或已清理的检查点上改字段。原工具/证据保持冻结。新实例额外声明目标与EFCT已加载缓存；原文件/GPU加载和完整世界寿命没有执行。

## 连续原执行

原467020分别绑定目标/演员，原475270请求后完整475700准备并出手；原40A100推进至首个攻击帧，原482A30→482AC0→482B50自然进入48AAE0。原栈直接续跑48AAE0→48AC90→4DEAA0/46B3E0→4824D0，再返回整个482A30，不另造独立伤害计算根。

原记录+3Ah/+3Ch/+38h分别提供unsigned power/spread/accuracy，防御记录+4Ch/+4Dh/+52h提供evasion/armor/mental。原MAP05格和MAPCOM地形实际给出系数；代表双方位置为(29,5)/(30,5)，闪避120%、护甲110%。44字节双方快照、实际命中返回、伤害与游戏RNG状态由独立模型全字节核对。原4DFA70实际检查三个空条件块，未给状态函数返回桩；附加状态与其他攻击类别仍待扩展。

## 原判定与打包规则

- 游戏随机数467E00先返回旧seed高16位&32767，再以`seed*0x48D159E1+1`按32位回绕，并递增计数。第一个值%100用于命中；spread非零时再取一次%spread；受击图像变体可能再取一次%5。所有值由原指令产生，输入只有初始种子。
- 残余命中值为`accuracy-trunc(evasion*terrain/100)-roll`。有闪避时，roll<5强制暴击路径；roll≥95或残余<0落空；残余≥150为暴击。无闪避时，原代码直接略过落空分支，仅残余≥150才暴击，其余仍为普通命中。零闪避并不强制150%伤害，roll95也不必落空；旧`school_attack_inputs.scalar_damage`纯公式镜像在这一类别存在差异，保留冻结但不作为本单元依据。
- 普通倍率100，暴击倍率max(150,残余)。伤害为`trunc((power+spreadRoll)*multiplier/100)-trunc(armor*terrain/100)`，原32位乘法回绕和有符号除法保留。普通伤害<1返回4（格挡）并存0；正伤害>3*mental返回3，>mental返回2，其余1。暴击统一返回3，负伤害改1，但恰为0保留0。0为落空；严格大于的两个mental边界独立核对。
- 目标unit+6攻击标志非零时，原4692E0使非零结果改为1，伤害数值不变；原始命中分类和最终事件分类分别保留。
- 原48AC90复制原12字节攻击包，将结果写byte6，把计算结果的低16位取负后写signed SHORT+10。它不是32位伤害直写HP：例如306692打包后得到正delta20988，HP100/max30000实际变21088；32768打包为−32768。该行为如实保留，没有替原版修正符号。

## 受击效果与HP路径

原482D60按原表选择2001等普通、2007等重击、2052等格挡效果并由原游戏RNG选变体；原46BEB0/465140/40AF40使用EFCT实际元数据创建子动画。首个标志8帧由40A520/40BDD0立即把受击包排到目标动画事件表；这与已验标志4攻击事件分开。完整原482A30回收攻击事件后，明确补充原4918D0(target,1)消费受击事件，再补充493450(target)消费实际伤害链：4919F0→491EF0→493090→原512槽伤害池→472550，原492F00回收并清链。HP写入的原指令PC、地址、大小和值另有只读观察。

普通代表实际计算39，HP100→61；34例覆盖全部五种返回、四职业101–104、落空/格挡无HP写、非致命/HP0、保命到1、当前HP低于阈值、unsigned阈值65535及容量截断。30例有实际HP store（含delta0）；落空/格挡4例没有。记录+54h非零、原和<1、delta<0、先前HP≥unsigned阈值且−delta≥阈值时保留1，之后仍按0..maxHP截断。

结果2/3通过原4753F0保存旧命令、437D90取消路径、475270请求8/9，设置受击来源和反击目标；结果1只设置反击目标，格挡也保留对应反馈。后继8/9命令尚未执行。HP0后单位使用位与alive仍保持原值，本单元未运行472770死亡入口，不能把数值归零写成死亡/移除/奖励完成。

## 原CRT与当前Win32 TLS

弹出数值实际创建原512槽popup记录并执行495630。其随机数467E70→570FE0→5753B0整个原体均执行：原rand更新当前客体74h字节上下文+14h的`seed*0x343FD+0x269EC3`，取新高16位&32767。没有旧5753B0状态返回适配器或预填随机数。

只有原IAT目标的GetLastError、TlsGetValue、SetLastError为平台叶：通过当前Python线程真实Win32调用。当前自有TLS槽存放客体上下文token（Windows不解引用），客体slot51显式映射到本次真实槽，IAT未重绑。ctypes的LastError交换机制隔离/恢复错误域，原5753B0完整保存和恢复4660；SetLastError为void，其无语义EAX规范化0。原生槽/线程回执与确定性客体执行分列，新实例不要求分配到相同原生槽号。每例原调用链2次CRT rand/6次实际平台叶，34例共204叶；实验创建/清token/TlsFree/释放后无token回读另验，未称其为原CRT启动/销毁。客体CRT/游戏函数无返回代用；不是逐Windows内核指令重放。

## 证据与限制

正式语料`analysis/battle-hit-damage-source-v1-20261024.json.gz`，独立证明`analysis/battle-hit-damage-proof-v1-20261024.json`。34例共1000650条原指令/446447次原写入。全双单位/记录、游戏/CRT种子、子动画/事件/伤害/popup池独立逐步核对，新实例全部29拥有区、57项所记录CPU、实际指令与写入轨迹复现；每实例当前真实TLS回执/正常释放分别复核。原EFCT的15662260字节完整身份固定，使用其77212字节元数据前缀及原静态映射，不称实际显示/声音设备。

效果子动画通过完整原40A100额外更新自然结束；演员活动子动画由明确补充原40AC90清理，popup记录由明确补充原494D70清理，不冒充弹出绘制/自然过期。早期缓存/方向缺口、原函数准入边界及分类不足的探针保留，正式34例不包含失败。原生TLS释放后的槽不复用为当前资源。

70项专项测试及319项相关回归通过，涵盖原分类/HP连接、关键边界、真实TLS/耗尽清理及破坏原栈/CPU/快照/HP原写入/资源/RNG/API回执拒绝。原资源、父38份和递归原资料保全另验。

完整46B760世界、阶段22恢复、死亡/移除/奖励、魔法/治疗/高级技能/附加状态、其他地图和动态占用/实际显示仍待验。原Godot、存档和历史报告未改，无OS输入或屏幕解锁要求，R3/R4/R6继续未完成，2026-11-20目标不变。

复核使用`.venv-audit/Scripts/python.exe`、`PYTHONPATH=.`、`PYTHONUTF8=1`，输出须为全新路径：

```bash
python -m tools.battle_hit_damage_emulation --out analysis/battle-hit-damage-source-fresh.json.gz
python -m tools.battle_hit_damage_verification --report analysis/battle-hit-damage-source-fresh.json.gz --out analysis/battle-hit-damage-proof-fresh.json
python -m unittest tools.tests.test_battle_hit_damage -v
python -m tools.battle_hit_damage_preservation --out analysis/battle-hit-damage-preservation-fresh.json
```
