extends "res://sim/tests/test_base.gd"

const Replay = preload("res://sim/workroom_return_replay.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func _fixture() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/workroom_return_evidence.json")))


func _drive(replay: RefCounted, example: Dictionary, rules: Dictionary) -> Dictionary:
	var begun: Dictionary = replay.begin("return", example["context"], example["before"], rules)
	assert_true(begun["supported"])
	if not begun["supported"]:
		return begun
	var work: Dictionary = replay.continue_workroom("return", example["continue_ready"])
	assert_eq(Roles._integers(work["after"]), Roles._integers(example["expected_after_workroom"]))
	if example["ch002_context"] != null:
		var start: Dictionary = replay.start_ch002("return", example["ch002_context"])
		assert_true(start["supported"])
		return replay.finish_ch002("return", example["ch002_end_ready"])
	return work


func test_all_four_paths_match_entire_native_snapshots_without_extra_week() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		var result := _drive(Replay.new(), example, fixture["rules"])
		assert_true(result["supported"])
		if not result["supported"]:
			continue
		assert_eq(result["after"], example["expected_after"])
		assert_eq(result["requested_state"], example["expected_pending_state"])
		assert_eq(result["pending_flag"], example["expected_pending_flag"])
		assert_eq(result["ch002_completed"], example["ch002_end_ready"])
		assert_eq(result["script_requests"], [{"path": "Data\\Adv\\dat\\CH002.ybc", "next_task_state": 9}]
			if not example["expected_ch002_requests"].is_empty() or example["ch002_context"] != null else [])
		assert_false(result["week_executed"])
		assert_false(result["school_initialized"])
		assert_false(result["live_witness"])
		assert_false(result["authorizes_persistent_write"])


func test_waits_write_music_only_after_ch002_execution_and_require_end_for9() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var replay := Replay.new()
	var begun := replay.begin("return", example["context"], example["before"], fixture["rules"])
	assert_eq(begun["after"], example["before"])
	assert_false(replay.finish_ch002("return", true)["supported"])
	for tick in range(3):
		var wait := replay.continue_workroom("return", false)
		assert_eq(wait["after"], example["before"])
		assert_eq(wait["pending_flag"], 0)
		assert_eq(wait["script_requests"], [])
	var work := replay.continue_workroom("return", true)
	assert_eq(work["after"]["flags"]["0x7a55f6"], 9)
	assert_eq(work["requested_state"], 6)
	assert_false(replay.finish_ch002("return", true)["supported"])
	var start := replay.start_ch002("return", example["ch002_context"])
	assert_eq(start["after"]["flags"]["0x7a55f6"], 11)
	assert_eq(start["after"]["flags"]["0x7e11a0"], 0)
	for tick in range(3):
		var wait := replay.finish_ch002("return", false)
		assert_eq(wait["after"], start["after"])
		assert_eq(wait["requested_state"], 6)
		assert_eq(wait["pending_flag"], 0)
	assert_eq(replay.finish_ch002("return", true)["requested_state"], 9)


func test_duplicates_never_repeat_writes_and_all_views_are_frozen_copies() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var replay := Replay.new()
	var result := _drive(replay, example, fixture["rules"])
	var expected: Dictionary = result.duplicate(true)
	result["after"]["flags"]["0x7a4e62"] = 0
	result["after"]["participants"][0]["attributes"][0] = 0
	result["script_requests"].clear()
	result["phase_log"].clear()
	for tick in range(3):
		for next in [replay.begin("return", example["context"], example["before"], fixture["rules"]),
				replay.continue_workroom("return", false), replay.start_ch002("return", example["ch002_context"]),
				replay.finish_ch002("return", false)]:
			assert_eq(next["after"], expected["after"])
			assert_eq(next["phase_log"], expected["phase_log"])
			assert_eq(next["requested_state"], 9)
	var changed: Dictionary = example["context"].duplicate(true)
	changed["adv_completed"] = false
	assert_false(replay.begin("return", changed, example["before"], fixture["rules"])["supported"])
	changed = example["ch002_context"].duplicate(true)
	changed["next_task_state"] = 8
	assert_false(replay.start_ch002("return", changed)["supported"])
	assert_eq(replay.finish_ch002("return", false)["after"], expected["after"])


