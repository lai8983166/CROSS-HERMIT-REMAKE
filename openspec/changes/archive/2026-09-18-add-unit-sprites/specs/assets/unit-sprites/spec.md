## Purpose

把 DATA/DxAnim/ 单位动画容器与 UNITPAL.BIN 调色板库变成重制可用的精灵资产：
解码→帧 PNG + 数据驱动的帧表（朝向/状态/锚点/调色板绑定全部 JSON，可魔改替换）。

## ADDED Requirements

### Requirement: DxAnim 容器解码
导出工具解析 DxAnim 容器：文件头 `{u32 总长; u32 块数; u32 偏移表}`，块内为帧/动画数据。
容器级结构（块数、偏移自洽、总长校验）与像素级格式分开定案；像素级无法从数据定论的
（编码/调色板绑定疑点）显式记为开口项，不用猜测值产出资产。

#### Scenario: 容器自洽校验
- **WHEN** 解析任一 DxAnim 文件
- **THEN** 末块终点 == 文件总长（不符则报错退出，不产出半成品）

#### Scenario: 调色板绑定
- **WHEN** 帧为 8bpp 索引数据
- **THEN** 每帧记录其调色板 id（UNITPAL 序号或容器内绑定字段），输出 PNG 用对应调色板上色；
  绑定关系写进帧表元数据

### Requirement: 精灵资产产出
每个被导出的动画产出：帧 PNG（按 `unit<id>/<状态或序列名>_<帧号>.png` 命名）+
`prototype/data/unit_sprites.json` 汇总表（帧路径、尺寸、锚点、朝向→帧序列映射、调色板 id）。
锚点（脚底对格心的偏移）从数据推导；推不出时填默认值并在 `_meta.open_items` 标注。

#### Scenario: 帧序列完整
- **WHEN** 导出 `01E.BIN`
- **THEN** 帧文件数量与容器内帧数一致，PNG 尺寸与帧头一致，透明通道正确（索引 0 = 透明）

#### Scenario: 资产可替换
- **WHEN** 修改 unit_sprites.json 中某帧路径或锚点后重载
- **THEN** 渲染立即按新表工作（数据驱动，不含代码常量）

### Requirement: sim 精灵渲染
战斗视图中单位以精灵帧渲染：按朝向（当前移动方向 8 向）与状态（待机/移动/攻击/死亡）
从帧表选序列循环播放；帧锚点对齐格心、脚底椭圆阴影。精灵资产缺失或帧表无对应序列时
回退现有色块渲染，功能不损。

#### Scenario: 精灵渲染
- **WHEN** 单位在移动
- **THEN** 显示对应朝向的行走帧序列（按 sim 时间推进循环），位置随格移动平滑插值

#### Scenario: 回退
- **WHEN** assets/unit/ 或 unit_sprites.json 缺失
- **THEN** 自动回退色块渲染，HUD 提示资产缺失，战斗逻辑不受影响
