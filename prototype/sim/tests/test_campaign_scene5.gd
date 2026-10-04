extends "res://sim/tests/test_base.gd"

const Campaign = preload("res://sim/campaign_result_state.gd")
const Return = preload("res://sim/battle_return.gd")
const Selection = preload("res://sim/scene5_condition_selection.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func _fixture(raw := false) -> Dictionary:
	var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/campaign_scene5_evidence.json"))
	return data if raw else Roles._integers(data)


func _handoff(example: Dictionary) -> Return:
	var handoff := Return.new()
	# This is a declared caller terminal fact, not a native tactical simulation.
	assert_true(handoff.accept_terminal_snapshot(example["declared_terminal_snapshot"]))
	return handoff


func _prepare(handoff: Return, example: Dictionary, ready := true) -> Dictionary:
	return handoff.prepare_scene5_result_replay(example["event_world"], example["exit_frame"],
		example["dispatch_context"], example["round_before"], example["round_table"], ready)


func test_both_native_condition_task_result_and_school_paths_share_the_actual_case_inputs() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		var selected := Selection.select(example["event_world"])
		assert_true(selected["supported"])
		assert_eq(selected["selector_arg"], example["expected_selector"])
		assert_eq(selected["script_sub"], example["expected_sub"])
		assert_eq(selected["tactical_result_selector"], example["expected_task_result_selector"])
		assert_eq(selected["round_grade_index"], example["context"]["round_grade"])
		var handoff := _handoff(example)
		var gate := _prepare(handoff, example)
		assert_true(gate["supported"])
		assert_eq(gate["state_requests"], [11, 10, 12])
		assert_true(gate["round_after"] == example["round_after"])
		var campaign := Campaign.new()
		assert_true(campaign.initialize(example["before_result"], fixture["rules"]))
		assert_true(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
		assert_true(handoff.finish_result_replay("battle", true, true)["supported"])
		assert_true(campaign.read_snapshot() == example["after_result"], example["name"] + " native result")
		assert_true(handoff.begin_school_return_replay("school")["supported"])
		assert_true(campaign.read_snapshot() == example["after_chapter"])
		assert_true(handoff.advance_school_return_replay("school", true, true, true)["school_constructed"])
		assert_true(campaign.read_snapshot() == example["before_boot"])
		var projected := handoff.project_school_return_boot_replay("school")
		assert_true(projected["school_boot_data_projected"])
		assert_true(campaign.read_snapshot() == example["expected_after"])
		assert_true(campaign.read_school_snapshot()["snapshot"] == example["expected_school_after"])
		assert_eq(campaign.revision(), 5)
		assert_eq(handoff.status(), "school_boot_data_projected")
		assert_eq(campaign.journal()[0]["source_inputs"]["result_gate"]["scene5_condition_selection"]["declared_event_world"], example["event_world"])
		for key in ["school_initialized", "interactive_school_ready", "live_witness", "authorizes_persistent_write"]:
			assert_false(projected[key])
		assert_eq(campaign.journal().filter(func(row): return row["phase"] == "state7_week").size(), 1)
		for delivery in range(2):
			assert_eq(_prepare(handoff, example)["status"], "duplicate")
			assert_eq(handoff.finish_result_replay("battle", true, true)["status"], "duplicate")
			assert_eq(handoff.project_school_return_boot_replay("school")["status"], "duplicate")
			assert_eq(campaign.revision(), 5)
			assert_true(campaign.read_snapshot() == example["expected_after"])


func test_bad_condition_fields_reject_before_gate_creation_and_good_retry_succeeds() -> void:
	var example: Dictionary = _fixture()["cases"][0]
	for kind in range(10):
		var world: Dictionary = example["event_world"].duplicate(true)
		match kind:
			0: world["scene_id"] = 6
			1: world["own_side"] = 1
			2: world["field_2e6f4"] = 1
			3: world["event_bit3_0_word"] = 0.5
			4: world["event_bit3_0_word"] = 1
			5: world["units"][0]["side_a4"] = 0
			6: world["units"][1]["field_f"] = 1
			7: world["units"][0]["wrapper_index"] = 3
			8: world["units"][1]["enemy_number"] = 3
			9: world["units"][1]["character_id"] = 49
		var handoff := _handoff(example)
		assert_false(handoff.prepare_scene5_result_replay(world, example["exit_frame"], example["dispatch_context"],
			example["round_before"], example["round_table"], true)["supported"])
		assert_false(handoff.inputs().has("result_replay_gate"))
		assert_eq(handoff.status(), "pending_task_exit")
		assert_true(_prepare(handoff, example)["supported"])


func test_cross_case_task_selector_or_result_grade_cannot_write_the_shared_campaign() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var other: Dictionary = fixture["cases"][1]
	var handoff := _handoff(example)
	assert_false(handoff.prepare_scene5_result_replay(other["event_world"], example["exit_frame"], example["dispatch_context"],
		example["round_before"], example["round_table"], true)["supported"])
	assert_true(_prepare(handoff, example)["supported"])
	var campaign := Campaign.new()
	assert_true(campaign.initialize(example["before_result"], fixture["rules"]))
	for grade in [2, -1, 3.5]:
		var context: Dictionary = example["context"].duplicate(true)
		context["round_grade"] = grade
		assert_false(handoff.begin_result_replay("battle", context, campaign)["supported"])
		assert_eq(campaign.revision(), 0)
		assert_true(campaign.read_snapshot() == example["before_result"])
	assert_true(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])


func test_condition_binding_cannot_be_replaced_or_added_after_generic_gate_creation() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var handoff := _handoff(example)
	assert_true(_prepare(handoff, example)["supported"])
	assert_false(_prepare(handoff, fixture["cases"][1])["supported"])
	assert_eq(_prepare(handoff, example)["status"], "duplicate")
	var generic := _handoff(example)
	assert_true(generic.prepare_result_replay(example["exit_frame"], example["dispatch_context"],
		example["round_before"], example["round_table"], true)["supported"])
	assert_false(_prepare(generic, example)["supported"])
	assert_false(generic.inputs()["result_replay_gate"].has("scene5_condition_selection"))


func test_waiting_state11_requires_completion_before_result_and_can_retry_same_condition() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := Campaign.new()
	assert_true(campaign.initialize(example["before_result"], fixture["rules"]))
	var handoff := _handoff(example)
	assert_eq(_prepare(handoff, example, false)["status"], "pending_state11")
	assert_false(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
	assert_eq(campaign.revision(), 0)
	assert_true(_prepare(handoff, example, true)["supported"])
	assert_true(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])


func test_raw_json_and_reordered_event_units_freeze_nested_condition_source_inputs() -> void:
	var fixture := _fixture(true)
	var example: Dictionary = fixture["cases"][0].duplicate(true)
	example["event_world"]["units"].reverse()
	example["event_world"]["presentation"] = {"zoom": 1.25}
	var before: Dictionary = example["event_world"].duplicate(true)
	var handoff := _handoff(example)
	var gate := _prepare(handoff, example)
	assert_true(gate["supported"])
	example["event_world"]["units"].clear()
	gate["scene5_condition_selection"]["declared_event_world"]["units"].clear()
	handoff.inputs()["result_replay_gate"]["scene5_condition_selection"].clear()
	var campaign := Campaign.new()
	assert_true(campaign.initialize(example["before_result"], fixture["rules"]))
	assert_true(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
	assert_true(handoff.finish_result_replay("battle", true, true)["supported"])
	assert_true(Roles._integers(campaign.read_snapshot()) == Roles._integers(example["after_result"]))
	var source: Dictionary = campaign.journal()[0]["source_inputs"]["result_gate"]["scene5_condition_selection"]["declared_event_world"]
	assert_eq(source, before)
	assert_eq(source["presentation"]["zoom"], 1.25)


func test_local_winner_does_not_choose_the_native_event_branch() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		for winner in [0, 1]:
			var terminal: Dictionary = example["declared_terminal_snapshot"].duplicate(true)
			terminal["winner"] = winner
			var handoff := Return.new()
			assert_true(handoff.accept_terminal_snapshot(terminal))
			var gate := _prepare(handoff, example)
			assert_true(gate["supported"])
			assert_eq(gate["scene5_condition_selection"]["script_sub"], example["expected_sub"])
