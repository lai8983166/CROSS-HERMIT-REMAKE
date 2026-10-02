extends "res://sim/tests/test_base.gd"

const Boot = preload("res://sim/school_boot_replay.gd")
const Entry = preload("res://sim/school_entry_replay.gd")
const Return = preload("res://sim/workroom_return_replay.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func _fixture() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_boot_evidence.json")))


func test_native_first_visited_and_ch002_wait_match_entire_captured_snapshots() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		var result := Boot.new().initialize_once("boot", example["context"], example["before"], fixture["role_rules"], fixture["boot_rules"])
		assert_eq(result["supported"], example["expected_supported"])
		if result["supported"]:
			assert_eq(result["after"], example["expected_after"])
			assert_eq(result["after"]["school_control"]["idle_student_ids"], [3, 5, 4, 9])
			assert_eq(result["after"]["school_control"]["adventure_entries"], [[], [], [[1, 1, 8, 5, 0]]])
			assert_false(result["week_executed"])
		assert_false(result["school_initialized"])
		assert_false(result["interactive_school_ready"])
		assert_false(result["live_witness"])
		assert_false(result["authorizes_persistent_write"])


func test_workroom_ch002_dispatch_and_boot_use_the_same_role_calendar_snapshot() -> void:
	var fixture := _fixture()
	var dispatch: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/school_dispatch_evidence.json")))
	var work: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/workroom_return_evidence.json")))
	for pair in [[0, 0, 0], [1, 1, 2], [2, 3, 3]]:
		var example: Dictionary = fixture["cases"][pair[0]]
		var work_example: Dictionary = work["cases"][pair[2]]
		var work_replay := Return.new()
		assert_true(work_replay.begin("return", work_example["context"], work_example["before"], work["rules"])["supported"])
		var returned := work_replay.continue_workroom("return", work_example["continue_ready"])
		if work_example["ch002_context"] != null:
			assert_true(work_replay.start_ch002("return", work_example["ch002_context"])["supported"])
			returned = work_replay.finish_ch002("return", work_example["ch002_end_ready"])
		var dispatch_context: Dictionary = dispatch["cases"][pair[1]]["context"].duplicate(true)
		dispatch_context["task_state"] = returned["requested_state"]
		dispatch_context["pending_flag"] = returned["pending_flag"]
		var dispatched := Entry.new().dispatch_once("school", dispatch_context, returned["after"], dispatch["rules"])
		var context := {"school_constructed": dispatched["school_constructed"], "task_state": returned["requested_state"],
			"pending_flag": returned["pending_flag"], "tasks": []}
		var before: Dictionary = returned["after"].duplicate(true)
		if dispatched["supported"]:
			context["pending_flag"] = dispatched["pending_flag"]
			context["tasks"] = dispatched["tasks"]
			before = dispatched["after"]
		# Fresh constructor controls are a declared input, separate from role state.
		before["school_control"] = example["before"]["school_control"].duplicate(true)
		assert_eq(before, example["before"])
		assert_eq(context, example["context"])
		var booted := Boot.new().initialize_once("boot", context, before, fixture["role_rules"], fixture["boot_rules"])
		assert_eq(booted["supported"], example["expected_supported"])
		if booted["supported"]:
			assert_eq(booted["after"], example["expected_after"])


func test_raw_json_and_reordered_records_use_stable_ids_and_roster_rank_order() -> void:
	var fixture: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/school_boot_evidence.json"))
	for example in fixture["cases"].slice(0, 2):
		example["before"]["participants"].reverse()
		example["expected_after"]["participants"].reverse()
		var result := Boot.new().initialize_once("boot", example["context"], example["before"], fixture["role_rules"], fixture["boot_rules"])
		assert_true(result["supported"])
		# Compare integral source values across JSON's float representation, while
		# separately requiring untouched records to retain their input types/data.
		assert_eq(Roles._integers(result["after"]), Roles._integers(example["expected_after"]))
		assert_eq(result["after"]["participants"], example["before"]["participants"])


func test_same_instance_duplicate_conflict_and_nested_mutations_preserve_cached_projection() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var replay := Boot.new()
	var before: Dictionary = example["before"].duplicate(true)
	var rules: Dictionary = fixture["boot_rules"].duplicate(true)
	var first := replay.initialize_once("boot", example["context"], before, fixture["role_rules"], rules)
	assert_true(first["supported"])
	first["after"]["school_control"]["lecture_unlock_flags"].clear()
	first["after"]["participants"].clear()
	before["participants"][0]["level_50"] += 1
	rules["adventures"][7]["duration"] += 1
	assert_false(replay.initialize_once("boot", example["context"], before, fixture["role_rules"], rules)["supported"])
	for delivery in range(3):
		var duplicate := replay.initialize_once("boot", example["context"], example["before"], fixture["role_rules"], fixture["boot_rules"])
		assert_eq(duplicate["status"], "duplicate")
		assert_eq(duplicate["after"], example["expected_after"])


