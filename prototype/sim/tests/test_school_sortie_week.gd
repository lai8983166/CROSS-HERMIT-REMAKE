extends "res://sim/tests/test_base.gd"
const Calendar := preload("res://sim/school_sortie_week.gd")
const Adventures := preload("res://sim/school_return_adventures.gd")
const Courses := preload("res://sim/school_return_courses.gd")
const Return := preload("res://sim/school_postbattle_return.gd")
const Helpers := preload("res://sim/tests/test_school_return_courses.gd")


func test_routed_source_pages_and_chapter_boundaries() -> void:
	var story := Calendar.story()
	assert_true(story["supported"])
	if not story["supported"]: return
	assert_eq(story["school_entry"],[])
	for stage in [["pre_week",23,110,236],["week_start",24,140,243]]:
		var pages: Array = story[stage[0]]
		assert_eq(pages.size(),stage[2])
		var indices := []
		for page in pages:
			assert_eq(page["chapter"],stage[1])
			indices.append_array(page["text_indices"])
		assert_eq(indices,range(stage[3]))


func test_sourced_week_and_planning_after_either_consumed_adventure() -> void:
	var original := Helpers.new()._returned()
	var ledger := Adventures.initial()
	for id in [8,17]:
		var selected := Adventures.select(original,ledger,id)
		var committed := Adventures.submit(selected["after"],ledger)
		var source: Dictionary = committed["after"].duplicate(true)
		assert_false(Calendar.next_week(source)["supported"])
		# Declared post-settlement input. The end-to-end test owns result settlement.
		source["phase"]="sortie_settled"
		var saved := source.duplicate(true)
		var week := Calendar.next_week(source)
		assert_true(week["supported"],str(week.get("reason")))
		if not week["supported"]: continue
		assert_eq(source,saved)
		assert_eq(week["date"],[5,2])
		assert_false(Calendar.next_week(week["after"])["supported"])
		var advanced: Dictionary = week["after"]
		assert_eq(advanced["records"],source["records"])
		assert_eq(advanced["counts"],source["counts"])
		assert_false(Calendar.school_return(advanced,committed["ledger_after"])["supported"])
		var room := Calendar.finish_story(advanced)
		assert_true(room["supported"],str(room.get("reason")))
		if not room["supported"]: continue
		assert_false(Calendar.school_return(room["after"],ledger)["supported"])
		var opened := Calendar.school_return(room["after"],committed["ledger_after"])
		assert_true(opened["supported"],str(opened.get("reason")))
		if not opened["supported"]: continue
		var after: Dictionary = opened["after"]
		assert_eq(opened["ledger_after"],committed["ledger_after"],"week entry does not age a second time")
		assert_eq(after["newly_dated_adventures"],[])
		assert_eq(opened["unlocked_work_ids"],[13])
		assert_eq([after["adv_background"],after["flags"]["0x7a55f6"],after["flags"]["0x7e11a0"]],[8,16,1])
		assert_eq(after["school"]["lecture_active"],1 if id==17 else 0)
		assert_eq(after["school"]["student_ids"].slice(0,4),[3,4,9,5])
		assert_false(Calendar.school_return(after,opened["ledger_after"])["supported"])
		var listed := Courses.list_courses(after,0)
		assert_true(listed["supported"])
		var ids := []
		for category in listed["courses"]:
			for row in category: ids.append(row[1])
		ids.sort()
		assert_eq(ids,[1,2,3,4,5,10,11,12])
		var teaching := Courses.set_mode(after,0,true)
		var plan := Courses.assign_course(teaching["after"],0,11)
		assert_true(plan["supported"])
		assert_false(Courses.settle(plan["after"])["supported"])
		var chosen := Adventures.select(after,opened["ledger_after"],17)
		var prepared := Adventures.prepare(chosen["after"],opened["ledger_after"])
		assert_true(prepared["supported"])
		assert_false(Adventures.submit(chosen["after"],opened["ledger_after"])["supported"])
		assert_true(Return.move_member(after,{"kind":"student","member_id":9,"target_group":-1,"target_slot":-1})["supported"])
