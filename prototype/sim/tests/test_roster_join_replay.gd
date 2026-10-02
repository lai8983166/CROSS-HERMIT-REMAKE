extends "res://sim/tests/test_base.gd"

const Join = preload("res://sim/roster_join_replay.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const Start = preload("res://sim/week_start_replay.gd")


func _fixture() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/roster_join_evidence.json")))


func _candidate(snapshot: Dictionary) -> Dictionary:
	for record in snapshot["participants"]:
		if int(record["character_id"]) == 5:
			return record
	return {}


func test_four_complete_outputs_match_independent_native_execution() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		var replay := Join.new()
		var saved: Dictionary = example["before"].duplicate(true)
		var result := replay.apply_once(example["name"], example["context"], example["before"], fixture["rules"])
		assert_true(result["supported"])
		if result["supported"]:
			assert_eq(result["after"], example["expected_after"])
		assert_eq(example["before"], saved)
		for key in ["chapter_completed", "school_initialized", "live_witness", "authorizes_persistent_write"]:
			assert_false(result[key])


func test_progress_pools_calendar_groups_and_other_roles_remain_unchanged() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var result := Join.new().apply_once("preserve", example["context"], example["before"], fixture["rules"])
	assert_true(result["supported"])
	if not result["supported"]:
		return
	for key in ["month", "week", "flags", "teacher_ids", "teacher_count", "group_student_ids", "group_student_indices"]:
		assert_eq(result["after"][key], example["before"][key])
	for record in example["before"]["participants"]:
		if record["character_id"] != 5:
			assert_true(result["after"]["participants"].has(record))
	for key in ["attributes", "growth_pools", "job", "job_progress"]:
		assert_eq(_candidate(result["after"])[key], _candidate(example["before"])[key])
	assert_eq(_candidate(result["after"])["unlock_reserved_bytes"], [0, 0])


func test_same_instance_and_new_delivery_do_not_repeat_roster_or_reset_role() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var replay := Join.new()
	var first := replay.apply_once("once", example["context"], example["before"], fixture["rules"])
	assert_true(first["supported"])
	if not first["supported"]:
		return
	for tick in range(3):
		assert_eq(replay.apply_once("once", example["context"], example["before"], fixture["rules"]), first)
	var after: Dictionary = first["after"].duplicate(true)
	_candidate(after)["level_50"] = 49
	_candidate(after)["unlock_reserved_bytes"] = [7, 8]
	var again := replay.apply_once("redelivered", example["context"], after, fixture["rules"])
	assert_eq(again["status"], "already_available")
	assert_eq(again["after"], after)
	assert_eq(again["after"]["student_count"], 4)


func test_difficulty_controls_actual_skill_ids_and_claimed_item_slots() -> void:
	var fixture := _fixture()
	for index in range(2):
		var example: Dictionary = fixture["cases"][index]
		var result := Join.new().apply_once("equip", example["context"], example["before"], fixture["rules"])
		assert_true(result["supported"])
		if not result["supported"]:
			continue
		var candidate := _candidate(result["after"])
		assert_eq(candidate["equipped_items"], [6, 0, 0, 0, 0, 0, 0, 0])
		assert_eq(result["after"]["item_flags"][5], 0x30b)
		assert_eq(result["after"]["item_flags"][6], 0x101)
		if index == 0:
			assert_eq(candidate["skill_statuses"].slice(0, 3), [6, 6, 0])
		else:
			assert_eq(candidate["equipped_skills"], [0, 0, 0, 0, 0, 0, 0, 0])
			assert_eq(candidate["skill_statuses"], _candidate(example["before"])["skill_statuses"])


func test_level_uses_growth_pools_and_learned_skill_costs() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var before: Dictionary = example["before"].duplicate(true)
	_candidate(before)["growth_pools"] = [0, 0, 0, 0, 0, 0, 0]
	_candidate(before)["skill_statuses"].fill(0)
	_candidate(before)["equipped_skills"].fill(0)
	var result := Join.new().apply_once("level", example["context"], before, fixture["rules"])
	assert_true(result["supported"])
	if result["supported"]:
		assert_eq(_candidate(result["after"])["level_50"], 1)
		assert_eq(_candidate(result["after"])["attributes"], _candidate(before)["attributes"])


func test_wrong_state_source_opcode_and_unsupported_teacher_or_group_reject() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for pair in [["task_state", 7], ["script_path", "DATA/ADV/DAT/Chapter021.ybc"],
			["script_file_offset", 24], ["opcode", 145], ["character_id", 101],
			["group", 0], ["slot", 0], ["difficulty", 1], ["difficulty", 0.5]]:
		var context: Dictionary = example["context"].duplicate(true)
		context[pair[0]] = pair[1]
		var replay := Join.new()
		assert_false(replay.apply_once("bad", context, example["before"], fixture["rules"])["supported"])
		assert_true(replay.apply_once("bad", example["context"], example["before"], fixture["rules"])["supported"])
	for key in example["context"]:
		var context: Dictionary = example["context"].duplicate(true)
		context.erase(key)
		assert_false(Join.new().apply_once("missing", context, example["before"], fixture["rules"])["supported"])


func test_invalid_records_roster_and_rules_leave_input_and_instance_untouched() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for kind in range(17):
		var before: Dictionary = example["before"].duplicate(true)
		var rules: Dictionary = fixture["rules"].duplicate(true)
		match kind:
			0: before["participants"].remove_at(2)
			1: before["participants"][1]["character_id"] = 3
			2: _candidate(before).erase("growth_pools")
			3: _candidate(before)["job"] = 0
			4: _candidate(before)["unlock_reserved_bytes"] = [1]
			5: before["student_count"] = 4
			6: before["student_ids"][1] = 3
			7: before["student_ids"][3] = 5
			8: before["availability"][5] = 1
			9: before["teacher_count"] = 1
			10: before["group_student_indices"][0][0] = 1
			11: before["item_flags"].pop_back()
			12: rules["week"]["unlock_rules"].pop_back()
			13: rules["level_thresholds"][4] = -1
			14: rules["learned_points"] = []
			15: before["week"] = 4
			16: _candidate(before)["growth_pools"][0] = 2147483647
		var saved := before.duplicate(true)
		var replay := Join.new()
		assert_false(replay.apply_once("bad", example["context"], before, rules)["supported"], "invalid case " + str(kind))
		assert_eq(before, saved)
		assert_true(replay.apply_once("bad", example["context"], example["before"], fixture["rules"])["supported"])


func test_cache_conflicts_and_output_aliases_cannot_undo_or_overwrite_join() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var replay := Join.new()
	var result := replay.apply_once("cached", example["context"], example["before"], fixture["rules"])
	result["after"]["student_ids"].fill(-1)
	_candidate(result["after"])["skill_statuses"].fill(0)
	var changed: Dictionary = example["before"].duplicate(true)
	changed["week"] = 4
	assert_false(replay.apply_once("cached", example["context"], changed, fixture["rules"])["supported"])
	var context: Dictionary = example["context"].duplicate(true)
	context["character_id"] = 101
	assert_eq(replay.apply_once("cached", context, example["before"], fixture["rules"])["reason"], "instance_input_conflict")
	var rules: Dictionary = fixture["rules"].duplicate(true)
	rules["learned_points"][0] += 1
	assert_false(replay.apply_once("cached", example["context"], example["before"], rules)["supported"])
	assert_eq(replay.apply_once("cached", example["context"], example["before"], fixture["rules"])["after"], example["expected_after"])


func test_raw_json_and_reordered_records_match_by_character_id() -> void:
	var fixture: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/roster_join_evidence.json"))
	var example: Dictionary = fixture["cases"][0]
	example["before"]["participants"].reverse()
	example["expected_after"]["participants"].reverse()
	var result := Join.new().apply_once("ids", example["context"], example["before"], fixture["rules"])
	assert_true(result["supported"])
	if result["supported"]:
		assert_eq(Roles._integers(result["after"]), Roles._integers(example["expected_after"]))


func test_unrelated_metadata_preserved_and_distinct_instances_are_independent() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var before: Dictionary = example["before"].duplicate(true)
	before["relationships"] = [[0.75]]
	_candidate(before)["extra"] = {"ratio": 0.25}
	var replay := Join.new()
	var result := replay.apply_once("one", example["context"], before, fixture["rules"])
	assert_true(result["supported"])
	if result["supported"]:
		assert_eq(result["after"]["relationships"], [[0.75]])
		assert_eq(_candidate(result["after"])["extra"], {"ratio": 0.25})
	var existing: Dictionary = fixture["cases"][2]
	assert_eq(replay.apply_once("two", existing["context"], existing["before"], fixture["rules"])["after"], existing["before"])


func test_joined_role_is_required_and_preserved_for_following_whole_week() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var joined := Join.new().apply_once("join", example["context"], example["before"], fixture["rules"])
	assert_true(joined["supported"])
	if not joined["supported"]:
		return
	var context := {"task_state": 7, "adv_completed": true} # Explicit completion input, not a chapter witness.
	var result := Start.new().begin("week", context, joined["after"], fixture["rules"]["week"])
	assert_true(result["supported"])
	if result["supported"]:
		assert_eq([result["after"]["month"], result["after"]["week"]], [5, 1])
		assert_eq(result["after"]["student_ids"], joined["after"]["student_ids"])
		for key in ["growth_pools", "job_progress", "level_50"]:
			assert_eq(_candidate(result["after"])[key], _candidate(joined["after"])[key])
		assert_false(result["school_initialized"])
	var missing: Dictionary = joined["after"].duplicate(true)
	missing["participants"].remove_at(2)
	assert_false(Start.new().begin("bad", context, missing, fixture["rules"]["week"])["supported"])
