extends "res://sim/tests/test_base.gd"

const Layout = preload("res://sim/campaign_school_layout.gd")
const Campaign = preload("res://sim/campaign_result_state.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func _fixture(raw := false) -> Dictionary:
	var value: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/campaign_school_layout_evidence.json"))
	return value if raw else Roles._integers(value)


func _role(snapshot: Dictionary, identity: int) -> Dictionary:
	for record in snapshot["characters"]:
		if int(record["character_id"]) == identity:
			return record
	return {}


func test_both_layouts_match_every_independently_read_native_snapshot() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		for pair in [["before", "school_before"], ["after_result", "school_after_result"],
				["after_join_probe", "school_after_join_probe"], ["after_week_probe", "school_after_week_probe"]]:
			if example[pair[0]] == null:
				continue
			var canonical: Dictionary = example[pair[0]]
			var saved := canonical.duplicate(true)
			var view := Layout.school_view(canonical, fixture["rules"]["week"])
			assert_true(view["supported"], example["name"] + "/" + pair[0])
			if not view["supported"]:
				continue
			assert_true(view["snapshot"] == example[pair[1]], "complete independent school layout " + example["name"] + "/" + pair[0])
			assert_eq(view["snapshot"]["adv_globals"]["0x7e1180"], canonical["recipient_id"])
			for key in ["live_witness", "authorizes_persistent_write", "school_initialized"]:
				assert_false(view[key])
			assert_false(canonical["school"]["adv_globals"].has("0x7e1180"))
			for record in view["snapshot"]["participants"]:
				for key in Layout.RESULT_ONLY:
					assert_false(record.has(key))
			var restored := Layout.merge_school(canonical, view["snapshot"], fixture["rules"]["week"])
			assert_true(restored["supported"])
			if restored["supported"]:
				assert_true(restored["snapshot"] == canonical, "lossless catalog round trip")
			assert_true(canonical == saved, "mapping never mutates input")


func test_shared_result_publication_matches_three_native_full_catalog_paths() -> void:
	var fixture := _fixture()
	for example in fixture["cases"]:
		var campaign := Campaign.new()
		assert_true(campaign.initialize(example["before"], fixture["rules"]))
		var started := campaign.begin_result("battle", example["context"])
		assert_true(started["supported"], example["name"])
		if not started["supported"]:
			continue
		assert_eq(started["result"]["after"]["characters"].size(), 3)
		assert_eq(campaign.read_snapshot()["characters"].size(), 4)
		assert_eq(campaign.read_snapshot()["relationships"].size(), 20)
		assert_true(_role(campaign.read_snapshot(), 5) == _role(example["before"], 5), "inactive candidate unchanged at initialization")
		var complete := campaign.finish_result("battle", example["confirmed"], example["mvp_ready"])
		assert_true(complete["supported"], example["name"])
		if not complete["supported"]:
			continue
		assert_true(campaign.read_snapshot() == example["after_result"], "complete native result catalog " + example["name"])
		assert_true(campaign.read_school_snapshot()["snapshot"] == example["school_after_result"], "independent native school result " + example["name"])
		assert_eq(complete["result"]["requested_state"], example["result_requested_state"])
		assert_eq(complete["result"]["branch"], example["result_branch"])
		assert_eq(complete["result"]["week_executed"], example["result_native_week"])
		assert_eq(complete["result"]["learning_draws"], example["learning_draws"].map(func(draw): return draw["rand"]))
		assert_eq(complete["result"]["rand_state"], example["native_rand_state"])
		assert_eq(campaign.revision(), 1 if int(example["result_requested_state"]) == 12 else 2)
		for key in ["live_witness", "authorizes_persistent_write", "school_initialized"]:
			assert_false(complete[key])
		assert_true(_role(campaign.read_snapshot(), 5) == _role(example["before"], 5), "inactive candidate unchanged after result and native week")


func test_full_catalog_journal_retains_native_phase_order_and_week_before_image() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][2]
	var campaign := Campaign.new()
	assert_true(campaign.initialize(example["before"], fixture["rules"]))
	assert_true(campaign.begin_result("battle", example["context"])["supported"])
	assert_true(campaign.finish_result("battle", true, true)["supported"])
	var log := campaign.journal()
	assert_eq(log.map(func(entry): return entry["phase"]), ["initialized", "result_fields", "week_settlement"])
	assert_eq(log.map(func(entry): return entry["revision"]), [1, 2, 2])
	assert_true(log[0]["before"] == example["before"])
	assert_true(log[1]["before"] == log[0]["after"])
	assert_true(log[1]["after"] == example["result_before_week"])
	assert_true(log[2]["before"] == example["result_before_week"])
	assert_true(log[2]["after"] == example["after_result"])
	for entry in log:
		assert_eq(entry["before"]["characters"].size(), 4)
		assert_eq(entry["after"]["relationships"].size(), 20)


