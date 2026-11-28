# 十月第 1 周的圣者坟墓（冒险 33）

进入十月第 1 周的学校，在冒险列表选择「冒险33」，把参战班级切换成冒险，然后确认出击。未出击的班级可以保留原课程。战场可逐人移动、选定攻击目标和占领塔泉。确认战果后按本周行动分开发放战斗成长与授课成长，播放既有十月剧情，再回到第 2 周的学校。

原任务在 10/1 开放，开放期限为无期限，行动类别为可选冒险，第一回合唯一目的地为场景 33。原 MAP33.BIN 的逻辑尺寸是 128×192。战术模板表有 83 项，包括 74 个敌方战斗单位和 9 处塔泉。T0033 有 5 页开场及各结果分支的 3 页文本。[登记、地图与奖励表](../prototype/data/school_october_thirty_three.json)

原分派例程 432100 的 case 0x21 调用 4359C0。该例程先查询清场；清场时按用时不超过 36000、54000、108000 或更晚，依次选择脚本 2、5、8、11。尚有敌人且己方已全灭时，也选择 11。原例程 28 个边界用例覆盖各时限两侧、未清场、全灭及同帧冲突。[原指令验证器](../devtools/verify_map33_objective.py)

原模板第 1 项使用搜索模式 2，另外 82 项为模式 1。重制从战斗记录的视距字节裁剪目标，再查原版三条路线、行进目的地与等待时间；8 名单位带有非零巡逻路号。塔泉可按所属阵营攻击或治疗。移动和攻击仍由重制的 30 Hz 战术时钟调度。[原始搜敌与路线](../prototype/data/school_october_thirty_three_ai.json)

原指令分支验证以清场和全灭查询的返回值为输入；原版与重制整场同操作的逐帧对照仍待验证。十月学校的实际战术重放中，原编组 11 人击破 51 敌后全队倒下，第四档返校，683 次有效攻击、用时 76638。原指令核得经验增加 103254，累计 2427779，MVP 为学生 8，同时复核 33 次成长抽取、16 份履历、339 次关系调用和 420 个关系值。

胜利路线在学校将 5 名待命学生分别放入已有班级的空位，以 16 人出击。战术重放使用已装备的屏障、攻击法术、治愈、毒箭与空压斩，实现全清 74 敌，1317 次有效攻击、用时 55304，对应第三档 sub8。确认后学校累计经验 2546015（本场增加 221490），MVP 为学生 4，获得物品 149 与 71，经剧情返回十月第 2 周。独立原指令核对了 16 名参战者的成长、69 次抽取、16 份履历、474 次关系写入和 420 个关系数值。[数值及来源摘要](../analysis/m3-adventure33.json)

从项目根目录复查现有十月初学校档时，输入文件 SHA-256 为 3c1eee1843f5835493569835514268d4cb81a6dcc8dad69d3c393d592eb9d82e。可选第二参数为待新建的第 2 周重制存档。[十月父存档的跨月来源](school_year_loop.md)

    godot --headless --path prototype --script F:/project/chaomofa/devtools/replay_m3_adventure33.gd -- F:/project/chaomofa/.venv-audit/october-one-v31.json
    .venv-audit/Scripts/python.exe -m devtools.verify_map33_objective

回放的第三个可选参数指定新导出的核验输入目录，其中 settlement.json 和 submission.json 可传给下列验证器。

    .venv-audit/Scripts/python.exe -m devtools.verify_november_sortie_result OUTPUT/settlement.json OUTPUT/submission.json

在原档路径前加 --mixed 可复现首班 3 人直攻首领、其余 8 人留校修课的分支。冒险得到 73200 经验。原指令核对 8 个授课包、47 次授课抽取、共用随机序列的 57 次抽取，以及 131 次关系写入，结算后回到 10/2。

在原档前用 --victory 可复现 16 人清场路线，省略此参数则使用原有 11 人编组。

用以下命令可在全新进程从胜利档重放学校和战场指令，并检查父档指令前缀、返校日期、评分和重新导出的状态摘要。

    godot --headless --path prototype --script F:/project/chaomofa/devtools/replay_m3_adventure33.gd -- --reload F:/project/chaomofa/.venv-audit/october-one-v31.json F:/project/chaomofa/.venv-audit/m3-map33-victory-week2.json

胜利档的独立冷重放已完成。该 v32 存档有 1439 条学校指令，占 177619 字节，SHA-256 为 6c7482490b0cce734f15bfc15b6a980956bc6a594ed47a554d59050929d996bb。重新执行后得到相同的十月第 2 周、第三档评价和累计 2546015 经验，状态摘要为 b8be9058978e1acadfd1ebebfde32e3f847f3865c5979b8545693569b9cdf910。
