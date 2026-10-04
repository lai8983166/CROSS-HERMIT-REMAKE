extends "res://sim/tests/test_base.gd"

const Campaign = preload("res://sim/campaign_result_state.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")
const Layout = preload("res://sim/campaign_school_layout.gd")
const Return = preload("res://sim/battle_return.gd")


func _fixture(raw := false) -> Dictionary:
	var data: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/campaign_school_boot_evidence.json"))
	return data if raw else Roles._integers(data)


func _campaign(fixture: Dictionary, example: Dictionary, fade_ready := true) -> Campaign:
	var campaign := Campaign.new()
	assert_true(campaign.initialize(example["before_result"], fixture["rules"]))
	assert_true(campaign.begin_result("battle", example["context"])["supported"])
	assert_true(campaign.finish_result("battle", true, true)["supported"])
	assert_true(campaign.read_snapshot() == example["after_result"])
	assert_true(campaign.begin_school_return("school", "battle")["supported"])
	assert_true(campaign.read_snapshot() == example["after_chapter"])
	assert_true(campaign.advance_school_return("school", true, true, fade_ready)["supported"])
	return campaign


func test_native_complete_and_blocked_paths_match_full_canonical_and_school_views() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		var campaign := _campaign(fixture, example, example["school_fade_ready"])
		assert_true(campaign.read_snapshot() == example["before_boot"], "continuous construction input")
		assert_true(campaign.read_school_snapshot()["snapshot"] == example["expected_school_before_boot"])
		var result := campaign.project_school_return_boot("school")
		assert_eq(result["supported"], example["expected_boot_projected"])
		assert_true(campaign.read_snapshot() == example["expected_after"], example["name"])
		assert_true(campaign.read_school_snapshot()["snapshot"] == example["expected_school_after"])
		assert_eq(campaign.revision(), 5 if example["expected_boot_projected"] else 4)
		if result["supported"]:
			assert_true(result["school_boot_data_projected"])
			assert_true(result["school_constructed"])
			assert_eq(result["result"]["tasks"], example["expected_tasks"])
			for key in ["school_initialized", "interactive_school_ready", "live_witness", "authorizes_persistent_write"]:
				assert_false(result[key])


func test_ch002_wait_resume_projects_once_without_second_week_or_result_history() -> void:
	var fixture := _fixture()
	var wait: Dictionary = fixture["cases"][1]
	var campaign := _campaign(fixture, wait, false)
	for delivery in range(3):
		assert_false(campaign.project_school_return_boot("school")["supported"])
		assert_eq(campaign.revision(), 4)
		assert_true(campaign.read_snapshot() == wait["expected_after"])
	assert_true(campaign.advance_school_return("school", false, false, true)["school_constructed"])
	assert_eq(campaign.revision(), 5)
	assert_true(campaign.read_snapshot() == fixture["cases"][0]["before_boot"])
	assert_true(campaign.project_school_return_boot("school")["school_boot_data_projected"])
	assert_eq(campaign.revision(), 6)
	for delivery in range(3):
		assert_eq(campaign.project_school_return_boot("school")["status"], "duplicate")
		assert_eq(campaign.begin_school_return("school", "battle")["status"], "duplicate")
		assert_eq(campaign.advance_school_return("school", false, false, false)["status"], "duplicate")
		assert_eq(campaign.revision(), 6)
	assert_true(campaign.read_snapshot() == fixture["cases"][0]["expected_after"])
	assert_eq(campaign.journal().filter(func(row): return row["phase"] == "state7_week").size(), 1)
	assert_eq(campaign.journal().filter(func(row): return row["phase"] == "school_boot_data").size(), 1)


func _next_context(example: Dictionary) -> Dictionary:
	var context: Dictionary = example["context"].duplicate(true)
	context["participant_ids"].append(5)
	context["round_ids"].append(5)
	context["group_slots"][0][3] = 3
	return context


