extends "res://sim/tests/test_base.gd"

const Demo = preload("res://sim/campaign_return_demo.gd")
const Roles = preload("res://sim/all_result_role_replay.gd")


func _battle() -> Battle:
	var setup: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var battle := Battle.start(Demo.battle_setup(setup), 42)
	battle.run_to_finish()
	assert_true(battle.finished)
	return battle


func test_two_routes_use_actual_battle_and_match_native_full_catalogs_without_oracles() -> void:
	var data: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(Demo.CHAIN_PATH)))
	var preparation: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(Demo.PREP_PATH)))
	var terminal := _battle().get_terminal_snapshot()
	for route in range(2):
		var demo := Demo.new()
		assert_true(demo.start(route))
		assert_eq(demo.view()["snapshot"], preparation["cases"][route]["before_world"])
		assert_false(demo.confirm_result())
		assert_false(demo.enter_school())
		assert_true(demo.accept_terminal(terminal))
		assert_eq(demo.view()["summary"]["total_after"], preparation["cases"][route]["expected_summary"]["total_after"])
		assert_eq(demo.view()["loot"], preparation["cases"][route]["expected_summary"]["loot_groups"])
		assert_false(demo.enter_school())
		assert_true(demo.confirm_result())
		assert_eq(demo.view()["snapshot"], data["cases"][route]["after_result"])
		assert_true(demo.enter_school())
		assert_eq(demo.view()["snapshot"], data["cases"][route]["expected_after"])
		assert_eq(demo.view()["revision"], 6)
		assert_eq(demo.journal().filter(func(row): return row["phase"] == "state7_week").size(), 1)
		assert_eq(demo.view()["terminal"], terminal)
		for key in ["school_initialized", "interactive_school_ready", "live_witness", "authorizes_persistent_write"]:
			assert_false(demo.view()[key])
		assert_false(str(demo._source).contains("expected_after"))
		assert_false(str(demo._source).contains("declared_terminal_snapshot"))


func test_duplicates_views_and_reset_cannot_reaward_or_carry_old_session() -> void:
	var demo := Demo.new()
	assert_true(demo.start(0))
	var initial: Dictionary = demo.view()["snapshot"]
	assert_true(demo.accept_terminal(_battle().get_terminal_snapshot()))
	assert_true(demo.confirm_result())
	assert_true(demo.enter_school())
	var finished := demo.view()
	var log := demo.journal()
	for i in range(3):
		assert_true(demo.confirm_result())
		assert_true(demo.enter_school())
		var view := demo.view()
		view["snapshot"]["month"] = 99
		view["summary"]["total_after"] = 0
		view["before"]["characters"].clear()
		demo.journal().clear()
		assert_eq(demo.view(), finished)
		assert_eq(demo.journal(), log)
	assert_false(demo.accept_terminal(_battle().get_terminal_snapshot()))
	assert_true(demo.start(1))
	assert_eq(demo.view()["revision"], 0)
	assert_eq(demo.view()["snapshot"], initial)
	assert_eq(demo.view()["terminal"], {})
	assert_eq(demo.journal(), [])
	demo.reset()
	assert_eq(demo.view()["stage"], "idle")
	assert_eq(demo.view()["snapshot"], {})


func test_invalid_source_route_and_role_fail_without_success_or_rewards() -> void:
	var demo := Demo.new()
	assert_false(demo.start(2))
	assert_false(demo.start(0, "res://missing-source.json"))
	assert_eq(demo.view()["error"], "missing_source")
	assert_false(demo.start(0, "res://data/battle_setup.json"))
	assert_eq(demo.view()["error"], "source_integrity_mismatch")
	assert_true(demo.start(0))
	var initial: Dictionary = demo.view()["snapshot"]
	var terminal := _battle().get_terminal_snapshot()
	terminal["units"][0]["character_id"] = 5
	assert_false(demo.accept_terminal(terminal))
	assert_eq(demo.view()["stage"], "error")
	assert_eq(demo.view()["snapshot"], initial)
	assert_eq(demo.view()["revision"], 0)
	assert_false(demo.confirm_result())
	assert_false(demo.enter_school())


func test_demo_setup_keeps_default_data_and_enemy_units() -> void:
	var base: Dictionary = JSON.parse_string(FileAccess.get_file_as_string("res://data/battle_setup.json"))
	var saved := base.duplicate(true)
	var setup := Demo.battle_setup(base)
	assert_eq(base, saved)
	assert_eq(setup["units"].size(), 7)
	assert_eq(setup["units"].slice(0, 3).map(func(unit): return unit["character_id"]), [3, 4, 9])
	assert_eq(setup["units"].slice(3), base["units"].slice(4))
	base["units"] = base["units"].slice(0, 2)
	assert_eq(Demo.battle_setup(base), {})
