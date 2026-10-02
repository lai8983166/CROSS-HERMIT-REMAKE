extends "res://sim/tests/test_base.gd"

const Entry = preload("res://sim/school_entry_replay.gd")
const Return = preload("res://sim/workroom_return_replay.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func _fixture() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_dispatch_evidence.json")))


func test_native_first_visited_and_wait_cases_match_full_snapshots_and_both_descriptors() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		var result := Entry.new().dispatch_once("school", example["context"], example["before"], fixture["rules"])
		assert_eq(result["supported"], example["expected_supported"])
		if result["supported"]:
			assert_eq(result["after"], example["expected_after"])
			assert_eq(result["tasks"], example["expected_tasks"])
			assert_eq(result["pending_flag"], example["expected_pending_flag"])
			assert_eq(result["pending_state"], example["expected_pending_state"])
			assert_false(result["week_executed"])
		assert_false(result["school_initialized"])
		assert_false(result["live_witness"])
		assert_false(result["authorizes_persistent_write"])


func test_workroom_and_ch002_handoff_dispatch_only_after_actual_fixture_request9() -> void:
	var fixture := _fixture()
	var work: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/workroom_return_evidence.json")))
	# The two fixtures are separate exports of the SAME native CPU chain.
	for index in range(4):
		var example: Dictionary = work["cases"][[0,2,1,3][index]]
		var replay := Return.new()
		assert_true(replay.begin("return", example["context"], example["before"], work["rules"])["supported"])
		var result := replay.continue_workroom("return", example["continue_ready"])
		if example["ch002_context"] != null:
			assert_true(replay.start_ch002("return", example["ch002_context"])["supported"])
			result = replay.finish_ch002("return", example["ch002_end_ready"])
		var context: Dictionary = fixture["cases"][index]["context"].duplicate(true)
		context["task_state"] = result["requested_state"]
		context["pending_flag"] = result["pending_flag"]
		var dispatched := Entry.new().dispatch_once("school", context, result["after"], fixture["rules"])
		assert_eq(dispatched["supported"], fixture["cases"][index]["expected_supported"])
		if dispatched["supported"]:
			assert_eq(dispatched["after"], fixture["cases"][index]["expected_after"])
			assert_eq(dispatched["tasks"].size(), 2)


func test_duplicate_delivery_and_mutation_cannot_repeat_tasks_or_change_roles() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var replay := Entry.new()
	var context: Dictionary = example["context"].duplicate(true)
	var before: Dictionary = example["before"].duplicate(true)
	var first := replay.dispatch_once("school", context, before, fixture["rules"])
	first["tasks"].clear()
	first["after"]["participants"].clear()
	context["task_state"] = 8
	before["flags"]["0x7a4e62"] = 0
	assert_false(replay.dispatch_once("school", context, before, fixture["rules"])["supported"])
	for tick in range(3):
		var duplicate := replay.dispatch_once("school", example["context"], example["before"], fixture["rules"])
		assert_eq(duplicate["status"], "duplicate")
		assert_eq(duplicate["tasks"], example["expected_tasks"])
		assert_eq(duplicate["after"], example["expected_after"])


func test_incomplete_request_active_adv_and_missing_role_reject_before_instance() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for pair in [["task_state", 8], ["pending_flag", 0], ["adv_active", 1],
			["adv_active", false], ["source_request_va", "winner"]]:
		var replay := Entry.new()
		var context: Dictionary = example["context"].duplicate(true)
		context[pair[0]] = pair[1]
		assert_false(replay.dispatch_once("school", context, example["before"], fixture["rules"])["supported"])
		assert_true(replay.dispatch_once("school", example["context"], example["before"], fixture["rules"])["supported"])
	var missing: Dictionary = example["before"].duplicate(true)
	missing["participants"].remove_at(3)
	var replay := Entry.new()
	assert_false(replay.dispatch_once("school", example["context"], missing, fixture["rules"])["supported"])
	assert_eq(missing["participants"].size(), 3)
	assert_true(replay.dispatch_once("school", example["context"], example["before"], fixture["rules"])["supported"])


func test_raw_json_and_reordered_role_ids_do_not_change_dispatch() -> void:
	var fixture: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/school_dispatch_evidence.json"))
	for example in fixture["cases"].slice(0,2):
		example["before"]["participants"].reverse()
		example["expected_after"]["participants"].reverse()
		var result := Entry.new().dispatch_once("school", example["context"], example["before"], fixture["rules"])
		assert_true(result["supported"])
		assert_eq(result["after"], example["expected_after"])
		assert_eq(Roles._integers(result["tasks"]), Roles._integers(example["expected_tasks"]))
