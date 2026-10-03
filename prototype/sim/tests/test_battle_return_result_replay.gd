extends "res://sim/tests/test_base.gd"

const Return = preload("res://sim/battle_return.gd")
const Campaign = preload("res://sim/campaign_result_state.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func _fixture(path: String = "res://data/result_transaction_evidence_v2.json") -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(path)))


func _terminal() -> Dictionary:
	return {"frame": 42, "winner": 0, "units": [
		{"battle_index": 0, "character_id": 3, "faction": 0},
		{"battle_index": 1, "character_id": 4, "faction": 0},
		{"battle_index": 2, "character_id": 9, "faction": 0},
		{"battle_index": 3, "character_id": -1, "faction": 1}]}


func _campaign(example: Dictionary, fixture: Dictionary) -> Campaign:
	var campaign := Campaign.new()
	assert_true(campaign.initialize(example["before"], fixture["rules"]))
	return campaign


func _prepare(handoff: Return, round_index: int = 0, state11_complete: bool = true) -> Dictionary:
	# These are separately sourced, DECLARED task/round replay inputs. They are
	# not a same-world/live witness for the local Battle or a full school chain.
	var task: Dictionary = _fixture("res://data/scene5_task_execution_evidence.json")["cases"][0]
	var round_example: Dictionary = _fixture("res://data/battle_round_execution_evidence.json")["cases"][round_index]
	return handoff.prepare_result_replay(task["exit_frame"], task["dispatch_context"],
		round_example["before"], round_example["synthetic_round_table"], state11_complete)


func test_all_six_native_result_paths_publish_through_battle_return_with_explicit_replay_gates() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		var campaign := _campaign(example, fixture)
		var handoff := Return.new()
		assert_true(handoff.accept_terminal_snapshot(_terminal()))
		var gate := _prepare(handoff)
		assert_true(gate["supported"])
		assert_eq(gate["state_requests"], [11, 10, 12])
		assert_true(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
		var result := handoff.finish_result_replay("battle", example["confirmed"], example["mvp_ready"])
		assert_true(result["supported"])
		assert_eq(campaign.read_snapshot(), example["expected_after"])
		assert_eq(result["result"]["requested_state"], example["expected_requested_state"])
		assert_eq(result["result"]["before_week"], example["expected_before_week"])
		assert_false(result["live_witness"])
		assert_false(result["authorizes_persistent_write"])


func test_local_battle_snapshot_alone_then_declared_gate_and_result_use_shared_state() -> void:
	var setup: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/battle_setup.json"))
	# Explicit IDs for the three students, removing the fourth local ally.
	setup["units"].remove_at(3)
	for index in range(3):
		setup["units"][index]["character_id"] = [3, 4, 9][index]
	var battle := Battle.start(setup, 42)
	battle.run_to_finish()
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := _campaign(example, fixture)
	var handoff := Return.new()
	assert_true(handoff.accept_terminal_snapshot(battle.get_terminal_snapshot()))
	assert_false(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
	assert_eq(campaign.revision(), 0)
	assert_true(_prepare(handoff)["supported"])
	assert_true(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
	assert_true(handoff.finish_result_replay("battle", true, true)["supported"])
	assert_eq(campaign.read_snapshot(), example["expected_after"])
	assert_eq(handoff.status(), "result_completed")
	# The role fixture is a declared result input, not derived from these units'
	# damage/HP or a claim that this local battle matches the original world.


func test_winner_and_intermediate112_do_not_open_result_gate_or_write_campaign() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := _campaign(example, fixture)
	var handoff := Return.new()
	assert_true(handoff.accept_terminal_snapshot(_terminal()))
	var script_event: Dictionary = _fixture("res://data/battle_script_signals.json")["signals"][0]
	script_event["source_tick"] = 42
	assert_true(handoff.accept_script_signal(script_event))
	assert_false(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
	assert_false(handoff.finish_result_replay("battle", true, true)["supported"])
	assert_eq(handoff.status(), "pending_task_exit")
	assert_eq(campaign.read_snapshot(), example["before"])
	assert_true(campaign.journal().is_empty())


func test_state11_wait_and_next_round16_never_publish_total_result() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := _campaign(example, fixture)
	var handoff := Return.new()
	assert_true(handoff.accept_terminal_snapshot(_terminal()))
	assert_eq(_prepare(handoff, 0, false)["requested_state"], 11)
	assert_eq(handoff.status(), "pending_state11")
	assert_false(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
	assert_true(_prepare(handoff, 0, true)["supported"])
	var next_handoff := Return.new()
	assert_true(next_handoff.accept_terminal_snapshot(_terminal()))
	assert_eq(_prepare(next_handoff, 1)["state_requests"], [11, 10, 16])
	assert_eq(next_handoff.status(), "pending_next_round")
	assert_false(next_handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
	assert_false(_prepare(next_handoff, 0)["supported"], "不能把已请求下一场的同一输入改成已完成")
	assert_eq(campaign.revision(), 0)


func test_unfinished_task_and_menu_exit_block_result_without_changing_state() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var task := _fixture("res://data/scene5_task_execution_evidence.json")
	var round_example: Dictionary = _fixture("res://data/battle_round_execution_evidence.json")["cases"][0]
	for input in task["cases"]:
		if not input["bounded_stop"] and input["name"] != "menu_exit":
			continue
		var campaign := _campaign(example, fixture)
		var handoff := Return.new()
		assert_true(handoff.accept_terminal_snapshot(_terminal()))
		var result := handoff.prepare_result_replay(input["exit_frame"], input["dispatch_context"],
			round_example["before"], {}, true)
		assert_true(result["supported"])
		assert_eq(result["requested_state"], 1 if input["name"] == "menu_exit" else -1)
		assert_false(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
		assert_eq(campaign.revision(), 0)


func test_gate_types_state12_counts_and_unknown_result_context_reject_then_allow_valid_retry() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var handoff := Return.new()
	assert_true(handoff.accept_terminal_snapshot(_terminal()))
	var task: Dictionary = _fixture("res://data/scene5_task_execution_evidence.json")["cases"][0]
	var round_example: Dictionary = _fixture("res://data/battle_round_execution_evidence.json")["cases"][0]
	var invalid: Dictionary = task["exit_frame"].duplicate(true)
	invalid["transition_function_return"] = 1.5
	assert_false(handoff.prepare_result_replay(invalid, task["dispatch_context"], round_example["before"], {}, true)["supported"])
	assert_true(_prepare(handoff)["supported"])
	for changes in [{"task_state": 10}, {"task_state": 16}, {"current": 0}, {"total": 2}, {"mode": 2}, {"round_ids": [3, 4, 5]}]:
		var campaign := _campaign(example, fixture)
		var context: Dictionary = example["context"].duplicate(true)
		context.merge(changes, true)
		assert_false(handoff.begin_result_replay("battle", context, campaign)["supported"])
		assert_eq(campaign.revision(), 0)
	var campaign := _campaign(example, fixture)
	assert_true(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])


func test_terminal_id_mapping_uses_ids_not_positions_names_or_enemy_template_ids() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for mutate in range(6):
		var terminal := _terminal()
		match mutate:
			0: terminal["units"][0].erase("character_id")
			1: terminal["units"][1]["character_id"] = 3
			2: terminal["units"][0]["character_id"] = 3.5
			3: terminal["units"][1]["battle_index"] = 0
			4: terminal["units"][0]["faction"] = 2
			5:
				terminal["units"][3]["character_id"] = 3 # Enemy template is not an ally record.
				terminal["units"].reverse()
		var campaign := _campaign(example, fixture)
		var handoff := Return.new()
		assert_true(handoff.accept_terminal_snapshot(terminal))
		assert_true(_prepare(handoff)["supported"])
		var result := handoff.begin_result_replay("battle", example["context"], campaign)
		assert_eq(result["supported"], mutate == 5)
		assert_eq(campaign.revision(), 1 if mutate == 5 else 0)


func test_bound_instance_deep_copies_and_duplicate_deliveries_cannot_republish_or_redirect() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][5]
	var campaign := _campaign(example, fixture)
	var handoff := Return.new()
	var terminal := _terminal()
	assert_true(handoff.accept_terminal_snapshot(terminal))
	terminal["units"].clear()
	var gate := _prepare(handoff)
	gate["round_after"]["current"] = 0
	handoff.inputs()["result_replay_gate"]["state_requests"].clear()
	var context: Dictionary = example["context"].duplicate(true)
	assert_true(handoff.begin_result_replay("battle", context, campaign)["supported"])
	context["clock_seed"] += 1
	assert_false(handoff.begin_result_replay("battle", context, campaign)["supported"])
	assert_false(handoff.begin_result_replay("another", example["context"], campaign)["supported"])
	assert_false(handoff.begin_result_replay("battle", example["context"], _campaign(example, fixture))["supported"])
	assert_false(handoff.finish_result_replay("another", true, true)["supported"])
	var complete := handoff.finish_result_replay("battle", true, true)
	complete["campaign_snapshot"]["characters"].clear()
	for delivery in range(3):
		assert_eq(_prepare(handoff)["status"], "duplicate")
		assert_eq(handoff.begin_result_replay("battle", example["context"], campaign)["status"], "duplicate")
		assert_eq(handoff.finish_result_replay("battle", false, false)["status"], "duplicate")
	assert_eq(campaign.read_snapshot(), example["expected_after"])
	assert_eq(campaign.revision(), 2)
	assert_eq(campaign.journal().size(), 3)
	assert_eq(campaign.journal()[0]["source_inputs"]["terminal_snapshot"], _terminal())
	assert_eq(campaign.journal()[0]["source_inputs"]["result_gate"]["state_requests"], [11, 10, 12])


func test_different_battle_cannot_reuse_same_campaign_instance_id_even_with_identical_result_context() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := _campaign(example, fixture)
	var first := Return.new()
	assert_true(first.accept_terminal_snapshot(_terminal()))
	assert_true(_prepare(first)["supported"])
	assert_true(first.begin_result_replay("battle", example["context"], campaign)["supported"])
	assert_true(first.finish_result_replay("battle", true, true)["supported"])
	var next := Return.new()
	var terminal := _terminal()
	terminal["frame"] = 43
	assert_true(next.accept_terminal_snapshot(terminal))
	assert_true(_prepare(next)["supported"])
	assert_false(next.begin_result_replay("battle", example["context"], campaign)["supported"])
	assert_false(next.finish_result_replay("battle", true, true)["supported"])
	assert_eq(campaign.revision(), 2)
	assert_eq(campaign.read_snapshot(), example["expected_after"])
	assert_true(next.begin_result_replay("next_battle", example["context"], campaign)["supported"])
