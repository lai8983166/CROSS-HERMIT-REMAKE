extends "res://sim/tests/test_base.gd"

const Roles = preload("res://sim/all_result_role_replay.gd")


func _fixture() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/role_application_evidence.json")))


func test_six_state12_paths_match_complete_native_role_snapshots() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		var replay := Roles.new()
		var initial := replay.begin(example["name"], example["context"], example["before"], fixture["rules"])
		assert_true(initial["supported"], example["name"] + " " + initial.get("reason", ""))
		if not initial["supported"]:
			continue
		assert_eq(initial["branch"], example["expected_branch"])
		assert_eq(initial["learning_draws"], example["expected_learning_draws"], "原版所有随机消费顺序")
		assert_eq(initial["rand_state"], example["expected_rand_state"])
		assert_eq(initial["skill_display_needed"], example["expected_skill_display_needed"])
		var actual := replay.finish(example["name"], example["confirmed"], example["mvp_ready"])
		assert_true(actual["supported"])
		assert_eq(actual["after"], example["expected_after"], example["name"] + " 全字段")
		assert_eq(actual["requested_state"], example["expected_requested_state"])
		assert_false(actual["school_initialized"])
		assert_false(actual["authorizes_persistent_write"])


func test_skill_random_attribute_pending_and_exact_job_boundary_match_native() -> void:
	var fixture := _fixture()
	for example in fixture["skill_probes"]:
		var result := Roles.project_growth(example["before"], [3], example["clock_seed"], fixture["rules"])
		assert_true(result["supported"], example["name"] + " " + result.get("reason", ""))
		if not result["supported"]:
			continue
		assert_eq(result["after"], example["expected_after"], example["name"])
		assert_eq(result["learning_draws"], example["expected_learning_draws"])
		assert_eq(result["rand_state"], example["expected_rand_state"])
		assert_eq(result["skill_display_needed"], example["expected_skill_display_needed"])
		assert_false(result["authorizes_persistent_write"])


func test_progress_byte_wrap_100_sentinel_and_99_cap_match_native() -> void:
	var example: Dictionary = _fixture()["post_field_probes"][0]
	var result := Roles.project_post_fields(example["before"], example["context"])
	assert_true(result["supported"])
	if result["supported"]:
		assert_eq(result["after"], example["expected_after"], "127→0、100保留、99封顶，包括完整关系与历史")


func test_json_numbers_produce_same_snapshots_and_rng_as_integer_inputs() -> void:
	var fixture: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/role_application_evidence.json"))
	for example in fixture["cases"]:
		var replay := Roles.new()
		var initial := replay.begin("raw-json", example["context"], example["before"], fixture["rules"])
		assert_true(initial["supported"])
		if not initial["supported"]:
			continue
		var result := replay.finish("raw-json", example["confirmed"], example["mvp_ready"])
		assert_eq(result["after"], Roles._integers(example["expected_after"]))
		assert_eq(result["learning_draws"], Roles._integers(example["expected_learning_draws"]))


func test_missing_duplicate_fractional_id_or_relationship_rejects_atomically() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for kind in range(6):
		var before: Dictionary = example["before"].duplicate(true)
		match kind:
			0: before["characters"][0].erase("character_id")
			1: before["characters"][1]["character_id"] = 3
			2: before["characters"][0]["character_id"] = 3.5
			3: before["characters"][0]["skill_statuses"].pop_back()
			4: before["relationships"].pop_back()
			5: before["relationships"][1] = before["relationships"][0].duplicate()
		var saved := before.duplicate(true)
		var replay := Roles.new()
		assert_false(replay.begin("bad", example["context"], before, fixture["rules"])["supported"])
		assert_false(replay.finish("bad", true, true)["supported"], "失败初始化不留下可应用阶段")
		assert_eq(before, saved)


func test_state10_state16_incomplete_round_and_unknown_branch_cannot_initialize() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for changes in [{"task_state": 10}, {"task_state": 16}, {"current": 0}, {"mode": 2},
			{"result_flag": 2}, {"task_state": 12.5}, {"total": 6, "current": 6}]:
		var context: Dictionary = example["context"].duplicate(true)
		context.merge(changes, true)
		var replay := Roles.new()
		assert_false(replay.begin("bad", context, example["before"], fixture["rules"])["supported"])
		assert_false(replay.finish("bad", true, true)["supported"])
	var replay := Roles.new()
	assert_false(replay.begin("", example["context"], example["before"], fixture["rules"])["supported"])
	assert_false(replay.begin("bad", {}, example["before"], fixture["rules"])["supported"])


