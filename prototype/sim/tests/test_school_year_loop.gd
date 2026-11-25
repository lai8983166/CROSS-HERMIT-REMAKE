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
