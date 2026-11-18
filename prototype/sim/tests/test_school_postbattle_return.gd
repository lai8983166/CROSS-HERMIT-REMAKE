extends "res://sim/tests/test_base.gd"
const Return := preload("res://sim/school_postbattle_return.gd")
const Helpers := preload("res://sim/tests/test_school_combat_session.gd")
const Battle := preload("res://sim/school_battle_settlement.gd")
const BattleTests := preload("res://sim/tests/test_school_battle_settlement.gd")
const Groups := preload("res://sim/school_teacher_group_replay.gd")


func _bundle(waiting := false) -> Dictionary:
	var model = Helpers.new()._school()
	if waiting:
		assert_true(model.execute({"op":"plan_move","kind":"student","member_id":9,"target_group":-1,"target_slot":-1})["supported"])
	var context: Dictionary = model.adventure_result_context()
	var result := Battle.new()
	assert_true(result.initialize(context))
	assert_true(result.prepare(BattleTests.new()._inputs(context["preparation"]["rounds"][0]["student_ids"]))["supported"])
	result.confirm_round()
	var confirmed := result.confirm_total(true)
	var growth: Array = context["growth"].duplicate(true)
	for row in confirmed["growth"]["after"]["characters"]:
		for index in range(growth.size()):
			if growth[index]["character_id"]==row["character_id"]: growth[index]=row.duplicate(true)
	return {"school":confirmed["confirmation"]["after"],"growth":growth,
		"records":confirmed["confirmation"]["records"],"counts":confirmed["confirmation"]["counts"],
		"participants":model._school_entry["after"]["participants"].duplicate(true),
		"flags":model._school_entry["after"]["flags"].duplicate(true),"item_flags":confirmed["item_flags"]}


func test_real_current_growth_history_and_teacher_survive_join_and_week() -> void:
	var before := _bundle(true)
	var original := before.duplicate(true)
	var joined := Return.join(before)
	assert_true(joined["supported"],str(joined.get("reason")))
	if not joined["supported"]: return
	var after: Dictionary = joined["after"]
	assert_eq(after["school"]["student_ids"].slice(0,4),[3,4,9,5])
	assert_eq(after["school"]["teacher_ids"],before["school"]["teacher_ids"])
	assert_eq(after["records"].slice(0,3),before["records"])
	assert_eq(after["counts"].slice(0,3),before["counts"])
	assert_eq(after["school"]["relationships"].slice(0,12),before["school"]["relationships"])
	assert_eq(after["school"]["relationships"].size(),20)
	assert_eq(after["participants"][3]["equipped_skills"],[11,0,0,0,0,0,0,0])
	assert_eq(after["participants"][3]["skill_statuses"][10],6,"difficulty1 retains template skill")
	assert_eq(after["participants"][3]["job_progress"].slice(0,5),[0,0,1,0,1])
	assert_eq(after["records"][3]["week_records"],Return.Origin._filled(177,0))
	for i in range(3):
		assert_eq(after["participants"][i]["growth_pools"],before["growth"][i]["growth_pools"])
		assert_eq(after["participants"][i]["skill_statuses"],before["growth"][i]["skill_statuses"])
		assert_eq(after["participants"][i]["job_progress"],before["records"][i]["job_progress"].slice(0,31))
	var week := Return.next_week(after)
	assert_true(week["supported"],str(week.get("reason")))
	if not week["supported"]: return
	assert_eq([week["after"]["school"]["month"],week["after"]["school"]["week"]],[5,1])
	assert_eq(week["after"]["records"],after["records"])
	assert_eq(week["after"]["counts"],after["counts"])
	assert_eq(week["after"]["school"]["global_total_511c"],before["school"]["global_total_511c"])
	assert_eq(before,original,"all operations are pure")
	assert_false(Return.join(after)["supported"])
	assert_false(Return.next_week(week["after"])["supported"])


