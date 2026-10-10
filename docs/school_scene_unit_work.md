# 场景单位工作区与动画请求前缀

本轮从前轮已验证的场景5首条战术记录继续，执行原版 `4680B0` 的工作区、状态、模板覆盖、职业资源选择和缓存控制器前缀，停在 `464EB0 → 4500B0` 动画文件请求，尚未装载该动画档案或完成构造函数。学校实际链路和独立模板测试分别记录，不把后者当作完整场景循环。

## 实际学校续接

原版 `453540` 的首条记录索引249、角色5、职业4、类别7。在同一学校CPU上继续 `4680B0`，天然返回地址仍为 `453630`，本轮不返回到这里：

- 清零1312字节工作区，建立记录指针、索引、方向字段和记录哨兵。
- `474FB0` 对类别≥4使用另一份状态模板；`4750B0` 从场景模板进入 `4DA710`，复制64字节并重置规定字段，将模板偏移`10`的字复制到记录`A8`。
- 活跃NPC的初始状态为2，前轮活跃学生为25；未激活模板的状态为11。类别与最终部署归属分开，不把全部模板称为已出场敌人。
- `467020` 读取职业4的资源组4与方式2，原版角色颜色表选出编号5。
- 原版查找512项缓存，使用首个空槽，分配并构造84字节控制器，绑定原始动作/位置表并增加资源计数。
- 停在原版请求 `data\DxAnim\a1a.bin`，参数为文件指针、5、1、0；还没有进入文件加载函数体。

允许写入的范围只有选中工作区、176字节记录、一个缓存槽、计数器、分配后的84字节控制器、栈与SEH。每个前缀前后比较其余所有已映射字节，已有学生工作区、资源、地图、效果、持久人物和日历均受保护。文件、GPU、场景部署和VM不允许进入；CRT清零、堆分配和调试输出只接受精确调用方与参数。

## 声明驱动与独立来源

35个场景模板先由原版`4DA450`生成数值记录，再分别执行原版工作前缀。每次明确声明空缓存、计数110、渲染器输入、零控制器分配、分类选择0及零关系矩阵。各次索引249至215，使用自然文件请求作为停止点，不运行构造函数尾部；这不是学校完整35次场景循环。

独立规则读取原EXE的存储指令、分支、状态模板、场景覆盖规则、职业/颜色/动作/位置表。逐字节预测完整1312字节工作区、176字节记录、4096字节缓存及84字节控制器，并核对资源请求参数与计数。特殊角色的工作模式通过原版角色分派表和关系跳转表计算，不能假定所有单位都沿学生分支。

10个职业选用了9个不同动画档案。职业316与317共用`04e.bin`，颜色编号不同。规则记录原始文件长度、SHA-256、九段边界、图像/颜色条数和遮罩身份；这些是只读文件清点，不能算作原版CPU已经加载纹理。

另有六次声明输入变更测试：NPC模板64字节及覆盖字变化、记录类别改为学生分支、特殊角色关系值1/2/3、分类选择等于自身类别。原版完整前缀与独立计算分别比较，尤其检查复制后的字段重置、状态2/25与模式6/9/2/3。这些测试不来自真实学校操作，也不改写原版存档。

## 文件与使用

- 原版执行：[school_scene_unit_work_emulation.py](../tools/school_scene_unit_work_emulation.py)
- 独立来源与纯计算：[school_scene_unit_work_catalog.py](../tools/school_scene_unit_work_catalog.py)
- 声明输入变更：[school_scene_unit_work_counter.py](../tools/school_scene_unit_work_counter.py)
- 固定证据：`analysis/school-scene-unit-work-v1-20261010.json`及`school-scene-unit-work-counter-v1-20261010.json`。
- 分离导出：`prototype/data/school_scene_unit_work_rules.json`与`school_scene_unit_work_evidence.json`；运行时与存档不消费它们。

```bash
PYTHONPATH=. .venv-audit/Scripts/python.exe -m tools.school_scene_unit_work_emulation --out analysis/<new-immutable-path>.json
PYTHONPATH=. .venv-audit/Scripts/python.exe -m tools.school_scene_unit_work_counter --out analysis/<new-counter-path>.json
PYTHONPATH=. .venv-audit/Scripts/python.exe -m tools.school_scene_unit_work_catalog --rules-out prototype/data/school_scene_unit_work_rules.json --fixture-out prototype/data/school_scene_unit_work_evidence.json
```

需要继续装载并绑定场景单位动画，完成构造函数尾部与实际35次循环，然后执行`468910`部署、`t0005` VM及波次事件，最后接入当前学校阵容的图形战斗。本轮没有改变Godot画面或开放学校战斗，也未清除必修门槛。
