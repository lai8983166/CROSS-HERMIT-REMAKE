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
	assert_true(Calendar.story(4)["supported"])
	assert_true(Calendar.story(5)["supported"])
	assert_false(Calendar.story(6)["supported"])

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


func test_mandatory_seven_registers_both_members_before_week_settlement() -> void:
	var story := Calendar.story(4)
	assert_eq(story["pre_week"].size(),71)
	assert_eq(story["pre_week"][0]["chapter"],"030B")
	assert_eq(story["week_start"].size(),55)
	assert_eq(story["week_start"][0]["chapter"],31)
	assert_eq(story["school_entry"],[])
	var bundle := Helpers.new()._returned()
	var ledger := Adventures.initial()
	for week in [1,2,3]:
		bundle["phase"]="courses_confirmed"
		var advanced := Calendar.next_week(bundle)
		var room := Calendar.finish_story(advanced["after"])
		var opening := Calendar.school_return(room["after"],Adventures.advance(ledger,0),ledger)
		bundle=opening["after"]
		ledger=opening["ledger_after"]
	bundle["phase"]="sortie_settled"
	var saved := bundle.duplicate(true)
	assert_false(Calendar.next_week(bundle)["supported"])
	var joined := Calendar.begin_story(bundle)
	assert_true(joined["supported"],str(joined.get("reason")))
	if not joined["supported"]: return
	assert_eq(bundle,saved)
	bundle=joined["after"]
	assert_eq(bundle["school"]["week"],4)
	assert_eq(bundle["school"]["student_ids"].slice(0,6),[3,4,9,5,8,6])
	assert_eq(bundle["school"]["teacher_ids"].slice(0,3),[101,110,115])
	assert_eq(bundle["school"]["relationships"].size(),72)
	assert_false(Calendar.begin_story(bundle)["supported"])
	var advanced := Calendar.next_week(bundle)
	assert_true(advanced["supported"],str(advanced.get("reason")))
	if not advanced["supported"]: return
	assert_eq(advanced["date"],[5,5])
	var room := Calendar.finish_story(advanced["after"])
	assert_true(room["supported"],str(room.get("reason")))
	if not room["supported"]: return
	var opened := Calendar.school_return(room["after"],Adventures.advance(ledger,7),ledger)
	assert_true(opened["supported"],str(opened.get("reason")))
	if not opened["supported"]: return
	assert_eq(opened["unlocked_work_ids"],[17,18,23,27])
	bundle=opened["after"]
	assert_eq(bundle["flags"]["0x7e11a0"],1)
	assert_eq(bundle["adv_background"],6)
	assert_eq(bundle["school"]["adventure_gate"],0)
	assert_eq(bundle["school"]["lecture_active"],0)
	assert_eq(bundle["school"]["idle_teacher_ids"],[110,115])
	assert_true(bundle["school"]["idle_student_ids"].has(6))
	var school: Dictionary=bundle["school"]
	var working := Return.Session._working(school)
	working.merge({"teacher_sort_mode":2,"drag_kind":1,"drag_origin":1,"drag_group":0,
		"drag_slot":-1,"drag_id":101},true)
	var rules := Return._rules()
	var sorted := Return.Teacher.move_teacher(working,{"kind":"teacher","teacher_id":101,
		"source_group":0,"source_slot":-1,"target_group":-1,"released":true},
		Return.Session._student_profiles(school),Return.group_rules(school),
		rules["school"]["sort_rules"],Return.work_rules(school,rules))
	assert_true(sorted["supported"],str(sorted.get("reason")))
	if sorted["supported"]: assert_eq(sorted["after"]["idle_teacher_ids"],[101,115,110])
	var moved := Return.move_member(bundle,{"kind":"teacher","member_id":115,"target_group":2})
	assert_true(moved["supported"],str(moved.get("reason")))
	if not moved["supported"]: return
	moved=Return.move_member(moved["after"],{"kind":"student","member_id":6,"target_group":2,"target_slot":0})
	assert_true(moved["supported"],str(moved.get("reason")))
	if not moved["supported"]: return
	var courses := Courses.list_courses(moved["after"],2)
	assert_true(courses["supported"],str(courses.get("reason")))
	if not courses["supported"]: return
	var ids := []
	for category in courses["courses"]:
		for row in category: ids.append(row[1])
	assert_true(ids.has(23) and ids.has(27))