func test_cached_old_boot_never_overwrites_later_result_and_unprojected_stale_parent_rejects() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for project_first in [true, false]:
		var campaign := _campaign(fixture, example)
		if project_first:
			assert_true(campaign.project_school_return_boot("school")["supported"])
		assert_true(campaign.begin_result("next", _next_context(example))["supported"])
		var current := campaign.read_snapshot()
		var revision := campaign.revision()
		var result := campaign.project_school_return_boot("school")
		assert_eq(result["supported"], project_first)
		if project_first:
			assert_eq(result["status"], "duplicate")
			assert_true(result["campaign_snapshot"] == current)
		assert_true(campaign.read_snapshot() == current)
		assert_eq(campaign.revision(), revision)


func test_missing_rules_controls_ids_and_pending_chapter_reject_without_publication() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	assert_false(Campaign.new().project_school_return_boot("school")["supported"])
	for kind in range(3):
		var input: Dictionary = fixture.duplicate(true)
		if kind == 0:
			input["rules"].erase("school_boot")
		elif kind == 1:
			input["cases"][0]["before_result"]["school"].erase("school_control")
			input["cases"][0]["after_result"]["school"].erase("school_control")
			input["cases"][0]["after_chapter"]["school"].erase("school_control")
		else:
			input["rules"]["school_boot"]["adventures"][7]["id"] = 9
		var campaign := _campaign(input, input["cases"][0])
		var saved := campaign.read_snapshot()
		assert_false(campaign.project_school_return_boot("wrong")["supported"])
		for delivery in range(2):
			assert_false(campaign.project_school_return_boot("school")["supported"])
			assert_true(campaign.read_snapshot() == saved)
			assert_eq(campaign.revision(), 4)
	var waiting := Campaign.new()
	assert_true(waiting.initialize(example["before_result"], fixture["rules"]))
	assert_true(waiting.begin_result("battle", example["context"])["supported"])
	assert_false(waiting.project_school_return_boot("school")["supported"])
	assert_true(waiting.finish_result("battle", true, true)["supported"])
	assert_true(waiting.begin_school_return("school", "battle")["supported"])
	assert_false(waiting.project_school_return_boot("school")["supported"])
	assert_eq(waiting.revision(), 3)


func test_malformed_captured_control_and_raw_class_aliases_reject_initialization() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for kind in range(9):
		var before: Dictionary = example["before_result"].duplicate(true)
		var control: Dictionary = before["school"]["school_control"]
		match kind:
			0: control.erase("group_raw_bytes")
			1: control["group_raw_bytes"][16] = 0
			2: control["group_rankings"][0][0] = 0.5
			3: control["person_phase"] = 2
			4: control["adventure_entries"] = [[], []]
			5: control["adventure_counts"][0] = 1
			6: control["lecture_unlock_flags"].pop_back()
			7: control["idle_student_ids"] = [99]
			8: before["school"]["school_control"] = []
		var campaign := Campaign.new()
		assert_false(campaign.initialize(before, fixture["rules"]))
		assert_eq(campaign.revision(), 0)
		assert_true(campaign.read_snapshot().is_empty())
		assert_true(campaign.initialize(example["before_result"], fixture["rules"]))


func test_raw_json_reordered_catalog_frozen_templates_and_nested_outputs_preserve_metadata() -> void:
	var fixture := _fixture(true)
	var example: Dictionary = fixture["cases"][0]
	var before: Dictionary = example["before_result"].duplicate(true)
	before["characters"].reverse()
	before["relationships"].reverse()
	before["school"]["school_control"]["presentation"] = {"zoom": 1.25}
	before["characters"][0]["portrait"] = {"offset": 0.75}
	var rules: Dictionary = fixture["rules"].duplicate(true)
	var campaign := Campaign.new()
	assert_true(campaign.initialize(before, rules))
	before["school"]["school_control"].clear()
	rules["school_boot"]["adventures"].clear()
	rules["school_boot"]["lectures"].clear()
	assert_true(campaign.begin_result("battle", example["context"])["supported"])
	assert_true(campaign.finish_result("battle", true, true)["supported"])
	assert_true(campaign.begin_school_return("school", "battle")["supported"])
	assert_true(campaign.advance_school_return("school", true, true, true)["supported"])
	var projected := campaign.project_school_return_boot("school")
	assert_true(projected["supported"])
	if not projected["supported"]:
		return
	var expected: Dictionary = example["expected_after"].duplicate(true)
	expected["characters"].reverse()
	expected["relationships"].reverse()
	expected["school"]["school_control"]["presentation"] = {"zoom": 1.25}
	expected["characters"][0]["portrait"] = {"offset": 0.75}
	assert_true(Roles._integers(campaign.read_snapshot()) == Roles._integers(expected))
	assert_eq(campaign.read_snapshot()["school"]["school_control"]["presentation"]["zoom"], 1.25)
	assert_eq(campaign.read_snapshot()["characters"][0]["portrait"]["offset"], 0.75)
	projected["result"]["after"]["characters"].clear()
	projected["campaign_snapshot"]["school"]["school_control"]["idle_student_ids"].clear()
	campaign.journal()[-1]["after"]["school"]["school_control"].clear()
	campaign.read_school_snapshot()["snapshot"]["school_control"].clear()
	assert_eq(campaign.project_school_return_boot("school")["status"], "duplicate")
	assert_true(Roles._integers(campaign.read_snapshot()) == Roles._integers(expected))