func test_return_course_availability_and_four_member_movement() -> void:
	var joined := Return.join(_bundle())
	assert_true(joined["supported"],str(joined.get("reason")))
	if not joined["supported"]: return
	var week := Return.next_week(joined["after"])
	assert_true(week["supported"],str(week.get("reason")))
	if not week["supported"]: return
	var returned := Return.school_return(week["after"])
	assert_true(returned["supported"],str(returned.get("reason")))
	if not returned["supported"]: return
	var before: Dictionary = returned["after"]
	assert_eq(returned["unlocked_work_ids"],[1,2,3,4,5])
	assert_eq(before["school"]["course_counts"][0],8)
	assert_eq(before["school"]["idle_student_ids"],[5])
	assert_eq(before["school"]["derived_student_ids"][0],[3,4,9,-1])
	assert_eq(before["school"]["derived_teacher_ids"],[101,-1,-1,-1,-1])
	assert_eq(before["newly_dated_adventures"].map(func(r):return r["id"]),[8])
	assert_false(returned["adventure_catalog_complete"])
	assert_false(returned["interactive_school_ready"])
	assert_false(Return.school_return(before)["supported"])
	var moved := Return.move_member(before,{"kind":"student","member_id":5,"target_group":0,"target_slot":3})
	assert_true(moved["supported"],str(moved.get("reason")))
	if not moved["supported"]: return
	assert_eq(moved["after"]["school"]["derived_student_ids"][0],[3,4,9,5])
	assert_eq(moved["after"]["school"]["idle_student_ids"],[])
	assert_eq(moved["after"]["participants"],before["participants"])
	assert_eq(moved["after"]["records"],before["records"])
	var relocated := Return.move_member(moved["after"],{"kind":"teacher","member_id":101,"target_group":1,"target_slot":-1})
	assert_true(relocated["supported"],str(relocated.get("reason")))
	if not relocated["supported"]: return
	assert_eq(relocated["after"]["school"]["derived_teacher_ids"],[-1,101,-1,-1,-1])
	assert_eq(relocated["after"]["school"]["idle_student_ids"].size(),4)
	assert_eq(before["school"]["derived_student_ids"][0],[3,4,9,-1])


func test_malformed_bundle_and_wrong_phase_refuse_without_changes() -> void:
	var before := _bundle()
	for mutate in [func(b):b.erase("flags"),func(b):b["school"]["difficulty"]=3,
		func(b):b["growth"][0]["skill_statuses"]=[],func(b):b["records"][0]["job_progress"]=[],
		func(b):b["participants"][0]["equipped_skills"] = [],func(b):b["item_flags"] = [],
		func(b):b["school"]["teacher_ids"][0]=-1,func(b):b["counts"][0]["count"]=6]:
		var bad := before.duplicate(true)
		mutate.call(bad)
		var original := bad.duplicate(true)
		assert_false(Return.join(bad)["supported"])
		assert_eq(bad,original)
	assert_false(Return.next_week(before)["supported"])
	assert_false(Return.school_return(before)["supported"])


func test_chapter029_registers_two_waiting_members_without_overwriting_the_active_class() -> void:
	var calendar := preload("res://sim/school_sortie_week.gd")
	var adventures := preload("res://sim/school_return_adventures.gd")
	var joined := Return.join(_bundle())
	var bundle: Dictionary = Return.school_return(Return.next_week(joined["after"])["after"])["after"]
	var ledger := adventures.initial()
	for start_week in [1,2,3]:
		bundle["phase"]="courses_confirmed"
		var advanced := calendar.next_week(bundle)
		assert_true(advanced["supported"],str(advanced.get("reason")))
		if not advanced["supported"]: return
		if start_week==3:
			var current: Dictionary=advanced["after"]
			assert_false(Return.join_week_four(current,Return._rules())["supported"])
			assert_eq(current["records"].slice(0,4),bundle["records"])
			assert_eq(current["school"]["group_raw_bytes"],bundle["school"]["group_raw_bytes"])
			assert_eq(current["school"]["relationships"].size(),42)
			assert_eq(current["growth"][-1]["attributes"],[1,1,1,1,1,1,1])
			assert_eq(current["participants"][-1]["equipped_items"],[0,0,0,0,0,0,0,0])
			assert_eq(current["counts"][-1],{"character_id":8,"count":0})
		var room := calendar.finish_story(advanced["after"])
		var opening := calendar.school_return(room["after"],adventures.advance(ledger,0),ledger)
		assert_true(opening["supported"],str(opening.get("reason")))
		if not opening["supported"]: return
		bundle=opening["after"]
		ledger=opening["ledger_after"]
	var stale: Dictionary=bundle.duplicate(true)
	stale["school"]["member_profiles"][-1].erase("attributes")
	assert_eq(Return.validate_planning_roster(stale,Return._rules()),"invalid_chapter029_teacher_profile")
	assert_eq(bundle["school"]["idle_teacher_ids"],[110])
	assert_true(bundle["school"]["idle_student_ids"].has(8))
	var teacher := Return.move_member(bundle,{"kind":"teacher","member_id":110,"target_group":1})
	assert_true(teacher["supported"],str(teacher.get("reason")))
	if not teacher["supported"]: return
	var student := Return.move_member(teacher["after"],{"kind":"student","member_id":8,"target_group":1,"target_slot":0})
	assert_true(student["supported"],str(student.get("reason")))
	if not student["supported"]: return
	assert_eq(student["after"]["school"]["derived_teacher_ids"][1],110)
	assert_eq(student["after"]["school"]["derived_student_ids"][1],[8,-1,-1,-1])
	assert_eq(student["after"]["ratings"][1]["work_fields"],[3,6,7,0])
