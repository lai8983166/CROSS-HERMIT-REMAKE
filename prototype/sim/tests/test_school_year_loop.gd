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
	assert_false(year.has_departure(11,2))
