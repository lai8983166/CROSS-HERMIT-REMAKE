extends "res://sim/tests/test_base.gd"

const Transaction = preload("res://sim/result_transaction_replay.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func _fixture() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/result_transaction_evidence.json")))


func test_joint_snapshot_matches_all_six_native_task_paths() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		var replay := Transaction.new()
		var initial := replay.begin(example["name"], example["context"], example["before"], fixture["rules"])
		assert_true(initial["supported"], example["name"] + " " + initial.get("reason", ""))
		if not initial["supported"]:
			continue
		assert_eq(initial["learning_draws"], example["expected_learning_draws"])
		assert_eq(initial["rand_state"], example["expected_rand_state"])
		var result := replay.finish(example["name"], example["confirmed"], example["mvp_ready"])
		assert_true(result["supported"], example["name"] + " " + result.get("reason", ""))
		if not result["supported"]:
			continue
		assert_eq(result["after"], example["expected_after"], example["name"] + " 完整事务快照")
		assert_eq(result["before_week"], example["expected_before_week"])
		assert_eq(result["branch"], example["expected_branch"])
		assert_eq(result["week_executed"], example["expected_week_executed"])
		assert_eq(result["requested_state"], example["expected_requested_state"])
		assert_eq(result["school_script_requests"], example["expected_school_script"])
		assert_eq(result["completed"], example["expected_requested_state"] != 12)
		assert_false(result["school_initialized"])
		assert_false(result["school_task_executed"])
		assert_false(result["authorizes_persistent_write"])


func test_week_observes_growth_post_fields_relationships_and_recipient_in_native_order() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][5]
	var replay := Transaction.new()
	assert_true(replay.begin("order", example["context"], example["before"], fixture["rules"])["supported"])
	var result := replay.finish("order", false, false)
	assert_true(result["supported"])
	if not result["supported"]:
		return
	assert_eq(result["phase_log"].map(func(entry): return entry["phase"]),
		["initialized", "result_fields", "week_settlement"])
	assert_eq(result["phase_log"][1]["after"], example["expected_before_week"])
	assert_eq(result["phase_log"][2]["before"], example["expected_before_week"])
	assert_eq(result["phase_log"][2]["after"], example["expected_after"])
	assert_eq(result["before_week"]["characters"][1]["recipient_count"], 1)
	assert_eq(result["before_week"]["characters"][0]["skill_statuses"].slice(0, 2), [6, 6])
	assert_eq(result["after"]["characters"][0]["skill_statuses"].slice(0, 2), [6, 5])
	assert_eq(result["before_week"]["item_flags"].slice(0, 5), [0x301, 0x307, 0x407, 0x40b, 0x205])
	assert_eq(result["after"]["item_flags"].slice(0, 5), [0x101, 0x307, 0x107, 0x10b, 0x205])
	assert_false(result["week_pending"])