func test_malformed_school_catalogs_reject_before_result_instance_or_publication() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	for kind in range(16):
		var before: Dictionary = example["before"].duplicate(true)
		match kind:
			0: before["school"]["student_count"] = 4
			1: before["school"]["student_ids"][1] = 3
			2: before["school"]["student_ids"][3] = 5
			3: before["availability"][5] = 1
			4: before["availability"][9] = 0
			5: before["school"]["teacher_count"] = 1
			6: before["school"]["teacher_ids"][0] = 10
			7: before["school"]["group_student_indices"][0][0] = 1
			8: before["school"]["group_student_ids"][0][0] = 5
			9: before["school"]["adv_globals"]["0x7e1180"] = 4
			10: before["school"]["adv_globals"].erase("0x7e1182")
			11: _role(before, 5)["unlock_reserved_bytes"] = [1]
			12: before["relationships"].pop_back()
			13: before["school"]["student_count"] = 3.5
			14: before["school"]["group_student_indices"][0][0] = 20
			15: before["school"]["adv_globals"]["0x7a5292"] = 32768
		var campaign := Campaign.new()
		assert_false(campaign.initialize(before, fixture["rules"]), "invalid layout " + str(kind))
		assert_true(campaign.read_snapshot().is_empty())
		assert_eq(campaign.revision(), 0)
		assert_true(campaign.initialize(example["before"], fixture["rules"]), "retry after layout validation")
		assert_true(campaign.begin_result("battle", example["context"])["supported"])


func test_result_subset_cannot_drop_an_available_week_role_or_create_unknown_role() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	assert_true(Layout.result_view(example["before"], [3, 4, 9], fixture["rules"]["week"])["supported"])
	for ids in [[3, 4], [3, 3, 9], [3, 4, 12], [3, 4, 9.5], []]:
		assert_false(Layout.result_view(example["before"], ids, fixture["rules"]["week"])["supported"])
	assert_false(Layout.result_view(example["after_join_probe"], [3, 4, 9], fixture["rules"]["week"])["supported"])
	assert_true(Layout.result_view(example["after_join_probe"], [3, 4, 9, 5], fixture["rules"]["week"])["supported"])
	var campaign := Campaign.new()
	assert_true(campaign.initialize(example["before"], fixture["rules"]))
	var bad: Dictionary = example["context"].duplicate(true)
	bad["participant_ids"] = [3, 4]
	assert_false(campaign.begin_result("retry", bad)["supported"])
	assert_true(campaign.read_snapshot() == example["before"])
	assert_true(campaign.journal().is_empty())
	assert_true(campaign.begin_result("retry", example["context"])["supported"])


