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
		assert_true(Courses.settle(plan["after"])["supported"])
		var chosen := Adventures.select(after,opened["ledger_after"],17)
		var prepared := Adventures.prepare(chosen["after"],opened["ledger_after"])
		assert_true(prepared["supported"])
		assert_true(Adventures.submit(chosen["after"],opened["ledger_after"])["supported"])
		assert_true(Return.move_member(after,{"kind":"student","member_id":9,"target_group":-1,"target_slot":-1})["supported"])


func test_may_week3_chapter_chain_and_carried_planning_state() -> void:
	var story := Calendar.story(2)
	assert_true(story["supported"])
	assert_eq(story["pre_week"].size(),20)
	assert_eq(story["week_start"].size(),336)
	assert_eq(story["week_start"][102]["chapter"],26)
	assert_eq(story["week_start"][103]["chapter"],27)
	assert_eq(story["school_entry"],[])
	assert_true(Calendar.story(3)["supported"])
	assert_false(Calendar.story(4)["supported"])

	var initial := Adventures.initial()
	var original := Helpers.new()._returned()
	for first in [0,8,17]:
		var source: Dictionary = original.duplicate(true)
		if first!=0:
			source = Adventures.select(source,initial,first)["after"]
		source["phase"] = "courses_confirmed" if first==0 else "sortie_settled"
		var w2 := Calendar.next_week(source)
		var room2 := Calendar.finish_story(w2["after"])
		var opened2 := Calendar.school_return(room2["after"],Adventures.advance(initial,first))
		var ledger: Dictionary = opened2["ledger_after"]
		var selections := [0]
		for entry in Adventures.available(ledger): selections.append(entry["id"])
		for second in selections:
			var settled: Dictionary = opened2["after"].duplicate(true)
			if second!=0: settled = Adventures.select(settled,ledger,second)["after"]
			settled["phase"] = "courses_confirmed" if second==0 else "sortie_settled"
			var advanced := Calendar.next_week(settled)
			assert_true(advanced["supported"],str(advanced.get("reason")))
			if not advanced["supported"]: continue
			assert_eq(advanced["date"],[5,3])
			var room := Calendar.finish_story(advanced["after"])
			assert_true(room["supported"],str(room.get("reason")))
			if not room["supported"]: continue
			assert_eq(room["after"]["flags"]["0x7e11a0"],0)
			var submitted := Adventures.advance(ledger,second)
			assert_false(Calendar.school_return(room["after"],submitted)["supported"])
			assert_false(Calendar.school_return(room["after"],submitted,initial)["supported"])
			assert_false(Calendar.school_return(room["after"],ledger,ledger)["supported"])
			var opened := Calendar.school_return(room["after"],submitted,ledger)
			assert_true(opened["supported"],str(opened.get("reason")))
			if not opened["supported"]: continue
			var after: Dictionary = opened["after"]
			assert_eq(opened["ledger_after"],submitted)
			assert_eq(after["records"],settled["records"])
			assert_eq(after["counts"],settled["counts"])
			assert_eq(after["flags"]["0x7a55f6"],11)
			assert_eq(after["flags"]["0x7e11a0"],1)
			assert_eq(opened["unlocked_work_ids"],[6,7])
			var listed := Courses.list_courses(after,0)
			assert_true(listed["supported"])
			if not listed["supported"]: continue
			var ids := []
			for category in listed["courses"]:
				for row in category: ids.append(row[1])
			ids.sort()
			assert_eq(ids,[1,2,3,4,5,6,7,10,11,12])
			assert_true(Return.move_member(after,{"kind":"student","member_id":9,"target_group":-1,"target_slot":-1})["supported"])
			var teaching := Courses.set_mode(after,0,true)
			var planned := Courses.assign_course(teaching["after"],0,7)
			assert_true(planned["supported"])
			if planned["supported"]: assert_true(Courses.settle(planned["after"])["supported"])