func test_missing_task_wrong_descriptor_and_unconsumed_request_reject_before_cache() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for key in ["school_constructed", "tasks", "task_state", "pending_flag"]:
		var context: Dictionary = example["context"].duplicate(true)
		context.erase(key)
		_assert_rejected_then_valid(context, example["before"], fixture["boot_rules"], fixture)
	for pair in [["task_state", 8], ["pending_flag", 1], ["school_constructed", 1]]:
		var context: Dictionary = example["context"].duplicate(true)
		context[pair[0]] = pair[1]
		_assert_rejected_then_valid(context, example["before"], fixture["boot_rules"], fixture)
	for mutate in range(4):
		var context: Dictionary = example["context"].duplicate(true)
		if mutate == 0:
			context["tasks"].remove_at(1)
		elif mutate == 1:
			context["tasks"].reverse()
		elif mutate == 2:
			context["tasks"][1]["vtable"] = "0x5a0a40"
		else:
			context["tasks"][1]["active"] = 1.5
		_assert_rejected_then_valid(context, example["before"], fixture["boot_rules"], fixture)


func test_fractional_opaque_metadata_is_preserved_and_input_and_output_cannot_alias() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var before: Dictionary = example["before"].duplicate(true)
	before["presentation"] = {"zoom": 1.25}
	before["participants"][0]["presentation"] = {"opacity": 0.75}
	before["school_control"]["presentation"] = {"scroll": 2.5}
	var original: Dictionary = before.duplicate(true)
	var replay := Boot.new()
	var result := replay.initialize_once("boot", example["context"], before, fixture["role_rules"], fixture["boot_rules"])
	assert_true(result["supported"])
	assert_eq(before, original)
	assert_eq(result["after"]["presentation"]["zoom"], 1.25)
	assert_eq(result["after"]["participants"], before["participants"])
	assert_eq(result["after"]["school_control"]["presentation"]["scroll"], 2.5)
	result["after"]["presentation"]["zoom"] = 4.5
	before["participants"][0]["presentation"]["opacity"] = 1.0
	var duplicate := replay.initialize_once("boot", example["context"], original, fixture["role_rules"], fixture["boot_rules"])
	assert_eq(duplicate["after"]["presentation"]["zoom"], 1.25)
	assert_eq(duplicate["after"]["participants"][0]["presentation"]["opacity"], 0.75)


func test_incomplete_roster_stale_controls_and_inconsistent_class_bytes_reject_atomically() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for mutate in range(11):
		var before: Dictionary = example["before"].duplicate(true)
		match mutate:
			0: before["participants"].remove_at(0)
			1: before["participants"][0].erase("level_50")
			2: before["student_ids"][1] = 3
			3: before["teacher_count"] = 1
			4: before["school_control"]["adventure_unlock_flags"][7] = 1
			5: before["school_control"]["adventure_entries"][2] = [[1, 1, 8, 5, 0]]
			6: before["school_control"]["group_raw_bytes"][16] = 4
			7: before["group_student_indices"][0][0] = 1
			8: before["school_control"]["group_raw_bytes"][0] = 101
			9: before["school_control"]["group_rankings"].remove_at(0)
			10: before["month"] = 6
		_assert_rejected_then_valid(example["context"], before, fixture["boot_rules"], fixture)


func test_template_counts_ids_signed_domains_and_role_rules_are_validated_before_cache() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for mutate in range(6):
		var rules: Dictionary = fixture["boot_rules"].duplicate(true)
		match mutate:
			0: rules["adventures"].remove_at(0)
			1: rules["lectures"][0]["id"] = 2
			2: rules["adventures"][7]["subkind"] = 128
			3: rules["lectures"][0]["kind"] = 32768
			4: rules["adventures"][7]["gate"] = true
			5: rules["lectures"][0].erase("week")
		_assert_rejected_then_valid(example["context"], example["before"], rules, fixture)
	var replay := Boot.new()
	assert_false(replay.initialize_once("boot", example["context"], example["before"], {}, fixture["boot_rules"])["supported"])
	assert_true(replay.initialize_once("boot", example["context"], example["before"], fixture["role_rules"], fixture["boot_rules"])["supported"])


func _assert_rejected_then_valid(context: Dictionary, before: Dictionary, rules: Dictionary, fixture: Dictionary) -> void:
	var replay := Boot.new()
	var original: Dictionary = before.duplicate(true)
	assert_false(replay.initialize_once("boot", context, before, fixture["role_rules"], rules)["supported"])
	assert_eq(before, original)
	var example: Dictionary = fixture["cases"][0]
	assert_true(replay.initialize_once("boot", example["context"], example["before"], fixture["role_rules"], fixture["boot_rules"])["supported"])
