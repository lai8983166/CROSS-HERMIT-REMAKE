extends "res://sim/tests/test_base.gd"
const Week := preload("res://sim/week_settlement_replay.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")


func test_thirty_calendar_positions_against_original_week_settlement() -> void:
	var path := "res://data/week_settlement_evidence.json"
	var raw := FileAccess.get_file_as_string(path).replace("\r\n","\n")
	var checks: Dictionary = Roles._integers(JSON.parse_string(FileAccess.get_file_as_string(
		"res://data/school_year_calendar_checkpoints.json")))
	assert_eq(raw.sha256_text(),checks.parent_sha256)
	var parent: Dictionary = Roles._integers(JSON.parse_string(raw))
	var state: Dictionary = parent.cases.filter(func(c):return c.name==checks.parent_case)[0].before
	state.month=checks.start_date[0]
	state.week=checks.start_date[1]
	assert_eq(checks.checkpoints.size(),30)
	for point in checks.checkpoints:
		var advanced := Week.project(state,parent.rules)
		assert_true(advanced.supported,str(advanced.get("reason")))
		if not advanced.supported:return
		state=advanced.after
		assert_eq([state.month,state.week],point.date)
		assert_eq(JSON.stringify(state,"",true).sha256_text(),point.state_sha256,str(point.date))


func test_job_selection_matches_original_personal_screen() -> void:
	var job_menu := preload("res://sim/school_job_eligibility.gd")
	var menu: Dictionary = Roles._integers(job_menu.menu_data())
	assert_false(menu.is_empty())
	if menu.is_empty():return
	for probe in menu.lookup_probes:
		var student := {"character_id":probe.member,"unlock_flags":probe.flags}
		assert_eq(job_menu.calculate_eligibility(student,menu),probe.selectable_jobs)


func test_job_change_equipment_against_original() -> void:
	var eligibility := preload("res://sim/school_job_eligibility.gd")
	var rules := eligibility.equipment_rules()
	assert_false(rules.is_empty())
	if rules.is_empty():return
	var observed: Dictionary=rules.case.before.duplicate(true)
	eligibility.apply_equipment(observed,observed.item_flags,rules.case.target,rules)
	assert_eq(observed,rules.case.after)

func test_autumn_calendar_uses_dated_school_events() -> void:
	var year := preload("res://sim/school_year_loop.gd")
	var expected := [[10,2,10,3,11,0,9,11],[10,3,10,4,11,0,14,11],
		[10,4,10,5,11,0,15,11],[10,5,11,1,19,1,15,4],[11,1,11,2,11,0,50,11]]
	for row in expected:
		var route := year.story(row[0],row[1])
		assert_true(route.supported)
		if not route.supported:return
		assert_false(route.pre_week.is_empty())
		assert_eq(not route.school_entry.is_empty(),row[2]==11 and row[3]==1)
		var state := {"school":{"month":row[2],"week":row[3]},"flags":{}}
		assert_true(year.apply_arrival_effects(state,false))
		assert_eq([state.flags["0x7a55f6"],state.flags["0x7e11a0"],state.adv_background],row.slice(4,7))
		assert_true(year.apply_arrival_effects(state,true))
		assert_eq([state.flags["0x7a55f6"],state.flags["0x7e11a0"]],[row[7],1])
	assert_false(year.has_departure(11,3))


func test_november_three_requires_departure_before_story_completion() -> void:
	var year := preload("res://sim/school_year_loop.gd")
	var adventures := preload("res://sim/school_return_adventures.gd")
	var route := year.story(11,2)
	assert_true(route.supported)
	if not route.supported:return
	assert_eq(route.pre_week,[])
	assert_eq(route.school_entry,[])
	assert_eq(route.week_start.size(),152)
	assert_eq(route.week_start[0].chapter,71)
	var state := {"school":{"month":11,"week":3},"flags":{}}
	assert_false(year.apply_arrival_effects(state,false))
	state.chapter071_absent={"participants":{"character_id":2}}
	assert_true(year.apply_arrival_effects(state,false))
	assert_eq([state.flags["0x7a55f6"],state.flags["0x7e11a0"],state.adv_background],[2,1,10])
	assert_eq(adventures._mandatory_id(11,2),0)
	assert_eq(adventures._mandatory_id(11,3),41)


