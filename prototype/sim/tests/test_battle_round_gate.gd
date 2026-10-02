extends "res://sim/tests/test_base.gd"

const Gate = preload("res://sim/battle_round_gate.gd")


func _fixture() -> Dictionary:
	return JSON.parse_string(FileAccess.get_file_as_string(
		"res://data/battle_round_execution_evidence.json"))


func _assert_snapshot(actual: Dictionary, expected: Dictionary) -> void:
	# JSON numbers load as floats; compare integer fields and slots individually.
	for key in ["current", "total", "temp_count", "combat_count", "scene_id"]:
		assert_eq(int(actual[key]), int(expected[key]), "原版字段 " + key)
	assert_eq(actual["temp_roster"].size(), expected["temp_roster"].size(), "临时表长度")
	for ordinal in range(expected["temp_roster"].size()):
		assert_eq(int(actual["temp_roster"][ordinal]), int(expected["temp_roster"][ordinal]),
			"原版名单槽 %d" % ordinal)


func test_native_round_counter_and_roster_projection() -> void:
	assert_eq(_fixture()["evidence_kind"], "native_round_gate_with_synthetic_round_tables",
		"声明场次输入是合成表")
	for example in _fixture()["cases"]:
		var actual := Gate.step(example["before"], example["synthetic_round_table"],
			example["state10_dispatched_in_emulation"])
		assert_true(actual["supported"], example["name"])
		_assert_snapshot(actual["after"], example["after"])
		assert_eq(int(actual["requested_state"]), int(example["requested_state"]),
			"同一实例请求 12 或 16")
		assert_false(actual["preparation_resolved"], "三段战果计算未执行")
		assert_false(actual["combat_units_ready"], "单位派生边界未执行")
		assert_false(actual["authorizes_persistent_write"], "场次门槛不授权事务")


func test_complete_branch_keeps_existing_roster_and_count() -> void:
	for example in _fixture()["cases"]:
		if example["name"] == "next_round":
			continue
		# Equality branch never consumes the next-round table, even if absent.
		var actual := Gate.step(example["before"], {}, true)
		assert_eq(actual["after"], example["before"], "已完成不清临时表，不递增")
		assert_eq(actual["dispatch_target_va"], 0x4C1D30, "总战果构造入口")


func test_pending_state10_and_invalid_tables_do_not_advance() -> void:
	var example: Dictionary = _fixture()["cases"][1]
	var before: Dictionary = example["before"].duplicate(true)
	var table: Dictionary = example["synthetic_round_table"].duplicate(true)
	assert_eq(Gate.step(before, table, false)["requested_state"], -1, "未到状态 10 保持待定")
	before["current"] = 3
	assert_false(Gate.step(before, table, true)["supported"], "无效计数不能再递增")
	before["current"] = 1.5
	assert_false(Gate.step(before, table, true)["supported"], "不能截断小数计数")
	before = example["before"].duplicate(true)
	table["next_roster"] = [3, -1, 9]
	assert_false(Gate.step(before, table, true)["supported"], "缺 ID 不进行名单准备")
	table["next_roster"] = []
	table["next_roster"].resize(21)
	table["next_roster"].fill(3)
	assert_false(Gate.step(before, table, true)["supported"], "超出原始场次名单区域")
	table = example["synthetic_round_table"].duplicate(true)
	table["config_id"] = 6
	assert_false(Gate.step(before, table, true)["supported"], "其它配置未纳入回放")
	table.erase("config_id")
	assert_false(Gate.step(before, table, true)["supported"], "没有隐式配置")


func test_projection_preserves_inputs_and_returned_snapshot_is_independent() -> void:
	var example: Dictionary = _fixture()["cases"][1]
	var before: Dictionary = example["before"].duplicate(true)
	var table: Dictionary = example["synthetic_round_table"].duplicate(true)
	var saved := before.duplicate(true)
	var saved_table := table.duplicate(true)
	var actual := Gate.step(before, table, true)
	assert_eq(before, saved, "回放不改变输入场次")
	assert_eq(table, saved_table, "回放不改变来源表")
	actual["after"]["temp_roster"][0] = 44
	assert_eq(before, saved, "输出不是输入的共享数组")
	assert_eq(table, saved_table, "输出不是来源名单的共享数组")
	_assert_snapshot(Gate.step(before, table, true)["after"], example["after"])
