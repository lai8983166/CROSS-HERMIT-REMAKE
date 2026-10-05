extends "res://sim/tests/test_base.gd"

const Sort = preload("res://sim/school_waitlist_sort.gd")
const Demo = preload("res://sim/campaign_return_demo.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func _data() -> Dictionary:
	return Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(Demo.WAITLIST_PATH)))


func _school(route := 0) -> Demo:
	var demo := Demo.new()
	assert_true(demo.start(route))
	var base: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var battle := Battle.start(Demo.battle_setup(base), 42)
	battle.run_to_finish()
	assert_true(demo.accept_terminal(battle.get_terminal_snapshot()))
	assert_true(demo.confirm_result())
	assert_true(demo.enter_school())
	return demo


func test_every_native_case_and_command_sequence_matches_without_mutating_inputs() -> void:
	var data := _data()
	for case in data["cases"]:
		var profiles: Array = case["declared_profiles"].duplicate(true)
		var saved := profiles.duplicate(true)
		for step in case["steps"]:
			var ids: Array = step["before"]["idle_student_ids"].duplicate()
			var old := ids.duplicate()
			var result := Sort.order(profiles, ids, step["command"] - 11, data["rules"])
			assert_eq(profiles, saved)
			assert_eq(ids, old)
			if step["command"] == 55:
				assert_false(result["supported"])
			else:
				assert_true(result["supported"])
				assert_eq(result["idle_student_ids"], step["after"]["idle_student_ids"], case["name"])
				assert_eq(result["idle_sort_mode"], step["after"]["idle_sort_mode"])


func test_invalid_modes_members_profiles_and_categories_reject() -> void:
	var data := _data()
	var case: Dictionary = data["cases"][0]
	var profiles: Array = case["declared_profiles"]
	var ids: Array = case["declared_initial"]["idle_student_ids"]
	for mode in [-1, 3, 1.5, "1", null, true]:
		assert_false(Sort.order(profiles, ids, mode, data["rules"])["supported"])
	for list in [[3, 3], [0], [12], [3, "5"], null]:
		assert_false(Sort.order(profiles, list, 0, data["rules"])["supported"])
	for pair in [["job", 31], ["level_50", 256], ["attributes", [1, 2]], ["attributes", [0, 0, 0, 0, 0, 0, -1]]]:
		var invalid := profiles.duplicate(true)
		invalid[0][pair[0]] = pair[1]
		assert_false(Sort.order(invalid, ids, 0, data["rules"])["supported"])
	var bad_rules: Dictionary = data["rules"].duplicate(true)
	bad_rules["job_categories"][4] = 6
	assert_false(Sort.order(profiles, ids, 1, bad_rules)["supported"])
	bad_rules = data["rules"].duplicate(true)
	bad_rules["source_image_sha256"] = "other"
	assert_false(Sort.order(profiles, ids, 1, bad_rules)["supported"])


func test_premature_requests_preserve_catalog_and_journal() -> void:
	var demo := Demo.new()
	assert_false(demo.sort_waitlist(1))
	assert_true(demo.start(0))
	var view := demo.view()
	assert_false(demo.sort_waitlist(1))
	assert_false(demo._campaign.sort_school_waitlist("demo-school", 1)["supported"])
	assert_eq(demo.view(), view)
	assert_eq(demo.journal(), [])