func test_june_registration_and_compulsory_boot_after_each_may_week_five_result() -> void:
	var story := Calendar.story(5)
	assert_eq([story["pre_week"].size(),story["week_start"].size(),story["school_entry"]],[68,58,[]])
	var may := Helpers.new()._returned()
	var ledger := Adventures.initial()
	for selection in [0,0,0,7]:
		may["phase"]="courses_confirmed" if selection==0 else "sortie_settled"
		if selection==7: may=Calendar.begin_story(may)["after"]
		var advanced := Calendar.next_week(may)
		var room := Calendar.finish_story(advanced["after"])
		var returned := Calendar.school_return(room["after"],Adventures.advance(ledger,selection),ledger)
		may=returned["after"]
		ledger=returned["ledger_after"]
	var permitted := [0]
	for entry in Adventures.available(ledger): permitted.append(entry["id"])
	assert_true(permitted.has(17))
	for id in permitted:
		var settled := may.duplicate(true)
		if id!=0: settled=Adventures.select(settled,ledger,id)["after"]
		settled["phase"]="courses_confirmed" if id==0 else "sortie_settled"
		var advanced := Calendar.next_week(settled)
		assert_true(advanced["supported"],str(advanced.get("reason")))
		if not advanced["supported"]: continue
		assert_eq(advanced["date"],[6,1])
		var joined: Dictionary=advanced["after"]
		var item_claimed: bool = settled["item_flags"][188] & 1 != 0
		assert_eq(joined["participants"].back()["equipped_items"][0],0 if item_claimed else 189)
		if not item_claimed: assert_eq(joined["item_flags"][188]&0xfff,0x303)
		assert_eq(joined["records"].slice(0,6),settled["records"])
		assert_eq(joined["counts"].slice(0,6),settled["counts"])
		var school: Dictionary=joined["school"]
		assert_eq(school["student_ids"].slice(0,7),[3,4,9,5,8,6,1])
		assert_eq(school["teacher_ids"].slice(0,3),[101,110,115])
		assert_eq(school["relationships"].size(),90)
		assert_eq(joined["records"].back()["week_records"].count(0),177)
		assert_eq(joined["counts"].back(),{"character_id":1,"count":0})
		assert_false(Return.join_chapter033(joined,Return._rules())["supported"])
		assert_false(Calendar.next_week(joined)["supported"])
		var room := Calendar.finish_story(joined)
		assert_true(room["supported"],str(room.get("reason")))
		if not room["supported"]: continue
		assert_eq([room["after"]["adv_background"],room["after"]["flags"]["0x7a55f6"],room["after"]["flags"]["0x7e11a0"]],[6,8,1])
		var submitted := Adventures.advance(ledger,id)
		assert_false(Calendar.school_return(room["after"],submitted)["supported"])
		var returned := Calendar.school_return(room["after"],submitted,ledger)
		assert_true(returned["supported"],str(returned.get("reason")))
		if not returned["supported"]: continue
		var after: Dictionary=returned["after"]
		assert_eq([after["flags"]["0x7a55f6"],after["flags"]["0x7e11a0"]],[11,0])
		assert_eq(after["newly_dated_adventures"].size(),1)
		assert_eq(returned["unlocked_work_ids"],[])
		assert_eq(after["school"]["lecture_work_fields"],[3,3,4,0])
		assert_eq(after["school"]["adventure_gate"],1)
		assert_true(after["school"]["idle_student_ids"].has(1))
		assert_true(Return.move_member(after,{"kind":"student","member_id":1,"target_group":0,"target_slot":0})["supported"])
		assert_false(Calendar.next_week(after)["supported"])

		if id==0: _june_week_two(after,returned["ledger_after"])


func _june_week_two(june: Dictionary, ledger: Dictionary) -> void:
	var story := Calendar.story(1,6)
	assert_true(story["supported"])
	assert_false(Calendar.story(4,8)["supported"])
	assert_eq(story["pre_week_join_page"],81)
	assert_eq([story["pre_week"][80]["chapter"],story["pre_week"][81]["chapter"]],[35,36])
	assert_eq([story["week_start"][78]["chapter"],story["week_start"][79]["chapter"]],[37,38])
	assert_eq(story["school_entry"].size(),128)
	var settled := june.duplicate(true)
	settled["phase"]="sortie_settled"
	assert_false(Calendar.next_week(settled)["supported"])
	var joined := Calendar.begin_story(settled)
	assert_true(joined["supported"],str(joined.get("reason")))
	if not joined["supported"]:return
	assert_eq(joined["after"]["school"]["week"],1)
	assert_eq(joined["after"]["school"]["student_ids"].slice(0,8),[3,4,9,5,8,6,1,2])
	assert_eq(joined["after"]["school"]["relationships"].size(),110)
	assert_eq(joined["after"]["records"].back()["week_records"].count(0),177)
	assert_false(Calendar.begin_story(joined["after"])["supported"])
	var advanced := Calendar.next_week(joined["after"])
	assert_true(advanced["supported"],str(advanced.get("reason")))
	if not advanced["supported"]:return
	assert_eq(advanced["date"],[6,2])
	assert_false(Calendar.next_week(advanced["after"])["supported"])
	var room := Calendar.finish_story(advanced["after"])
	assert_true(room["supported"],str(room.get("reason")))
	if not room["supported"]:return
	assert_eq([room["after"]["adv_background"],room["after"]["flags"]["0x7a55f6"],room["after"]["flags"]["0x7e11a0"]],[7,6,1])
	var submitted := Adventures.advance(ledger,4)
	assert_false(Calendar.school_return(room["after"],submitted)["supported"])
	var opened := Calendar.school_return(room["after"],submitted,ledger)
	assert_true(opened["supported"],str(opened.get("reason")))
	if not opened["supported"]:return
	var after: Dictionary=opened["after"]
	assert_eq(opened["unlocked_work_ids"],[])
	assert_eq(after["school"]["lecture_work_fields"],[3,5,6,0])
	assert_eq(after["school"]["adventure_gate"],1)
	assert_eq([after["flags"]["0x7a55f6"],after["flags"]["0x7e11a0"]],[11,0])
	assert_true(after["school"]["idle_student_ids"].has(2))
	assert_true(Return.move_member(after,{"kind":"student","member_id":2,"target_group":1,"target_slot":0})["supported"])
	assert_false(Courses.set_mode(after,0,true)["supported"])
	assert_false(Calendar.school_return(after,submitted,ledger)["supported"])

	_june_week_three(after,opened["ledger_after"])


