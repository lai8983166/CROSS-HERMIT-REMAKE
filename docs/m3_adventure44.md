# 冒险 44 原版对照

目标是一月第 2 周从学校出击，执行存档记录的战术指令，经过结算与剧情返回一月第 3 周学校。重制侧通过普通学校指令接口与独立战斗进程重放。原版侧使用已校验的程序镜像执行出击、任务终局判定、战果、成长和换周例程。逐人结果与输入摘要见[机器对照报告](../analysis/m3-adventure44.json)。

| 阶段 | 数据与比较 |
| --- | --- |
| 学校编班与出击 | 从相同 v40 指令前缀恢复。第 1578 条指令把学生 4 移入第 2 班第 2 格，第 1579 条出击。将此时的学校记录交给原版 4A7D30、4A6A10，比较出击资格、五班评价、关卡、场次数、师生及成员顺序。 |
| 战前与战中 | 在独立 Godot 进程从学校交接构造战场，重放第 1580 条指令内的 482 个战术操作。每次终局判定前采集原例程使用的角色编号、所属方、状态、工作槽、损失和超时条件。只合并连续相同的判定输入，同一段内非零剩余时间的变化不影响此例程。 |
| 终局 | 原版场景分派 432100 的 44 号分支调用 4360B0。核对每段的脚本子号和战果选择值。导出的角色状态来自重制战场，原版单独计算这些状态是否触发终局。 |
| 战果与成长 | 将重放产生的战果输入送入原 4BD210、4BCA40、4BBD40，核对积分、物品和角色成长包。原 4C00C0、4C1350 消费成长包，核对属性、成长池、技能状态、等级、MVP、履历、职业和关系值。时钟与成长随机种子沿用该战斗记录的 4660。 |
| 返校 | 连续执行至第 1585 条学校指令。核对结算学生记录在原 4D3510 换周入口的字段，再将原换周产生的学生字段、在籍表和物品与实际返校数据比较。原换周与返校剧情之间的旗标分开记录。报告按学生列出属性增量、等级前后值和返校成长摘要。 |

第 6624 tick 首次触发子脚本 8、战果选择值 3。原例程共执行 71 次，覆盖全部 6624 个逻辑 tick 的判定输入。战果评级为 3，积分增加 854131，返校时累计 4988007。MVP 为学生 2，等级由 39 升至 41。19 名学生中有 17 人升级，学生 15 从 27 升至 32。

原换周完成与学校可操作之间还有 Chapter229。第 1584 条指令进入入校剧情，第 1585 条才回到可操作的学校。原章文件偏移 550 的 151 指令把音乐参数设为 11、1；验证器据此核对返校旗标，同时比较学校实际使用的每名角色记录与战后成长记录。

### 原版战场仍缺的来源

项目里可检查的原版 v7 存档与重制 v40 的指令格式不同。安装目录和研究目录的两个原档具有不同的 SHA-256，各自校验和正确，日期都是四月第 1 周，在籍学生均为 35 人。本例要求一月第 2 周的 19 人队伍。原版存档函数 4D7720 写出 198356 字节，包含完整角色和运行记录。仅替换日期或编班无法建立同档身份。[存档函数](../analysis/decomp_all/4d7720.c) · [原始存档及载入观察](../analysis/downloaded_saves/atwiki-all-characters.source.json)

全程验收还需要在隔离客体取得原版同一起点，验证队伍、职业装备、属性与成长池、关系、物品、剧情和任务进度。然后按同一顺序投放战术操作，独立记录原版目标、伤亡、耗时、战果和返校成长。现有 482 条记录使用重制的单位标识与逻辑 tick；其中没有原版接收操作的回执，也没有原版独立生成的战斗状态。本例的行军、攻击、命中、AI 时序及随机种子来源仍待这一对照。

### 复查

在项目根目录运行，先建立 F 盘的空观察目录。以下 Git Bash 示例使用已安装的 Godot 控制台及项目的 Unicorn Python 环境。所用两个父档来自已封存的 M2 来源，目录变量为原生程序可识别的绝对路径。

~~~sh
root=F:/project/chaomofa
parent="$root/.venv-audit/school-year-completion/corrected"
obs="$root/.venv-audit/m3-44-recheck"
mkdir -p "$obs"
export APPDATA="$obs" TMP="$obs" TEMP="$obs"
godot --headless --path "$root/prototype" --log-file "$obs/school.log" --script "$root/devtools/replay_m3_adventure44.gd" -- "$parent/formal/chapter310-v40.json" "$parent/formal/march-ending-v40.json" "$obs/school.json"
godot --headless --path "$root/prototype" --log-file "$obs/objective.log" --script "$root/devtools/replay_m3_adventure44_objective.gd" -- "$parent/formal/handoff-44.json" "$parent/trace-44.json" "$obs/objective.json"
.venv-audit/Scripts/python.exe -m devtools.verify_m3_adventure44 "$obs"
~~~

两个 Godot 进程都成功退出后再运行 Python。完整学校观察与角色工作槽是可重建的中间文件，Git 只保留脚本、小报告和来源摘要。全图范围见[地图覆盖表](m3_battle_map_coverage.md)。
