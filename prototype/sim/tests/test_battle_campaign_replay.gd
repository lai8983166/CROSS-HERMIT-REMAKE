extends "res://sim/tests/test_base.gd"
## Real local Battle facts + explicit, same-CPU native scene5 replay inputs.
## Native end-world predicates/result records are NOT derived from local damage.

const Campaign = preload("res://sim/campaign_result_state.gd")
const Return = preload("res://sim/battle_return.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func _data() -> Dictionary:
	var chain: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/campaign_scene5_evidence.json"))
	var preparation: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/campaign_preparation_evidence.json"))
	chain["rules"]["preparation"] = preparation["rules"]
	return Roles._integers({"chain": chain, "preparation": preparation})


func _battle(ids: Array) -> Battle:
	var setup: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/battle_setup.json"))
	setup["units"].remove_at(3)
	for index in range(3):
		setup["units"][index]["character_id"] = ids[index]
	var battle := Battle.start(setup, 42)
	battle.run_to_finish()
	assert_true(battle.finished)
	assert_true(battle.frame > 0)
	return battle


func _gate(handoff: Return, example: Dictionary) -> Dictionary:
	return handoff.prepare_scene5_result_replay(example["event_world"], example["exit_frame"],
		example["dispatch_context"], example["round_before"], example["round_table"], true)


func test_real_local_battle_terminal_and_both_native_return_inputs_reach_one_owned_school_catalog() -> void:
	var data := _data()
	var first_terminal := _battle([3, 4, 9]).get_terminal_snapshot()
	assert_eq(first_terminal, _battle([3, 4, 9]).get_terminal_snapshot(), "local combat seed is deterministic")
	for index in range(2):
		var example: Dictionary = data["chain"]["cases"][index]
		var prep: Dictionary = data["preparation"]["cases"][index]
		var campaign := Campaign.new()
		assert_true(campaign.initialize(prep["before_world"], data["chain"]["rules"]))
		var handoff := Return.new()
		assert_true(handoff.accept_terminal_snapshot(first_terminal))
		# Actual local winner/HP do not create native condition/result records.
		assert_false(handoff.prepare_tactics_replay("prep", prep["inputs"], campaign)["supported"])
		assert_false(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
		assert_eq(campaign.revision(), 0)
		assert_eq(campaign.read_snapshot(), prep["before_world"])
		var gate := _gate(handoff, example)
		assert_true(gate["supported"])
		assert_eq(gate["state_requests"], [11, 10, 12])
		assert_true(handoff.prepare_tactics_replay("prep", prep["inputs"], campaign)["supported"])
		assert_eq(campaign.read_snapshot(), example["before_result"])
		assert_true(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
		assert_true(handoff.finish_result_replay("battle", true, true)["supported"])
		assert_eq(campaign.read_snapshot(), example["after_result"])
		assert_true(handoff.begin_school_return_replay("school")["supported"])
		assert_eq(campaign.read_snapshot(), example["after_chapter"])
		assert_true(handoff.advance_school_return_replay("school", true, true, true)["school_constructed"])
		assert_eq(campaign.read_snapshot(), example["before_boot"])
		var boot := handoff.project_school_return_boot_replay("school")
		assert_true(boot["school_boot_data_projected"])
		assert_eq(campaign.read_snapshot(), example["expected_after"])
		assert_eq(campaign.read_school_snapshot()["snapshot"], example["expected_school_after"])
		assert_eq(campaign.revision(), 6)
		assert_eq(handoff.status(), "school_boot_data_projected")
		assert_eq(campaign.journal()[0]["source_inputs"]["terminal_snapshot"], first_terminal)
		assert_eq(campaign.journal()[0]["source_inputs"]["tactical_preparation_inputs"]["result_inputs"], example["state11_entry_inputs"])
		assert_eq(campaign.journal().filter(func(row): return row["phase"] == "state7_week").size(), 1)
		for delivery in range(2):
			assert_eq(handoff.prepare_tactics_replay("prep", prep["inputs"], campaign)["status"], "duplicate")
			assert_eq(handoff.finish_result_replay("battle", true, true)["status"], "duplicate")
			assert_eq(handoff.project_school_return_boot_replay("school")["status"], "duplicate")
			assert_eq(campaign.revision(), 6)
			assert_eq(campaign.read_snapshot(), example["expected_after"])
		for key in ["school_initialized", "interactive_school_ready", "live_witness", "authorizes_persistent_write"]:
			assert_false(boot[key])


func test_real_local_battle_with_missing_source_role_cannot_award_or_start_total_result() -> void:
	var data := _data()
	var example: Dictionary = data["chain"]["cases"][0]
	var prep: Dictionary = data["preparation"]["cases"][0]
	var battle := _battle([3, 4, 5])
	var campaign := Campaign.new()
	assert_true(campaign.initialize(prep["before_world"], data["chain"]["rules"]))
	var handoff := Return.new()
	assert_true(handoff.accept_terminal_snapshot(battle.get_terminal_snapshot()))
	assert_true(_gate(handoff, example)["supported"])
	assert_false(handoff.prepare_tactics_replay("prep", prep["inputs"], campaign)["supported"])
	assert_false(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
	assert_eq(campaign.revision(), 0)
	assert_eq(campaign.journal(), [])
	assert_eq(campaign.read_snapshot(), prep["before_world"])