func _june_week_three(june: Dictionary, ledger: Dictionary) -> void:
	var story := Calendar.story(2,6)
	assert_true(story["supported"])
	assert_false(story.has("pre_week_join_page"))
	assert_eq([story["pre_week"].size(),story["week_start"].size(),story["school_entry"]],[140,35,[]])
	assert_eq([story["pre_week"][74]["chapter"],story["pre_week"][75]["chapter"]],["039A",40])
	assert_eq([story["week_start"][5]["chapter"],story["week_start"][6]["chapter"]],[41,210])
	var settled := june.duplicate(true)
	settled["phase"]="sortie_settled"
	assert_false(Calendar.begin_story(settled)["supported"])
	var wrong := settled.duplicate(true)
	wrong["school"]["lecture_work_fields"]=[3,3,4,0]
	assert_false(Calendar.next_week(wrong)["supported"])
	var advanced := Calendar.next_week(settled)
	assert_true(advanced["supported"],str(advanced.get("reason")))
	if not advanced["supported"]:return
	assert_eq(advanced["date"],[6,3])
	assert_eq(advanced["after"]["school"]["student_ids"],settled["school"]["student_ids"])
	assert_eq(advanced["after"]["records"],settled["records"])
	assert_eq(advanced["after"]["counts"],settled["counts"])
	assert_false(Calendar.next_week(advanced["after"])["supported"])
	var room := Calendar.finish_story(advanced["after"])
	assert_true(room["supported"],str(room.get("reason")))
	if not room["supported"]:return
	assert_eq([room["after"]["adv_background"],room["after"]["flags"]["0x7a55f6"],room["after"]["flags"]["0x7e11a0"]],[6,16,1])
	var submitted := Adventures.advance(ledger,6)
	assert_false(Calendar.school_return(room["after"],submitted)["supported"])
	var opened := Calendar.school_return(room["after"],submitted,ledger)
	assert_true(opened["supported"],str(opened.get("reason")))
	if not opened["supported"]:return
	var after: Dictionary=opened["after"]
	assert_eq([after["flags"]["0x7a55f6"],after["flags"]["0x7e11a0"]],[16,1])
	assert_eq(after["school"]["lecture_work_fields"],[3,9,10,0])
	assert_eq(after["school"]["adventure_gate"],1)
	assert_eq([after["school"]["student_count"],after["school"]["teacher_count"]],[8,3])
	assert_eq(opened["unlocked_work_ids"],[])
	assert_true(Return.move_member(after,{"kind":"student","member_id":2,"target_group":1,"target_slot":0})["supported"])
	assert_false(Courses.set_mode(after,0,true)["supported"])
	assert_false(Calendar.school_return(after,submitted,ledger)["supported"])

	# Start at the consumed result boundary. The combat suite owns the battle trace.
	for skip in [false,true]:
		var flow := preload("res://sim/school_postbattle_flow.gd").new()
		flow.phase="sortie_result"
		flow.bundle=settled.duplicate(true)
		flow.planning={"sortie_summary":{},"ledger":submitted,"opening_ledger":ledger}
		flow._set_dated_story(story)
		assert_true(flow.execute({"op":"post_next"})["supported"])
		for stage in [["post_story",140],["new_week_story",35]]:
			assert_eq(flow.phase,stage[0])
			for i in range(1 if skip else stage[1]):
				assert_true(flow.execute({"op":"post_skip" if skip else "post_next"})["supported"])
		assert_eq(flow.phase,"post_workroom")
		assert_true(flow.execute({"op":"post_school"})["supported"])
		assert_eq(flow.phase,"returned_school")
		assert_eq(flow.bundle,after)
		assert_eq(flow.planning["ledger"],opened["ledger_after"])

	_june_week_four(after,opened["ledger_after"])


func _june_week_four(june: Dictionary, ledger: Dictionary) -> void:
	var story := Calendar.story(3,6)
	assert_true(story["supported"])
	assert_eq([story["pre_week"],story["school_entry"]],[[],[]])
	assert_eq(story["week_start"].size(),13)
	var settled := june.duplicate(true)
	settled["phase"]="sortie_settled"
	var invalid := settled.duplicate(true)
	invalid["school"]["availability"][117]=1
	assert_false(Calendar.next_week(invalid)["supported"])
	var submitted := Adventures.advance(ledger,10)
	var ending := {}
	for skip in [false,true]:
		var flow := preload("res://sim/school_postbattle_flow.gd").new()
		flow.phase="sortie_result"
		flow.bundle=settled.duplicate(true)
		flow.planning={"sortie_summary":{},"ledger":submitted,"opening_ledger":ledger}
		flow._set_dated_story(story)
		var advance := flow.execute({"op":"post_next"})
		assert_true(advance["supported"],str(advance.get("reason")))
		if not advance["supported"]:return
		assert_eq(flow.phase,"new_week_story")
		assert_eq(flow.snapshot()["page"]["chapter"],213)
		assert_eq(flow.bundle["school"]["week"],4)
		for key in ["availability","teacher_ids","raw_teacher_ids","student_ids","raw_student_ids","relationships"]:
			assert_eq(flow.bundle["school"][key],settled["school"][key])
		assert_eq(flow.bundle["records"],settled["records"])
		assert_eq(flow.bundle["counts"],settled["counts"])
		for i in range(1 if skip else 13):
			assert_true(flow.execute({"op":"post_skip" if skip else "post_next"})["supported"])
		assert_eq(flow.phase,"post_workroom")
		assert_eq([flow.bundle["adv_background"],flow.bundle["flags"]["0x7a55f6"],flow.bundle["flags"]["0x7e11a0"]],[8,9,1])
		var returned := flow.execute({"op":"post_school"})
		assert_true(returned["supported"],str(returned.get("reason")))
		if not returned["supported"]:return
		assert_eq(flow.phase,"returned_school")
		var school: Dictionary=flow.bundle["school"]
		assert_eq([school["month"],school["week"],school["lecture_work_fields"],school["adventure_gate"]],[6,4,[3,12,13,0],1])
		assert_eq([flow.bundle["flags"]["0x7a55f6"],flow.bundle["flags"]["0x7e11a0"]],[9,1])
		assert_true(Return.move_member(flow.bundle,{"kind":"student","member_id":2,"target_group":0,"target_slot":0})["supported"])
		assert_false(Courses.set_mode(flow.bundle,0,true)["supported"])
		assert_false(Calendar.next_week(flow.bundle)["supported"])
		if skip:assert_eq(flow.bundle,ending)
		ending=flow.bundle

		if skip:_june_week_five(flow.bundle,flow.planning["ledger"])


