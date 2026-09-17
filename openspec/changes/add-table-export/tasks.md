# Tasks: add-table-export

## 1. 工具骨架

- [ ] 1.1 创建 `tools/table_export.py`：CLI（`level|attack|job|all` 参数）、镜像存在性检查、
       文件偏移 = VA − 0x400000 的读取助手、`_meta`（source_va/stride/count/naming_ref/
       image_sha1_8）组装。验证：`python tools/table_export.py` 无参数时打印用法并退出码 2
- [ ] 1.2 表注册结构 `TABLES`（TableSpec: name/va/count/stride/decoder/output）。验证：注册
       level/attack/job 三项后 `--list` 列出三表（无则跳过 --list，直接导出验证）

## 2. 三张表解码器

- [ ] 2.1 level 解码器：i32[50] @0x625300，首值 149999、末值 8500000 的 magic 校验。
       验证：`python tools/table_export.py level` 后 json 首末值与文档一致
- [ ] 2.2 attack 解码器：×0x48，上界 (0x6D4E58−0x6C2DC8)//0x48，尾部全零截断 + 量级护栏
       (<10 或 >4096 报错)。字段按 battle_mechanics.md §1.1 命名（category、equip_series、
       attack_class、use_condition、job_threshold、mp_cost、cast_frames、recovery_frames、
       accuracy_base、accuracy_scale、aoe_radius、aoe_scale、targeting、target_filter、
       hit_effect、power_base/scale、power_a_base/scale、power_b_base/scale、power2_base/scale、
       growth2_base/scale、growth_tri0_base/scale、growth_tri1_base/scale、level_points），
       未定名字段 `u16_0xNN`。验证：entry0 的 level_points==40、entry1==16000、entry2==36000
- [ ] 2.3 job 解码器：×0x40 ×30 条（base_attack、group、hp_coef、mp_coef、spirit_coef、
       coef_d、coef_e、ai_move_type 等，AI 性格块字段按 §1 职业表行）。验证：30 条、
       全部 group 值 ∈ 0..11

## 3. 输出与验收

- [ ] 3.1 JSON 写出：`prototype/data/<name>_table.json`，UTF-8、ensure_ascii=False、
       根级 `{_meta, rows}`。验证：`python -c "import json;json.load(open(...))"` 三个文件全过
- [ ] 3.2 Godot 加载验收：headless 跑一次性脚本（`prototype/` 内临时 gd 或 --script）用
       `JSON.parse_string` 解析三个文件。验证：返回非 null 且 rows 条数与 _meta.count 一致
- [ ] 3.3 攻击表抽查：打印 entry0/1/2 关键字段与 battle_mechanics.md §1.1 对照（人工核对）
       后提交 git（信息按仓库惯例）
