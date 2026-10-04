extends "res://sim/tests/test_base.gd"

const Campaign = preload("res://sim/campaign_result_state.gd")
const Continuation = preload("res://sim/school_return_continuation.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const Return = preload("res://sim/battle_return.gd")
const Work = preload("res://sim/workroom_return_replay.gd")
const Layout = preload("res://sim/campaign_school_layout.gd")


func _fixture(raw := false) -> Dictionary:
	var value: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/campaign_return_chain_evidence.json"))
	return value if raw else Roles._integers(value)


func _campaign(fixture: Dictionary, example: Dictionary) -> Campaign:
	var campaign := Campaign.new()
	assert_true(campaign.initialize(example["before_result"], fixture["rules"]))
	assert_true(campaign.begin_result("battle", example["context"])["supported"])
	assert_true(campaign.finish_result("battle", example["confirmed"], true)["supported"])
	return campaign


func test_all_five_native_paths_match_full_catalog_and_independent_school_layout() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		var campaign := _campaign(fixture, example)
		assert_true(campaign.read_snapshot() == example["after_result"], example["name"] + " result")
		var result := campaign.begin_school_return("school", "battle")
		if not example["confirmed"]:
			assert_false(result["supported"])
			assert_true(campaign.read_snapshot() == example["expected_after"])
			assert_false(campaign.advance_school_return("school", true, true, true)["supported"])
			continue
		assert_true(result["supported"], example["name"])
		if not result["supported"]:
			continue
		assert_true(campaign.read_snapshot() == example["after_chapter"], "source join before chapter END")
		result = campaign.advance_school_return("school", example["chapter_key_ready"], example["continue_ready"], example["school_fade_ready"])
		assert_true(result["supported"], example["name"])
		if not result["supported"]:
			continue
		assert_true(campaign.read_snapshot() == example["expected_after"], example["name"] + " complete native catalog")
		assert_true(campaign.read_school_snapshot()["snapshot"] == example["expected_school_after"], example["name"] + " independent school view")
		assert_eq(result["result"]["requested_state"], example["expected_controller"]["pending_state"])
		assert_eq(result["result"]["pending_flag"], example["expected_controller"]["pending_flag"])
		assert_eq(result["school_constructed"], example["expected_school_constructed"])
		assert_eq(result["result"]["tasks"], example["expected_tasks"])
		for key in ["school_initialized", "live_witness", "authorizes_persistent_write"]:
			assert_false(result[key])


func test_every_native_checkpoint_matches_phase_journal_in_original_order() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := _campaign(fixture, example)
	assert_true(campaign.begin_school_return("school", "battle")["supported"])
	assert_true(campaign.advance_school_return("school", true, true, true)["supported"])
	var log := campaign.journal().slice(2)
	assert_eq(log.map(func(entry): return entry["phase"]), ["chapter020_join", "chapter021_end", "state7_week",
		"ch001_end", "workroom_constructed", "workroom_continue", "ch002_opcode151", "ch002_end", "school_dispatch"])
	var expected := {"chapter020_join": example["after_chapter"], "chapter021_end": example["after_chapter"],
		"state7_week": example["checkpoints"]["new_adv"], "ch001_end": example["checkpoints"]["workroom"],
		"workroom_constructed": example["checkpoints"]["workroom"], "workroom_continue": example["checkpoints"]["ch002_adv"],
		"ch002_opcode151": example["expected_after"], "ch002_end": example["expected_after"], "school_dispatch": example["expected_after"]}
	var previous: Dictionary = example["after_result"]
	for entry in log:
		assert_true(entry["before"] == previous, "continuous phase before-image")
		assert_true(entry["after"] == expected[entry["phase"]], "native phase " + entry["phase"])
		assert_eq(entry["after"]["relationships"].size(), 20)
		assert_eq(entry["after"]["recipient_id"], 4)
		previous = entry["after"]
	assert_eq(log.map(func(entry): return entry["revision"]), [3, 4, 4, 4, 4, 4, 4, 4, 4])
	assert_eq(log[1]["source"]["offset"], 0x61e)
	assert_eq(log[3]["source"]["offset"], 0x1b0)
	assert_eq(log[7]["source"]["offset"], 0x6d0)


func test_waits_resume_without_rejoining_replaying_history_or_settling_a_second_week() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := _campaign(fixture, example)
	assert_true(campaign.begin_school_return("school", "battle")["supported"])
	for delivery in range(3):
		assert_eq(campaign.advance_school_return("school", false, true, true)["status"], "waiting_chapter_end")
		assert_true(campaign.read_snapshot() == fixture["cases"][2]["expected_after"])
		assert_eq(campaign.revision(), 3)
	assert_eq(campaign.advance_school_return("school", true, false, true)["status"], "waiting_continue")
	assert_true(campaign.read_snapshot() == fixture["cases"][3]["expected_after"])
	assert_eq(campaign.revision(), 4)
	for delivery in range(3):
		assert_eq(campaign.advance_school_return("school", false, false, true)["status"], "waiting_continue")
		assert_eq(campaign.revision(), 4)
	assert_eq(campaign.advance_school_return("school", false, true, false)["status"], "waiting_ch002_end")
	assert_true(campaign.read_snapshot() == fixture["cases"][4]["expected_after"])
	assert_eq(campaign.revision(), 5)
	assert_eq(campaign.advance_school_return("school", true, true, false)["status"], "waiting_ch002_end")
	assert_eq(campaign.revision(), 5)
	assert_true(campaign.advance_school_return("school", false, false, true)["result"]["completed"])
	assert_true(campaign.read_snapshot() == example["expected_after"])
	assert_eq(campaign.revision(), 6)
	for delivery in range(3):
		assert_eq(campaign.begin_school_return("school", "battle")["status"], "duplicate")
		assert_eq(campaign.advance_school_return("school", false, false, false)["status"], "duplicate")
		assert_eq(campaign.finish_result("battle", true, true)["status"], "duplicate")
		assert_true(campaign.read_snapshot() == example["expected_after"])
		assert_eq(campaign.revision(), 6)
	assert_eq(campaign.journal().filter(func(entry): return entry["phase"] == "state7_week").size(), 1)


func test_pending_return_locks_new_results_and_probes_and_rejects_instance_collisions() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := _campaign(fixture, example)
	assert_true(campaign.begin_school_return("school", "battle")["supported"])
	var before := campaign.read_snapshot()
	assert_false(campaign.begin_result("next", example["context"])["supported"])
	assert_false(campaign.begin_result("school", example["context"])["supported"])
	assert_false(campaign.begin_school_return("another", "battle")["supported"])
	assert_false(campaign.begin_school_return("school", "different")["supported"])
	assert_false(campaign.begin_school_return("battle", "battle")["supported"])
	assert_false(campaign.probe_school_join("join", "battle", Continuation.JOIN_CONTEXT)["supported"])
	assert_false(campaign.probe_school_week("week", "join")["supported"])
	assert_false(campaign.advance_school_return("wrong", true, true, true)["supported"])
	assert_true(campaign.read_snapshot() == before)
	assert_eq(campaign.revision(), 3)
	assert_true(campaign.advance_school_return("school", true, true, true)["supported"])
	assert_eq(campaign.revision(), 4)


func test_rejected_waiting_special_and_stale_parents_do_not_reserve_return_instance() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][1]
	var campaign := _campaign(fixture, example)
	assert_false(campaign.begin_school_return("school", "battle")["supported"])
	assert_eq(campaign.revision(), 1)
	assert_true(campaign.finish_result("battle", true, true)["supported"])
	assert_true(campaign.begin_school_return("school", "battle")["supported"])
	var fresh := _campaign(fixture, fixture["cases"][0])
	assert_true(fresh.begin_result("new", example["context"])["supported"])
	assert_true(fresh.finish_result("new", true, true)["supported"])
	var saved := fresh.read_snapshot()
	assert_false(fresh.begin_school_return("school", "battle")["supported"])
	assert_true(fresh.read_snapshot() == saved)
	assert_true(fresh.begin_school_return("school", "new")["supported"])
	var special_fixture: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/campaign_school_layout_evidence.json")))
	var special := Campaign.new()
	var input: Dictionary = special_fixture["cases"][2]
	assert_true(special.initialize(input["before"], special_fixture["rules"]))
	assert_true(special.begin_result("battle", input["context"])["supported"])
	assert_true(special.finish_result("battle", true, true)["supported"])
	assert_false(special.begin_school_return("school", "battle")["supported"])
	assert_true(special.read_snapshot() == input["after_result"])