func _june_week_five(june: Dictionary, ledger: Dictionary) -> void:
	var story:=Calendar.story(4,6)
	assert_true(story["supported"])
	if not story["supported"]:return
	assert_eq([story["pre_week"],story["school_entry"]],[[],[]])
	assert_eq(story["week_start"].size(),155)
	assert_eq([story["week_start"][94]["chapter"],story["week_start"][95]["chapter"]],[42,302])
	var settled:=june.duplicate(true)
	settled["phase"]="sortie_settled"
	var submitted:=Adventures.advance(ledger,13)
	var ending:={}
	for skip in [false,true]:
		var flow:=preload("res://sim/school_postbattle_flow.gd").new()
		flow.phase="sortie_result"
		flow.bundle=settled.duplicate(true)
		flow.planning={"sortie_summary":{},"ledger":submitted,"opening_ledger":ledger}
		flow._set_dated_story(story)
		var advanced:=flow.execute({"op":"post_next"})
		assert_true(advanced["supported"],str(advanced.get("reason")))
		if not advanced["supported"]:return
		assert_eq(flow.phase,"new_week_story")
		var school: Dictionary=flow.bundle["school"]
		assert_eq([school["month"],school["week"]],[6,5])
		assert_eq(school["teacher_ids"].slice(0,4),[101,110,115,118])
		assert_eq(school["availability"][118],1)
		assert_eq(school["student_ids"],june["school"]["student_ids"])
		assert_eq(flow.bundle["records"],settled["records"])
		assert_eq(school["relationships"].size(),132)
		for i in range(1 if skip else 155):
			assert_true(flow.execute({"op":"post_skip" if skip else "post_next"})["supported"])
		assert_eq(flow.phase,"post_workroom")
		assert_eq([flow.bundle["adv_background"],flow.bundle["flags"]["0x7a55f6"],flow.bundle["flags"]["0x7e11a0"]],[8,2,1])
		var returned:=flow.execute({"op":"post_school"})
		assert_true(returned["supported"],str(returned.get("reason")))
		if not returned["supported"]:return
		school=flow.bundle["school"]
		assert_eq([school["adventure_gate"],school["lecture_active"]],[0,0])
		assert_true(school["idle_teacher_ids"].has(118))
		var unlocked: Array=[]
		for id in school["course_unlocked_flags"].size():
			if school["course_unlocked_flags"][id]!=june["school"]["course_unlocked_flags"][id]:
				unlocked.append(id)
		assert_eq(unlocked,[8,19,20,26,28,29])
		assert_eq(school["course_buffers"][17].slice(0,2).map(func(row):return row[3]),[29,28])
		assert_eq(flow.bundle["newly_dated_adventures"],[])
		assert_eq(Adventures.available(flow.planning["ledger"]).map(func(r):return r["id"]),[17])
		var move:=Return.move_member(flow.bundle,{"kind":"teacher","member_id":118,"target_group":3,"target_slot":-1})
		assert_true(move["supported"],str(move.get("reason")))
		if skip:assert_eq(flow.bundle,ending)
		ending=flow.bundle

		if skip:_july_week_one(flow.bundle,flow.planning["ledger"])


func _july_week_one(june: Dictionary, ledger: Dictionary) -> void:
	var story:=Calendar.story(5,6)
	assert_true(story["supported"])
	assert_eq([story["pre_week"],story["school_entry"]],[[],[]])
	assert_eq(story["week_start"].size(),51)
	assert_eq([story["week_start"][31]["chapter"],story["week_start"][32]["chapter"]],[303,218])
	assert_true(Adventures.valid_opening(ledger,5,6))
	var wrong:=ledger.duplicate(true)
	wrong["unlock_flags"][12]=0
	assert_false(Adventures.valid_opening(wrong,5,6))
	for course in [true,false]:
		var selected:=june.duplicate(true)
		if not course:
			var plan:=Adventures.select(june,ledger,17)
			assert_true(plan["supported"])
			selected=plan["after"]
		selected["phase"]="courses_confirmed" if course else "sortie_settled"
		var advanced:=Calendar.next_week(selected)
		assert_true(advanced["supported"],str(advanced.get("reason")))
		if not advanced["supported"]:return
		var next: Dictionary=advanced["after"]
		assert_eq([next["school"]["month"],next["school"]["week"]],[7,1])
		for key in ["availability","member_profiles","teacher_ids","student_ids","relationships"]:
			assert_eq(next["school"][key],selected["school"][key])
		assert_eq(next["records"],selected["records"])
		assert_false(Calendar.next_week(next)["supported"])
		var room:=Calendar.finish_story(next)
		assert_true(room["supported"],str(room.get("reason")))
		if not room["supported"]:return
		var work: Dictionary=room["after"]
		assert_eq([work["flags"]["0x7a55f6"],work["flags"]["0x7e11a0"],work["adv_background"]],[12,1,8])
		var submitted:=Adventures.advance(ledger,0 if course else 17)
		var boot:=Calendar.school_return(work,submitted,ledger)
		assert_true(boot["supported"],str(boot.get("reason")))
		if not boot["supported"]:return
		var opened: Dictionary=boot["ledger_after"]
		var bundle: Dictionary=boot["after"]
		var school: Dictionary=bundle["school"]
		assert_true(Adventures.valid_opening(opened,1,7))
		assert_eq(Adventures.available(opened),[{"id":18,"category":2,"remaining":1,"cooldown":0},{"id":17,"category":1,"remaining":-1,"cooldown":1}])
		assert_eq(bundle["newly_dated_adventures"].map(func(row):return row["id"]),[18])
		assert_eq(boot["unlocked_work_ids"],[])
		assert_eq(school["course_counts"],selected["school"]["course_counts"])
		assert_eq(school["adventure_gate"],0)
		assert_eq(school["lecture_active"],0 if course else 1)
		if not course:assert_eq(school["lecture_work_fields"],[1,0,17,0])
		var sidequest:=Adventures.select(bundle,opened,18)
		assert_true(sidequest["supported"])
		assert_eq(sidequest["after"]["school"]["lecture_work_fields"],[0,0,18,0])
		assert_true(Return.move_member(bundle,{"kind":"teacher","member_id":118,"target_group":3,"target_slot":-1})["supported"])
		assert_true(Adventures.prepare(sidequest["after"],opened)["supported"])
		if course:_july_two_and_three(bundle,opened)



