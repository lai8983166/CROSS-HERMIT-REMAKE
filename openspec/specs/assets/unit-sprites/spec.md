## Purpose

把 DATA/DXANIM 单位动画容器（`{A..E}{0,1}A.BIN` 十档，每档一个角色全动作集）变成重制
可用的精灵资产：解码 → 帧 PNG + 数据驱动的帧表（序列/锚点/时长/朝向翻转全部 JSON，
可魔改替换）。格式定案记录于 docs/formats.md §10；##E 系特效档与 COMMON.BIN 头像库的
排除论证见 change 归档 design.md。

## Requirements

### Requirement: DxAnim 容器解码
导出工具解析 DxAnim 容器：`{u32 总长; u32 块数; u32 offs[]}`（offs[0]==8+4n 自洽、
相邻相等=空块、头部总长==文件长度，不符报错退出不产出半成品）。块0=动画序列表
（10B 记录：b≤-2→帧索引、-1→空白帧、b≥0→控制/终止记录）、块5=帧画布矩形
（帧数×8B 直排无头）、块6=帧容器（每帧标准 8bpp BMP 内嵌 1024B 调色板，索引 0 透明）。
无法从数据定论的（块1 合成表、块4 运动字节码、-b≥帧数的跨档外部引用）显式记开口项，
不用猜测值产出资产。

#### Scenario: 容器自洽校验
- **WHEN** 解析任一单位档 DxAnim 文件
- **THEN** 校验失败即报错退出，不产出半成品

#### Scenario: 帧解码
- **WHEN** 导出一档
- **THEN** 每帧 PNG 尺寸与帧头一致、索引 0 透明、用帧内嵌调色板直出
  （块7 换色调色板的选择字段未定位 → 记开口）

### Requirement: 精灵资产产出
每个被导出的档产出 `assets/unit/<档>/frame_*.png` + `_preview.png`（抽样条带，目检/
语义标注用）+ `prototype/data/unit_sprites.json` 汇总表（帧路径、尺寸、画布矩形、
锚点=画布底中在帧内的像素偏移、动画序列、anim_map 默认序列、_meta 时长单位与开口项）。
默认序列（MOVE=帧引用最多的连续+等时长循环、IDLE=首条单帧动画）为启发式，只含界内
帧引用，JSON 手改即生效。

#### Scenario: 帧序列完整
- **WHEN** 导出一档
- **THEN** 帧文件数与容器帧数一致，默认 MOVE/IDLE 序列的帧引用全部在界内

#### Scenario: 资产可替换
- **WHEN** 修改 unit_sprites.json 的 anim_map/锚点/dur_unit_seconds 后重载
- **THEN** 渲染立即按新表工作（数据驱动，视图不含代码常量）

### Requirement: sim 精灵渲染
战斗视图中配了 anim_id 的单位以精灵渲染：状态（待机/移动/攻击/死亡）→ anim_map 选
序列循环（相位按 sim 逻辑帧推进，单位间错相），锚点对格心、格间平滑插值（跨
move_interval 逻辑帧）、脚底椭圆阴影、朝向右行水平翻转（anim_map 数据标志）。
帧表缺失/未配 anim_id/资产缺失 → 色块回退，功能不损，HUD 提示。

#### Scenario: 精灵渲染
- **WHEN** 单位在移动
- **THEN** 显示行走帧序列循环，位置随格平滑插值

#### Scenario: 回退
- **WHEN** assets/unit/ 或 unit_sprites.json 缺失，或 anim_id 无效
- **THEN** 自动回退色块渲染，战斗逻辑不受影响