func test_missing_catalog_bad_recipient_and_dates_reject_before_checkpoint_creation() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for kind in range(6):
		var before: Dictionary = example["after_result"].duplicate(true)
		match kind:
			0: before.erase("school")
			1: before["recipient_id"] = 3
			2: before["month"] = 5
			3: before["school"]["student_ids"][0] = 9
			4: before["school"]["adv_globals"]["0x7e1182"] = 1
			5: before["school"]["adv_globals"]["0x7a5292"] = 8
		var replay := Continuation.new()
		assert_false(replay.begin("school", before, fixture["rules"])["supported"])
		assert_false(replay.advance("school", true, true, true)["supported"])
		assert_true(replay.begin("school", example["after_result"], fixture["rules"])["supported"])
	assert_false(Campaign.new().begin_school_return("school", "missing")["supported"])


func test_recipient_alias_four_is_preserved_and_other_unaudited_values_stay_closed() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var before: Dictionary = Layout.school_view(example["checkpoints"]["workroom"], fixture["rules"]["week"])["snapshot"]
	for value in [0, 4, 1, 13, 0.5]:
		var snapshot := before.duplicate(true)
		snapshot["adv_globals"]["0x7e1180"] = value
		var replay := Work.new()
		var result := replay.begin("work", Continuation.WORK_CONTEXT, snapshot, fixture["rules"]["week"])
		assert_eq(result["supported"], value == 0 or value == 4)
		if result["supported"]:
			assert_eq(result["after"]["adv_globals"]["0x7e1180"], value)


