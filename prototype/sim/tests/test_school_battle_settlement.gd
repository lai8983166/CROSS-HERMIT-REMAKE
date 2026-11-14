extends "res://sim/tests/test_base.gd"
const Settlement := preload("res://sim/school_battle_settlement.gd")
const Helpers := preload("res://sim/tests/test_school_combat_session.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")


func _inputs(ids: Array) -> Dictionary:
	var objectives := []; objectives.resize(16); objectives.fill(0)
	return {"result_selector":1,"time_key":1,"unit_condition_key":1,"objective_slots":objectives,
		"units":ids.map(func(id): return {"character_id":id,"count_field_aa":1,"contribution_field_ac":15 if id==3 else 2,"status_field_ae":0})}


func test_current_school_round_growth_confirmation_and_exactly_once_handoff() -> void:
	var school = Helpers.new()._school(); var before: Dictionary = school.state()
	var context: Dictionary = school.adventure_result_context(); var original := context.duplicate(true)
	var result := Settlement.new(); assert_true(result.initialize(context))
	var first := result.prepare(_inputs([3,4,9])); assert_true(first["supported"])
	assert_eq(first["phase"],"round_result"); assert_false(first["growth_applied"])
	assert_false(first.has("adv_request")); assert_true(first["score"]["total_delta"]>0)
	assert_false(result.confirm_total(true)["supported"],"no skipping the one-round boundary")
	assert_false(result.prepare(_inputs([3,4,9]))["supported"],"no duplicate award")
	var grown := result.confirm_round(); assert_true(grown["growth_applied"])
	assert_false(grown["confirmation_applied"]); assert_eq(result.confirm_round(),grown)
	assert_eq(result.confirm_total(false),grown,"MVP readiness is a separate gate")
	var confirmed := result.confirm_total(true)
	assert_eq(confirmed["adv_request"]["script"],"adv/dat/ch003.ybc")
	assert_eq(confirmed["adv_request"]["next_task"],7)
	assert_eq(confirmed["confirmation"]["after"]["month"],4)
	assert_eq(confirmed["confirmation"]["after"]["week"],5)
	assert_eq(result.confirm_total(true),confirmed)
	assert_eq(result.confirm_round(),confirmed)
	assert_eq(context,original); assert_eq(school.state(),before)
	var initial: Array = context["growth"]
	for row in confirmed["growth"]["after"]["characters"]:
		var old: Dictionary = initial.filter(func(r): return r["character_id"]==row["character_id"])[0]
		for k in range(7): assert_eq(row["growth_pools"][k],old["growth_pools"][k]+row["staged_package"][k])
	confirmed["confirmation"]["counts"][0]["count"] = 999
	assert_false(result.snapshot()["confirmation"]["counts"][0]["count"]==999,"owned result is not aliased")


func test_waiting_students_are_not_awarded_and_invalid_input_is_atomic() -> void:
	for count in [1,2]:
		var school = Helpers.new()._school()
		for id in [3,4,9].slice(count):
			assert_true(school.execute({"op":"plan_move","kind":"student","member_id":id,"target_group":-1,"target_slot":-1})["supported"])
		var context: Dictionary = school.adventure_result_context()
		var ids: Array = context["preparation"]["rounds"][0]["student_ids"]
		var result := Settlement.new(); assert_true(result.initialize(context))
		var wrong := _inputs(ids); wrong["units"][0]["character_id"] = 5
		assert_false(result.prepare(wrong)["supported"]); assert_eq(result.snapshot()["phase"],"waiting_battle")
		var prepared := result.prepare(_inputs(ids)); assert_true(prepared["supported"])
		assert_eq(prepared["score"]["characters"].size(),count)
		result.confirm_round(); var done := result.confirm_total(true)
		for id in [3,4,9].slice(count):
			var row: Dictionary = done["confirmation"]["records"].filter(func(r): return r["character_id"]==id)[0]
			assert_eq(row["week_records"][12],3)
		assert_false(done["week_advanced"])


func test_growth_record_helper_retains_original_fixture_outputs() -> void:
	var fixture: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string("res://data/role_application_evidence.json")))
	# Existing complete-world contract stays the oracle; compare only its pure growth.
	for example in fixture["cases"]:
		var before: Dictionary = example["before"]
		var ids: Array = before["characters"].map(func(r): return r["character_id"])
		if ids.size()>3: continue
		var full := Roles.project_growth(before,ids,4660,fixture["rules"])
		var records := Roles.project_growth_records(before["characters"],ids,4660,fixture["rules"])
		assert_true(full["supported"]); assert_true(records["supported"])
		assert_eq(records["after"]["characters"],full["after"]["characters"])
		assert_eq(records["learning_draws"],full["learning_draws"])


func test_invalid_current_context_refuses_before_replacing_owned_state() -> void:
	var school = Helpers.new()._school()
	var context: Dictionary = school.adventure_result_context()
	for mutate in [func(c): c["growth"][0].erase("character_id"),
		func(c): c["growth"][0]["skill_statuses"] = [],
		func(c): c["growth"][0]["job"] = 31,
		func(c): c["growth"][0]["growth_pools"][0] = -1,
		func(c): c["records"][0]["job_progress"] = [],
		func(c): c["counts"][0]["count"] = 6]:
		var broken := context.duplicate(true); mutate.call(broken)
		var result := Settlement.new()
		assert_false(result.initialize(broken)); assert_eq(result.snapshot()["phase"],"closed")
	var session = Helpers.new()._combat(school)
	var state: Dictionary = session.ending_snapshot()
	var combat: Dictionary = school.adventure_combat_limits()
	combat["result_context"]["preparation"]["class_ratings"][0]["relationship_mean"] += 1
	assert_false(session.open(school.adventure_preparation(),combat))
	assert_eq(session.ending_snapshot(),state)
