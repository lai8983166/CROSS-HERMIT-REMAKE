extends "res://sim/tests/test_base.gd"

const Start = preload("res://sim/week_start_replay.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const Transaction = preload("res://sim/result_transaction_replay.gd")


func _fixture() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/week_start_evidence.json")))


func test_three_native_task_paths_match_whole_week_and_script_requests() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		var replay := Start.new()
		var result := replay.begin(example["name"], example["context"], example["before"], fixture["rules"])
		assert_true(result["supported"])
		if not result["supported"]:
			continue
		assert_eq(result["after"], example["expected_after"])
		result = replay.finish(example["name"], example["fade_ready"])
		assert_eq(result["after"], example["expected_after"])
		assert_eq(result["requested_state"], example["expected_requested_state"])
		assert_eq(result["script_requests"], example["expected_script_requests"])
		assert_eq(result["fade_frames"], 90)
		assert_false(result["school_initialized"])
		assert_false(result["live_witness"])
		assert_false(result["authorizes_persistent_write"])


func test_busy_fade_does_not_reapply_week_and_resume_requests_ch001_once() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][1]
	var replay := Start.new()
	assert_true(replay.begin("wait", example["context"], example["before"], fixture["rules"])["supported"])
	for tick in range(5):
		var result := replay.finish("wait", false)
		assert_eq(result["status"], "waiting_fade")
		assert_eq(result["after"], example["expected_after"])
		assert_eq(result["script_requests"], [])
		assert_eq(result["phase_log"].size(), 1)
	var complete := replay.finish("wait", true)
	assert_eq(complete["script_requests"], example["expected_script_requests"])
	assert_eq(complete["phase_log"].size(), 2)
	for tick in range(3):
		assert_eq(replay.finish("wait", false)["after"], example["expected_after"])
		assert_eq(replay.begin("wait", example["context"], example["before"], fixture["rules"])["phase_log"].size(), 2)


func test_missing_adv_completion_and_wrong_states_cannot_advance_calendar() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][1]
	for context in [{"task_state": 6, "adv_completed": true}, {"task_state": 12, "adv_completed": true},
			{"task_state": 18, "adv_completed": true}, {"task_state": 7}, {"task_state": 7, "adv_completed": 1}]:
		var replay := Start.new()
		assert_false(replay.begin("bad", context, example["before"], fixture["rules"])["supported"])
		assert_false(replay.finish("bad", true)["supported"])
	var replay := Start.new()
	var result := replay.begin("pending", {"task_state": 7, "adv_completed": false}, example["before"], fixture["rules"])
	assert_eq(result["status"], "waiting_adv")
	assert_eq(result["after"], example["before"])
	assert_false(result["week_executed"])
	assert_false(replay.finish("pending", true)["supported"])


func test_invalid_whole_week_data_leaves_no_confirmable_instance() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][1]
	for kind in range(5):
		var before: Dictionary = example["before"].duplicate(true)
		match kind:
			0: before["participants"][0].erase("unlock_flags")
			1: before["availability"][5] = 1
			2: before["month"] = 15
			3: before["participants"][1]["character_id"] = 3
			4: before["item_flags"].pop_back()
		var saved := before.duplicate(true)
		var replay := Start.new()
		assert_false(replay.begin("bad", example["context"], before, fixture["rules"])["supported"])
		assert_false(replay.finish("bad", true)["supported"])
		assert_eq(before, saved)


func test_completed_output_is_deeply_copied_and_changed_input_is_rejected() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][1]
	var replay := Start.new()
	var initial := replay.begin("once", example["context"], example["before"], fixture["rules"])
	initial["after"]["week"] = 4
	var complete := replay.finish("once", true)
	complete["phase_log"].clear()
	complete["script_requests"][0]["next_task_state"] = 18
	complete["after"]["item_flags"][0] = 0
	var cached := replay.finish("once", true)
	assert_eq(cached["after"], example["expected_after"])
	assert_eq(cached["script_requests"], example["expected_script_requests"])
	assert_eq(cached["phase_log"].size(), 2)
	var changed: Dictionary = example["before"].duplicate(true)
	changed["week"] = 4
	assert_false(replay.begin("once", example["context"], changed, fixture["rules"])["supported"])
	assert_false(replay.begin("once", {"task_state": 7, "adv_completed": false},
		example["before"], fixture["rules"])["supported"], "修改完成输入不能把已推进实例显示为未推进")
	assert_eq(replay.finish("once", false)["after"], example["expected_after"])


func test_reordered_characters_and_raw_json_equipment_match_native_owners() -> void:
	var fixture: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/week_start_evidence.json"))
	var example: Dictionary = fixture["cases"][1]
	example["before"]["participants"].reverse()
	example["expected_after"]["participants"].reverse()
	var replay := Start.new()
	var result := replay.begin("ids", example["context"], example["before"], fixture["rules"])
	assert_true(result["supported"])
	if result["supported"]:
		assert_eq(Roles._integers(result["after"]), Roles._integers(example["expected_after"]))


func test_ordinary_result_then_declared_adv_completion_advances_without_double_role_fields() -> void:
	var fixture: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/result_transaction_evidence_v2.json")))
	var example: Dictionary = fixture["cases"][0]
	var transaction := Transaction.new()
	assert_true(transaction.begin("result", example["context"], example["before"], fixture["rules"])["supported"])
	var result := transaction.finish("result", true, true)
	assert_eq(result["after"]["month"], 4)
	assert_eq(result["after"]["week"], 5)
	assert_false(result["week_executed"])
	assert_eq(result["school_script_requests"][0]["next_task_state"], 7)
	var before: Dictionary = result["after"].duplicate(true)
	before["participants"] = before["characters"]
	before.erase("characters")
	var start := Start.new()
	var next := start.begin("start", {"task_state": 7, "adv_completed": true}, before, fixture["rules"]["week"])
	assert_true(next["supported"], "此处ADV完成是合成输入，不宣称剧情已执行")
	if not next["supported"]:
		return
	assert_eq([next["after"]["month"], next["after"]["week"]], [5, 1])
	for index in range(before["participants"].size()):
		for key in ["growth_pools", "recipient_count", "week_records", "job_progress"]:
			assert_eq(next["after"]["participants"][index][key], before["participants"][index][key])
	assert_eq(next["after"]["relationships"], before["relationships"])
	assert_false(next["school_initialized"])