func _july_two_and_three(july: Dictionary, ledger: Dictionary) -> void:
	var card_story:=Calendar.story(1,7)
	assert_true(card_story["supported"])
	assert_eq([card_story["pre_week"],card_story["week_start"],card_story["school_entry"]],[[],[],[]])
	var card: Dictionary=card_story["date_card"]
	assert_eq([card["position"],card["size"],card["source_rect"],card["wait_ticks"]],[[0,324],[1024,128],[0,0,1024,128],600])
	assert_eq(FileAccess.get_sha256(card["image"]),card["png_sha256"])
	var next_story:=Calendar.story(2,7)
	assert_true(next_story["supported"])
	assert_eq(next_story["week_start"].size(),52)
	assert_eq(next_story["week_start"][0]["chapter"],209)
	for selection in [0,17,18]:
		var bundle:=july.duplicate(true)
		var opening:=ledger.duplicate(true)
		for week in [1,2]:
			var adventure: int=selection if week==1 else (17 if selection==18 else 0)
			if adventure:
				var select:=Adventures.select(bundle,opening,adventure)
				assert_true(select["supported"],str(select.get("reason")))
				if not select["supported"]:return
				bundle=select["after"]
			bundle["phase"]="sortie_settled" if adventure else "courses_confirmed"
			var advanced:=Calendar.next_week(bundle)
			assert_true(advanced["supported"],str(advanced.get("reason")))
			if not advanced["supported"]:return
			var next: Dictionary=advanced["after"]
			assert_eq([next["school"]["month"],next["school"]["week"]],[7,week+1])
			for key in ["member_profiles","relationships","raw_student_ids","raw_teacher_ids","availability"]:
				assert_eq(next["school"][key],bundle["school"][key])
			var room:=Calendar.finish_story(next)
			assert_true(room["supported"],str(room.get("reason")))
			if not room["supported"]:return
			var work: Dictionary=room["after"]
			assert_eq([work["flags"]["0x7a55f6"],work["flags"]["0x7e11a0"],work["adv_background"]],[3,0,2] if week==1 else [17,1,8])
			var submitted:=Adventures.advance(opening,adventure)
			var boot:=Calendar.school_return(work,submitted,opening)
			assert_true(boot["supported"],str(boot.get("reason")))
			if not boot["supported"]:return
			bundle=boot["after"]
			opening=boot["ledger_after"]
			assert_eq(boot["unlocked_work_ids"],[])
			assert_eq([bundle["flags"]["0x7a55f6"],bundle["flags"]["0x7e11a0"]],[3,1] if week==1 else [17,1])
			assert_eq(Adventures.available(opening).map(func(r):return r["id"]),[17] if week==1 else [9,17])
			assert_false(Adventures.select(bundle,opening,18)["supported"])
			if week==1:
				assert_eq(bundle["school"]["adventure_gate"],0)
				assert_eq(bundle["school"]["lecture_active"],1 if selection==17 else 0)
			else:
				assert_eq(bundle["school"]["adventure_gate"],1)
				assert_eq(bundle["school"]["lecture_work_fields"],[3,8,9,0])
				assert_eq(bundle["newly_dated_adventures"].map(func(r):return r["id"]),[9])
				assert_false(Calendar.story(4,8)["supported"])
				if selection==18:_july_week_four(bundle,opening)


