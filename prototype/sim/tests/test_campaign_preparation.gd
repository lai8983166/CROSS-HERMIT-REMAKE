extends "res://sim/tests/test_base.gd"

const Campaign = preload("res://sim/campaign_result_state.gd")
const Return = preload("res://sim/battle_return.gd")
const Preparation = preload("res://sim/campaign_tactics_preparation.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func _data(raw := false) -> Dictionary:
	var preparation: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/campaign_preparation_evidence.json"))
	var chain: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/campaign_scene5_evidence.json"))
	chain["rules"]["preparation"] = preparation["rules"]
	var result := {"preparation": preparation, "chain": chain, "rules": chain["rules"]}
	return result if raw else Roles._integers(result)


func _handoff(example: Dictionary, ready := true) -> Return:
	var handoff := Return.new()
	assert_true(handoff.accept_terminal_snapshot(example["declared_terminal_snapshot"]))
	assert_true(handoff.prepare_scene5_result_replay(example["event_world"], example["exit_frame"],
		example["dispatch_context"], example["round_before"], example["round_table"], ready)["supported"])
	return handoff


func test_full_owned_preparation_result_and_school_match_both_continuous_native_worlds() -> void:
	var data := _data()
	for index in range(2):
		var example: Dictionary = data["chain"]["cases"][index]
		var prep: Dictionary = data["preparation"]["cases"][index]
		var campaign := Campaign.new()
		assert_true(campaign.initialize(prep["before_world"], data["rules"]))
		var handoff := _handoff(example)
		var result := handoff.prepare_tactics_replay("preparation", prep["inputs"], campaign)
		assert_true(result["supported"])
		if not result["supported"]:
			_fail(str(result))
			continue
		assert_true(campaign.read_snapshot() == prep["expected_after"], prep["name"] + " native full preparation")
		assert_true(campaign.read_snapshot() == example["before_result"])
		for key in ["grade_index", "time_display", "unit_display", "total_delta", "total_after"]:
			assert_eq(result["result"]["summary"][key], prep["expected_summary"][key], key)
		assert_eq(result["result"]["summary"]["task_grade"], prep["expected_task_grade"])
		assert_eq(result["result"]["loot_groups"], prep["expected_summary"]["loot_groups"])
		assert_eq(result["result"]["loot_rand_state"], prep["expected_loot_rand_state"])
		assert_eq(campaign.revision(), 1)
		assert_eq(handoff.status(), "tactical_result_prepared")
		assert_true(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
		assert_true(handoff.finish_result_replay("battle", true, true)["supported"])
		assert_true(campaign.read_snapshot() == example["after_result"])
		assert_true(handoff.begin_school_return_replay("school")["supported"])
		assert_true(campaign.read_snapshot() == example["after_chapter"])
		assert_true(handoff.advance_school_return_replay("school", true, true, true)["school_constructed"])
		assert_true(campaign.read_snapshot() == example["before_boot"])
		assert_true(handoff.project_school_return_boot_replay("school")["school_boot_data_projected"])
		assert_true(campaign.read_snapshot() == example["expected_after"])
		assert_eq(campaign.read_school_snapshot()["snapshot"], example["expected_school_after"])
		assert_eq(campaign.revision(), 6)
		var log := campaign.journal()
		assert_eq(log[0]["phase"], "tactical_grade_preparation")
		assert_eq(log[1]["phase"], "tactical_loot_preparation")
		assert_eq(log[2]["phase"], "tactical_score_preparation")
		assert_eq(log[0]["before"], prep["before_world"])
		assert_eq(log[0]["after"], log[1]["before"])
		assert_eq(log[1]["after"], log[2]["before"])
		assert_eq(log[2]["after"], example["before_result"])
		assert_eq(log.filter(func(row): return row["phase"] == "state7_week").size(), 1)
		assert_eq(log[0]["source_inputs"]["result_gate"]["scene5_condition_selection"]["declared_event_world"], example["event_world"])
		assert_eq(log[0]["source_inputs"]["tactical_preparation_inputs"], prep["inputs"])
		assert_eq(log[3]["source_inputs"]["tactical_preparation_parent"]["instance_id"], "preparation")
		assert_eq(log[3]["source_inputs"]["tactical_preparation_parent"]["revision"], 1)
		assert_eq(log[3]["source_inputs"]["tactical_preparation_parent"]["inputs"], prep["inputs"])
		for delivery in range(2):
			assert_eq(handoff.prepare_tactics_replay("preparation", prep["inputs"], campaign)["status"], "duplicate")
			assert_eq(handoff.begin_result_replay("battle", example["context"], campaign)["status"], "duplicate")
			assert_eq(handoff.finish_result_replay("battle", true, true)["status"], "duplicate")
			assert_eq(handoff.status(), "school_boot_data_projected")
			assert_eq(campaign.revision(), 6)
			assert_eq(campaign.read_snapshot(), example["expected_after"])


func test_preparation_uses_owned_skill_status_job_and_pool_instead_of_static_templates() -> void:
	var data := _data()
	var prep: Dictionary = data["preparation"]["cases"][0]
	var before: Dictionary = prep["before_world"].duplicate(true)
	var record: Dictionary = Roles._records(before)[3]
	var learned := 0
	var missing := -1
	for skill in range(84):
		var points := int(data["rules"]["role"]["skills"][skill]["learned_points"])
		if int(record["skill_statuses"][skill]) in [3, 5, 6]:
			learned += points
		elif points > 100 and missing < 0:
			missing = skill
	var total := 8500000 - learned - 100
	record["growth_pools"] = [1200000, 1200000, 1200000, 1200000, 1200000, 1200000, total - 7200000]
	var first := Preparation.project(before, prep["inputs"], data["rules"])
	assert_true(first["supported"])
	assert_eq(Roles._records(first["after"])[3]["staged_total"], 100)
	assert_true(missing >= 0)
	record["skill_statuses"][missing] = 6
	var second := Preparation.project(before, prep["inputs"], data["rules"])
	assert_true(second["supported"])
	assert_eq(Roles._records(second["after"])[3]["staged_total"], 0)
	before = prep["before_world"].duplicate(true)
	Roles._records(before)[3]["job"] = Roles._records(before)[4]["job"]
	var changed := Preparation.project(before, prep["inputs"], data["rules"])
	assert_true(changed["supported"])
	assert_true(Roles._records(changed["after"])[3]["staged_package"] != Roles._records(prep["expected_after"])[3]["staged_package"])


func test_bad_preparation_inputs_reject_without_publication_or_occupying_instance() -> void:
	var data := _data()
	var prep: Dictionary = data["preparation"]["cases"][0]
	var example: Dictionary = data["chain"]["cases"][0]
	for kind in range(16):
		var inputs: Dictionary = prep["inputs"].duplicate(true)
		match kind:
			0: inputs["task_id"] = 37
			1: inputs["mode"] = 1
			2: inputs["cap_mode"] = 1
			3: inputs["initial_grade"] = 0
			4: inputs["group_bonus"] = 0.5
			5: inputs["clock_seed"] = -1
			6: inputs["objective_slots"][0] = 0.5
			7: inputs["result_inputs"]["result_selector"] = 3
			8: inputs["result_inputs"]["time_key"] = 4
			9: inputs["result_inputs"]["unit_condition_key"] = 0
			10: inputs["result_inputs"]["units"][1]["character_id"] = 3
			11: inputs["result_inputs"]["units"][1]["character_id"] = 5
			12: inputs["result_inputs"]["units"][1]["ordinal"] = 0
			13: inputs["result_inputs"]["units"][1]["count_field_aa"] = 1001
			14: inputs["result_inputs"]["units"][1]["contribution_field_ac"] = 0.5
			15: inputs["result_inputs"]["units"][1]["status_field_ae"] = 128
		var campaign := Campaign.new()
		assert_true(campaign.initialize(prep["before_world"], data["rules"]))
		var handoff := _handoff(example)
		assert_false(handoff.prepare_tactics_replay("prep", inputs, campaign)["supported"], str(kind))
		assert_eq(campaign.revision(), 0)
		assert_eq(campaign.read_snapshot(), prep["before_world"])
		assert_eq(campaign.journal(), [])
		assert_true(handoff.prepare_tactics_replay("prep", prep["inputs"], campaign)["supported"])


func test_waiting_state11_state16_and_generic_gates_cannot_publish_preparation() -> void:
	var data := _data()
	var prep: Dictionary = data["preparation"]["cases"][0]
	var example: Dictionary = data["chain"]["cases"][0].duplicate(true)
	var campaign := Campaign.new()
	assert_true(campaign.initialize(prep["before_world"], data["rules"]))
	var pending := _handoff(example, false)
	assert_false(pending.prepare_tactics_replay("prep", prep["inputs"], campaign)["supported"])
	var generic := Return.new()
	assert_true(generic.accept_terminal_snapshot(example["declared_terminal_snapshot"]))
	assert_true(generic.prepare_result_replay(example["exit_frame"], example["dispatch_context"],
		example["round_before"], example["round_table"], true)["supported"])
	assert_false(generic.prepare_tactics_replay("prep", prep["inputs"], campaign)["supported"])
	example["round_before"]["total"] = 2
	example["round_table"] = {"config_id": 5, "next_roster": [3, 4, 9]}
	var next_round := Return.new()
	assert_true(next_round.accept_terminal_snapshot(example["declared_terminal_snapshot"]))
	var next_gate := next_round.prepare_scene5_result_replay(example["event_world"], example["exit_frame"], example["dispatch_context"],
		example["round_before"], example["round_table"], true)
	assert_true(next_gate["supported"])
	assert_eq(next_gate["requested_state"], 16)
	assert_false(next_round.prepare_tactics_replay("prep", prep["inputs"], campaign)["supported"])
	assert_eq(campaign.revision(), 0)
	assert_eq(campaign.read_snapshot(), prep["before_world"])


func test_preparation_parent_locks_operations_and_requires_matching_result_grade_and_ids() -> void:
	var data := _data()
	var prep: Dictionary = data["preparation"]["cases"][0]
	var example: Dictionary = data["chain"]["cases"][0]
	var campaign := Campaign.new()
	assert_true(campaign.initialize(prep["before_world"], data["rules"]))
	var handoff := _handoff(example)
	assert_true(handoff.prepare_tactics_replay("prep", prep["inputs"], campaign)["supported"])
	assert_false(campaign.prepare_tactics("second", prep["inputs"])["supported"])
	assert_false(campaign.begin_result("result", example["context"])["supported"])
	assert_false(campaign.begin_school_return("school", "missing")["supported"])
	assert_false(campaign.probe_school_join("probe", "missing", {})["supported"])
	for kind in range(4):
		var context: Dictionary = example["context"].duplicate(true)
		match kind:
			0: context["round_grade"] = 2
			1: context["round_ids"].reverse()
			2: context["participant_ids"] = [3, 4, 5]
			3: context["mode"] = 1
		assert_false(handoff.begin_result_replay("result", context, campaign)["supported"])
		assert_eq(campaign.revision(), 1)
	assert_false(handoff.begin_result_replay("prep", example["context"], campaign)["supported"])
	assert_true(handoff.begin_result_replay("result", example["context"], campaign)["supported"])
	assert_false(campaign.prepare_tactics("new", prep["inputs"])["supported"])


func test_preparation_identity_and_inputs_cannot_be_swapped_or_added_after_result_start() -> void:
	var data := _data()
	var prep: Dictionary = data["preparation"]["cases"][0]
	var example: Dictionary = data["chain"]["cases"][0]
	var campaign := Campaign.new()
	var other := Campaign.new()
	assert_true(campaign.initialize(prep["before_world"], data["rules"]))
	assert_true(other.initialize(prep["before_world"], data["rules"]))
	var handoff := _handoff(example)
	assert_true(handoff.prepare_tactics_replay("prep", prep["inputs"], campaign)["supported"])
	assert_false(handoff.prepare_tactics_replay("changed", prep["inputs"], campaign)["supported"])
	assert_false(handoff.prepare_tactics_replay("prep", prep["inputs"], other)["supported"])
	assert_false(handoff.prepare_tactics_replay("prep", data["preparation"]["cases"][1]["inputs"], campaign)["supported"])
	assert_false(handoff.begin_result_replay("result", example["context"], other)["supported"])
	assert_eq(other.revision(), 0)
	var old := Campaign.new()
	assert_true(old.initialize(example["before_result"], data["rules"]))
	var legacy := _handoff(example)
	assert_true(legacy.begin_result_replay("result", example["context"], old)["supported"])
	assert_false(legacy.prepare_tactics_replay("prep", prep["inputs"], old)["supported"])


func test_missing_or_bad_rules_cannot_publish_and_nonparticipant_metadata_are_preserved() -> void:
	var data := _data()
	var prep: Dictionary = data["preparation"]["cases"][0]
	for kind in range(5):
		var rules: Dictionary = data["rules"].duplicate(true)
		match kind:
			0: rules.erase("preparation")
			1: rules["preparation"]["job_rate_classes"][10] = 6
			2: rules["preparation"]["item_types"][0] = 9
			3: rules["preparation"]["loot_quotas"][3][0] = 0.5
			4: rules["preparation"]["objective_rewards"][0][1] = 8
		var campaign := Campaign.new()
		assert_true(campaign.initialize(prep["before_world"], rules))
		assert_false(campaign.prepare_tactics("prep", prep["inputs"])["supported"])
		assert_eq(campaign.revision(), 0)
	var before: Dictionary = prep["before_world"].duplicate(true)
	before["presentation"] = {"zoom": 1.25}
	Roles._records(before)[5]["staged_package"] = [11, 22, 33, 44, 55, 66, 77, 88]
	Roles._records(before)[5]["staged_total"] = 99
	var result := Preparation.project(before, prep["inputs"], data["rules"])
	assert_true(result["supported"])
	assert_eq(Roles._records(result["after"])[5], Roles._records(before)[5])
	assert_eq(result["after"]["presentation"]["zoom"], 1.25)
	assert_eq(result["after"]["relationships"], before["relationships"])
	assert_eq(result["after"]["school"], before["school"])


func test_raw_json_reordered_units_and_catalog_keep_ids_and_frozen_nested_inputs() -> void:
	var data := _data(true)
	var prep: Dictionary = data["preparation"]["cases"][0].duplicate(true)
	var example: Dictionary = data["chain"]["cases"][0]
	prep["before_world"]["characters"].reverse()
	prep["inputs"]["result_inputs"]["units"].reverse()
	prep["inputs"]["presentation"] = {"zoom": 1.25}
	var original: Dictionary = prep["inputs"].duplicate(true)
	var campaign := Campaign.new()
	assert_true(campaign.initialize(prep["before_world"], data["rules"]))
	data["rules"]["preparation"]["loot_quotas"].clear()
	var handoff := _handoff(example)
	var result := handoff.prepare_tactics_replay("prep", prep["inputs"], campaign)
	assert_true(result["supported"])
	var expected: Dictionary = prep["expected_after"].duplicate(true)
	expected["characters"].reverse()
	assert_eq(Roles._integers(campaign.read_snapshot()), Roles._integers(expected))
	prep["inputs"]["result_inputs"]["units"].clear()
	result["result"]["after"].clear()
	campaign.journal()[0]["after"].clear()
	assert_eq(handoff.prepare_tactics_replay("prep", original, campaign)["status"], "duplicate")
	assert_true(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
	assert_true(handoff.finish_result_replay("battle", true, true)["supported"])
	assert_eq(campaign.revision(), 3)
	assert_eq(campaign.journal()[0]["source_inputs"]["tactical_preparation_inputs"], original)
	assert_eq(campaign.journal()[3]["source_inputs"]["tactical_preparation_parent"]["inputs"]["presentation"]["zoom"], 1.25)


func test_loot_owned_duplicate_draws_cascade_and_keep_nonownership_flag_bits() -> void:
	var data := _data()
	var prep: Dictionary = data["preparation"]["cases"][0]
	var before: Dictionary = prep["before_world"].duplicate(true)
	# Original native cases already encounter owned item1 and cascade. A second
	# projection owns all type1 items, so their duplicate draws must never award.
	for item in range(360):
		if int(data["rules"]["preparation"]["item_types"][item]) == 1:
			before["item_flags"][item] = 0xa701
	var projected := Preparation.project(before, prep["inputs"], data["rules"])
	assert_true(projected["supported"])
	assert_eq(projected["loot_groups"][6], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
	for item in range(360):
		if int(data["rules"]["preparation"]["item_types"][item]) == 1:
			assert_eq(projected["after"]["item_flags"][item], 0xa701)
	before = prep["before_world"].duplicate(true)
	before["item_flags"][13] = 0xa604
	projected = Preparation.project(before, prep["inputs"], data["rules"])
	assert_true(projected["supported"])
	assert_eq(projected["after"]["item_flags"][13], 0xa105)


func test_three_unit_preparation_cannot_award_then_lock_an_uncovered_four_student_result() -> void:
	var data := _data()
	var prep: Dictionary = data["preparation"]["cases"][0]
	var before: Dictionary = data["chain"]["cases"][0]["expected_after"]
	var campaign := Campaign.new()
	assert_true(campaign.initialize(before, data["rules"]))
	var handoff := _handoff(data["chain"]["cases"][0])
	assert_false(handoff.prepare_tactics_replay("prep", prep["inputs"], campaign)["supported"])
	assert_eq(campaign.revision(), 0)
	assert_eq(campaign.journal(), [])
	assert_eq(campaign.read_snapshot(), before)
	assert_eq(handoff.status(), "pending_result_transaction")
