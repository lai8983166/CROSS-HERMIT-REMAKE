extends "res://sim/tests/test_base.gd"
const Adventures := preload("res://sim/school_return_adventures.gd")
const Courses := preload("res://sim/school_return_courses.gd")
const Helpers := preload("res://sim/tests/test_school_return_courses.gd")
const Return := preload("res://sim/school_postbattle_return.gd")


func test_complete_current_list_and_native_ledger_transitions() -> void:
	var ledger := Adventures.initial();var before := ledger.duplicate(true)
	assert_eq(ledger["entries"].map(func(r):return r["id"]),[8,17])
	assert_eq(ledger["entries"].map(func(r):return r["elapsed"]),[0,2])
	assert_eq(ledger["unlock_flags"].count(1),3)
	assert_eq(Adventures.available(ledger),[{"id":8,"category":2,"remaining":5,"cooldown":0},{"id":17,"category":1,"remaining":-1,"cooldown":1}])
	var consumed := Adventures.advance(ledger,8)
	assert_eq(consumed["entries"].map(func(r):return r["id"]),[17])
	var reused := Adventures.advance(ledger,17)
	assert_eq(reused["entries"].map(func(r):return r["id"]),[8,17])
	assert_eq([reused["entries"][1]["busy"],reused["entries"][1]["busy_elapsed"],reused["entries"][1]["elapsed"]],[0,1,3])
	for i in range(4):reused=Adventures.advance(reused,0)
	assert_eq(reused["entries"].map(func(r):return r["id"]),[17])
	assert_eq(ledger,before,"preview and submission projections do not mutate the current ledger")


func test_actual_four_person_assignment_and_both_scene_handoffs() -> void:
	var bundle := Helpers.new()._returned()
	bundle=Return.move_member(bundle,{"kind":"student","member_id":5,"target_group":0,"target_slot":3})["after"]
	var ledger := Adventures.initial()
	for id in [8,17]:
		var selection := Adventures.select(bundle,ledger,id)
		assert_true(selection["supported"])
		var chosen: Dictionary=selection["after"]
		var result := Adventures.submit(chosen,ledger)
		assert_true(result["supported"],str(result))
		if not result["supported"]:continue
		var handoff: Dictionary=result["handoff"]
		assert_eq(handoff["prepared"]["rounds"],[{"scene_id":id,"teacher_ids":[101],"student_ids":[3,4,9,5],"student_groups":[0,0,0,0]}])
		assert_eq(handoff["participants"],bundle["participants"])
		assert_eq(handoff["growth"],bundle["growth"])
		assert_eq(handoff["requested_states"],[10,16]);assert_eq(handoff["round_cursor"],1)
		assert_eq(handoff["scene"]["script"],"T%04d.BIN" % id)
		assert_eq(handoff["scene"]["template_count"],132 if id==8 else 61)
		assert_false(handoff["scene_playable"]);assert_false(handoff["battle_executed"])
		for key in ["growth","records","counts","item_flags","participants"]:assert_eq(result["after"][key],bundle[key])
		assert_eq(result["after"]["school"],chosen["school"])
		assert_false(Adventures.submit(result["after"],result["ledger_after"])["supported"])
	var waiting: Dictionary = Return.move_member(bundle,{"kind":"student","member_id":9,"target_group":-1,"target_slot":-1})["after"]
	waiting=Adventures.select(waiting,ledger,17)["after"]
	var prepared := Adventures.prepare(waiting,ledger)
	assert_eq(prepared["prepared"]["rounds"][0]["student_ids"],[3,4,5])
	assert_eq(prepared["idle_student_ids"],[9])


func test_unavailable_teaching_and_empty_class_do_not_commit() -> void:
	var bundle := Helpers.new()._returned();var original := bundle.duplicate(true);var ledger := Adventures.initial()
	for id in [0,5,7,18,101]:assert_false(Adventures.select(bundle,ledger,id)["supported"])
	assert_false(Adventures.prepare(bundle,ledger)["supported"])
	var chosen: Dictionary = Adventures.select(bundle,ledger,8)["after"]
	var teaching: Dictionary = Courses.set_mode(chosen,0,true)["after"]
	teaching=Courses.assign_course(teaching,0,1)["after"]
	assert_false(Adventures.submit(teaching,ledger)["supported"])
	var confirmed := Courses.settle(teaching)
	assert_true(confirmed["supported"])
	assert_false(Adventures.submit(confirmed["after"],ledger)["supported"])
	for id in [3,4,9]:chosen=Return.move_member(chosen,{"kind":"student","member_id":id,"target_group":-1,"target_slot":-1})["after"]
	assert_false(Adventures.submit(chosen,ledger)["supported"])
	assert_eq(bundle,original)