func _july_week_four(school: Dictionary, ledger: Dictionary) -> void:
	var story:=Calendar.story(3,7)
	assert_true(story["supported"])
	if not story["supported"]:return
	assert_eq([story["pre_week"],story["school_entry"]],[[],[]])
	assert_eq(story["week_start"].size(),30)
	assert_eq(story["date_card"]["source"],"data/adv/bin/tc0704.bin")
	assert_eq(FileAccess.get_sha256(story["date_card"]["image"]),story["date_card"]["png_sha256"])
	var settled:=school.duplicate(true)
	settled["phase"]="courses_confirmed"
	assert_false(Calendar.next_week(settled)["supported"])
	settled["phase"]="sortie_settled"
	var wrong:=settled.duplicate(true)
	wrong["school"]["lecture_work_fields"]=[1,0,17,0]
	assert_false(Calendar.next_week(wrong)["supported"])
	var advanced:=Calendar.next_week(settled)
	assert_true(advanced["supported"],str(advanced.get("reason")))
	if not advanced["supported"]:return
	var next: Dictionary=advanced["after"]
	assert_eq([next["school"]["month"],next["school"]["week"]],[7,4])
	for key in ["availability","member_profiles","teacher_ids","student_ids","relationships"]:
		assert_eq(next["school"][key],settled["school"][key])
	var room:=Calendar.finish_story(next)
	assert_true(room["supported"],str(room.get("reason")))
	if not room["supported"]:return
	var work: Dictionary=room["after"]
	assert_eq([work["flags"]["0x7a55f6"],work["flags"]["0x7e11a0"],work["adv_background"]],[10,1,8])
	var boot:=Calendar.school_return(work,Adventures.advance(ledger,9),ledger)
	assert_true(boot["supported"],str(boot.get("reason")))
	if not boot["supported"]:return
	var after: Dictionary=boot["after"]
	assert_eq(Adventures.available(boot["ledger_after"]).map(func(r):return r["id"]),[14,17])
	assert_eq(boot["unlocked_work_ids"],[])
	assert_eq(after["newly_dated_adventures"].map(func(r):return r["id"]),[14])
	assert_eq([after["school"]["lecture_active"],after["school"]["adventure_gate"],after["school"]["lecture_work_fields"]],[1,1,[3,13,14,0]])
	assert_false(Adventures.select(after,boot["ledger_after"],17)["supported"])
	assert_true(Return.move_member(after,{"kind":"teacher","member_id":118,"target_group":3,"target_slot":-1})["supported"])

	var flow:=preload("res://sim/school_postbattle_flow.gd").new()
	flow.bundle=settled.duplicate(true)
	flow.phase="sortie_result"
	flow.planning={"sortie_summary":{},"ledger":Adventures.advance(ledger,9),"opening_ledger":ledger}
	flow._set_dated_story(story)
	assert_true(flow.execute({"op":"post_next"})["supported"])
	assert_eq(flow.phase,"new_week_story")
	var card:=flow.snapshot()
	assert_eq([card["total"],card["page"],card["date_card"]],[0,{},story["date_card"]])
	assert_true(flow.execute({"op":"post_next"})["supported"])
	for i in range(30):
		var view:=flow.snapshot()
		assert_eq(view["page"],story["week_start"][i])
		assert_eq([view["total"],view["cursor"],view.has("date_card")],[30,i,false])
		assert_true(flow.execute({"op":"post_next"})["supported"])
	assert_eq(flow.phase,"post_workroom")
	assert_true(flow.execute({"op":"post_school"})["supported"])
	assert_eq(flow.phase,"returned_school")
	assert_eq(flow.bundle,after)

	_july_week_five(after,boot["ledger_after"])


func _july_week_five(school: Dictionary,ledger: Dictionary) -> void:
	var story:=Calendar.story(4,7)
	assert_true(story.supported)
	if not story.supported:return
	assert_eq([story.pre_week.size(),story.week_start.size(),story.school_entry],[70,21,[]])
	var flow:=preload("res://sim/school_postbattle_flow.gd").new()
	flow.bundle=school.duplicate(true)
	flow.bundle.phase="sortie_settled"
	var wrong:=flow.bundle.duplicate(true)
	wrong.school.lecture_work_fields=[1,0,17,0]
	assert_false(Calendar.begin_story(wrong).supported)
	assert_false(Calendar.next_week(flow.bundle).supported)
	flow.phase="sortie_result"
	flow.planning={"sortie_summary":{},"ledger":Adventures.advance(ledger,14),"opening_ledger":ledger}
	flow._set_dated_story(story)
	assert_true(flow.execute({"op":"post_next"}).supported)
	assert_eq(flow.phase,"post_story")
	assert_eq(flow.bundle.school.student_ids.slice(8,10),[16,17])
	assert_eq(flow.bundle.school.relationships.size(),14*13)
	assert_eq(flow.bundle.participants.size(),10)
	assert_eq(flow.bundle.records.size(),10)
	assert_false(Calendar.begin_story(flow.bundle).supported)
	for page in story.pre_week:
		assert_eq(flow.snapshot().page,page)
		var result: Dictionary=flow.execute({"op":"post_next"})
		assert_true(result.supported,str(result))
		if not result.supported:return
	assert_eq(flow.snapshot().date_card,story.date_card)
	assert_eq([flow.bundle.school.month,flow.bundle.school.week],[7,5])
	assert_true(flow.execute({"op":"post_next"}).supported)
	for page in story.week_start:
		assert_eq(flow.snapshot().page,page)
		assert_true(flow.execute({"op":"post_next"}).supported)
	assert_eq(flow.phase,"post_workroom")
	assert_eq([flow.bundle.flags["0x7a55f6"],flow.bundle.flags["0x7e11a0"],flow.bundle.adv_background],[9,1,122])
	var boot: Dictionary=flow.execute({"op":"post_school"})
	assert_true(boot.supported,str(boot))
	if not boot.supported:return
	assert_eq(flow.bundle.newly_dated_adventures,[])
	assert_eq(Adventures.available(flow.planning.ledger).map(func(r):return r.id),[17])
	assert_eq(flow.bundle.school.adventure_gate,0)
	assert_eq(flow.bundle.school.lecture_active,0)
	assert_eq(flow.bundle.school.course_unlocked_flags,school.school.course_unlocked_flags)
	for id in [16,17]:
		assert_true(id in flow.bundle.school.idle_student_ids)
		var moved: Dictionary=flow.execute({"op":"return_move","kind":"student","member_id":id,"target_group":0,"target_slot":3})
		assert_true(moved.supported,str(moved))
		if moved.supported:assert_eq(flow.bundle.school.derived_student_ids[0][3],id)

	_august_week_one(flow.bundle,flow.planning.ledger)