func test_raw_reordered_catalog_frozen_inputs_sources_and_fractional_metadata_survive() -> void:
	var fixture := _fixture(true)
	var example: Dictionary = fixture["cases"][0]
	var before: Dictionary = example["before_result"].duplicate(true)
	before["characters"].reverse()
	before["relationships"].reverse()
	before["presentation"] = {"zoom": 1.25}
	before["characters"][0]["portrait"] = {"offset": 0.75}
	var rules: Dictionary = fixture["rules"].duplicate(true)
	var campaign := Campaign.new()
	assert_true(campaign.initialize(before, rules))
	before["characters"].clear()
	rules["role"]["skills"].clear()
	rules["week"]["unlock_rules"].clear()
	var sources := {"declared": {"revision": 1}}
	assert_true(campaign.begin_result("battle", example["context"], sources)["supported"])
	sources["declared"]["revision"] = 2
	assert_true(campaign.finish_result("battle", true, true)["supported"])
	var first := campaign.begin_school_return("school", "battle")
	assert_true(first["supported"])
	first["result"]["after"]["characters"].clear()
	first["campaign_snapshot"]["school"]["student_ids"].clear()
	campaign.journal()[2]["source_inputs"].clear()
	assert_true(campaign.advance_school_return("school", true, true, true)["supported"])
	var expected: Dictionary = example["expected_after"].duplicate(true)
	expected["characters"].reverse()
	expected["relationships"].reverse()
	expected["presentation"] = {"zoom": 1.25}
	expected["characters"][0]["portrait"] = {"offset": 0.75}
	assert_true(Roles._integers(campaign.read_snapshot()) == Roles._integers(expected))
	assert_eq(campaign.read_snapshot()["presentation"]["zoom"], 1.25)
	assert_eq(campaign.read_snapshot()["characters"][0]["portrait"]["offset"], 0.75)
	assert_eq(campaign.journal()[2]["source_inputs"]["result_source_inputs"]["declared"]["revision"], 1)
	assert_eq(campaign.revision(), 4)


func test_battle_return_binds_continuation_and_old_result_delivery_does_not_reset_status() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := Campaign.new()
	assert_true(campaign.initialize(example["before_result"], fixture["rules"]))
	var handoff := Return.new()
	assert_false(handoff.begin_school_return_replay("school")["supported"])
	assert_true(handoff.accept_terminal_snapshot({"frame": 42, "winner": 0, "units": [
		{"battle_index": 0, "character_id": 3, "faction": 0}, {"battle_index": 1, "character_id": 4, "faction": 0},
		{"battle_index": 2, "character_id": 9, "faction": 0}, {"battle_index": 3, "character_id": -1, "faction": 1}]}))
	var task: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/scene5_task_execution_evidence.json")))["cases"][0]
	var round_input: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/battle_round_execution_evidence.json")))["cases"][0]
	# Task/round input remains separate declared evidence, not a same-world
	# native battle witness. The result->school catalog has one-CPU evidence.
	assert_true(handoff.prepare_result_replay(task["exit_frame"], task["dispatch_context"],
		round_input["before"], round_input["synthetic_round_table"], true)["supported"])
	assert_true(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
	assert_false(handoff.begin_school_return_replay("school")["supported"])
	assert_true(handoff.finish_result_replay("battle", true, true)["supported"])
	assert_true(handoff.begin_school_return_replay("school")["supported"])
	assert_false(handoff.begin_school_return_replay("different")["supported"])
	assert_false(handoff.advance_school_return_replay("different", true, true, true)["supported"])
	assert_true(handoff.advance_school_return_replay("school", true, true, true)["school_constructed"])
	assert_eq(handoff.status(), "school_constructed")
	assert_eq(handoff.finish_result_replay("battle", false, false)["status"], "duplicate")
	assert_eq(handoff.status(), "school_constructed")
	assert_eq(handoff.begin_result_replay("battle", example["context"], campaign)["status"], "duplicate")
	assert_eq(handoff.status(), "school_constructed")
	assert_true(campaign.read_snapshot() == example["expected_after"])
	assert_eq(campaign.revision(), 4)
