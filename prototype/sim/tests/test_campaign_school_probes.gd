extends "res://sim/tests/test_base.gd"

const Campaign = preload("res://sim/campaign_result_state.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const Return = preload("res://sim/battle_return.gd")


func _fixture(path := "res://data/campaign_school_layout_evidence.json", raw := false) -> Dictionary:
	var value: Dictionary = JSON.parse_string(FileAccess.get_file_as_string(path))
	return value if raw else Roles._integers(value)


func _campaign(fixture: Dictionary, index := 0) -> Campaign:
	var campaign := Campaign.new()
	assert_true(campaign.initialize(fixture["cases"][index]["before"], fixture["rules"]))
	return campaign


func _complete(campaign: Campaign, example: Dictionary, identity := "battle") -> void:
	assert_true(campaign.begin_result(identity, example["context"])["supported"])
	assert_true(campaign.finish_result(identity, true, true)["supported"])


func test_owned_result_join_week_matches_same_cpu_full_catalog_and_school_snapshots() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := _campaign(fixture)
	_complete(campaign, example)
	assert_true(campaign.read_snapshot() == example["after_result"])
	var joined := campaign.probe_school_join("join", "battle", example["join_context"])
	assert_true(joined["supported"])
	if not joined["supported"]:
		return
	assert_eq(joined["status"], "joined_once")
	assert_true(joined["campaign_snapshot"] == example["after_join_probe"], "complete native catalog after source join instruction")
	assert_true(joined["result"]["after"] == example["school_after_join_probe"], "independently captured school layout after join")
	assert_eq(campaign.revision(), 3)
	var settled := campaign.probe_school_week("week", "join")
	assert_true(settled["supported"])
	if not settled["supported"]:
		return
	assert_true(settled["campaign_snapshot"] == example["after_week_probe"], "complete native catalog after direct week call")
	assert_true(settled["result"]["after"] == example["school_after_week_probe"], "independently captured school layout after week")
	assert_true(campaign.read_school_snapshot()["snapshot"] == example["school_after_week_probe"])
	assert_eq(campaign.revision(), 4)
	var log := campaign.journal()
	assert_eq(log.map(func(entry): return entry["phase"]), ["initialized", "result_fields", "direct_join_probe", "direct_week_probe"])
	assert_eq(log.map(func(entry): return entry["revision"]), [1, 2, 3, 4])
	assert_true(log[2]["before"] == example["after_result"])
	assert_true(log[2]["after"] == log[3]["before"])
	assert_true(log[3]["after"] == example["after_week_probe"])
	assert_eq(log[2]["source_inputs"]["direct_source_call"], "Chapter020 opcode144")
	assert_eq(log[3]["source_inputs"]["direct_source_call"], "0x4d3510")
	assert_eq(log[3]["source_inputs"]["join_source_inputs"]["result_instance"], "battle")
	for output in [joined, settled]:
		assert_eq(output["execution_scope"], "isolated_direct_data_probe")
		for key in ["chapter_completed", "school_initialized", "live_witness", "authorizes_persistent_write"]:
			assert_false(output[key])
	# Direct probes do not turn the source request into an ADV completion.
	assert_eq(campaign.finish_result("battle", false, false)["result"]["requested_state"], 6)


func test_confirmation_wait_and_special_result_do_not_open_ordinary_join_or_week() -> void:
	var fixture := _fixture()
	var join_context: Dictionary = fixture["cases"][0]["join_context"]
	for index in [1, 2]:
		var example: Dictionary = fixture["cases"][index]
		var campaign := _campaign(fixture, index)
		assert_true(campaign.begin_result("battle", example["context"])["supported"])
		assert_true(campaign.finish_result("battle", example["confirmed"], example["mvp_ready"])["supported"])
		var before := campaign.read_snapshot()
		var version := campaign.revision()
		assert_false(campaign.probe_school_join("join", "battle", join_context)["supported"])
		assert_false(campaign.probe_school_week("week", "join")["supported"])
		assert_true(campaign.read_snapshot() == before)
		assert_eq(campaign.revision(), version)
		if index == 1:
			assert_eq(campaign.finish_result("battle", true, false)["status"], "waiting_mvp")
			assert_false(campaign.probe_school_join("join", "battle", join_context)["supported"])
			assert_true(campaign.finish_result("battle", false, true)["supported"])
			assert_true(campaign.probe_school_join("join", "battle", join_context)["supported"], "rejected join ID was not reserved")


func test_invalid_join_context_and_missing_parent_never_publish_or_reserve_probe() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := _campaign(fixture)
	assert_false(campaign.probe_school_join("join", "missing", example["join_context"])["supported"])
	assert_false(campaign.probe_school_week("week", "join")["supported"])
	assert_true(campaign.read_snapshot() == example["before"])
	_complete(campaign, example)
	for changes in [{"task_state": 7}, {"opcode": 145}, {"character_id": 12},
			{"difficulty": 0.5}, {"group": 0}, {"script_file_offset": 24}]:
		var context: Dictionary = example["join_context"].duplicate(true)
		context.merge(changes, true)
		assert_false(campaign.probe_school_join("join", "battle", context)["supported"])
		assert_true(campaign.read_snapshot() == example["after_result"])
		assert_eq(campaign.revision(), 2)
		assert_eq(campaign.journal().size(), 2)
	assert_true(campaign.probe_school_join("join", "battle", example["join_context"])["supported"])
	assert_true(campaign.probe_school_week("week", "join")["supported"])
	assert_true(campaign.read_snapshot() == example["after_week_probe"])


func test_duplicate_and_conflicting_operations_cannot_reset_join_or_advance_second_week() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := _campaign(fixture)
	_complete(campaign, example)
	assert_true(campaign.probe_school_join("join", "battle", example["join_context"])["supported"])
	assert_false(campaign.probe_school_join("battle", "battle", example["join_context"])["supported"])
	assert_false(campaign.probe_school_week("join", "join")["supported"])
	assert_false(campaign.begin_result("join", example["context"])["supported"])
	assert_false(campaign.probe_school_join("new_join", "battle", example["join_context"])["supported"])
	assert_true(campaign.probe_school_week("week", "join")["supported"])
	for delivery in range(3):
		var joined := campaign.probe_school_join("join", "battle", example["join_context"])
		assert_eq(joined["status"], "duplicate")
		assert_true(joined["result"]["after"] == example["school_after_join_probe"])
		assert_true(joined["campaign_snapshot"] == example["after_week_probe"])
		assert_eq(campaign.probe_school_week("week", "join")["status"], "duplicate")
		assert_eq(campaign.finish_result("battle", false, false)["status"], "duplicate")
		assert_true(campaign.read_snapshot() == example["after_week_probe"])
		assert_eq(campaign.revision(), 4)
		assert_eq(campaign.journal().size(), 4)
	var changed: Dictionary = example["join_context"].duplicate(true)
	changed["difficulty"] = 2
	assert_false(campaign.probe_school_join("join", "battle", changed)["supported"])
	assert_false(campaign.probe_school_join("join", "different_battle", example["join_context"])["supported"])
	assert_false(campaign.probe_school_week("week", "different_join")["supported"])
	assert_false(campaign.probe_school_week("second_week", "join")["supported"])
	assert_eq(campaign.revision(), 4)
	assert_true(campaign.read_snapshot() == example["after_week_probe"])


func test_stale_result_and_join_parents_cannot_overwrite_a_later_result() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := _campaign(fixture)
	_complete(campaign, example, "old")
	_complete(campaign, example, "new")
	var before := campaign.read_snapshot()
	assert_false(campaign.probe_school_join("join", "old", example["join_context"])["supported"])
	assert_true(campaign.read_snapshot() == before)
	assert_true(campaign.probe_school_join("join", "new", example["join_context"])["supported"])
	# This synthetic context exercises revision locking only. It is not another
	# source-witnessed battle or proof of the full campaign control sequence.
	var context: Dictionary = example["context"].duplicate(true)
	context["participant_ids"] = [3, 4, 9, 5]
	context["round_ids"] = [3, 4, 9, 5]
	context["group_slots"][0] = [0, 1, 2, 3]
	assert_true(campaign.begin_result("next", context)["supported"])
	before = campaign.read_snapshot()
	var version := campaign.revision()
	assert_false(campaign.probe_school_week("week", "join")["supported"])
	assert_true(campaign.read_snapshot() == before)
	assert_eq(campaign.revision(), version)
	assert_true(campaign.finish_result("next", true, true)["supported"])
	before = campaign.read_snapshot()
	version = campaign.revision()
	assert_false(campaign.probe_school_week("week", "join")["supported"])
	assert_true(campaign.read_snapshot() == before)
	assert_eq(campaign.revision(), version)


func test_raw_reordered_catalog_uses_frozen_rules_and_preserves_result_history_and_metadata() -> void:
	var fixture := _fixture("res://data/campaign_school_layout_evidence.json", true)
	var example: Dictionary = fixture["cases"][0]
	var before: Dictionary = example["before"].duplicate(true)
	before["characters"].reverse()
	before["relationships"].reverse()
	before["presentation"] = {"zoom": 1.25}
	before["characters"][0]["portrait"] = {"offset": 0.75}
	var rules: Dictionary = fixture["rules"].duplicate(true)
	var campaign := Campaign.new()
	assert_true(campaign.initialize(before, rules))
	rules["week"]["unlock_rules"].clear()
	rules["role"]["level_thresholds"].fill(0)
	rules["role"]["skills"].clear()
	var sources := {"declared_evidence": {"version": 1}}
	assert_true(campaign.begin_result("battle", example["context"], sources)["supported"])
	sources["declared_evidence"]["version"] = 2
	assert_true(campaign.finish_result("battle", true, true)["supported"])
	var context: Dictionary = example["join_context"].duplicate(true)
	var joined := campaign.probe_school_join("join", "battle", context)
	assert_true(joined["supported"])
	context["opcode"] = 145
	if not joined["supported"]:
		return
	joined["result"]["after"]["participants"].clear()
	joined["campaign_snapshot"]["school"]["student_ids"].clear()
	campaign.journal()[2]["source_inputs"]["result_source_inputs"].clear()
	assert_true(campaign.probe_school_week("week", "join")["supported"])
	var expected: Dictionary = example["after_week_probe"].duplicate(true)
	expected["characters"].reverse()
	expected["relationships"].reverse()
	expected["presentation"] = {"zoom": 1.25}
	expected["characters"][0]["portrait"] = {"offset": 0.75}
	assert_true(Roles._integers(campaign.read_snapshot()) == Roles._integers(expected), "all native integral fields after reversed raw JSON probes")
	assert_eq(campaign.read_snapshot()["presentation"]["zoom"], 1.25)
	assert_eq(campaign.read_snapshot()["characters"][0]["portrait"]["offset"], 0.75)
	assert_eq(campaign.journal()[2]["source_inputs"]["result_source_inputs"]["declared_evidence"]["version"], 1)
	assert_eq(campaign.journal()[3]["source_inputs"]["join_source_inputs"]["join_context"]["opcode"], 144)
	assert_true(campaign.probe_school_join("join", "battle", example["join_context"])["supported"])
	assert_eq(campaign.revision(), 4)


func test_battle_return_declared_gates_use_same_owned_catalog_through_direct_data_probes() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := _campaign(fixture)
	var handoff := Return.new()
	var terminal := {"frame": 42, "winner": 0, "units": [
		{"battle_index": 0, "character_id": 3, "faction": 0},
		{"battle_index": 1, "character_id": 4, "faction": 0},
		{"battle_index": 2, "character_id": 9, "faction": 0},
		{"battle_index": 3, "character_id": -1, "faction": 1}]}
	assert_true(handoff.accept_terminal_snapshot(terminal))
	var task: Dictionary = _fixture("res://data/scene5_task_execution_evidence.json")["cases"][0]
	var round_example: Dictionary = _fixture("res://data/battle_round_execution_evidence.json")["cases"][0]
	# The task/round gate inputs are separate declared evidence. Only the layout
	# result->direct join->direct week snapshots were captured in the same CPU.
	assert_true(handoff.prepare_result_replay(task["exit_frame"], task["dispatch_context"],
		round_example["before"], round_example["synthetic_round_table"], true)["supported"])
	assert_true(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
	assert_true(handoff.finish_result_replay("battle", true, true)["supported"])
	assert_true(campaign.probe_school_join("join", "battle", example["join_context"])["supported"])
	assert_true(campaign.probe_school_week("week", "join")["supported"])
	assert_true(campaign.read_snapshot() == example["after_week_probe"])
	assert_eq(handoff.status(), "result_completed")
	var result := handoff.finish_result_replay("battle", false, false)
	assert_eq(result["status"], "duplicate")
	assert_true(result["campaign_snapshot"] == example["after_week_probe"])
	assert_eq(result["result"]["requested_state"], 6)
	assert_false(result["live_witness"])
	assert_false(result["school_initialized"])
	assert_eq(campaign.revision(), 4)
	assert_eq(campaign.journal()[2]["source_inputs"]["result_source_inputs"]["result_gate"]["state_requests"], [11, 10, 12])


func test_missing_campaign_empty_ids_and_legacy_layout_do_not_create_school_state() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var empty := Campaign.new()
	assert_false(empty.probe_school_join("join", "battle", example["join_context"])["supported"])
	assert_false(empty.probe_school_week("week", "join")["supported"])
	assert_true(empty.read_snapshot().is_empty())
	var legacy := _fixture("res://data/result_transaction_evidence_v2.json")
	var campaign := Campaign.new()
	assert_true(campaign.initialize(legacy["cases"][0]["before"], legacy["rules"]))
	_complete(campaign, legacy["cases"][0])
	var saved := campaign.read_snapshot()
	assert_false(campaign.read_school_snapshot()["supported"])
	assert_false(campaign.probe_school_join("join", "battle", example["join_context"])["supported"])
	assert_false(campaign.probe_school_week("week", "join")["supported"])
	assert_false(campaign.probe_school_join("", "battle", example["join_context"])["supported"])
	assert_false(campaign.probe_school_week("", "join")["supported"])
	assert_true(campaign.read_snapshot() == saved)
	assert_eq(campaign.revision(), 2)