func _august_week_one(school: Dictionary, ledger: Dictionary) -> void:
	var story:=Calendar.story(5,7)
	assert_true(story.supported)
	if not story.supported:return
	assert_eq([story.pre_week,story.week_start,story.school_entry],[[],[],[]])
	assert_eq(story.date_card.source,"data/adv/bin/tc0801.bin")
	var selected:=Adventures.select(school,ledger,17)
	assert_true(selected.supported,str(selected))
	if not selected.supported:return
	for course in [true,false]:
		var flow:=preload("res://sim/school_postbattle_flow.gd").new()
		flow.bundle=(school if course else selected.after).duplicate(true)
		var before: Dictionary=flow.bundle.school.duplicate(true)
		flow.bundle.phase="courses_confirmed" if course else "sortie_settled"
		flow.phase="course_result" if course else "sortie_result"
		flow.planning={"ledger":Adventures.advance(ledger,0 if course else 17),"opening_ledger":ledger}
		if course:flow.planning.course_summary={}
		else:
			flow.planning.sortie_summary={}
			flow._set_dated_story(story)
			var wrong:=flow.bundle.duplicate(true)
			wrong.school.lecture_work_fields=[0,0,18,0]
			assert_false(Calendar.next_week(wrong).supported)
		var advanced: Dictionary=flow.execute({"op":"course_story" if course else "post_next"})
		assert_true(advanced.supported,str(advanced))
		if not advanced.supported:return
		var card:=flow.snapshot()
		assert_eq([flow.phase,card.page,card.total,card.date_card],["new_week_story",{},0,story.date_card])
		assert_eq([flow.bundle.school.month,flow.bundle.school.week],[8,1])
		assert_true(flow.execute({"op":"post_skip" if course else "post_next"}).supported)
		assert_eq([flow.phase,flow.bundle.adv_background,flow.bundle.flags["0x7a55f6"],flow.bundle.flags["0x7e11a0"]],["post_workroom",122,9,0])
		var boot: Dictionary=flow.execute({"op":"post_school"})
		assert_true(boot.supported,str(boot))
		if not boot.supported:return
		assert_eq(flow.phase,"returned_school")
		assert_eq([flow.bundle.flags["0x7a55f6"],flow.bundle.flags["0x7e11a0"]],[9,1])
		for key in ["availability","teacher_ids","student_ids","member_profiles","relationships","course_unlocked_flags","derived_student_ids"]:
			assert_eq(flow.bundle.school[key],before[key])
		assert_eq([flow.bundle.school.adventure_gate,flow.bundle.newly_dated_adventures],[0,[]])
		assert_eq(Adventures.available(flow.planning.ledger).map(func(r):return r.id),[17])
		if not course:assert_eq([flow.bundle.school.lecture_active,flow.bundle.school.lecture_work_fields],[1,[1,0,17,0]])
		assert_true(Return.move_member(flow.bundle,{"kind":"student","member_id":16,"target_group":0,"target_slot":3}).supported)

		if course:_august_week_two(flow.bundle,flow.planning.ledger)


func _august_week_two(school: Dictionary,ledger: Dictionary) -> void:
	var story:=Calendar.story(1,8)
	assert_true(story.supported)
	if not story.supported:return
	assert_eq([story.pre_week,story.school_entry,story.week_start.size()],[[],[],6])
	assert_eq(story.date_card.source,"data/adv/bin/tc0802.bin")
	var flow:=preload("res://sim/school_postbattle_flow.gd").new()
	flow.bundle=school.duplicate(true)
	flow.bundle.phase="courses_confirmed"
	flow.phase="course_result"
	flow.planning={"course_summary":{},"ledger":Adventures.advance(ledger,0),"opening_ledger":ledger}
	var advanced: Dictionary=flow.execute({"op":"course_story"})
	assert_true(advanced.supported,str(advanced))
	if not advanced.supported:return
	assert_eq([flow.bundle.school.month,flow.bundle.school.week,flow.phase],[8,2,"new_week_story"])
	assert_eq(flow.snapshot().date_card,story.date_card)
	assert_true(flow.execute({"op":"post_next"}).supported)
	for page in story.week_start:
		assert_eq(flow.snapshot().page,page)
		assert_true(flow.execute({"op":"post_next"}).supported)
	assert_eq([flow.phase,flow.bundle.flags["0x7a55f6"],flow.bundle.flags["0x7e11a0"],flow.bundle.adv_background],["post_workroom",5,1,122])
	var boot: Dictionary=flow.execute({"op":"post_school"})
	assert_true(boot.supported,str(boot))
	if not boot.supported:return
	var result: Dictionary=flow.bundle.school
	assert_eq([result.lecture_work_fields,result.lecture_active,result.adventure_gate],[[3,19,20,0],1,1])
	assert_eq(flow.bundle.newly_dated_adventures.map(func(r):return r.id),[20])
	assert_eq(Adventures.available(flow.planning.ledger).map(func(r):return r.id),[20,17])
	assert_false(Adventures.select(flow.bundle,flow.planning.ledger,17).supported)
	for key in ["student_ids","teacher_ids","derived_student_ids","course_unlocked_flags","relationships"]:
		assert_eq(result[key],school.school[key])
	assert_true(Return.move_member(flow.bundle,{"kind":"student","member_id":17,"target_group":1,"target_slot":2}).supported)
	assert_false(Calendar.next_week(flow.bundle).supported)
	_august_week_three(flow.bundle,flow.planning.ledger)


