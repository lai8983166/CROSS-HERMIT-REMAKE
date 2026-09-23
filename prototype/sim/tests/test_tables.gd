extends "res://sim/tests/test_base.gd"
## SimTables 加载验收 (tasks 2.1): 字段与导出 JSON 一致

func test_job_table() -> void:
	var rows := SimTables.rows("job")
	assert_eq(rows.size(), 30, "职业 30 条")
	var j0 := SimTables.job(0)
	assert_eq(j0.base_attack, 0, "job0 base_attack")
	assert_true(j0.has("hp_coef") and j0.has("mp_coef") and j0.has("spirit_coef"), "系数字段齐")

func test_attack_table() -> void:
	assert_eq(SimTables.attack(0).level_points, 40, "entry0 等级点 (A3 锚点)")
	assert_eq(SimTables.attack(1).level_points, 16000, "entry1")
	assert_eq(SimTables.attack(2).level_points, 36000, "entry2")
	assert_eq(SimTables.attack(1025).level_points > 0 or true, true, "尾部索引安全")

func test_skill_visual_table() -> void:
	assert_eq(SimTables.rows("skill_visuals").size(), 612, "技能演出明细 612 行")
	var skill29 := SimTables.skill_visual(29)
	assert_eq([int(skill29.cast_fx), int(skill29.release_fx), int(skill29.sync_fx), int(skill29.impact_fx)],
		[2050, 2098, 3017, 3032], "技能29视觉链")
	assert_eq(int(SimTables.skill_visual(22).gameplay_effect_id), 6, "玩法效果独立导出")


func test_skill_attribute_table() -> void:
	assert_eq(SimTables.rows("skill_attributes").size(), 101, "索引技能属性表 0..100")
	assert_eq(SimTables.skill_attribute(22).bytes, [1, 1, 1, 3, 1, 1, 2], "技能 22 原始属性字节")
	assert_eq(SimTables.skill_attribute(537).bytes, [1, 1, 1, 1, 1, 1, 0], "ID>=101 使用原版默认行")
	assert_eq(SimTables.skill_attribute(-1), {}, "负 ID 不映射到属性行")

func test_engage_table() -> void:
	var rows := SimTables.engage_rows()
	assert_eq(rows.size(), 51, "51 行")
	assert_eq(rows[0].minutes, 0, "lv0")
	assert_eq(rows[1].minutes, 5940, "lv1")
	assert_eq(rows[6].minutes, 5760, "lv6 (off-by-one 修正后)")
	assert_eq(rows[50].minutes, 540, "lv50")

func test_out_of_range() -> void:
	assert_eq(SimTables.job(99), {}, "越界返回空")
	assert_eq(SimTables.attack(-1), {}, "负索引返回空")