func test_both_routes_publish_only_list_and_mode_and_do_not_reaward() -> void:
	var data := _data()
	for route in range(2):
		var demo := _school(route)
		var baseline: Dictionary = demo.view()["snapshot"]
		var revision := 6
		for step in data["cases"][route]["steps"]:
			if step["command"] == 55:
				continue
			var before := demo.view()
			assert_true(demo.sort_waitlist(step["command"] - 11))
			var snapshot: Dictionary = demo.view()["snapshot"]
			var expected := baseline.duplicate(true)
			expected["school"]["school_control"]["idle_student_ids"] = step["after"]["idle_student_ids"]
			expected["school"]["school_control"]["idle_sort_mode"] = step["after"]["idle_sort_mode"]
			assert_eq(snapshot, expected)
			if snapshot != before["snapshot"]:
				revision += 1
			assert_eq(demo.view()["revision"], revision)
			assert_eq(demo.view()["summary"], before["summary"])
			assert_eq(demo.view()["loot"], before["loot"])
		assert_eq(revision, 9)
		assert_eq(demo.journal().filter(func(row): return row["phase"] == "school_waitlist_sort").size(), 3)
		assert_eq(demo.journal().filter(func(row): return row["phase"] == "state7_week").size(), 1)
		for key in ["live_witness", "authorizes_persistent_write", "school_initialized", "interactive_school_ready"]:
			assert_false(demo.view()[key])


func test_repetition_views_and_late_boot_duplicates_cannot_rollback_order() -> void:
	var demo := _school()
	assert_true(demo.sort_waitlist(1))
	var view := demo.view()
	var log := demo.journal()
	for i in range(3):
		assert_true(demo.sort_waitlist(1))
		assert_true(demo.confirm_result())
		assert_true(demo.enter_school())
		assert_true(demo._handoff.project_school_return_boot_replay("demo-school")["supported"])
		assert_true(demo._handoff.advance_school_return_replay("demo-school", true, true, true)["supported"])
		var copy := demo.view()
		copy["snapshot"]["school"]["school_control"]["idle_student_ids"].clear()
		demo.journal().clear()
		assert_eq(demo.view(), view)
		assert_eq(demo.journal(), log)


func test_invalid_current_catalog_or_rule_does_not_publish() -> void:
	var demo := _school()
	for pair in [["idle_student_ids", [3,3,4,9]], ["idle_student_ids", [3,4,9]],
			["idle_sort_mode", 3], ["person_ready", 0]]:
		var pristine: Dictionary = demo._campaign._snapshot.duplicate(true)
		demo._campaign._snapshot["school"]["school_control"][pair[0]] = pair[1]
		var view := demo.view()
		var log := demo.journal()
		assert_false(demo.sort_waitlist(1))
		assert_eq(demo.view(), view)
		assert_eq(demo.journal(), log)
		demo._campaign._snapshot = pristine
	var before := demo.view()
	assert_false(demo.sort_waitlist(3))
	assert_eq(demo.view(), before)
	demo._campaign._rules.erase("school_waitlist")
	assert_false(demo.sort_waitlist(0))
	assert_eq(demo.view(), before)


func test_stale_or_pending_owner_cannot_apply_sorting() -> void:
	var demo := _school()
	for key in ["_active", "_active_return", "_active_preparation"]:
		demo._campaign.set(key, "pending")
		var before := demo.view()
		assert_false(demo.sort_waitlist(1))
		assert_eq(demo.view(), before)
		demo._campaign.set(key, "")
	demo._campaign._revision += 1
	var stale := demo.view()
	assert_false(demo.sort_waitlist(1))
	assert_eq(demo.view(), stale)


func test_restart_discards_order_and_fixture_outcomes_are_not_retained() -> void:
	var demo := _school()
	assert_true(demo.sort_waitlist(1))
	assert_true(demo.start(1))
	assert_eq(demo.view()["revision"], 0)
	assert_eq(demo.journal(), [])
	assert_false(str(demo._source).contains("declared_profiles"))
	assert_false(str(demo._campaign._rules).contains("visited_original_addresses"))
	assert_false(demo.start(0, Demo.CHAIN_PATH, Demo.PREP_PATH, "res://missing-sort.json"))
	assert_eq(demo.view()["error"], "missing_source")
	assert_false(demo.start(0, Demo.CHAIN_PATH, Demo.PREP_PATH, "res://data/battle_setup.json"))
	assert_eq(demo.view()["error"], "source_integrity_mismatch")