func test_ordinary_month_end_preserves_calendar_unlocks_and_cleanup_inputs() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var replay := Transaction.new()
	assert_true(replay.begin("ordinary", example["context"], example["before"], fixture["rules"])["supported"])
	var result := replay.finish("ordinary", true, true)
	assert_eq(result["after"]["month"], 4)
	assert_eq(result["after"]["week"], 5)
	assert_false(result["week_executed"])
	for key in ["flags", "item_flags", "availability"]:
		assert_eq(result["after"][key], example["before"][key])
	assert_eq(result["after"]["characters"][0]["skill_statuses"].slice(0, 2), [6, 6])
	assert_eq(result["after"]["characters"][0]["unlock_flags"], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
	assert_eq(result["phase_log"].size(), 2)
	assert_eq(result["school_script_requests"], [{"path": "Data\\Adv\\dat\\CH003.ybc", "subroutine": 7}])


func test_waits_publish_only_initialized_roles_and_keep_confirmation_across_deliveries() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var replay := Transaction.new()
	assert_true(replay.begin("wait", example["context"], example["before"], fixture["rules"])["supported"])
	var result := replay.finish("wait", false, true)
	assert_eq(result["status"], "waiting_confirmation")
	assert_eq(result["after"], fixture["cases"][1]["expected_after"])
	assert_eq(result["phase_log"].size(), 1)
	assert_eq(result["school_script_requests"], [])
	result = replay.finish("wait", true, false)
	assert_eq(result["status"], "waiting_mvp")
	assert_eq(result["after"], fixture["cases"][2]["expected_after"])
	assert_eq(result["requested_state"], 12)
	assert_false(result["completed"])
	result = replay.finish("wait", false, true)
	assert_eq(result["after"], example["expected_after"])
	assert_true(result["completed"])


func test_duplicate_initialization_and_finish_preserve_entire_completed_week() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][5]
	var replay := Transaction.new()
	var first := replay.begin("once", example["context"], example["before"], fixture["rules"])
	assert_true(first["supported"])
	if not first["supported"]:
		return
	first["after"]["characters"][0]["growth_pools"][0] = 0
	first["phase_log"].clear()
	var duplicate := replay.begin("once", example["context"], example["before"], fixture["rules"])
	assert_eq(duplicate["status"], "duplicate")
	assert_eq(duplicate["phase_log"].size(), 1)
	var complete := replay.finish("once", true, true)
	complete["after"]["week"] = 1
	complete["before_week"]["characters"][1]["recipient_count"] = 5
	complete["phase_log"][2]["after"]["item_flags"][0] = 0
	complete["school_script_requests"][0]["subroutine"] = 7
	for k in range(3):
		duplicate = replay.finish("once", false, false)
		assert_eq(duplicate["status"], "duplicate")
		assert_eq(duplicate["after"], example["expected_after"])
		assert_eq(duplicate["before_week"], example["expected_before_week"])
		assert_eq(duplicate["phase_log"].size(), 3)
		assert_eq(duplicate["school_script_requests"], example["expected_school_script"])
	duplicate = replay.begin("once", example["context"], example["before"], fixture["rules"])
	assert_eq(duplicate["after"], example["expected_after"], "初始化重送不回退到未推进周的角色阶段")


func test_week_snapshot_and_rules_are_validated_before_any_role_stage() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][5]
	for kind in range(7):
		var before: Dictionary = example["before"].duplicate(true)
		var rules: Dictionary = fixture["rules"].duplicate(true)
		match kind:
			0: before["characters"][0].erase("unlock_flags")
			1: before["characters"][0]["equipped_items"][0] = 361
			2: before["availability"][5] = 1
			3: before["item_flags"][0] = 0x301 | (99 << 1)
			4: rules["week"]["unlock_rules"].pop_back()
			5: before["flags"].erase("0x7a55f6")
			6: rules.erase("week")
		var saved := before.duplicate(true)
		var replay := Transaction.new()
		assert_false(replay.begin("bad", example["context"], before, rules)["supported"])
		assert_false(replay.finish("bad", true, true)["supported"], "周数据缺失不留下已加成长的实例")
		assert_eq(before, saved)


func test_state_gate_unknown_modes_or_missing_ids_do_not_create_transaction() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][5]
	for changes in [{"task_state": 10}, {"task_state": 16}, {"current": 0}, {"mode": 2}, {"result_flag": 2}]:
		var context: Dictionary = example["context"].duplicate(true)
		context.merge(changes, true)
		var replay := Transaction.new()
		assert_false(replay.begin("bad", context, example["before"], fixture["rules"])["supported"])
		assert_false(replay.finish("bad", true, true)["supported"])
	for kind in range(3):
		var before: Dictionary = example["before"].duplicate(true)
		match kind:
			0: before["characters"][0].erase("character_id")
			1: before["characters"][1]["character_id"] = 3
			2: before["characters"][0]["character_id"] = 3.5
		assert_false(Transaction.new().begin("bad", example["context"], before, fixture["rules"])["supported"])
	assert_false(Transaction.new().begin("", example["context"], example["before"], fixture["rules"])["supported"])


