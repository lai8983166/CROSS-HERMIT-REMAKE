extends "res://sim/tests/test_base.gd"

const Preparation = preload("res://sim/tactics_score_preparation.gd")


func _fixture() -> Dictionary:
	return JSON.parse_string(FileAccess.get_file_as_string(
		"res://data/tactics_score_preparation_evidence.json"))


func test_packages_and_summary_match_native_execution() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		var actual := Preparation.calculate(example["inputs"], fixture["rules"])
		assert_true(actual["supported"], example["name"])
		for key in ["task_grade", "grade_index", "time_display", "unit_display", "total_delta", "total_after"]:
			assert_eq(int(actual[key]), int(example["expected"][key]), example["name"] + ":" + key)
		for ordinal in range(3):
			var expected: Dictionary = example["expected"]["characters"][ordinal]
			var character: Dictionary = actual["characters"][ordinal]
			assert_eq(character["character_id"], int(expected["character_id"]), "原始 ID")
			assert_eq(character["staged_total"], int(expected["staged_total"]), "原版点包合计")
			for attribute in range(8):
				assert_eq(character["staged_package"][attribute], int(expected["staged_package"][attribute]),
					"逐属性整数计算和截断")
		assert_false(actual["authorizes_persistent_write"], "准备计算不授权持久写入")


func test_missing_duplicate_and_unknown_inputs_stay_unresolved() -> void:
	var fixture := _fixture()
	var inputs: Dictionary = fixture["cases"][0]["inputs"].duplicate(true)
	inputs["characters"][0].erase("character_id")
	assert_false(Preparation.calculate(inputs, fixture["rules"])["supported"], "缺 ID 不能按数组位置补写")
	inputs = fixture["cases"][0]["inputs"].duplicate(true)
	inputs["characters"][1]["character_id"] = 3
	assert_false(Preparation.calculate(inputs, fixture["rules"])["supported"], "重复 ID 不能覆盖点包")
	inputs = fixture["cases"][0]["inputs"].duplicate(true)
	inputs["mode"] = 1
	assert_false(Preparation.calculate(inputs, fixture["rules"])["supported"], "其它模式未实现")
	inputs["mode"] = 0
	inputs["result_selector"] = 6
	assert_false(Preparation.calculate(inputs, fixture["rules"])["supported"], "未知结果不能索引原始表")
	inputs["result_selector"] = 1.5
	assert_false(Preparation.calculate(inputs, fixture["rules"])["supported"], "不能截断结果编号")
	inputs = fixture["cases"][0]["inputs"].duplicate(true)
	inputs["characters"][0]["growth_pools"] = [100]
	assert_false(Preparation.calculate(inputs, fixture["rules"])["supported"], "缺属性记录保持未解析")


func test_capped_package_retains_other_units_and_compensation() -> void:
	var fixture := _fixture()
	var normal := Preparation.calculate(fixture["cases"][0]["inputs"], fixture["rules"])
	var capped := Preparation.calculate(fixture["cases"][2]["inputs"], fixture["rules"])
	assert_eq(capped["characters"][0]["staged_package"], [0, 0, 0, 0, 0, 0, 0, 0], "上限点包为零")
	assert_eq(capped["characters"].slice(1), normal["characters"].slice(1), "未封顶角色保留各自输出")
	assert_eq(capped["total_after"], 98277, "保留原版截断补偿顺序")


func test_inputs_and_growth_pools_are_immutable_and_repeatable() -> void:
	var fixture := _fixture()
	var inputs: Dictionary = fixture["cases"][0]["inputs"].duplicate(true)
	var rules: Dictionary = fixture["rules"].duplicate(true)
	var saved_inputs := inputs.duplicate(true)
	var saved_rules := rules.duplicate(true)
	var first := Preparation.calculate(inputs, rules)
	assert_eq(inputs, saved_inputs, "不修改人物池、条件和初始合计")
	assert_eq(rules, saved_rules, "不修改来源规则")
	first["characters"][0]["staged_package"][0] = 999
	var second := Preparation.calculate(inputs, rules)
	assert_eq(second["characters"][0]["staged_package"][0], 2818, "输出独立，不重复累加")
	assert_eq(inputs, saved_inputs, "不共享点包或成长池")


func test_incomplete_source_rules_do_not_index_missing_data() -> void:
	var fixture := _fixture()
	var inputs: Dictionary = fixture["cases"][0]["inputs"]
	var rules: Dictionary = fixture["rules"].duplicate(true)
	rules["base_points"] = []
	assert_false(Preparation.calculate(inputs, rules)["supported"], "缺结果等级表")
	rules = fixture["rules"].duplicate(true)
	rules["rates"][5] = [100]
	assert_false(Preparation.calculate(inputs, rules)["supported"], "缺职业权重项")
	rules = fixture["rules"].duplicate(true)
	rules["attribute_thresholds"][0] = -1
	assert_false(Preparation.calculate(inputs, rules)["supported"], "无效阈值")
	rules = fixture["rules"].duplicate(true)
	rules["task_id"] = 37
	assert_false(Preparation.calculate(inputs, rules)["supported"], "规则不是任务 5")
