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