func test_confirmation_and_mvp_waits_do_not_apply_later_fields() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var replay := Roles.new()
	var initial := replay.begin("phases", example["context"], example["before"], fixture["rules"])
	assert_true(initial["supported"])
	if not initial["supported"]:
		return
	var waiting := replay.finish("phases", false, true)
	assert_eq(waiting["status"], "waiting_confirmation")
	assert_eq(waiting["after"], fixture["cases"][1]["expected_after"])
	waiting = replay.finish("phases", true, false)
	assert_eq(waiting["status"], "waiting_mvp")
	assert_eq(waiting["after"], fixture["cases"][2]["expected_after"])
	var final := replay.finish("phases", false, true)
	assert_eq(final["after"], example["expected_after"], "先前确认已记录，不需再次按确认")
	assert_true(final["result_fields_completed"])
	assert_eq(final["requested_state"], 6)


func test_duplicate_stages_do_not_add_pools_progress_relationships_or_recipient_again() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var replay := Roles.new()
	var first := replay.begin("once", example["context"], example["before"], fixture["rules"])
	assert_true(first["supported"])
	if not first["supported"]:
		return
	first["after"]["characters"][0]["growth_pools"][0] = 0
	first["display_request"].clear()
	var duplicate := replay.begin("once", example["context"], example["before"], fixture["rules"])
	assert_eq(duplicate["status"], "duplicate")
	assert_eq(duplicate["after"], fixture["cases"][1]["expected_after"])
	assert_eq(duplicate["display_request"].size(), 3)
	var final := replay.finish("once", true, true)
	final["after"]["characters"][1]["recipient_count"] = 5
	final["after"]["relationships"][0]["value"] = 0
	for k in range(3):
		duplicate = replay.finish("once", false, false)
		assert_eq(duplicate["status"], "duplicate")
		assert_eq(duplicate["after"], example["expected_after"])
	duplicate = replay.begin("once", example["context"], example["before"], fixture["rules"])
	assert_eq(duplicate["after"], example["expected_after"], "重送初始化不会退回成长阶段")


func test_changed_instance_inputs_cannot_overwrite_cached_record() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var replay := Roles.new()
	assert_true(replay.begin("same", example["context"], example["before"], fixture["rules"])["supported"])
	var changed: Dictionary = example["before"].duplicate(true)
	changed["characters"][0]["staged_package"][0] += 1
	assert_false(replay.begin("same", example["context"], changed, fixture["rules"])["supported"])
	var context: Dictionary = example["context"].duplicate(true)
	context["clock_seed"] += 1
	assert_false(replay.begin("same", context, example["before"], fixture["rules"])["supported"])
	assert_eq(replay.finish("same", true, true)["after"], example["expected_after"])


func test_reordered_records_use_ids_and_keep_original_group_rng_order() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var before: Dictionary = example["before"].duplicate(true)
	var expected: Dictionary = example["expected_after"].duplicate(true)
	before["characters"].reverse()
	expected["characters"].reverse()
	var replay := Roles.new()
	var result := replay.begin("ids", example["context"], before, fixture["rules"])
	assert_true(result["supported"])
	if not result["supported"]:
		return
	assert_eq(result["learning_draws"], example["expected_learning_draws"])
	assert_eq(replay.finish("ids", true, true)["after"], expected)
	var context: Dictionary = example["context"].duplicate(true)
	context["participant_ids"] = [9, 3, 4]
	context["group_slots"][0] = [1, 2, 0, -1]
	replay = Roles.new()
	result = replay.begin("indices", context, before, fixture["rules"])
	assert_true(result["supported"])
	if result["supported"]:
		assert_eq(result["learning_draws"], example["expected_learning_draws"])
		assert_eq(replay.finish("indices", true, true)["after"], expected)


