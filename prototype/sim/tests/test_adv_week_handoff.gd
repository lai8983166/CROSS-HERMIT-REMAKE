extends "res://sim/tests/test_base.gd"

const Join = preload("res://sim/roster_join_replay.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const Start = preload("res://sim/week_start_replay.gd")


func _fixture() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/adv_week_handoff_evidence.json")))


func test_join_and_week_match_three_shared_native_memory_paths() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		var joined := Join.new().apply_once("join", example["join_context"], example["before"], fixture["rules"])
		assert_true(joined["supported"])
		if not joined["supported"]:
			continue
		assert_eq(joined["after"], example["expected_after_adv"])
		var replay := Start.new()
		# This fixture's completion is sourced from real Chapter021 END and
		# native request7 in the SAME CPU, rather than a synthetic boolean.
		var week := replay.begin("week", example["week_context"], joined["after"], fixture["rules"]["week"])
		assert_true(week["supported"])
		if not week["supported"]:
			continue
		assert_eq(week["week_executed"], example["expected_week_executed"])
		assert_eq(week["after"], example["expected_after_week"])
		if example["expected_week_executed"]:
			assert_eq(example["native_adv_state_requests"], [{"va": "0x439e30", "state": 7}])
			assert_eq(example["native_consumed_request"]["adv_active"], 0)
			var result := replay.finish("week", example["week_fade_ready"])
			assert_eq(result["script_requests"], example["expected_script_requests"])
			assert_eq(result["after"], example["expected_after_week"])
			assert_eq(result["requested_state"], 6 if example["week_fade_ready"] else 7)
		else:
			assert_eq(week["status"], "waiting_adv")
			assert_eq(example["native_adv_state_requests"], [])
			assert_false(replay.finish("week", true)["supported"])
		assert_false(week["school_initialized"])
		assert_false(week["authorizes_persistent_write"])


func test_joint_native_snapshots_survive_raw_json_reordered_ids_and_duplicate_delivery() -> void:
	var fixture: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/adv_week_handoff_evidence.json"))
	var example: Dictionary = fixture["cases"][0]
	for key in ["before", "expected_after_adv", "expected_after_week"]:
		example[key]["participants"].reverse()
	var join := Join.new()
	var first := join.apply_once("join", example["join_context"], example["before"], fixture["rules"])
	assert_true(first["supported"])
	if not first["supported"]:
		return
	assert_eq(Roles._integers(first["after"]), Roles._integers(example["expected_after_adv"]))
	var replay := Start.new()
	var week := replay.begin("week", example["week_context"], first["after"], fixture["rules"]["week"])
	assert_true(week["supported"])
	if not week["supported"]:
		return
	var complete := replay.finish("week", true)
	assert_eq(Roles._integers(complete["after"]), Roles._integers(example["expected_after_week"]))
	for tick in range(3):
		assert_eq(join.apply_once("join", example["join_context"], example["before"], fixture["rules"])["after"], first["after"])
		assert_eq(replay.begin("week", example["week_context"], first["after"], fixture["rules"]["week"])["after"], complete["after"])
		assert_eq(replay.finish("week", false)["after"], complete["after"])
	assert_eq(complete["after"]["student_count"], 4)
	assert_eq([complete["after"]["month"], complete["after"]["week"]], [5, 1])
	assert_false(complete["school_initialized"])


func test_real_adv_completion_does_not_override_missing_joined_role_or_cache_conflicts() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var missing: Dictionary = example["expected_after_adv"].duplicate(true)
	missing["participants"].remove_at(2)
	var replay := Start.new()
	assert_false(replay.begin("week", example["week_context"], missing, fixture["rules"]["week"])["supported"])
	assert_false(replay.finish("week", true)["supported"])
	assert_true(replay.begin("week", example["week_context"], example["expected_after_adv"], fixture["rules"]["week"])["supported"])
	var complete := replay.finish("week", true)
	assert_false(replay.begin("week", {"task_state": 7, "adv_completed": false}, example["expected_after_adv"], fixture["rules"]["week"])["supported"])
	assert_eq(replay.finish("week", false)["after"], complete["after"])
	assert_eq(complete["after"], example["expected_after_week"])
	assert_eq(complete["script_requests"], example["expected_script_requests"])
