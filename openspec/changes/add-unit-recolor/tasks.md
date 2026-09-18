# Tasks: add-unit-recolor

## 1. 导出管线

- [ ] 1.1 tools/unit_recolor_export.py：块7 → data/unit_recolors.json（40×256/档）
       + assets/unit/<档>/_recolors.png 预览图。验证：10 档全导出、条目数与块7 头一致、
       匹配率校验（帧像素 ∈ 块7[0] 的比例 = 100%）
- [ ] 1.2 formats.md §10 块7 行更新（[0]=基色/[9]=黑影/步长9 分组/选择字段开口）。
       验证：开口分明无猜测值

## 2. sim 集成

- [ ] 2.1 main.gd 重映射纹理路径：(anim_id, frame, palette_id) 缓存 + 精确 RGB 匹配；
       匹配失败像素保原色。验证：窗口中同档不同 palette_id 配色可辨
- [ ] 2.2 battle_setup.json：faction_palettes 默认 + 单位级 palette_id 覆盖 + 越界回退基色。
       验证：改配置即生效；palette_id=999 不报错

## 3. 回归与验收

- [ ] 3.1 测试：换色表加载/条目数/重映射匹配率/越界回退 + 全量 runner 绿。
       验证：0 failures
- [ ] 3.2 用户目检：红蓝阵营配色区分，观感与预览图一致。验证：用户确认
- [ ] 3.3 提交 + 归档
