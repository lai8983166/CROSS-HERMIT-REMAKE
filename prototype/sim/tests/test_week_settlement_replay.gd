extends "res://sim/tests/test_base.gd"

const Settlement = preload("res://sim/week_settlement_replay.gd")


func _fixture() -> Dictionary:
	return _integer_numbers(JSON.parse_string(FileAccess.get_file_as_string("res://data/week_settlement_evidence.json")))


func _integer_numbers(value: Variant) -> Variant:
	if value is float:
		return int(value)
	if value is Array:
		var result := []
		for entry in value:
			result.append(_integer_numbers(entry))
		return result
	if value is Dictionary:
		var result := {}
		for key in value:
			result[key] = _integer_numbers(value[key])
		return result
	return value


func test_entire_week_snapshot_matches_native_execution() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		var actual := Settlement.project(example["before"], fixture["rules"])
		assert_true(actual["supported"], example["name"])
		assert_eq(actual["after"], example["expected_after"], "角色、解锁、物品、技能与月周逐字段一致")
		assert_false(actual["authorizes_persistent_write"], "隔离回放不授权实机写入")


func test_json_numeric_ids_keep_equipped_items_and_skills() -> void:
	var fixture := _fixture()
	var raw: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/week_settlement_evidence.json"))
	for example in raw["cases"]:
		var actual := Settlement.project(example["before"], raw["rules"])
		assert_true(actual["supported"])
		assert_eq(_integer_numbers(actual["after"]), _integer_numbers(example["expected_after"]),
			"原版整数 ID 和 JSON 整数数值均保留真实装备成员关系")
	assert_eq(Settlement.project(raw["cases"][0]["before"], raw["rules"])["after"],
		fixture["cases"][0]["expected_after"])


func test_state12_round_and_result_fields_gate_before_projection() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for changes in [{"task_state": 10}, {"task_state": 16}, {"current": 0}, {"mode": 1},
			{"mode": 2}, {"total": 6}, {"result_fields_completed": false}, {"task_state": 12.5}]:
		var context: Dictionary = example["context"].duplicate(true)
		context.merge(changes, true)
		var replay := Settlement.new()
		assert_false(replay.apply_once("week-a", context, example["before"], fixture["rules"])["supported"],
			"状态10/16、未完场次、未知模式和未完前置字段不计算周事务")
	var replay := Settlement.new()
	assert_false(replay.apply_once("", example["context"], example["before"], fixture["rules"])["supported"])
	assert_false(replay.apply_once("week-a", {}, example["before"], fixture["rules"])["supported"])


func test_ordinary_branch_preserves_whole_input_snapshot() -> void:
	var fixture := _fixture()
	for index in [1, 2]:
		var before: Dictionary = fixture["cases"][index]["before"]
		var replay := Settlement.new()
		var result := replay.apply_once("ordinary", fixture["cases"][0]["context"], before, fixture["rules"])
		assert_true(result["supported"])
		assert_eq(result["status"], "no_week_request")
		assert_eq(result["after"], before, "普通总战果不消费裸周函数探针")


func test_duplicate_delivery_and_changed_instance_input_are_safe() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var replay := Settlement.new()
	var first := replay.apply_once("week-a", example["context"], example["before"], fixture["rules"])
	assert_eq(first["status"], "projected_once")
	first["after"]["week"] = 1
	first["after"]["participants"][0]["unlock_flags"][0] = 0
	var second := replay.apply_once("week-a", example["context"], example["before"], fixture["rules"])
	assert_eq(second["status"], "duplicate")
	assert_eq(second["after"], example["expected_after"], "重送不再次推进，也不共享外部可变快照")
	var changed: Dictionary = example["before"].duplicate(true)
	changed["flags"]["0x7a55fa"] = 10
	assert_false(replay.apply_once("week-a", example["context"], changed, fixture["rules"])["supported"],
		"同实例更换输入不能覆盖已记录结果")


func test_missing_duplicate_id_or_available_record_rejects_atomically() -> void:
	var fixture := _fixture()
	var original: Dictionary = fixture["cases"][0]["before"]
	for kind in range(5):
		var before: Dictionary = original.duplicate(true)
		match kind:
			0: before["participants"][0].erase("character_id")
			1: before["participants"][1]["character_id"] = 3
			2: before["participants"][0]["character_id"] = 3.5
			3: before["availability"][5] = 1
			4: before["participants"][0]["skill_statuses"] = [6]
		var saved := before.duplicate(true)
		assert_false(Settlement.project(before, fixture["rules"])["supported"])
		assert_eq(before, saved, "整体验证失败不产生部分解锁或月周写入")


func test_unlock_date_sentinel_and_exact_prerequisite_boundary() -> void:
	var fixture := _fixture()
	var before: Dictionary = fixture["cases"][1]["before"].duplicate(true)
	before["week"] = 1 # Source function sees week2 after its increment.
	var result := Settlement.project(before, fixture["rules"])
	assert_eq(result["after"]["participants"][0]["unlock_flags"].slice(0, 10), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
	before["participants"][0]["job_progress"][1] = 100
	result = Settlement.project(before, fixture["rules"])
	assert_eq(result["after"]["participants"][0]["unlock_flags"].slice(0, 10), [1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
	before["participants"][0]["attributes"] = [75, 0, 0, 0, 0, 75, 50]
	for progress in [14, 15]:
		before["participants"][0]["job_progress"][1] = progress
		result = Settlement.project(before, fixture["rules"])
		assert_eq(result["after"]["participants"][0]["unlock_flags"][10], 1 if progress == 15 else 0,
			"和原版直接函数探针相同的属性及职业条件")


func test_incomplete_rules_and_uncovered_owner_fail_before_any_projection() -> void:
	var fixture := _fixture()
	var before: Dictionary = fixture["cases"][0]["before"].duplicate(true)
	var rules: Dictionary = fixture["rules"].duplicate(true)
	rules["unlock_rules"].pop_back()
	assert_false(Settlement.project(before, rules)["supported"])
	rules = fixture["rules"].duplicate(true)
	rules["unlock_rules"][0]["job_requirements"][0]["type"] = 31
	assert_false(Settlement.project(before, rules)["supported"])
	before["item_flags"][0] = 0x301 | (99 << 1)
	var saved := before.duplicate(true)
	assert_false(Settlement.project(before, fixture["rules"])["supported"])
	assert_eq(before, saved)


func test_source_inputs_and_output_snapshots_are_independent() -> void:
	var fixture := _fixture()
	var before: Dictionary = fixture["cases"][0]["before"].duplicate(true)
	var rules: Dictionary = fixture["rules"].duplicate(true)
	var saved_before := before.duplicate(true)
	var saved_rules := rules.duplicate(true)
	var result := Settlement.project(before, rules)
	result["after"]["participants"][0]["equipped_skills"][0] = 2
	result["after"]["item_flags"][0] = 0
	assert_eq(before, saved_before)
	assert_eq(rules, saved_rules)
	assert_eq(Settlement.project(before, rules)["after"], fixture["cases"][0]["expected_after"])