func test_boot_journal_preserves_native_before_after_and_role_alias_continuity() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := _campaign(fixture, example)
	assert_true(campaign.project_school_return_boot("school")["supported"])
	var log := campaign.journal()
	for index in range(1, log.size()):
		assert_true(log[index]["before"] == log[index - 1]["after"])
	var boot: Dictionary = log[-1]
	assert_eq(boot["phase"], "school_boot_data")
	assert_eq(boot["revision"], 5)
	assert_true(boot["before"] == example["before_boot"])
	assert_true(boot["after"] == example["expected_after"])
	assert_eq(boot["source"]["group_body_va"], "0x4ab7a0")
	assert_eq(boot["source"]["person_body_va"], "0x4b8d50")
	for key in ["characters", "relationships", "global_total_511c", "recipient_id", "month", "week"]:
		assert_true(boot["before"][key] == boot["after"][key])
	assert_eq(campaign.read_school_snapshot()["snapshot"]["adv_globals"]["0x7e1180"], 4)


func test_battle_return_projects_bound_school_and_late_deliveries_preserve_status() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := Campaign.new()
	assert_true(campaign.initialize(example["before_result"], fixture["rules"]))
	var handoff := Return.new()
	assert_false(handoff.project_school_return_boot_replay("school")["supported"])
	assert_true(handoff.accept_terminal_snapshot({"frame": 42, "winner": 0, "units": [
		{"battle_index": 0, "character_id": 3, "faction": 0}, {"battle_index": 1, "character_id": 4, "faction": 0},
		{"battle_index": 2, "character_id": 9, "faction": 0}, {"battle_index": 3, "character_id": -1, "faction": 1}]}))
	# Tactical predecessor inputs remain separately declared; this is not a
	# same-world live battle witness. The result-return segment has one-CPU data.
	var task: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/scene5_task_execution_evidence.json")))["cases"][0]
	var round_input: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/battle_round_execution_evidence.json")))["cases"][0]
	assert_true(handoff.prepare_result_replay(task["exit_frame"], task["dispatch_context"],
		round_input["before"], round_input["synthetic_round_table"], true)["supported"])
	assert_true(handoff.begin_result_replay("battle", example["context"], campaign)["supported"])
	assert_true(handoff.finish_result_replay("battle", true, true)["supported"])
	assert_true(handoff.begin_school_return_replay("school")["supported"])
	assert_false(handoff.project_school_return_boot_replay("school")["supported"])
	assert_true(handoff.advance_school_return_replay("school", true, true, true)["school_constructed"])
	assert_false(handoff.project_school_return_boot_replay("different")["supported"])
	assert_true(handoff.project_school_return_boot_replay("school")["school_boot_data_projected"])
	assert_eq(handoff.status(), "school_boot_data_projected")
	assert_eq(handoff.begin_school_return_replay("school")["status"], "duplicate")
	assert_eq(handoff.advance_school_return_replay("school", false, false, false)["status"], "duplicate")
	assert_eq(handoff.finish_result_replay("battle", false, false)["status"], "duplicate")
	assert_eq(handoff.status(), "school_boot_data_projected")
	assert_true(campaign.read_snapshot() == example["expected_after"])
	assert_eq(campaign.revision(), 5)
