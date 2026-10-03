extends "res://sim/tests/test_base.gd"

const Campaign = preload("res://sim/campaign_result_state.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func _fixture() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/result_transaction_evidence_v2.json")))


func test_shared_state_matches_all_six_native_role_and_week_paths() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		var campaign := Campaign.new()
		assert_true(campaign.initialize(example["before"], fixture["rules"]))
		var started := campaign.begin_result("battle", example["context"])
		assert_true(started["supported"])
		assert_eq(campaign.read_snapshot(), started["result"]["after"])
		var finished := campaign.finish_result("battle", example["confirmed"], example["mvp_ready"])
		assert_true(finished["supported"])
		assert_eq(campaign.read_snapshot(), example["expected_after"])
		assert_eq(finished["result"]["before_week"], example["expected_before_week"])
		assert_eq(finished["result"]["requested_state"], example["expected_requested_state"])
		assert_eq(finished["result"]["week_executed"], example["expected_week_executed"])
		assert_eq(campaign.revision(), 2 if finished["result"]["completed"] else 1)
		assert_false(finished["authorizes_persistent_write"])
		assert_false(finished["live_witness"])


func test_result_initialization_and_confirmed_post_week_publish_in_native_order() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][5]
	var campaign := Campaign.new()
	assert_true(campaign.initialize(example["before"], fixture["rules"]))
	assert_true(campaign.begin_result("battle", example["context"])["supported"])
	assert_eq(campaign.journal().map(func(entry): return entry["phase"]), ["initialized"])
	var finished := campaign.finish_result("battle", false, false)
	assert_true(finished["supported"])
	var log := campaign.journal()
	assert_eq(log.map(func(entry): return entry["phase"]), ["initialized", "result_fields", "week_settlement"])
	assert_eq(log.map(func(entry): return entry["revision"]), [1, 2, 2])
	assert_eq(log[0]["before"], example["before"])
	assert_eq(log[1]["before"], log[0]["after"])
	assert_eq(log[1]["after"], example["expected_before_week"])
	assert_eq(log[2]["before"], example["expected_before_week"])
	assert_eq(log[2]["after"], example["expected_after"])


func test_confirmation_and_mvp_waits_lock_campaign_against_a_second_result() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := Campaign.new()
	assert_true(campaign.initialize(example["before"], fixture["rules"]))
	var initialized := campaign.begin_result("a", example["context"])
	assert_true(initialized["supported"])
	assert_eq(campaign.finish_result("a", false, true)["status"], "waiting_confirmation")
	assert_eq(campaign.read_snapshot(), initialized["result"]["after"])
	assert_eq(campaign.revision(), 1)
	assert_false(campaign.begin_result("b", example["context"])["supported"])
	assert_false(campaign.finish_result("b", true, true)["supported"])
	assert_eq(campaign.finish_result("a", true, false)["status"], "waiting_mvp")
	assert_eq(campaign.revision(), 1)
	assert_eq(campaign.journal().size(), 1)
	assert_true(campaign.finish_result("a", false, true)["result"]["completed"])
	assert_eq(campaign.read_snapshot(), example["expected_after"])
	assert_eq(campaign.revision(), 2)


func test_invalid_state_missing_ids_and_unknown_branch_never_publish_or_reserve_instance() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for changes in [{"task_state": 10}, {"task_state": 16}, {"current": 0}, {"mode": 2},
			{"result_flag": 2}, {"participant_ids": [3, 4, 5]}]:
		var campaign := Campaign.new()
		assert_true(campaign.initialize(example["before"], fixture["rules"]))
		var context: Dictionary = example["context"].duplicate(true)
		context.merge(changes, true)
		assert_false(campaign.begin_result("bad", context)["supported"])
		assert_eq(campaign.read_snapshot(), example["before"])
		assert_eq(campaign.revision(), 0)
		assert_true(campaign.journal().is_empty())
		assert_true(campaign.begin_result("bad", example["context"])["supported"])


func test_snapshots_rules_journal_and_cached_outputs_do_not_alias_callers() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][5]
	var snapshot: Dictionary = example["before"].duplicate(true)
	var rules: Dictionary = fixture["rules"].duplicate(true)
	var campaign := Campaign.new()
	assert_true(campaign.initialize(snapshot, rules))
	snapshot["characters"].clear()
	rules["week"]["unlock_rules"].clear()
	var context: Dictionary = example["context"].duplicate(true)
	var first := campaign.begin_result("battle", context)
	context["participant_ids"].clear()
	first["campaign_snapshot"]["characters"].clear()
	first["result"]["after"]["week"] = 1
	var complete := campaign.finish_result("battle", true, true)
	complete["campaign_snapshot"]["item_flags"].clear()
	campaign.read_snapshot()["characters"].clear()
	campaign.journal()[0]["after"]["characters"].clear()
	for delivery in range(3):
		assert_eq(campaign.begin_result("battle", example["context"])["status"], "duplicate")
		assert_eq(campaign.finish_result("battle", false, false)["result"]["after"], example["expected_after"])
		assert_eq(campaign.read_snapshot(), example["expected_after"])
		assert_eq(campaign.revision(), 2)
		assert_eq(campaign.journal().size(), 3)
	assert_false(campaign.initialize(example["before"], fixture["rules"]))


func test_completed_old_delivery_does_not_roll_back_a_later_campaign_result() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var campaign := Campaign.new()
	assert_true(campaign.initialize(example["before"], fixture["rules"]))
	assert_true(campaign.begin_result("a", example["context"])["supported"])
	assert_true(campaign.finish_result("a", true, true)["supported"])
	var second := campaign.begin_result("b", example["context"])
	assert_true(second["supported"])
	var newer := campaign.read_snapshot()
	assert_eq(campaign.revision(), 3)
	var old := campaign.finish_result("a", true, true)
	assert_eq(old["result"]["after"], example["expected_after"])
	assert_eq(old["campaign_snapshot"], newer)
	assert_eq(campaign.revision(), 3)
	assert_true(campaign.finish_result("b", true, true)["supported"])
	var final := campaign.read_snapshot()
	assert_eq(campaign.begin_result("a", example["context"])["status"], "duplicate")
	assert_eq(campaign.read_snapshot(), final)
	assert_eq(campaign.revision(), 4)


func test_reordered_records_and_fractional_metadata_survive_shared_publication() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][5]
	var before: Dictionary = example["before"].duplicate(true)
	var expected: Dictionary = example["expected_after"].duplicate(true)
	before["characters"].reverse()
	expected["characters"].reverse()
	before["presentation"] = {"zoom": 1.25}
	expected["presentation"] = {"zoom": 1.25}
	var campaign := Campaign.new()
	assert_true(campaign.initialize(before, fixture["rules"]))
	assert_true(campaign.begin_result("battle", example["context"])["supported"])
	assert_true(campaign.finish_result("battle", true, true)["supported"])
	assert_eq(campaign.read_snapshot(), expected)