func test_missing_end_source_and_wrong_next_state_reject_before_caching() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for pair in [["adv_completed", false], ["adv_completed", 1], ["task_state", 6],
			["vm_active", 1], ["next_task_state", 9], ["pending_flag", 0],
			["end_file_offset", 20], ["opcode", 112], ["script_path", "ch001.ybc"]]:
		var context: Dictionary = example["context"].duplicate(true)
		context[pair[0]] = pair[1]
		var replay := Replay.new()
		assert_false(replay.begin("return", context, example["before"], fixture["rules"])["supported"])
		assert_false(replay.continue_workroom("return", true)["supported"])
		assert_false(replay.finish_ch002("return", true)["supported"])
		assert_true(replay.begin("return", example["context"], example["before"], fixture["rules"])["supported"])


func test_invalid_roster_calendar_background_and_ch002_load_cannot_advance() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var bad: Array = []
	for pair in [["month", 4], ["week", 5], ["student_count", 3]]:
		var before: Dictionary = example["before"].duplicate(true)
		before[pair[0]] = pair[1]
		bad.append(before)
	var missing: Dictionary = example["before"].duplicate(true)
	missing["participants"].remove_at(3)
	bad.append(missing)
	var background: Dictionary = example["before"].duplicate(true)
	background["adv_globals"]["0x7a5292"] = 1
	bad.append(background)
	var roster: Dictionary = example["before"].duplicate(true)
	roster["student_ids"][3] = 3
	bad.append(roster)
	for before in bad:
		var replay := Replay.new()
		var saved: Dictionary = before.duplicate(true)
		assert_false(replay.begin("return", example["context"], before, fixture["rules"])["supported"])
		assert_eq(before, saved)
		assert_false(replay.continue_workroom("return", true)["supported"])
	var replay := Replay.new()
	assert_true(replay.begin("return", example["context"], example["before"], fixture["rules"])["supported"])
	assert_false(replay.start_ch002("return", example["ch002_context"])["supported"])
	var work := replay.continue_workroom("return", true)
	for key in ["path", "state", "pending_flag", "vm_active", "vm_pc", "next_task_state"]:
		var context: Dictionary = example["ch002_context"].duplicate(true)
		context.erase(key)
		assert_false(replay.start_ch002("return", context)["supported"])
		assert_eq(replay.continue_workroom("return", false)["after"], work["after"])
		assert_false(replay.finish_ch002("return", true)["supported"])


func test_raw_json_reordered_records_and_visited_branch_preserve_roles() -> void:
	var fixture: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/workroom_return_evidence.json"))
	for example in fixture["cases"]:
		for key in ["before", "expected_after_workroom", "expected_after"]:
			example[key]["participants"].reverse()
		var replay := Replay.new()
		var result := _drive(replay, example, fixture["rules"])
		assert_eq(Roles._integers(result["after"]), Roles._integers(example["expected_after"]))
		if example["visited_override"] != null:
			assert_eq(result["after"]["flags"]["0x7a55f6"], 9.0)
			assert_eq(result["script_requests"], [])
			assert_false(replay.start_ch002("return", {})["supported"])
			assert_false(replay.finish_ch002("return", true)["supported"])


func test_mutating_caller_inputs_after_begin_cannot_change_cached_branch() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var before: Dictionary = example["before"].duplicate(true)
	var context: Dictionary = example["context"].duplicate(true)
	var rules: Dictionary = fixture["rules"].duplicate(true)
	var replay := Replay.new()
	assert_true(replay.begin("return", context, before, rules)["supported"])
	before["flags"]["0x7a4e62"] = 1
	before["participants"].clear()
	context["adv_completed"] = false
	rules.clear()
	var work := replay.continue_workroom("return", true)
	assert_eq(work["requested_state"], 6)
	assert_eq(work["after"], example["expected_after_workroom"])
	assert_false(replay.begin("return", context, before, rules)["supported"])
	assert_true(replay.start_ch002("return", example["ch002_context"])["supported"])
	assert_eq(replay.finish_ch002("return", true)["after"], example["expected_after"])