func _august_week_three(school: Dictionary,ledger: Dictionary) -> void:
	var story:=Calendar.story(2,8)
	assert_true(story.supported)
	if not story.supported:return
	assert_eq([story.pre_week,story.school_entry,story.week_start.size()],[[],[],34])
	assert_eq(story.date_card.source,"data/adv/bin/tc0803.bin")
	var flow:=preload("res://sim/school_postbattle_flow.gd").new()
	flow.bundle=school.duplicate(true)
	flow.bundle.phase="sortie_settled"
	flow.phase="sortie_result"
	flow.planning={"sortie_summary":{},"ledger":Adventures.advance(ledger,20),"opening_ledger":ledger}
	flow._set_dated_story(story)
	var wrong:=flow.bundle.duplicate(true)
	wrong.phase="courses_confirmed"
	assert_false(Calendar.next_week(wrong).supported)
	wrong.phase="sortie_settled"
	wrong.school.lecture_work_fields=[1,0,17,0]
	assert_false(Calendar.next_week(wrong).supported)
	var advanced:=flow.execute({"op":"post_next"})
	assert_true(advanced.supported,str(advanced))
	if not advanced.supported:return
	assert_eq([flow.bundle.school.month,flow.bundle.school.week,flow.phase],[8,3,"new_week_story"])
	assert_eq(flow.snapshot().date_card,story.date_card)
	assert_true(flow.execute({"op":"post_next"}).supported)
	for page in story.week_start:
		assert_eq(flow.snapshot().page,page)
		assert_true(flow.execute({"op":"post_next"}).supported)
	assert_eq([flow.phase,flow.bundle.flags["0x7a55f6"],flow.bundle.flags["0x7e11a0"],flow.bundle.adv_background],["post_workroom",12,1,122])
	var boot:=flow.execute({"op":"post_school"})
	assert_true(boot.supported,str(boot))
	if not boot.supported:return
	var result: Dictionary=flow.bundle.school
	assert_eq([result.lecture_work_fields,result.lecture_active,result.adventure_gate],[[3,20,21,0],1,1])
	assert_eq(flow.bundle.newly_dated_adventures.map(func(r):return r.id),[21])
	assert_eq(Adventures.available(flow.planning.ledger).map(func(r):return r.id),[21,17])
	assert_false(Adventures.select(flow.bundle,flow.planning.ledger,17).supported)
	for key in ["student_ids","teacher_ids","derived_student_ids","course_unlocked_flags","relationships"]:
		assert_eq(result[key],school.school[key])
	assert_true(Return.move_member(flow.bundle,{"kind":"student","member_id":17,"target_group":1,"target_slot":2}).supported)
	_august_week_four(flow.bundle,flow.planning.ledger)


func _august_week_four(school: Dictionary, ledger: Dictionary) -> void:
	var story:=Calendar.story(3,8)
	assert_true(story.supported)
	if not story.supported:return
	assert_eq([story.pre_week.size(),story.week_start,story.school_entry.size()],[79,[],38])
	assert_eq([story.pre_week[39].chapter,story.pre_week[40].chapter,story.school_entry[0].chapter],["043A",45,306])
	assert_eq(story.date_card.source,"data/adv/bin/tc0804.bin")
	var before:=school.duplicate(true)
	before.phase="sortie_settled"
	var wrong:=before.duplicate(true)
	wrong.school.lecture_work_fields=[3,19,20,0]
	assert_false(Calendar.next_week(wrong).supported)
	var advanced:=Calendar.next_week(before)
	assert_true(advanced.supported,str(advanced.get("reason")))
	if not advanced.supported:return
	assert_eq([advanced.after.school.month,advanced.after.school.week],[8,4])
	var room:=Calendar.finish_story(advanced.after)
	assert_true(room.supported,str(room.get("reason")))
	if not room.supported:return
	assert_eq([room.after.flags["0x7a55f6"],room.after.flags["0x7e11a0"],room.after.adv_background],[4,0,14])
	var worn:=Adventures.advance(ledger,21)
	assert_false(Calendar.school_return(room.after,worn,ledger).supported)
	var entry:=Calendar.begin_school_entry(room.after)
	assert_true(entry.supported,str(entry.get("reason")))
	if not entry.supported:return
	assert_eq(entry.joined_ids,[116,13])
	assert_eq([entry.after.school.teacher_count,entry.after.school.student_count],[5,11])
	assert_eq([entry.after.school.teacher_ids[4],entry.after.school.student_ids[10]],[116,13])
	assert_eq(entry.after.school.relationships.size(),16*15)
	assert_false(Calendar.begin_school_entry(entry.after).supported)
	var boot:=Calendar.school_return(entry.after,worn,ledger)
	assert_true(boot.supported,str(boot.get("reason")))
	if not boot.supported:return
	assert_eq(boot.unlocked_work_ids,[30,33])
	var bundle: Dictionary=boot.after
	assert_eq([bundle.school.lecture_active,bundle.school.adventure_gate,bundle.newly_dated_adventures],[0,0,[]])
	assert_eq([bundle.flags["0x7a55f6"],bundle.flags["0x7e11a0"],bundle.adv_background],[4,1,14])
	assert_eq(Adventures.available(boot.ledger_after).map(func(r):return r.id),[17])
	assert_true(bundle.school.idle_teacher_ids.has(116) and bundle.school.idle_student_ids.has(13))
	var moved:=Return.move_member(bundle,{"kind":"teacher","member_id":116,"target_group":4})
	assert_true(moved.supported,str(moved.get("reason")))
	if not moved.supported:return
	moved=Return.move_member(moved.after,{"kind":"student","member_id":13,"target_group":4,"target_slot":0})
	assert_true(moved.supported,str(moved.get("reason")))
	if moved.supported:
		assert_eq(moved.after.school.derived_student_ids[4][0],13)
		var list:=Courses.list_courses(moved.after,4)
		assert_true(list.supported,str(list.get("reason")))
		if list.supported:assert_true(list.courses[0].any(func(row):return row[1]==33))
	assert_false(Calendar.story(4,8).supported)
	assert_false(Calendar.next_week(bundle).supported)
