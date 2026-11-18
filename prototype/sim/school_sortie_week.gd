extends RefCounted
## May 1 course or sortie result, CH003, state 7, CH001, workroom and school boot.
const Return := preload("res://sim/school_postbattle_return.gd")
const Week := preload("res://sim/week_settlement_replay.gd")
const Roles := preload("res://sim/all_result_role_replay.gd")
const Courses := preload("res://sim/school_course_unlocking.gd")
const Adventures := preload("res://sim/school_return_adventures.gd")
const PATH := "res://data/school_sortie_week_story.json"
const SHA := "eb886bac32bb4b98652b37490277c56144a6dbda105730ac59beb5dbb1328175"


static func story() -> Dictionary:
	var raw := FileAccess.get_file_as_string(PATH).replace("\r\n","\n")
	if raw.sha256_text()!=SHA:
		return {"supported":false,"reason":"sortie_week_story_changed"}
	var data: Dictionary = Roles._integers(JSON.parse_string(raw))
	return {"supported":true,"pre_week":data["scenes"][0]["pages"],
		"week_start":data["scenes"][1]["pages"],"school_entry":[]}


static func next_week(before: Dictionary) -> Dictionary:
	var rules := Return._rules()
	var course: bool = before.get("phase")=="courses_confirmed"
	var reason := _guard(before,1,"courses_confirmed" if course else "sortie_settled",rules)
	if not reason.is_empty(): return {"supported":false,"reason":reason}
	var result := Week.project(Return._week_input(before),rules["week"])
	if not result["supported"]: return result
	var after := before.duplicate(true)
	var advanced: Dictionary = result["after"]
	after["school"]["month"] = advanced["month"]
	after["school"]["week"] = advanced["week"]
	for key in ["participants","flags","item_flags"]: after[key] = advanced[key]
	for row in after["growth"]:
		var participant := Return._find(after["participants"],row["character_id"])
		for key in Return.GROWTH_KEYS:
			row[key] = participant[key].duplicate(true) if participant[key] is Array else participant[key]
	after["phase"] = "course_week_advanced" if course else "sortie_week_advanced"
	return Return._result(after,after["phase"],{"date":[5,2],"week_executed":true})


static func finish_story(before: Dictionary) -> Dictionary:
	var course: bool = before.get("phase")=="course_week_advanced"
	var reason := _guard(before,2,"course_week_advanced" if course else "sortie_week_advanced",Return._rules())
	if not reason.is_empty(): return {"supported":false,"reason":reason}
	var after := before.duplicate(true)
	# Chapter024 ends with op151 [16,1], op91 [8,2] and END to task8.
	after["flags"]["0x7a55f6"] = 16
	after["flags"]["0x7e11a0"] = 1
	after["adv_background"] = 8
	after["phase"] = "course_workroom" if course else "sortie_workroom"
	return Return._result(after,after["phase"])


static func school_return(before: Dictionary, ledger: Dictionary) -> Dictionary:
	var rules := Return._rules()
	var course: bool = before.get("phase")=="course_workroom"
	var reason := _guard(before,2,"course_workroom" if course else "sortie_workroom",rules)
	if not reason.is_empty(): return {"supported":false,"reason":reason}
	var id: int = before["school"]["lecture_work_fields"][2]
	var initial := Adventures.initial()
	if initial.is_empty() or (not course and id not in [8,17]) or ledger!=Adventures.advance(initial,0 if course else id):
		return {"supported":false,"reason":"invalid_sortie_week_ledger"}
	var opened := ledger.duplicate(true)
	Adventures._open(opened,5,2,Adventures.rules())
	var unlocked := Courses.unlock_courses(before["school"],rules["school"]["course_rules"])
	if not unlocked["supported"]: return unlocked
	var after := before.duplicate(true)
	after["phase"] = "school_returned"
	after["school"] = unlocked["after"]
	after["school"]["adventure_gate"] = 0
	# 4A5CE0 preserves the previous selection only while it remains available.
	if after["school"]["lecture_active"]==1:
		if Adventures.available(opened).any(func(row):return row["id"]==id):
			var selected := Adventures.select(after,opened,id)
			if not selected["supported"]: return selected
			after["school"] = selected["after"]["school"]
		else:
			after["school"]["lecture_active"] = 0
	var prepared := Return._prepare(after["school"],rules)
	if not prepared["supported"]: return prepared
	after["school"] = prepared["after"]
	after["ratings"] = prepared["ratings"]
	after["rankings"] = Return._rankings(after["school"])
	after["flags"]["0x7a55fa"] = 0
	after["flags"]["0x7a4e62"] = 1
	# CH002(5/2) jumps directly to END; music and background retain Chapter024's values.
	after["newly_dated_adventures"] = []
	return Return._result(after,"school_returned",{"ledger_after":opened,"unlocked_work_ids":unlocked["unlocked_work_ids"]})


static func _guard(before: Dictionary, week: int, phase: String, rules: Dictionary) -> String:
	if rules.is_empty(): return "invalid_sortie_week_sources"
	if before.get("phase")!=phase: return "unexpected_sortie_week_phase"
	return Return._validate(before,[3,4,9,5],5,week,rules)