func test_november_five_starts_after_student_four_leaves() -> void:
	var year := preload("res://sim/school_year_loop.gd")
	var route := year.story(11,4)
	assert_true(route.supported)
	if not route.supported:return
	assert_eq([route.pre_week,route.school_entry,route.week_start.size()],[[],[],122])
	assert_eq(route.week_start[0].chapter,76)
	var state := {"school":{"month":11,"week":5},"flags":{}}
	assert_false(year.apply_arrival_effects(state,false))
	state.chapter076_absent={"participants":{"character_id":2}}
	assert_false(year.apply_arrival_effects(state,false))
	state.chapter076_absent.participants.character_id=4
	assert_true(year.apply_arrival_effects(state,false))
	assert_eq([state.flags["0x7a55f6"],state.flags["0x7e11a0"],state.adv_background],[11,0,10])
	assert_true(year.apply_arrival_effects(state,true))
	assert_eq([state.flags["0x7a55f6"],state.flags["0x7e11a0"]],[11,1])


func test_december_one_route_and_mandatory_adventure() -> void:
	var year := preload("res://sim/school_year_loop.gd")
	var adventures := preload("res://sim/school_return_adventures.gd")
	var route := year.story(11,5)
	assert_true(route.supported)
	if not route.supported:return
	assert_eq([route.pre_week.size(),route.pre_week[0].chapter],[56,77])
	assert_eq(route.week_start,[])
	assert_eq(route.date_card.source,"data/adv/bin/tc1201.bin")
	assert_eq([route.school_entry.size(),route.school_entry[0].chapter],[27,231])
	var state := {"school":{"month":12,"week":1},"flags":{}}
	assert_true(year.apply_arrival_effects(state,false))
	assert_eq([state.flags["0x7a55f6"],state.flags["0x7e11a0"],state.adv_background],[9,0,15])
	assert_true(year.apply_arrival_effects(state,true))
	assert_eq([state.flags["0x7a55f6"],state.flags["0x7e11a0"]],[9,1])
	assert_eq(adventures._mandatory_id(11,5),0)
	assert_eq(adventures._mandatory_id(12,1),31)


func test_loop_phase_guards_preserve_order_and_reject_duplicate_transactions() -> void:
	var loop := preload("res://sim/school_year_loop.gd")
	for row in [["returned_school","planning","return_depart"],["sortie_pending","execution","sortie_finish"],
			["sortie_result","settlement","post_next"],["course_result","settlement","course_story"],
			["post_story","story","post_skip"],["new_week_story","next_week","post_next"],
			["post_workroom","next_week","post_school"],["chapter310_choice","story","post_choice"]]:
		assert_eq(loop.phase_for(row[0]),row[1])
		assert_true(loop.accepts(row[0],row[2]))
	assert_true(loop.accepts("returned_school","return_skill"))
	for row in [["returned_school","sortie_finish"],["sortie_result","sortie_finish"],["course_result","return_settle"],
			["chapter310_choice","post_skip"],["post_workroom","return_depart"],["school_year_complete","post_school"]]:
		assert_false(loop.accepts(row[0],row[1]))


func test_winter_choice_grades_and_march_ending_use_distinct_original_paths() -> void:
	var winter := preload("res://sim/school_winter_story.gd")
	var loop := preload("res://sim/school_year_loop.gd")
	assert_true(loop.has_departure(12,3))
	assert_eq(loop.story(12,3).choice_labels.size(),2)
	var arrival := {"school":{"month":13,"week":2},"flags":{}}
	assert_true(loop.apply_arrival_effects(arrival,false))
	assert_eq([arrival.flags["0x7a55f6"],arrival.flags["0x7e11a0"],arrival.adv_background],[2,1,15])
	assert_eq(winter.story(12,3,{}).choice_labels.size(),2)
	assert_eq(winter.story(12,3,{},[1]).choice_labels.size(),3)
	assert_eq(winter.story(12,3,{},[0]).effects[0],[])
	for i in range(3):
		assert_eq(winter.story(12,3,{},[1,i]).effects[0][0].operands,[[23],[24],[22]][i])
	for grade in range(1,6):
		var joins := []
		for e in winter.story(13,3,{13:grade}).effects[1]:
			if e.opcode==144:joins.append(e.operands[0])
		assert_eq(joins,[113,33] if grade<=3 else [113])
		joins.clear()
		for e in winter.story(13,4,{29:grade}).effects[0]:
			if e.opcode==144:joins.append(e.operands[0])
		assert_eq(joins,[10,12]+([25,31] if grade==1 else [27,29] if grade<4 else [26,30])+[112])
	var ending := winter.story(15,4,{})
	assert_true(ending.terminal)
	assert_eq(ending.pre_week[-1].chapter,"097A")
	assert_eq(winter.story(15,4,{},[],{4:7,5:7}).pre_week[-1].chapter,"097D")
	assert_eq(winter.story(15,4,{},[],{11:1,12:99}).pre_week[-1].chapter,"097K")
	assert_eq(winter.ending_member({2:-1,12:100}),1)
	assert_false(winter.departure(15,5))