func test_merges_reject_role_history_injection_missing_fields_and_bad_aliases() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][0]
	var before: Dictionary = example["after_result"].duplicate(true)
	for kind in range(6):
		var view: Dictionary = example["school_after_join_probe"].duplicate(true)
		match kind:
			0: view["participants"][0]["week_records"] = _role(before, 3)["week_records"].duplicate()
			1: view["participants"].remove_at(3)
			2: view["participants"][3]["character_id"] = 3
			3: view["participants"][0].erase("growth_pools")
			4: view["adv_globals"]["0x7e1180"] = 13
			5: view["student_ids"][1] = 3
		assert_false(Layout.merge_school(before, view, fixture["rules"]["week"])["supported"], "invalid school merge " + str(kind))
	var result: Dictionary = Layout.result_view(before, [3, 4, 9], fixture["rules"]["week"])["snapshot"]
	result["characters"][0]["character_id"] = 12
	assert_false(Layout.merge_result(before, result, fixture["rules"]["week"])["supported"])
	assert_true(before == example["after_result"], "failed merges do not modify canonical state")
	var joined := Layout.merge_school(before, example["school_after_join_probe"], fixture["rules"]["week"])
	assert_true(joined["supported"])
	if joined["supported"]:
		assert_true(joined["snapshot"] == example["after_join_probe"], "join keeps all result-only fields and 20 relationships")


func test_terminal_calendar_is_readable_but_cannot_start_another_result() -> void:
	var fixture := _fixture()
	var example: Dictionary = fixture["cases"][2]
	assert_true(Layout.school_view(example["after_result"], fixture["rules"]["week"])["supported"])
	assert_eq(Roles._validate_snapshot(example["after_result"]), "history_overlaps_progress_fields")
	var campaign := Campaign.new()
	assert_true(campaign.initialize(example["before"], fixture["rules"]))
	assert_true(campaign.begin_result("a", example["context"])["supported"])
	assert_true(campaign.finish_result("a", true, true)["supported"])
	assert_false(campaign.begin_result("b", example["context"])["supported"])
	assert_true(campaign.read_snapshot() == example["after_result"])
	assert_eq(campaign.revision(), 2)


func test_raw_json_reordered_catalog_and_fractional_metadata_remain_isolated() -> void:
	var fixture := _fixture(true)
	var example: Dictionary = fixture["cases"][0]
	var before: Dictionary = example["before"].duplicate(true)
	before["characters"].reverse()
	before["relationships"].reverse()
	before["presentation"] = {"zoom": 1.25}
	_role(before, 5)["portrait"] = {"offset": 0.75}
	var rules: Dictionary = fixture["rules"].duplicate(true)
	var campaign := Campaign.new()
	assert_true(campaign.initialize(before, rules))
	before["characters"].clear()
	rules["week"]["unlock_rules"].clear()
	assert_true(campaign.begin_result("battle", example["context"])["supported"])
	assert_true(campaign.finish_result("battle", true, true)["supported"])
	var expected: Dictionary = example["after_result"].duplicate(true)
	expected["characters"].reverse()
	expected["relationships"].reverse()
	expected["presentation"] = {"zoom": 1.25}
	_role(expected, 5)["portrait"] = {"offset": 0.75}
	assert_true(Roles._integers(campaign.read_snapshot()) == Roles._integers(expected), "raw JSON integral semantic comparison")
	assert_eq(campaign.read_snapshot()["presentation"]["zoom"], 1.25)
	assert_eq(_role(campaign.read_snapshot(), 5)["portrait"]["offset"], 0.75)
	campaign.read_school_snapshot()["snapshot"]["participants"][0]["attributes"].clear()
	campaign.read_snapshot()["school"]["student_ids"].clear()
	campaign.journal()[0]["after"]["relationships"].clear()
	var saved := campaign.read_snapshot()
	var second := campaign.begin_result("new", example["context"])
	assert_true(second["supported"])
	var current := campaign.read_snapshot()
	assert_eq(campaign.finish_result("battle", false, false)["status"], "duplicate")
	assert_true(campaign.read_snapshot() == current, "old duplicate cannot revert newer full catalog")
	assert_false(current == saved)
	assert_eq(campaign.revision(), 3)