func test_uncovered_groups_teachers_support_and_incomplete_rules_reject() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for kind in range(5):
		var context: Dictionary = example["context"].duplicate(true)
		match kind:
			0: context["teacher_ids"][0] = 1
			1: context["task_teacher_slots"][0] = -1
			2: context["support_count"] = 1
			3: context["group0_activity_type"] = 4
			4: context["group_slots"][0][1] = 0
		assert_false(Roles.new().begin("bad", context, example["before"], fixture["rules"])["supported"])
	for kind in range(4):
		var rules: Dictionary = fixture["rules"].duplicate(true)
		match kind:
			0: rules["skills"].pop_back()
			1: rules["skill_grid"][0][0] = 85
			2: rules["job_skill_caps"][10][0] = 8
			3: rules["attribute_increments"][1] = 0
		assert_false(Roles.new().begin("bad", example["context"], example["before"], rules)["supported"])


func test_special_date_bypasses_confirmation_and_stops_before_week_or_school() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][5]
	var replay := Roles.new()
	assert_true(replay.begin("special", example["context"], example["before"], fixture["rules"])["supported"])
	var result := replay.finish("special", false, false)
	assert_true(result["supported"])
	if not result["supported"]:
		return
	assert_eq(result["status"], "week_boundary")
	assert_eq(result["after"], example["expected_after"])
	assert_true(result["week_pending"])
	assert_true(result["result_fields_completed"])
	assert_eq(result["after"]["week"], 4)
	assert_eq(result["requested_state"], 12)
	assert_false(result["school_initialized"])
	assert_eq(replay.finish("special", true, true)["after"], example["expected_after"])


func test_display_records_preserve_before_values_and_level_can_rederive_downward() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var result := Roles.new().begin("display", example["context"], example["before"], fixture["rules"])
	assert_true(result["supported"])
	if not result["supported"]:
		return
	for index in range(3):
		assert_eq(result["display_request"][index]["character_id"], example["before"]["characters"][index]["character_id"])
		assert_eq(result["display_request"][index]["attributes_before"], example["before"]["characters"][index]["attributes"])
		assert_eq(result["display_request"][index]["attributes_after"], example["expected_after"]["characters"][index]["attributes"])
	assert_eq(result["display_request"][0]["level_before"], 45)
	assert_eq(result["display_request"][0]["level_after"], 31)
	assert_lt(result["display_request"][0]["level_after"], result["display_request"][0]["level_before"])


func test_inputs_rules_and_returned_records_have_no_shared_mutable_arrays() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var saved_before: Dictionary = example["before"].duplicate(true)
	var saved_rules: Dictionary = fixture["rules"].duplicate(true)
	var result := Roles.new().begin("copies", example["context"], example["before"], fixture["rules"])
	assert_true(result["supported"])
	if result["supported"]:
		result["after"]["characters"][0]["skill_statuses"][0] = 0
		result["display_request"][0]["attributes_before"][0] = 1
	assert_eq(example["before"], saved_before)
	assert_eq(fixture["rules"], saved_rules)


func test_history_overlap_and_pool_table_overrun_reject_before_store_changes() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for kind in range(2):
		var before: Dictionary = example["before"].duplicate(true)
		if kind == 0:
			before["month"] = 15
			before["week"] = 5
		else:
			before["characters"][2]["growth_pools"][0] = 0x7fffffff
		var saved := before.duplicate(true)
		var replay := Roles.new()
		assert_false(replay.begin("bad", example["context"], before, fixture["rules"])["supported"])
		assert_false(replay.finish("bad", true, true)["supported"])
		assert_eq(before, saved)


func test_unrelated_fractional_metadata_is_preserved_and_input_conflicts_are_detected() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var before: Dictionary = example["before"].duplicate(true)
	before["opaque"] = [1.25, {"value": 2.5}]
	before["characters"][0]["presentation_alpha"] = 0.5
	var expected: Dictionary = example["expected_after"].duplicate(true)
	expected["opaque"] = before["opaque"].duplicate(true)
	expected["characters"][0]["presentation_alpha"] = 0.5
	var replay := Roles.new()
	assert_true(replay.begin("opaque", example["context"], before, fixture["rules"])["supported"])
	var changed := before.duplicate(true)
	changed["opaque"][0] = 1.75
	assert_false(replay.begin("opaque", example["context"], changed, fixture["rules"])["supported"])
	assert_eq(replay.finish("opaque", true, true)["after"], expected)