func test_cached_instance_rejects_changed_calendar_equipment_rules_or_context() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][5]
	var replay := Transaction.new()
	assert_true(replay.begin("cache", example["context"], example["before"], fixture["rules"])["supported"])
	for kind in range(4):
		var before: Dictionary = example["before"].duplicate(true)
		var rules: Dictionary = fixture["rules"].duplicate(true)
		var context: Dictionary = example["context"].duplicate(true)
		match kind:
			0: before["week"] = 3
			1: before["characters"][0]["equipped_skills"][0] = 2
			2: rules["week"]["unlock_rules"][0]["month"] = 1
			3: context["clock_seed"] += 1
		assert_false(replay.begin("cache", context, before, rules)["supported"])
	assert_eq(replay.finish("cache", true, true)["after"], example["expected_after"])


func test_reordered_role_records_and_participant_indices_preserve_native_week_identity() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][5]
	var before: Dictionary = example["before"].duplicate(true)
	var expected: Dictionary = example["expected_after"].duplicate(true)
	var before_week: Dictionary = example["expected_before_week"].duplicate(true)
	before["characters"].reverse()
	expected["characters"].reverse()
	before_week["characters"].reverse()
	var context: Dictionary = example["context"].duplicate(true)
	context["participant_ids"] = [9, 3, 4]
	context["group_slots"][0] = [1, 2, 0, -1]
	var replay := Transaction.new()
	assert_true(replay.begin("ids", context, before, fixture["rules"])["supported"])
	var result := replay.finish("ids", false, false)
	assert_eq(result["after"], expected)
	assert_eq(result["before_week"], before_week)
	assert_eq(result["learning_draws"], example["expected_learning_draws"])


func test_raw_json_numeric_equipment_preserves_real_membership_during_cleanup() -> void:
	var fixture: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/result_transaction_evidence.json"))
	for example in fixture["cases"]:
		var replay := Transaction.new()
		var initial := replay.begin("json", example["context"], example["before"], fixture["rules"])
		assert_true(initial["supported"])
		if not initial["supported"]:
			continue
		var result := replay.finish("json", example["confirmed"], example["mvp_ready"])
		assert_true(result["supported"])
		if result["supported"]:
			assert_eq(Roles._integers(result["after"]), Roles._integers(example["expected_after"]))
			assert_eq(Roles._integers(result["before_week"]), Roles._integers(example["expected_before_week"]))


func test_unrelated_metadata_and_input_snapshots_survive_joint_settlement() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][5]
	var before: Dictionary = example["before"].duplicate(true)
	before["metadata"] = {"fraction": 1.25, "notes": ["independent"]}
	before["characters"][0]["presentation_alpha"] = 0.5
	var saved := before.duplicate(true)
	var saved_rules: Dictionary = fixture["rules"].duplicate(true)
	var expected: Dictionary = example["expected_after"].duplicate(true)
	expected["metadata"] = before["metadata"].duplicate(true)
	expected["characters"][0]["presentation_alpha"] = 0.5
	var replay := Transaction.new()
	assert_true(replay.begin("extra", example["context"], before, fixture["rules"])["supported"])
	var result := replay.finish("extra", true, true)
	assert_eq(result["after"], expected)
	result["after"]["metadata"]["fraction"] = 2.5
	assert_eq(before, saved)
	assert_eq(fixture["rules"], saved_rules)
	assert_eq(replay.finish("extra", false, false)["after"], expected)


func test_one_instance_cannot_redirect_another_instances_pending_confirmation() -> void:
	var fixture := _fixture()
	var ordinary: Dictionary = fixture["cases"][0]
	var special: Dictionary = fixture["cases"][5]
	var replay := Transaction.new()
	assert_true(replay.begin("a", ordinary["context"], ordinary["before"], fixture["rules"])["supported"])
	assert_true(replay.begin("b", special["context"], special["before"], fixture["rules"])["supported"])
	assert_eq(replay.finish("b", false, false)["after"], special["expected_after"])
	var waiting := replay.finish("a", false, true)
	assert_eq(waiting["status"], "waiting_confirmation")
	assert_eq(waiting["after"], fixture["cases"][1]["expected_after"])
	assert_eq(replay.finish("a", true, true)["after"], ordinary["expected_after"])
